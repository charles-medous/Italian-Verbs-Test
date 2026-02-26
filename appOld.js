"use strict";

/* ---------- Config ---------- */
const DEFAULT_CARDS = 5;
const DECK_BASE = "decks";
/* ---------- State ---------- */
const state = {
  direction: "fr-it",
  deckFiles: [],
  verbs: [],
  availableTenses: [],      // "Mood|Tense" strings
  selectedTense: "",
  gameCount: DEFAULT_CARDS,
  queue: [],
  index: 0,
  current: null,
  answersAll: [],
  results: [],
  sessionOrder: {}, // remembers a shuffled order per direction+tense across games
};
  


/* ---------- Elements ---------- */
document.getElementById("resetShuffleBtn")?.addEventListener("click", () => {
  if (!state.selectedTense) {
    // If no tense chosen yet, clear all rotations
    state.sessionOrder = {};
  } else {
    const [mood, tense] = state.selectedTense.split("|");
    const key = `${state.direction}__${mood}__${tense}`;
    delete state.sessionOrder[key];
  }
  alert("Shuffle reset — the next game will use a fresh random order.");
});
const el = {
  setup: document.getElementById("setup"),
  game: document.getElementById("game"),
  results: document.getElementById("results"),
  direction: document.getElementById("direction"),
  tense: document.getElementById("tense"),
  count: document.getElementById("count"),
  startBtn: document.getElementById("startBtn"),
  deckInfo: document.getElementById("deckInfo"),
  progress: document.getElementById("progress"),
  tenseLabel: document.getElementById("tenseLabel"),
  promptLemma: document.getElementById("promptLemma"),
  targetLemma: document.getElementById("targetLemma"),
  instruction: document.getElementById("instruction"),
  inputsGrid: document.getElementById("inputsGrid"),
  checkBtn: document.getElementById("checkBtn"),
  nextBtn: document.getElementById("nextBtn"),
  instantScore: document.getElementById("instantScore"),
  scoreLine: document.getElementById("scoreLine"),
  resultsTableWrap: document.getElementById("resultsTableWrap"),
  restartBtn: document.getElementById("restartBtn")
};

/* ---------- Utils ---------- */
function normalize(s) {
  return (s ?? "")
    .toString()
    .trim()
    .toLowerCase()
    .normalize("NFD")              // split accents
    .replace(/[\u0300-\u036f]/g, "") // strip accents
    .replace(/\s+/g, " ");         // collapse spaces
}
function sample(arr, k) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a.slice(0, k);
}
function showSetup(){ el.setup.classList.remove("hidden"); el.game.classList.add("hidden"); el.results.classList.add("hidden"); }
function showGame(){  el.setup.classList.add("hidden");    el.game.classList.remove("hidden"); el.results.classList.add("hidden"); }
function showResults(){el.setup.classList.add("hidden");    el.game.classList.add("hidden");    el.results.classList.remove("hidden"); }


function bareForm(expectedFull, pronoun) {
  let s = (expectedFull || "").toLowerCase().trim();
  if (s.startsWith("che ")) s = s.slice(4).trim();          // drop "che " (congiuntivo)
  const p = (pronoun || "").toLowerCase().trim();
  if (p && s.startsWith(p + " ")) s = s.slice(p.length + 1).trim(); // drop pronoun
  return s;
}
function scrollToSection(sectionEl) {
  requestAnimationFrame(() => {
    sectionEl.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}
function keepViewport(fn) {
  const x = window.scrollX, y = window.scrollY;
  fn();                          // run the DOM update
  window.scrollTo(x, y);         // put the viewport back exactly
}
function infinitiveLabel(lang) {
  return lang === "it" ? "Infinito" : (lang === "fr" ? "Infinitif" : "Infinitive");
}
function getExpectedInfinitive(verbObj) {
  // Prefer the JSON “Infinito/Infinitif → Presente/Présent”, fallback to target_lemma
  return (verbObj.Infinito?.Presente?.[0])
      || (verbObj.Infinitif?.["Présent"]?.[0])
      || verbObj.target_lemma
      || "";
}
function shuffleInPlace(a) {
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
}


/* ---------- Data loading ---------- */
async function loadDeck(direction) {
  state.direction = direction;
  el.deckInfo.textContent = `Deck: ${direction}`;
  el.tense.innerHTML = `<option value="" disabled selected>Loading tenses…</option>`;

  // Load index.json

  const idxUrl = `${DECK_BASE}/${direction}/index.json`;
  let files;
  try {
    const idxRes = await fetch(idxUrl, { cache: "no-store" });
    if (!idxRes.ok) throw new Error(`HTTP ${idxRes.status} at ${idxUrl}`);
    const data = await idxRes.json();
    files = data.files || [];
  } catch (e) {
    console.error("Failed to load deck index:", e);
    el.tense.innerHTML = `<option value="" disabled selected>Cannot load ${idxUrl}</option>`;
    return;
  }
  state.deckFiles = files;

  // Load each verb JSON
  const verbs = [];
  for (const f of files) {
    const url = `${DECK_BASE}/${direction}/${f}`;
    try {
      const r = await fetch(url, { cache: "no-store" });
      if (!r.ok) throw new Error(`HTTP ${r.status} at ${url}`);
      const v = await r.json();
      verbs.push(v);
    } catch (e) {
      console.error("Failed to load verb file:", url, e);
      alert(`Problem with ${url}\n→ ${e.message}`);
    }
  }
  state.verbs = verbs;

  // Build available tenses (Mood|Tense) where there are exactly 6 forms
  const tensesSet = new Set();
  for (const v of state.verbs) {
    for (const mood of Object.keys(v)) {
      if (["source_lang","target_lang","source_lemma","target_lemma","meta","pronouns"].includes(mood)) continue;
      const moodObj = v[mood];
      if (!moodObj || typeof moodObj !== "object") continue;
      for (const tense of Object.keys(moodObj)) {
        const arr = moodObj[tense];
        if (Array.isArray(arr) && arr.length === 6) {
          tensesSet.add(`${mood}|${tense}`);
        }
      }
    }
  }
  state.availableTenses = Array.from(tensesSet);

  // Populate tense select
  if (state.availableTenses.length === 0) {
    el.tense.innerHTML = `<option value="" disabled selected>No tenses found</option>`;
    return;
  }
  el.tense.innerHTML = `<option value="" disabled selected>Select a tense…</option>`;
  const byMood = {};
  for (const mt of state.availableTenses) {
    const [mood, tense] = mt.split("|");
    (byMood[mood] ||= []).push(tense);
  }
  for (const mood of Object.keys(byMood)) {
    const group = document.createElement("optgroup");
    group.label = mood;
    for (const tense of byMood[mood]) {
      const opt = document.createElement("option");
      opt.value = `${mood}|${tense}`;
      opt.textContent = `${mood} — ${tense}`;
      group.appendChild(opt);
    }
    el.tense.appendChild(group);
  }

  // Make the tense picker scrollable when there are many entries
  if (state.availableTenses.length > 8) {
    el.tense.size = Math.min(12, state.availableTenses.length); // shows a scroll
  } else {
    el.tense.size = 1; // standard dropdown
  }
}

/* ---------- Game build ---------- */
function buildQueue() {
  const [mood, tense] = state.selectedTense.split("|");
  const pool = state.verbs.filter(
    v => v[mood] && Array.isArray(v[mood][tense]) && v[mood][tense].length === 6
  );
  if (pool.length === 0) {
    alert(`No verbs have "${mood} → ${tense}" in this deck.`);
    return false;
  }

  // Key per direction+tense so each combo has its own rotation
  const key = `${state.direction}__${mood}__${tense}`;

  // Build/refresh the rotation if it doesn't exist or is out of sync with pool
  // (e.g., you added/removed files)
  const poolSet = new Set(pool.map(v => v.source_lemma + "→" + v.target_lemma));
  let rot = state.sessionOrder[key]?.filter(v =>
    poolSet.has(v.source_lemma + "→" + v.target_lemma)
  ) || [];

  // If rotation is empty or too small for a game, (re)fill it with a fresh shuffle
  if (rot.length < state.gameCount) {
    // Start from all available verbs, shuffle, then append to whatever was left
    const fresh = pool.slice();
    shuffleInPlace(fresh);
    // Remove any duplicates that might already be in rot
    const seen = new Set(rot.map(v => v.source_lemma + "→" + v.target_lemma));
    const newOnes = fresh.filter(v => !seen.has(v.source_lemma + "→" + v.target_lemma));
    rot = rot.concat(newOnes);
  }

  // Take k from the front (no repeats until exhaustion)
  const k = Math.min(state.gameCount, rot.length);
  state.queue = rot.slice(0, k);
  // Save the remainder for the next game
  state.sessionOrder[key] = rot.slice(k);

  state.index = 0;
  state.answersAll = [];
  state.results = [];
  return true;
}


/* ---------- Rendering ---------- */
function renderCard() {
  const [mood, tense] = state.selectedTense.split("|");
  const v = state.queue[state.index];

  // Always reset the game area and jump to top
  el.inputsGrid.innerHTML = "";
  window.scrollTo({ top: 0, behavior: "instant" });

  const tgtLang = v.target_lang;
  const pronouns = v.pronouns?.[tgtLang] || [];
  const forms = v[mood][tense];

  state.current = { verb: v, forms, pronouns, answers: Array(6).fill("") };

  el.progress.textContent = `${state.index + 1} / ${state.queue.length}`;
  el.tenseLabel.textContent = `Tense: ${mood} — ${tense}`;
  el.promptLemma.textContent = v.source_lemma || "—";
  el.targetLemma.textContent = v.target_lemma || "—";
  el.instruction.textContent = `First type the ${infinitiveLabel(v.target_lang)} (lemma), then fill the ${tense} forms (${tgtLang.toUpperCase()}):`;


  // --- Infinitive row (target language) ---
  const infLabTxt = infinitiveLabel(v.target_lang);     // "Infinito" or "Infinitif"
  const expectedInf = getExpectedInfinitive(v);         // e.g., "amare"
  state.current.infExpected = expectedInf;
  state.current.infAnswer = "";

  const infRow = document.createElement("div");
  infRow.className = "item";
  const infLab = document.createElement("label");
  infLab.textContent = infLabTxt;
  const infInp = document.createElement("input");
  infInp.type = "text";
  infInp.placeholder = "…";
  infInp.addEventListener("input", (e) => {
    state.current.infAnswer = e.target.value;
  });
  infRow.appendChild(infLab);
  infRow.appendChild(infInp);
  el.inputsGrid.appendChild(infRow);

  // Build one row per pronoun
  for (let i = 0; i < 6; i++) {
    const cell = document.createElement("div");
    cell.className = "item";
    const lab = document.createElement("label");
    lab.textContent = pronouns[i] || "—";
    const inp = document.createElement("input");
    inp.type = "text";
    inp.placeholder = "…";
    inp.dataset.index = String(i);
    inp.addEventListener("input", (e) => {
      const idx = Number(e.target.dataset.index);
      state.current.answers[idx] = e.target.value;
    });
    cell.appendChild(lab);
    cell.appendChild(inp);
    el.inputsGrid.appendChild(cell);
  }

  el.checkBtn.disabled = false;
  el.nextBtn.disabled = true;
  el.instantScore.textContent = "";
  const first = el.inputsGrid.querySelector("input");
  if (first) first.focus({ preventScroll: true });
}

function gradeCurrent() {
  const { forms, answers, pronouns, infExpected, infAnswer } = state.current;
  const rows = [];
  let correctCount = 0;

  // 1) Infinitive first
  const wantInf = infExpected || "";
  const gotInf  = infAnswer || "";
  const okInf   = normalize(gotInf) === normalize(wantInf);
  if (okInf) correctCount++;
  rows.push({ pronoun: infinitiveLabel(state.current.verb.target_lang), want: wantInf, got: gotInf, ok: okInf });

  // 2) Six persons
  for (let i = 0; i < 6; i++) {
    const wantFull = forms[i];              // e.g. "io amo"
    const got      = answers[i] || "";
    const pronoun  = pronouns[i] || "";

    // Accept with or without pronoun ("io amo" or "amo")
    const wantNorm = normalize(wantFull);
    const wantBare = (function bareForm(expectedFull, p){
      let s = (expectedFull || "").toLowerCase().trim();
      if (s.startsWith("che ")) s = s.slice(4).trim();      // drop "che " (subj.)
      const pr = (p || "").toLowerCase().trim();
      if (pr && s.startsWith(pr + " ")) s = s.slice(pr.length + 1).trim();
      return s;
    })(wantFull, pronoun);
    const gotNorm  = normalize(got);

    const ok = (gotNorm === wantNorm) || (gotNorm === wantBare);
    if (ok) correctCount++;
    rows.push({ pronoun, want: wantFull, got, ok });
  }

  const score = { correct: correctCount, total: 7, rows };   // 1 (inf) + 6 persons
  state.results.push(score);
  state.answersAll.push([infAnswer, ...answers]);

  // Instant feedback
  el.instantScore.textContent = `Card score: ${correctCount} / ${score.total}`;
  el.checkBtn.disabled = true;
  el.nextBtn.disabled = false;

  // Color inputs (now 7 inputs: infinitive + 6 persons)
  const inputs = el.inputsGrid.querySelectorAll("input");
  inputs.forEach((inp, i) => {
    const ok = rows[i].ok;               // row 0 is the infinitive
    inp.classList.remove("ok","bad");
    inp.classList.add(ok ? "ok" : "bad");
  });
}

function renderResults() {
  const totalRight = state.results.reduce((acc, r) => acc + r.correct, 0);
  const totalAsked = state.results.reduce((acc, r) => acc + r.total, 0);
  el.scoreLine.textContent = `Total: ${totalRight} / ${totalAsked}`;

  const [mood, tense] = state.selectedTense.split("|");
  let html = "";
  html += `<div class="muted">Tense: ${mood} — ${tense}</div>`;
  html += `<div class="divider"></div>`;
  html += `<div class="compare">`;

  for (let c = 0; c < state.queue.length; c++) {
    const v = state.queue[c];
    const r = state.results[c];

    const left = r.rows.map(row =>
      `<li><span class="pron">${row.pronoun}</span><span class="answer ok">${row.want}</span></li>`
    ).join("");

    const right = r.rows.map(row =>
      `<li><span class="pron">${row.pronoun}</span><span class="answer ${row.ok ? "ok" : "bad"}">${row.got || "—"}</span></li>`
    ).join("");

    html += `
      <div class="compare-card">
        <div class="compare-head">${c+1}. ${v.source_lemma} → ${v.target_lemma}</div>
        <div class="compare-grid">
          <div class="col">
            <h4>Correct</h4>
            <ul class="list">${left}</ul>
          </div>
          <div class="col">
            <h4>Your answers</h4>
            <ul class="list">${right}</ul>
          </div>
        </div>
      </div>`;
  }

  html += `</div>`;
  el.resultsTableWrap.innerHTML = html;
}



/* ---------- Events ---------- */
el.direction.addEventListener("change", async () => {
  await loadDeck(el.direction.value);
});
el.tense.addEventListener("change", () => {
  state.selectedTense = el.tense.value;
});
el.count.addEventListener("change", () => {
  state.gameCount = Number(el.count.value || DEFAULT_CARDS);
});

el.checkBtn.addEventListener("click", () => {
  gradeCurrent();
});
el.startBtn.addEventListener("click", () => {
  state.selectedTense = el.tense.value;
  state.gameCount = Number(el.count.value || DEFAULT_CARDS);
  if (!state.selectedTense) return alert("Please choose a tense.");
  if (!buildQueue()) return;
  showGame();
  renderCard();
  scrollToSection(el.game);        // <— jump to the game section
});

el.nextBtn.addEventListener("click", () => {
  state.index++;

  // Finished? Show results and SCROLL to them.
  if (state.index >= state.queue.length) {
    showResults();        // hides setup & game, shows results
    renderResults();
    scrollToSection(el.results);   // <-- crucial: do NOT wrap this in keepViewport
    return;
  }

  // Not finished yet: render next card WITHOUT moving the page
  keepViewport(() => renderCard());  // <-- this keeps you on the same spot
});


el.restartBtn.addEventListener("click", () => {
  showSetup();
  scrollToSection(el.setup);       // <— back to setup
});

document.addEventListener("keydown", (e) => {
  if (e.key !== "Enter") return;
  if (!el.game.classList.contains("hidden")) {
    if (!el.checkBtn.disabled) el.checkBtn.click();
    else if (!el.nextBtn.disabled) el.nextBtn.click();
  }
});

/* ---------- Init ---------- */
(async function init() {
  el.count.value = String(DEFAULT_CARDS);
  el.direction.value = "fr-it";
  await loadDeck("fr-it");
})();
