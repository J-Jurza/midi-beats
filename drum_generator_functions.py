# drum_pattern_generator.py

"""
A self-contained MIDI drum pattern generator for multiple genres (House,
Breaks, UK Garage, Drum & Bass). Each function receives all required parameters
(explicit GM note numbers, output directories, etc.) so there are no
external global dependencies. Output directories are also passed in,
allowing flexible organisation of generated MIDI files.
"""

import os
import random
import datetime
from midiutil import MIDIFile


def prepare_output_directory(base_path):
    """
    Create a dated subfolder in a user-specified base_path.
    Test write permissions by creating and deleting a temporary test file.

    Args:
        base_path (str): Top-level folder where the dated subfolder will be created.

    Returns:
        str: Full path to the newly created dated subfolder.

    Raises:
        Exception: If the test file cannot be written or verified.
    """
    today_str = datetime.datetime.now().strftime("%Y_%m_%d")
    output_dir = os.path.join(base_path, today_str)
    os.makedirs(output_dir, exist_ok=True)

    test_filename = "test_midi_clip.txt"
    test_filepath = os.path.join(output_dir, test_filename)

    try:
        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write("MIDI data (placeholder)")

        if not os.path.exists(test_filepath):
            raise Exception("Test file was not created.")

        os.remove(test_filepath)
        print(f"Output directory verified: {output_dir}")
        return output_dir
    except Exception as exc:
        raise Exception(f"Failed to verify output directory: {exc}")


def humanize_events(events, velocity_variation=0, timing_variation=0.0):
    """
    Apply random velocity and timing offsets to each MIDI event (humanization).

    Args:
        events (dict[str, list[tuple[float, int, int]]]): Dictionary of instrument -> list of (time, note, velocity).
        velocity_variation (int): Maximum random ±offset for velocity. 0 for no variation.
        timing_variation (float): Maximum random ±offset for timing in beats. 0 for no variation.

    Returns:
        None; modifies the 'events' list in-place.
    """
    for instrument, notes in events.items():
        for i, (time, note, vel) in enumerate(notes):
            if velocity_variation > 0:
                vel += random.randint(-velocity_variation, velocity_variation)
                vel = max(1, min(127, vel))
            if timing_variation > 0:
                time += random.uniform(-timing_variation, timing_variation)
                if time < 0:
                    time = 0
            notes[i] = (time, note, vel)


def save_midi_files(
        events, output_dir, genre, tempo, variation_str="var_01", channel=9
    ):
    """
    Save the events dict to separate MIDI files per instrument within the specified folder.

    Args:
        events (dict[str, list[tuple[float, int, int]]]): Mapping of instrument name
            to list of (time, note, velocity) events.
        output_dir (str): Base directory where MIDI files are saved.
        genre (str): Genre name, used to name the subfolder (e.g. 'house', 'breaks').
        tempo (float): Tempo in BPM for the MIDI file.
        variation_str (str): A folder/label for each variation (e.g. 'var_05').
        channel (int): MIDI channel to use for all drum notes (9 is typical for drums).

    Returns:
        None; writes MIDI files to disk.
    """
    variation_path = os.path.join(output_dir, genre, variation_str)
    os.makedirs(variation_path, exist_ok=True)

    for instrument, notes in events.items():
        midi_filename = f"{genre}_{instrument}.mid"
        file_path = os.path.join(variation_path, midi_filename)

        midi = MIDIFile(numTracks=1)
        midi.addTempo(track=0, time=0, tempo=tempo)

        for (time, note, vel) in notes:
            # We'll use a short fixed duration for drum hits (0.1 beats).
            midi.addNote(
                track=0,
                channel=channel,
                pitch=note,
                time=time,
                duration=0.1,
                volume=vel
            )

        with open(file_path, "wb") as f:
            midi.writeFile(f)


def create_house_patterns(
        output_dir,
        gm_kick=36, gm_snare=38, gm_clap=39, gm_chh=42, gm_ohh=46,
        num_variations=10,
        velocity_var=15,
        timing_var=0.02,
        tempo=120.0
    ):
    """
    Generate and save House drum pattern variations (4 bars each, with a fill on bar 4).
    Each instrument's events are saved in separate MIDI clips in a subfolder.

    Args:
        output_dir (str): Base directory for output.
        gm_kick (int): MIDI note for Kick.
        gm_snare (int): MIDI note for Snare.
        gm_clap (int): MIDI note for Clap.
        gm_chh (int): MIDI note for Closed Hi-Hat.
        gm_ohh (int): MIDI note for Open Hi-Hat.
        num_variations (int): How many variations to generate.
        velocity_var (int): Maximum random ±offset for velocity.
        timing_var (float): Maximum random ±offset for timing (in beats).
        tempo (float): BPM for the generated MIDI file.

    Returns:
        None; writes out 1..num_variations subfolders with separate .mid files.
    """
    genre = "house"
    for variation in range(1, num_variations + 1):
        random.seed(1000 + variation)

        kick_pattern = [0.0, 1.0, 2.0, 3.0]
        snare_pattern = [1.0, 3.0]
        clap_pattern = [1.0, 3.0]
        ohh_pattern = [0.5, 1.5, 2.5, 3.5]

        # Randomly choose closed-hat resolution (16th or 8th)
        if random.random() < 0.5:
            chh_pattern = [i * 0.25 for i in range(16)]
        else:
            chh_pattern = [i * 0.5 for i in range(8)]

        events = {
            "kick": [],
            "snare": [],
            "clap": [],
            "hats": []
        }

        # Bars 1-3
        for bar in range(3):
            offset = bar * 4.0
            for t in kick_pattern:
                events["kick"].append((offset + t, gm_kick, 100))
            for t in snare_pattern:
                events["snare"].append((offset + t, gm_snare, 110))
            for t in clap_pattern:
                events["clap"].append((offset + t, gm_clap, 110))
            for t in chh_pattern:
                events["hats"].append((offset + t, gm_chh, 90))
            for t in ohh_pattern:
                events["hats"].append((offset + t, gm_ohh, 100))

        # Bar 4 (including fill)
        offset = 3 * 4.0
        for t in kick_pattern:
            events["kick"].append((offset + t, gm_kick, 100))
        for t in snare_pattern:
            events["snare"].append((offset + t, gm_snare, 110))
        for t in clap_pattern:
            events["clap"].append((offset + t, gm_clap, 110))
        for t in chh_pattern:
            events["hats"].append((offset + t, gm_chh, 90))
        for t in ohh_pattern:
            events["hats"].append((offset + t, gm_ohh, 100))

        # Decide fill type
        if random.random() < 0.5:
            # Snare roll fill
            for t in [offset + 3.25, offset + 3.5, offset + 3.75]:
                events["snare"].append((t, gm_snare, 100))
        else:
            # Kick fill
            events["kick"].append((offset + 3.5, gm_kick, 100))
            events["kick"].append((offset + 3.75, gm_kick, 100))

        # Humanize & save
        humanize_events(events, velocity_variation=velocity_var,
                        timing_variation=timing_var)
        var_str = f"var_{variation:02d}"
        save_midi_files(events, output_dir, genre, tempo, var_str)


def create_breaks_patterns(
        output_dir,
        gm_kick=36, gm_snare=38, gm_chh=42,
        num_variations=10,
        velocity_var=15,
        timing_var=0.02,
        tempo=130.0
    ):
    """
    Generate and save Breakbeat pattern variations (4 bars with a fill on bar 4).
    Each instrument's events are saved in separate MIDI clips in a subfolder.

    Args:
        output_dir (str): Base directory for output.
        gm_kick (int): MIDI note for Kick.
        gm_snare (int): MIDI note for Snare.
        gm_chh (int): MIDI note for Closed Hi-Hat (or Ride).
        num_variations (int): Number of pattern variations.
        velocity_var (int): Max random ±offset for velocity.
        timing_var (float): Max random ±offset for timing (in beats).
        tempo (float): BPM for the generated MIDI file.

    Returns:
        None
    """
    genre = "breaks"
    for variation in range(1, num_variations + 1):
        random.seed(2000 + variation)

        kick_pattern = [0.0, 2.5]
        snare_pattern = [1.0, 3.0]
        ghost_snare_positions = [1.25, 2.75]
        ghost_kick_positions = []
        if random.random() < 0.5:
            ghost_kick_positions.append(3.5)  # Kick on 'and' of 4

        hat_pattern = [i * 0.5 for i in range(8)]

        events = {
            "kick": [],
            "snare": [],
            "hats": []
        }

        # Bars 1-3
        for bar in range(3):
            offset = bar * 4.0
            for t in kick_pattern:
                events["kick"].append((offset + t, gm_kick, 100))
            for t in snare_pattern:
                events["snare"].append((offset + t, gm_snare, 110))
            for t in ghost_snare_positions:
                events["snare"].append((offset + t, gm_snare, 70))
            for t in ghost_kick_positions:
                events["kick"].append((offset + t, gm_kick, 80))
            for t in hat_pattern:
                events["hats"].append((offset + t, gm_chh, 100))

        # Bar 4 w/ fill
        offset = 3 * 4.0
        for t in kick_pattern:
            events["kick"].append((offset + t, gm_kick, 100))
        for t in snare_pattern:
            events["snare"].append((offset + t, gm_snare, 110))
        for t in ghost_snare_positions:
            events["snare"].append((offset + t, gm_snare, 70))
        for t in ghost_kick_positions:
            events["kick"].append((offset + t, gm_kick, 80))
        for t in hat_pattern:
            events["hats"].append((offset + t, gm_chh, 100))

        # Amen-style fill or simpler fill
        if random.random() < 0.5:
            # Amen fill
            events["kick"] = [
                n for n in events["kick"]
                if not (n[0] == offset and n[1] == gm_kick)
            ]
            events["snare"].append((offset + 0.0, gm_snare, 100))
            events["snare"].append((offset + 0.25, gm_snare, 90))
            events["kick"].append((offset + 0.5, gm_kick, 100))
            # Shift final snare
            events["snare"] = [
                n for n in events["snare"]
                if not (n[0] == offset + 3.0 and n[1] == gm_snare)
            ]
            events["snare"].append((offset + 3.5, gm_snare, 110))
        else:
            # Simpler fill
            if random.random() < 0.5:
                # Snare roll
                for t in [offset + 3.25, offset + 3.5, offset + 3.75]:
                    events["snare"].append((t, gm_snare, 100))
            else:
                # Double kick
                events["kick"].append((offset + 3.5, gm_kick, 100))
                events["kick"].append((offset + 3.75, gm_kick, 100))

        humanize_events(events, velocity_variation=velocity_var,
                        timing_variation=timing_var)
        var_str = f"var_{variation:02d}"
        save_midi_files(events, output_dir, genre, tempo, var_str)


def create_ukg_patterns(
        output_dir,
        gm_kick=36, gm_snare=38, gm_clap=39, gm_chh=42, gm_ohh=46,
        num_variations=10,
        velocity_var=15,
        timing_var=0.02,
        tempo=132.0
    ):
    """
    Generate and save UK Garage (2-Step) drum pattern variations (4 bars w/ fill on bar 4).

    Args:
        output_dir (str): Base directory for output.
        gm_kick (int): MIDI note for Kick.
        gm_snare (int): MIDI note for Snare.
        gm_clap (int): MIDI note for Clap.
        gm_chh (int): MIDI note for Closed Hi-Hat.
        gm_ohh (int): MIDI note for Open Hi-Hat.
        num_variations (int): Number of pattern variations.
        velocity_var (int): Max random ±offset for velocity.
        timing_var (float): Max random ±offset for timing (in beats).
        tempo (float): BPM for the generated MIDI file.

    Returns:
        None
    """
    genre = "ukg"
    for variation in range(1, num_variations + 1):
        random.seed(3000 + variation)

        kick_pattern = [0.0, 2.5]
        snare_pattern = [1.0, 3.0]
        clap_pattern = [1.0, 3.0]

        open_hat_pattern = [0.5, 1.5, 3.5]
        closed_hat_pattern = [0.0, 1.0, 2.0, 3.0]
        swung_hat = 2.25

        extra_ghost_kick = None
        if random.random() < 0.5:
            extra_ghost_kick = 1.75

        events = {
            "kick": [],
            "snare": [],
            "clap": [],
            "hats": []
        }

        # Bars 1-3
        for bar in range(3):
            offset = bar * 4.0
            for t in kick_pattern:
                events["kick"].append((offset + t, gm_kick, 100))
            for t in snare_pattern:
                events["snare"].append((offset + t, gm_snare, 110))
            for t in clap_pattern:
                events["clap"].append((offset + t, gm_clap, 110))
            for t in closed_hat_pattern:
                events["hats"].append((offset + t, gm_chh, 90))
            for t in open_hat_pattern:
                events["hats"].append((offset + t, gm_ohh, 100))

            # Swung closed hat
            events["hats"].append((offset + swung_hat, gm_chh, 80))
            # Extra ghost kick
            if extra_ghost_kick is not None:
                events["kick"].append((offset + extra_ghost_kick, gm_kick, 60))

        # Bar 4 with fill
        offset = 3 * 4.0
        for t in kick_pattern:
            events["kick"].append((offset + t, gm_kick, 100))
        for t in snare_pattern:
            events["snare"].append((offset + t, gm_snare, 110))
        for t in clap_pattern:
            events["clap"].append((offset + t, gm_clap, 110))
        for t in closed_hat_pattern:
            events["hats"].append((offset + t, gm_chh, 90))
        for t in open_hat_pattern:
            events["hats"].append((offset + t, gm_ohh, 100))
        events["hats"].append((offset + swung_hat, gm_chh, 80))
        if extra_ghost_kick is not None:
            events["kick"].append((offset + extra_ghost_kick, gm_kick, 60))

        # Fill: snare roll or double kick
        if random.random() < 0.5:
            for t in [offset + 3.25, offset + 3.5, offset + 3.75]:
                events["snare"].append((t, gm_snare, 100))
        else:
            events["kick"].append((offset + 3.5, gm_kick, 100))
            events["kick"].append((offset + 3.75, gm_kick, 100))

        humanize_events(events, velocity_variation=velocity_var,
                        timing_variation=timing_var)
        var_str = f"var_{variation:02d}"
        save_midi_files(events, output_dir, genre, tempo, var_str)


def create_dnb_patterns(
        output_dir,
        gm_kick=36, gm_snare=38, gm_chh=42,
        num_variations=10,
        velocity_var=15,
        timing_var=0.02,
        tempo=174.0
    ):
    """
    Generate and save Drum & Bass pattern variations (4 bars w/ fill on bar 4).

    Args:
        output_dir (str): Base directory for output.
        gm_kick (int): MIDI note for Kick.
        gm_snare (int): MIDI note for Snare.
        gm_chh (int): MIDI note for Closed Hi-Hat.
        num_variations (int): Number of pattern variations.
        velocity_var (int): Max random ±offset for velocity.
        timing_var (float): Max random ±offset for timing (in beats).
        tempo (float): BPM for the generated MIDI file.

    Returns:
        None
    """
    genre = "dnb"
    for variation in range(1, num_variations + 1):
        random.seed(4000 + variation)

        # Two-step DnB
        kick_pattern = [0.0, 2.5]
        snare_pattern = [1.0, 3.0]
        ghost_snare_positions = [1.25, 2.75]
        ghost_kick_positions = []
        if random.random() < 0.5:
            ghost_kick_positions.append(0.75)

        # 16th hats
        hat_pattern = [i * 0.25 for i in range(16)]
        high_vel, low_vel = 100, 60

        events = {
            "kick": [],
            "snare": [],
            "hats": []
        }

        # Bars 1-3
        for bar in range(3):
            offset = bar * 4.0
            for t in kick_pattern:
                events["kick"].append((offset + t, gm_kick, 100))
            for t in snare_pattern:
                events["snare"].append((offset + t, gm_snare, 110))
            for t in ghost_snare_positions:
                events["snare"].append((offset + t, gm_snare, 70))
            for t in ghost_kick_positions:
                events["kick"].append((offset + t, gm_kick, 80))

            for i, t in enumerate(hat_pattern):
                vel = high_vel if i % 2 == 0 else low_vel
                events["hats"].append((offset + t, gm_chh, vel))

        # Bar 4 with fill
        offset = 3 * 4.0
        for t in kick_pattern:
            events["kick"].append((offset + t, gm_kick, 100))
        for t in snare_pattern:
            events["snare"].append((offset + t, gm_snare, 110))
        for t in ghost_snare_positions:
            events["snare"].append((offset + t, gm_snare, 70))
        for t in ghost_kick_positions:
            events["kick"].append((offset + t, gm_kick, 80))

        for i, t in enumerate(hat_pattern):
            vel = high_vel if i % 2 == 0 else low_vel
            events["hats"].append((offset + t, gm_chh, vel))

        # Amen or simple fill
        if random.random() < 0.5:
            # Amen fill
            events["kick"] = [
                n for n in events["kick"]
                if not (n[0] == offset and n[1] == gm_kick)
            ]
            events["snare"].append((offset + 0.0, gm_snare, 100))
            events["snare"].append((offset + 0.25, gm_snare, 90))
            events["kick"].append((offset + 0.5, gm_kick, 100))
            # Shift final snare
            events["snare"] = [
                n for n in events["snare"]
                if not (n[0] == offset + 3.0 and n[1] == gm_snare)
            ]
            events["snare"].append((offset + 3.5, gm_snare, 110))
        else:
            # Simple fill
            if random.random() < 0.5:
                # Snare roll
                for t in [offset + 3.25, offset + 3.5, offset + 3.75]:
                    events["snare"].append((t, gm_snare, 100))
            else:
                # Double kick
                events["kick"].append((offset + 3.5, gm_kick, 100))
                events["kick"].append((offset + 3.75, gm_kick, 100))

        humanize_events(events, velocity_variation=velocity_var,
                        timing_variation=timing_var)
        var_str = f"var_{variation:02d}"
        save_midi_files(events, output_dir, genre, tempo, var_str)


if __name__ == "__main__":
    # Example usage (uncomment to run directly):
    # base_path = "/Users/<username>/Production Library/Libraries/Ableton/User Library/MIDI Clips"
    # out_dir = prepare_output_directory(base_path)
    #
    # create_house_patterns(out_dir, num_variations=2)
    # create_breaks_patterns(out_dir, num_variations=2)
    # create_ukg_patterns(out_dir, num_variations=2)
    # create_dnb_patterns(out_dir, num_variations=2)
    pass