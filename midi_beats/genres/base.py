"""Shared fills and TR-8 slot / chain composition."""

from __future__ import annotations

import random

from midi_beats.core.events import EventMap, empty_event_map, merge_event_maps, shift_events
from midi_beats.core.pattern_model import (
    CHAIN_SEQUENCES,
    AutoFillConfig,
    ChainPreset,
    DrumPattern,
)

RNG = random.Random
BarRenderer = type  # Callable[[EventMap, float], None] — use callable in signatures below


def append_hits(
    events: EventMap,
    instrument: str,
    offset: float,
    times: list[float],
    velocity: int,
) -> None:
    for t in times:
        events[instrument].append((offset + t, velocity))


def apply_mini_fill(
    events: EventMap,
    offset: float,
    rng: RNG,
    snare_velocity: int = 110,
    kick_velocity: int = 100,
) -> None:
    if rng.random() < 0.5:
        events["snare"].append((offset + 3.75, snare_velocity))
    else:
        events["kick"].append((offset + 3.5, kick_velocity))
        events["kick"].append((offset + 3.75, kick_velocity))


def apply_snare_roll_fill(
    events: EventMap,
    offset: float,
    rng: RNG,
    kick_velocity: int = 100,
    roll_velocity: int = 100,
) -> None:
    if rng.random() < 0.5:
        for t in (3.25, 3.5, 3.75):
            events["snare"].append((offset + t, roll_velocity))
    else:
        events["kick"].append((offset + 3.5, kick_velocity))
        events["kick"].append((offset + 3.75, kick_velocity))


def apply_amen_partial_fill(
    events: EventMap,
    offset: float,
    rng: RNG,
) -> bool:
    if rng.random() >= 0.5:
        return False

    events["kick"] = [e for e in events["kick"] if abs(e[0] - offset) > 0.001]
    events["snare"].append((offset + 0.0, 100))
    events["snare"].append((offset + 0.25, 90))
    events["kick"].append((offset + 0.5, 100))
    events["snare"] = [
        e for e in events["snare"] if abs(e[0] - (offset + 3.0)) > 0.001
    ]
    events["snare"].append((offset + 3.5, 110))
    return True


def render_bar(render, offset: float = 0.0) -> EventMap:
    events = empty_event_map()
    render(events, offset)
    return events


def compose_abac_pattern(
    genre: str,
    bar_a,
    bar_b=None,
    bar_c=None,
    *,
    chain: tuple[str, ...] = CHAIN_SEQUENCES[ChainPreset.ABAC],
    seed_base: int | None = None,
    pattern_id: str | None = None,
) -> DrumPattern:
    """
    TR-8 mapping:
      A  = base groove
      B  = variation / mini fill  → FILL1
      C  = full fill              → FILL2
    Default chain ABAC = Roland-style 4-bar song form for Ableton export.
    """
    pattern = DrumPattern(
        genre=genre,
        chain=chain,
        seed_base=seed_base,
        pattern_id=pattern_id,
        auto_fill=AutoFillConfig(interval_bars=4, slot="FILL1"),
    )
    pattern.set_slot("A", render_bar(bar_a, 0.0))
    pattern.set_slot("B", render_bar(bar_b or bar_a, 0.0))
    pattern.set_slot("C", render_bar(bar_c or bar_a, 0.0))
    pattern.set_slot("FILL1", pattern.get_slot("B"))
    pattern.set_slot("FILL2", pattern.get_slot("C"))
    return pattern


def pattern_to_events(
    pattern: DrumPattern,
    target: EventMap | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    """Flatten pattern chain into an EventMap (optional offset for concatenation)."""
    out = target if target is not None else empty_event_map()
    chained = pattern.to_chain_events()
    if base_offset:
        chained = shift_events(chained, base_offset)
    merge_event_maps(out, chained)
    return out


def make_rng(seed_base: int | None, variation_index: int) -> RNG:
    rng = RNG()
    if seed_base is not None:
        rng.seed(seed_base + variation_index)
    return rng
