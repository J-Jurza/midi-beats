# drum_pattern_generator.py

import os
import random
from midiutil import MIDIFile

# General MIDI drum note constants
GM_KICK = 36
GM_SNARE = 38
GM_CLAP = 39
GM_CHH = 42
GM_OHH = 46
GM_RIDE = 51

########################################
# Utilities for separate instrument .mid files
########################################

def humanize_instrument_events(events_dict, velocity_variation=0, timing_variation=0.0):
    """
    In-place random velocity/timing offsets for each instrument's event list.
    events_dict: {"kick": [(time, vel), ...], "snare": [...], ...}.
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


def save_instrument_midis(events_dict, output_dir, genre, tempo=120.0):
    """
    Write separate .mid files per instrument, with all appended variations in time.
    
    events_dict: {"kick": [(time, vel), ...], "snare": [...], ...}
    We'll map instrument -> GM note. Each instrument's entire pattern is saved
    to a single-track .mid file, sorted by time.
    """
    os.makedirs(output_dir, exist_ok=True)

    for instrument, ev_list in events_dict.items():
        # Decide GM note per instrument
        if instrument == "kick":
            note = GM_KICK
        elif instrument == "snare":
            note = GM_SNARE
        elif instrument == "clap":
            note = GM_CLAP
        elif instrument == "chh":
            note = GM_CHH
        elif instrument == "ohh":
            note = GM_OHH
        else:
            # Unrecognised instrument -> skip
            continue

        # Sort events by time
        ev_list.sort(key=lambda x: x[0])

        # Build single-track MIDI
        midi = MIDIFile(numTracks=1)
        midi.addTempo(track=0, time=0, tempo=tempo)

        # Add each event
        for (t, vel) in ev_list:
            midi.addNote(
                track=0,
                channel=9,   # standard drum channel
                pitch=note,
                time=t,
                duration=0.1,
                volume=vel
            )

        # e.g. "house_kick.mid"
        filename = f"{genre}_{instrument}.mid"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "wb") as f:
            midi.writeFile(f)

########################################
# House ABAC
########################################

def create_house_patterns(
    output_dir,
    num_variations=5,
    velocity_var=15,
    timing_var=0.02,
    tempo=120.0
):
    """
    Generate House ABAC sequences for 'num_variations' times, then
    export each instrument's hits to separate .mid files.
    """
    genre = "house"
    os.makedirs(output_dir, exist_ok=True)

    # event dictionary for separate instruments
    events = {
        "kick":  [],
        "snare": [],
        "clap":  [],
        "chh":   [],
        "ohh":   []
    }

    # Base patterns
    kick_pat = [0.0, 1.0, 2.0, 3.0]
    snare_pat = [1.0, 3.0]
    clap_pat = [1.0, 3.0]
    ohh_pat = [0.5, 1.5, 2.5, 3.5]

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
        # mini fill
        bar_A(offset, chh_list)
        if random.random() < 0.5:
            # single snare at 3.75
            events["snare"].append((offset + 3.75, 110))
        else:
            # double kick at 3.5, 3.75
            events["kick"].append((offset + 3.5, 100))
            events["kick"].append((offset + 3.75, 100))

    def bar_C(offset, chh_list):
        # full fill
        bar_A(offset, chh_list)
        if random.random() < 0.5:
            # snare roll
            for ft in [3.25, 3.5, 3.75]:
                events["snare"].append((offset + ft, 100))
        else:
            # double kick
            events["kick"].append((offset + 3.5, 100))
            events["kick"].append((offset + 3.75, 100))

    random_seed_base = 1000
    for i in range(1, num_variations + 1):
        random.seed(random_seed_base + i)
        base_offset = (i - 1) * 16.0

        # random closed-hat pattern
        if random.random() < 0.5:
            chh_list = [x * 0.25 for x in range(16)]
        else:
            chh_list = [x * 0.5 for x in range(8)]

        # ABAC
        bar_A(base_offset + 0.0, chh_list)
        bar_B(base_offset + 4.0, chh_list)
        bar_A(base_offset + 8.0, chh_list)
        bar_C(base_offset + 12.0, chh_list)

    # Humanise and save
    humanize_instrument_events(events, velocity_var, timing_var)
    final_dir = os.path.join(output_dir, genre)
    save_instrument_midis(events, final_dir, genre, tempo)
    return final_dir


########################################
# Breaks ABAC
########################################

def create_breaks_patterns(
    output_dir,
    num_variations=5,
    velocity_var=15,
    timing_var=0.02,
    tempo=130.0
):
    genre = "breaks"
    os.makedirs(output_dir, exist_ok=True)

    events = {
        "kick":  [],
        "snare": [],
        "clap":  [],
        "chh":   [],
        "ohh":   []
    }

    kick_pat = [0.0, 2.5]
    snare_pat = [1.0, 3.0]

    def base_bar(off, g_snares, g_kicks, hat_pat):
        for t in kick_pat:
            events["kick"].append((off + t, 100))
        for t in snare_pat:
            events["snare"].append((off + t, 110))
        for gs in g_snares:
            events["snare"].append((off + gs, 70))
        for gk in g_kicks:
            events["kick"].append((off + gk, 80))
        for h in hat_pat:
            events["chh"].append((off + h, 100))

    def bar_B(off, g_snares, g_kicks, hat_pat):
        base_bar(off, g_snares, g_kicks, hat_pat)
        if random.random() < 0.5:
            # single snare at 3.75
            events["snare"].append((off + 3.75, 100))
        else:
            # double kick
            events["kick"].append((off + 3.5, 100))
            events["kick"].append((off + 3.75, 100))

    def bar_C(off, g_snares, g_kicks, hat_pat):
        base_bar(off, g_snares, g_kicks, hat_pat)
        if random.random() < 0.5:
            # Amen partial fill
            events["kick"] = [x for x in events["kick"] if abs(x[0] - off) > 0.001]
            events["snare"].append((off + 0.0, 100))
            events["snare"].append((off + 0.25, 90))
            events["kick"].append((off + 0.5, 100))
            events["snare"] = [x for x in events["snare"] if abs(x[0] - (off + 3.0)) > 0.001]
            events["snare"].append((off + 3.5, 110))
        else:
            # simpler fill
            if random.random() < 0.5:
                # snare roll
                for ft in [3.25, 3.5, 3.75]:
                    events["snare"].append((off + ft, 100))
            else:
                # double kick
                events["kick"].append((off + 3.5, 100))
                events["kick"].append((off + 3.75, 100))

    random_seed_base = 2000
    for var_i in range(1, num_variations + 1):
        random.seed(random_seed_base + var_i)
        base_offset = (var_i - 1) * 16.0

        ghost_snares = [1.25, 2.75]
        ghost_kicks = []
        if random.random() < 0.5:
            ghost_kicks.append(3.5)
        hat_pat = [x * 0.5 for x in range(8)]

        # ABAC
        base_bar(base_offset, ghost_snares, ghost_kicks, hat_pat)
        bar_B(base_offset + 4.0, ghost_snares, ghost_kicks, hat_pat)
        base_bar(base_offset + 8.0, ghost_snares, ghost_kicks, hat_pat)
        bar_C(base_offset + 12.0, ghost_snares, ghost_kicks, hat_pat)

    humanize_instrument_events(events, velocity_var, timing_var)
    final_dir = os.path.join(output_dir, genre)
    save_instrument_midis(events, final_dir, genre, tempo)
    return final_dir


########################################
# UKG ABAC
########################################

def create_ukg_patterns(
    output_dir,
    num_variations=5,
    velocity_var=15,
    timing_var=0.02,
    tempo=132.0
):
    genre = "ukg"
    os.makedirs(output_dir, exist_ok=True)

    events = {
        "kick":  [],
        "snare": [],
        "clap":  [],
        "chh":   [],
        "ohh":   []
    }

    kick_pat = [0.0, 2.5]
    snare_pat = [1.0, 3.0]
    clap_pat = [1.0, 3.0]
    oh_pat = [0.5, 1.5, 3.5]
    ch_pat = [0.0, 1.0, 2.0, 3.0]
    swung_hat = 2.25

    def bar_A(off, ghost_kick):
        for t in kick_pat:
            events["kick"].append((off + t, 100))
        for t in snare_pat:
            events["snare"].append((off + t, 110))
        for t in clap_pat:
            events["clap"].append((off + t, 110))
        for t in ch_pat:
            events["chh"].append((off + t, 90))
        for t in oh_pat:
            events["ohh"].append((off + t, 100))
        events["chh"].append((off + swung_hat, 80))
        if ghost_kick is not None:
            events["kick"].append((off + ghost_kick, 60))

    def bar_B(off, ghost_kick):
        bar_A(off, ghost_kick)
        if random.random() < 0.5:
            # single snare accent
            events["snare"].append((off + 3.75, 100))
        else:
            # double kick
            events["kick"].append((off + 3.5, 100))
            events["kick"].append((off + 3.75, 100))

    def bar_C(off, ghost_kick):
        bar_A(off, ghost_kick)
        if random.random() < 0.5:
            # snare roll
            for ft in [3.25, 3.5, 3.75]:
                events["snare"].append((off + ft, 100))
        else:
            # double kick
            events["kick"].append((off + 3.5, 100))
            events["kick"].append((off + 3.75, 100))

    random_seed_base = 3000
    for var_i in range(1, num_variations + 1):
        random.seed(random_seed_base + var_i)
        base_offset = (var_i - 1) * 16.0

        ghost_k = None
        if random.random() < 0.5:
            ghost_k = 1.75

        bar_A(base_offset, ghost_k)
        bar_B(base_offset + 4.0, ghost_k)
        bar_A(base_offset + 8.0, ghost_k)
        bar_C(base_offset + 12.0, ghost_k)

    humanize_instrument_events(events, velocity_var, timing_var)
    final_dir = os.path.join(output_dir, genre)
    save_instrument_midis(events, final_dir, genre, tempo)
    return final_dir

########################################
# DnB ABAC
########################################

def create_dnb_patterns(
    output_dir,
    num_variations=5,
    velocity_var=15,
    timing_var=0.02,
    tempo=174.0
):
    genre = "dnb"
    os.makedirs(output_dir, exist_ok=True)

    events = {
        "kick":  [],
        "snare": [],
        "clap":  [],
        "chh":   [],
        "ohh":   []
    }

    kick_pat = [0.0, 2.5]
    snare_pat = [1.0, 3.0]
    ghost_snares = [1.25, 2.75]
    hat_pat = [i * 0.25 for i in range(16)]
    high_vel, low_vel = 100, 60

    def bar_A(off, ghost_kicks):
        for t in kick_pat:
            events["kick"].append((off + t, 100))
        for t in snare_pat:
            events["snare"].append((off + t, 110))
        for gsn in ghost_snares:
            events["snare"].append((off + gsn, 70))
        for gk in ghost_kicks:
            events["kick"].append((off + gk, 80))
        # hats
        for i, h_t in enumerate(hat_pat):
            vel = high_vel if (i % 2 == 0) else low_vel
            events["chh"].append((off + h_t, vel))

    def bar_B(off, ghost_kicks):
        bar_A(off, ghost_kicks)
        if random.random() < 0.5:
            # single ghost snare near 3.75
            events["snare"].append((off + 3.75, 100))
        else:
            # double kick
            events["kick"].append((off + 3.5, 100))
            events["kick"].append((off + 3.75, 100))

    def bar_C(off, ghost_kicks):
        bar_A(off, ghost_kicks)
        if random.random() < 0.5:
            # Amen partial fill
            events["kick"] = [e for e in events["kick"] if abs(e[0] - off) > 0.001]
            events["snare"].append((off + 0.0, 100))
            events["snare"].append((off + 0.25, 90))
            events["kick"].append((off + 0.5, 100))
            events["snare"] = [x for x in events["snare"] if abs(x[0] - (off + 3.0)) > 0.001]
            events["snare"].append((off + 3.5, 110))
        else:
            # simpler fill
            if random.random() < 0.5:
                for ft in [3.25, 3.5, 3.75]:
                    events["snare"].append((off + ft, 100))
            else:
                events["kick"].append((off + 3.5, 100))
                events["kick"].append((off + 3.75, 100))

    random_seed_base = 4000
    for var_i in range(1, num_variations + 1):
        random.seed(random_seed_base + var_i)
        base_offset = (var_i - 1) * 16.0

        ghost_k = []
        if random.random() < 0.5:
            ghost_k.append(0.75)

        bar_A(base_offset, ghost_k)
        bar_B(base_offset + 4.0, ghost_k)
        bar_A(base_offset + 8.0, ghost_k)
        bar_C(base_offset + 12.0, ghost_k)

    humanize_instrument_events(events, velocity_var, timing_var)
    final_dir = os.path.join(output_dir, genre)
    save_instrument_midis(events, final_dir, genre, tempo)
    return final_dir

########################################
# Usage Example
########################################

if __name__ == "__main__":
    # Example:
    # out_dir = "/path/to/folder"
    # create_house_patterns(out_dir, num_variations=5)
    # create_breaks_patterns(out_dir, num_variations=5)
    # create_ukg_patterns(out_dir, num_variations=5)
    # create_dnb_patterns(out_dir, num_variations=5)
    pass
