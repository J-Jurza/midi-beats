"""Tests for TR-8 pattern model, grid, and library."""

import json
import tempfile
import unittest
from pathlib import Path

from midi_beats.core.grid import events_to_step_grid, step_grid_to_events
from midi_beats.core.pattern_model import ChainPreset, CHAIN_SEQUENCES
from midi_beats.genres.house import generate_house_pattern
from midi_beats.genres.registry import generate_pattern_for_genre
from midi_beats.library.seed_io import load_seed_json, seed_to_bar_events
from midi_beats.library.store import PatternStore


class TestPatternModel(unittest.TestCase):
    def test_slots_are_one_bar(self):
        pattern = generate_house_pattern(1, seed_base=1)
        for slot in ("A", "B", "C", "FILL1"):
            for inst, evs in pattern.get_slot(slot).items():
                for t, _ in evs:
                    self.assertLess(t, 4.0, msg=f"{slot}/{inst}")

    def test_abac_chain_length(self):
        pattern = generate_house_pattern(1, seed_base=2)
        events = pattern.to_chain_events()
        times = [t for evs in events.values() for t, _ in evs]
        self.assertGreater(max(times), 12.0)
        self.assertLess(max(times), 16.0)

    def test_manifest_extras(self):
        pattern = generate_pattern_for_genre("house", 1, 3)
        extras = pattern.to_manifest_extras()
        self.assertEqual(extras["chain"], list(CHAIN_SEQUENCES[ChainPreset.ABAC]))
        self.assertIn("FILL1", extras["slots"])


class TestGrid(unittest.TestCase):
    def test_round_trip(self):
        pattern = generate_house_pattern(1, seed_base=5)
        bar_a = pattern.get_slot("A")
        grid = events_to_step_grid(bar_a)
        back = step_grid_to_events(grid)
        for inst in ("kick", "snare"):
            self.assertEqual(
                sorted(t for t, _ in bar_a[inst]),
                sorted(t for t, _ in back[inst]),
            )


class TestLibrary(unittest.TestCase):
    def test_import_and_load_seed(self):
        seed_path = Path(__file__).resolve().parents[1] / "data/patterns/house/base_four_floor.json"
        seed = load_seed_json(seed_path)
        events = seed_to_bar_events(seed)
        self.assertIn(0.0, [t for t, _ in events["kick"]])

    def test_sqlite_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "test.db"
            store = PatternStore(db)
            seed_path = Path(__file__).resolve().parents[1] / "data/patterns/house/base_four_floor.json"
            pid = store.import_seed_file(seed_path)
            loaded = store.get_slot_events(pid, "A")
            self.assertTrue(loaded["kick"])


if __name__ == "__main__":
    unittest.main()
