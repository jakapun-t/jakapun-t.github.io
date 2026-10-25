"""Pictures added above the text of stats-dh L15 cards (data reliability and annotation agreement), in the stats-dh card
style: a student can skim the picture and read the card's text for the detail.
  l15-labels-everywhere.svg  S01  everyday places where people label data or judges must agree
  l15-quality-four.svg       S03  the four sides of data quality, each drawn
  l15-shortcut.svg           S05  the validity exercise's idea: the concept you mean vs an easy shortcut (no answer)
  l15-guide-checklist.svg    S07  the five parts to look for in a guideline (empty checklist, no answer)
  l15-lazy-annotator.svg     S08  100 letters: B says Anxiety on 35; a lazy "no" to everything still agrees on 65
  l15-kappa-scale.svg        S10  the Landis & Koch scale with the letters' 0.35 and 0.415
  l15-two-shapes.svg         S11  the table shapes Fleiss (letters × labels) and Krippendorff (raters × letters) take
  l15-which-measure.svg      S13  how many raters × what kind of label → which measure (pilot 1 values)
  l15-lf-votes.svg           S15  4 labeling functions voting on 8 sentences, with how often each is right
  l15-llm-prompt.svg         S16  zero-shot vs a guided prompt on "It wasn't bad."
  l15-active-loop.svg        S17  the active-learning loop and the three letters' probabilities
  l15-takeaways.svg          S19  six takeaways as icons

    course/.venv/bin/python scripts/diagrams/stats_l15_cards.py courses/stats-dh/images

Real numbers (the lesson's code cells on scripts/diagrams/l15_practice_data.py output): B says Anxiety on 35 of 100, a
lazy all-"no" agrees 0.65; kappa Anxiety-or-not 0.35, 4 emotions (A vs B) 0.415; Fleiss 0.373, Krippendorff alpha 0.375,
ICC formality 0.418; labeling functions: lf_cry 4 of 4 right, lf_heartbroken 2 of 2, lf_happy 2 of 3, lf_has_I 2 of 6;
letters X [0.99, 0.005, 0.005] margin 0.98 entropy 0.09, Y [0.51, 0.49, 0] 0.02 / 1.00, Z [0.33, 0.33, 0.34] 0.01 / 1.58.
The B-Anxiety letters in the S08 grid are placed for the picture (35 of 100, as in the data), not at their real row
numbers. Exercise pictures show the task, not the answer. The app tiles are analogies.
Uses the mp-*, ml-*, nt-*, rc-*, dg-*, pl-* classes in templates/page.css.
"""

import math

from stats_svg import Svg, app_grid, circ, embed_png, emoji_or_icon, person, ring, term_grid, width  # noqa: F401

W = 1100
OK, NO, BLUE, GOLD = "var(--tag-exercise-dot)", "var(--accent)", "var(--tag-concept-dot)", "var(--tag-example-dot)"

# ================================================================ S01 labels made by people, every day
s = Svg(W, "Everyday places where people label data or must agree: CAPTCHA asks you to click every traffic light (people "
           "label data), chatbot thumbs up or down rate answers (human feedback), three dance judges give three scores "
           "(agreement between raters), critics and fans often disagree (reliability), content moderators follow a "
           "rulebook (guidelines), and nobody agrees whether 4 stars is good (an unclear scale).")
s.bubble("ทุกวันมีคน “ติดป้าย” ข้อมูล และต้องเห็นตรงกัน", "Every day people “label” data, and need to agree")
bottom = app_grid(s, [
    ("🚦", "CAPTCHA", "CAPTCHA", "คลิกทุกภาพที่มีไฟจราจร", "click every traffic light", "คนติดป้ายข้อมูล", "people label data"),
    ("👍", "ปุ่มถูกใจของแชตบอต", "Chatbot 👍 / 👎", "ให้คะแนนแต่ละคำตอบ", "rate each answer", "feedback จากคน", "human feedback"),
    ("🕺", "กรรมการเต้น", "Dance judges", "กรรมการ 3 คน 3 คะแนน", "3 judges, 3 scores", "ความตรงกัน (ICC)", "agreement (ICC)"),
    ("🍅", "นักวิจารณ์กับคนดู", "Critics vs fans", "เห็นไม่ตรงกันบ่อย", "they often disagree", "reliability", "reliability"),
    ("🚩", "ทีมตรวจโพสต์", "Content moderators", "มีคู่มือว่าอะไรผิดกฎ", "a rulebook for posts", "คู่มือ (guideline)", "guidelines"),
    ("⭐", "รีวิว 5 ดาว", "5-star reviews", "4 ดาวคือดีหรือแค่พอใช้", "is 4 stars good or meh?", "สเกลไม่ชัด", "an unclear scale"),
])
s.save("l15-labels-everywhere.svg", bottom + 10)


# ================================================================ S03 four sides of quality
def chipr(x, y, w, label, cls="ml-cell"):
    s.box(x, y, w, 26, cls, 13)
    s.text(x + w / 2, y + 18, label, "mp-c", "middle")


def d_acc(x, y, w, h):
    chipr(x + 20, y + 14, 90, "Anxiety")
    chipr(x + 130, y + 14, 90, "Anxiety", "rc-res")
    s.text(x + 65, y + 66, "label", "mp-s", "middle")
    s.text(x + 175, y + 66, "gold ✓", "ml-ok", "middle")


def d_cons(x, y, w, h):
    for i, n in enumerate("AB"):
        embed_png(s, ("cast-ra-a.png", "cast-ra-b.png")[i], x + 16 + i * 110, y + 4, 36, 54)
        chipr(x + 54 + i * 110, y + 28, 64, "Joy", "ml-cell-b")
        s.text(x + 34 + i * 110, y + 80, n, "mp-c", "middle")


def d_comp(x, y, w, h):
    for r in range(3):
        for c in range(4):
            blank = (r, c) == (1, 2)
            s.box(x + 30 + c * 46, y + 10 + r * 22, 42, 18, "pl-chip-del" if blank else "ml-cell", 3)
    s.text(x + 30 + 2 * 46 + 21, y + 10 + 22 + 14, "?", "mp-acc", "middle")


def d_valid(x, y, w, h):
    for r in (30, 20, 10):
        ring(s, x + 70, y + 42, r, "mp-axis")
    circ(s, x + 70, y + 42, 4, NO)
    s.text(x + 116, y + 34, "fake news?", "mp-c")
    s.text(x + 116, y + 58, "≠ angry words", "mp-acc")


s = Svg(W, "Four sides of data quality: accuracy (the label matches a gold standard), consistency or reliability (the same "
           "letter gets the same label from anyone, this lesson's focus), completeness (no blank labels), validity (the "
           "label measures the concept you mean, e.g. fake news rather than angry language).")
term_grid(s, [
    (("ความถูกต้อง", "Accuracy"), d_acc, "ตรงกับ gold standard", "matches a gold standard", "เช่น ผู้เชี่ยวชาญ", "e.g. an expert's label"),
    (("ความสม่ำเสมอ", "Consistency"), d_cons, "ใครติดก็ได้ป้ายเดียวกัน", "same label from anyone", "← บทนี้เน้นข้อนี้", "← this lesson's focus"),
    (("ความครบ", "Completeness"), d_comp, "ไม่มีป้ายที่หายไป", "no missing labels", "ทุกช่องมีค่า", "every cell filled"),
    (("ความตรงตามที่วัด", "Validity"), d_valid, "วัดแนวคิดที่ตั้งใจจริง", "measures what you mean", "ไม่ใช่ทางลัดที่เห็นง่าย", "not an easy shortcut"),
])
s.save("l15-quality-four.svg", 212)

# ================================================================ S05 the concept vs the shortcut (story only)
s = Svg(W, "A label should measure the concept you mean, which is hard to see (deep, under the surface). Annotators may "
           "fall back on a cue that is easy to see on the surface. The exercise asks which surface cue each task's label "
           "might be measuring instead.")
s.bubble("ป้ายของเรากำลังวัดสิ่งที่ตั้งใจ หรือ “ทางลัด” ที่เห็นง่าย", "Does the label measure what you mean, or an easy “shortcut”?")
s.raw('<path d="M0 170 Q275 156 550 170 T1100 170 L1100 400 L0 400 Z" style="fill:var(--tag-concept-bg)"/>')
s.raw('<path d="M460 170 L520 92 L590 104 L640 170 Z" style="fill:var(--card);stroke:var(--card-border);stroke-width:2"/>')
s.raw('<path d="M400 172 L700 172 L780 300 L640 380 L470 372 L330 290 Z" style="fill:var(--card);stroke:var(--tag-concept-dot);stroke-width:2;opacity:.9"/>')
s.both(550, 150, "สิ่งที่เห็นง่าย = ?", "easy to see = ?", "mp-acc", "middle")
s.both(555, 270, "แนวคิดที่ตั้งใจวัด", "the concept you mean", "mp-t", "middle")
s.both(555, 300, "(เห็นยาก อยู่ใต้ผิว)", "(hard to see, under the surface)", "mp-s", "middle")
embed_png(s, "cast-ra-a.png", 190, 74, 60, 80)
s.raw('<path d="M240 120 L470 130" class="nt-arrow" stroke-dasharray="6 5"/>')
s.both(258, 96, "ผู้ติดป้ายมองแค่ผิว?", "the annotator looks at the surface?", "mp-s")
s.both(860, 230, "A สุภาพ · B โรแมนติก · C กังวล", "A polite · B Romantic · C anxious", "mp-c", "middle")
s.both(860, 256, "แต่ละงาน ทางลัดคืออะไร", "what is each task's shortcut?", "mp-s", "middle")
s.save("l15-shortcut.svg", 400)

# ================================================================ S07 what a good guideline has (empty checklist)
PARTS = [("นิยามที่ชัดและวัดได้", "clear, measurable definitions"), ("ตัวอย่างบวกและลบ", "positive and negative examples"),
         ("กฎกรณีขอบ", "edge-case rules"), ("กฎเมื่อป้ายชนกัน", "a rule when labels clash"), ("ป้าย “ไม่แน่ใจ”", "an Unsure code")]
s = Svg(W, "What to look for in a guideline: clear, measurable definitions; positive and negative examples; edge-case rules; "
           "a rule for when labels clash; an Unsure code. The exercise checks guidelines A, B and C against these five.")
s.bubble("คู่มือที่ดีมีครบ 5 ส่วนไหม", "Does the guideline have all 5 parts?")
s.box(320, 70, 460, 300, "ml-cell", 16)
s.fill(470, 60, 160, 26, "var(--ink-2)", 8)
for i, (th, en) in enumerate(PARTS):
    y = 116 + i * 50
    s.box(350, y, 28, 28, "ml-cell", 6)
    s.both(394, y + 21, th, en, "mp-t")
for k, n in enumerate("ABC"):
    s.box(840, 120 + k * 76, 200, 56, "nt-band-a", 12)
    s.both(940, 154 + k * 76, f"คู่มือ {n}: ?", f"guideline {n}: ?", "mp-t", "middle")
emoji_or_icon(s, "📋", 150, 222, 110)
s.save("l15-guide-checklist.svg", 382)

# ================================================================ S08 the lazy annotator
s = Svg(W, "Why percent agreement is not enough. 100 letters: research assistant B labels 35 of them Anxiety (red). A lazy "
           "annotator answers 'not anxious' for every letter without reading. They still agree on the 65 letters B called "
           "not anxious: 65% agreement for free.")
s.bubble("คนขี้เกียจตอบ “ไม่กังวล” ทุกฉบับ ตรงกับ B กี่ %", "A lazy annotator says “not anxious” to all: how often do they agree with B?")
s.panel(10, 70, 560, 300, "ml-cell", "จดหมาย 100 ฉบับ: ป้ายของ B", "100 letters: B's labels", 1)
anx = {(r * 10 + c) for r in range(10) for c in range(10) if (r * 7 + c * 3) % 20 < 7}
while len(anx) > 35:
    anx.pop()
for i in range(100):
    r, c = divmod(i, 10)
    s.fill(40 + c * 30, 110 + r * 24, 24, 18, NO if i in anx else "var(--card-border)", 3)
s.fill(360, 140, 18, 18, NO, 3)
s.both(386, 154, f"Anxiety {len(anx)}", f"Anxiety {len(anx)}", "mp-c")
s.fill(360, 172, 18, 18, "var(--card-border)", 3)
s.both(386, 186, f"ไม่กังวล {100 - len(anx)}", f"not anxious {100 - len(anx)}", "mp-c")
s.panel(590, 70, 500, 300, "ml-cell", "คนขี้เกียจไม่อ่านเลย", "The lazy annotator reads nothing", 2)
embed_png(s, "cast-yawn.png", 612, 104, 76, 104)
s.box(690, 140, 180, 34, "nt-bubble", 17)
s.both(780, 162, "“ไม่กังวล” ×100", "“not anxious” ×100", "mp-c", "middle")
s.box(620, 220, 440, 120, "rc-con", 12)
s.both(840, 252, "ตรงกับ B", "agrees with B", "mp-s", "middle")
s.text(840, 294, "65% ✗", "mp-big", "middle")
s.both(840, 324, "ทั้งที่ไม่ได้อ่านสักฉบับ", "without reading a single letter", "mp-s", "middle")
s.save("l15-lazy-annotator.svg", 380)

# ================================================================ S10 the kappa scale
BANDS = [("< 0", "แย่กว่าบังเอิญ", "Poor", -0.2, 0.0), ("0–0.20", "เล็กน้อย", "Slight", 0.0, 0.2), ("0.21–0.40", "พอใช้", "Fair", 0.2, 0.4),
         ("0.41–0.60", "ปานกลาง", "Moderate", 0.4, 0.6), ("0.61–0.80", "ค่อนข้างมาก", "Substantial", 0.6, 0.8),
         ("0.81–1", "เกือบสมบูรณ์", "Almost perfect", 0.8, 1.0)]
s = Svg(W, "The Landis & Koch kappa scale: below 0 poor, 0 to 0.20 slight, 0.21 to 0.40 fair, 0.41 to 0.60 moderate, 0.61 "
           "to 0.80 substantial, 0.81 to 1 almost perfect. The letters' pilot 1: Anxiety or not, kappa 0.35 (fair); four "
           "emotions, kappa 0.415 (moderate). A guide, not a law.")
s.bubble("kappa 0.35 หรือ 0.415 ถือว่าดีไหม", "Is a kappa of 0.35 or 0.415 good?")
XL, XR = 60, 1040
X = lambda v: XL + (v + 0.2) / 1.2 * (XR - XL)
shades = ["var(--accent)", "var(--accent-tint)", "var(--tag-example-bg)", "var(--tag-concept-bg)", "var(--tag-exercise-bg)", OK]
for (rng_, th, en, a, b), col in zip(BANDS, shades):
    s.fill(X(a), 150, X(b) - X(a) - 3, 60, col, 6)
    s.both((X(a) + X(b)) / 2, 236, th, en, "mp-c", "middle")
    s.text((X(a) + X(b)) / 2, 260, rng_, "mp-s", "middle")
for v, th, en, up in ((0.35, "Anxiety หรือไม่: 0.35", "Anxiety or not: 0.35", True), (0.415, "4 อารมณ์: 0.415", "4 emotions: 0.415", False)):
    s.raw(f'<path d="M{X(v):g} {140 if up else 220} L{X(v):g} {120 if up else 300}" class="mp-curve"/>')
    circ(s, X(v), 140 if up else 220, 6, "var(--ink)")
    s.both(X(v), 110 if up else 320, th, en, "mp-acc", "middle")
s.both(XR, 320, "ใช้เป็นแนวทาง ไม่ใช่กฎตายตัว", "a guide, not a law", "mp-s", "end")
s.save("l15-kappa-scale.svg", 340)

# ================================================================ S11 the two table shapes
s = Svg(W, "Fleiss' kappa and Krippendorff's alpha take the same labels in different table shapes. Fleiss: one row per "
           "letter, one column per label, each cell counts how many raters chose that label (every letter needs the same "
           "number of raters). Krippendorff: one row per rater, one column per letter, a blank where a rater skipped a "
           "letter is allowed. On pilot 1's emotions they give 0.373 and 0.375.")
s.bubble("ผู้ติดป้าย 3 คน วัดความตรงกันพร้อมกันอย่างไร", "Three raters: how do you measure agreement all at once?")
s.panel(10, 70, 530, 300, "ml-cell", "Fleiss' kappa: จดหมาย × ป้าย", "Fleiss' kappa: letters × labels", 1)
cols = ["Neutral", "Joy", "Anxiety", "Sadness"]
rows = [[2, 0, 1, 0], [3, 0, 0, 0], [0, 0, 2, 1], [1, 1, 1, 0]]
for c, name in enumerate(cols):
    s.text(160 + c * 90, 130, name, "mp-s", "middle")
for r, row in enumerate(rows):
    s.both(40, 162 + r * 40, f"จดหมาย {r + 1}", f"letter {r + 1}", "mp-c")
    for c, v in enumerate(row):
        s.box(124 + c * 90, 142 + r * 40, 72, 30, "ml-cell-b" if v else "ml-cell", 6)
        s.text(160 + c * 90, 163 + r * 40, str(v), "mp-n", "middle")
s.both(30, 346, "ช่อง = มีผู้ติดป้ายกี่คนเลือกป้ายนั้น", "cell = how many raters chose it", "mp-s")
s.text(520, 346, "κ = 0.373", "mp-acc", "end")
s.panel(560, 70, 530, 300, "ml-cell", "Krippendorff's α: ผู้ติดป้าย × จดหมาย", "Krippendorff's α: raters × letters", 2)
grid = [["Neu", "Neu", "Anx", "Joy"], ["Neu", "Neu", "Anx", "Neu"], ["Anx", "Neu", "Sad", None]]
for c in range(4):
    s.both(700 + c * 92, 130, f"ฉบับ {c + 1}", f"letter {c + 1}", "mp-s", "middle")
for r, row in enumerate(grid):
    s.text(600, 163 + r * 44, "ABC"[r], "mp-n")
    for c, v in enumerate(row):
        s.box(664 + c * 92, 142 + r * 44, 74, 30, "pl-chip-del" if v is None else "ml-cell", 6)
        s.text(701 + c * 92, 163 + r * 44, v or "–", "mp-c" if v else "mp-acc", "middle")
s.both(580, 346, "เว้นว่างได้ (ไม่ได้ติดป้าย)", "blanks allowed (skipped)", "mp-s")
s.text(1070, 346, "α = 0.375", "mp-acc", "end")
s.save("l15-two-shapes.svg", 380)

# ================================================================ S13 which measure
s = Svg(W, "Choosing an agreement measure from two questions, how many raters and what kind of label: 2 raters with "
           "categories → Cohen's kappa (letters A vs B: 0.415); 3 or more raters, same number per item, categories → Fleiss' "
           "kappa (0.373); any number, gaps allowed, any kind of label → Krippendorff's alpha (0.375); numbers or scales → "
           "ICC (formality: 0.418).")
s.bubble("ข้อมูลของเราควรใช้ตัววัดไหน", "Which measure fits your data?")
s.box(40, 180, 200, 60, "ml-model", 14)
s.both(140, 206, "ผู้ติดป้ายกี่คน", "how many raters?", "ml-model-text", "middle")
s.both(140, 228, "ป้ายแบบไหน", "what kind of label?", "ml-model-sub", "middle")
LEAVES = [("2 คน · ป้ายกลุ่ม", "2 raters · categories", "Cohen's κ", "0.415"),
          ("3+ คน ครบทุกชิ้น · กลุ่ม", "3+, every item complete", "Fleiss' κ", "0.373"),
          ("กี่คนก็ได้ ขาดได้ · ป้ายแบบใดก็ได้", "any number, gaps OK · any label", "Krippendorff's α", "0.375"),
          ("ป้ายเป็นตัวเลข / สเกล", "numbers or scales", "ICC", "0.418")]
for i, (cth, cen, m, v) in enumerate(LEAVES):
    y = 74 + i * 76
    s.arrow(244, 210, 330, y + 26)
    s.box(334, y, 360, 52, "nt-band-a", 12)
    s.both(352, y + 32, cth, cen, "mp-t")
    s.arrow(698, y + 26, 736, y + 26)
    s.box(740, y, 200, 52, "rc-res", 12)
    s.text(840, y + 33, m, "mp-t", "middle")
    s.text(1060, y + 33, v, "mp-acc", "end")
s.both(1060, 384, "ค่าจาก pilot 1", "pilot 1 values", "mp-s", "end")
s.save("l15-which-measure.svg", 396)

# ================================================================ S15 labeling functions vote
VOTES = [("SAD", None, None, "NOT", "SAD"), (None, "SAD", None, "NOT", "SAD"), (None, None, "NOT", None, "NOT"),
         (None, None, "NOT", "NOT", "NOT"), ("SAD", None, None, None, "SAD"), (None, None, None, "NOT", "NOT"),
         ("SAD", "SAD", None, "NOT", "SAD"), ("SAD", None, "NOT", "NOT", "SAD")]
RULES = [("lf_cry", "4 / 4"), ("lf_heartbroken", "2 / 2"), ("lf_happy", "2 / 3"), ("lf_has_I", "2 / 6")]
s = Svg(W, "Four labeling functions vote on 8 sentences: SAD, NOT or abstain (blank), next to the true (gold) label. A vote "
           "matching gold is solid, a wrong vote is outlined in red. Right out of votes cast: lf_cry 4 of 4, lf_heartbroken "
           "2 of 2, lf_happy 2 of 3, lf_has_I 2 of 6 (a bad rule that clashes with the others).")
s.bubble("ให้กฎ 4 ข้อโหวตป้ายของประโยค ป้ายที่ได้ดีแค่ไหน", "Let 4 rules vote on each sentence: how good are the labels?")
CX = [250, 420, 590, 760, 950]
for c, (name, _) in enumerate(RULES):
    s.text(CX[c], 92, name, "mp-mono", "middle")
s.text(CX[4], 92, "gold", "mp-mono", "middle")
for r, row in enumerate(VOTES):
    y = 104 + r * 32
    s.both(40, y + 20, f"ประโยค {r + 1}", f"sentence {r + 1}", "mp-c")
    gold = row[4]
    for c, v in enumerate(row):
        if v is None:
            s.text(CX[c], y + 20, "·", "mp-s", "middle")
            continue
        if c == 4:
            cls = "rc-ctx"
        else:
            cls = "ml-cell-b" if v == gold else "rc-con"
        s.box(CX[c] - 40, y + 3, 80, 24, cls, 12)
        s.text(CX[c], y + 20, v, "mp-c", "middle")
s.line(30, 366, 1070, 366, "mp-axis")
s.both(40, 392, "ถูก / โหวต", "right / votes", "mp-c")
for c, (name, r) in enumerate(RULES):
    bad = name == "lf_has_I"
    s.text(CX[c], 392, r + (" ✗" if bad else ""), "ml-neg" if bad else "mp-n", "middle")
s.save("l15-lf-votes.svg", 404)

# ================================================================ S16 LLM prompts
s = Svg(W, "Making an LLM follow your guideline. Zero-shot ('Label the sentiment') turns 'It wasn't bad.' into positive, "
           "against the guideline. A prompt with the guideline, few-shot examples, step-by-step reasoning and a JSON format "
           "returns neutral with its reason: a negated negative is weak praise.")
s.bubble("ให้ LLM ติดป้ายตามคู่มือของเรา ไม่ใช่ตามความเข้าใจของมันเอง", "Make the LLM label by your guideline, not its own idea")
for k, (tth, ten, chips, ans_th, ans_en, ok) in enumerate((
        ("Zero-shot", "Zero-shot", [("บอกงานอย่างเดียว", "just the task")], "positive ✗", "positive ✗", False),
        ("Prompt ที่มีคู่มือ", "A guided prompt", [("คู่มือ", "guideline"), ("ตัวอย่าง", "few-shot"), ("คิดทีละขั้น", "step by step"),
                                                  ("JSON", "JSON")], "neutral ✓", "neutral ✓", True))):
    y = 80 + k * 150
    s.box(10, y, 1080, 130, "rc-res" if ok else "rc-con", 14)
    s.both(30, y + 34, tth, ten, "mp-t")
    cx = 30
    for cth, cen in chips:
        w = max(width(cth, 16), width(cen, 16)) + 28
        s.box(cx, y + 52, w, 30, "ml-cell", 15)
        s.both(cx + w / 2, y + 73, cth, cen, "mp-chip", "middle")
        cx += w + 10
    s.box(560, y + 40, 210, 44, "ml-cell", 10)
    s.text(665, y + 68, "“It wasn't bad.”", "mp-c", "middle")
    s.arrow(774, y + 62, 810, y + 62)
    emoji_or_icon(s, "🤖", 840, y + 54, 50)
    s.both(870, y + 70, ans_th, ans_en, "ml-ok" if ok else "ml-neg")
    if ok:
        s.both(560, y + 112, "เหตุผล: ปฏิเสธคำลบ = ชมแบบจืด", "reason: a negated negative is weak praise", "mp-s")
s.save("l15-llm-prompt.svg", 380)

# ================================================================ S17 active learning
s = Svg(W, "Active learning. Left: the loop: 1 people label 100 letters, 2 train a model, 3 the model scores the other 900 "
           "letters, 4 the 100 it is least sure about go back to people; repeat with 200, 300 labels. Right: three letters' "
           "probabilities for SAD, NEUTRAL, JOY: X 0.99 / 0.005 / 0.005 (margin 0.99 − 0.005 = 0.98, sure), Y 0.51 / 0.49 / 0 "
           "(margin 0.02), Z 0.33 / 0.33 / 0.34 (margin 0.01, the least sure): send Z first, skip X.")
s.bubble("ควรส่งจดหมายฉบับไหนให้คนอ่าน", "Which letter should a person read?")
s.panel(10, 70, 470, 360, "ml-cell", "วงจร active learning", "The active-learning loop", 1)
LOOP = [(30, 126, "① คนติดป้าย 100 ฉบับ", "① people label 100"),
        (262, 126, "② ฝึกโมเดล", "② train a model"),
        (262, 296, "③ โมเดลทาย 900 ฉบับที่เหลือ", "③ model scores the other 900"),
        (30, 296, "④ ส่ง 100 ฉบับที่ไม่แน่ใจที่สุด", "④ send the 100 least sure")]
BW, BH = 198, 56
for (x, y, th, en) in LOOP:
    s.box(x, y, BW, BH, "nt-band-a", 12)
    s.both(x + BW / 2, y + 34, th, en, "mp-chip", "middle")
s.arrow(30 + BW + 4, 154, 262 - 4, 154)                    # 1 → 2
s.arrow(262 + BW / 2, 126 + BH + 4, 262 + BW / 2, 296 - 4)  # 2 → 3
s.arrow(262 - 4, 324, 30 + BW + 4, 324)                    # 3 → 4
s.arrow(30 + BW / 2, 296 - 4, 30 + BW / 2, 126 + BH + 4)    # 4 → 1
s.both(245, 232, "วนซ้ำ", "repeat", "pl-label", "middle")
s.both(245, 258, "ป้าย 100 → 200 → 300 …", "labels 100 → 200 → 300 …", "mp-s", "middle")
s.both(30, 408, "คนอ่านเฉพาะฉบับที่โมเดลยังไม่รู้ ไม่เสียเวลากับฉบับที่ง่าย", "People only read what the model can't decide yet", "mp-s")
s.panel(500, 70, 590, 360, "ml-cell", "โมเดลมั่นใจแค่ไหน", "How sure is the model?", 2)
LET = [("X", [0.99, 0.005, 0.005], "0.99 − 0.005 = 0.98", ("มั่นใจ ไม่ต้องส่ง", "sure: skip")),
       ("Y", [0.51, 0.49, 0.0], "0.51 − 0.49 = 0.02", ("ลังเล SAD/NEUTRAL", "torn SAD/NEUTRAL")),
       ("Z", [0.33, 0.33, 0.34], "0.34 − 0.33 = 0.01", ("ไม่รู้เลย ส่งก่อน ✓", "no idea: send first ✓"))]
COLS = (BLUE, "var(--muted)", OK)
for c, (lab, col) in enumerate(zip(("SAD", "NEUTRAL", "JOY"), COLS)):
    s.fill(530 + c * 120, 126, 14, 14, col, 3)
    s.text(550 + c * 120, 138, lab, "mp-s")
s.both(900, 138, "margin = อันดับ 1 − อันดับ 2", "margin = top − second", "mp-s")
for r, (n, ps, calc, (vth, ven)) in enumerate(LET):
    y = 158 + r * 80
    s.both(526, y + 26, f"ฉบับ {n}", f"letter {n}", "mp-t")
    x = 610
    for p, col in zip(ps, COLS):
        if p >= 0.05:
            s.fill(x, y + 6, p * 270, 30, col, 3)
            s.raw(f'<text x="{x + p * 135:.1f}" y="{y + 27}" text-anchor="middle" style="fill:#fff;font:600 14px var(--font-head)">{p:g}</text>')
        x += p * 270
    pick = n == "Z"
    s.text(900, y + 20, calc, "mp-acc" if pick else "mp-c")
    s.both(900, y + 44, vth, ven, "ml-ok" if pick else "mp-s")
s.both(526, 408, "margin ยิ่งน้อย โมเดลยิ่งไม่แน่ใจ → คนควรอ่านฉบับนั้น", "The smaller the margin, the less sure the model → a person should read it", "mp-s")
s.save("l15-active-loop.svg", 440)

# ================================================================ S18 compare the three ways to scale up
SCALE = [
    ("weak supervision", "weak supervision", "📜",
     ("คนทำ: เขียนกฎสั้น ๆ 10–50 ข้อ", "People: write 10–50 rules"),
     [("ป้ายครบ 20,000 ฉบับในไม่กี่นาที", "labels all 20,000 in minutes"),
      ("กฎอ่านออก อธิบายและแก้ได้", "rules are readable and fixable")],
     [("ต้องมีผู้เชี่ยวชาญเขียนกฎ", "needs an expert to write rules"),
      ("พลาดสิ่งที่ไม่มีคำบ่งชี้ เช่น ประชด", "misses what has no keyword")],
     ("เหมาะ: ข้อมูลมาก มีคำบ่งชี้ชัด", "Best: big data, clear cue words")),
    ("LLM ติดป้ายรอบแรก", "LLM first pass", "🤖",
     ("คนทำ: ใส่คู่มือใน prompt แล้วตรวจแก้", "People: prompt it, then review"),
     [("เข้าใจบริบท ประชด การตีความ", "gets context, irony, nuance"),
      ("เร็วกว่าเริ่มจากศูนย์ 5–10 เท่า", "5–10× faster than from scratch")],
     [("ผิดได้อย่างมั่นใจ ต้องสุ่มตรวจ", "can be confidently wrong"),
      ("เสียเงิน และส่งข้อมูลออกนอก", "costs money, data leaves you")],
     ("เหมาะ: งานตีความที่เขียนกฎไม่ได้", "Best: interpretive tasks")),
    ("active learning", "active learning", "🙋",
     ("คนทำ: ติดป้ายเฉพาะฉบับที่โมเดลถาม", "People: label only what it asks"),
     [("ใช้เวลาคนคุ้มที่สุด", "spends people's time best"),
      ("ทุกป้ายมาจากคน คุณภาพสูง", "every label is human")],
     [("ต้องวนฝึก-ทาย-ส่ง หลายรอบ", "needs many rounds"),
      ("ชุดที่ได้เอียงไปทางฉบับยาก", "labels lean to hard cases")],
     ("เหมาะ: มีคนติดป้าย แต่เวลาน้อย", "Best: few annotator hours")),
]
s = Svg(W, "Comparing the three ways to scale up labelling. Weak supervision: people write 10–50 rules; it labels all 20,000 "
           "letters in minutes and the rules can be read and fixed, but it needs an expert and misses anything without a "
           "cue word, such as irony. LLM first pass: people put the guideline in a prompt and review; it understands "
           "context and is 5–10 times faster than starting from scratch, but it can be confidently wrong, costs money and "
           "sends the data away. Active learning: people label only the letters the model asks about; it spends their "
           "time best and every label is human, but it needs many rounds and the labelled set leans to hard cases. All "
           "three need a human gold set to check quality, and they can be combined.")
s.bubble("ขยายการติดป้ายสามวิธี ได้อะไร เสียอะไร", "Three ways to scale up: what do you gain, what do you lose?")
PW = 352
for i, (tth, ten, icon_, (dth, den), pros, cons, (bth, ben)) in enumerate(SCALE):
    x0 = 10 + i * (PW + 12)
    s.panel(x0, 70, PW, 440, "ml-cell", tth, ten, i + 1)
    emoji_or_icon(s, icon_, x0 + PW / 2, 150, 52)
    s.both(x0 + 20, 206, dth, den, "pl-note")
    s.box(x0 + 14, 222, PW - 28, 104, "nt-band-a", 10)
    s.both(x0 + 28, 248, "ข้อดี", "Benefits", "mp-s")
    for k, (th, en) in enumerate(pros):
        s.both(x0 + 28, 278 + k * 30, "✓ " + th, "✓ " + en, "pl-note")
    s.box(x0 + 14, 336, PW - 28, 104, "sw-warn-box", 10)
    s.both(x0 + 28, 362, "ข้อเสีย", "Drawbacks", "mp-s")
    for k, (th, en) in enumerate(cons):
        s.both(x0 + 28, 392 + k * 30, "✗ " + th, "✗ " + en, "pl-note")
    s.both(x0 + 20, 478, bth, ben, "pl-label")
    for txt in [dth, den, bth, ben] + [t for pair in pros + cons for t in pair]:
        if width(txt, 17) >= PW - 40:
            print('LONG', round(width(txt, 17)), txt)
s.both(10, 540, "ทั้งสามวิธีต้องมีชุด gold ที่คนติดป้ายไว้เพื่อตรวจคุณภาพ และใช้ร่วมกันได้: LLM ติดรอบแรก แล้ว active learning ส่งฉบับที่ไม่แน่ใจให้คน",
       "All three need a human gold set to check quality, and they combine: an LLM labels first, then active learning sends the unsure ones to people", "mp-s")
s.save("l15-scale-compare.svg", 556)


# ================================================================ S19 takeaways
def emoji(icon):
    return lambda x, y, w, h: emoji_or_icon(s, icon, x + w / 2, y + h / 2, 66)


s = Svg(W, "Six takeaways: garbage in, garbage out; the guideline is your contract; measure inter-rater reliability instead "
           "of guessing; scale up with a gold set; repeat the quality loop; reliable is not the same as valid.")
bottom = term_grid(s, [
    ("GIGO", emoji("🗑️"), "ป้ายแย่ = ข้อสรุปแย่", "bad labels, bad findings", "โมเดลเก่งแค่ไหนก็แก้ไม่ได้", "no model can fix them"),
    (("คู่มือ = สัญญา", "Guidelines = contract"), emoji("📜"), "นิยาม ตัวอย่าง กรณีขอบ", "definitions, examples,", "และป้ายสำรอง", "edge cases, fallbacks"),
    (("วัด IRR อย่าเดา", "Measure IRR"), emoji("📏"), "κ, α หรือ ICC", "κ, α or ICC", "ค่าต่ำ = แก้คู่มือ", "low = fix the guide"),
    (("ขยายอย่างฉลาด", "Scale smart"), emoji("📈"), "ใช้ชุด gold คุมงาน", "a gold set steers", "weak sup., LLM, active", "weak sup., LLMs, active"),
    (("ทำวงจรซ้ำ", "Repeat the loop"), emoji("🔁"), "แก้ → วัด → ขยาย", "refine → measure →", "→ ตรวจ → แก้", "scale → audit → refine"),
    ("Reliable ≠ valid", emoji("🎯"), "ตรงกันอาจวัดผิดเรื่อง", "agreeing ≠ measuring", "ตรวจแนวคิดเสมอ", "the right concept"),
], cols=3, tw=352)
s.save("l15-takeaways.svg", bottom + 10)
