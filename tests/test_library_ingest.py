"""Pattern library ingest and build tests."""

import tempfile
import unittest
from pathlib import Path

from midi_beats.library.ingest import build_pattern_library, ingest_json_directory
from midi_beats.library.parquet_store import PatternCatalog
from midi_beats.library.seed_io import load_seed_json, validate_seed
from midi_beats.genres.registry import generate_pattern_for_genre
from midi_beats.library.ingest import load_default_catalog


class TestLibraryIngest(unittest.TestCase):
    def test_validate_seed(self):
        path = Path(__file__).resolve().parents[1] / "data/patterns/house/base_four_floor.json"
        validate_seed(load_seed_json(path))

    def test_build_library_with_generate(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_dir = Path(tmp) / "patterns"
            pq = Path(tmp) / "lib.parquet"
            summary = build_pattern_library(
                json_dir,
                pq,
                generate=True,
                generate_per_genre=2,
                seed_start=5000,
            )
            self.assertGreaterEqual(summary["total_patterns"], 4)
            self.assertTrue(pq.is_file())
            cat = PatternCatalog(pq)
            self.assertGreater(len(cat.list_patterns(genre="house")), 0)

    def test_catalog_used_for_ukg(self):
        with tempfile.TemporaryDirectory() as tmp:
            json_dir = Path(tmp) / "patterns"
            pq = Path(tmp) / "lib.parquet"
            build_pattern_library(json_dir, pq, generate=True, generate_per_genre=1, seed_start=8000)
            cat = PatternCatalog(pq)
            p = generate_pattern_for_genre("ukg", 1, 99, pattern_catalog=cat)
            if cat.list_patterns(genre="ukg"):
                self.assertTrue(p.pattern_id)


class TestPhraseGrid(unittest.TestCase):
    def test_phrase_grid_64_steps(self):
        from midi_beats.visualizer.serialize import pattern_to_ui_payload

        payload = pattern_to_ui_payload(
            generate_pattern_for_genre("house", 1, 42, chain_preset="ABCB")
        )
        self.assertEqual(len(payload["phrase"]["kick"]), 64)
        self.assertEqual(len(payload["phrase_bar_markers"]), 64)


if __name__ == "__main__":
    unittest.main()
