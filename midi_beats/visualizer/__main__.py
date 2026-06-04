"""Launch UI: python -m midi_beats.visualizer [--port 8765]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from midi_beats.library.parquet_store import PatternCatalog
from midi_beats.visualizer.server import run_server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MIDI Beats step sequencer UI")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--import-seeds", action="store_true", help="Import JSON seeds into Parquet first")
    args = parser.parse_args(argv)

    catalog = PatternCatalog()
    seed_dir = Path(__file__).resolve().parents[2] / "data" / "patterns"
    if args.import_seeds or not catalog.path.is_file():
        if seed_dir.is_dir():
            n = catalog.import_seed_directory(seed_dir)
            print(f"Imported {len(n)} seed(s) → {catalog.path}")

    run_server(args.host, args.port, catalog)
    return 0


if __name__ == "__main__":
    sys.exit(main())
