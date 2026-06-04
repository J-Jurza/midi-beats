"""Shared ABAC bar builders and fill logic."""

from __future__ import annotations

import random
from typing import Callable

from midi_beats.core.events import EventMap

RNG = random.Random


def append_hits(
    events: EventMap,
    instrument: str,
    offset: float,
    times: list[float],
    velocity: int,
) -> None:
    for t in times:
        events[instrument].append((offset + t, velocity))


def apply_mini_fill(
    events: EventMap,
    offset: float,
    rng: RNG,
    snare_velocity: int = 110,
    kick_velocity: int = 100,
) -> None:
    """Bar B: snare pickup at 3.75 or double kick at 3.5 / 3.75."""
    if rng.random() < 0.5:
        events["snare"].append((offset + 3.75, snare_velocity))
    else:
        events["kick"].append((offset + 3.5, kick_velocity))
        events["kick"].append((offset + 3.75, kick_velocity))


def apply_snare_roll_fill(
    events: EventMap,
    offset: float,
    rng: RNG,
    kick_velocity: int = 100,
    roll_velocity: int = 100,
) -> None:
    """Bar C: snare roll on beats 3.25–3.75 or double kick."""
    if rng.random() < 0.5:
        for t in (3.25, 3.5, 3.75):
            events["snare"].append((offset + t, roll_velocity))
    else:
        events["kick"].append((offset + 3.5, kick_velocity))
        events["kick"].append((offset + 3.75, kick_velocity))


def apply_amen_partial_fill(
    events: EventMap,
    offset: float,
    rng: RNG,
) -> bool:
    """
    Bar C amen-style fragment. Returns True if amen was applied.

    Mutates kick/snare for the bar at ``offset`` only.
    """
    if rng.random() >= 0.5:
        return False

    events["kick"] = [
        e for e in events["kick"] if abs(e[0] - offset) > 0.001
    ]
    events["snare"].append((offset + 0.0, 100))
    events["snare"].append((offset + 0.25, 90))
    events["kick"].append((offset + 0.5, 100))
    events["snare"] = [
        e for e in events["snare"] if abs(e[0] - (offset + 3.0)) > 0.001
    ]
    events["snare"].append((offset + 3.5, 110))
    return True


def compose_abac(
    events: EventMap,
    bar_a: Callable[[float], None],
    bar_b: Callable[[float], None] | None = None,
    bar_c: Callable[[float], None] | None = None,
    base_offset: float = 0.0,
) -> None:
    """Standard 4-bar ABAC at base_offset (bars at +0, +4, +8, +12)."""
    bar_a(base_offset + 0.0)
    (bar_b or bar_a)(base_offset + 4.0)
    bar_a(base_offset + 8.0)
    (bar_c or bar_a)(base_offset + 12.0)


def make_rng(seed_base: int | None, variation_index: int) -> RNG:
    rng = RNG()
    if seed_base is not None:
        rng.seed(seed_base + variation_index)
    return rng
