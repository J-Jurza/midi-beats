"""Breakbeat / breaks drum patterns."""

from __future__ import annotations

from midi_beats.core.events import EventMap, empty_event_map
from midi_beats.genres.base import (
    append_hits,
    apply_amen_partial_fill,
    apply_mini_fill,
    apply_snare_roll_fill,
    compose_abac,
    make_rng,
)

KICK_PAT = [0.0, 2.5]
SNARE_PAT = [1.0, 3.0]
GHOST_SNARES = [1.25, 2.75]
HAT_PAT = [x * 0.5 for x in range(8)]


def generate_breaks_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    events = empty_event_map()
    rng = make_rng(seed_base, variation_index)

    ghost_kicks: list[float] = []
    if rng.random() < 0.5:
        ghost_kicks.append(3.5)

    def base_bar(offset: float) -> None:
        append_hits(events, "kick", offset, KICK_PAT, 100)
        append_hits(events, "snare", offset, SNARE_PAT, 110)
        append_hits(events, "snare", offset, GHOST_SNARES, 70)
        for gk in ghost_kicks:
            events["kick"].append((offset + gk, 80))
        append_hits(events, "chh", offset, HAT_PAT, 100)

    def bar_b(offset: float) -> None:
        base_bar(offset)
        apply_mini_fill(events, offset, rng, snare_velocity=100)

    def bar_c(offset: float) -> None:
        base_bar(offset)
        if not apply_amen_partial_fill(events, offset, rng):
            apply_snare_roll_fill(events, offset, rng)

    compose_abac(events, base_bar, bar_b, bar_c, base_offset)
    return events
