"""
Backward-compatible facade for midi_beats.

Prefer: ``from midi_beats import generate_midi_patterns, generate_events``
"""

from __future__ import annotations

from midi_beats.core.events import BEATS_PER_VARIATION, merge_event_maps, shift_events
from midi_beats.core.humanize import humanize_events as _humanize_events
from midi_beats.core.midi_export import build_midi_files
from midi_beats.genres.breaks import generate_breaks_events
from midi_beats.genres.dnb import generate_dnb_events
from midi_beats.genres.house import generate_house_events
from midi_beats.genres.ukg import generate_ukg_events
from midi_beats.pipeline import generate_events, generate_midi_patterns


def humanize_instrument_events(
    events_dict,
    velocity_variation=0,
    timing_variation=0.0,
    seed=None,
    lock_backbeat=False,
):
    """Legacy name; see ``midi_beats.core.humanize.humanize_events``."""
    _humanize_events(
        events_dict,
        velocity_variation=velocity_variation,
        timing_variation=timing_variation,
        seed=seed,
        lock_backbeat=lock_backbeat,
    )


def _legacy_generate(generator, num_variations=5, seed_base=None, variation_index=None):
    """Support old aggregated multi-variation API."""
    if variation_index is not None:
        return generator(variation_index=variation_index, seed_base=seed_base, base_offset=0.0)

    from midi_beats.core.events import empty_event_map

    combined = empty_event_map()
    for i in range(1, num_variations + 1):
        chunk = generator(variation_index=i, seed_base=seed_base, base_offset=0.0)
        merge_event_maps(combined, shift_events(chunk, (i - 1) * BEATS_PER_VARIATION))
    return combined


def generate_drum_events_house(num_variations=5, seed_base=None, variation_index=None):
    return _legacy_generate(generate_house_events, num_variations, seed_base, variation_index)


def generate_drum_events_ukg(num_variations=5, seed_base=None, variation_index=None):
    return _legacy_generate(generate_ukg_events, num_variations, seed_base, variation_index)


def generate_drum_events_dnb(num_variations=5, seed_base=None, variation_index=None):
    return _legacy_generate(generate_dnb_events, num_variations, seed_base, variation_index)


def generate_drum_events_breaks(num_variations=5, seed_base=None, variation_index=None):
    return _legacy_generate(generate_breaks_events, num_variations, seed_base, variation_index)


def create_house_patterns(output_dir, **kwargs):
    return generate_midi_patterns("house", output_dir, **kwargs)


def create_breaks_patterns(output_dir, **kwargs):
    return generate_midi_patterns("breaks", output_dir, **kwargs)


def create_ukg_patterns(output_dir, **kwargs):
    return generate_midi_patterns("ukg", output_dir, **kwargs)


def create_dnb_patterns(output_dir, **kwargs):
    return generate_midi_patterns("dnb", output_dir, **kwargs)


__all__ = [
    "humanize_instrument_events",
    "generate_drum_events_house",
    "generate_drum_events_ukg",
    "generate_drum_events_dnb",
    "generate_drum_events_breaks",
    "build_midi_files",
    "generate_midi_patterns",
    "generate_events",
    "create_house_patterns",
    "create_breaks_patterns",
    "create_ukg_patterns",
    "create_dnb_patterns",
]
