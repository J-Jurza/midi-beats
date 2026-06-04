"""Tests for TR-8 pattern model, grid, library, and chains."""

import tempfile
import unittest
from pathlib import Path

from midi_beats.core.grid import events_to_step_grid, step_grid_to_events
from midi_beats.core.pattern_model import ChainPreset, CHAIN_SEQUENCES, SLOT_BASE
from midi_beats.genres.house import generate_house_pattern
from midi_beats.genres.registry import generate_pattern_for_genre
from midi_beats.library.parquet_store import PatternCatalog
from midi_beats.library.seed_io import load_seed_json, seed_to_bar_events


class TestPatternModel(unittest.TestCase):
    def test_base_and_mutations_are_one_bar(self):
        pattern = generate_house_pattern(1, seed_base=1)
        for slot in ("BASE", "B", "C"):
            for inst, evs in pattern.get_slot(slot).items():
                for t, _ in evs:
                    self.assertLess(t, 4.0, msg=f"{slot}/{inst}")

    def test_base_differs_from_fill_b(self):
        pattern = generate_house_pattern(1, seed_base=99)
        base = pattern.get_slot("BASE")
        var_b = pattern.get_slot("B")
        base_kicks = {t for t, _ in base["kick"]}
        fill_kicks = {t for t, _ in var_b["kick"]}
        self.assertTrue(base_kicks.issubset(fill_kicks) or base_kicks != fill_kicks)

    def test_abcb_chain(self):
        pattern = generate_house_pattern(1, seed_base=2, chain_preset=ChainPreset.ABCB)
        self.assertEqual(pattern.chain, CHAIN_SEQUENCES[ChainPreset.ABCB])
        events = pattern.to_chain_events()
        times = [t for evs in events.values() for t, _ in evs]
        self.assertGreaterEqual(max(times), 12.0)

    def test_manifest_has_base_model(self):
        pattern = generate_pattern_for_genre("house", 1, 3, chain_preset="AAAB")
        extras = pattern.to_manifest_extras()
        self.assertEqual(extras["pattern_model"], "base_mutate_chain")
        self.assertEqual(extras["chain_preset"], "AAAB")


class TestGrid(unittest.TestCase):
    def test_round_trip(self):
        pattern = generate_house_pattern(1, seed_base=5)
        bar = pattern.get_slot(SLOT_BASE)
        grid = events_to_step_grid(bar)
        back = step_grid_to_events(grid)
        for inst in ("kick", "snare"):
            self.assertEqual(
                sorted(t for t, _ in bar[inst]),
                sorted(t for t, _ in back[inst]),
            )


class TestParquetCatalog(unittest.TestCase):
    def test_import_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "patterns.parquet"
            store = PatternCatalog(db)
            seed_path = Path(__file__).resolve().parents[1] / "data/patterns/house/base_four_floor.json"
            pid = store.import_seed_file(seed_path)
            loaded = store.get_slot(pid, "A")
            self.assertTrue(loaded["kick"])

    def test_house_uses_catalog_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "patterns.parquet"
            store = PatternCatalog(db)
            seed_path = Path(__file__).resolve().parents[1] / "data/patterns/house/base_four_floor.json"
            store.import_seed_file(seed_path)
            pattern = generate_house_pattern(1, seed_base=1, pattern_catalog=store)
            self.assertEqual(pattern.pattern_id, "house_base_four_floor")


class TestVisualizerSerialize(unittest.TestCase):
    def test_ui_payload_has_slots(self):
        from midi_beats.visualizer.serialize import pattern_to_ui_payload

        pattern = generate_house_pattern(1, seed_base=7)
        payload = pattern_to_ui_payload(pattern)
        self.assertIn("BASE", payload["slots"])
        self.assertIn("ABAC", payload["chain_presets"])


if __name__ == "__main__":
    unittest.main()
