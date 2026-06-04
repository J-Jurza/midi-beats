"""Base pattern + mutate workflow and phrase composition."""

from __future__ import annotations

import random
from typing import Callable

from midi_beats.core.events import EventMap, empty_event_map, merge_event_maps, shift_events
from midi_beats.core.fills import (
    apply_amen_partial_fill,
    apply_mini_fill,
    apply_snare_roll_fill,
)
from midi_beats.core.mutate import MutateKind, mutate_bar
from midi_beats.core.pattern_model import (
    CHAIN_SEQUENCES,
    AutoFillConfig,
    ChainPreset,
    DrumPattern,
    SLOT_BASE,
    SLOT_VAR_B,
    SLOT_VAR_C,
    resolve_chain_preset,
)

RNG = random.Random
BarRenderer = Callable[[EventMap, float], None]

# Re-export for genre modules
__all__ = [
    "append_hits",
    "apply_mini_fill",
    "apply_snare_roll_fill",
    "apply_amen_partial_fill",
    "compose_from_base",
    "compose_abac_pattern",
    "pattern_to_events",
    "make_rng",
    "render_bar",
]


def append_hits(
    events: EventMap,
    instrument: str,
    offset: float,
    times: list[float],
    velocity: int,
) -> None:
    for t in times:
        events[instrument].append((offset + t, velocity))


def render_bar(render: BarRenderer, offset: float = 0.0) -> EventMap:
    events = empty_event_map()
    render(events, offset)
    return events


def compose_from_base(
    genre: str,
    base_bar: BarRenderer,
    rng: RNG,
    *,
    mutate_b: MutateKind = MutateKind.MINI,
    mutate_c: MutateKind = MutateKind.FULL,
    mutate_d: MutateKind | None = None,
    chain_preset: ChainPreset | str = ChainPreset.ABAC,
    seed_base: int | None = None,
    pattern_id: str | None = None,
    use_amen_for_c: bool = False,
    pattern_catalog=None,
) -> DrumPattern:
    preset = resolve_chain_preset(chain_preset)
    pattern = DrumPattern(
        genre=genre,
        chain=CHAIN_SEQUENCES[preset],
        chain_preset=preset,
        seed_base=seed_base,
        pattern_id=pattern_id,
        auto_fill=AutoFillConfig(interval_bars=4, slot="FILL1"),
    )

    base = render_bar(base_bar, 0.0)
    pattern.set_slot(SLOT_BASE, base)

    kind_c = MutateKind.AMEN if use_amen_for_c else mutate_c
    pattern.set_slot(SLOT_VAR_B, mutate_bar(base, mutate_b, rng))
    pattern.set_slot(SLOT_VAR_C, mutate_bar(base, kind_c, rng))

    if mutate_d is not None or "D" in pattern.chain:
        kind_d = mutate_d or MutateKind.FULL
        pattern.set_slot("D", mutate_bar(base, kind_d, rng))

    pattern.register_workflow_slots()
    if pattern_catalog is not None:
        from midi_beats.genres.catalog_mix import apply_catalog_base
        apply_catalog_base(pattern, pattern_catalog, genre, rng)
    return pattern


def compose_abac_pattern(
    genre: str,
    bar_a: BarRenderer,
    bar_b: BarRenderer | None = None,
    bar_c: BarRenderer | None = None,
    *,
    chain: tuple[str, ...] | None = None,
    chain_preset: ChainPreset | str = ChainPreset.ABAC,
    seed_base: int | None = None,
    pattern_id: str | None = None,
) -> DrumPattern:
    preset = resolve_chain_preset(chain_preset)
    seq = chain or CHAIN_SEQUENCES[preset]
    pattern = DrumPattern(
        genre=genre,
        chain=seq,
        chain_preset=preset,
        seed_base=seed_base,
        pattern_id=pattern_id,
        auto_fill=AutoFillConfig(interval_bars=4, slot="FILL1"),
    )
    pattern.set_slot(SLOT_BASE, render_bar(bar_a, 0.0))
    pattern.set_slot(SLOT_VAR_B, render_bar(bar_b or bar_a, 0.0))
    pattern.set_slot(SLOT_VAR_C, render_bar(bar_c or bar_a, 0.0))
    if "D" in seq:
        pattern.set_slot("D", render_bar(bar_c or bar_a, 0.0))
    pattern.register_workflow_slots()
    if pattern_catalog is not None:
        from midi_beats.genres.catalog_mix import apply_catalog_base
        apply_catalog_base(pattern, pattern_catalog, genre, rng)
    return pattern


def pattern_to_events(
    pattern: DrumPattern,
    target: EventMap | None = None,
    base_offset: float = 0.0,
) -> EventMap:
    out = target if target is not None else empty_event_map()
    chained = pattern.to_chain_events()
    if base_offset:
        chained = shift_events(chained, base_offset)
    merge_event_maps(out, chained)
    return out


def make_rng(seed_base: int | None, variation_index: int) -> RNG:
    rng = RNG()
    if seed_base is not None:
        rng.seed(seed_base + variation_index)
    return rng
