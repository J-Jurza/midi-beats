"""UK Garage drum patterns."""

from __future__ import annotations

from midi_beats.core.events import EventMap
from midi_beats.core.pattern_model import DrumPattern
from midi_beats.genres.base import (
    append_hits,
    apply_mini_fill,
    apply_snare_roll_fill,
    compose_abac_pattern,
    make_rng,
    pattern_to_events,
)

KICK_PAT = [0.0, 2.5]
SNARE_PAT = [1.0, 3.0]
CLAP_PAT = [1.0, 3.0]
CHH_PAT = [0.0, 1.0, 2.0, 3.0]
OHH_PAT = [0.5, 1.5, 3.5]
SWUNG_HAT = 2.25


def generate_ukg_pattern(
    variation_index: int = 1,
    seed_base: int | None = None,
) -> DrumPattern:
    rng = make_rng(seed_base, variation_index)

    def bar_a(ev, offset: float) -> None:
        append_hits(ev, "kick", offset, KICK_PAT, 100)
        append_hits(ev, "snare", offset, SNARE_PAT, 110)
        append_hits(ev, "clap", offset, CLAP_PAT, 110)
        append_hits(ev, "chh", offset, CHH_PAT, 90)
        append_hits(ev, "ohh", offset, OHH_PAT, 100)
        ev["chh"].append((offset + SWUNG_HAT, 80))
        if rng.random() < 0.5:
            ev["kick"].append((offset + 1.75, 60))

    def bar_b(ev, offset: float) -> None:
        bar_a(ev, offset)
        apply_mini_fill(ev, offset, rng)

    def bar_c(ev, offset: float) -> None:
        bar_a(ev, offset)
        apply_snare_roll_fill(ev, offset, rng)

    return compose_abac_pattern("ukg", bar_a, bar_b, bar_c, seed_base=seed_base)


def generate_ukg_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    return pattern_to_events(
        generate_ukg_pattern(variation_index, seed_base),
        base_offset=base_offset,
    )
