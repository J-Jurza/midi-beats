import os
import random
from midiutil import MIDIFile

# General MIDI drum note constants
GM_KICK    = 36  # C1: Bass Drum 1
GM_SNARE   = 38  # D1: Acoustic Snare
GM_CLAP    = 39  # Eb1: Hand Clap
GM_CHH     = 42  # F#1: Closed Hi-Hat
GM_OHH     = 46  # Bb1: Open Hi-Hat
GM_RIDE    = 51  # Db2: Ride Cymbal 1

# Utils
#############################################################################

def humanize_events(events, velocity_variation=0, timing_variation=0.0):
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

def save_midi_files(events, genre, tempo):
    for instrument, notes in events.items():
        instrument_dir = os.path.join(genre, instrument)
        os.makedirs(instrument_dir, exist_ok=True)
        filename = f"{genre}_{instrument}".lower()
        file_path = os.path.join(instrument_dir, f"{filename}.mid")

        midi = MIDIFile(1)
        midi.addTempo(track=0, time=0, tempo=tempo)
        channel = 9
        for (time, note, vel) in notes:
            duration = 0.1
            midi.addNote(track=0, channel=channel, pitch=note,
                         time=time, duration=duration, volume=vel)
        with open(file_path, 'wb') as f:
            midi.writeFile(f)

# Pattern generators (to be imported individually)
#############################################################################


def create_house_patterns(num_variations=10, velocity_var=15, timing_var=0.02):
    """
    Generate and save 10 House drum pattern variations (4 bars each with a 4th-bar fill).
    Uses GM_KICK, GM_SNARE, GM_CLAP, GM_CHH, GM_OHH from this module.
    """
    genre = "house"
    tempo = 120  # typical House tempo
    for variation in range(1, num_variations+1):
        random.seed(1000 + variation)  # seed for reproducibility of this variation
        # Base one-bar pattern (times in beats relative to bar start)
        kick_pattern  = [0.0, 1.0, 2.0, 3.0]   # kick on every beat (1,2,3,4)
        snare_pattern = [1.0, 3.0]            # snare on beats 2,4
        clap_pattern  = [1.0, 3.0]            # clap layered on beats 2,4
        open_hat_pattern = [0.5, 1.5, 2.5, 3.5]  # open hat on off-beats

        # Random variation: half the patterns use dense 16th-note hats
        if random.random() < 0.5:
            closed_hat_pattern = [i * 0.25 for i in range(16)]  # 16th-note hats
        else:
            closed_hat_pattern = [i * 0.5 for i in range(8)]    # 8th-note hats

        # Prepare 4-bar events; duplicate base patterns for bars 1-3
        events = {'kick': [], 'snare': [], 'clap': [], 'hats': []}

        # Bars 1-3
        for bar in range(3):
            offset = bar * 4.0
            for t in kick_pattern:
                events['kick'].append((offset + t, GM_KICK, 100))
            for t in snare_pattern:
                events['snare'].append((offset + t, GM_SNARE, 110))
            for t in clap_pattern:
                events['clap'].append((offset + t, GM_CLAP, 110))
            for t in closed_hat_pattern:
                events['hats'].append((offset + t, GM_CHH, 90))
            for t in open_hat_pattern:
                events['hats'].append((offset + t, GM_OHH, 100))

        # Bar 4 with fill
        offset = 3 * 4.0
        # Base pattern in bar 4
        for t in kick_pattern:
            events['kick'].append((offset + t, GM_KICK, 100))
        for t in snare_pattern:
            events['snare'].append((offset + t, GM_SNARE, 110))
        for t in clap_pattern:
            events['clap'].append((offset + t, GM_CLAP, 110))
        for t in closed_hat_pattern:
            events['hats'].append((offset + t, GM_CHH, 90))
        for t in open_hat_pattern:
            events['hats'].append((offset + t, GM_OHH, 100))

        # Decide fill type (snare roll or kick fill) for the last beat of bar 4
        if random.random() < 0.5:
            # Snare roll fill
            roll_times = [offset + 3.25, offset + 3.5, offset + 3.75]
            for t in roll_times:
                events['snare'].append((t, GM_SNARE, 100))
        else:
            # Kick fill (two rapid kicks)
            events['kick'].append((offset + 3.5, GM_KICK, 100))
            events['kick'].append((offset + 3.75, GM_KICK, 100))

        # Humanise & save
        humanize_events(events, velocity_variation=velocity_var, timing_variation=timing_var)
        save_midi_files(events, f"{genre}/var_{variation:02d}", tempo)

def create_breaks_patterns(num_variations=10, velocity_var=15, timing_var=0.02):
    """
    Generate and save 10 Breakbeat pattern variations (4 bars with a fill on bar 4).
    Uses GM_KICK, GM_SNARE, GM_CHH from this module; can add more if desired.
    """
    genre = "breaks"
    tempo = 130  # typical Breaks tempo
    for variation in range(1, num_variations+1):
        random.seed(2000 + variation)

        # Base pattern
        kick_pattern  = [0.0, 2.5]    # Kick on beat 1 and halfway through beat 3
        snare_pattern = [1.0, 3.0]    # Snare on beats 2 and 4
        ghost_snare_positions = [1.25, 2.75]
        ghost_kick_positions  = []
        if random.random() < 0.5:
            ghost_kick_positions.append(3.5)  # Kick on the 'and' of 4

        hat_pattern = [i * 0.5 for i in range(8)]  # 8th note hats

        events = {'kick': [], 'snare': [], 'hats': []}
        # Bars 1-3
        for bar in range(3):
            offset = bar * 4.0
            for t in kick_pattern:
                events['kick'].append((offset + t, GM_KICK, 100))
            for t in snare_pattern:
                events['snare'].append((offset + t, GM_SNARE, 110))
            # Ghost hits
            for t in ghost_snare_positions:
                events['snare'].append((offset + t, GM_SNARE, 70))
            for t in ghost_kick_positions:
                events['kick'].append((offset + t, GM_KICK, 80))
            for t in hat_pattern:
                events['hats'].append((offset + t, GM_CHH, 100))

        # Bar 4 with fill
        offset = 3 * 4.0
        for t in kick_pattern:
            events['kick'].append((offset + t, GM_KICK, 100))
        for t in snare_pattern:
            events['snare'].append((offset + t, GM_SNARE, 110))
        for t in ghost_snare_positions:
            events['snare'].append((offset + t, GM_SNARE, 70))
        for t in ghost_kick_positions:
            events['kick'].append((offset + t, GM_KICK, 80))
        for t in hat_pattern:
            events['hats'].append((offset + t, GM_CHH, 100))

        # Amen-style fill or simpler fill
        if random.random() < 0.5:
            # Amen fill: remove downbeat kick, add quick snare/kick
            events['kick'] = [n for n in events['kick'] if not (n[0] == offset and n[1] == GM_KICK)]
            events['snare'].append((offset + 0.0, GM_SNARE, 100))
            events['snare'].append((offset + 0.25, GM_SNARE, 90))
            events['kick'].append((offset + 0.5, GM_KICK, 100))
            # shift final snare to 3.5 (remove snare on beat 4.0)
            events['snare'] = [n for n in events['snare'] if not (n[0] == offset + 3.0 and n[1] == GM_SNARE)]
            events['snare'].append((offset + 3.5, GM_SNARE, 110))
        else:
            # Simpler fill: snare roll or double kick
            if random.random() < 0.5:
                for t in [offset + 3.25, offset + 3.5, offset + 3.75]:
                    events['snare'].append((t, GM_SNARE, 100))
            else:
                events['kick'].append((offset + 3.5, GM_KICK, 100))
                events['kick'].append((offset + 3.75, GM_KICK, 100))

        humanize_events(events, velocity_variation=velocity_var, timing_variation=timing_var)
        save_midi_files(events, f"{genre}/var_{variation:02d}", tempo)

def create_ukg_patterns(num_variations=10, velocity_var=15, timing_var=0.02):
    """
    Generate and save 10 UK Garage (2-Step) drum pattern variations (4 bars with fill on bar 4).
    Uses GM_KICK, GM_SNARE, GM_CLAP, GM_CHH, GM_OHH from this module.
    """
    genre = "ukg"
    tempo = 132
    for variation in range(1, num_variations+1):
        random.seed(3000 + variation)
        kick_pattern  = [0.0, 2.5]  # beats 1 & 'and' of 3
        snare_pattern = [1.0, 3.0]  # beats 2 & 4
        clap_pattern  = [1.0, 3.0]  # layered on 2 & 4

        # Hats: closed on quarter beats, open on offbeats (except 2.5), plus a swung hat around 2.25
        open_hat_pattern = [0.5, 1.5, 3.5]
        closed_hat_pattern = [0.0, 1.0, 2.0, 3.0]
        swung_hat = 2.25

        # Possibly add an extra ghost kick
        extra_ghost_kick = None
        if random.random() < 0.5:
            extra_ghost_kick = 1.75

        events = {'kick': [], 'snare': [], 'clap': [], 'hats': []}

        # Bars 1-3
        for bar in range(3):
            offset = bar * 4.0
            for t in kick_pattern:
                events['kick'].append((offset + t, GM_KICK, 100))
            for t in snare_pattern:
                events['snare'].append((offset + t, GM_SNARE, 110))
            for t in clap_pattern:
                events['clap'].append((offset + t, GM_CLAP, 110))
            for t in closed_hat_pattern:
                events['hats'].append((offset + t, GM_CHH, 90))
            for t in open_hat_pattern:
                events['hats'].append((offset + t, GM_OHH, 100))
            # Add the swung closed hat
            events['hats'].append((offset + swung_hat, GM_CHH, 80))
            # Ghost kick if chosen
            if extra_ghost_kick is not None:
                events['kick'].append((offset + extra_ghost_kick, GM_KICK, 60))

        # Bar 4 with fill
        offset = 3 * 4.0
        for t in kick_pattern:
            events['kick'].append((offset + t, GM_KICK, 100))
        for t in snare_pattern:
            events['snare'].append((offset + t, GM_SNARE, 110))
        for t in clap_pattern:
            events['clap'].append((offset + t, GM_CLAP, 110))
        for t in closed_hat_pattern:
            events['hats'].append((offset + t, GM_CHH, 90))
        for t in open_hat_pattern:
            events['hats'].append((offset + t, GM_OHH, 100))
        events['hats'].append((offset + swung_hat, GM_CHH, 80))
        if extra_ghost_kick is not None:
            events['kick'].append((offset + extra_ghost_kick, GM_KICK, 60))

        # Fill: snare roll or double kick
        if random.random() < 0.5:
            for t in [offset + 3.25, offset + 3.5, offset + 3.75]:
                events['snare'].append((t, GM_SNARE, 100))
        else:
            events['kick'].append((offset + 3.5, GM_KICK, 100))
            events['kick'].append((offset + 3.75, GM_KICK, 100))

        humanize_events(events, velocity_variation=velocity_var, timing_variation=timing_var)
        save_midi_files(events, f"{genre}/var_{variation:02d}", tempo)

def create_dnb_patterns(num_variations=10, velocity_var=15, timing_var=0.02):
    """
    Generate and save 10 Drum & Bass pattern variations (4 bars with fill on bar 4).
    Uses GM_KICK, GM_SNARE, GM_CHH from this module. (Feel free to add GM_RIDE, GM_CLAP, etc. if needed.)
    """
    genre = "dnb"
    tempo = 174
    for variation in range(1, num_variations+1):
        random.seed(4000 + variation)

        # Standard DnB: Kick on 1 & 'and' of 3, Snare on 2 & 4
        kick_pattern  = [0.0, 2.5]
        snare_pattern = [1.0, 3.0]
        ghost_snare_positions = [1.25, 2.75]
        ghost_kick_positions  = []
        if random.random() < 0.5:
            ghost_kick_positions.append(0.75)  # double kick after beat 1

        # 16th hats
        hat_pattern = [i * 0.25 for i in range(16)]
        high_vel, low_vel = 100, 60

        events = {'kick': [], 'snare': [], 'hats': []}

        # Bars 1-3
        for bar in range(3):
            offset = bar * 4.0
            for t in kick_pattern:
                events['kick'].append((offset + t, GM_KICK, 100))
            for t in snare_pattern:
                events['snare'].append((offset + t, GM_SNARE, 110))
            for t in ghost_snare_positions:
                events['snare'].append((offset + t, GM_SNARE, 70))
            for t in ghost_kick_positions:
                events['kick'].append((offset + t, GM_KICK, 80))
            # Hats with alternating velocities
            for i, t in enumerate(hat_pattern):
                vel = high_vel if i % 2 == 0 else low_vel
                events['hats'].append((offset + t, GM_CHH, vel))

        # Bar 4 with fill
        offset = 3 * 4.0
        for t in kick_pattern:
            events['kick'].append((offset + t, GM_KICK, 100))
        for t in snare_pattern:
            events['snare'].append((offset + t, GM_SNARE, 110))
        for t in ghost_snare_positions:
            events['snare'].append((offset + t, GM_SNARE, 70))
        for t in ghost_kick_positions:
            events['kick'].append((offset + t, GM_KICK, 80))
        for i, t in enumerate(hat_pattern):
            vel = high_vel if i % 2 == 0 else low_vel
            events['hats'].append((offset + t, GM_CHH, vel))

        # Fill: 50% chance Amen/jungle fill vs simple fill
        if random.random() < 0.5:
            # Amen fill
            events['kick'] = [n for n in events['kick'] if not (n[0] == offset and n[1] == GM_KICK)]
            events['snare'].append((offset + 0.0, GM_SNARE, 100))
            events['snare'].append((offset + 0.25, GM_SNARE, 90))
            events['kick'].append((offset + 0.5, GM_KICK, 100))
            # Shift final snare
            events['snare'] = [n for n in events['snare'] if not (n[0] == offset + 3.0 and n[1] == GM_SNARE)]
            events['snare'].append((offset + 3.5, GM_SNARE, 110))
        else:
            # Simple fill: snare roll or double kick
            if random.random() < 0.5:
                for t in [offset + 3.25, offset + 3.5, offset + 3.75]:
                    events['snare'].append((t, GM_SNARE, 100))
            else:
                events['kick'].append((offset + 3.5, GM_KICK, 100))
                events['kick'].append((offset + 3.75, GM_KICK, 100))

        humanize_events(events, velocity_variation=velocity_var, timing_variation=timing_var)
        save_midi_files(events, f"{genre}/var_{variation:02d}", tempo)
