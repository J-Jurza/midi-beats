"""Velocity and timing humanization."""

from __future__ import annotations

import random

from midi_beats.core.events import EventMap


def humanize_events(
    events: EventMap,
    velocity_variation: int = 0,
    timing_variation: float = 0.0,
    seed: int | None = None,
    lock_backbeat: bool = False,
) -> None:
    """
    Apply in-place random velocity and timing offsets.

    Parameters:
        lock_backbeat: When True, kick and snare share the same timing jitter per
            event index (preserves their relative grid relationship).
        seed: If set, makes humanization reproducible for a given event map state.
    """
    rng = random.Random(seed) if seed is not None else random

    backbeat_jitters: list[float] = []

    for instrument, ev_list in events.items():
        for i, (time, vel) in enumerate(ev_list):
            if velocity_variation > 0:
                delta_vel = rng.randint(-velocity_variation, velocity_variation)
                vel = max(1, min(127, vel + delta_vel))

            if timing_variation > 0:
                if lock_backbeat and instrument in ("kick", "snare"):
                    while len(backbeat_jitters) <= i:
                        backbeat_jitters.append(
                            rng.uniform(-timing_variation, timing_variation)
                        )
                    delta_time = backbeat_jitters[i]
                else:
                    delta_time = rng.uniform(-timing_variation, timing_variation)
                time = max(0.0, time + delta_time)

            ev_list[i] = (time, vel)
