"""Pattern library CLI.

  python -m midi_beats.library build --generate
  python -m midi_beats.library ingest data/patterns
"""

from __future__ import annotations

import argparse
import json
import sys

from midi_beats.library.ingest import (
    build_pattern_library,
    ingest_json_directory,
    load_default_catalog,
)
from midi_beats.library.parquet_store import PatternCatalog


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="MIDI Beats pattern library (Parquet)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build", help="Generate JSON seeds + ingest to Parquet")
    p_build.add_argument(
        "--json-dir",
        default="data/patterns",
        help="Directory for JSON seed files",
    )
    p_build.add_argument(
        "--parquet",
        default=None,
        help="Parquet catalog path (default: data/patterns.parquet)",
    )
    p_build.add_argument(
        "--generate",
        action="store_true",
        help="Generate procedural BASE seeds per genre before ingest",
    )
    p_build.add_argument(
        "--per-genre",
        type=int,
        default=5,
        help="Procedural seeds per genre when --generate",
    )
    p_build.add_argument("--seed-start", type=int, default=1000)

    p_ingest = sub.add_parser("ingest", help="Ingest JSON directory into Parquet")
    p_ingest.add_argument(
        "directory",
        nargs="?",
        default="data/patterns",
    )
    p_ingest.add_argument("--parquet", default=None)

    p_list = sub.add_parser("list", help="List patterns in catalog")
    p_list.add_argument("--genre", default=None)
    p_list.add_argument("--parquet", default=None)

    args = parser.parse_args(argv)

    if args.command == "build":
        summary = build_pattern_library(
            args.json_dir,
            args.parquet,
            generate=args.generate,
            generate_per_genre=args.per_genre,
            seed_start=args.seed_start,
        )
        print(json.dumps(summary, indent=2))
        return 0

    if args.command == "ingest":
        catalog = PatternCatalog(args.parquet)
        ids = ingest_json_directory(args.directory, catalog)
        print(f"Imported {len(ids)} slot records → {catalog.path}")
        for pid in sorted(set(ids)):
            print(f"  {pid}")
        return 0

    if args.command == "list":
        catalog = PatternCatalog(args.parquet) if args.parquet else load_default_catalog()
        if catalog is None:
            print("No catalog found. Run: python -m midi_beats.library build --generate")
            return 1
        rows = catalog.list_patterns(genre=args.genre)
        for row in rows:
            print(f"{row['pattern_id']} ({row['genre']})")
        print(f"Total: {len(rows)}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
