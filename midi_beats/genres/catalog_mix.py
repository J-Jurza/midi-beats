"""Apply pattern library base grooves to generated patterns."""

from __future__ import annotations

from midi_beats.core.pattern_model import SLOT_BASE, DrumPattern


def apply_catalog_base(
    pattern: DrumPattern,
    catalog,
    genre: str,
    rng,
) -> None:
    """Replace BASE slot with a random catalog entry for this genre, if available."""
    if catalog is None:
        return
    pid = catalog.random_pattern_id(genre, rng)
    if not pid:
        return
    try:
        base_events = catalog.get_slot(pid, "A")
    except KeyError:
        return
    pattern.set_slot(SLOT_BASE, base_events)
    pattern.pattern_id = pid
    pattern.register_workflow_slots()
