const GENRES = ["house", "breaks", "ukg", "dnb"];
const TRACK_ORDER = ["kick", "snare", "clap", "chh", "ohh"];
const TRACK_LABELS = { kick: "KCK", snare: "SNR", clap: "CLP", chh: "CHH", ohh: "OHH" };
const AMEN_GENRES = new Set(["breaks", "dnb"]);

let state = { activeSlot: "BASE", data: null, dirty: false };

const el = (id) => document.getElementById(id);

function syncAliasSlots() {
  if (!state.data?.slots) return;
  if (state.data.slots.B) {
    state.data.slots.FILL1 = JSON.parse(JSON.stringify(state.data.slots.B));
  }
  if (state.data.slots.C) {
    state.data.slots.FILL2 = JSON.parse(JSON.stringify(state.data.slots.C));
  }
}

function payloadForApi() {
  return {
    genre: state.data.genre,
    tempo: state.data.tempo,
    seed_base: state.data.seed_base,
    pattern_id: state.data.pattern_id,
    chain_preset: el("chain").value,
    chain: state.data.chain,
    slots: state.data.slots,
  };
}

function initControls() {
  const g = el("genre");
  GENRES.forEach((genre) => {
    const o = document.createElement("option");
    o.value = genre;
    o.textContent = genre.toUpperCase();
    g.appendChild(o);
  });
  g.addEventListener("change", loadPattern);

  el("chain").addEventListener("change", loadPattern);
  el("btn-gen").addEventListener("click", loadPattern);
  el("seed").addEventListener("change", loadPattern);
  el("btn-mutate-b").addEventListener("click", () => mutateSlot("B", "mini"));
  el("btn-mutate-c").addEventListener("click", () => {
    const kind = AMEN_GENRES.has(el("genre").value) ? "amen" : "full";
    mutateSlot("C", kind);
  });
  el("btn-export").addEventListener("click", exportMidi);

  document.querySelectorAll(".slot-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".slot-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.activeSlot = btn.dataset.slot;
      renderGrid();
    });
  });
}

async function loadPattern() {
  el("status").textContent = "Generating…";
  el("export-msg").textContent = "";
  const params = new URLSearchParams({
    genre: el("genre").value,
    chain: el("chain").value,
    variation: "1",
  });
  const seed = el("seed").value;
  if (seed !== "") params.set("seed", seed);

  try {
    const res = await fetch(`/api/pattern?${params}`);
    state.data = await res.json();
    state.dirty = false;
    populateChainSelect();
    renderChain();
    renderGrid();
    el("status").textContent = `${state.data.genre.toUpperCase()} · ${state.data.tempo} BPM · ${state.data.chain_preset}`;
    el("pattern-id").textContent = state.data.pattern_id || "";
  } catch (e) {
    el("status").textContent = "Error: " + e.message;
  }
}

async function mutateSlot(target, kind) {
  if (!state.data) return;
  el("status").textContent = "Mutating…";
  try {
    const res = await fetch("/api/mutate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...payloadForApi(), target, kind }),
    });
    const data = await res.json();
    if (data.error) throw new Error(data.error);
    state.data = data;
    syncAliasSlots();
    state.dirty = true;
    renderGrid();
    renderChain();
    el("status").textContent = `Mutated ${target} from BASE`;
  } catch (e) {
    el("status").textContent = "Mutate error: " + e.message;
  }
}

async function exportMidi() {
  if (!state.data) return;
  syncAliasSlots();
  el("status").textContent = "Exporting MIDI…";
  try {
    const res = await fetch("/api/export", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...payloadForApi(), layout: "both" }),
    });
    const data = await res.json();
    if (!data.ok) throw new Error(data.error || "Export failed");
    const files = Object.values(data.chain_files || {}).join(", ");
    el("export-msg").textContent = `Saved → ${data.output_dir}`;
    el("status").textContent = "Export complete";
    state.dirty = false;
  } catch (e) {
    el("status").textContent = "Export error: " + e.message;
  }
}

function populateChainSelect() {
  const sel = el("chain");
  const current = state.data.chain_preset;
  sel.innerHTML = "";
  Object.entries(state.data.chain_presets).forEach(([key, val]) => {
    const o = document.createElement("option");
    o.value = key;
    o.textContent = `${key} — ${val.label}`;
    if (key === current) o.selected = true;
    sel.appendChild(o);
  });
}

function renderChain() {
  const box = el("chain-display");
  box.innerHTML = "";
  (state.data.chain || []).forEach((letter, i) => {
    const s = document.createElement("span");
    s.className = "chain-step";
    s.textContent = letter;
    s.title = `Bar ${i + 1}`;
    box.appendChild(s);
  });
  el("chain-label").textContent = state.data.chain_label || "";
}

function toggleStep(inst, stepIndex) {
  const slot = state.data.slots[state.activeSlot];
  if (!slot || !slot[inst]) return;
  const cell = slot[inst][stepIndex];
  if (cell.on) {
    cell.on = false;
    cell.vel = null;
  } else {
    cell.on = true;
    cell.vel = cell.vel || 100;
  }
  state.dirty = true;
  if (state.activeSlot === "B") syncAliasSlots();
  if (state.activeSlot === "C") syncAliasSlots();
  if (state.activeSlot === "BASE") {
    /* BASE edit only — user can re-mutate B/C */
  }
}

function renderGrid() {
  const root = el("grid");
  root.innerHTML = "";
  const slot = state.data.slots[state.activeSlot];
  if (!slot) {
    root.textContent = "No data for this slot.";
    return;
  }

  TRACK_ORDER.forEach((inst) => {
    const row = slot[inst];
    if (!row) return;

    const track = document.createElement("div");
    track.className = "track";

    const name = document.createElement("div");
    name.className = "track-name";
    name.textContent = TRACK_LABELS[inst] || inst.toUpperCase();
    track.appendChild(name);

    const stepsEl = document.createElement("div");
    stepsEl.className = "steps";

    row.forEach((cell, i) => {
      const pad = document.createElement("button");
      pad.type = "button";
      pad.className = "step";
      if (i > 0 && i % 4 === 0) pad.classList.add("bar-start");
      if (cell.on) {
        pad.classList.add("on");
        const v = cell.vel || 100;
        if (v < 80) pad.classList.add("low");
        else if (v < 110) pad.classList.add("mid");
        pad.style.opacity = String(0.45 + (v / 127) * 0.55);
      }
      pad.title = `Step ${i + 1}`;
      pad.addEventListener("click", () => {
        toggleStep(inst, i);
        renderGrid();
      });
      stepsEl.appendChild(pad);
    });

    track.appendChild(stepsEl);
    root.appendChild(track);
  });
}

initControls();
loadPattern();
