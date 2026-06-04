"""SQLite pattern catalog for scale (ML, UI, search)."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from midi_beats.core.events import EventMap
from midi_beats.library.seed_io import load_seed_json, seed_to_bar_events

DEFAULT_DB = Path(__file__).resolve().parents[2] / "data" / "patterns.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS patterns (
    id TEXT PRIMARY KEY,
    genre TEXT NOT NULL,
    name TEXT,
    tempo REAL,
    tags TEXT,
    source TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS variation_slots (
    pattern_id TEXT NOT NULL,
    slot TEXT NOT NULL,
    steps_json TEXT NOT NULL,
    PRIMARY KEY (pattern_id, slot),
    FOREIGN KEY (pattern_id) REFERENCES patterns(id)
);
CREATE INDEX IF NOT EXISTS idx_patterns_genre ON patterns(genre);
CREATE INDEX IF NOT EXISTS idx_patterns_tags ON patterns(tags);
"""


class PatternStore:
    """CRUD for pattern seeds and slots."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path or DEFAULT_DB)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(_SCHEMA)

    def import_seed_file(self, path: str | Path, *, slot: str = "A") -> str:
        seed = load_seed_json(path)
        pattern_id = seed["id"]
        events = seed_to_bar_events(seed)
        steps = _events_to_steps_json(events)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO patterns (id, genre, name, tags, source)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    pattern_id,
                    seed.get("genre", "unknown"),
                    seed.get("name", pattern_id),
                    json.dumps(seed.get("tags", [])),
                    str(path),
                ),
            )
            conn.execute(
                """
                INSERT OR REPLACE INTO variation_slots (pattern_id, slot, steps_json)
                VALUES (?, ?, ?)
                """,
                (pattern_id, slot, json.dumps(steps)),
            )
        return pattern_id

    def import_seed_directory(self, directory: str | Path) -> list[str]:
        ids = []
        for path in sorted(Path(directory).glob("**/*.json")):
            ids.append(self.import_seed_file(path))
        return ids

    def get_slot_events(self, pattern_id: str, slot: str = "A") -> EventMap:
        from midi_beats.library.seed_io import seed_to_bar_events

        with self._connect() as conn:
            row = conn.execute(
                "SELECT steps_json FROM variation_slots WHERE pattern_id=? AND slot=?",
                (pattern_id, slot),
            ).fetchone()
        if not row:
            raise KeyError(f"No slot {slot!r} for pattern {pattern_id!r}")
        steps = json.loads(row["steps_json"])
        seed = {"tracks": _steps_to_tracks(steps)}
        return seed_to_bar_events(seed)

    def list_patterns(self, genre: str | None = None, limit: int = 100) -> list[dict]:
        with self._connect() as conn:
            if genre:
                rows = conn.execute(
                    "SELECT id, genre, name, tags FROM patterns WHERE genre=? LIMIT ?",
                    (genre, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT id, genre, name, tags FROM patterns LIMIT ?",
                    (limit,),
                ).fetchall()
        return [dict(r) for r in rows]

    def random_base_id(self, genre: str, rng) -> str | None:
        patterns = self.list_patterns(genre=genre, limit=500)
        if not patterns:
            return None
        return rng.choice(patterns)["id"]


def _events_to_steps_json(events: EventMap) -> dict[str, list[int]]:
    from midi_beats.core.grid import beat_to_step

    out: dict[str, list[int]] = {}
    for inst, evs in events.items():
        steps = sorted({beat_to_step(t) for t, _ in evs})
        if steps:
            out[inst] = steps
    return out


def _steps_to_tracks(steps: dict[str, list[int]]) -> dict[str, Any]:
    return {
        inst: {"steps": step_list, "default_velocity": 100}
        for inst, step_list in steps.items()
    }
