# Lesson style guide

How a lesson should look and read. It records what the teacher asked for while lesson 10
(pandas) was built, so every new lesson follows the same format. `courses/nlp-basic/lesson10-pandas.md`
is the worked example: when in doubt, copy how it does it. CLAUDE.md covers the build, the syntax
and security; this file covers teaching style.

## Who it is for

- Humanities students, many new to programming. Taught in a classroom on a projector, then
  reread at home. Desktop first, not mobile first.
- The teacher switches ไทย / EN often, so both languages must say the same thing.

## The main rule: show it, don't explain it

An infographic beats a paragraph. Before writing an explanation, ask which picture would make it
obvious, and use one of these:

| To show | Use |
|---|---|
| One table turning into another (filter, groupby, pivot, melt, explode, fill) | `::: transform {before after}` with tints by `group` |
| Two tables becoming one (merge, concat, duplicate keys) | `::: transform {before right after before_name right_name after_name}` |
| Several cases side by side (policies, statistics, join types, a task's steps, key terms) | ```` ```cards ```` (mini column before → after, `venn:`, or `cols`/`rows`) |
| An idea students should try with their hands | an interactive block (the ```` ```index-explorer ```` is the model) |
| A sequence | `::: steps`, or `{steps="…"}` on code for line-by-line focus |
| Code next to its explanation | `::: columns` (first block left) |
| Why something is needed, or what goes wrong without it | a ✗ vs ✓ picture in the style of nlp `images/l12-why-chunk.svg` (below) |
| A system with several steps that feed each other | a flow diagram with icons and numbered steps, or a clickable ```` ```pipeline ```` |

**The model concept picture (teacher: "way clearer, I like this style", 2026-10-18)** is nlp
`images/l12-why-chunk.svg` (`scripts/diagrams/nlp_l12_figures.py`, figure 17):
1. The running example's question in a bubble at the top.
2. Two panels side by side answering that same question: **✗ the problem** (`sw-warn-box`) and **✓ the fix** (`nt-band-a`).
3. In each panel a **drawn object**, not numbers: a page with text lines, a grid of small cards, a stack of pages.
4. **Arrows pointing at the exact spot**, each with 1–2 short labels; the one thing that matters is highlighted (a filled band, a lit card).
5. A one-line result at the bottom of each panel (red ✗, green ✓), and an optional takeaway row in everyday units ("≈ 330 pages" vs "≈ 1 page").
6. **Keep the real numbers and equations** ("the numbers and equation is still important"), attached to what they describe: the cosine beside its dot, the score under its bar, the formula on its panel, Recall@k on the result line. A bare list of scores, ranks and token counts with no picture was "not clear at all"; the numbers themselves stay.
7. **Show every realistic case, not a straw man.** "Without chunking" shows both a small model that reads only the first ~1,000 characters and a big model (up to 1M tokens) that reads it all but blurs 55 scenes into one vector; measure both.
8. **Decide per card how much text it needs.** A picture that tells one complete ✗/✓ story can stand with 1–3 short points. A key card, or a picture packed with several items or new terms (many tiles, strategies, two models compared), needs real context: number the items in the picture and explain each one under it with the running example, because students reread the page at home without the teacher. Test: could a student explain the card back from the page alone?
9. **Important cards end with "Learn more:" links to outside sources**: 3–6 stable, primary or well-known sources (official docs, the original paper, a good visual guide, a benchmark), each with its publisher and one line on what it gives, in both languages. Check every URL loads before adding it. (Pointing to another section or lesson is still not allowed; outside reading is.)

- Mini examples have 3–8 rows, are real rows of the course dataset (or clearly labelled practice
  tables), and every number in them is checked by running pandas.
- Colour tints connect the same thing across tables (same airline, same key value).
- Name the trap in the picture itself: NaN rows, a dropped row, a duplicated row.

## Data

- One running dataset per lesson (lesson 10: the airline reviews, `reviews`; the 8-row `small`).
- Show the data students need **inside the same card** as the question.
- Practice tables get a Download CSV (```` ```dataframe ````) so students can try them in VS Code (the nlp-basic course is taught in VS Code, `env: vscode`).

## Prompts (AI is part of the workflow)

- Every working code cell has the plain-words prompt that writes it: ```` ```prompt {attach} ````
  right after the cell (and its output). It sits behind a **Prompt** button.
- `{attach open}` starts it opened: use it where the prompt is the lesson (the groupby sections).
- Write prompts the way a student would: name the table (`` `reviews` ``), the columns, and what to
  get back. Short lines. Use **the same words as the code** so students can map one to the other,
  for example "group by `Airline Name` แล้วหา mean ของ `Rating`".
- No prompt on: deliberately broken code, predict-the-output exercise cells, timing demos.
- When code is wrong, explain **what is wrong** (a ระวัง box); don't show a "repair prompt".

## Exercises

- Always individual: `mode="solo"` (ทำคนเดียว / On your own).
- Self-contained: the question, the data and any rule are in the same card. Never "ตามกติกาใน
  L10-S25"; write the rule out.
- This holds everywhere, not only in exercises: never point students to another section or lesson
  ("L13-S06", "(บทที่ 12)", "ต้นบท", "see the chart in S05"). Show the data, chart, code or rule
  again where it is needed, or say it in a few words.
- Start with the goal (**โจทย์:** what we want and why), then short numbered steps.
- Students predict by hand first, then use AI or run the code, then compare.
- Answers are checked in pandas. In focus mode and the slide PDF, answers stay hidden.
- Important operations get hands-on practice per case (lesson 10: one set per join type), on
  small tables students can see, plus a "pick the right one for the job" set.

## Big picture first, then the details (2026-10-18)

The teacher explains top-down: the whole route first, then each stop. A lesson made of separate cards
"cuts from one thing to the next with no coherence". So every lesson:

- **Opens with the hook, then a map card**: one picture of the whole lesson (the problem, the 3–5 ways the
  lesson deals with it, what each changes, its tools, and its result on the lesson's running example).
  nlp L11-S21 (`images/l11-map-lesson.svg`) is the model.
- **Groups its cards into parts** with front matter `parts:` (`- { from: l11-s05, title: Fix the query,
  title_th: แก้ query }`). Each card shows "Part 2 of 6 · Fix the query" above its heading and the menu
  groups cards under part titles. Part titles are the map's labels, word for word.
- **Starts each part with a one-sentence bridge**: what the last approach could not do, in a few words, and
  what this part changes ("Part 3: even with the right words, several places match, so rank them better").
  State it; don't point back ("as we saw in S05").
- **Keeps one running example** through every part (nlp L11: *romantic dinner for two*), so each part
  shows its effect on the same search.

## Writing a card and an exercise (nlp lesson 11, 2026-10-18)

What made the teacher say "I don't understand" and what fixed it:

- **Open with a concrete question, then the picture.** "A school posts *Recruiting secondary school
  instructor*; a teacher types *hiring a teacher*. Will they see it?", then the search-bar picture, then one
  short paragraph that answers it. Not a definition first.
- **Use the lesson's own data, with real results.** An abstract mini-table ("bank → river bank? money
  bank?") with no lead-in confused the teacher; "typed *light* → meant a light meal → BM25 returned Rooftop
  52, because its description says *city lights*" did not. Columns that read as a sentence work: *Typed |
  Meant | Returned*.
- **Both sides of a comparison answer the same question.** Lexical vs semantic cards both take *who plays
  Iron Man in Avengers*; never a different example per card.
- **One picture per idea, made from real data** (WordNet around *car*, BM25 scoring *romantic dinner for
  two* word by word). Put the code under it, folded; say the idea in one or two sentences.
- **Exercises: give the material as a small labelled table, never a long comma list.** The 22 synonyms of
  *cheap* became 4 boxes A–D (WordNet's real senses, one row each, the key word in bold). Then two short
  numbered questions that point at the table ("Which box…?", "Which word pulled it in, and from which
  box?").
- **Answers name the item first, then one line of why**: "Box A: *inexpensive*: the only box about price".
- **The projector gets a compact copy** (`::: focus {page=false}`: fewer words per cell, no per-cell Thai
  subtitles) when the page table is too tall; the page keeps the full table.

## Every card has its own context (nlp lesson 12, 2026-10-18)

"I don't understand this" / "some cards have no context" (Part 5, reranking and hybrid search) and "we haven't
taught this before, make it so clear" (faithfulness, correctness) were fixed like this:

- **Open every card with a bold question on the running example**, then the picture, then **numbered points
  (1–3) that explain the picture** with the real numbers (L12 "Beyond naive RAG": *What is taught on 19 October?*
  → fact 4 ranked 4th → why → the reranker moves it to 1st). A picture plus one paragraph, or a bare list of
  cards, reads as "no context".
- **Define each term in the card where it first appears** (naive RAG, bi-encoder, BM25, reranker, candidate
  recall). A picture label such as "bi-encoder (cosine)" does not teach the term.
- **Say why it fails, with a measurement**, and prefer real timings to "too slow" (reranker ≈ 1 ms per pair →
  100,000 chunks ≈ 100 s per question).
- **A set of technique cards gives each technique an example on the course data with its real result**, not a
  one-line definition (multi-query: fact 4 from 4th to 2nd; routing: "What was my midterm score?" → the grades table).
- **A new metric gets four things**: what it compares (a map picture), the formula with every symbol named, a
  hand-worked example on the running question (several answers, each showing a different failure), and how people
  compute it in practice (by hand → similarity scores → LLM as a judge), with real numbers showing why the simpler
  way fails. Then an exercise that scores one example by hand.
- A formula inside a numbered item: inline `$\dfrac{…}{…}$` on its own line (end the lines before it with `\`);
  a `$$…$$` block breaks the list item.

## Explaining

- Define a word before using it (lesson 10 had to add "key" before groupby and merge).
- Basics before shortcuts: `[n:m]` gives n … m-1 on a list before `.loc`/`.iloc` slices; write a
  function with `def`, test it on one example, then `.apply()` it.
- Show the bad way next to the good way when it matters, with real numbers (loop vs `.apply()`
  vs whole-column timing).
- Teach the most common use first (pivot tables: counting before means).
- Keep it simple. If an example or section is hard and not essential, cut it (lesson 10 removed
  the `fares` map/apply example and the assert/mean-of-means section).

## Wording (Thai)

- English technical terms stay in English inside Thai sentences (`DataFrame`, `key`, `merge`).
- "สร้าง copy" (not ทำสำเนา).
- Short sentences. Bold the one idea per paragraph.

## Code

- Lines short enough to fit their box without sideways scrolling (about 60 characters when the code
  shares space). Break long calls over lines; prefer a named step (`keys = [...]`, `extra = ...`)
  over a long one-liner.
- But never split one data item over lines to save width: one string, one row, one fact per line, even if
  that line scrolls. Two string pieces joined silently by Python ("…Mondays, " / "13:00-16:00…") were "too hard
  to recognize" (teacher, 2026-10-18).
- Outputs are real: run `npm run outputs -- <course> <lesson>` after editing code.

### Show or fold a code cell

A folded cell shows only its header (Show code, Prompt, Copy, Download); Show code opens the code and its
output together. Show what the section teaches; fold what only makes it run.

- **Course default** (`code:` in `course.yml`): `open` where writing the code is the skill (nlp-basic,
  stats-dh); `collapsed` where the idea is the point and the code is support (nlp).
- **Show** (`{open}` in a folded course): the code the section is about, cells the teacher steps through
  (`{steps}`), "predict the output" cells, one-line result cells the next paragraph talks about, and code
  inside `::: answer` (it is hidden behind Show answer already).
- **Fold** (`{collapsed}` in an open course): setup (imports only, loading or reloading data, downloads),
  "run to check" copies of a predict cell, plotting code whose chart is the point (a plot cell folds only
  its code; the chart stays on the page), and long helpers whose result a picture or table already shows.
- When a folded cell's result matters to the text, show it on the page anyway: a `::: focus` table or
  figure with the numbers (L11-S09, S12 in nlp).

## Focus mode and PDFs

- Every frame must fit 1280×720 at projector size. Check each changed section in focus mode,
  in **both ไทย and EN**: the Thai subtitle under the heading makes Thai frames about 40px taller.
- Use `::: focus {page=false}` for a projector-only frame (for example the table plus the code to
  predict), so the page does not repeat it.
- When a frame is too tall, fix the projector, not the page: keep the page text as the teacher
  wrote it.
  - Cards: split the set into two ```` ```cards ```` blocks at a point that keeps the page's
    2-per-row rows whole (after card 2 or 4), and give the second `{start=N}` (L10-S28, S39, S40).
  - Transform: `{focus=false}` on it, then a `::: focus {page=false}` copy of the same transform
    with no caption; the teacher says the caption (L10-S28, S33, S35–S37).
  - Change shared CSS only as a last resort, scoped so it reaches no other lesson's frames.
- The only PDF students download is the slides (ดาวน์โหลด PDF (สไลด์): one 16:9 page per frame,
  answers left out), so every frame should also read well on paper.

## Checklist for a new or changed section

1. Picture first; text only for what the picture cannot say.
2. Data visible in the card; numbers verified in pandas; `npm run outputs`.
3. Prompts on working code, in the same words as the code.
4. Both languages say the same thing.
5. Page view at 1280px: nothing scrolls sideways. Focus mode: every frame fits.
6. `npm run check` passes. Publish, commit, push only when the teacher says so.
