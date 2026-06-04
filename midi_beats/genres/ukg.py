"""UK Garage drum patterns."""

from __future__ import annotations

from midi_beats.core.events import EventMap
from midi_beats.core.pattern_model import ChainPreset, DrumPattern
from midi_beats.genres.base import (
    append_hits,
    compose_from_base,
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
    *,
    chain_preset: ChainPreset | str = ChainPreset.ABAC,
    pattern_catalog=None,
) -> DrumPattern:
    rng = make_rng(seed_base, variation_index)

    def base_bar(ev, offset: float) -> None:
        append_hits(ev, "kick", offset, KICK_PAT, 100)
        append_hits(ev, "snare", offset, SNARE_PAT, 110)
        append_hits(ev, "clap", offset, CLAP_PAT, 110)
        append_hits(ev, "chh", offset, CHH_PAT, 90)
        append_hits(ev, "ohh", offset, OHH_PAT, 100)
        ev["chh"].append((offset + SWUNG_HAT, 80))
        if rng.random() < 0.5:
            ev["kick"].append((offset + 1.75, 60))

    return compose_from_base(
        "ukg",
        base_bar,
        rng,
        chain_preset=chain_preset,
        seed_base=seed_base,
        pattern_id=f"ukg_{variation_index}",
        pattern_catalog=pattern_catalog,
    )


def generate_ukg_events(
    variation_index: int = 1,
    seed_base: int | None = None,
    base_offset: float = 0.0,
    **kwargs,
) -> EventMap:
    return pattern_to_events(
        generate_ukg_pattern(variation_index, seed_base, **kwargs),
        base_offset=base_offset,
    )
