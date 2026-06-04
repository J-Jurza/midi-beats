"""Pattern slots (BASE + mutations), phrase chains, and composition."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum

from midi_beats.core.events import (
    BEATS_PER_BAR,
    BEATS_PER_VARIATION,
    EventMap,
    empty_event_map,
    merge_event_maps,
    shift_events,
)

SLOT_BASE = "BASE"
SLOT_VAR_B = "B"
SLOT_VAR_C = "C"
SLOT_FILL1 = "FILL1"
SLOT_FILL2 = "FILL2"
CHAIN_LETTER_A = "A"

UI_VIEW_SLOTS = (SLOT_BASE, SLOT_VAR_B, SLOT_VAR_C, SLOT_FILL1, SLOT_FILL2)
VIEW_TO_CHAIN = {SLOT_BASE: CHAIN_LETTER_A, SLOT_VAR_B: "B", SLOT_VAR_C: "C"}


class ChainPreset(str, Enum):
    ABAC = "ABAC"
    AAAA = "AAAA"
    AABB = "AABB"
    AAAB = "AAAB"
    ABCB = "ABCB"
    ABBC = "ABBC"
    AABA = "AABA"
    ABCD = "ABCD"
    AAAC = "AAAC"
    BABC = "BABC"


CHAIN_SEQUENCES: dict[ChainPreset, tuple[str, ...]] = {
    ChainPreset.ABAC: ("A", "B", "A", "C"),
    ChainPreset.AAAA: ("A", "A", "A", "A"),
    ChainPreset.AABB: ("A", "B", "A", "B"),
    ChainPreset.AAAB: ("A", "A", "A", "B"),
    ChainPreset.ABCB: ("A", "B", "C", "B"),
    ChainPreset.ABBC: ("A", "B", "B", "C"),
    ChainPreset.AABA: ("A", "A", "B", "A"),
    ChainPreset.ABCD: ("A", "B", "C", "D"),
    ChainPreset.AAAC: ("A", "A", "A", "C"),
    ChainPreset.BABC: ("B", "A", "B", "C"),
}

CHAIN_LABELS: dict[ChainPreset, str] = {
    ChainPreset.ABAC: "A–B–A–C (classic)",
    ChainPreset.AAAA: "A–A–A–A (steady)",
    ChainPreset.AABB: "A–B–A–B (call-response)",
    ChainPreset.AAAB: "A–A–A–B (3 bars + fill)",
    ChainPreset.ABCB: "A–B–C–B (build & release)",
    ChainPreset.ABBC: "A–B–B–C (double variation)",
    ChainPreset.AABA: "A–A–B–A (bridge)",
    ChainPreset.ABCD: "A–B–C–D (all different)",
    ChainPreset.AAAC: "A–A–A–C (long build + fill)",
    ChainPreset.BABC: "B–A–B–C (variation lead-in)",
}


@dataclass
class AutoFillConfig:
    interval_bars: int = 4
    slot: str = SLOT_FILL1


def resolve_chain_preset(preset: ChainPreset | str | None) -> ChainPreset:
    if preset is None:
        return ChainPreset.ABAC
    if isinstance(preset, ChainPreset):
        return preset
    return ChainPreset(str(preset).upper())


@dataclass
class DrumPattern:
    genre: str
    slots: dict[str, EventMap] = field(default_factory=dict)
    chain: tuple[str, ...] = CHAIN_SEQUENCES[ChainPreset.ABAC]
    tempo: float = 120.0
    seed_base: int | None = None
    pattern_id: str | None = None
    auto_fill: AutoFillConfig | None = None
    chain_preset: ChainPreset = ChainPreset.ABAC

    def set_slot(self, name: str, events: EventMap) -> None:
        self.slots[name] = _normalize_bar(events)

    def get_slot(self, name: str) -> EventMap:
        key = _view_slot_key(name)
        return deepcopy(self.slots.get(key, empty_event_map()))

    def register_workflow_slots(self) -> None:
        if SLOT_BASE in self.slots:
            self.slots[CHAIN_LETTER_A] = deepcopy(self.slots[SLOT_BASE])
        if SLOT_VAR_B in self.slots:
            self.slots[SLOT_FILL1] = deepcopy(self.slots[SLOT_VAR_B])
        if SLOT_VAR_C in self.slots:
            self.slots[SLOT_FILL2] = deepcopy(self.slots[SLOT_VAR_C])

    def set_chain_preset(self, preset: ChainPreset | str) -> None:
        p = resolve_chain_preset(preset)
        self.chain_preset = p
        self.chain = CHAIN_SEQUENCES[p]

    def to_chain_events(self, sequence: tuple[str, ...] | None = None) -> EventMap:
        seq = sequence or self.chain
        combined = empty_event_map()
        for bar_index, letter in enumerate(seq):
            key = letter.upper()
            slot_events = self.slots.get(key)
            if not slot_events:
                continue
            merge_event_maps(
                combined,
                shift_events(slot_events, bar_index * BEATS_PER_BAR),
            )
        return combined

    def to_manifest_extras(self) -> dict:
        return {
            "pattern_model": "base_mutate_chain",
            "chain_preset": self.chain_preset.value,
            "chain": list(self.chain),
            "chain_label": CHAIN_LABELS.get(self.chain_preset, ""),
            "slots": sorted(self.slots.keys()),
            "ui_slots": list(UI_VIEW_SLOTS),
            "auto_fill": (
                {
                    "interval_bars": self.auto_fill.interval_bars,
                    "slot": self.auto_fill.slot,
                }
                if self.auto_fill
                else None
            ),
        }


def _view_slot_key(name: str) -> str:
    n = name.upper()
    if n == "BASE":
        return SLOT_BASE
    if n == "FILL1":
        return SLOT_VAR_B
    if n == "FILL2":
        return SLOT_VAR_C
    return n


def _normalize_bar(events: EventMap) -> EventMap:
    out = empty_event_map()
    for inst, evs in events.items():
        for t, vel in evs:
            if t < BEATS_PER_BAR:
                out[inst].append((t, vel))
            elif t < BEATS_PER_VARIATION:
                out[inst].append((t % BEATS_PER_BAR, vel))
    return out
