"""Generation and export pipeline."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any

from midi_beats.core.events import (
    BEATS_PER_VARIATION,
    INSTRUMENT_FILENAMES,
    EventMap,
    empty_event_map,
    merge_event_maps,
    normalize_to_bar_zero,
    shift_events,
)
from midi_beats.core.humanize import humanize_events
from midi_beats.core.midi_export import build_midi_files
from midi_beats.genres.registry import generate_pattern_for_genre, get_genre


class ExportLayout(str, Enum):
    PER_VARIATION = "per_variation"
    CONCATENATED = "concatenated"


@dataclass
class ExportConfig:
    genre: str
    output_dir: str
    num_variations: int = 5
    layout: ExportLayout = ExportLayout.PER_VARIATION
    velocity_var: int = 15
    timing_var: float = 0.02
    tempo: float | None = None
    seed_base: int | None = None
    lock_backbeat: bool = False
    skip_empty_instruments: bool = True
    write_manifest: bool = True
    verbose: bool = False


def generate_pattern(
    genre: str,
    variation_index: int = 1,
    seed_base: int | None = None,
    *,
    pattern_store=None,
):
    """TR-8 slot model: A/B/C + FILL1/FILL2 with ABAC chain."""
    config = get_genre(genre)
    kwargs = dict(variation_index=variation_index, seed_base=seed_base)
    if pattern_store is not None and genre == "house":
        kwargs["pattern_store"] = pattern_store
    return config.pattern_generator(**kwargs)


def generate_events(
    genre: str,
    variation_index: int = 1,
    seed_base: int | None = None,
    *,
    normalize: bool = True,
    pattern_store=None,
) -> EventMap:
    """Generate one ABAC chain (16 beats) from TR-8 slots."""
    pattern = generate_pattern(
        genre, variation_index, seed_base, pattern_store=pattern_store
    )
    events = pattern.to_chain_events()
    if normalize:
        events = normalize_to_bar_zero(events, 0.0)
    return events


def _humanize_seed(seed_base: int | None, variation_index: int) -> int | None:
    if seed_base is None:
        return None
    return seed_base + 10000 + variation_index


def _save_midi_files(
    midi_files: dict,
    var_output_dir: str,
    genre: str,
    variation_index: int,
    *,
    legacy_names: bool = False,
) -> dict[str, str]:
    os.makedirs(var_output_dir, exist_ok=True)
    saved: dict[str, str] = {}

    for inst, midi_obj in midi_files.items():
        name_part = INSTRUMENT_FILENAMES.get(inst, inst)
        if legacy_names:
            base_filename = f"{genre}_{inst}.mid"
        else:
            base_filename = f"{name_part}_{genre}_{variation_index}.mid"
        final_filename = base_filename
        suffix = 1
        while os.path.exists(os.path.join(var_output_dir, final_filename)):
            final_filename = f"{name_part}_{genre}_{variation_index}_{suffix}.mid"
            suffix += 1
        filepath = os.path.join(var_output_dir, final_filename)
        with open(filepath, "wb") as f:
            midi_obj.writeFile(f)
        saved[inst] = filepath

    return saved


def _write_manifest(path: str, data: dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def export_midi(
    events: EventMap,
    output_dir: str,
    genre: str,
    variation_index: int,
    tempo: float,
    *,
    skip_empty: bool = True,
    seed_base: int | None = None,
    write_manifest: bool = True,
    legacy_names: bool = False,
    pattern_meta: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Write per-instrument MIDI files for one variation."""
    midi_files = build_midi_files(events, tempo=tempo, skip_empty=skip_empty)
    saved = _save_midi_files(
        midi_files, output_dir, genre, variation_index, legacy_names=legacy_names
    )

    if write_manifest:
        manifest = {
            "genre": genre,
            "variation": variation_index,
            "tempo_bpm": tempo,
            "beats": BEATS_PER_VARIATION,
            "bars": 4,
            "structure": "ABAC",
            "seed_base": seed_base,
            "instruments": {
                inst: len(events.get(inst, [])) for inst in events
            },
            "files": saved,
        }
        if pattern_meta is not None:
            manifest.update(pattern_meta)
        _write_manifest(os.path.join(output_dir, "manifest.json"), manifest)

    return saved


def generate_midi_patterns(
    genre: str,
    output_dir: str,
    num_variations: int = 5,
    velocity_var: int = 15,
    timing_var: float = 0.02,
    tempo: float | None = None,
    seed_base: int | None = None,
    verbose: bool = False,
    *,
    layout: str | ExportLayout = ExportLayout.PER_VARIATION,
    lock_backbeat: bool = False,
    skip_empty_instruments: bool = True,
    write_manifest: bool = True,
) -> dict[int, dict[str, str]]:
    """
    Generate, humanize, and export MIDI patterns for a genre.

    Returns:
        Mapping of 1-based variation index to instrument → file path.
    """
    config = get_genre(genre)
    bpm = tempo if tempo is not None else config.default_tempo
    export_layout = (
        layout if isinstance(layout, ExportLayout) else ExportLayout(layout)
    )

    if verbose:
        print(f"Processing {config.name} patterns ({export_layout.value})...")

    saved_all: dict[int, dict[str, str]] = {}

    if export_layout == ExportLayout.CONCATENATED:
        combined = empty_event_map()
        for var in range(1, num_variations + 1):
            events = generate_events(config.name, var, seed_base)
            humanize_events(
                events,
                velocity_variation=velocity_var,
                timing_variation=timing_var,
                seed=_humanize_seed(seed_base, var),
                lock_backbeat=lock_backbeat,
            )
            merge_event_maps(combined, shift_events(events, (var - 1) * BEATS_PER_VARIATION))

        genre_dir = os.path.join(output_dir, config.name)
        os.makedirs(genre_dir, exist_ok=True)
        saved = export_midi(
            combined,
            genre_dir,
            config.name,
            variation_index=1,
            tempo=bpm,
            skip_empty=skip_empty_instruments,
            seed_base=seed_base,
            write_manifest=write_manifest,
            legacy_names=True,
        )
        saved_all[1] = saved
        if verbose:
            print(f"  concatenated ({num_variations} variations) → {genre_dir}")
            for inst, path in saved.items():
                print(f"    {inst}: {path}")
    else:
        for var in range(1, num_variations + 1):
            pattern = generate_pattern(config.name, var, seed_base)
            events = pattern.to_chain_events()
            humanize_events(
                events,
                velocity_variation=velocity_var,
                timing_variation=timing_var,
                seed=_humanize_seed(seed_base, var),
                lock_backbeat=lock_backbeat,
            )
            var_dir = os.path.join(output_dir, config.name, f"variation_{var}")
            saved = export_midi(
                events,
                var_dir,
                config.name,
                variation_index=var,
                tempo=bpm,
                skip_empty=skip_empty_instruments,
                seed_base=seed_base,
                write_manifest=write_manifest,
                pattern_meta=pattern.to_manifest_extras(),
            )
            saved_all[var] = saved
            if verbose:
                print(f"  variation {var}:")
                for inst, path in saved.items():
                    print(f"    {inst}: {path}")

    return saved_all


def export_from_config(config: ExportConfig) -> dict[int, dict[str, str]]:
    return generate_midi_patterns(
        config.genre,
        config.output_dir,
        num_variations=config.num_variations,
        velocity_var=config.velocity_var,
        timing_var=config.timing_var,
        tempo=config.tempo,
        seed_base=config.seed_base,
        verbose=config.verbose,
        layout=config.layout,
        lock_backbeat=config.lock_backbeat,
        skip_empty_instruments=config.skip_empty_instruments,
        write_manifest=config.write_manifest,
    )
