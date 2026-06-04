"""Drum & Bass drum patterns."""

from __future__ import annotations

from midi_beats.core.events import EventMap
from midi_beats.core.mutate import MutateKind
from midi_beats.core.pattern_model import ChainPreset, DrumPattern
from midi_beats.genres.base import (
    append_hits,
    compose_from_base,
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
    *,
    chain_preset: ChainPreset | str = ChainPreset.ABAC,
) -> DrumPattern:
    rng = make_rng(seed_base, variation_index)
    ghost_kicks: list[float] = []
    if rng.random() < 0.5:
        ghost_kicks.append(0.75)

    def base_bar(ev, offset: float) -> None:
        append_hits(ev, "kick", offset, KICK_PAT, 100)
        append_hits(ev, "snare", offset, SNARE_PAT, 110)
        append_hits(ev, "snare", offset, GHOST_SNARES, 70)
        for gk in ghost_kicks:
            ev["kick"].append((offset + gk, 80))
        for i, h_t in enumerate(HAT_PAT):
            vel = HIGH_VEL if i % 2 == 0 else LOW_VEL
            ev["chh"].append((offset + h_t, vel))

    return compose_from_base(
        "dnb",
        base_bar,
        rng,
        chain_preset=chain_preset,
        use_amen_for_c=True,
        seed_base=seed_base,
    )


def generate_dnb_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
    **kwargs,
) -> EventMap:
    return pattern_to_events(
        generate_dnb_pattern(variation_index, seed_base, **kwargs),
        base_offset=base_offset,
    )
