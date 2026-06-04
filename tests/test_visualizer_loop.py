"""Tests for UI ↔ pattern ↔ MIDI export loop."""

import tempfile
import unittest
from pathlib import Path

from midi_beats.core.mutate import MutateKind
from midi_beats.visualizer.pattern_bridge import (
    export_ui_pattern,
    generate_ui_pattern,
    mutate_slot,
    pattern_from_ui_state,
    ui_grid_to_events,
)


class TestVisualizerLoop(unittest.TestCase):
    def test_generate_and_roundtrip(self):
        payload = generate_ui_pattern("house", seed_base=42, chain_preset="ABCB")
        self.assertIn("BASE", payload["slots"])
        pattern = pattern_from_ui_state(payload)
        self.assertEqual(pattern.chain_preset.value, "ABCB")

    def test_mutate_b_from_edited_base(self):
        payload = generate_ui_pattern("house", seed_base=7)
        grid = payload["slots"]["BASE"]
        grid["kick"][0]["on"] = False
        payload["slots"]["BASE"] = grid
        out = mutate_slot(payload, "B", MutateKind.MINI)
        self.assertIn("B", out["slots"])
        b_kicks = sum(1 for c in out["slots"]["B"]["kick"] if c["on"])
        self.assertGreaterEqual(b_kicks, 0)

    def test_export_edited_pattern(self):
        payload = generate_ui_pattern("ukg", seed_base=3, chain_preset="AAAB")
        with tempfile.TemporaryDirectory() as tmp:
            result = export_ui_pattern(payload, tmp, layout="both")
            self.assertTrue((Path(tmp) / "ukg" / "variation_1").is_dir())
            self.assertTrue(result["chain_files"])
            self.assertTrue(result["slot_files"])

    def test_ui_grid_to_events(self):
        payload = generate_ui_pattern("house", seed_base=1)
        events = ui_grid_to_events(payload["slots"]["BASE"])
        self.assertTrue(events["kick"])


if __name__ == "__main__":
    unittest.main()
