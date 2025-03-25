import random
import copy
import os
import datetime
import mido

# Drum mapping (MIDI note numbers for common drum sounds)
drum_map = {
    "kick": 36,   # Bass Drum
    "snare": 38,  # Snare Drum
    "hihat": 42,  # Closed Hi-Hat
    "oh": 46,     # Open Hi-Hat
    "clap": 39,   # Hand Clap
    "tom": 43     # Low Tom
}

# Helper function to apply a method to a pattern
def apply_method(pattern, method):
    return method(copy.deepcopy(pattern))

# --- Variation Methods (A and B) ---
def random_hit_removal(pattern, removal_prob=0.1):
    for drum in pattern:
        if drum not in ['pattern_num', 'genre', 'tags', 'desc']:
            pattern[drum] = [v if random.random() > removal_prob else 0 for v in pattern[drum]]
    return pattern

def random_hit_addition(pattern, addition_prob=0.1):
    for drum in pattern:
        if drum not in ['pattern_num', 'genre', 'tags', 'desc']:
            pattern[drum] = [v if v > 0 else (random.randint(60, 100) if random.random() < addition_prob else 0) for v in pattern[drum]]
    return pattern

def velocity_variation(pattern, variation_range=10):
    for drum in pattern:
        if drum not in ['pattern_num', 'genre', 'tags', 'desc']:
            pattern[drum] = [max(0, min(127, v + random.randint(-variation_range, variation_range))) if v > 0 else 0 for v in pattern[drum]]
    return pattern

def drum_swap(pattern, swap_prob=0.1):
    swappable_drums = ['snare', 'clap']
    for i in range(16):
        if random.random() < swap_prob:
            if pattern['snare'][i] > 0:
                pattern['clap'][i] = pattern['snare'][i]
                pattern['snare'][i] = 0
            elif pattern['clap'][i] > 0:
                pattern['snare'][i] = pattern['clap'][i]
                pattern['clap'][i] = 0
    return pattern

def add_ghost_notes(pattern, ghost_prob=0.1):
    for drum in ['snare', 'kick']:
        for i in range(16):
            if pattern[drum][i] == 0 and random.random() < ghost_prob:
                pattern[drum][i] = random.randint(20, 40)  # Low velocity for ghost notes
    return pattern

variation_methods = [
    random_hit_removal,
    random_hit_addition,
    velocity_variation,
    drum_swap,
    add_ghost_notes
]

# --- Mini Fill Methods (C) ---
def snare_roll(pattern):
    pattern['snare'][12:16] = [100, 100, 100, 100]
    return pattern

def kick_roll(pattern):
    pattern['kick'][12:16] = [100, 100, 100, 100]
    return pattern

def tom_mini_fill(pattern):
    pattern['tom'][12:16] = [80, 0, 80, 0]
    return pattern

def cymbal_swell(pattern):
    pattern['oh'][12:16] = [60, 70, 80, 90]
    return pattern

def silence_mini_fill(pattern):
    for drum in pattern:
        if drum not in ['pattern_num', 'genre', 'tags', 'desc']:
            pattern[drum][12:16] = [0] * 4
    return pattern

mini_fill_methods = [
    snare_roll,
    kick_roll,
    tom_mini_fill,
    cymbal_swell,
    silence_mini_fill
]

# --- Full Fill Methods (D) ---
def tom_fill(pattern):
    pattern['tom'] = [0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80]
    return pattern

def snare_fill(pattern):
    pattern['snare'] = [100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0]
    return pattern

def kick_snare_alternation(pattern):
    pattern['kick'] = [100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0]
    pattern['snare'] = [0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100, 0, 100]
    return pattern

def cymbal_crash_fill(pattern):
    pattern['oh'] = [100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0, 100, 0, 0, 0]
    return pattern

def polyrhythmic_fill(pattern):
    pattern['kick'] = [100, 0, 0, 90, 0, 0, 100, 0, 0, 0, 0, 0, 100, 0, 0, 0]
    pattern['snare'] = [0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0]
    return pattern

fill_methods = [
    tom_fill,
    snare_fill,
    kick_snare_alternation,
    cymbal_crash_fill,
    polyrhythmic_fill
]

# --- Generate a 4-bar Clip ---
def generate_4_bar_clip(base_pattern):
    # Generate variations A and B
    method_a = random.choice(variation_methods)
    method_b = random.choice(variation_methods)
    variation_a = apply_method(base_pattern, method_a)
    variation_b = apply_method(base_pattern, method_b)
    
    # Generate mini fill C and full fill D
    mini_fill_c = apply_method(base_pattern, random.choice(mini_fill_methods))
    fill_d = apply_method(base_pattern, random.choice(fill_methods))
    
    return variation_a, variation_b, mini_fill_c, fill_d

def create_midi_sequence(phrase, drum_map, ticks_per_16th=120, mode='both', velocity_range=10, timing_range=10):
    """
    Convert a pattern to a MIDI sequence with optional velocity and timing humanization.
    
    Parameters:
    - phrase: List of bars, where each bar is a dict mapping drum names to lists of velocities (16 steps).
    - drum_map: Dict mapping drum names to MIDI note numbers.
    - ticks_per_16th: Number of ticks per 16th note (default 120).
    - mode: 'both' (velocity and timing), 'velocity', 'timing', or 'none'.
    - velocity_range: Max random variation for velocity (0-127 range).
    - timing_range: Max random variation for timing in ticks.
    
    Returns:
    - track: mido.MidiTrack object containing the MIDI sequence.
    """
    # Adjust ranges based on mode
    if mode == 'velocity':
        timing_range = 0
    elif mode == 'timing':
        velocity_range = 0
    elif mode == 'none':
        velocity_range = 0
        timing_range = 0
    # else mode == 'both', use provided ranges

    events = []
    bar_start_time = 0
    for bar in phrase:
        for step in range(16):
            step_time = bar_start_time + step * ticks_per_16th
            for drum in bar:
                if drum in drum_map and bar[drum][step] > 0:
                    note = drum_map[drum]
                    base_velocity = bar[drum][step]
                    # Humanize velocity
                    velocity_adjustment = random.randint(-velocity_range, velocity_range) if velocity_range > 0 else 0
                    velocity = max(1, min(127, base_velocity + velocity_adjustment))
                    # Humanize timing
                    timing_offset = random.randint(-timing_range, timing_range) if timing_range > 0 else 0
                    note_on_time = step_time + timing_offset
                    note_off_time = note_on_time + ticks_per_16th  # 1/16th note duration
                    # Add note on and note off events
                    events.append((note_on_time, mido.Message('note_on', note=note, velocity=velocity)))
                    events.append((note_off_time, mido.Message('note_off', note=note, velocity=0)))
        bar_start_time += 16 * ticks_per_16th

    # Sort events by absolute time
    events.sort(key=lambda x: x[0])

    # Build the MIDI track with delta times
    track = mido.MidiTrack()
    current_time = 0
    for time, msg in events:
        delta = time - current_time
        if delta < 0:
            delta = 0  # Prevent negative delta times
        msg.time = delta
        track.append(msg)
        current_time += delta
    return track

def save_midi_clip(track, instrument, genre, output_dir="/MIDI Clips"):
    """
    Save the MIDI track to a file with a structured folder and filename.
    
    Parameters:
    - track: mido.MidiTrack object to save.
    - instrument: String name of the instrument (e.g., 'drums').
    - genre: String name of the genre (e.g., 'rock').
    - output_dir: Base directory for saving MIDI files.
    """
    # Get today's date in YYYY_MM_DD format
    today = datetime.date.today().strftime("%Y_%m_%d")
    
    # Create date folder
    date_dir = os.path.join(output_dir, today)
    if not os.path.exists(date_dir):
        os.makedirs(date_dir)
    
    # Create genre subfolder
    genre_dir = os.path.join(date_dir, genre)
    if not os.path.exists(genre_dir):
        os.makedirs(genre_dir)
    
    # Find next available file number
    i = 1
    while True:
        filename = f"{instrument}_{genre}_{i}.mid"
        filepath = os.path.join(genre_dir, filename)
        if not os.path.exists(filepath):
            break
        i += 1
    
    # Create and save MIDI file
    mid = mido.MidiFile()
    mid.tracks.append(track)
    mid.save(filepath)
    print(f"Saved MIDI clip to: {filepath}")