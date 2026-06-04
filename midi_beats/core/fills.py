"""Fill and variation hit logic (shared by mutate + genres)."""

from __future__ import annotations

from midi_beats.core.events import EventMap

RNG = __import__("random").Random


def apply_mini_fill(
    events: EventMap,
    offset: float,
    rng: RNG,
    snare_velocity: int = 110,
    kick_velocity: int = 100,
) -> None:
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
    if rng.random() >= 0.5:
        return False

    events["kick"] = [e for e in events["kick"] if abs(e[0] - offset) > 0.001]
    events["snare"].append((offset + 0.0, 100))
    events["snare"].append((offset + 0.25, 90))
    events["kick"].append((offset + 0.5, 100))
    events["snare"] = [
        e for e in events["snare"] if abs(e[0] - (offset + 3.0)) > 0.001
    ]
    events["snare"].append((offset + 3.5, 110))
    return True
