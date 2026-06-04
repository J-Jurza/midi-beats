"""Breakbeat / breaks drum patterns."""

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
HAT_PAT = [x * 0.5 for x in range(8)]


def generate_breaks_pattern(
    variation_index: int = 1,
    seed_base: int | None = None,
) -> DrumPattern:
    rng = make_rng(seed_base, variation_index)
    ghost_kicks: list[float] = []
    if rng.random() < 0.5:
        ghost_kicks.append(3.5)

    def base_bar(ev, offset: float) -> None:
        append_hits(ev, "kick", offset, KICK_PAT, 100)
        append_hits(ev, "snare", offset, SNARE_PAT, 110)
        append_hits(ev, "snare", offset, GHOST_SNARES, 70)
        for gk in ghost_kicks:
            ev["kick"].append((offset + gk, 80))
        append_hits(ev, "chh", offset, HAT_PAT, 100)

    def bar_b(ev, offset: float) -> None:
        base_bar(ev, offset)
        apply_mini_fill(ev, offset, rng, snare_velocity=100)

    def bar_c(ev, offset: float) -> None:
        base_bar(ev, offset)
        if not apply_amen_partial_fill(ev, offset, rng):
            apply_snare_roll_fill(ev, offset, rng)

    return compose_abac_pattern("breaks", base_bar, bar_b, bar_c, seed_base=seed_base)


def generate_breaks_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    return pattern_to_events(
        generate_breaks_pattern(variation_index, seed_base),
        base_offset=base_offset,
    )
