"""JSON seed pattern format (git-friendly, imported into SQLite)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from midi_beats.core.events import BEATS_PER_BAR, EventMap, empty_event_map

STEPS_PER_BAR = 16


def load_seed_json(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def seed_to_bar_events(seed: dict[str, Any]) -> EventMap:
    """
    Convert seed JSON tracks → one bar EventMap.

    Seed format::
        {
          "id": "house_kick_four_floor",
          "genre": "house",
          "slot_role": "base",
          "tracks": {
            "kick": {"steps": [0, 4, 8, 12], "default_velocity": 100}
          }
        }

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
    return {
        "id": pattern_id,
        "genre": genre,
        "slot_role": slot_role,
        "tags": tags or [],
        "tracks": tracks,
    }
