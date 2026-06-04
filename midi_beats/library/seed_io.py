"""JSON seed pattern format (git-friendly, imported into Parquet)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from midi_beats.core.events import BEATS_PER_BAR, EventMap, INSTRUMENTS, empty_event_map

STEPS_PER_BAR = 16

SLOT_ROLE_MAP = {
    "base": "A",
    "a": "A",
    "variation_b": "B",
    "b": "B",
    "variation_c": "C",
    "c": "C",
    "fill1": "FILL1",
    "fill2": "FILL2",
}


def slot_from_seed(seed: dict) -> str:
    role = (seed.get("slot_role") or seed.get("slot") or "base").lower()
    return SLOT_ROLE_MAP.get(role, role.upper())

VALID_GENRES = {"house", "breaks", "ukg", "dnb"}


def load_seed_json(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_seed_json(path: str | Path, seed: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(seed, f, indent=2)
        f.write("\n")


def validate_seed(seed: dict[str, Any]) -> None:
    if "id" not in seed:
        raise ValueError("Seed missing 'id'")
    if seed.get("genre") not in VALID_GENRES:
        raise ValueError(f"Invalid genre {seed.get('genre')!r}")
    tracks = seed.get("tracks")
    if not tracks or not isinstance(tracks, dict):
        raise ValueError("Seed missing 'tracks'")
    for inst, td in tracks.items():
        if inst not in INSTRUMENTS:
            raise ValueError(f"Unknown instrument {inst!r}")
        steps = td.get("steps", [])
        for s in steps:
            if not 0 <= int(s) < STEPS_PER_BAR:
                raise ValueError(f"Step {s} out of range 0-15 in {inst}")


def seed_to_bar_events(seed: dict[str, Any]) -> EventMap:
    """
    Convert seed JSON tracks → one bar EventMap.

    Steps are 0–15 sixteenth indices (TR-8 pads).
    """
    events = empty_event_map()
    step_len = BEATS_PER_BAR / STEPS_PER_BAR
    tracks = seed.get("tracks", {})

    for inst, track_data in tracks.items():
        if inst not in events:
            continue
        steps = track_data.get("steps", [])
        vel = track_data.get("default_velocity", 100)
        for step in steps:
            beat = int(step) * step_len
            events[inst].append((beat, vel))

    return events


def events_to_seed(
    events: EventMap,
    *,
    pattern_id: str,
    genre: str,
    slot_role: str = "base",
    tags: list[str] | None = None,
    name: str | None = None,
) -> dict[str, Any]:
    """Serialize one bar of events to seed JSON."""
    step_len = BEATS_PER_BAR / STEPS_PER_BAR
    tracks: dict[str, Any] = {}
    for inst, evs in events.items():
        steps = sorted(
            {int(round(t / step_len)) for t, _ in evs if t < BEATS_PER_BAR}
        )
        if not steps:
            continue
        vels = [v for t, v in evs if t < BEATS_PER_BAR]
        tracks[inst] = {
            "steps": steps,
            "default_velocity": vels[0] if vels else 100,
        }
    out: dict[str, Any] = {
        "id": pattern_id,
        "genre": genre,
        "slot_role": slot_role,
        "tags": tags or [],
        "tracks": tracks,
    }
    if name:
        out["name"] = name
    return out
