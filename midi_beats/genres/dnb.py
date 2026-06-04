"""Drum & Bass drum patterns."""

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
HAT_PAT = [x * 0.25 for x in range(16)]
HIGH_VEL = 100
LOW_VEL = 60


def generate_dnb_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    events = empty_event_map()
    rng = make_rng(seed_base, variation_index)

    ghost_kicks: list[float] = []
    if rng.random() < 0.5:
        ghost_kicks.append(0.75)

    def bar_a(offset: float) -> None:
        append_hits(events, "kick", offset, KICK_PAT, 100)
        append_hits(events, "snare", offset, SNARE_PAT, 110)
        append_hits(events, "snare", offset, GHOST_SNARES, 70)
        for gk in ghost_kicks:
            events["kick"].append((offset + gk, 80))
        for i, h_t in enumerate(HAT_PAT):
            vel = HIGH_VEL if i % 2 == 0 else LOW_VEL
            events["chh"].append((offset + h_t, vel))

    def bar_b(offset: float) -> None:
        bar_a(offset)
        apply_mini_fill(events, offset, rng, snare_velocity=100)

    def bar_c(offset: float) -> None:
        bar_a(offset)
        if not apply_amen_partial_fill(events, offset, rng):
            apply_snare_roll_fill(events, offset, rng)

    compose_abac(events, bar_a, bar_b, bar_c, base_offset)
    return events
