"""Mutate a base bar into variations and fills."""

from __future__ import annotations

from copy import deepcopy
from enum import Enum

from midi_beats.core.events import EventMap
from midi_beats.core.fills import (
    apply_amen_partial_fill,
    apply_mini_fill,
    apply_snare_roll_fill,
)

RNG = __import__("random").Random


class MutateKind(str, Enum):
    MINI = "mini"
    FULL = "full"
    AMEN = "amen"
    NONE = "none"


def clone_bar(base: EventMap) -> EventMap:
    return deepcopy(base)


def mutate_bar(
    base: EventMap,
    kind: MutateKind,
    rng: RNG,
    *,
    offset: float = 0.0,
) -> EventMap:
    events = clone_bar(base)
    if kind == MutateKind.NONE:
        return events
    if kind == MutateKind.MINI:
        apply_mini_fill(events, offset, rng)
    elif kind == MutateKind.FULL:
        apply_snare_roll_fill(events, offset, rng)
    elif kind == MutateKind.AMEN:
        if not apply_amen_partial_fill(events, offset, rng):
            apply_snare_roll_fill(events, offset, rng)
    return events
