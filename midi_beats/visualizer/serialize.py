"""Serialize DrumPattern for the web UI."""

from __future__ import annotations

from midi_beats.core.events import INSTRUMENTS
from midi_beats.core.grid import STEPS_PER_ABAC_CHAIN, STEPS_PER_BAR, events_to_step_grid
from midi_beats.core.pattern_model import (
    CHAIN_LABELS,
    CHAIN_SEQUENCES,
    ChainPreset,
    DrumPattern,
    UI_VIEW_SLOTS,
)


def _grid_to_json(grid: dict) -> dict:
    out = {}
    for inst, cells in grid.items():
        out[inst] = [
            {"on": c.on, "vel": c.velocity if c.on else None}
            for c in cells
        ]
    return out


def _phrase_bar_markers(chain: list[str], steps_per_bar: int = STEPS_PER_BAR) -> list[str]:
    markers = []
    for bar_i, letter in enumerate(chain):
        for _ in range(steps_per_bar):
            markers.append(letter)
    return markers


def pattern_to_ui_payload(
    pattern: DrumPattern,
    *,
    base_edited: bool = False,
) -> dict:
    """JSON-serializable pattern for the step sequencer UI."""
    slots = {}
    for slot in UI_VIEW_SLOTS:
        ev = pattern.get_slot(slot)
        if any(evs for evs in ev.values()):
            slots[slot] = _grid_to_json(events_to_step_grid(ev))

    chain_events = pattern.to_chain_events()
    phrase_grid = _grid_to_json(
        events_to_step_grid(
            chain_events,
            steps=STEPS_PER_ABAC_CHAIN,
            max_beat=16.0,
        )
    )

    chain_presets = {
        p.value: {
            "sequence": list(CHAIN_SEQUENCES[p]),
            "label": CHAIN_LABELS.get(p, p.value),
        }
        for p in ChainPreset
    }

    has_variations = bool(slots.get("B") or slots.get("C"))

    return {
        "genre": pattern.genre,
        "tempo": pattern.tempo,
        "pattern_id": pattern.pattern_id,
        "seed_base": pattern.seed_base,
        "steps_per_bar": STEPS_PER_BAR,
        "phrase_steps": STEPS_PER_ABAC_CHAIN,
        "bars": len(pattern.chain),
        "chain_preset": pattern.chain_preset.value,
        "chain": list(pattern.chain),
        "chain_label": CHAIN_LABELS.get(pattern.chain_preset, ""),
        "chain_presets": chain_presets,
        "phrase_bar_markers": _phrase_bar_markers(list(pattern.chain)),
        "active_slot": "BASE",
        "view_mode": "slot",
        "slots": slots,
        "phrase": phrase_grid,
        "instruments": list(INSTRUMENTS),
        "base_edited": base_edited,
        "mutate_recommended": base_edited and has_variations,
        "catalog_patterns": None,
    }
