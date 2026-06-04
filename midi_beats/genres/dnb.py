"""Drum & Bass drum patterns."""

from __future__ import annotations

from midi_beats.core.events import EventMap
from midi_beats.core.pattern_model import DrumPattern
from midi_beats.genres.base import (
    append_hits,
    apply_amen_partial_fill,
    apply_mini_fill,
    apply_snare_roll_fill,
    compose_abac_pattern,
    make_rng,
    pattern_to_events,
)

KICK_PAT = [0.0, 2.5]
SNARE_PAT = [1.0, 3.0]
GHOST_SNARES = [1.25, 2.75]
HAT_PAT = [x * 0.25 for x in range(16)]
HIGH_VEL = 100
LOW_VEL = 60


def generate_dnb_pattern(
    variation_index: int = 1,
    seed_base: int | None = None,
) -> DrumPattern:
    rng = make_rng(seed_base, variation_index)
    ghost_kicks: list[float] = []
    if rng.random() < 0.5:
        ghost_kicks.append(0.75)

    def bar_a(ev, offset: float) -> None:
        append_hits(ev, "kick", offset, KICK_PAT, 100)
        append_hits(ev, "snare", offset, SNARE_PAT, 110)
        append_hits(ev, "snare", offset, GHOST_SNARES, 70)
        for gk in ghost_kicks:
            ev["kick"].append((offset + gk, 80))
        for i, h_t in enumerate(HAT_PAT):
            vel = HIGH_VEL if i % 2 == 0 else LOW_VEL
            ev["chh"].append((offset + h_t, vel))

    def bar_b(ev, offset: float) -> None:
        bar_a(ev, offset)
        apply_mini_fill(ev, offset, rng, snare_velocity=100)

    def bar_c(ev, offset: float) -> None:
        bar_a(ev, offset)
        if not apply_amen_partial_fill(ev, offset, rng):
            apply_snare_roll_fill(ev, offset, rng)

    return compose_abac_pattern("dnb", bar_a, bar_b, bar_c, seed_base=seed_base)


def generate_dnb_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    return pattern_to_events(
        generate_dnb_pattern(variation_index, seed_base),
        base_offset=base_offset,
    )
