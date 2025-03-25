import os
import random
from midiutil import MIDIFile
from datetime import datetime

# --- Humanization Function ---
def humanize_instrument_events(events_dict, velocity_variation=0, timing_variation=0.0):
    """
    Applies in-place random velocity and timing offsets to each instrument's events.
    
    Parameters:
        events_dict (dict): Dictionary mapping instrument names to lists of (time, velocity) tuples.
        velocity_variation (int): Maximum variation to add/subtract from velocity.
        timing_variation (float): Maximum variation to add/subtract from the event time.
    """
    for instrument, ev_list in events_dict.items():
        for i, (time, vel) in enumerate(ev_list):
            if velocity_variation > 0:
                delta_vel = random.randint(-velocity_variation, velocity_variation)
                vel = max(1, min(127, vel + delta_vel))
            if timing_variation > 0:
                delta_time = random.uniform(-timing_variation, timing_variation)
                time = max(0, time + delta_time)
            ev_list[i] = (time, vel)

# --- Individual Generator Functions ---
def generate_house_events(num_variations=5, seed_base=None):
    """
    Generates a dictionary of MIDI event tuples for the 'house' genre using an ABAC structure.
    This generator includes a merged kick pattern with a breaks-inspired hit.
    
    Parameters:
        num_variations (int): Number of 4-bar ABAC loops to generate.
        seed_base (int or None): If provided, fixes the random seed for reproducibility.
    
    Returns:
        dict: Dictionary with keys "kick", "snare", "clap", "chh", "ohh" mapping to event lists.
    """
    events = {"kick": [], "snare": [], "clap": [], "chh": [], "ohh": []}
    # House patterns
    kick_pat = [0.0, 1.0, 2.0, 2.5, 3.0]  # Merged kick pattern (breaks influence added)
    snare_pat = [1.0, 3.0]
    clap_pat  = [1.0, 3.0]
    ohh_pat   = [0.5, 1.5, 2.5, 3.5]
    
    def bar_A(offset, chh_list):
        for t in kick_pat:
            events["kick"].append((offset + t, 100))
        for t in snare_pat:
            events["snare"].append((offset + t, 110))
        for t in clap_pat:
            events["clap"].append((offset + t, 110))
        for t in chh_list:
            events["chh"].append((offset + t, 90))
        for t in ohh_pat:
            events["ohh"].append((offset + t, 100))
    
    def bar_B(offset, chh_list):
        bar_A(offset, chh_list)
        # Variation: add a snare accent or a double kick
        if random.random() < 0.5:
            events["snare"].append((offset + 3.75, 110))
        else:
            events["kick"].append((offset + 3.5, 100))
            events["kick"].append((offset + 3.75, 100))
    
    def bar_C(offset, chh_list):
        bar_A(offset, chh_list)
        if random.random() < 0.5:
            for t in [3.25, 3.5, 3.75]:
                events["snare"].append((offset + t, 100))
        else:
            events["kick"].append((offset + 3.5, 100))
            events["kick"].append((offset + 3.75, 100))
    
    for i in range(1, num_variations + 1):
        if seed_base is not None:
            random.seed(seed_base + i)
        base_offset = (i - 1) * 16.0
        # Choose a closed-hat pattern: either dense (16 steps) or sparse (8 steps)
        if random.random() < 0.5:
            chh_list = [x * 0.25 for x in range(16)]
        else:
            chh_list = [x * 0.5 for x in range(8)]
        # ABAC structure
        bar_A(base_offset + 0.0, chh_list)
        bar_B(base_offset + 4.0, chh_list)
        bar_A(base_offset + 8.0, chh_list)
        bar_C(base_offset + 12.0, chh_list)
    return events


def generate_ukg_events(num_variations=5, seed_base=None):
    """
    Generates a dictionary of MIDI event tuples for the 'ukg' genre using an ABAC structure.
    
    Parameters:
        num_variations (int): Number of 4-bar ABAC loops to generate.
        seed_base (int or None): If provided, fixes the random seed for reproducibility.
    
    Returns:
        dict: Dictionary with keys "kick", "snare", "clap", "chh", "ohh" mapping to event lists.
    """
    events = {"kick": [], "snare": [], "clap": [], "chh": [], "ohh": []}
    kick_pat = [0.0, 2.5]
    snare_pat = [1.0, 3.0]
    clap_pat  = [1.0, 3.0]
    ohh_pat   = [0.5, 1.5, 3.5]
    chh_pat   = [0.0, 1.0, 2.0, 3.0]
    swung_hat = 2.25

    def bar_A(offset):
        for t in kick_pat:
            events["kick"].append((offset + t, 100))
        for t in snare_pat:
            events["snare"].append((offset + t, 110))
        for t in clap_pat:
            events["clap"].append((offset + t, 110))
        for t in chh_pat:
            events["chh"].append((offset + t, 90))
        events["chh"].append((offset + swung_hat, 80))
        if random.random() < 0.5:
            events["kick"].append((offset + 1.75, 60))
    
    def bar_B(offset):
        bar_A(offset)
        if random.random() < 0.5:
            events["snare"].append((offset + 3.75, 110))
        else:
            events["kick"].append((offset + 3.5, 100))
            events["kick"].append((offset + 3.75, 100))
    
    def bar_C(offset):
        bar_A(offset)
        if random.random() < 0.5:
            for t in [3.25, 3.5, 3.75]:
                events["snare"].append((offset + t, 100))
        else:
            events["kick"].append((offset + 3.5, 100))
            events["kick"].append((offset + 3.75, 100))
    
    for i in range(1, num_variations + 1):
        if seed_base is not None:
            random.seed(seed_base + i)
        base_offset = (i - 1) * 16.0
        bar_A(base_offset + 0.0)
        bar_B(base_offset + 4.0)
        bar_A(base_offset + 8.0)
        bar_C(base_offset + 12.0)
    return events


def generate_dnb_events(num_variations=5, seed_base=None):
    """
    Generates a dictionary of MIDI event tuples for the 'dnb' (Drum & Bass) genre using an ABAC structure.
    
    Parameters:
        num_variations (int): Number of 4-bar ABAC loops to generate.
        seed_base (int or None): If provided, fixes the random seed for reproducibility.
    
    Returns:
        dict: Dictionary with keys "kick", "snare", "clap", "chh", "ohh" mapping to event lists.
    """
    events = {"kick": [], "snare": [], "clap": [], "chh": [], "ohh": []}
    kick_pat     = [0.0, 2.5]
    snare_pat    = [1.0, 3.0]
    ghost_snares = [1.25, 2.75]
    hat_pat      = [x * 0.25 for x in range(16)]
    high_vel     = 100
    low_vel      = 60

    def bar_A(offset, ghost_kicks):
        for t in kick_pat:
            events["kick"].append((offset + t, 100))
        for t in snare_pat:
            events["snare"].append((offset + t, 110))
        for t in ghost_snares:
            events["snare"].append((offset + t, 70))
        for gk in ghost_kicks:
            events["kick"].append((offset + gk, 80))
        for i, h_t in enumerate(hat_pat):
            vel = high_vel if i % 2 == 0 else low_vel
            events["chh"].append((offset + h_t, vel))
    
    def bar_B(offset, ghost_kicks):
        bar_A(offset, ghost_kicks)
        if random.random() < 0.5:
            events["snare"].append((offset + 3.75, 100))
        else:
            events["kick"].append((offset + 3.5, 100))
            events["kick"].append((offset + 3.75, 100))
    
    def bar_C(offset, ghost_kicks):
        bar_A(offset, ghost_kicks)
        if random.random() < 0.5:
            # Amen partial fill:
            events["kick"] = [e for e in events["kick"] if abs(e[0] - offset) > 0.001]
            events["snare"].append((offset + 0.0, 100))
            events["snare"].append((offset + 0.25, 90))
            events["kick"].append((offset + 0.5, 100))
            events["snare"] = [e for e in events["snare"] if abs(e[0] - (offset + 3.0)) > 0.001]
            events["snare"].append((offset + 3.5, 110))
        else:
            if random.random() < 0.5:
                for t in [3.25, 3.5, 3.75]:
                    events["snare"].append((offset + t, 100))
            else:
                events["kick"].append((offset + 3.5, 100))
                events["kick"].append((offset + 3.75, 100))
    
    for i in range(1, num_variations + 1):
        if seed_base is not None:
            random.seed(seed_base + i)
        base_offset = (i - 1) * 16.0
        ghost_kicks = []
        if random.random() < 0.5:
            ghost_kicks.append(0.75)
        bar_A(base_offset, ghost_kicks)
        bar_B(base_offset + 4.0, ghost_kicks)
        bar_A(base_offset + 8.0, ghost_kicks)
        bar_C(base_offset + 12.0, ghost_kicks)
    return events

# --- MIDI Building Function ---
def build_midi_files(events, tempo=120.0, genre="house", gm_mapping=None):
    """
    Converts an events dictionary into a dictionary of MIDIFile objects (one per instrument).
    
    Parameters:
        events (dict): Dictionary mapping instrument names to lists of (time, velocity) tuples.
        tempo (float): Tempo (BPM) for the MIDI file.
        genre (str): Genre label (used for file naming).
        gm_mapping (dict or None): Mapping of instrument names to General MIDI note numbers.
            If None, defaults are used:
              { "kick": 36, "snare": 38, "clap": 39, "chh": 42, "ohh": 46 }
    
    Returns:
        dict: Mapping from instrument names to MIDIFile objects.
    """
    if gm_mapping is None:
        gm_mapping = {
            "kick": 36,
            "snare": 38,
            "clap": 39,
            "chh": 42,
            "ohh": 46
        }
    
    midi_files = {}
    for instrument, ev_list in events.items():
        # Use the provided GM note mapping for this instrument.
        if instrument not in gm_mapping:
            continue
        note = gm_mapping[instrument]
        
        ev_list.sort(key=lambda x: x[0])
        midi = MIDIFile(1)
        midi.addTempo(track=0, time=0, tempo=tempo)
        for (t, vel) in ev_list:
            midi.addNote(track=0, channel=9, pitch=note, time=t, duration=0.1, volume=vel)
        midi_files[instrument] = midi
    return midi_files

# --- Process and Save Wrapper ---
def process_and_save_genre(genre, output_dir, num_variations=5, velocity_var=15, timing_var=0.02, tempo=120.0, seed_base=None):
    """
    Processes a given genre by:
      1. Generating raw MIDI events using the appropriate generator.
      2. Applying humanization to the events.
      3. Converting the events into MIDIFile objects.
      4. Saving each instrument's MIDI file to the output directory.
    
    Parameters:
        genre (str): The genre ("house", "ukg", or "dnb").
        output_dir (str): Directory in which to save the MIDI files.
        num_variations (int): Number of ABAC loops to generate.
        velocity_var (int): Maximum variation in velocity for humanization.
        timing_var (float): Maximum variation in timing for humanization.
        tempo (float): Tempo (BPM) for the MIDI file.
        seed_base (int or None): Seed value for reproducibility; if None, randomness is not fixed.
    
    Returns:
        dict: Mapping from instrument names to the saved MIDI file paths.
    """
    if genre.lower() == "house":
        events = generate_house_events(num_variations=num_variations, seed_base=seed_base)
    elif genre.lower() == "ukg":
        events = generate_ukg_events(num_variations=num_variations, seed_base=seed_base)
    elif genre.lower() == "dnb":
        events = generate_dnb_events(num_variations=num_variations, seed_base=seed_base)
    else:
        raise ValueError("Unsupported genre. Choose from 'house', 'ukg', or 'dnb'.")
    
    # Apply humanization to the events.
    humanize_instrument_events(events, velocity_variation=velocity_var, timing_variation=timing_var)
    
    # Build MIDIFile objects from the events.
    midi_files = build_midi_files(events, tempo=tempo, genre=genre)
    
    # Ensure the output directory exists.
    os.makedirs(output_dir, exist_ok=True)
    saved_files = {}
    for inst, midi_obj in midi_files.items():
        filename = f"{genre}_{inst}.mid"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            midi_obj.writeFile(f)
        saved_files[inst] = filepath
    return saved_files

# --- Main Block: Process Each Genre Consecutively ---
if __name__ == "__main__":
    # Define the master output directory with a dated subfolder.
    output_base = "/Users/honzik/Production Library/Libraries/Ableton/User Library/MIDI Clips"
    date_tag = datetime.now().strftime("%Y_%m_%d")
    output_dir = os.path.join(output_base, date_tag)
    os.makedirs(output_dir, exist_ok=True)
    
    # Set generation parameters.
    n_variations = 5
    velocity_var = 15
    timing_var = 0.02
    tempo_house = 120.0
    tempo_ukg = 132.0
    tempo_dnb = 174.0
    # For reproducibility, set a seed (e.g., 1000); otherwise, set to None.
    seed = 1000  
    
    # Process and save each genre consecutively.
    print("Processing house patterns...")
    house_files = process_and_save_genre("house", output_dir, num_variations=n_variations, 
                                          velocity_var=velocity_var, timing_var=timing_var, 
                                          tempo=tempo_house, seed_base=seed)
    
    print("Processing ukg patterns...")
    ukg_files = process_and_save_genre("ukg", output_dir, num_variations=n_variations, 
                                        velocity_var=velocity_var, timing_var=timing_var, 
                                        tempo=tempo_ukg, seed_base=seed)
    
    print("Processing dnb patterns...")
    dnb_files = process_and_save_genre("dnb", output_dir, num_variations=n_variations, 
                                        velocity_var=velocity_var, timing_var=timing_var, 
                                        tempo=tempo_dnb, seed_base=seed)
    
    # Print summary of generated file paths.
    print("✅ MIDI files generated and saved:")
    print("House:")
    for inst, path in house_files.items():
        print(f"  {inst}: {path}")
    print("UKG:")
    for inst, path in ukg_files.items():
        print(f"  {inst}: {path}")
    print("DnB:")
    for inst, path in dnb_files.items():
        print(f"  {inst}: {path}")
