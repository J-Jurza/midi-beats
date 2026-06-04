"""Genre registry and configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from midi_beats.core.events import EventMap, INSTRUMENTS
from midi_beats.core.pattern_model import DrumPattern
from midi_beats.genres.breaks import generate_breaks_events, generate_breaks_pattern
from midi_beats.genres.dnb import generate_dnb_events, generate_dnb_pattern
from midi_beats.genres.house import generate_house_events, generate_house_pattern
from midi_beats.genres.ukg import generate_ukg_events, generate_ukg_pattern

EventGenerator = Callable[..., EventMap]
PatternGenerator = Callable[..., DrumPattern]


@dataclass(frozen=True)
class GenreConfig:
    name: str
    generator: EventGenerator
    pattern_generator: PatternGenerator
    default_tempo: float
    instruments: tuple[str, ...]
    description: str = ""


GENRES: dict[str, GenreConfig] = {
    "house": GenreConfig(
        name="house",
        generator=generate_house_events,
        pattern_generator=generate_house_pattern,
        default_tempo=120.0,
        instruments=INSTRUMENTS,
        description="Four-on-the-floor house with syncopated kick and hat variations",
    ),
    "breaks": GenreConfig(
        name="breaks",
        generator=generate_breaks_events,
        pattern_generator=generate_breaks_pattern,
        default_tempo=130.0,
        instruments=("kick", "snare", "chh"),
        description="Breakbeat with ghost snares and amen-style bar C fills",
    ),
    "ukg": GenreConfig(
        name="ukg",
        generator=generate_ukg_events,
        pattern_generator=generate_ukg_pattern,
        default_tempo=132.0,
        instruments=INSTRUMENTS,
        description="UK garage 2-step with swung hat accent",
    ),
    "dnb": GenreConfig(
        name="dnb",
        generator=generate_dnb_events,
        pattern_generator=generate_dnb_pattern,
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


def generate_pattern_for_genre(
    genre: str,
    variation_index: int = 1,
    seed_base: int | None = None,
) -> DrumPattern:
    return get_genre(genre).pattern_generator(
        variation_index=variation_index,
        seed_base=seed_base,
    )
