const GENRES = ["house", "breaks", "ukg", "dnb"];
const TRACK_ORDER = ["kick", "snare", "clap", "chh", "ohh"];
const TRACK_LABELS = { kick: "KCK", snare: "SNR", clap: "CLP", chh: "CHH", ohh: "OHH" };

let state = { activeSlot: "BASE", data: null };

const el = (id) => document.getElementById(id);

function initControls() {
  const g = el("genre");
  GENRES.forEach((genre) => {
    const o = document.createElement("option");
    o.value = genre;
    o.textContent = genre.toUpperCase();
    g.appendChild(o);
  });
  g.addEventListener("change", loadPattern);

  el("chain").addEventListener("change", () => {
    if (state.data) {
      const preset = el("chain").value;
      state.data.chain_preset = preset;
      state.data.chain = state.data.chain_presets[preset].sequence;
      state.data.chain_label = state.data.chain_presets[preset].label;
      renderChain();
      loadPattern();
    }
  });

  el("btn-gen").addEventListener("click", loadPattern);
  el("seed").addEventListener("change", loadPattern);

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
    populateChainSelect();
    renderChain();
    renderGrid();
    el("status").textContent = `${state.data.genre.toUpperCase()} · ${state.data.tempo} BPM · ${state.data.chain_preset}`;
    el("pattern-id").textContent = state.data.pattern_id || "";
  } catch (e) {
    el("status").textContent = "Error: " + e.message;
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

function renderGrid() {
  const root = el("grid");
  root.innerHTML = "";
  const slot = state.data.slots[state.activeSlot];
  if (!slot) {
    root.textContent = "No data for this slot.";
    return;
  }

  const steps = state.data.steps_per_bar || 16;

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
      const pad = document.createElement("div");
      pad.className = "step";
      if (i > 0 && i % 4 === 0) pad.classList.add("bar-start");
      if (cell.on) {
        pad.classList.add("on");
        const v = cell.vel || 100;
        if (v < 80) pad.classList.add("low");
        else if (v < 110) pad.classList.add("mid");
        pad.style.opacity = String(0.45 + (v / 127) * 0.55);
      }
      stepsEl.appendChild(pad);
    });

    track.appendChild(stepsEl);
    root.appendChild(track);
  });
}

initControls();
loadPattern();
