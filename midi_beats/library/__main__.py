"""Import JSON seeds: python -m midi_beats.library data/patterns"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from midi_beats.library.store import PatternStore


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import pattern seed JSON into SQLite")
    parser.add_argument(
        "directory",
        nargs="?",
        default="data/patterns",
        help="Directory of seed JSON files",
    )
    parser.add_argument("--db", default=None, help="SQLite database path")
    args = parser.parse_args(argv)

    store = PatternStore(args.db)
    ids = store.import_seed_directory(args.directory)
    print(f"Imported {len(ids)} patterns into {store.db_path}")
    for pid in ids:
        print(f"  {pid}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
