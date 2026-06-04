"""MIDI file construction from event maps."""

from __future__ import annotations

from midiutil import MIDIFile

from midi_beats.core.events import EventMap, GM_DRUM_MAP


def build_midi_files(
    events: EventMap,
    tempo: float = 120.0,
    gm_mapping: dict[str, int] | None = None,
    skip_empty: bool = True,
) -> dict[str, MIDIFile]:
    """
    Convert an event map into one MIDIFile per instrument.

    Parameters:
        skip_empty: Omit instruments with no hits (reduces empty DAW lanes).
    """
    mapping = gm_mapping or GM_DRUM_MAP
    midi_files: dict[str, MIDIFile] = {}

    for instrument, ev_list in events.items():
        if instrument not in mapping:
            continue
        if skip_empty and not ev_list:
            continue

        ev_list.sort(key=lambda x: x[0])
        midi = MIDIFile(1)
        midi.addTempo(track=0, time=0, tempo=tempo)
        note = mapping[instrument]
        for t, vel in ev_list:
            midi.addNote(
                track=0,
                channel=9,
                pitch=note,
                time=t,
                duration=0.1,
                volume=vel,
            )
        midi_files[instrument] = midi

    return midi_files
