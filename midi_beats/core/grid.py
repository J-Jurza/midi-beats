"""Step grid conversion (TR-8 style: 16 sixteenth steps per bar)."""

from __future__ import annotations

from dataclasses import dataclass

from midi_beats.core.events import BEATS_PER_BAR, EventMap, INSTRUMENTS

STEPS_PER_BAR = 16
STEPS_PER_ABAC_CHAIN = STEPS_PER_BAR * 4
SIXTEENTHS_PER_BEAT = STEPS_PER_BAR / BEATS_PER_BAR


@dataclass
class StepCell:
    on: bool
    velocity: int | None = None


def beat_to_step(beat: float, steps_per_bar: int = STEPS_PER_BAR) -> int:
    """Map beat within a bar to step index 0..steps_per_bar-1."""
    beat_in_bar = beat % BEATS_PER_BAR
    step = int(round(beat_in_bar * (steps_per_bar / BEATS_PER_BAR)))
    return max(0, min(steps_per_bar - 1, step))


def beat_to_phrase_step(beat: float, total_steps: int = STEPS_PER_ABAC_CHAIN) -> int:
    """Map beat across a phrase (e.g. 16 beats) to 0..total_steps-1."""
    idx = int(round(beat * SIXTEENTHS_PER_BEAT))
    return max(0, min(total_steps - 1, idx))


def events_to_step_grid(
    events: EventMap,
    *,
    steps: int = STEPS_PER_BAR,
    max_beat: float | None = None,
    instruments: tuple[str, ...] | None = None,
) -> dict[str, list[StepCell]]:
    """
    Quantize events to a step grid per instrument.

    For one bar use steps=16. For a 4-bar phrase use steps=64, max_beat=16.
    """
    insts = instruments or INSTRUMENTS
    grid: dict[str, list[StepCell]] = {
        inst: [StepCell(on=False) for _ in range(steps)] for inst in insts
    }
    limit = max_beat if max_beat is not None else steps / SIXTEENTHS_PER_BEAT
    use_phrase = steps > STEPS_PER_BAR

    for inst in insts:
        for beat, vel in events.get(inst, []):
            if beat >= limit - 0.001:
                continue
            if use_phrase:
                idx = beat_to_phrase_step(beat, steps)
            else:
                idx = beat_to_step(beat, steps)
            cell = grid[inst][idx]
            if not cell.on or (cell.velocity or 0) < vel:
                grid[inst][idx] = StepCell(on=True, velocity=vel)

    return grid


def step_grid_to_events(
    grid: dict[str, list[StepCell]],
    *,
    steps: int = STEPS_PER_BAR,
) -> EventMap:
    """Convert a step grid back to beat/velocity events."""
    from midi_beats.core.events import empty_event_map

    events = empty_event_map()
    step_len = 1.0 / SIXTEENTHS_PER_BEAT
    for inst, cells in grid.items():
        if inst not in events:
            continue
        for i, cell in enumerate(cells):
            if cell.on:
                t = i * step_len
                events[inst].append((t, cell.velocity or 100))
    return events
