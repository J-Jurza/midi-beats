"""House drum patterns."""

from __future__ import annotations

from midi_beats.core.events import EventMap
from midi_beats.core.pattern_model import DrumPattern
from typing import TYPE_CHECKING

from midi_beats.genres.base import (
    append_hits,
    apply_mini_fill,
    apply_snare_roll_fill,
    compose_abac_pattern,
    make_rng,
    pattern_to_events,
)

KICK_PAT = [0.0, 1.0, 2.0, 2.5, 3.0]
SNARE_PAT = [1.0, 3.0]
CLAP_PAT = [1.0, 3.0]
OHH_PAT = [0.5, 1.5, 2.5, 3.5]


def generate_house_pattern(
    variation_index: int = 1,
    seed_base: int | None = None,
    pattern_store=None,
) -> DrumPattern:
    rng = make_rng(seed_base, variation_index)
    if rng.random() < 0.5:
        chh_list = [x * 0.25 for x in range(16)]
    else:
        chh_list = [x * 0.5 for x in range(8)]

    def bar_a(ev, offset: float) -> None:
        append_hits(ev, "kick", offset, KICK_PAT, 100)
        append_hits(ev, "snare", offset, SNARE_PAT, 110)
        append_hits(ev, "clap", offset, CLAP_PAT, 110)
        append_hits(ev, "chh", offset, chh_list, 90)
        append_hits(ev, "ohh", offset, OHH_PAT, 100)

    def bar_b(ev, offset: float) -> None:
        bar_a(ev, offset)
        apply_mini_fill(ev, offset, rng)

    def bar_c(ev, offset: float) -> None:
        bar_a(ev, offset)
        apply_snare_roll_fill(ev, offset, rng)


    pattern = compose_abac_pattern(
        "house",
        bar_a,
        bar_b,
        bar_c,
        seed_base=seed_base,
        pattern_id=f"house_{variation_index}",
    )
    if pattern_store is not None:
        pid = pattern_store.random_base_id("house", rng)
        if pid:
            pattern.set_slot("A", pattern_store.get_slot_events(pid, "A"))
            pattern.pattern_id = pid
    return pattern


def generate_house_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    pattern = generate_house_pattern(variation_index, seed_base)
    return pattern_to_events(pattern, base_offset=base_offset)
