"""UK Garage drum patterns."""

from __future__ import annotations

from midi_beats.core.events import EventMap, empty_event_map
from midi_beats.genres.base import (
    append_hits,
    apply_mini_fill,
    apply_snare_roll_fill,
    compose_abac,
    make_rng,
)

KICK_PAT = [0.0, 2.5]
SNARE_PAT = [1.0, 3.0]
CLAP_PAT = [1.0, 3.0]
CHH_PAT = [0.0, 1.0, 2.0, 3.0]
OHH_PAT = [0.5, 1.5, 3.5]
SWUNG_HAT = 2.25


def generate_ukg_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    events = empty_event_map()
    rng = make_rng(seed_base, variation_index)

    def bar_a(offset: float) -> None:
        append_hits(events, "kick", offset, KICK_PAT, 100)
        append_hits(events, "snare", offset, SNARE_PAT, 110)
        append_hits(events, "clap", offset, CLAP_PAT, 110)
        append_hits(events, "chh", offset, CHH_PAT, 90)
        append_hits(events, "ohh", offset, OHH_PAT, 100)
        events["chh"].append((offset + SWUNG_HAT, 80))
        if rng.random() < 0.5:
            events["kick"].append((offset + 1.75, 60))

    def bar_b(offset: float) -> None:
        bar_a(offset)
        apply_mini_fill(events, offset, rng)

    def bar_c(offset: float) -> None:
        bar_a(offset)
        apply_snare_roll_fill(events, offset, rng)

    compose_abac(events, bar_a, bar_b, bar_c, base_offset)
    return events
