"""Step grid conversion (TR-8 style: 16 sixteenth steps per bar)."""

from __future__ import annotations

from dataclasses import dataclass

from midi_beats.core.events import BEATS_PER_BAR, EventMap, INSTRUMENTS

STEPS_PER_BAR = 16
STEPS_PER_ABAC_CHAIN = STEPS_PER_BAR * 4


@dataclass
class StepCell:
    on: bool
    velocity: int | None = None


def beat_to_step(beat: float, steps_per_bar: int = STEPS_PER_BAR) -> int:
    """Map beat within a bar to step index 0..steps_per_bar-1."""
    beat_in_bar = beat % BEATS_PER_BAR
    step = int(round(beat_in_bar * (steps_per_bar / BEATS_PER_BAR)))
    return max(0, min(steps_per_bar - 1, step))


def events_to_step_grid(
    events: EventMap,
    *,
    steps: int = STEPS_PER_BAR,
    instruments: tuple[str, ...] | None = None,
) -> dict[str, list[StepCell]]:
    """
    Quantize one bar of events to a 16-step grid per instrument.

    Multiple hits on the same step keep the highest velocity.
    """
    insts = instruments or INSTRUMENTS
    grid: dict[str, list[StepCell]] = {
        inst: [StepCell(on=False) for _ in range(steps)] for inst in insts
    }

    for inst in insts:
        for beat, vel in events.get(inst, []):
            if beat >= BEATS_PER_BAR:
                continue
            idx = beat_to_step(beat, steps)
            cell = grid[inst][idx]
            if not cell.on or (cell.velocity or 0) < vel:
                grid[inst][idx] = StepCell(on=True, velocity=vel)

    return grid


def step_grid_to_events(
    grid: dict[str, list[StepCell]],
    *,
    steps_per_bar: int = STEPS_PER_BAR,
) -> EventMap:
    """Convert a 16-step grid back to beat/velocity events for one bar."""
    from midi_beats.core.events import empty_event_map

    events = empty_event_map()
    step_len = BEATS_PER_BAR / steps_per_bar
    for inst, cells in grid.items():
        if inst not in events:
            continue
        for i, cell in enumerate(cells):
            if cell.on:
                t = i * step_len
                events[inst].append((t, cell.velocity or 100))
    return events
