# 🥁 MIDI Drum Pattern Generator

A Python-based generator for classic electronic drum patterns across multiple genres including **House**, **Breaks**, **UK Garage**, and **Drum & Bass**. Generates 4-bar `ABAC` loop sequences and outputs **separate MIDI clips per instrument** to be easily imported into DAWs like Ableton Live.

---

## 🎛 Features

- Genre-specific groove logic (House, Breaks, UKG, DnB)
- ABAC loop structure per variation:
  - A = base pattern  
  - B = mini fill  
  - C = full fill
- Humanisation for timing and velocity
- Outputs individual MIDI clips per instrument (kick, snare, hats, etc.)
- Cleanly structured functions for reuse and extension
- Configurable output directory and loop count

---

## 📂 Project Structure

```
.
├── drum_pattern_generator.py       # Core generation logic and functions
├── midi_drum_pattern_generator.ipynb  # Jupyter Notebook interface for generation
├── README.md                       # This file
└── [Generated MIDI Folders]        # Output: separate .mid files per instrument
```

---

## 🚀 Getting Started

### 1. Clone this repo

```bash
git clone https://github.com/your-username/drum-pattern-generator.git
cd drum-pattern-generator
```

### 2. Install dependencies

This project requires Python 3.8+ and [`midiutil`](https://pypi.org/project/MIDIUtil/):

```bash
pip install midiutil
```

### 3. Run via Jupyter Notebook

Launch the notebook interface:

```bash
jupyter notebook midi_drum_pattern_generator.ipynb
```

Inside the notebook:

```python
from drum_pattern_generator import (
    create_house_patterns,
    create_breaks_patterns,
    create_ukg_patterns,
    create_dnb_patterns
)

output_dir = "/your/ableton/user/library/path"
create_house_patterns(output_dir)
create_breaks_patterns(output_dir)
create_ukg_patterns(output_dir)
create_dnb_patterns(output_dir)
```

---

## 📆 Output

Each function creates:
- A genre folder inside the output directory (e.g. `house/`, `breaks/`, etc.)
- Separate `.mid` files for each instrument:

```
<output_dir>/
├── house/
│   ├── house_kick.mid
│   ├── house_snare.mid
│   └── ...
├── dnb/
│   ├── dnb_kick.mid
│   ├── dnb_chh.mid
│   └── ...
...
```

Import them directly into your DAW and loop to your heart’s content.

---

## 🛠️ Customisation

You can tweak these parameters:

- `output_dir`: Path to save generated MIDI clips
- `num_variations`: Number of ABAC loops per genre
- `velocity_var`: Max variation applied to velocity (default = 15)
- `timing_var`: Max timing shift in beats (default = 0.02)
- `tempo`: Optional, controls tempo metadata in exported files

---

## 👥 Contributing

Pull requests and feature ideas welcome! Please open an issue to discuss larger changes first.

---

## 📄 License

This project is open-source under the MIT License.

---

## 🎧 Author

Made with ❤️ for rhythm nerds by **Honzik**.

Let the groove guide you.

