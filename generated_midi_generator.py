import os
import random
import logging
from typing import Dict, List, Tuple, Optional
from midiutil import MIDIFile
from datetime import datetime
import argparse
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Default MIDI mappings (General MIDI percussion)
DEFAULT_MIDI_MAPPING = {
    "kick": 36,  # Bass Drum 1
    "snare": 38,  # Acoustic Snare
    "clap": 39,  # Hand Clap
    "chh": 42,  # Closed Hi-Hat
    "ohh": 46   # Open Hi-Hat
}

class DrumPatternGenerator:
    """Base class for generating drum patterns across genres."""
    
    def __init__(self, tempo: float, bar_length: int = 4, seed: Optional[int] = None):
        self.tempo = tempo
        self.bar_length = bar_length
        self.seed = seed
        if seed is not None:
            random.seed(seed)
    
    def apply_groove(self, events: Dict[str, List[Tuple[float, int]]], swing_percent: float = 0.5) -> None:
        """Apply a swing groove to offbeat events."""
        for ev_list in events.values():
            for i, (time, vel) in enumerate(ev_list):
                if i % 2 == 1:  # Offbeat
                    new_time = time + swing_percent * 0.25
                    ev_list[i] = (new_time, vel)

    def humanize_events(self, events: Dict[str, List[Tuple[float, int]]], 
                       velocity_var: int = 15, timing_var: float = 0.02) -> None:
        """Apply random velocity and timing variations to events."""
        for ev_list in events.values():
            for i, (time, vel) in enumerate(ev_list):
                if velocity_var > 0:
                    delta_vel = random.randint(-velocity_var, velocity_var)
                    vel = max(1, min(127, vel + delta_vel))
                if timing_var > 0:
                    delta_time = random.uniform(-timing_var, timing_var)
                    time = max(0, time + delta_time)
                ev_list[i] = (time, vel)

    def generate_events(self, variation_index: int) -> Dict[str, List[Tuple[float, int]]]:
        """Generate MIDI events for a specific variation. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement generate_events")

    def build_midi_files(self, events: Dict[str, List[Tuple[float, int]]], 
                        gm_mapping: Dict[str, int] = DEFAULT_MIDI_MAPPING) -> Dict[str, MIDIFile]:
        """Convert events to MIDIFile objects."""
        midi_files = {}
        for inst, ev_list in events.items():
            if inst not in gm_mapping:
                logger.warning(f"Skipping unknown instrument: {inst}")
                continue
            note = gm_mapping[inst]
            ev_list.sort(key=lambda x: x[0])
            midi = MIDIFile(1)
            midi.addTempo(track=0, time=0, tempo=self.tempo)
            for (t, vel) in ev_list:
                midi.addNote(track=0, channel=9, pitch=note, time=t, duration=0.1, volume=vel)
            midi_files[inst] = midi
        return midi_files

class HouseGenerator(DrumPatternGenerator):
    """Generates House drum patterns with a 4-on-the-floor base and variations."""
    
    def generate_events(self, variation_index: int) -> Dict[str, List[Tuple[float, int]]]:
        """Generate a 4-bar ABAC House pattern with randomized fills."""
        events = {"kick": [], "snare": [], "clap": [], "chh": [], "ohh": []}
        kick_base = [0.0, 1.0, 2.0, 3.0]  # Four-on-the-floor
        snare_base = [1.0, 3.0]  # Backbeat
        clap_base = [1.0]  # Offbeat clap
        ohh_base = [0.5, 1.5, 2.5, 3.5]  # Offbeat open hats
        
        base_offset = (variation_index - 1) * self.bar_length * 4.0
        chh_list = [x * 0.25 for x in range(int(self.bar_length * 16))] if random.random() < 0.5 else [x * 0.5 for x in range(int(self.bar_length * 8))]

        def bar_a(offset: float) -> None:
            for t in kick_base:
                events["kick"].append((offset + t, 100))
            for t in snare_base:
                events["snare"].append((offset + t, 110))
            for t in clap_base:
                events["clap"].append((offset + t, 90))
            for t in chh_list[:int(self.bar_length * 4)]:
                events["chh"].append((offset + t, 85))
            for t in ohh_base:
                events["ohh"].append((offset + t, 95))

        def bar_b(offset: float) -> None:
            bar_a(offset)
            if random.random() < 0.5:
                events["snare"].append((offset + 3.75, 110))  # Snare fill
            else:
                events["kick"].append((offset + 3.5, 100))  # Double kick

        def bar_c(offset: float) -> None:
            bar_a(offset)
            if random.random() < 0.5:
                for t in [3.25, 3.5, 3.75]:
                    events["snare"].append((offset + t, 100))  # Triplet fill
            else:
                events["kick"].append((offset + 3.75, 100))  # Kick accent

        bar_a(base_offset + 0.0)
        bar_a(base_offset + 4.0)
        bar_b(base_offset + 8.0)
        bar_c(base_offset + 12.0)
        return events

class UKGGenerator(DrumPatternGenerator):
    """Generates UK Garage patterns with 2-step rhythms and swing."""
    
    def generate_events(self, variation_index: int) -> Dict[str, List[Tuple[float, int]]]:
        """Generate a 4-bar ABAC UKG pattern with swung hats."""
        events = {"kick": [], "snare": [], "clap": [], "chh": [], "ohh": []}
        kick_base = [0.0, 2.5]  # 2-step kick
        snare_base = [1.0, 3.0]
        clap_base = [1.0]
        ohh_base = [0.5, 3.5]
        chh_base = [0.0, 1.0, 2.0, 3.0, 2.25]  # Swung hat
        
        base_offset = (variation_index - 1) * self.bar_length * 4.0
        
        def bar_a(offset: float) -> None:
            for t in kick_base:
                events["kick"].append((offset + t, 100))
            for t in snare_base:
                events["snare"].append((offset + t, 110))
            for t in clap_base:
                events["clap"].append((offset + t, 90))
            for t in chh_base:
                events["chh"].append((offset + t, 85))
            for t in ohh_base:
                events["ohh"].append((offset + t, 95))

        def bar_b(offset: float) -> None:
            bar_a(offset)
            events["snare"].append((offset + 3.75, 110))

        def bar_c(offset: float) -> None:
            bar_a(offset)
            for t in [3.5, 3.75]:
                events["kick"].append((offset + t, 100))

        bar_a(base_offset + 0.0)
        bar_a(base_offset + 4.0)
        bar_b(base_offset + 8.0)
        bar_c(base_offset + 12.0)
        self.apply_groove(events, swing_percent=0.6)
        return events

class DnBGenerator(DrumPatternGenerator):
    """Generates Drum & Bass patterns with breakbeat influences."""
    
    def generate_events(self, variation_index: int) -> Dict[str, List[Tuple[float, int]]]:
        """Generate a 4-bar ABAC DnB pattern with ghost notes and fills."""
        events = {"kick": [], "snare": [], "clap": [], "chh": [], "ohh": []}
        kick_base = [0.0, 2.5]
        snare_base = [1.0, 3.0]
        ghost_snares = [1.25, 2.75]
        chh_base = [x * 0.25 for x in range(int(self.bar_length * 16))]
        
        base_offset = (variation_index - 1) * self.bar_length * 4.0
        
        def bar_a(offset: float) -> None:
            for t in kick_base:
                events["kick"].append((offset + t, 100))
            for t in snare_base:
                events["snare"].append((offset + t, 110))
            for t in ghost_snares:
                events["snare"].append((offset + t, 70))
            for i, t in enumerate(chh_base[:int(self.bar_length * 16)]):
                vel = 100 if i % 2 == 0 else 60
                events["chh"].append((offset + t, vel))

        def bar_b(offset: float) -> None:
            bar_a(offset)
            events["kick"].append((offset + 3.5, 100))

        def bar_c(offset: float) -> None:
            bar_a(offset)
            events["snare"].append((offset + 0.25, 90))  # Amen-style fill
            events["kick"].append((offset + 0.5, 100))

        bar_a(base_offset + 0.0)
        bar_a(base_offset + 4.0)
        bar_b(base_offset + 8.0)
        bar_c(base_offset + 12.0)
        return events

def generate_midi_patterns(generator: DrumPatternGenerator, output_dir: str, num_variations: int = 1,
                          velocity_var: int = 15, timing_var: float = 0.02) -> Dict[int, Dict[str, str]]:
    """Generate and save MIDI patterns for a given generator."""
    saved_files_all = {}
    for var in range(1, num_variations + 1):
        try:
            events = generator.generate_events(var)
            generator.humanize_events(events, velocity_var, timing_var)
            midi_files = generator.build_midi_files(events)
            
            var_output_dir = os.path.join(output_dir, generator.__class__.__name__.lower().replace("generator", ""), f"var{var}")
            os.makedirs(var_output_dir, exist_ok=True)
            
            saved_files = {}
            for inst, midi_obj in midi_files.items():
                filename = f"{inst}_{generator.__class__.__name__.lower().replace('generator', '')}_var{var}_{int(generator.tempo)}bpm.mid"
                filepath = os.path.join(var_output_dir, filename)
                with open(filepath, "wb") as f:
                    midi_obj.writeFile(f)
                saved_files[inst] = filepath
            saved_files_all[var] = saved_files
            logger.info(f"Generated variation {var} at {var_output_dir}")
        except Exception as e:
            logger.error(f"Failed to generate variation {var}: {e}")
            raise
    return saved_files_all

def main():
    """CLI entry point for generating MIDI drum patterns."""
    parser = argparse.ArgumentParser(description="Generate MIDI drum patterns for electronic genres.")
    parser.add_argument("--genre", choices=["house", "ukg", "dnb"], required=True, help="Genre to generate")
    parser.add_argument("--output", type=str, default="./midi", help="Output directory")
    parser.add_argument("--variations", type=int, default=1, help="Number of variations")
    parser.add_argument("--tempo", type=float, help="Tempo in BPM (overrides default)")
    parser.add_argument("--seed", type=int, help="Random seed for reproducibility")
    parser.add_argument("--bar-length", type=int, default=4, help="Length of pattern in bars")
    args = parser.parse_args()

    tempos = {"house": 120.0, "ukg": 132.0, "dnb": 174.0}
    tempo = args.tempo if args.tempo else tempos[args.genre]
    
    generators = {
        "house": HouseGenerator(tempo, args.bar_length, args.seed),
        "ukg": UKGGenerator(tempo, args.bar_length, args.seed),
        "dnb": DnBGenerator(tempo, args.bar_length, args.seed)
    }
    
    generator = generators[args.genre]
    generate_midi_patterns(generator, args.output, args.variations)

if __name__ == "__main__":
    main()