const GENRES = ["house", "breaks", "ukg", "dnb"];
const TRACK_ORDER = ["kick", "snare", "clap", "chh", "ohh"];
const TRACK_LABELS = { kick: "KCK", snare: "SNR", clap: "CLP", chh: "CHH", ohh: "OHH" };
const AMEN_GENRES = new Set(["breaks", "dnb"]);
const VEL_CYCLE = [100, 110, 80];

let state = {
  activeSlot: "BASE",
  viewMode: "slot",
  data: null,
  baseEdited: false,
  baseSnapshot: null,
};

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

function snapshotBase() {
  if (state.data?.slots?.BASE) {
    state.baseSnapshot = JSON.stringify(state.data.slots.BASE);
    state.baseEdited = false;
  }
}

function checkBaseEdited() {
  if (!state.baseSnapshot || !state.data?.slots?.BASE) return;
  state.baseEdited = JSON.stringify(state.data.slots.BASE) !== state.baseSnapshot;
  updateBanner();
}

function updateBanner() {
  const banner = el("banner");
  if (state.data?.mutate_recommended || (state.baseEdited && (state.data.slots?.B || state.data.slots?.C))) {
    banner.textContent =
      "BASE was edited — use Mutate → VAR B / VAR C to refresh variations from the new groove.";
    banner.classList.remove("hidden");
  } else {
    banner.classList.add("hidden");
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
    base_edited: state.baseEdited,
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
    mutateSlot("C", AMEN_GENRES.has(el("genre").value) ? "amen" : "full");
  });
  el("btn-export").addEventListener("click", exportMidi);

  document.querySelectorAll(".slot-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (state.viewMode === "phrase") return;
      document.querySelectorAll(".slot-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.activeSlot = btn.dataset.slot;
      renderGrid();
    });
  });

  document.querySelectorAll(".view-mode-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".view-mode-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.viewMode = btn.dataset.mode;
      const slotRow = document.querySelector(".slot-row");
      slotRow.style.opacity = state.viewMode === "phrase" ? "0.45" : "1";
      renderGrid();
    });
  });
}

async function loadCatalogInfo() {
  try {
    const res = await fetch("/api/catalog");
    const info = await res.json();
    if (info.loaded) {
      const parts = Object.entries(info.by_genre || {})
        .map(([g, n]) => `${g}:${n}`)
        .join(" ");
      el("catalog-info").textContent = `Library: ${parts}`;
    } else {
      el("catalog-info").textContent = "Library: empty (run library build)";
    }
  } catch (_) {
    el("catalog-info").textContent = "";
  }
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
    state.viewMode = state.data.view_mode || "slot";
    snapshotBase();
    syncAliasSlots();
    populateChainSelect();
    renderChain();
    renderGrid();
    updateBanner();
    el("status").textContent = `${state.data.genre.toUpperCase()} · ${state.data.tempo} BPM · ${state.data.chain_preset}`;
    el("pattern-id").textContent = state.data.pattern_id ? `id: ${state.data.pattern_id}` : "";
  } catch (e) {
    el("status").textContent = "Error: " + e.message;
  }
}

async function mutateSlot(target, kind) {
  if (!state.data || state.viewMode === "phrase") return;
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
    if (target === "B" || target === "C") {
      state.baseEdited = false;
      snapshotBase();
    }
    renderGrid();
    updateBanner();
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
    el("export-msg").textContent = `Saved → ${data.output_dir}`;
    el("status").textContent = "Export complete";
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

function cycleVelocity(cell) {
  if (!cell.on) {
    cell.on = true;
    cell.vel = 100;
    return;
  }
  const idx = VEL_CYCLE.indexOf(cell.vel || 100);
  const next = VEL_CYCLE[(idx + 1) % VEL_CYCLE.length];
  if (idx === VEL_CYCLE.length - 1) {
    cell.on = false;
    cell.vel = null;
  } else {
    cell.vel = next;
  }
}

function toggleStep(inst, stepIndex, shiftKey) {
  if (state.viewMode === "phrase") return;
  const slot = state.data.slots[state.activeSlot];
  if (!slot || !slot[inst]) return;
  const cell = slot[inst][stepIndex];
  if (shiftKey) {
    cycleVelocity(cell);
  } else {
    if (cell.on) {
      cell.on = false;
      cell.vel = null;
    } else {
      cell.on = true;
      cell.vel = cell.vel || 100;
    }
  }
  if (state.activeSlot === "BASE") {
    checkBaseEdited();
  }
  if (state.activeSlot === "B") syncAliasSlots();
  if (state.activeSlot === "C") syncAliasSlots();
  renderGrid();
}

function renderGrid() {
  const root = el("grid");
  root.innerHTML = "";

  const isPhrase = state.viewMode === "phrase";
  const slot = isPhrase ? state.data.phrase : state.data.slots[state.activeSlot];
  const stepsPerBar = state.data.steps_per_bar || 16;
  const totalSteps = isPhrase ? state.data.phrase_steps || 64 : stepsPerBar;
  const markers = isPhrase ? state.data.phrase_bar_markers || [] : null;

  if (!slot) {
    root.textContent = "No data for this view.";
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
      pad.disabled = isPhrase;
      if (i > 0 && i % stepsPerBar === 0) pad.classList.add("bar-start");
      if (isPhrase && markers && markers[i]) {
        pad.dataset.bar = markers[i];
        pad.title = `Bar ${Math.floor(i / stepsPerBar) + 1} (${markers[i]})`;
      }
      if (cell.on) {
        pad.classList.add("on");
        const v = cell.vel || 100;
        if (v < 80) pad.classList.add("low");
        else if (v < 110) pad.classList.add("mid");
        pad.style.opacity = String(0.45 + (v / 127) * 0.55);
      }
      if (!isPhrase) {
        pad.addEventListener("click", (ev) => {
          toggleStep(inst, i, ev.shiftKey);
        });
      }
      stepsEl.appendChild(pad);
    });

    track.appendChild(stepsEl);
    root.appendChild(track);
  });
}

initControls();
loadCatalogInfo();
loadPattern();
