/* Beide Theile den Sieg – Both Sides Claimed the Victory: Altenkirchen, Kircheib, Höchstenbach 1796.
   Ein zweisprachiger Quellenapparat. Vanilla JS, Hash-Routen. */
"use strict";

const view = document.getElementById("view");
const D = { mods: null, plates: null, timeline: null, compare: null, texts: {} };

/* ------------------------------------------------------------ language */
let ui = "de";
try { ui = localStorage.getItem("sieg_ui") || ""; } catch (e) { /* storage blocked */ }
if (ui !== "de" && ui !== "en") ui = /^de\b/i.test(navigator.language || "") ? "de" : "en";
let langPref = null;
try { langPref = localStorage.getItem("sieg_lang"); } catch (e) { /* storage blocked */ }

const T = {
  de: {
    title: "Beide Theile den Sieg", nav: { "": "Übersicht", texts: "Texte", compare: "Vergleich", timeline: "Zeitleiste", plates: "Tafeln", sources: "Quellen" },
    switchTo: "English", loading: "Wird geladen…", allTexts: "← Alle Texte", allCmp: "← Alle Vergleiche", citeAs: "zitiert als", cite: "Zitieren als",
    orig: "Original", both: "Original + Übersetzung", trans: "Übersetzung", or: " oder ",
    srcNote: "Quelle und Editionsnotiz", source: "Quelle", planned: "geplant", notTaken: "nicht aufgenommen",
    shipped: "Abgedruckt", plannedH: "Geplant", missingH: "Geprüft und nicht aufgenommen",
    textsTag: "Texte", textsH: "Das Korpus", textsLede: "Jedes Modul ist vollständig lesbar, das Original neben einer Übersetzung: französische Texte mit deutscher, alle Texte mit englischer Übersetzung. Was geprüft und nicht aufgenommen wurde, steht unten mit Begründung.",
    cmpTag: "Vergleich", cmpH: "Kléber, Kray und die Zeugen", tlTag: "Zeitleiste", platesTag: "Tafeln", platesH: "Karten, Pläne, Köpfe",
    fail: "Der Apparat konnte nicht geladen werden: "
  },
  en: {
    title: "Both Sides Claimed the Victory", nav: { "": "Overview", texts: "Texts", compare: "Compare", timeline: "Timeline", plates: "Plates", sources: "Sources" },
    switchTo: "Deutsch", loading: "Loading…", allTexts: "← All texts", allCmp: "← All comparisons", citeAs: "cited as", cite: "Cite as",
    orig: "Original", both: "Original + English", trans: "English", or: " or ",
    srcNote: "Source and editorial note", source: "Source", planned: "planned", notTaken: "not included",
    shipped: "Printed here", plannedH: "Planned", missingH: "Examined and not included",
    textsTag: "Texts", textsH: "The corpus", textsLede: "Every module can be read in full, the original beside an English translation. What was examined and not included is listed below, with the reason.",
    cmpTag: "Compare", cmpH: "Kléber, Kray and the witnesses", tlTag: "Timeline", platesTag: "Plates", platesH: "Maps, plans, faces",
    fail: "The apparatus could not be loaded: "
  }
};
const S = k => T[ui][k];
const SIDES = {
  frz: { de: "Die Franzosen", en: "The French" },
  kais: { de: "Die Kaiserlichen", en: "The Imperial army" },
  land: { de: "Land und Leute", en: "Land and people" },
  zeugen: { de: "Zeugen", en: "Witnesses" },
  rezeption: { de: "Erinnerung", en: "Memory" }
};
const LANGS = {
  de: { de: "Deutsch", en: "German" }, fr: { de: "Französisch", en: "French" },
  la: { de: "Latein", en: "Latin" }, en: { de: "Englisch", en: "English" }
};
/* a field in the reader's language: o.k_en in English if present, else o.k */
const L = (o, k) => (o && ui === "en" && o[k + "_en"] != null) ? o[k + "_en"] : (o ? o[k] : "");

const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const side = s => `<span class="side ${s}">${esc(SIDES[s] ? SIDES[s][ui] : s)}</span>`;
const lname = l => LANGS[l] ? LANGS[l][ui] : l;
const plateOf = id => (D.plates.plates || []).find(p => p.id === id);
const getJSON = url => fetch(url).then(r => { if (!r.ok) throw new Error(url); return r.json(); });

function setUI(lang) {
  ui = lang;
  try { localStorage.setItem("sieg_ui", ui); } catch (e) { /* storage blocked */ }
  applyUI();
  route();
}

function applyUI() {
  document.documentElement.lang = ui;
  document.title = S("title");
  document.querySelectorAll(".top nav a[data-k]").forEach(a => a.textContent = S("nav")[a.dataset.k]);
  const b = document.getElementById("uiBtn");
  b.textContent = S("switchTo");
  b.lang = ui === "de" ? "en" : "de";
}

async function boot() {
  applyUI();
  document.getElementById("uiBtn").onclick = () => setUI(ui === "de" ? "en" : "de");
  [D.mods, D.plates, D.timeline, D.compare] = await Promise.all(
    ["data/modules.json", "data/plates.json", "data/timeline.json", "data/compare.json"].map(getJSON));
  document.getElementById("navCompare").hidden = !(D.compare.pairs || []).length;
  document.getElementById("navPlates").hidden = !(D.plates.plates || []).length;
  window.addEventListener("hashchange", route);
  route();
}

async function text(id) {
  if (!D.texts[id]) D.texts[id] = await getJSON(`data/${id}.json`);
  return D.texts[id];
}

function route() {
  const parts = (location.hash.replace(/^#\/?/, "") || "").split("/").filter(Boolean);
  const [page, ...args] = parts;
  document.querySelectorAll(".top nav a").forEach(a => {
    const t = a.getAttribute("href").replace(/^#\/?/, "");
    a.classList.toggle("on", (t || "") === (page === "text" ? "texts" : page || ""));
  });
  view.innerHTML = "";
  window.scrollTo(0, 0);
  const pages = { "": overview, texts, text: reader, compare, timeline, plates, sources };
  (pages[page || ""] || overview)(args);
}

/* ------------------------------------------------------------ overview */
const OVERVIEW = {
  de: {
    tag: "1796 · Siegburg · Uckerath · Kircheib · Altenkirchen · Höchstenbach",
    h: "Beide Theile eigneten sich den Sieg zu",
    lede: "Im Sommer und Herbst 1796 zogen die französische Sambre-und-Maas-Armee und die kaiserliche Armee dreimal über dieselbe Straße zwischen Sieg und Westerwald: am 4. Juni bei Altenkirchen, am 19. Juni bei Kircheib und Uckerath, am 19. September bei Höchstenbach und Altenkirchen, wo der französische General Marceau tödlich verwundet wurde. Durch ein Land, das mehreren Herren gehörte und zum Teil neutral war.",
    body: "Dieser Apparat folgt den drei Gefechten durch ihre Quellen, in gemeinfreien Drucken, das deutsche oder französische Original neben einer Übersetzung: die Darstellung des Erzherzogs Carl, die Akten des Wiener Kriegsarchivs in der Bearbeitung von 1896, die Erinnerungen Jourdans, Soults und Neys, Klébers Briefe, ein Augenzeuge aus Uckerath und das Tagebuch, das Marceaus letzte Tage festhielt. Die Quellen widersprechen sich in Stärken, Verlusten und Uhrzeiten; der Apparat zeigt die Widersprüche, statt sie zu glätten. Der Titel ist ein Satz des Erzherzogs über den 19. Juni.",
    q: [
      ["Wer hat gesiegt?", "Am 19. Juni, schrieb Erzherzog Carl 1814, eigneten sich beide Theile den Sieg zu. Kléber meldete am selben Tag, der Feind sei nach den mäßigsten Berichten 40.000 Mann stark; der Herausgeber seines Briefes setzte 1818 dagegen, es sei nur Krays Vorhut gewesen, 14.000 Mann. Was die Quellen zählen, hängt davon ab, wer zählt."],
      ["Wem gehörte das Land?", "Die Grafschaft Altenkirchen war, so ein Zeitgenosse, „als preußisches Gebiet neutral“; daneben lagen kurkölnische, bergische, saynische und wiedische Dörfer. Requiriert wurde überall, von beiden Armeen."],
      ["Was sahen die Leute?", "Ein Augenzeuge in Uckerath, Klagen über ein ausgesogenes Land, Plünderung, die der französische Oberbefehlshaber selbst eingestand, und die Ehren, die die Gegner dem sterbenden Marceau erwiesen."],
      ["Lässt sich das spielen?", "Das Begleitspiel ist ein Hexspiel über die drei Gefechte, für beide Seiten, auf der Karte der Landesaufnahme Tranchot/Müffling. Prototyp 0 spielt Kircheib und Uckerath am 19. Juni 1796 (beide-theile-spiel.netlify.app); am Abend schreibt jede Seite ihren Bericht, und die Partie wird mit den Zahlen der Quellen verglichen."]
    ],
    none: "Die ersten Module sind in Arbeit; die Seite „Texte“ nennt sie mit ihren Quellen.",
    have: "Was der Apparat enthält", qs: "Die Fragen"
  },
  en: {
    tag: "1796 · Siegburg · Uckerath · Kircheib · Altenkirchen · Höchstenbach",
    h: "Both sides claimed the victory",
    lede: "In the summer and autumn of 1796 the French Army of the Sambre and Meuse and the Imperial army fought three times along the same road between the Sieg and the Westerwald: on 4 June at Altenkirchen, on 19 June at Kircheib and Uckerath, on 19 September at Höchstenbach and Altenkirchen, where the French general Marceau was mortally wounded. Through a country that belonged to several lords and was in part neutral.",
    body: "This apparatus follows the three actions through their sources, in public-domain prints, the German or French original beside a translation: the account of Archduke Charles, the files of the Vienna war archive as edited in 1896, the memoirs of Jourdan, Soult and Ney, Kléber's letters, an eyewitness at Uckerath and the journal that recorded Marceau's last days. The sources contradict one another on strengths, losses and hours; the apparatus shows the contradictions instead of smoothing them. The title is the Archduke's sentence on 19 June.",
    q: [
      ["Who won?", "On 19 June, the Archduke wrote in 1814, both sides claimed the victory. Kléber reported that day that the most moderate reports put the enemy at 40,000 men; the editor of his letter answered in 1818 that it had been only Kray's advance guard, 14,000 men. What the sources count depends on who is counting."],
      ["Whose country was it?", "The county of Altenkirchen, a contemporary wrote, was “neutral as Prussian territory”; around it lay villages of the Electorate of Cologne, of Berg, of Sayn and of Wied. Both armies requisitioned everywhere."],
      ["What did the people see?", "An eyewitness at Uckerath, complaints of a country sucked dry, plundering admitted by the French commander-in-chief himself, and the honours the enemy paid to the dying Marceau."],
      ["Can it be played?", "The companion game is a hex game on the three actions, for both sides, on the map of the Tranchot/Müffling survey. Prototype 0 plays Kircheib and Uckerath on 19 June 1796 (beide-theile-spiel.netlify.app); in the evening each side writes its report, and the game is compared with the figures of the sources."]
    ],
    none: "The first modules are in preparation; the Texts page lists them with their sources.",
    have: "What the apparatus contains", qs: "The questions"
  }
};

function overview() {
  const O = OVERVIEW[ui];
  view.innerHTML = `
  <div class="hero one">
    <div>
      <span class="tag">${esc(O.tag)}</span>
      <h1>${esc(O.h)}</h1>
      <p class="lede">${esc(O.lede)}</p>
      <p class="readable">${esc(O.body)}</p>
    </div>
  </div>

  <h2>${esc(O.have)}</h2>
  ${D.mods.shipped.length ? `<div class="grid g2">${D.mods.shipped.map(card).join("")}</div>` : `<p class="fine">${esc(O.none)}</p>`}

  <h2>${esc(O.qs)}</h2>
  <div class="grid g2">${O.q.map(([h, p]) => `<div class="panel"><h3>${esc(h)}</h3><p>${esc(p)}</p></div>`).join("")}</div>`;
}

function card(m) {
  return `<a class="card" href="#/text/${m.id}">
    <div>${side(m.side)} <span class="fine">${esc(m.zk)}</span></div>
    <h3>${esc(L(m, "kurz"))}</h3><p class="fine">${esc(L(m, "warum"))}</p></a>`;
}

/* the translation shown: German for French originals in the German interface, else English */
const tr = (u, ul) => (ui === "de" && ul !== "de" && u.de) ? u.de : u.en;
const trLang = (u, ul) => (ui === "de" && ul !== "de" && u.de) ? "de" : "en";

/* ------------------------------------------------------------ texts */
function texts() {
  const other = (list, label) => list.map(m => `
      <div class="card planned"><div>${side(m.side)} <span class="fine">${esc(label)}</span></div>
      <h3>${esc(L(m, "kurz"))}</h3><p class="fine">${esc(L(m, "warum"))}</p><p class="fine"><b>${esc(S("source"))}:</b> ${esc(m.quelle)}</p></div>`).join("");
  view.innerHTML = `
    <span class="tag">${esc(S("textsTag"))}</span><h1>${esc(S("textsH"))}</h1>
    <p class="lede">${esc(S("textsLede"))}</p>
    ${D.mods.shipped.length ? `<h2>${esc(S("shipped"))}</h2><div class="grid g2">${D.mods.shipped.map(card).join("")}</div>` : ""}
    ${(D.mods.planned || []).length ? `<h2>${esc(S("plannedH"))}</h2><div class="grid g2">${other(D.mods.planned, S("planned"))}</div>` : ""}
    ${(D.mods.missing || []).length ? `<h2 id="missing">${esc(S("missingH"))}</h2><div class="grid g2">${other(D.mods.missing, S("notTaken"))}</div>` : ""}`;
}

async function reader([id, secId, unitN]) {
  const m = D.mods.shipped.find(x => x.id === id);
  if (!m) { location.hash = "#/texts"; return; }
  view.innerHTML = `<p class="fine">${esc(S("loading"))}</p>`;
  const t = await text(m.datei);
  const sec = t.sections.find(s => s.id === secId) || t.sections[0];
  const bilingual = sec.units.some(u => u.orig);
  const pref = langPref || (ui === "de" ? "orig" : "both");
  const lang = bilingual ? pref : "en";
  const langs = [...new Set(sec.units.filter(u => u.orig).map(u => u.lang || t.orig_sprache))];
  const origName = langs.length === 1 && langs[0] !== "de" ? `Original (${lname(langs[0])})` : S("orig");
  const labels = { both: S("both"), orig: origName, en: S("trans") };
  view.innerHTML = `
    <p class="fine"><a href="#/texts">${esc(S("allTexts"))}</a></p>
    <span class="tag">${side(m.side)} ${esc(t.jahr)} · ${esc(S("citeAs"))} ${esc(sec.zk)} [n]</span>
    <h1>${esc(L(t, "titel"))}</h1>
    <p class="fine">${esc(L(t, "autor"))}</p>
    <nav class="toc">${t.sections.map(s => `<a href="#/text/${id}/${s.id}" class="${s.id === sec.id ? "on" : ""}">${esc(L(s, "titel"))}</a>`).join("")}</nav>
    <div class="panel readable"><h3>${esc(L(sec, "titel"))}</h3><p>${esc(L(sec, "blurb"))}</p></div>
    ${bilingual ? `<div class="langbar" id="langbar">
      ${["orig", "both", "en"].map(k => `<button data-l="${k}" class="${k === lang ? "on" : ""}">${esc(labels[k])}</button>`).join("")}</div>` : ""}
    <div id="units"></div>
    <div class="panel readable hinweis"><span class="tag">${esc(S("srcNote"))}</span>
      <p><b>${esc(S("source"))}.</b> ${esc(t.quelle)}</p><p>${esc(L(t, "hinweis"))}</p></div>`;
  const box = view.querySelector("#units");
  for (const u of sec.units) {
    const showO = u.orig && lang !== "en", showE = !u.orig || lang !== "orig";
    const cls = ["unit", String(u.n) === unitN ? "hl" : ""].join(" ");
    const ul = u.lang || t.orig_sprache;
    box.insertAdjacentHTML("beforeend", `
      <div class="${cls}" id="u${u.n}">
        <div class="num"><a href="#/text/${id}/${sec.id}/${u.n}" title="${esc(S("cite"))} ${esc(sec.zk)} [${u.n}]">[${u.n}]</a>
          ${u.pg ? `<span class="pg">${esc(t.pg_label || "")} ${esc(pgL(u.pg))}</span>` : ""}</div>
        <div>${u.titel ? `<h4>${esc(L(u, "titel"))}${u.lang && langs.length > 1 ? ` <span class="fine">(${esc(lname(u.lang))})</span>` : ""}</h4>` : ""}
          <div class="cols ${showO && showE ? "" : "one"}">
            ${showO ? `<div class="orig" lang="${esc(ul)}">${esc(u.orig)}</div>` : ""}
            ${showE ? `<div class="text" lang="${trLang(u, ul)}">${esc(tr(u, ul))}</div>` : ""}
          </div></div>
        ${L(u, "note") ? `<div class="note">${esc(L(u, "note"))}</div>` : ""}
      </div>`);
  }
  view.querySelectorAll("#langbar button").forEach(b => b.onclick = () => {
    langPref = b.dataset.l;
    try { localStorage.setItem("mainz_lang", langPref); } catch (e) { /* storage blocked */ }
    route();
  });
  if (unitN) { const el = document.getElementById("u" + unitN); if (el) el.scrollIntoView({ block: "center" }); }
}

// Seitenangaben "S. 20–21" in der englischen Oberfläche als "pp. 20–21"
const pgL = pg => ui === "en" ? pg.replace(/\bAusg\. /g, "ed. ").replace(/\bS\. (\d+)\s*[–-]\s*(\d+)/g, "pp. $1–$2").replace(/\bS\. /g, "p. ").replace(/, Anm\.$/, ", note") : pg;

/* ------------------------------------------------------------ compare */
async function compare([pid]) {
  const CMP = D.compare;
  const pair = (CMP.pairs || []).find(p => p.id === pid);
  if (!pair) {
    view.innerHTML = `
      <span class="tag">${esc(S("cmpTag"))}</span><h1>${esc(S("cmpH"))}</h1>
      <p class="lede">${esc(L(CMP, "lede"))}</p>
      <div class="grid g2">${(CMP.pairs || []).map(p => `<a class="card" href="#/compare/${p.id}">
        <div>${p.voices.map(v => side(v.side || (D.mods.shipped.find(m => m.id === v.text) || {}).side)).join(" ")}</div>
        <h3>${esc(L(p, "titel"))}</h3><p class="fine">${esc(L(p, "frage"))}</p></a>`).join("")}</div>`;
    return;
  }
  view.innerHTML = `<p class="fine"><a href="#/compare">${esc(S("allCmp"))}</a></p><p class="fine">${esc(S("loading"))}</p>`;
  const docs = await Promise.all(pair.voices.map(v => {
    const m = D.mods.shipped.find(x => x.id === v.text);
    return text(m.datei).then(t => ({ v, m, t }));
  }));
  const col = ({ v, m, t }) => {
    const sec = t.sections.find(s => s.id === v.sec);
    const units = v.n.map(n => sec.units.find(u => u.n === n)).filter(Boolean);
    return `<div class="voice">
      <div class="vhead">${side(v.side || m.side)} <b>${esc(v.autor ? L(v, "autor") : L(t, "autor"))}</b><br><span class="fine">${esc(t.jahr)} · ${esc(L(sec, "titel"))}</span></div>
      ${units.map(u => `<div class="vunit">
        <div class="fine"><a href="#/text/${m.id}/${sec.id}/${u.n}">${esc(sec.zk)} [${u.n}]</a>${u.titel ? ` · ${esc(L(u, "titel"))}` : ""}</div>
        <div class="text">${esc(ui === "de" && u.orig && (u.lang || t.orig_sprache) === "de" ? u.orig : tr(u, u.lang || t.orig_sprache))}</div></div>`).join("")}
    </div>`;
  };
  view.innerHTML = `
    <p class="fine"><a href="#/compare">${esc(S("allCmp"))}</a></p>
    <span class="tag">${esc(S("cmpTag"))}</span><h1>${esc(L(pair, "titel"))}</h1>
    <p class="lede">${esc(L(pair, "frage"))}</p>
    <div class="panel readable"><p>${esc(L(pair, "note"))}</p></div>
    <div class="cmp n${docs.length}">${docs.map(col).join("")}</div>`;
}

/* ------------------------------------------------------------ timeline */
function timeline() {
  const TL = D.timeline;
  view.innerHTML = `
    <span class="tag">${esc(S("tlTag"))}</span><h1>1796–1820</h1>
    <p class="lede">${esc(L(TL, "lede"))}</p>
    <div class="legend">${Object.keys(SIDES).map(side).join(" ")}</div>
    <div class="tl">${TL.stations.map(s => {
      const p = s.plate && plateOf(s.plate);
      return `<div class="st" style="--c:var(--${s.side})">
        <div><div class="d">${esc(L(s, "d"))} · ${side(s.side)}</div><h3>${esc(L(s, "titel"))}</h3><p>${esc(L(s, "text"))}</p>
        ${s.cite ? `<p class="fine"><a href="${s.cite}">✦ ${esc(L(s, "citeLabel"))}</a></p>` : ""}</div>
        ${p ? `<img src="assets/plates/${p.id}_t.jpg" alt="${esc(L(p, "titel"))}" title="${esc(L(p, "titel"))}">` : "<span></span>"}
      </div>`;
    }).join("")}</div>`;
}

/* ------------------------------------------------------------ plates */
function plates() {
  view.innerHTML = `
    <span class="tag">${esc(S("platesTag"))}</span><h1>${esc(S("platesH"))}</h1>
    <p class="lede">${esc(L(D.plates, "lede"))}</p>
    <div class="grid g4">${D.plates.plates.map(p => `
      <figure class="plate card"><a href="#" data-p="${p.id}"><img src="assets/plates/${p.id}_t.jpg" alt="${esc(L(p, "titel"))}"></a>
      <figcaption>${side(p.side)} <b>${esc(L(p, "titel"))}</b><br>${esc(L(p, "caption"))}${p.cite ? ` <a href="${p.cite}">✦</a>` : ""}<br><i>${esc(p.source)}</i></figcaption></figure>`).join("")}</div>
    <p class="fine">${esc(L(D.plates, "credit"))}</p>`;
  view.querySelectorAll("[data-p]").forEach(a => a.onclick = e => {
    e.preventDefault();
    const p = plateOf(a.dataset.p);
    const lb = document.createElement("div");
    lb.className = "lightbox";
    lb.innerHTML = `<figure><img src="assets/plates/${p.id}.jpg" alt="${esc(L(p, "titel"))}"><figcaption class="cap"><b>${esc(L(p, "titel"))}.</b> ${esc(L(p, "caption"))}</figcaption></figure>`;
    lb.onclick = () => lb.remove();
    document.body.append(lb);
  });
}

/* ------------------------------------------------------------ sources */
const METHOD = {
  de: {
    tag: "Quellen, Methode, Grenzen", h: "Wie dieser Apparat gemacht ist",
    p: [
      ["Nur Gemeinfreies.", "Jeder Text stammt aus einem Druck, dessen Schutzfrist abgelaufen ist; die Quelle steht auf seiner Seite. Neuere Darstellungen, die noch geschützt sind, werden höchstens als Hinweis genannt."],
      ["Die Seite ist maßgeblich.", "Die Texte sind am Seitenbild gelesen, nicht aus der maschinellen Texterkennung übernommen, die bei Fraktur nur Hilfsmittel ist. Schreibung und Zeichensetzung der Drucke bleiben erhalten; jede Korrektur, die über das Offensichtliche hinausgeht, steht in den Anmerkungen."],
      ["Übersetzungen.", "Die Übersetzungen ins Deutsche und Englische sind eigene Arbeit, nah am Original und gemeinfrei (CC0): eine Lesehilfe, keine kritische Übersetzung."],
      ["Stimmen und Abstände.", "Der Erzherzog schrieb achtzehn Jahre nach den Gefechten, als Feldherr und Lehrer der Kriegskunst; Jourdan, Soult und Ney verteidigten in ihren Erinnerungen ihre eigenen Entscheidungen; das Kriegsarchiv bearbeitete 1896 die Akten einer Seite. Jedes Modul nennt, wer schrieb, wann und für wen."],
      ["Widersprüche.", "Wo die Quellen in Stärken, Verlusten oder Uhrzeiten auseinandergehen, stehen sie nebeneinander, mit der Angabe, wer welche Zahl nennt. Der Apparat entscheidet nicht, wo die Quellen es nicht erlauben."]
    ],
    printed: "Abgedruckte Quellen", plates: "Tafeln"
  },
  en: {
    tag: "Sources, method, limits", h: "How this apparatus is made",
    p: [
      ["Public domain only.", "Every text comes from a print whose term of protection has expired; the source is named on its page. More recent studies still under copyright are named at most as pointers."],
      ["The page decides.", "The texts are read against the page images, not taken from machine text recognition, which for blackletter is only an aid. Spelling and punctuation of the prints are kept; any correction beyond the obvious is given in the notes."],
      ["Translations.", "The German and English translations are my own, close to the original and in the public domain (CC0): a reading aid, not a critical translation."],
      ["Voices and distances.", "The Archduke wrote eighteen years after the actions, as a commander and a teacher of the art of war; Jourdan, Soult and Ney defended their own decisions in their memoirs; the war archive edited one side's files in 1896. Every module says who wrote, when and for whom."],
      ["Contradictions.", "Where the sources differ on strengths, losses or hours, they stand side by side, with who gives which figure. The apparatus does not decide where the sources do not allow it."]
    ],
    printed: "Sources printed here", plates: "Plates"
  }
};

function sources() {
  const M = METHOD[ui];
  view.innerHTML = `
    <span class="tag">${esc(M.tag)}</span><h1>${esc(M.h)}</h1>
    <div class="readable">${M.p.map(([b, p]) => `<p><b>${esc(b)}</b> ${esc(p)}</p>`).join("")}</div>
    ${D.mods.shipped.length ? `<h2>${esc(M.printed)}</h2>
    <div class="grid g2">${D.mods.shipped.map(m => `<div class="panel"><b>${esc(L(m, "kurz"))}</b><p class="fine" id="src-${m.id}">…</p></div>`).join("")}</div>` : ""}
    ${(D.plates.plates || []).length ? `<h2>${esc(M.plates)}</h2><p class="fine readable">${esc(L(D.plates, "credit"))}</p>` : ""}`;
  D.mods.shipped.forEach(async m => {
    const t = await text(m.datei);
    const el = document.getElementById("src-" + m.id);
    if (el) el.textContent = t.quelle;
  });
}

boot().catch(e => { view.innerHTML = `<p>${esc(S("fail"))}${esc(e.message)}</p>`; });
