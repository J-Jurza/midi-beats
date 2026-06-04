"""Event map types and time utilities."""

from __future__ import annotations

from typing import TypeAlias

Event = tuple[float, int]  # (beat_time, velocity)
EventMap: TypeAlias = dict[str, list[Event]]

INSTRUMENTS = ("kick", "snare", "clap", "chh", "ohh")

GM_DRUM_MAP = {
    "kick": 36,
    "snare": 38,
    "clap": 39,
    "chh": 42,
    "ohh": 46,
}

INSTRUMENT_FILENAMES = {
    "kick": "kick",
    "snare": "snare",
    "clap": "clap",
    "chh": "hats",
    "ohh": "ohh",
}

BEATS_PER_BAR = 4
BARS_PER_ABAC = 4
BEATS_PER_VARIATION = BEATS_PER_BAR * BARS_PER_ABAC  # 16


def empty_event_map() -> EventMap:
    return {inst: [] for inst in INSTRUMENTS}


def shift_events(events: EventMap, offset: float) -> EventMap:
    if offset == 0:
        return events
    return {
        inst: [(t + offset, vel) for t, vel in ev_list]
        for inst, ev_list in events.items()
    }


def normalize_to_bar_zero(events: EventMap, base_offset: float) -> EventMap:
    """Shift all events so a variation slice starts at beat 0."""
    if base_offset == 0:
        return events
    return {
        inst: [(t - base_offset, vel) for t, vel in ev_list]
        for inst, ev_list in events.items()
    }


def merge_event_maps(target: EventMap, source: EventMap) -> None:
    for inst in INSTRUMENTS:
        target[inst].extend(source[inst])
