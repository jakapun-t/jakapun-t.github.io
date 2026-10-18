// Interactive blocks added for stats-dh lesson 10 (model tuning). Runtime: templates/interactives.js.
// Both reuse the .ixp card look of ```index-explorer, so focus mode scales them the same way.
//
// ```stepper {control="slider"}       one bar chart per step; a slider (or ← → buttons) moves between them
// title_th: ...                          the card header
// title_en: ...
// slider_th: ค่า alpha                   label of the slider (control="slider")
// slider_en: alpha
// start: 2                               step shown first (default 0)
// steps:
//   - label: "alpha = 0.1"               shown above the bars, and under the slider as its tick
//     bars: { bmi: 505, bp: 317, ... }   name: value; negative values grow left of a centre line
//     highlight: [bmi]                   bars drawn in the accent colour (e.g. the round's winner)
//     note_th: ...                       one sentence under the bars
//     note_en: ...
// A bar whose value is exactly 0 is drawn as "0" with a crossed-out name (a feature Lasso dropped).
// Every step is rendered at build time; the script only shows one at a time.
//
// ```sorter                             click Keep / Drop for each column, then Check
// target: SalePrice
// items:
//   - name: OwnerName
//     def_th: ชื่อเจ้าของ
//     def_en: Owner's name
//     answer: drop                       keep | drop | either (any choice is fine; the reason matters)
//     why_th: ...
//     why_en: ...

import { load as loadYaml } from 'js-yaml';
import { esc, inline, T, icon } from './render.mjs';
import { LectureError } from './parse.mjs';

const TH = (th, en) => T([inline(String(th ?? en ?? '')), inline(String(en ?? th ?? ''))], { thHtml: true, enHtml: true });

function yamlOf(n, ctx, kind) {
  try {
    return loadYaml(n.text);
  } catch (e) {
    throw new LectureError(ctx.file, n.line, `\`\`\`${kind} is not valid YAML: ${e.message.split('\n')[0]}`);
  }
}

const fmt = (v) => (Number.isInteger(v) ? String(v) : String(Math.round(v * 1000) / 1000));

function renderStepper(n, ctx) {
  const d = yamlOf(n, ctx, 'stepper');
  if (!d || !Array.isArray(d.steps) || !d.steps.length) throw new LectureError(ctx.file, n.line, '```stepper needs steps: (a list)');
  const values = d.steps.flatMap((s, k) => {
    if (!s.bars || typeof s.bars !== 'object') throw new LectureError(ctx.file, n.line, `\`\`\`stepper step ${k + 1} needs bars: { name: value, ... }`);
    return Object.values(s.bars).map(Number);
  });
  const max = Math.max(...values.map(Math.abs)) || 1;
  const signed = values.some((v) => v < 0);
  const start = Math.min(Math.max(Number(d.start) || 0, 0), d.steps.length - 1);
  const slider = (n.attrs.control ?? 'slider') === 'slider';

  const panels = d.steps
    .map((s, k) => {
      const hl = new Set(s.highlight ?? []);
      const bars = Object.entries(s.bars)
        .map(([name, raw]) => {
          const v = Number(raw);
          const w = ((Math.abs(v) / max) * (signed ? 50 : 100)).toFixed(2);
          const cls = ['stp-bar', v < 0 ? 'is-neg' : '', hl.has(name) ? 'is-hl' : ''].filter(Boolean).join(' ');
          const zero = v === 0;
          return `<li class="stp-row${zero ? ' is-zero' : ''}${hl.has(name) ? ' is-hl' : ''}"><span class="stp-name">${esc(name)}</span><span class="stp-track${signed ? ' is-signed' : ''}">${zero ? '' : `<span class="${cls}" style="--w:${w}%"></span>`}</span><span class="stp-val">${fmt(v)}</span></li>`;
        })
        .join('');
      const note = s.note_th || s.note_en ? `<p class="stp-note">${TH(s.note_th, s.note_en)}</p>` : '';
      return `<div class="stp-panel" data-step="${k}"${k === start ? '' : ' hidden'}><p class="stp-label">${inline(String(s.label ?? ''))}</p><ul class="stp-bars">${bars}</ul>${note}</div>`;
    })
    .join('');

  const labels = d.steps.map((s) => String(s.label ?? ''));
  const control = slider
    ? `<label class="stp-slider"><span class="stp-slider-label">${TH(d.slider_th ?? 'เลื่อน', d.slider_en ?? 'Slide')}</span><input type="range" min="0" max="${d.steps.length - 1}" step="1" value="${start}" aria-valuetext="${esc(labels[start])}"></label><ol class="stp-ticks">${labels.map((l, k) => `<li style="--f:${labels.length > 1 ? k / (labels.length - 1) : 0}">${esc(l.replace(/^[^=]*=\s*/, ''))}</li>`).join('')}</ol>`
    : `<div class="stp-buttons"><button type="button" data-stp="prev">← ${T(['ก่อนหน้า', 'Back'])}</button><span class="stp-pos" aria-live="polite">${start + 1} / ${d.steps.length}</span><button type="button" data-stp="next">${T(['ถัดไป', 'Next'])} →</button></div>`;

  return `<figure class="ixp stp" data-stp data-labels="${esc(JSON.stringify(labels))}">
<figcaption class="ixp-head">${icon('pointer', 16)}${TH(d.title_th ?? 'ลองเล่น', d.title_en ?? 'Try it')}</figcaption>
<div class="ixp-body"><div class="stp-control">${control}</div>${panels}</div>
</figure>`;
}

const ANSWERS = new Set(['keep', 'drop', 'either']);

function renderSorter(n, ctx) {
  const d = yamlOf(n, ctx, 'sorter');
  if (!d || !Array.isArray(d.items) || !d.items.length) throw new LectureError(ctx.file, n.line, '```sorter needs items: (a list)');
  const rows = d.items
    .map((it, k) => {
      if (!it.name || !ANSWERS.has(it.answer)) throw new LectureError(ctx.file, n.line, `\`\`\`sorter item ${k + 1} needs name: and answer: keep | drop | either`);
      return `<li class="srt-row" data-answer="${it.answer}">
<div class="srt-feat"><code>${esc(it.name)}</code><span class="srt-def">${TH(it.def_th, it.def_en)}</span></div>
<div class="srt-btns" role="group" aria-label="${esc(it.name)}"><button type="button" data-choice="keep" aria-pressed="false">${icon('ok', 14)}${T(['เก็บ', 'Keep'])}</button><button type="button" data-choice="drop" aria-pressed="false">${icon('bad', 14)}${T(['ตัด', 'Drop'])}</button></div>
<p class="srt-why" hidden><span class="srt-verdict"></span>${TH(it.why_th, it.why_en)}</p>
</li>`;
    })
    .join('');
  return `<figure class="ixp srt" data-srt>
<figcaption class="ixp-head">${icon('pointer', 16)}${T(['ลองเล่น: เก็บหรือตัด', 'Try it: keep or drop'])}${d.target ? `<span class="srt-target">target: <code>${esc(d.target)}</code></span>` : ''}</figcaption>
<div class="ixp-body"><ul class="srt-list">${rows}</ul>
<div class="srt-actions"><button type="button" data-srt="check">${T(['ตรวจคำตอบ', 'Check'])}</button><button type="button" data-srt="reset">${T(['เริ่มใหม่', 'Reset'])}</button><span class="srt-score" aria-live="polite"></span></div></div>
</figure>`;
}

// ```pipeline                           a clickable flow diagram (nlp lesson 12, the RAG pipeline)
// title_th: ...                          the card header
// title_en: ...
// rows:                                  the bands, top to bottom
//   - { title_th: ..., title_en: 1 Indexing, note_th: ..., note_en: once, before any question }
// nodes:                                 in reading order (Back / Next follow it)
//   - id: docs
//     row: 1                             which band (1-based)
//     name_th: เอกสาร
//     name_en: Documents
//     icon: doc                          doc | scissors | vector | database | question | search | chunks | prompt | llm | answer
//     to: [split]                        where its output goes; inputs are worked out from these
//     what_th: ...                       one or two sentences: what this step does
//     what_en: ...
//     example: |                         real data from the lesson, shown in mono
//       fact 7: The final exam is ...
// Clicking a box (or Back / Next) shows its panel and marks the boxes it reads from ("in") and feeds ("out").
// Line icons for ```pipeline boxes (24×24, stroke = currentColor); a node picks one with `icon: <name>`.
const PFL_ICONS = {
  doc: '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="M9 12h6M9 15h6M9 18h4"/>',
  scissors: '<circle cx="6" cy="7" r="2.5"/><circle cx="6" cy="17" r="2.5"/><path d="M8.2 8.3L20 18M8.2 15.7L20 6"/>',
  vector: '<path d="M7 4H4v16h3M17 4h3v16h-3"/><circle cx="9" cy="12" r="1" fill="currentColor"/><circle cx="12" cy="12" r="1" fill="currentColor"/><circle cx="15" cy="12" r="1" fill="currentColor"/>',
  database: '<ellipse cx="12" cy="6" rx="7" ry="2.8"/><path d="M5 6v12c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8V6"/><path d="M5 12c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8"/>',
  question: '<path d="M4 5h16v11H10l-4 4v-4H4z"/><path d="M10.2 8.6a1.9 1.9 0 1 1 2.6 1.8c-.6.3-.8.7-.8 1.3"/><circle cx="12" cy="13.6" r=".6" fill="currentColor"/>',
  search: '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
  chunks: '<path d="M8 3h10v13H8z"/><path d="M5 6v14h10"/><path d="M11 7h4M11 10h4M11 13h3"/>',
  prompt: '<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M7 9l3 3-3 3"/><path d="M12 15h5"/>',
  llm: '<circle cx="6" cy="7" r="2"/><circle cx="6" cy="17" r="2"/><circle cx="18" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><path d="M8 7.8l2.3 3M8 16.2l2.3-3M14 12h2"/>',
  answer: '<path d="M4 5h16v11H10l-4 4v-4H4z"/><path d="M8.5 10.5l2.5 2.5 4.5-4.5"/>',
};
const pflIcon = (name) => (PFL_ICONS[name] ? `<svg class="pfl-ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${PFL_ICONS[name]}</svg>` : '');

function renderPipeline(n, ctx) {
  const d = yamlOf(n, ctx, 'pipeline');
  if (!d || !Array.isArray(d.rows) || !Array.isArray(d.nodes) || !d.nodes.length) throw new LectureError(ctx.file, n.line, '```pipeline needs rows: and nodes: (lists)');
  const ids = new Set(d.nodes.map((x) => x.id));
  const name = new Map(d.nodes.map((x) => [x.id, TH(x.name_th, x.name_en)]));
  const from = new Map(d.nodes.map((x) => [x.id, []]));
  for (const x of d.nodes) {
    for (const t of x.to ?? []) {
      if (!ids.has(t)) throw new LectureError(ctx.file, n.line, `\`\`\`pipeline node "${x.id}" goes to unknown node "${t}"`);
      from.get(t).push(x.id);
    }
  }
  const num = new Map(d.nodes.map((x, k) => [x.id, k + 1]));
  const start = ids.has(d.start) ? d.start : d.nodes[0].id;

  const rows = d.rows
    .map((r, k) => {
      const nodes = d.nodes
        .filter((x) => Number(x.row) === k + 1)
        .map((x) => `<li><button type="button" class="pfl-node" data-id="${esc(x.id)}" aria-pressed="${x.id === start}"><span class="pfl-n">${num.get(x.id)}</span>${pflIcon(x.icon)}<span class="pfl-name">${name.get(x.id)}</span></button></li>`)
        .join('');
      return `<div class="pfl-row pfl-row-${(k % 3) + 1}"><p class="pfl-row-title"><strong>${TH(r.title_th, r.title_en)}</strong>${r.note_th || r.note_en ? `<span>${TH(r.note_th, r.note_en)}</span>` : ''}</p><ol class="pfl-nodes">${nodes}</ol></div>`;
    })
    .join('');

  const chips = (list) => list.map((id) => `<span class="pfl-chip">${num.get(id)} ${name.get(id)}</span>`).join(' ');
  const panels = d.nodes
    .map((x) => {
      const ins = from.get(x.id);
      const outs = x.to ?? [];
      const io = `<p class="pfl-io"><span class="pfl-io-in"><b>${T(['รับจาก', 'Gets'])}</b> ${ins.length ? chips(ins) : T(['(จุดเริ่มต้น)', '(the start)'])}</span><span class="pfl-io-out"><b>${T(['ส่งต่อให้', 'Sends to'])}</b> ${outs.length ? chips(outs) : T(['(ผลลัพธ์สุดท้าย)', '(the end result)'])}</span></p>`;
      const ex = x.example ? `<pre class="pfl-ex">${esc(String(x.example).replace(/\s+$/, ''))}</pre>` : '';
      return `<div class="pfl-panel" data-id="${esc(x.id)}" data-in="${esc(ins.join(' '))}" data-out="${esc(outs.join(' '))}"${x.id === start ? '' : ' hidden'}>
<p class="pfl-title"><span class="pfl-n">${num.get(x.id)}</span>${pflIcon(x.icon)}${name.get(x.id)}</p><p class="pfl-what">${TH(x.what_th, x.what_en)}</p>${io}${ex}</div>`;
    })
    .join('');

  return `<figure class="ixp pfl" data-pfl>
<figcaption class="ixp-head">${icon('pointer', 16)}${TH(d.title_th ?? 'ลองกดแต่ละขั้น', d.title_en ?? 'Click each step')}</figcaption>
<div class="ixp-body"><div class="pfl-map">${rows}</div>
<div class="pfl-side"><div class="pfl-nav"><button type="button" data-pfl="prev">← ${T(['ก่อนหน้า', 'Back'])}</button><span class="pfl-pos" aria-live="polite">${num.get(start)} / ${d.nodes.length}</span><button type="button" data-pfl="next">${T(['ถัดไป', 'Next'])} →</button></div>${panels}
<p class="pfl-key"><span class="pfl-key-in"></span>${T(['รับจาก', 'gets from'])}<span class="pfl-key-out"></span>${T(['ส่งต่อให้', 'sends to'])}</p></div></div>
</figure>`;
}

export const INTERACTIVE_LANGS = new Set(['stepper', 'sorter', 'pipeline']);

export function renderInteractive(n, ctx) {
  if (n.lang === 'pipeline') return renderPipeline(n, ctx);
  return n.lang === 'stepper' ? renderStepper(n, ctx) : renderSorter(n, ctx);
}
