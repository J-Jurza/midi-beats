"""CLI: python -m midi_beats house -o ./output -n 5 --seed 42"""

from __future__ import annotations

import argparse
import sys

from midi_beats.genres.registry import list_genres
from midi_beats.pipeline import ExportLayout, generate_midi_patterns


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate procedural drum MIDI patterns (ABAC loops)."
    )
    parser.add_argument(
        "genre",
        choices=list_genres(),
        help="Genre to generate",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Output directory",
    )
    parser.add_argument(
        "-n",
        "--variations",
        type=int,
        default=5,
        help="Number of variations (default: 5)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Base random seed for reproducibility",
    )
    parser.add_argument(
        "--tempo",
        type=float,
        default=None,
        help="Tempo BPM (default: genre-specific)",
    )
    parser.add_argument(
        "--velocity-var",
        type=int,
        default=15,
        help="Max velocity humanization (default: 15)",
    )
    parser.add_argument(
        "--timing-var",
        type=float,
        default=0.02,
        help="Max timing humanization in beats (default: 0.02)",
    )
    parser.add_argument(
        "--layout",
        choices=[e.value for e in ExportLayout],
        default=ExportLayout.PER_VARIATION.value,
        help="Export layout",
    )
    parser.add_argument(
        "--lock-backbeat",
        action="store_true",
        help="Keep kick/snare timing jitter aligned",
    )
    parser.add_argument(
        "--concatenated",
        action="store_true",
        help="Shortcut for --layout concatenated",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
    )
    parser.add_argument(
        "--all-genres",
        action="store_true",
        help="Generate all genres into the output directory",
    )

    args = parser.parse_args(argv)
    layout = (
        ExportLayout.CONCATENATED
        if args.concatenated
        else ExportLayout(args.layout)
    )

    genres = list_genres() if args.all_genres else [args.genre]

    for genre in genres:
        generate_midi_patterns(
            genre,
            args.output,
            num_variations=args.variations,
            velocity_var=args.velocity_var,
            timing_var=args.timing_var,
            tempo=args.tempo,
            seed_base=args.seed,
            verbose=args.verbose,
            layout=layout,
            lock_backbeat=args.lock_backbeat,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
