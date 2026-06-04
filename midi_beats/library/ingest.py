"""Build and maintain the Parquet pattern library from JSON seeds."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from midi_beats.core.events import BEATS_PER_BAR
from midi_beats.core.pattern_model import ChainPreset
from midi_beats.genres.catalog_mix import apply_catalog_base
from midi_beats.genres.registry import list_genres
from midi_beats.library.parquet_store import PatternCatalog, DEFAULT_PARQUET
from midi_beats.library.seed_io import (
    events_to_seed,
    load_seed_json,
    slot_from_seed,
    validate_seed,
    write_seed_json,
)


def process_seed_file(
    path: str | Path,
    catalog: PatternCatalog,
    *,
    slot: str | None = None,
) -> str:
    """
    Validate a JSON seed and add it to the Parquet catalog.

    Returns pattern_id.
    """
    path = Path(path)
    seed = load_seed_json(path)
    validate_seed(seed)
    slot_key = slot or slot_from_seed(seed)
    return catalog.import_seed_record(seed, slot=slot_key, source=str(path))


def ingest_json_directory(
    directory: str | Path,
    catalog: PatternCatalog | None = None,
) -> list[str]:
    """Import all ``**/*.json`` seeds under ``directory`` into the catalog."""
    catalog = catalog or PatternCatalog()
    ids: list[str] = []
    root = Path(directory)
    for path in sorted(root.glob("**/*.json")):
        try:
            ids.append(process_seed_file(path, catalog))
        except (ValueError, KeyError) as e:
            print(f"Skip {path}: {e}")
    return ids


def generate_procedural_seeds(
    output_dir: str | Path,
    *,
    per_genre: int = 5,
    seed_start: int = 1000,
    chain_preset: str = ChainPreset.ABAC.value,
) -> list[Path]:
    """
    Generate BASE-bar JSON seeds from procedural generators and write to disk.

    Does not mutate — exports the BASE slot only for library variety.
    """
    from midi_beats.genres.registry import generate_pattern_for_genre

    output_dir = Path(output_dir)
    written: list[Path] = []

    for genre in list_genres():
        genre_dir = output_dir / genre
        genre_dir.mkdir(parents=True, exist_ok=True)
        for i in range(1, per_genre + 1):
            seed_base = seed_start + i * 17
            pattern = generate_pattern_for_genre(
                genre,
                variation_index=i,
                seed_base=seed_base,
                chain_preset=chain_preset,
            )
            base_events = pattern.get_slot("BASE")
            pattern_id = f"{genre}_proc_{seed_base}"
            seed = events_to_seed(
                base_events,
                pattern_id=pattern_id,
                genre=genre,
                slot_role="base",
                tags=["procedural", "generated", genre],
            )
            seed["name"] = f"{genre} procedural base {i}"
            path = genre_dir / f"{pattern_id}.json"
            write_seed_json(path, seed)
            written.append(path)

    return written


def build_pattern_library(
    json_dir: str | Path = "data/patterns",
    parquet_path: str | Path | None = None,
    *,
    generate: bool = False,
    generate_per_genre: int = 5,
    seed_start: int = 1000,
) -> dict[str, Any]:
    """
    Full pipeline: optionally generate JSON seeds, then ingest into Parquet.

    Returns summary dict with counts and catalog path.
    """
    json_dir = Path(json_dir)
    catalog = PatternCatalog(parquet_path)

    generated: list[str] = []
    if generate:
        paths = generate_procedural_seeds(
            json_dir,
            per_genre=generate_per_genre,
            seed_start=seed_start,
        )
        generated = [str(p) for p in paths]

    imported = ingest_json_directory(json_dir, catalog)
    summary = {
        "parquet_path": str(catalog.path),
        "json_dir": str(json_dir),
        "generated_files": len(generated),
        "imported_ids": imported,
        "total_patterns": len(set(imported)),
        "by_genre": _count_by_genre(catalog),
    }
    return summary


def _count_by_genre(catalog: PatternCatalog) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in catalog.list_patterns(limit=10_000):
        g = row["genre"]
        counts[g] = counts.get(g, 0) + 1
    return counts


def load_default_catalog() -> PatternCatalog | None:
    """Load catalog if parquet exists."""
    path = DEFAULT_PARQUET
    if path.is_file():
        return PatternCatalog(path)
    return None
