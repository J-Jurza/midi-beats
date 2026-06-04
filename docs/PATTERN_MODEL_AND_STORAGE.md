# Pattern model, TR-8 workflow, and pattern storage

## How vintage machines actually work (vs our ABAC)

### Roland TR-8S / TR-808 lineage

| Concept | TR-8S behavior | Our current ABAC export |
|---------|----------------|-------------------------|
| **Pattern** | One “song slot” (128 patterns); holds tempo, kit, FX | One generated “variation folder” |
| **Variation A–H** | **8 independent 1-bar** (16-step) snapshots | Not separate — baked into 4-bar chain |
| **Fill 1 / Fill 2** | **2 dedicated 1-bar** fills; manual trig or auto every N bars | Bar B ≈ mini fill, bar C ≈ full fill **inside** the 4-bar loop |
| **Playback** | User **switches** A→B live, or chains patterns; fills **interrupt** then return | DAW loops **one 4-bar MIDI file** (A-B-A-C pre-arranged) |
| **Steps** | 16 pads = 16th notes in **one bar** | Events are continuous beats 0–16 across 4 bars |

**ABAC in our code** is a **pre-arranged 4-bar form** (composition template), not TR-8’s performance model. That is still valuable for Ableton loops, but the UI and generator should **also** expose TR-8-style **slots** so users can think like the hardware.

### Mapping (evolve, don’t throw away)

| TR-8 slot | Our procedural role today | Evolution |
|-----------|---------------------------|-----------|
| **A** | `bar_A` base groove | **Base pattern** — can load from pattern DB |
| **B** | `bar_B` = A + mini fill | **Variation 1** (subtle) |
| **C–H** | (unused) | Extra variations: hat density, ghost kicks, etc. |
| **Fill 1** | `bar_B` alternate | Short fill pool |
| **Fill 2** | `bar_C` / amen | Long fill pool |
| **Chain export** | ABAC = A→B→A→C | One MIDI clip (current) |
| **Slot export** | — | `A.mid`, `B.mid`, `FILL1.mid` (TR-8 style) |

---

## Target pattern object (code: `midi_beats.core.pattern_model`)

```text
DrumPattern
├── id, genre, tempo, seed
├── slots: A | B | C | D | E | F | G | H | FILL1 | FILL2
│     └── each slot = 1 bar EventMap (beats 0.0–3.99)
├── chain: ["A", "B", "A", "C"]   # Ableton loop
└── auto_fill: { interval_bars: 4, slot: "FILL1" }  # performance metadata
```

**Generators** build slots using existing `bar_A` / `apply_mini_fill` helpers, then:

- `pattern.to_chain_events()` → 4-bar ABAC (backward compatible)
- `pattern.to_slot_events("A")` → 1-bar for TR-8 UI / separate export

---

## UI workflow (TR-8 intimate)

### Screen layout (one pattern at a time)

```text
┌─ PATTERN 042 ─ HOUSE 120 ─────────────────────────────┐
│  [A][B][C][D]  [E][F][G][H]     [F1][F2]  ← slot select (green=active)
├────────────────────────────────────────────────────────┤
│  KICK │■│□│□│□│■│□│□│□│■│□│■│□│■│□│□│□│  ← 16 steps, 1 bar only
│  SNR  │□│□│□│□│■│□│□│□│□│□│□│□│■│□│□│□│
│  CHH  │■│■│■│■│■│■│■│■│■│■│■│■│■│■│■│■│
├────────────────────────────────────────────────────────┤
│  CHAIN: [A]─[B]─[A]─[C]   EXPORT: ○ Slots  ● Chain   │
│  AUTO FILL: [every 4 bars ▼] → [FILL1 ▼]              │
│  [◀ Pat] [Gen from DB] [Mutate B] [Export MIDI] [▶]   │
└────────────────────────────────────────────────────────┘
```

### User flow (mirrors TR-REC)

1. **Select genre** → loads default **slot A** from pattern library (or procedural seed).
2. **Edit steps** on 16×N grid (read-only v1, toggle v2) for **active slot only**.
3. Press **B** → “Copy A → B” then auto-apply mini-fill mutation (existing `apply_mini_fill`).
4. Press **FILL1** → pick from fill pool (snare roll / double kick / amen) — existing `apply_snare_roll_fill` / `apply_amen_partial_fill`.
5. **CHAIN** row shows ABAC (editable to A-A-A-A or A-B-B-A for experimentation).
6. **Export**: “Slots” = 5–10 files per instrument; “Chain” = current `generate_midi_patterns` behavior.
7. **Auto Fill** does not render audio in v1 — stored in `manifest.json` for future live engine.

### Relation to visualizer plan

Phase 1 `grid.py` shows **one slot = 16 steps**. Phase 2 UI adds **A–H + F1/F2** buttons above the grid. Existing `generate_events()` becomes `pattern.to_chain_events()`.

---

## Pattern library → feeding generation

### Layers

```text
data/patterns/          ← human-curated JSON (git-friendly seeds)
        ↓ import
SQLite patterns.db      ← queryable catalog (thousands+)
        ↓ sample / retrieve
Genre generator         ← bar_A pulls template by tag
        ↓
DrumPattern slots       → MIDI + grid UI
```

### JSON seed file (good for: git, hand authoring, small libraries)

```json
{
  "id": "house_kick_four_floor",
  "genre": "house",
  "slot_role": "base",
  "tags": ["four-on-floor", "house"],
  "tracks": {
    "kick": { "steps": [0, 4, 8, 10, 12], "default_velocity": 100 },
    "snare": { "steps": [4, 12], "default_velocity": 110 }
  }
}
```

Steps are **0–15** sixteenths in one bar — matches TR-8 pads.

### When to use what (ML + scale)

| Format | Best for | Avoid for |
|--------|----------|-----------|
| **JSON / YAML** | <500 seeds, docs, PRs, hand curation | 100k+ training rows, fast similarity search |
| **SQLite** | 10³–10⁶ patterns, tags, genre, BPM, app UI, manifests | Heavy vector search (use extension or sidecar) |
| **Parquet** | ML pipelines, columnar features, cloud training | Interactive step editing |
| **Embedding DB** (Chroma/pgvector) | “Find patterns like this” for ML augments | Source of truth for step data |

**Recommendation:**  
- **Source of truth for steps:** SQLite `variations` table (BLOB or JSON column per slot).  
- **Git seeds:** `data/patterns/*.json` imported on build/dev.  
- **ML export:** nightly `export_parquet.py` → step matrices + metadata (genre, tempo, slot, tags).  
- **Do not** store 50k patterns only as loose JSON files in git.

### Schema (SQLite)

```sql
patterns (id, genre, name, tempo, tags, source, created_at)
variation_slots (pattern_id, slot, steps_json, velocities_json)
fills (pattern_id, slot FILL1|FILL2, steps_json)
chains (pattern_id, sequence_json)  -- e.g. ["A","B","A","C"]
```

`steps_json`: `{"kick": [0,4,8], "snare": [4,12]}` — compact, UI-friendly.

For ML, add derived columns: `kick_bitmap` (16-bit int), `density`, `syncopation_score`.

---

## Code evolution checklist

- [x] `pattern_model.DrumPattern` + `ChainPreset.ABAC`
- [x] `grid.py` — slot ↔ 16-step grid
- [x] `library/` — JSON import + SQLite store
- [x] `house.py` refactored to build `DrumPattern` then chain
- [ ] UI: slot buttons + single-bar grid (`docs/VISUALIZER_PLAN.md` update)
- [ ] Pipeline: export mode `slots` | `chain` | `both`
- [ ] Parquet ML export script

---

## Summary answer: JSON or database?

**Both, different jobs:** JSON for seeds and interchange; **SQLite as the app/ML catalog** once you have more than a few hundred patterns or need tagging/search. For large ML, **export Parquet from SQLite** rather than training directly on thousands of JSON files.
