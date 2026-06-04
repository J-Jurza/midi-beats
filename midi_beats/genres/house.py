"""House drum patterns."""

from __future__ import annotations

from midi_beats.core.events import EventMap
from midi_beats.core.pattern_model import ChainPreset, DrumPattern
from midi_beats.genres.base import (
    append_hits,
    compose_from_base,
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
    *,
    chain_preset: ChainPreset | str = ChainPreset.ABAC,
    pattern_catalog=None,
) -> DrumPattern:
    rng = make_rng(seed_base, variation_index)
    if rng.random() < 0.5:
        chh_list = [x * 0.25 for x in range(16)]
    else:
        chh_list = [x * 0.5 for x in range(8)]

    def base_bar(ev, offset: float) -> None:
        append_hits(ev, "kick", offset, KICK_PAT, 100)
        append_hits(ev, "snare", offset, SNARE_PAT, 110)
        append_hits(ev, "clap", offset, CLAP_PAT, 110)
        append_hits(ev, "chh", offset, chh_list, 90)
        append_hits(ev, "ohh", offset, OHH_PAT, 100)

    pattern = compose_from_base(
        "house",
        base_bar,
        rng,
        chain_preset=chain_preset,
        seed_base=seed_base,
        pattern_id=f"house_{variation_index}",
    )

    if pattern_catalog is not None:
        pid = pattern_catalog.random_pattern_id("house", rng)
        if pid:
            base_events = pattern_catalog.get_slot(pid, "A")
            pattern.set_slot("BASE", base_events)
            pattern.register_workflow_slots()
            pattern.pattern_id = pid

    return pattern


def generate_house_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
    **kwargs,
) -> EventMap:
    return pattern_to_events(
        generate_house_pattern(variation_index, seed_base, **kwargs),
        base_offset=base_offset,
    )
