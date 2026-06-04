"""TR-8-inspired pattern slots, chains, and composition."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable

from midi_beats.core.events import (
    BEATS_PER_BAR,
    BEATS_PER_VARIATION,
    EventMap,
    empty_event_map,
    merge_event_maps,
    shift_events,
)

# Roland TR-8S: 8 variations + 2 fills per pattern (we model all slots; use subset in UI)
VARIATION_SLOTS = ("A", "B", "C", "D", "E", "F", "G", "H")
FILL_SLOTS = ("FILL1", "FILL2")
ALL_SLOTS = (*VARIATION_SLOTS, *FILL_SLOTS)


class ChainPreset(str, Enum):
    """Common playback chains (bars)."""
    ABAC = "ABAC"
    AAAA = "AAAA"
    AABB = "AABB"
    AAAB = "AAAB"
    TR8_DEFAULT = "ABAC"  # our historical default export


CHAIN_SEQUENCES: dict[ChainPreset, tuple[str, ...]] = {
    ChainPreset.ABAC: ("A", "B", "A", "C"),
    ChainPreset.AAAA: ("A", "A", "A", "A"),
    ChainPreset.AABB: ("A", "B", "A", "B"),
    ChainPreset.AAAB: ("A", "A", "A", "B"),
}


@dataclass
class AutoFillConfig:
    """TR-8 Auto Fill In metadata (for manifest / future live engine)."""
    interval_bars: int = 4
    slot: str = "FILL1"


@dataclass
class DrumPattern:
    """
    One pattern: multiple 1-bar slots + optional chain for export.

    Each slot holds events in beat range [0, 4) — one bar, TR-8 style.
    """
    genre: str
    slots: dict[str, EventMap] = field(default_factory=dict)
    chain: tuple[str, ...] = CHAIN_SEQUENCES[ChainPreset.ABAC]
    tempo: float = 120.0
    seed_base: int | None = None
    pattern_id: str | None = None
    auto_fill: AutoFillConfig | None = None

    def set_slot(self, name: str, events: EventMap) -> None:
        self.slots[name] = _normalize_bar(events)

    def get_slot(self, name: str) -> EventMap:
        return deepcopy(self.slots.get(name, empty_event_map()))

    def clone_slot(self, src: str, dest: str) -> None:
        self.slots[dest] = deepcopy(self.slots[src])

    def to_chain_events(self, sequence: tuple[str, ...] | None = None) -> EventMap:
        """Merge slots into a multi-bar EventMap (e.g. 4 bars for ABAC)."""
        seq = sequence or self.chain
        combined = empty_event_map()
        for bar_index, slot_name in enumerate(seq):
            slot_events = self.slots.get(slot_name)
            if not slot_events:
                continue
            merge_event_maps(
                combined,
                shift_events(slot_events, bar_index * BEATS_PER_BAR),
            )
        return combined

    def to_manifest_extras(self) -> dict:
        return {
            "pattern_model": "tr8_slots",
            "chain": list(self.chain),
            "slots": list(self.slots.keys()),
            "auto_fill": (
                {
                    "interval_bars": self.auto_fill.interval_bars,
                    "slot": self.auto_fill.slot,
                }
                if self.auto_fill
                else None
            ),
        }


def _normalize_bar(events: EventMap) -> EventMap:
    """Keep only first-bar hits, normalize to beat 0."""
    out = empty_event_map()
    for inst, evs in events.items():
        for t, vel in evs:
            if t < BEATS_PER_BAR:
                out[inst].append((t, vel))
            elif t < BEATS_PER_VARIATION:
                out[inst].append((t % BEATS_PER_BAR, vel))
    return out


def extract_bar(events: EventMap, bar_index: int) -> EventMap:
    """Extract one bar from a multi-bar event map into slot-ready events (0–4 beats)."""
    start = bar_index * BEATS_PER_BAR
    end = start + BEATS_PER_BAR
    out = empty_event_map()
    for inst, evs in events.items():
        for t, vel in evs:
            if start <= t < end:
                out[inst].append((t - start, vel))
    return out


def build_pattern_from_bars(
    genre: str,
    bar_builders: dict[str, Callable[[], None]],
    chain: tuple[str, ...] = CHAIN_SEQUENCES[ChainPreset.ABAC],
    *,
    tempo: float = 120.0,
    seed_base: int | None = None,
    pattern_id: str | None = None,
    fill2_slot: str = "C",
) -> DrumPattern:
    """
    Build a DrumPattern from bar builder callbacks.

    Each builder receives a fresh EventMap and writes one bar at offset 0.
    Keys in bar_builders map slot names (A, B, C, FILL1, …) to builder fn.
    """
    pattern = DrumPattern(
        genre=genre,
        chain=chain,
        tempo=tempo,
        seed_base=seed_base,
        pattern_id=pattern_id,
        auto_fill=AutoFillConfig(interval_bars=4, slot="FILL1"),
    )
    for slot_name, builder in bar_builders.items():
        bar_events = empty_event_map()
        builder(bar_events)
        pattern.set_slot(slot_name, bar_events)

    # TR-8: Fill2 often maps to our heaviest bar (historically C)
    if fill2_slot in pattern.slots and "FILL2" not in pattern.slots:
        pattern.set_slot("FILL2", pattern.get_slot(fill2_slot))

    if "FILL1" not in pattern.slots and "B" in pattern.slots:
        pattern.set_slot("FILL1", pattern.get_slot("B"))

    return pattern


