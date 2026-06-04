"""Genre registry and configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from midi_beats.core.events import EventMap, INSTRUMENTS
from midi_beats.genres.breaks import generate_breaks_events
from midi_beats.genres.dnb import generate_dnb_events
from midi_beats.genres.house import generate_house_events
from midi_beats.genres.ukg import generate_ukg_events

EventGenerator = Callable[..., EventMap]


@dataclass(frozen=True)
class GenreConfig:
    name: str
    generator: EventGenerator
    default_tempo: float
    instruments: tuple[str, ...]
    description: str = ""


GENRES: dict[str, GenreConfig] = {
    "house": GenreConfig(
        name="house",
        generator=generate_house_events,
        default_tempo=120.0,
        instruments=INSTRUMENTS,
        description="Four-on-the-floor house with syncopated kick and hat variations",
    ),
    "breaks": GenreConfig(
        name="breaks",
        generator=generate_breaks_events,
        default_tempo=130.0,
        instruments=("kick", "snare", "chh"),
        description="Breakbeat with ghost snares and amen-style bar C fills",
    ),
    "ukg": GenreConfig(
        name="ukg",
        generator=generate_ukg_events,
        default_tempo=132.0,
        instruments=INSTRUMENTS,
        description="UK garage 2-step with swung hat accent",
    ),
    "dnb": GenreConfig(
        name="dnb",
        generator=generate_dnb_events,
        default_tempo=174.0,
        instruments=("kick", "snare", "chh"),
        description="Drum & bass with 16th hats and ghost notes",
    ),
}


def list_genres() -> list[str]:
    return sorted(GENRES.keys())


def get_genre(name: str) -> GenreConfig:
    key = name.lower().strip()
    if key not in GENRES:
        supported = ", ".join(list_genres())
        raise ValueError(f"Unsupported genre '{name}'. Choose from: {supported}")
    return GENRES[key]
