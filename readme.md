# MIDI Drum Pattern Generator

A Python-based generator for classic electronic drum patterns across **House**, **Breaks**, **UK Garage**, and **Drum & Bass**. Each variation is a **4-bar ABAC** loop (16 beats) exported as **separate MIDI clips per instrument** for DAWs like Ableton Live.

---

## Features

- Genre-specific groove logic: `house`, `breaks`, `ukg`, `dnb`
- ABAC loop structure per variation:
  - **A** = base pattern
  - **B** = mini fill
  - **C** = full fill (including amen-style fragments on breaks/dnb)
- Humanisation for timing and velocity (seeded when using `--seed`)
- Per-variation folders with `manifest.json` metadata
- CLI and library API

---

## Project structure

```
.
├── midi_beats/                 # Package (core, genres, pipeline, CLI)
│   ├── core/                   # Events, humanize, MIDI export
│   ├── genres/                 # house, breaks, ukg, dnb
│   └── pipeline.py
├── drum_pattern_generator.py   # Backward-compatible facade
├── midi_drum_pattern_generator.ipynb
├── tests/
├── requirements.txt
└── readme.md
```

---

## Getting started

### Install

```bash
git clone https://github.com/j-jurza/midi-beats.git
cd midi-beats
pip install -r requirements.txt
```

### CLI

```bash
python -m midi_beats house -o ./output -n 5 --seed 42 -v
python -m midi_beats breaks -o ./output -n 3 --seed 42
python -m midi_beats --all-genres -o ./output -n 5 --seed 42   # not supported; run per genre
```

Generate all genres:

```bash
for g in house breaks ukg dnb; do python -m midi_beats $g -o ./output -n 5 --seed 42; done
```

Legacy concatenated export (one timeline per instrument, `house_kick.mid` naming):

```bash
python -m midi_beats house -o ./output -n 5 --concatenated
```

### Python API

```python
from midi_beats import generate_midi_patterns, generate_events, list_genres

print(list_genres())  # ['breaks', 'dnb', 'house', 'ukg']

events = generate_events("ukg", variation_index=1, seed_base=1000)
paths = generate_midi_patterns("house", "./output", num_variations=5, seed_base=1000)
```

Backward-compatible imports still work:

```python
from drum_pattern_generator import generate_midi_patterns, create_breaks_patterns
```

### Jupyter notebook

```bash
jupyter notebook midi_drum_pattern_generator.ipynb
```

---

## Output layout

**Per variation (default):**

```
output/
├── house/
│   ├── variation_1/
│   │   ├── kick_house_1.mid
│   │   ├── snare_house_1.mid
│   │   ├── hats_house_1.mid
│   │   └── manifest.json
│   └── variation_2/
│       └── ...
├── breaks/
│   └── ...
```

Each MIDI clip starts at **beat 0** and spans **4 bars** (16 beats). Import into your DAW and loop.

---

## Customisation

| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_variations` | 5 | Number of ABAC loops |
| `velocity_var` | 15 | Max velocity humanization |
| `timing_var` | 0.02 | Max timing shift (beats) |
| `tempo` | genre default | BPM metadata in MIDI |
| `seed_base` | None | Reproducible patterns + humanization |
| `lock_backbeat` | False | Align kick/snare timing jitter |

Genre default tempos: House 120, Breaks 130, UKG 132, DnB 174.

---

## Development

```bash
git checkout cursor/development-6fd2
python3 -m unittest discover -s tests -v
```

---

## Contributing

Pull requests welcome. Open an issue for larger changes.

---

## License

MIT (see LICENSE)

---

## Author

Made for rhythm nerds by **Honzik**.
