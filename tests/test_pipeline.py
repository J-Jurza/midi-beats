"""Tests for midi_beats pipeline and timing correctness."""

import json
import os
import tempfile
import unittest

from midi_beats.core.events import BEATS_PER_VARIATION
from midi_beats.core.humanize import humanize_events
from midi_beats.genres.registry import list_genres
from midi_beats.pipeline import ExportLayout, generate_events, generate_midi_patterns


class TestVariationTiming(unittest.TestCase):
    def test_variation_starts_at_beat_zero(self):
        for genre in list_genres():
            for var in (1, 2, 3):
                events = generate_events(genre, variation_index=var, seed_base=42)
                all_times = [t for evs in events.values() for t, _ in evs]
                if all_times:
                    self.assertGreaterEqual(min(all_times), 0.0, genre)
                    self.assertLess(min(all_times), BEATS_PER_VARIATION, genre)

    def test_variation_two_kick_not_at_sixteen(self):
        events = generate_events("house", variation_index=2, seed_base=42)
        kick_times = [t for t, _ in events["kick"]]
        self.assertTrue(all(t < BEATS_PER_VARIATION for t in kick_times))
        self.assertNotIn(16.0, kick_times)


class TestReproducibility(unittest.TestCase):
    def test_seeded_humanize_is_stable(self):
        e1 = generate_events("dnb", 1, seed_base=99)
        e2 = generate_events("dnb", 1, seed_base=99)
        humanize_events(e1, 10, 0.02, seed=10999)
        humanize_events(e2, 10, 0.02, seed=10999)
        self.assertEqual(e1, e2)


class TestExport(unittest.TestCase):
    def test_per_variation_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = generate_midi_patterns(
                "house",
                tmp,
                num_variations=2,
                seed_base=1,
                verbose=False,
            )
            self.assertEqual(set(result.keys()), {1, 2})
            manifest_path = os.path.join(tmp, "house", "variation_1", "manifest.json")
            self.assertTrue(os.path.isfile(manifest_path))
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
            self.assertEqual(manifest["beats"], 16)
            self.assertEqual(manifest["structure"], "ABAC")

    def test_breaks_generates(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = generate_midi_patterns("breaks", tmp, num_variations=1, seed_base=7)
            self.assertIn(1, result)
            self.assertIn("kick", result[1])

    def test_dnb_skips_empty_clap(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = generate_midi_patterns("dnb", tmp, num_variations=1, seed_base=3)
            self.assertNotIn("clap", result[1])


class TestGenres(unittest.TestCase):
    def test_all_genres_registered(self):
        self.assertEqual(
            set(list_genres()),
            {"breaks", "dnb", "house", "ukg"},
        )


if __name__ == "__main__":
    unittest.main()
