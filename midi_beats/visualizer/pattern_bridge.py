"""Rebuild DrumPattern from UI state; mutate; export."""

from __future__ import annotations

import random
from typing import Any

from midi_beats.core.events import EventMap, INSTRUMENTS
from midi_beats.core.grid import STEPS_PER_BAR, StepCell, step_grid_to_events
from midi_beats.core.mutate import MutateKind, mutate_bar
from midi_beats.core.pattern_model import (
    CHAIN_SEQUENCES,
    DrumPattern,
    SLOT_BASE,
    SLOT_VAR_B,
    SLOT_VAR_C,
    resolve_chain_preset,
)
from midi_beats.genres.base import make_rng
from midi_beats.genres.registry import generate_pattern_for_genre, get_genre
from midi_beats.library.ingest import load_default_catalog
from midi_beats.visualizer.serialize import pattern_to_ui_payload

SLOT_ALIASES = {
    "BASE": SLOT_BASE,
    "FILL1": SLOT_VAR_B,
    "FILL2": SLOT_VAR_C,
}


def _resolve_slot(name: str) -> str:
    return SLOT_ALIASES.get(name.upper(), name.upper())


def ui_grid_to_events(grid_json: dict[str, list[dict]]) -> EventMap:
    cells: dict[str, list[StepCell]] = {}
    for inst in INSTRUMENTS:
        row = grid_json.get(inst)
        if not row:
            continue
        cells[inst] = [
            StepCell(on=bool(c.get("on")), velocity=c.get("vel") or 100)
            for c in row
        ]
    return step_grid_to_events(cells, steps=STEPS_PER_BAR)


def pattern_from_ui_state(data: dict[str, Any]) -> DrumPattern:
    genre = data["genre"]
    preset = resolve_chain_preset(data.get("chain_preset", "ABAC"))
    pattern = DrumPattern(
        genre=genre,
        chain=CHAIN_SEQUENCES[preset],
        chain_preset=preset,
        seed_base=data.get("seed_base"),
        pattern_id=data.get("pattern_id"),
        tempo=float(data.get("tempo") or get_genre(genre).default_tempo),
    )
    for slot_name, grid in (data.get("slots") or {}).items():
        if grid:
            pattern.set_slot(_resolve_slot(slot_name), ui_grid_to_events(grid))
    pattern.register_workflow_slots()
    return pattern


def _catalog_summary(catalog) -> dict | None:
    if catalog is None:
        return None
    by_genre = {}
    for g in ("house", "breaks", "ukg", "dnb"):
        by_genre[g] = len(catalog.list_patterns(genre=g))
    return {"path": str(catalog.path), "by_genre": by_genre}


def generate_ui_pattern(
    genre: str,
    *,
    seed_base: int | None = None,
    chain_preset: str = "ABAC",
    variation_index: int = 1,
    pattern_catalog=None,
    base_edited: bool = False,
) -> dict[str, Any]:
    catalog = pattern_catalog if pattern_catalog is not None else load_default_catalog()
    kwargs: dict[str, Any] = {
        "variation_index": variation_index,
        "seed_base": seed_base,
        "chain_preset": chain_preset,
        "pattern_catalog": catalog,
    }
    pattern = generate_pattern_for_genre(genre, **kwargs)
    pattern.tempo = get_genre(genre).default_tempo
    payload = pattern_to_ui_payload(pattern, base_edited=base_edited)
    payload["catalog_patterns"] = _catalog_summary(catalog)
    return payload


def mutate_slot(
    data: dict[str, Any],
    target: str,
    kind: MutateKind,
) -> dict[str, Any]:
    pattern = pattern_from_ui_state(data)
    base = pattern.get_slot(SLOT_BASE)
    seed = data.get("seed_base")
    rng = make_rng(seed, 1) if seed is not None else random.Random()
    key = _resolve_slot(target)
    if key not in (SLOT_VAR_B, SLOT_VAR_C):
        raise ValueError(f"Cannot mutate slot {target!r}")
    pattern.set_slot(key, mutate_bar(base, kind, rng))
    pattern.register_workflow_slots()
    return pattern_to_ui_payload(pattern, base_edited=data.get("base_edited", False))


def export_ui_pattern(
    data: dict[str, Any],
    output_dir: str,
    *,
    layout: str = "both",
    velocity_var: int = 15,
    timing_var: float = 0.02,
) -> dict[str, Any]:
    from midi_beats.pipeline import export_drum_pattern

    pattern = pattern_from_ui_state(data)
    return export_drum_pattern(
        pattern,
        output_dir,
        layout=layout,
        velocity_var=velocity_var,
        timing_var=timing_var,
        seed_base=data.get("seed_base"),
    )
