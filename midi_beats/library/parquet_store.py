"""Parquet pattern catalog (primary store; upgrade path to SQL DB later)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from midi_beats.core.events import EventMap
from midi_beats.library.seed_io import load_seed_json, seed_to_bar_events

DEFAULT_PARQUET = Path(__file__).resolve().parents[2] / "data" / "patterns.parquet"


class PatternCatalog:
    """
    Pattern library backed by Parquet.

    One row per (pattern_id, slot) with compact steps JSON.
    """

    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or DEFAULT_PARQUET)
        self._df = None

    def _load(self):
        if self._df is not None:
            return self._df
        import pandas as pd

        if self.path.is_file():
            self._df = pd.read_parquet(self.path)
        else:
            self._df = pd.DataFrame(
                columns=[
                    "pattern_id",
                    "genre",
                    "slot",
                    "steps_json",
                    "tags",
                    "source",
                ]
            )
        return self._df

    def _save(self) -> None:
        import pandas as pd

        self.path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(self._load()).to_parquet(self.path, index=False)

    def import_seed_file(self, path: str | Path, *, slot: str = "A") -> str:
        seed = load_seed_json(path)
        pattern_id = seed["id"]
        steps = _events_to_steps(seed_to_bar_events(seed))
        row = {
            "pattern_id": pattern_id,
            "genre": seed.get("genre", "unknown"),
            "slot": slot,
            "steps_json": json.dumps(steps),
            "tags": json.dumps(seed.get("tags", [])),
            "source": str(path),
        }
        import pandas as pd

        df = self._load()
        df = df[~((df["pattern_id"] == pattern_id) & (df["slot"] == slot))]
        self._df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        self._save()
        return pattern_id

    def import_seed_directory(self, directory: str | Path) -> list[str]:
        ids = []
        for path in sorted(Path(directory).glob("**/*.json")):
            ids.append(self.import_seed_file(path))
        return ids

    def get_slot(self, pattern_id: str, slot: str = "A") -> EventMap:
        df = self._load()
        row = df[(df["pattern_id"] == pattern_id) & (df["slot"] == slot)]
        if row.empty and slot == "A":
            row = df[(df["pattern_id"] == pattern_id) & (df["slot"] == "BASE")]
        if row.empty:
            raise KeyError(f"{pattern_id!r} slot {slot!r} not in catalog")
        steps = json.loads(row.iloc[0]["steps_json"])
        return seed_to_bar_events({"tracks": _steps_to_tracks(steps)})

    def list_patterns(self, genre: str | None = None, limit: int = 200) -> list[dict]:
        df = self._load()
        if df.empty:
            return []
        sub = df[df["genre"] == genre] if genre else df
        ids = sub["pattern_id"].drop_duplicates().head(limit)
        return [
            {
                "pattern_id": pid,
                "genre": sub[sub["pattern_id"] == pid].iloc[0]["genre"],
            }
            for pid in ids
        ]

    def random_pattern_id(self, genre: str, rng) -> str | None:
        patterns = self.list_patterns(genre=genre)
        if not patterns:
            return None
        return rng.choice(patterns)["pattern_id"]


def _events_to_steps(events: EventMap) -> dict[str, list[int]]:
    from midi_beats.core.grid import beat_to_step

    out: dict[str, list[int]] = {}
    for inst, evs in events.items():
        steps = sorted({beat_to_step(t) for t, _ in evs})
        if steps:
            out[inst] = steps
    return out


def _steps_to_tracks(steps: dict[str, list[int]]) -> dict[str, Any]:
    return {
        inst: {"steps": s, "default_velocity": 100}
        for inst, s in steps.items()
    }
