"""Procedural electronic drum MIDI pattern generator."""

from midi_beats.pipeline import (
    generate_pattern,
    ExportConfig,
    ExportLayout,
    generate_events,
    generate_midi_patterns,
    export_midi,
)
from midi_beats.genres.registry import GENRES, list_genres

__version__ = "0.2.0"

__all__ = [
    "ExportConfig",
    "ExportLayout",
    "generate_events",
    "generate_pattern",
    "generate_midi_patterns",
    "export_midi",
    "GENRES",
    "list_genres",
    "__version__",
]
