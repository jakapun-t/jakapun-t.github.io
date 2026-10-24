"""Draws the pictures of lesson 15 of the international NLP course (sequence tagging, NER and relation
extraction): SVG, inlined into the page; ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/nlp_l15_figures.py courses/nlp/images

Every number is real (computed in course/.venv on 2026-10-19):
- POS taggers trained on NLTK's Penn Treebank sample (first 3,500 sentences), tested on the other 414
  (10,329 tokens; 953 of them never seen in training): default NN 14.5%, unigram 87.9%, unigram + suffix
  rules 92.5%, HMM (Lidstone 0.1) 89.9%, CRF (sklearn-crfsuite, word/suffix/neighbour features) 96.2%.
- "They refuse to permit us to obtain the refuse permit .": unigram ... refuse/VBP permit/VB, HMM ... refuse/JJ
  permit/NNS, CRF ... refuse/NN permit/NN (P = 0.615 and 0.965).
- The HMM example is the slide corpus (Mary Jane can see Will / Spot will see Mary / Will Jane spot Mary /
  Mary will pat Spot): "Will can spot Mary" → N M V N with P = 1/3888 ≈ 0.000257 (81 paths, 2 non-zero).
- NER: dslim/bert-base-NER (PER, ORG, LOC, MISC) on the slide's airline announcement; seqeval for span F1.

Uses the nt-*, pl-*, sw-*, ml-* and dg-* classes in templates/page.css.
"""

import math
import os
import sys
import unicodedata
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp/images"
FS = 19


def width(s, fs=FS):
    return sum(0 if unicodedata.category(c) == "Mn" else fs * (1.1 if ord(c) > 0x1F000 else 0.58) for c in s)


class Svg:
    def __init__(self, w, title):
        self.w, self.title, self.out = w, title, []

    def both(self, x, y, th, en, cls, anchor="start"):
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="th">{escape(th)}</text>')
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="en" lang="en">{escape(en)}</text>')

    def text(self, x, y, s, cls, anchor="start"):
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}">{escape(s)}</text>')

    def box(self, x, y, w, h, cls, rx=12):
        self.out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}"/>')

    def line(self, x1, y1, x2, y2, dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="pl-line"{dash}/>')

    def arrow(self, x1, y1, x2, y2, dashed=False):
        self.line(x1, y1, x2, y2, dashed)
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 10 * math.cos(a - 0.55), y2 - 10 * math.sin(a - 0.55))
        p2 = (x2 - 10 * math.cos(a + 0.55), y2 - 10 * math.sin(a + 0.55))
        self.out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2:g} {y2:g} L{p2[0]:.1f} {p2[1]:.1f}" class="pl-line"/>')

    def raw(self, s):
        self.out.append(s)

    def chip(self, x, y, t, cls="ml-cell", tcls="pl-text", minw=0, h=36):
        w = max(width(t) + 22, minw)
        self.box(x, y, w, h, cls, 8)
        self.text(x + w / 2, y + h / 2 + 6, t, tcls, "middle")
        return w

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


def tagged(s, x, y, pairs, gap=10, tagcls=None, hi=()):
    """A row of word chips with their tag chips underneath; returns the end x. hi = indexes to highlight."""
    for i, (w, t) in enumerate(pairs):
        cw = max(width(w), width(t, 17)) + 22
        s.box(x, y, cw, 36, "sw-chip-warn" if i in hi else "ml-cell", 8)
        s.text(x + cw / 2, y + 24, w, "pl-text", "middle")
        if t:
            s.line(x + cw / 2, y + 38, x + cw / 2, y + 50)
            cls = (tagcls[i] if tagcls else None) or "nt-bubble"
            s.box(x, y + 52, cw, 30, cls, 8)
            s.text(x + cw / 2, y + 73, t, "dg-code", "middle")
        x += cw + gap
    return x


ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def ic(s, name, cx, cy, size):
    """A generated icon (assets/icon-<name>.png) centred on (cx, cy)."""
    import base64
    data = base64.b64encode(open(os.path.join(ASSETS, "icon-" + name + ".png"), "rb").read()).decode()
    s.raw(f'<image x="{cx - size / 2:g}" y="{cy - size / 2:g}" width="{size:g}" height="{size:g}" '
          f'preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>')


def bubble(s, W, text, y=8, w=None):
    w = w or width(text) + 60
    s.box(W / 2 - w / 2, y, w, 46, "nt-bubble", 23)
    s.text(W / 2, y + 30, text, "pl-text", "middle")


W = 1180

# ---------------------------------------------------------------- 1. hook: an announcement as text vs as a table
s = Svg(W, "From text to a table. The airline announcement is three sentences of text: a computer cannot sort or count what it says. "
           "Information extraction turns it into a table: United Airlines, parent UAL Corp., raised fares by $6 per round trip; "
           "American Airlines, parent AMR Corp., matched the move, spokesman Tim Wagner. Three steps get there, drawn below on "
           "sentence 2: 1 tag each word (American/NNP Airlines/NNPS, a/DT unit/NN of/IN AMR/NNP Corp./NNP ...); 2 find the "
           "names: American Airlines and AMR Corp. are ORG, Tim Wagner is PER; 3 link them: American Airlines part_of AMR "
           "Corp., Tim Wagner works_for American Airlines, which fill the Parent and Contact columns.")
s.box(20, 20, 470, 420, "sw-warn-box", 14)
s.both(40, 52, "✗ ที่มี: ข้อความยาว", "✗ What we have: text", "pl-label")
LINES = ["Citing high fuel prices, United", "Airlines said Friday it has", "increased fares by $6 per round", "trip on flights to some cities ...",
         "American Airlines, a unit of AMR", "Corp., immediately matched the", "move, spokesman Tim Wagner said.", "United, a unit of UAL Corp., said",
         "the increase took effect Thursday ..."]
for k, ln in enumerate(LINES):
    s.text(40, 92 + k * 30, ln, "dg-code")
s.both(40, 380, "คอมพิวเตอร์เรียง นับ หรือค้นข้อเท็จจริงในนี้ไม่ได้", "a computer can't sort, count or query", "ml-neg")
s.both(40, 406, "ในข้อความได้", "the facts in here", "ml-neg")
s.arrow(496, 230, 540, 230)
s.box(546, 20, 614, 420, "nt-band-a", 14)
s.both(566, 52, "✓ ที่อยากได้: ตาราง", "✓ What we want: a table", "pl-label")
COLS = [("สายการบิน", "Airline", 566), ("บริษัทแม่", "Parent", 762), ("เหตุการณ์", "Event", 872), ("ผู้แถลง", "Contact", 990)]
for th, en, x in COLS:
    s.both(x, 92, th, en, "pl-note")
ROWS = [("United Airlines", "UAL Corp.", "fares +$6", "–"), ("American Airlines", "AMR Corp.", "matched", "Tim Wagner")]
for r, row in enumerate(ROWS):
    y = 108 + r * 56
    s.box(560, y, 586, 46, "ml-cell", 8)
    for (th, en, x), v in zip(COLS, row):
        s.text(x + 6, y + 29, v, "pl-text")
s.both(566, 268, "แล้วจึงเรียง นับ และค้นได้ เช่น", "then it can be sorted, counted and queried,", "pl-text")
s.both(566, 294, "“สายการบินไหนขึ้นราคาวันศุกร์”", "e.g. “which airlines raised fares on Friday?”", "pl-text")
s.both(566, 350, "3 ขั้นที่ทำให้ได้ตารางนี้ ดูด้านล่าง ↓", "Three steps get there, below ↓", "pl-label")
s.both(566, 380, "ติดป้ายทุกคำ → หาชื่อ → โยงชื่อ", "tag each word → find the names → link them", "ml-ok")
# the three steps, drawn on sentence 2 (POS: NLTK's perceptron tagger; names: dslim/bert-base-NER, as in the lesson)
SENT = [("American", "NNP"), ("Airlines", "NNPS"), (",", ","), ("a", "DT"), ("unit", "NN"), ("of", "IN"), ("AMR", "NNP"),
        ("Corp.", "NNP"), (",", ","), ("immediately", "RB"), ("matched", "VBD"), ("the", "DT"), ("move", "NN"), (",", ","),
        ("spokesman", "NN"), ("Tim", "NNP"), ("Wagner", "NNP"), ("said", "VBD"), (".", ".")]
Y = 468
s.box(20, Y, 1140, 314, "ml-cell", 14)
s.both(40, Y + 30, "3 ขั้น บนประโยคที่ 2 ของประกาศ", "The three steps, on sentence 2 of the announcement", "pl-label")
X0, CH = 176, 8.6
xs, x = [], X0
for wd, tag in SENT:
    w = max(len(wd), len(tag)) * CH + 10
    xs.append((x, w))
    x += w + 4
ROWL = [("คำ", "words", 64), ("1 · ติดป้าย", "1 · tag", 100), ("2 · หาชื่อ", "2 · names", 150), ("3 · โยงชื่อ", "3 · links", 214)]
for th, en, dy in ROWL:
    s.both(36, Y + dy, th, en, "pl-label" if dy > 64 else "pl-note")
ENTS = [(0, 1, "ORG", "dg-hl-col"), (6, 7, "ORG", "dg-hl-col"), (15, 16, "PER", "ml-cell-b")]
for a_, b_, lab, cls in ENTS:  # the names, highlighted in the sentence itself
    s.box(xs[a_][0], Y + 45, xs[b_][0] + xs[b_][1] - xs[a_][0], 28, cls, 6)
for (wd, tag), (x, w) in zip(SENT, xs):
    s.text(x + w / 2, Y + 64, wd, "dg-code", "middle")
    s.raw(f'<text x="{x + w / 2:g}" y="{Y + 100}" class="pl-note" text-anchor="middle" style="font-size:15px">{escape(tag)}</text>')
centers = []
for a_, b_, lab, cls in ENTS:
    x1 = xs[a_][0]; x2 = xs[b_][0] + xs[b_][1]
    s.box(x1, Y + 128, x2 - x1, 32, cls, 8)
    s.text((x1 + x2) / 2, Y + 150, lab, "pl-label", "middle")
    centers.append((x1 + x2) / 2)
def arc(xa, xb, depth, label_th, label_en, label_y=None):
    y0 = Y + 162
    s.raw(f'<path d="M{xa:.1f} {y0} Q{(xa + xb) / 2:.1f} {y0 + depth} {xb:.1f} {y0}" class="pl-line"/>')
    hx = xb + (6 if xb < xa else -6)
    ang = math.atan2(y0 - (y0 + 14), xb - hx)
    p1 = (xb - 10 * math.cos(ang - 0.55), y0 - 10 * math.sin(ang - 0.55))
    p2 = (xb - 10 * math.cos(ang + 0.55), y0 - 10 * math.sin(ang + 0.55))
    s.raw(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{xb:.1f} {y0} L{p2[0]:.1f} {p2[1]:.1f}" class="pl-line"/>')
    s.both((xa + xb) / 2, label_y if label_y else y0 + depth / 2 + 22, label_th, label_en, "pl-label", "middle")
arc(centers[0], centers[1], 36, "part_of", "part_of", Y + 150)
arc(centers[2], centers[0], 124, "works_for", "works_for")
s.box(36, Y + 262, 1108, 40, "nt-out", 8)
s.both(52, Y + 288, "→ ตาราง: (American Airlines, part_of, AMR Corp.) = Parent · (Tim Wagner, works_for, American Airlines) = Contact",
       "→ the table: (American Airlines, part_of, AMR Corp.) = Parent · (Tim Wagner, works_for, American Airlines) = Contact", "hk-desc")
s.save("l15-hook.svg", Y + 328)


# ---------------------------------------------------------------- 2. lesson map
def tw(t, fs):
    return sum(0 if unicodedata.category(c) == "Mn" else fs * 0.58 for c in t)


ROWS = [
    ("1 ปัญหา", "1 The problem", "ข้อความเข้า ตารางออก", "Text in, a table out", "ข้อเท็จจริงจมอยู่ในประโยค ✗", "facts buried in sentences ✗"),
    ("2 Sequence tagging", "2 Sequence tagging", "ป้ายหนึ่งอันต่อหนึ่งคำ", "One label per word", "11 คำ → 11 ป้าย ✓", "11 words → 11 labels ✓"),
    ("3 POS tagging", "3 POS tagging", "ชนิดของคำตามบริบท", "Word classes in context", "“the refuse permit”: นามหรือกริยา? ✗", "“the refuse permit”: noun or verb? ✗"),
    ("4 โมเดลเชิงสถิติ", "4 Statistical taggers", "นับ → HMM → CRF", "Count → HMM → CRF", "CRF: refuse, permit = NN ✓ (96.2%)", "CRF: refuse, permit = NN ✓ (96.2%)"),
    ("5 โมเดล neural", "5 Neural taggers", "BiLSTM, BERT อ่านทั้งประโยค", "BiLSTM, BERT read it all", "≈ 97% ✓", "≈ 97% ✓"),
    ("6 NER", "6 Named entities", "หาชื่อด้วยป้าย BIO", "Find names with BIO tags", "American Airlines = ORG ✓", "American Airlines = ORG ✓"),
    ("7 LLM และการวัดผล", "7 LLMs and evaluation", "ขอ JSON ตรวจ แล้วให้คะแนน", "Ask for JSON, check it, score it", "ชนิดไหนก็ได้ ไม่ต้องเทรน ✓", "any types, no training ✓"),
    ("8 Relation extraction", "8 Relation extraction", "โยงชื่อเป็นคู่", "Link the names in pairs", "(American Airlines, part_of, AMR Corp.) ✓", "(American Airlines, part_of, AMR Corp.) ✓"),
]
s = Svg(W, "Lesson map: one airline announcement followed through eight parts: the problem (facts buried in text), sequence tagging "
           "(one label per word), part-of-speech tagging (is 'refuse' a noun or a verb?), statistical taggers (a CRF tags 'the refuse "
           "permit' as nouns, 96.2% accuracy), neural taggers (about 97%), named entities with BIO tags, LLMs and evaluation, and "
           "relation extraction (American Airlines part_of AMR Corp.).")
s.box(W / 2 - 300, 10, 600, 50, "ml-cell", 25)
s.text(W / 2, 42, "What does this airline announcement say, as a table?", "pl-text", "middle")
s.both(20, 92, "แต่ละส่วนเพิ่มอะไร", "What each part adds", "nt-head")
s.both(760, 92, "ข้อความของเราได้อะไร", "What our text gets", "nt-head")
y = 106
for tth, ten, dth, den, rth, ren in ROWS:
    bad = "✗" in ren
    s.box(20, y, W - 40, 46, "sw-warn-box" if bad else "ml-cell", 12)
    for lang, t, d in (("th", tth, dth), ("en", ten, den)):
        attr = ' lang="en"' if lang == "en" else ""
        s.raw(f'<g data-only="{lang}"{attr}>')
        s.raw(f'<text x="40" y="{y + 30}" class="nt-task">{escape(t)}</text>')
        s.raw(f'<text x="{40 + tw(t, 19) + 18:g}" y="{y + 30}" class="hk-desc">{escape(d)}</text>')
        s.raw("</g>")
    s.both(760, y + 30, rth, ren, "ml-neg" if bad else "ml-ok")
    y += 54
s.save("l15-map-lesson.svg", y + 2)


# ---------------------------------------------------------------- 3. one label per sentence vs one label per word
s = Svg(W, "Text classification gives one label to the whole sentence, for example 'travel'. Sequence tagging gives one label to "
           "every word: I will book a flight → PRP MD VB DT NN, five words and five tags. The tag of 'book' depends on its "
           "neighbour 'will': after 'will', 'book' is a verb.")
bubble(s, W, "I will book a flight")
s.box(20, 70, 360, 260, "ml-cell", 14)
s.both(40, 102, "Text classification", "Text classification", "pl-label")
s.both(40, 128, "ป้ายเดียวทั้งประโยค", "one label for the whole sentence", "pl-note")
s.box(40, 150, 320, 40, "ml-cell", 8)
s.text(56, 176, "I will book a flight", "pl-text")
s.arrow(200, 196, 200, 228)
s.box(140, 234, 120, 38, "nt-bubble", 10)
s.text(200, 259, "travel", "dg-code", "middle")
s.both(40, 310, "1 ประโยค → 1 ป้าย", "1 sentence → 1 label", "pl-note")
s.box(400, 70, 760, 260, "nt-band-a", 14)
s.both(420, 102, "Sequence tagging", "Sequence tagging", "pl-label")
s.both(420, 128, "ป้ายหนึ่งอันต่อหนึ่งคำ", "one label for every word", "pl-note")
tagged(s, 440, 160, [("I", "PRP"), ("will", "MD"), ("book", "VB"), ("a", "DT"), ("flight", "NN")], gap=16, hi=(2,))
s.both(420, 284, "5 คำ → 5 ป้าย: ยาวเท่ากันเสมอ", "5 words → 5 tags: always the same length", "ml-ok")
s.both(420, 312, "ป้ายของ book ขึ้นกับคำข้าง ๆ: หลัง will จึงเป็นกริยา (VB)", "book's tag depends on its neighbour: after will, a verb (VB)", "pl-text")
s.save("l15-seqtag.svg", 346)

# ---------------------------------------------------------------- 4. five tagging tasks
s = Svg(W, "Five tasks that are all sequence tagging. Part-of-speech: I will book a flight → PRP MD VB DT NN. Named entities with BIO: "
           "spokesman Tim Wagner said → O B-PER I-PER O. Chunking: They refuse to permit us → B-NP B-VP I-VP I-VP B-NP. Grammar "
           "correction: He eat food → KEEP, REPLACE with eats, KEEP. Tokenization of Thai, which has no spaces: each character "
           "of ฉันกินข้าว gets B (a word begins) or I (inside): B I I B I I B I I I, so the words are ฉัน | กิน | ข้าว.")
PANELS = [
    ("1 · Part-of-speech (POS)", "ชนิดของคำ", "word class", [("I", "PRP"), ("will", "MD"), ("book", "VB"), ("a", "DT"), ("flight", "NN")], ()),
    ("2 · Named entities (BIO)", "ชื่อเฉพาะ: B = เริ่ม I = ต่อ O = นอก", "names: B = begin, I = inside, O = outside",
     [("spokesman", "O"), ("Tim", "B-PER"), ("Wagner", "I-PER"), ("said", "O")], (1, 2)),
    ("3 · Chunking", "วลี: NP นาม VP กริยา", "phrases: NP noun, VP verb", [("They", "B-NP"), ("refuse", "B-VP"), ("to", "I-VP"), ("permit", "I-VP"), ("us", "B-NP")], ()),
    ("4 · Grammar correction", "แก้ไวยากรณ์ทีละคำ", "fix grammar word by word", [("He", "KEEP"), ("eat", "→ eats"), ("food", "KEEP")], (1,)),
]
for k, (title, sth, sen, pairs, hi) in enumerate(PANELS):
    x0, y0 = 20 + (k % 2) * 584, 20 + (k // 2) * 200
    s.box(x0, y0, 572, 188, "ml-cell", 14)
    s.text(x0 + 18, y0 + 32, title, "pl-label")
    s.both(x0 + 18, y0 + 58, sth, sen, "pl-note")
    tagged(s, x0 + 18, y0 + 76, pairs, gap=10, hi=hi)
# 5: tokenization as tagging: Thai has no spaces, so each character gets B (a word begins here) or I (inside a word)
s.box(20, 420, 1156, 150, "ml-cell", 14)
s.text(38, 452, "5 · Tokenization (word segmentation)", "pl-label")
s.both(38, 478, "ภาษาไทยไม่เว้นวรรค: ติดป้ายทุกตัวอักษร B = เริ่มคำ I = อยู่ในคำ", "Thai has no spaces: tag every character, B = a word begins, I = inside a word", "pl-note")
CHARS = [("ฉ", "B"), ("◌ั", "I"), ("น", "I"), ("ก", "B"), ("◌ิ", "I"), ("น", "I"), ("ข", "B"), ("◌้", "I"), ("า", "I"), ("ว", "I")]
end = tagged(s, 38, 486, CHARS, gap=8, hi=(0, 3, 6))
s.arrow(end + 6, 504, end + 40, 504)
s.box(end + 46, 486, 300, 36, "nt-out", 8)
s.both(end + 62, 510, "ฉัน | กิน | ข้าว", "ฉัน | กิน | ข้าว  (I eat rice)", "pl-text")
s.both(end + 46, 556, "ตัดคำตรงที่มี B", "cut before every B", "pl-note")
s.both(20, 598, "ทุกงาน: input n หน่วย → output n ป้าย และป้ายขึ้นกับป้ายข้าง ๆ (เช่น I-PER ต้องตามหลัง B-PER)",
       "Every task: n units in → n labels out, and labels depend on their neighbours (I-PER must follow B-PER)", "ml-ok")
s.save("l15-tasks.svg", 614)

# ---------------------------------------------------------------- 5. why POS tagging is hard: three kinds of ambiguity
s = Svg(W, "Why POS tagging is hard. Word ambiguity: book is a noun in 'I read a book' but a verb in 'I will book a flight'. "
           "Structure ambiguity: 'Visiting relatives can be boring' means either the act of visiting is boring or relatives who "
           "visit are boring. Domain ambiguity: 'shot' is a noun in sport (a great shot) and a verb in medicine (the nurse shot me).")
P3 = [("1 · คำเดียว หลายชนิด", "1 · One word, many classes"), ("2 · โครงสร้างกำกวม", "2 · Ambiguous structure"), ("3 · ต่างสาขา ต่างความหมาย", "3 · Domain changes it")]
for k, (th, en) in enumerate(P3):
    x0 = 20 + k * 384
    s.box(x0, 20, 372, 330, "ml-cell", 14)
    s.both(x0 + 18, 52, th, en, "pl-label")
x0 = 38
tagged(s, x0, 76, [("read", "VBD"), ("a", "DT"), ("book", "NN")], hi=(2,))
tagged(s, x0, 186, [("will", "MD"), ("book", "VB"), ("a", "DT")], hi=(1,))
s.both(x0, 310, "คำเดียวกัน: book = นาม / กริยา", "same word: book = noun / verb", "ml-neg")
s.both(x0, 334, "ต้องดูคำข้าง ๆ (a / will)", "the neighbour decides (a / will)", "pl-note")
x0 = 422
s.text(x0, 96, "Visiting relatives can be boring.", "dg-code")
s.box(x0, 116, 336, 74, "nt-bubble", 10)
s.both(x0 + 12, 142, "visiting = นาม (การไปเยี่ยม)", "visiting = noun (the act)", "pl-text")
s.both(x0 + 12, 170, "→ การไปเยี่ยมญาติน่าเบื่อ", "→ going to visit them is boring", "pl-note")
s.box(x0, 202, 336, 74, "nt-bubble", 10)
s.both(x0 + 12, 228, "visiting = คุณศัพท์", "visiting = adjective", "pl-text")
s.both(x0 + 12, 256, "→ ญาติที่มาเยี่ยมน่าเบื่อ", "→ relatives who visit are boring", "pl-note")
s.both(x0, 310, "ลองคิด: Time flies like an arrow", "Try: Time flies like an arrow", "ml-neg")
s.both(x0, 334, "มีกี่ความหมาย?", "how many meanings?", "pl-note")
x0 = 806
s.both(x0, 96, "กีฬา", "Sport", "pl-note")
tagged(s, x0, 104, [("great", "JJ"), ("shot", "NN")], hi=(1,))
s.both(x0, 218, "การแพทย์", "Medicine", "pl-note")
tagged(s, x0, 226, [("nurse", "NN"), ("shot", "VBD")], hi=(1,))
s.save("l15-pos-hard.svg", 366)

# ---------------------------------------------------------------- 6. tagsets: the same sentence in Penn Treebank and Universal POS
SENT = [("They", "PRP", "PRON"), ("refuse", "VBP", "VERB"), ("to", "TO", "PART"), ("permit", "VB", "VERB"), ("us", "PRP", "PRON"),
        ("to", "TO", "PART"), ("obtain", "VB", "VERB"), ("the", "DT", "DET"), ("refuse", "NN", "NOUN"), ("permit", "NN", "NOUN")]
OPEN = {"VERB", "NOUN", "ADJ", "ADV"}
s = Svg(W, "One sentence, two tagsets. Penn Treebank (about 45 tags) splits verbs by form: VBP for 'refuse' after They, VB after to. "
           "Universal POS (17 tags) calls both VERB. Open-class words (nouns, verbs, adjectives, adverbs) are highlighted; closed-class "
           "words (pronouns, determiners, particles) are a small fixed set. Below, one panel per tagset: Penn Treebank's six verb tags "
           "(VB to refuse, VBP they refuse, VBZ she refuses, VBD refused, VBN has refused, VBG refusing) all become UPOS VERB; the 17 "
           "Universal POS tags, with the five used in the sentence in blue; ORCHID (about 47 Thai tags) on two sentences tagged by "
           "PyThaiNLP: ฉัน/PPRS กิน/VACT ข้าว/NCMN (I eat rice) and แมว/NCMN 2/DCNM ตัว/CNIT (two cats), where CNIT is the classifier.")
x = 20 + width("Universal POS") + 18  # rows start right of the longest label
s.both(20, 56, "คำ", "word", "pl-note")
s.both(20, 110, "Penn Treebank", "Penn Treebank", "pl-note")
s.both(20, 162, "Universal POS", "Universal POS", "pl-note")
for w_, ptb, upos in SENT:
    cw = max(width(w_), width(ptb, 17), width(upos, 17)) + 18
    op = upos in OPEN
    s.box(x, 32, cw, 36, "sw-chip-warn" if op else "ml-cell", 8)
    s.text(x + cw / 2, 56, w_, "pl-text", "middle")
    s.box(x, 88, cw, 32, "nt-bubble", 8)
    s.text(x + cw / 2, 110, ptb, "dg-code", "middle")
    s.box(x, 140, cw, 32, "nt-band-a" if op else "ml-cell", 8)
    s.text(x + cw / 2, 162, upos, "dg-code", "middle")
    x += cw + 8
assert x < W - 12, x
# three panels: what each tagset looks like
P = 196
for k in range(3):
    s.box(20 + k * 384, P, 372, 284, "ml-cell", 12)
# 1 · Penn Treebank: six tags just for verbs, all folded into one UPOS VERB
x0 = 20
s.text(x0 + 16, P + 30, "Penn Treebank (PTB)", "pl-label")
s.both(x0 + 16, P + 54, "≈ 45 ป้าย · ภาษาอังกฤษ · กริยามี 6 ป้าย", "≈ 45 tags · English · 6 just for verbs", "pl-note")
VERBS = [("VB", "to refuse"), ("VBP", "they refuse"), ("VBZ", "she refuses"),
         ("VBD", "refused"), ("VBN", "has refused"), ("VBG", "refusing")]
for n, (t, ex) in enumerate(VERBS):
    cx, cy = x0 + 16 + (n // 3) * 178, P + 72 + (n % 3) * 40
    s.box(cx, cy, 56, 30, "nt-bubble", 8)
    s.text(cx + 28, cy + 21, t, "dg-code", "middle")
    s.text(cx + 64, cy + 21, ex, "pl-note")
s.both(x0 + 16, P + 228, "UPOS รวมทั้ง 6 ป้ายเป็น", "UPOS folds all 6 into", "pl-note")
vx = x0 + 16 + max(width("UPOS รวมทั้ง 6 ป้ายเป็น", 16), width("UPOS folds all 6 into", 16)) + 8
s.box(vx, P + 208, 64, 30, "nt-band-a", 8)
s.text(vx + 32, P + 229, "VERB", "dg-code", "middle")
s.both(x0 + 16, P + 262, "ละเอียด: แยกรูปของกริยาได้", "fine-grained: keeps the verb's form", "pl-note")
# 2 · Universal POS: all 17 tags, the ones in our sentence in blue
x0 = 404
s.text(x0 + 16, P + 30, "Universal POS (UD)", "pl-label")
s.both(x0 + 16, P + 54, "17 ป้าย · ใช้ชุดเดียวกันทุกภาษา", "17 tags · the same for every language", "pl-note")
UPOS = ["ADJ", "ADP", "ADV", "AUX", "CCONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN",
        "PUNCT", "SCONJ", "SYM", "VERB", "X"]
USED = {"PRON", "VERB", "PART", "DET", "NOUN"}
for n, t in enumerate(UPOS):
    cx, cy = x0 + 16 + (n % 6) * 56, P + 72 + (n // 6) * 38
    s.box(cx, cy, 51, 28, "nt-band-a" if t in USED else "nt-bubble", 7)
    s.text(cx + 25.5, cy + 19, t, "dg-code", "middle")
s.box(x0 + 16, P + 196, 18, 18, "nt-band-a", 4)
s.both(x0 + 42, P + 211, "= มีในประโยคของเรา", "= used in our sentence", "pl-note")
s.both(x0 + 16, P + 242, "ทั้งไทย จีน อาหรับ ใช้ 17 ป้ายนี้", "Thai, Chinese, Arabic … all use these 17,", "pl-note")
s.both(x0 + 16, P + 266, "จึงเทียบ tagger ข้ามภาษาได้", "so taggers compare across languages", "pl-note")
# 3 · ORCHID: Thai tags, real output of PyThaiNLP pos_tag(corpus="orchid")
x0 = 788
s.both(x0 + 16, P + 30, "ORCHID (ไทย)", "ORCHID (Thai)", "pl-label")
s.both(x0 + 16, P + 54, "≈ 47 ป้าย · ภาษาไทย", "≈ 47 tags · Thai", "pl-note")
e1 = tagged(s, x0 + 16, P + 66, [("ฉัน", "PPRS"), ("กิน", "VACT"), ("ข้าว", "NCMN")], gap=8)
s.both(e1 + 6, P + 104, "ฉันกินข้าว", "I eat rice", "pl-note")
e2 = tagged(s, x0 + 16, P + 160, [("แมว", "NCMN"), ("2", "DCNM"), ("ตัว", "CNIT")], gap=8, hi=(2,))
s.both(e2 + 6, P + 198, "แมว 2 ตัว", "two cats", "pl-note")
s.both(x0 + 16, P + 266, "CNIT = ลักษณนาม ภาษาอังกฤษไม่มีป้ายนี้", "CNIT = classifier, a tag English lacks", "pl-note")
L = P + 304
s.box(20, L, 18, 18, "sw-chip-warn", 4)
s.both(46, L + 15, "open class: นาม กริยา คุณศัพท์ กริยาวิเศษณ์ มีคำใหม่เพิ่มได้เรื่อย ๆ", "open class: nouns, verbs, adjectives, adverbs; new words keep arriving", "pl-text")
s.box(20, L + 32, 18, 18, "ml-cell", 4)
s.both(46, L + 47, "closed class: คำไวยากรณ์ชุดเล็ก ๆ (the, to, they) แทบไม่เปลี่ยน", "closed class: a small fixed set of function words (the, to, they)", "pl-text")
s.save("l15-tagsets.svg", L + 62)

# ---------------------------------------------------------------- 7. unigram tagger: majority vote per word
s = Svg(W, "A unigram tagger gives each word the tag it had most often in training, ignoring its neighbours. In the Penn Treebank "
           "sample, book was NN 4 times, VB once and NNP once, so it is always NN: right in 'I read a book', wrong in 'I will book a "
           "flight'. Unknown words fall back to rules by ending (-ing VBG, -ed VBD, -ly RB): accuracy goes from 14.5% (always NN) to "
           "87.9% (unigram) to 92.5% (unigram plus rules).")
s.box(20, 20, 560, 420, "sw-warn-box", 14)
s.both(40, 52, "✗ นับแล้วเลือกป้ายที่เจอบ่อยสุด", "✗ Count, then take the most common tag", "pl-label")
s.both(40, 78, "จำนวนครั้งใน training (Penn Treebank 3,500 ประโยค)", "counts in training (Penn Treebank, 3,500 sentences)", "pl-note")
for k, (w_, counts) in enumerate([("book", [("NN", 4), ("VB", 1), ("NNP", 1)]), ("like", [("IN", 44), ("VB", 7), ("VBP", 4)])]):
    y0 = 104 + k * 120
    s.text(40, y0 + 22, w_, "pl-label")
    mx = max(c for _, c in counts)
    for j, (tg, c) in enumerate(counts):
        y = y0 + j * 30
        s.text(150, y + 20, tg, "dg-code", "end")
        s.box(160, y + 4, 260 * c / mx, 22, "ml-bar-top" if j == 0 else "ml-bar", 4)
        s.text(160 + 260 * c / mx + 8, y + 21, str(c), "pl-note")
tagged(s, 40, 344, [("will", "MD"), ("book", "NN ✗"), ("a", "DT")], hi=(1,))
s.both(300, 372, "ต้องเป็น VB: unigram", "should be VB: a unigram", "ml-neg")
s.both(300, 398, "ไม่ดูคำว่า will เลย", "never looks at “will”", "ml-neg")
s.box(600, 20, 560, 420, "nt-band-a", 14)
s.both(620, 52, "✓ คำที่ไม่เคยเห็น: ดูจากท้ายคำ", "✓ Unseen words: guess from the ending", "pl-label")
RULES = [("-ing", "VBG", "running"), ("-ed", "VBD", "matched"), ("-ly", "RB", "immediately"), ("123", "CD", "2019"), ("Capital", "NNP", "Wagner")]
for k, (suf, tg, ex) in enumerate(RULES):
    y = 76 + k * 40
    s.box(620, y, 120, 32, "ml-cell", 8); s.text(680, y + 22, suf, "dg-code", "middle")
    s.arrow(746, y + 16, 772, y + 16)
    s.box(778, y, 80, 32, "nt-bubble", 8); s.text(818, y + 22, tg, "dg-code", "middle")
    s.text(874, y + 22, ex, "pl-note")
s.both(620, 302, "ความแม่นบนประโยคทดสอบ 414 ประโยค", "accuracy on 414 test sentences", "pl-note")
for k, (lab, v) in enumerate([("always NN", 14.5), ("unigram", 87.9), ("+ rules", 92.5)]):
    y = 314 + k * 34
    s.text(730, y + 20, lab, "pl-text", "end")
    s.box(740, y + 4, 300 * v / 100, 24, "ml-bar-top" if k == 2 else "ml-bar", 4)
    s.text(740 + 300 * v / 100 + 8, y + 22, f"{v}%", "pl-label")
s.save("l15-unigram.svg", 456)

# ---------------------------------------------------------------- 8a. HMM set-up: tagged training data, the question, the assumptions, other uses
TRAIN = [[("Mary", "N"), ("Jane", "N"), ("can", "M"), ("see", "V"), ("Will", "N")],
         [("Spot", "N"), ("will", "M"), ("see", "V"), ("Mary", "N")],
         [("Will", "M"), ("Jane", "N"), ("spot", "V"), ("Mary", "N")],
         [("Mary", "N"), ("will", "M"), ("pat", "V"), ("Spot", "N")]]
s = Svg(W, "The HMM problem set-up. Given: four training sentences that people already tagged with N (noun), M (modal: can, will) "
           "and V (verb): Mary Jane can see Will (N N M V N), Spot will see Mary (N M V N), Will Jane spot Mary (M N V N), Mary will "
           "pat Spot (N M V N). Wanted: the hidden tags of the new sentence Will can spot Mary, whose words we see. Two Markov "
           "assumptions: a tag depends only on the tag before it, and a word depends only on its own tag. The same recipe works "
           "whenever a hidden sequence produces a seen one: speech recognition, weather from ice creams eaten, a fitness watch "
           "guessing activity from steps, and Thai word segmentation (B/I per character).")
s.both(20, 24, "ที่มี: ประโยคเทรน 4 ประโยค ที่คนติดป้ายไว้แล้ว", "Given: 4 training sentences, already tagged by people", "pl-label")
for k, sent in enumerate(TRAIN):
    x0, y0 = 20 + (k % 2) * 590, 40 + (k // 2) * 92
    s.text(x0 + 6, y0 + 24, str(k + 1), "pl-note")
    tagged(s, x0 + 28, y0, sent, gap=8)
B = 232
s.box(20, B, 560, 146, "ml-cell", 12)
s.both(40, B + 28, "อยากรู้: ป้ายของประโยคใหม่", "Wanted: the tags of a new sentence", "pl-label")
s.both(40, B + 68, "เห็น: คำ", "seen: words", "pl-note")
s.both(40, B + 120, "ซ่อน: ป้าย", "hidden: tags", "pl-note")
e = tagged(s, 150, B + 44, [("Will", "?"), ("can", "?"), ("spot", "?"), ("Mary", "?")], gap=8,
           tagcls=["sw-chip-warn"] * 4)
for k, (th, en) in enumerate([("N = นาม", "N = noun"), ("M = can, will", "M = can, will"), ("V = กริยา", "V = verb")]):
    s.both(e + 12, B + 66 + k * 26, th, en, "pl-note")
s.box(600, B, 560, 146, "nt-band-a", 12)
s.both(620, B + 28, "สมมติฐาน 2 ข้อ (Markov)", "Two assumptions (Markov)", "pl-label")
s.both(620, B + 62, "① ป้ายขึ้นกับป้ายก่อนหน้าเท่านั้น", "① a tag depends only on the tag before it", "pl-text")
s.both(646, B + 86, "เช่น หลัง M มาเป็น V บ่อยแค่ไหน → transition", "e.g. after M, how often is it V? → transition", "pl-note")
s.both(620, B + 114, "② คำขึ้นกับป้ายของตัวเองเท่านั้น", "② a word depends only on its own tag", "pl-text")
s.both(646, B + 138, "เช่น ป้าย M เป็นคำว่า can บ่อยแค่ไหน → emission", "e.g. how often is an M the word can? → emission", "pl-note")
T = B + 168
s.both(20, T + 14, "สูตรเดียวกันใช้ได้ทุกที่ที่ลำดับที่ซ่อนอยู่สร้างลำดับที่เราเห็น", "The same recipe works wherever a hidden sequence makes a seen one", "pl-label")
USES = [("microphone", "รู้จำเสียงพูด", "Speech recognition", "ซ่อน: หน่วยเสียง", "hidden: speech sounds", "เห็น: คลื่นเสียง", "seen: the audio"),
        ("weather", "บันทึกอากาศ", "Weather diary", "ซ่อน: วันร้อน / หนาว", "hidden: hot or cold day", "เห็น: ไอศกรีมที่กินต่อวัน", "seen: ice creams eaten"),
        ("stopwatch", "นาฬิกาออกกำลังกาย", "Fitness watch", "ซ่อน: เดิน วิ่ง นอน", "hidden: walk, run, sleep", "เห็น: ก้าวต่อนาที", "seen: steps per minute"),
        ("scissors", "ตัดคำภาษาไทย", "Thai word cut", "ซ่อน: B / I ของแต่ละตัวอักษร", "hidden: B or I per letter", "เห็น: ตัวอักษร", "seen: the characters")]
for k, (icon, tth, ten, hth, hen, sth, sen) in enumerate(USES):
    x0 = 20 + k * 288
    s.box(x0, T + 28, 276, 112, "ml-cell", 12)
    ic(s, icon, x0 + 34, T + 58, 40)
    s.both(x0 + 62, T + 64, tth, ten, "pl-label")
    s.both(x0 + 16, T + 100, hth, hen, "pl-note")
    s.both(x0 + 16, T + 126, sth, sen, "pl-note")
s.save("l15-hmm-setup.svg", T + 152)

# ---------------------------------------------------------------- 8a2. the HMM equation: why there are two parts to count
s = Svg(W, "The HMM equation. The probability of a tag sequence with its words is the product, over every word i, of two parts: "
           "the transition P(t_i | t_i-1), how likely this tag is after the previous one (assumption 1, counted in step 1 as table A), "
           "and the emission P(w_i | t_i), how likely this word is given its tag (assumption 2, counted in step 2 as table B). "
           "On Will can spot Mary tagged N M V N it reads P(N|start) P(Will|N) P(M|N) P(can|M) P(V|M) P(spot|V) P(N|V) P(Mary|N) P(end|N): "
           "9 factors, all read from the two tables.")
FE = 21
parts = [("P(ป้าย, คำ)  =  ∏ᵢ", "P(tags, words)  =  ∏ᵢ", None), ("P(tᵢ | tᵢ₋₁)", "P(tᵢ | tᵢ₋₁)", "nt-band-a"),
         ("×", "×", None), ("P(wᵢ | tᵢ)", "P(wᵢ | tᵢ)", "sw-chip-warn")]
widths = [max(width(th, FE), width(en, FE)) + (36 if cls else 16) for th, en, cls in parts]
x = W / 2 - 150 - sum(widths) / 2
centres = []
for (th, en, cls), w_ in zip(parts, widths):
    if cls:
        s.box(x, 14, w_, 48, cls, 10)
    s.both(x + w_ / 2, 46, th, en, "nt-band-title", "middle")
    centres.append(x + w_ / 2)
    x += w_
s.both(x + 24, 34, "∏ = คูณกันทุกคำ i", "∏ = multiply over", "pl-note")
s.both(x + 24, 64, "ในประโยค", "every word i", "pl-note")
# the two parts, each tied to an assumption and to a counting step
PANELS = [(20, "nt-band-a", centres[1], "Transition  P(tᵢ | tᵢ₋₁)", "Transition  P(tᵢ | tᵢ₋₁)",
           "ป้ายนี้มาหลังป้ายก่อนหน้าบ่อยแค่ไหน", "how likely is this tag after the previous tag?",
           "สมมติฐาน ①: ดูแค่ป้ายก่อนหน้า", "assumption ①: only the tag before matters",
           "→ ขั้น 1 นับเป็นตาราง A", "→ step 1 counts it: table A"),
          (600, "sw-chip-warn", centres[3], "Emission  P(wᵢ | tᵢ)", "Emission  P(wᵢ | tᵢ)",
           "ป้ายนี้เป็นคำนี้บ่อยแค่ไหน", "how likely is this word, given its tag?",
           "สมมติฐาน ②: ดูแค่ป้ายของคำนั้นเอง", "assumption ②: only the word's own tag matters",
           "→ ขั้น 2 นับเป็นตาราง B", "→ step 2 counts it: table B")]
for x0, cls, cx, tth, ten, q_th, q_en, a_th, a_en, st_th, st_en in PANELS:
    s.line(cx, 62, cx, 104)
    s.line(cx, 104, x0 + 280, 104)
    s.arrow(x0 + 280, 104, x0 + 280, 114)
    s.box(x0, 116, 560, 128, cls, 12)
    s.both(x0 + 20, 146, tth, ten, "pl-label")
    s.both(x0 + 20, 174, q_th, q_en, "pl-text")
    s.both(x0 + 20, 202, a_th, a_en, "pl-note")
    s.both(x0 + 20, 230, st_th, st_en, "ml-b")
# the equation read on Will can spot Mary with tags N M V N
s.both(20, 284, "อ่านสูตรบน Will can spot Mary ถ้าป้ายเป็น N M V N", "Read on Will can spot Mary, if its tags are N M V N", "pl-label")
TAGS = ["N", "M", "V", "N"]; WORDS = ["Will", "can", "spot", "Mary"]
TR = ["P(N|start)", "P(M|N)", "P(V|M)", "P(N|V)"]; EM = ["P(Will|N)", "P(can|M)", "P(spot|V)", "P(Mary|N)"]
CY = 360
xs = [270 + k * 200 for k in range(4)]
s.box(20, CY - 25, 90, 50, "ml-cell", 25); s.text(65, CY + 6, "start", "pl-text", "middle")
s.box(1070, CY - 25, 90, 50, "ml-cell", 25); s.text(1115, CY + 6, "end", "pl-text", "middle")
prev = 110
for k, (x, tg, w_) in enumerate(zip(xs, TAGS, WORDS)):
    s.raw(f'<circle cx="{x}" cy="{CY}" r="32" class="nt-bubble"/>')
    s.text(x, CY + 8, tg, "pl-label", "middle")
    s.arrow(prev + 2, CY, x - 34, CY)
    mid = (prev + x - 34) / 2
    s.box(mid - 52, CY - 50, 104, 28, "nt-band-a", 6)
    s.text(mid, CY - 31, TR[k], "dg-code", "middle")
    prev = x + 32
    s.arrow(x, CY + 34, x, CY + 92)
    s.box(x + 8, CY + 46, 104, 28, "sw-chip-warn", 6)
    s.text(x + 60, CY + 65, EM[k], "dg-code", "middle")
    s.box(x - 48, CY + 96, 96, 42, "nt-out", 10)
    s.text(x, CY + 123, w_, "pl-label", "middle")
s.arrow(prev + 2, CY, 1068, CY)
mid = (prev + 1068) / 2
s.box(mid - 52, CY - 50, 104, 28, "nt-band-a", 6); s.text(mid, CY - 31, "P(end|N)", "dg-code", "middle")
s.both(20, CY + 176, "9 ตัวคูณ: transition 5 ตัว (ฟ้า) และ emission 4 ตัว (ส้ม) ทั้งหมดอ่านได้จากตาราง A และ B ที่นับไว้",
       "9 factors: 5 transitions (blue) and 4 emissions (orange), all read from the two counted tables A and B", "pl-text")
s.save("l15-hmm-equation.svg", CY + 194)

# ---------------------------------------------------------------- 8b. HMM steps 1-2: count transitions and emissions
s = Svg(W, "Steps 1 and 2 of an HMM: counting. Step 1, transitions: add start and end to each tagged training sentence "
           "(start N N M V N end, start N M V N end, start M N V N end, start N M V N end) and count which tag follows N: "
           "N 1, M 3, V 1, end 4, 9 in all, so P(N|N) = 1/9, P(M|N) = 3/9, P(V|N) = 1/9, P(end|N) = 4/9. Step 2, emissions: N "
           "appears 9 times as Mary 4, Jane 2, Spot 2, Will 1, so P(Mary|N) = 4/9; M appears 4 times as will 3, can 1; V appears "
           "4 times as see 2, spot 1, pat 1. Each probability is a count divided by how often the first tag appears.")
for x0, cls in [(20, "ml-cell"), (600, "ml-cell")]:
    s.box(x0, 0, 560, 424, cls, 14)
# step 1
s.both(40, 32, "ขั้น 1 · Transition: ป้ายไหนตามมา", "Step 1 · Transition: which tag comes next?", "pl-label")
s.both(40, 60, "เติม start / end แล้วไล่ดูทีละคู่", "add start / end, then read the pairs", "pl-note")
SEQS = [["start", "N", "N", "M", "V", "N", "end"], ["start", "N", "M", "V", "N", "end"],
        ["start", "M", "N", "V", "N", "end"], ["start", "N", "M", "V", "N", "end"]]
for r, seq in enumerate(SEQS):
    x, y = 40, 74 + r * 34
    for k, t in enumerate(seq):
        cw = 54 if t in ("start", "end") else 38
        after_n = k > 0 and seq[k - 1] == "N"
        s.box(x, y, cw, 26, "nt-band-a" if after_n else ("sw-chip-warn" if t == "N" else "nt-bubble"), 6)
        if after_n and t == "N":  # this N both follows an N and starts the next pair
            s.raw(f'<rect x="{x:g}" y="{y:g}" width="{cw:g}" height="26" rx="6" fill="none" stroke="var(--accent)" stroke-width="1.6"/>')
        s.text(x + cw / 2, y + 18, t, "dg-code", "middle")
        x += cw + 6
s.both(40, 236, "หลัง N (ส้ม) มาอะไร (ฟ้า): ทั้งหมด 9 คู่", "what follows N (orange)? the blue boxes: 9 pairs", "pl-note")
for r, (t, c) in enumerate([("N → N", 1), ("N → M", 3), ("N → V", 1), ("N → end", 4)]):
    y = 252 + r * 32
    s.text(40, y + 18, t, "dg-code")
    s.box(140, y, 56 * c, 24, "ml-bar", 4)
    s.text(146 + 56 * c, y + 18, str(c), "pl-note")
    s.text(480, y + 18, f"{c}/9", "pl-label")
s.text(40, 404, "P(M | N) = count(N → M) / count(N) = 3/9", "pl-label")
# step 2
s.both(620, 32, "ขั้น 2 · Emission: ป้ายนี้เป็นคำไหน", "Step 2 · Emission: which word is it?", "pl-label")
s.both(620, 60, "N ปรากฏ 9 ครั้ง เป็นคำเหล่านี้", "N appears 9 times, as these words", "pl-note")
for r, (w_, c) in enumerate([("Mary", 4), ("Jane", 2), ("Spot", 2), ("Will", 1)]):
    y = 74 + r * 32
    s.text(620, y + 18, w_, "pl-text")
    s.box(700, y, 56 * c, 24, "ml-bar-top", 4)
    s.text(706 + 56 * c, y + 18, str(c), "pl-note")
    s.text(1060, y + 18, f"{c}/9", "pl-label")
s.both(620, 222, "M ปรากฏ 4 ครั้ง", "M appears 4 times", "pl-note")
for r, (w_, c) in enumerate([("will", 3), ("can", 1)]):
    y = 234 + r * 32
    s.text(620, y + 18, w_, "pl-text")
    s.box(700, y, 56 * c, 24, "ml-bar-top", 4)
    s.text(706 + 56 * c, y + 18, str(c), "pl-note")
    s.text(1060, y + 18, f"{c}/4", "pl-label")
s.both(620, 328, "V ปรากฏ 4 ครั้ง: see 2 · spot 1 · pat 1", "V appears 4 times: see 2 · spot 1 · pat 1", "pl-note")
s.text(620, 352, "→ 2/4 · 1/4 · 1/4", "pl-label")
s.text(620, 404, "P(Mary | N) = count(N, Mary) / count(N) = 4/9", "pl-label")
s.save("l15-hmm-count.svg", 428)

# ---------------------------------------------------------------- 8. HMM step 3: score two tag sequences (the only two that are not 0)
from fractions import Fraction
import math as _m


def dec(v):
    """A probability with 3 significant digits, always as a plain decimal."""
    d = 2 - _m.floor(_m.log10(v))
    return f"{v:.{max(d, 3)}f}"


s = Svg(W, "Scoring two tag sequences for Will can spot Mary with the counted tables, multiplying left to right: a transition "
           "into each tag (blue), then that tag's emission (orange). A, N M V N (spot as a verb): 3/4, 1/9, 3/9, 1/4, 3/4, 1/4, "
           "4/4, 4/9, 4/9, product 1/3888, about 0.000257. B, N M N N (spot as a noun): the same first four factors, then "
           "M to N 1/4, spot as N 2/9, N to N 1/9, Mary as N 4/9, N to end 4/9, product 1/118098, about 0.0000085. A is about "
           "30 times more likely, so the tagger picks N M V N. The other 79 of the 81 possible sequences score 0.")
s.both(20, 24, "สองลำดับป้ายของ Will can spot Mary คูณจากซ้ายไปขวา: transition (ฟ้า) แล้ว emission (ส้ม)",
       "Two tag sequences for Will can spot Mary, multiplied left to right: transition (blue), then emission (orange)", "pl-label")
PATHS = [("A", "N M V N", "spot = กริยา", "spot = verb",
          [("start→N", "3/4", "t"), ("Will|N", "1/9", "e"), ("N→M", "3/9", "t"), ("can|M", "1/4", "e"), ("M→V", "3/4", "t"),
           ("spot|V", "1/4", "e"), ("V→N", "4/4", "t"), ("Mary|N", "4/9", "e"), ("N→end", "4/9", "t")]),
         ("B", "N M N N", "spot = นาม", "spot = noun",
          [("start→N", "3/4", "t"), ("Will|N", "1/9", "e"), ("N→M", "3/9", "t"), ("can|M", "1/4", "e"), ("M→N", "1/4", "t"),
           ("spot|N", "2/9", "e"), ("N→N", "1/9", "t"), ("Mary|N", "4/9", "e"), ("N→end", "4/9", "t")])]
totals = []
for r, (name, tags, sth, sen, steps) in enumerate(PATHS):
    y = 52 + r * 132
    s.box(20, y, 1140, 118, "ml-cell", 12)
    s.box(28, y + 8, 124, 102, "opt-a-box" if r == 0 else "opt-b-box", 10)
    s.text(40, y + 34, name, "opt-a-text" if r == 0 else "opt-b-text")
    s.text(40, y + 62, tags, "pl-label")
    s.both(40, y + 88, sth, sen, "pl-note")
    run = Fraction(1)
    for k, (lab, f, kind) in enumerate(steps):
        run *= Fraction(f)
        x = 160 + k * 110
        s.box(x, y + 12, 102, 30, "nt-band-a" if kind == "t" else "sw-chip-warn", 8)
        s.text(x + 51, y + 33, "× " + f, "dg-code", "middle")
        if r == 1 and steps[k] != PATHS[0][4][k]:  # where B differs from A
            s.raw(f'<rect x="{x - 3:g}" y="{y + 9:g}" width="108" height="36" rx="10" fill="none" stroke="var(--accent)" '
                  f'stroke-width="2" stroke-dasharray="5 3"/>')
        s.text(x + 51, y + 70, dec(float(run)), "dg-key", "middle")
        s.text(x + 51, y + 98, lab, "pl-note", "middle")
    totals.append(run)
assert totals == [Fraction(1, 3888), Fraction(1, 118098)]
# compare the two scores
Y = 330
s.both(20, Y, "เทียบคะแนน (ขีดประ = ช่องที่ B ต่างจาก A)", "Compare the scores (dashed = where B differs from A)", "pl-label")
s.text(40, Y + 44, "A", "opt-a-text")
s.box(80, Y + 22, 700, 30, "opt-a-bar", 6)
s.text(796, Y + 43, "1/3888 ≈ 0.000257", "pl-label")
s.text(40, Y + 88, "B", "opt-b-text")
s.box(80, Y + 66, max(700 * totals[1] / totals[0], 4), 30, "opt-b-bar", 6)
s.text(110, Y + 87, "1/118098 ≈ 0.0000085", "pl-label")
s.both(20, Y + 132, "A มีโอกาสมากกว่าราว 30 เท่า (118098 / 3888 ≈ 30) tagger จึงเลือก N M V N",
       "A is about 30 times more likely (118098 / 3888 ≈ 30), so the tagger picks N M V N", "ml-ok")
s.both(20, Y + 160, "อีก 79 จาก 81 ลำดับได้ 0 เช่น M M V N เพราะ M → M ไม่เคยเกิดในข้อมูลเทรน",
       "The other 79 of the 81 sequences score 0, e.g. M M V N, because M → M never happens in training", "pl-note")
s.save("l15-hmm.svg", Y + 176)

# ---------------------------------------------------------------- 9. search for the best tags: one setting strip, then brute force / Viterbi / beam
def setting(s):
    """The shared set-up, repeated on each search figure so it reads on its own."""
    s.box(20, 0, 1140, 70, "ml-cell", 12)
    s.both(40, 28, "โจทย์: ติดป้าย Will can spot Mary ด้วย N (นาม) M (modal) V (กริยา)",
           "Setting: tag Will can spot Mary with N (noun), M (modal), V (verb)", "pl-label")
    s.both(40, 56, "คะแนน = transition × emission ที่นับจากประโยคเทรน 4 ประโยค · เป้าหมาย: ลำดับป้ายที่คะแนนสูงสุด",
           "score = transitions × emissions counted from 4 tagged sentences · goal: the highest-scoring tag sequence", "pl-note")


TG = ["N", "M", "V"]
LINE = 'stroke="var(--rule)" stroke-width="1.2"'
# ---- 9a. brute force: the full tree of 81 paths
s = Svg(W, "Brute force: every tag sequence for Will can spot Mary as a tree. Each word can be N, M or V, so the tree splits in 3 at "
           "every word: 3 paths after Will, 9 after can, 27 after spot, 81 after Mary. Only two leaves score above 0: A, N M V N, "
           "1/3888, and B, N M N N, 1/118098. Each path needs 9 multiplications, so 81 × 9 = 729. With 45 tags and 20 words there "
           "are 45^20, about 1.2 × 10^33 paths.")
setting(s)
LV = [100, 160, 226, 292, 352]
LX0, LSTEP = 120, 900 / 80
def leafx(k): return LX0 + k * LSTEP
def nodex(level, idx):  # mean x of the node's 3^(4-level) leaves
    span = 3 ** (4 - level)
    return leafx(idx * span + (span - 1) / 2)
PA, PB = (0, 1, 2, 0), (0, 1, 0, 0)
def on(path, level, idx):
    code = 0
    for t in path[:level]:
        code = code * 3 + t
    return level == 0 or code == idx
for level, (lab_th, lab_en, cnt) in enumerate([("เริ่ม", "start", ""), ("Will", "Will", "3"), ("can", "can", "9"),
                                               ("spot", "spot", "27"), ("Mary", "Mary", "81")]):
    s.both(20, LV[level] + 6, lab_th, lab_en, "pl-label")
    if cnt:
        s.both(1160, LV[level] + 6, cnt + " เส้นทาง", cnt + " paths", "pl-note", "end")
# edges first, coloured paths last so they sit on top
coloured = []
for level in range(1, 5):
    for idx in range(3 ** level):
        x1, y1 = nodex(level - 1, idx // 3), LV[level - 1]
        x2, y2 = nodex(level, idx), LV[level]
        a, b = on(PA, level, idx), on(PB, level, idx)
        if a or b:
            coloured.append((x1, y1, x2, y2, "var(--tag-exercise-dot)" if a else "var(--tag-example-dot)"))
        else:
            s.raw(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" {LINE}/>')
for x1, y1, x2, y2, col in sorted(coloured, key=lambda c: c[4] == "var(--tag-exercise-dot)"):
    s.raw(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" stroke="{col}" stroke-width="4"/>')
R = {0: 18, 1: 15, 2: 13, 3: 10}
for level in range(0, 4):
    for idx in range(3 ** level):
        x = nodex(level, idx)
        hit = on(PA, level, idx) or on(PB, level, idx)
        s.raw(f'<circle cx="{x:g}" cy="{LV[level]}" r="{R[level]}" class="{"sw-chip-warn" if hit else "ml-cell"}"/>')
        if level:
            s.text(x, LV[level] + (6 if level < 3 else 5), TG[idx % 3], "dg-code" if level < 3 else "dg-index", "middle")
for k in range(81):
    hit = k in (15, 9)
    s.raw(f'<circle cx="{leafx(k):g}" cy="{LV[4]}" r="{6 if hit else 3.5}" '
          f'class="{"opt-a-bar" if k == 15 else ("opt-b-bar" if k == 9 else "pl-chip-del")}"/>')
s.text(nodex(0, 0), LV[0] + 6, "", "pl-note")
# the two non-zero leaves
s.line(leafx(15), LV[4] + 8, 330, 392)
s.box(330, 376, 190, 32, "opt-a-box", 8); s.text(425, 398, "A · N M V N = 1/3888", "dg-code", "middle")
s.line(leafx(9), LV[4] + 8, 200, 392)
s.box(64, 376, 200, 32, "opt-b-box", 8); s.text(164, 398, "B · N M N N = 1/118098", "dg-code", "middle")
s.both(540, 398, "อีก 79 ใบได้ 0 (จุดเทา)", "the other 79 leaves score 0 (grey dots)", "pl-note")
s.box(20, 424, 560, 104, "sw-warn-box", 12)
s.both(36, 454, "✗ ประโยคของเรา: 3 ป้าย 4 คำ", "✗ Our sentence: 3 tags, 4 words", "pl-label")
s.text(36, 482, "3 × 3 × 3 × 3 = 3⁴ = 81 paths", "pl-text")
s.both(36, 510, "เส้นละ 9 การคูณ → 81 × 9 = 729 การคูณ", "9 multiplications each → 81 × 9 = 729", "pl-text")
s.box(600, 424, 560, 104, "sw-warn-box", 12)
s.both(616, 454, "✗ ประโยคจริง: 45 ป้าย 20 คำ", "✗ A real sentence: 45 tags, 20 words", "pl-label")
s.text(616, 482, "45²⁰ ≈ 1.2 × 10³³ paths", "ml-neg")
s.both(616, 510, "พันล้านเส้นต่อวินาที ≈ 2.7 ล้านเท่าอายุจักรวาล", "at a billion per second: 2.7 million × the universe's age", "pl-note")
s.save("l15-brute.svg", 540)

# ---- 9b. the three searches at a glance: same mini table, three ways to walk it; panels 2 and 3 animate step by step
s = Svg(W, "Three ways to find the best tags for Will can spot Mary, on the same small table of 4 words by 3 tags. Brute force "
           "walks every path: 81 paths, always the best, too slow for real sentences. Viterbi, like a map app keeping only the "
           "fastest route to each stop, fills the table one word at a time and keeps one best arrow into each box: 36 steps, "
           "always the best, and finds N M V N. Beam search, like a talent show where only the top B go through, keeps the top B "
           "boxes per word: with B = 1 it keeps M after Will and drops N, then every box for can is 0, a dead end; with B = 2 it "
           "finds N M V N. For 45 tags and 20 words: 1.2 × 10^33 paths, 40,500 steps, and 4,500 steps with B = 5.")
# one shared 10-second loop: step k fades in at k × 15 %, everything holds, then resets
CYCLE, STEPS = 10, 5
css = []
for k in range(STEPS):
    p0 = k * 15
    css.append(f"@keyframes l15srch-k{k} {{ 0% {{ opacity: .1 }} {p0}% {{ opacity: .1 }} {p0 + 4}% {{ opacity: 1 }} "
               f"93% {{ opacity: 1 }} 100% {{ opacity: .1 }} }}")
    css.append(f".l15srch-k{k} {{ animation: l15srch-k{k} {CYCLE}s infinite; }}")
css.append("@keyframes l15srch-draw { 0%, 60% { stroke-dashoffset: 100 } 74%, 93% { stroke-dashoffset: 0 } 100% { stroke-dashoffset: 100 } }")
css.append(".l15srch-draw { stroke-dasharray: 100; animation: l15srch-draw %ds infinite; }" % CYCLE)
css.append("@media (prefers-reduced-motion: reduce) { [class*='l15srch-'] { animation: none !important; opacity: 1 !important; stroke-dashoffset: 0 !important; } }")
css.append("@media print { [class*='l15srch-'] { animation: none !important; opacity: 1 !important; stroke-dashoffset: 0 !important; } }")
s.raw("<style>" + " ".join(css) + "</style>")
setting(s)
ZERO = {("V", 0), ("N", 1), ("V", 1), ("M", 2), ("M", 3), ("V", 3)}
BESTP = [("N", 0), ("M", 1), ("V", 2), ("N", 3)]
BACK = {("M", 1): "N", ("N", 2): "M", ("V", 2): "M", ("N", 3): "V"}   # Viterbi: best box each box came from
PAN = [(20, "ml-cell", "1 · ลองทุกเส้นทาง", "1 · Try every path", "เหมือนลองทุกเส้นทางบนแผนที่", "like driving every possible route",
        "81 เส้นทาง", "81 paths", "✓ ได้ดีที่สุดเสมอ", "✓ always the best", "ml-ok"),
       (404, "nt-band-a", "2 · Viterbi", "2 · Viterbi", "แอปแผนที่: จำแค่ทางที่ดีที่สุดไปแต่ละจุด", "map app: best route to each stop",
        "36 ขั้น", "36 steps", "✓ ได้ดีที่สุดเสมอ", "✓ always the best", "ml-ok"),
       (788, "sw-warn-box", "3 · Beam search", "3 · Beam search", "ประกวดร้องเพลง: แต่ละรอบเหลือแค่ B คน", "talent show: only the top B go on",
        "≈ 12 ขั้น (B = 1)", "≈ 12 steps (B = 1)", "✗ อาจพลาดตัวที่ดีที่สุด", "✗ can miss the best", "ml-neg")]
GX = [56, 136, 216, 296]; GY = {"N": 186, "M": 238, "V": 290}


def dot(x, y, cls, label, tcls="dg-code"):
    s.raw(f'<circle cx="{x:g}" cy="{y:g}" r="15" class="{cls}"/>')
    s.text(x, y + 5, label, tcls, "middle")


def group(k):
    s.raw(f'<g class="l15srch-k{k}">')


for p, (x0, cls, tth, ten, ith, ien, cth, cen, gth, gen, gcls) in enumerate(PAN):
    s.box(x0, 86, 372, 360, cls, 14)
    s.both(x0 + 18, 116, tth, ten, "pl-label")
    s.both(x0 + 18, 142, ith, ien, "pl-note")
    for k, w_ in enumerate(WORDS):
        s.text(x0 + GX[k], 168, w_, "dg-code", "middle")
    def P(t_, k): return x0 + GX[k], GY[t_]
    if p == 0:      # static: every edge between neighbouring columns
        for k in range(3):
            for a in TG:
                for b in TG:
                    (x1, y1), (x2, y2) = P(a, k), P(b, k + 1)
                    s.raw(f'<path d="M{x1 + 15:g} {y1:g} L{x2 - 15:g} {y2:g}" stroke="var(--muted)" stroke-width="1.2" opacity=".55"/>')
        for t_ in TG:
            for k in range(4):
                dot(*P(t_, k), "ml-cell", t_)
        s.both(x0 + 18, 340, "→ ให้คะแนนทุกเส้น แล้วเลือกที่สูงสุด", "→ score them all, pick the top", "pl-note")
    elif p == 1:    # Viterbi: column k (with its best arrows in) appears at step k; the winning path draws at step 4
        for k in range(4):
            group(k)
            for (t_, kk), frm in BACK.items():
                if kk == k:
                    (x1, y1), (x2, y2) = P(frm, k - 1), P(t_, k)
                    s.raw(f'<path d="M{x1 + 15:g} {y1:g} L{x2 - 15:g} {y2:g}" class="pl-line" style="stroke-width:1.6"/>')
            for t_ in TG:
                z = (t_, k) in ZERO
                dot(*P(t_, k), "pl-chip-del" if z else "ml-cell", t_, "pl-note" if z else "dg-code")
            s.raw("</g>")
        pts = [P(t_, k) for t_, k in BESTP]
        d = "M" + " L".join(f"{x:g} {y:g}" for x, y in pts)
        s.raw(f'<path d="{d}" pathLength="100" fill="none" class="pl-line l15srch-draw" style="stroke-width:4"/>')
        group(4)
        for t_, k in BESTP:
            dot(*P(t_, k), "sw-chip-warn", t_)
        s.text(x0 + 18, 340, "→ N M V N = 1/3888", "ml-ok")
        s.raw("</g>")
    else:           # beam 1: Will appears, N is dropped and M kept, then can is all 0: dead end
        group(0)
        for t_ in TG:
            z = (t_, 0) in ZERO
            dot(*P(t_, 0), "pl-chip-del" if z else "ml-cell", t_, "pl-note" if z else "dg-code")
        s.raw("</g>")
        group(1)
        x, y = P("N", 0)
        s.raw(f'<path d="M{x - 11:g} {y - 11:g} L{x + 11:g} {y + 11:g} M{x + 11:g} {y - 11:g} L{x - 11:g} {y + 11:g}" stroke="var(--accent)" stroke-width="2.4"/>')
        dot(*P("M", 0), "sw-chip-warn", "M")
        s.both(x0 + 70, 322, "เก็บแค่อันดับ 1", "keep only the top 1", "pl-note")
        s.raw("</g>")
        group(2)
        (x1, y1), (x2, y2) = P("M", 0), P("M", 1)
        s.raw(f'<path d="M{x1 + 15:g} {y1:g} L{x2 - 15:g} {y2:g}" class="pl-line" stroke-dasharray="5 4"/>')
        for t_ in TG:
            dot(*P(t_, 1), "pl-chip-del", t_, "pl-note")
        s.raw("</g>")
        group(3)
        for t_ in TG:
            for k in (2, 3):
                dot(*P(t_, k), "pl-chip-del", "–", "pl-note")
        s.both(x0 + 18, 352, "B = 1: ทางตันที่ can", "B = 1: dead end at can", "ml-neg")
        s.raw("</g>")
        group(4)
        s.both(x0 + 18, 378, "B = 2: เจอ N M V N ✓", "B = 2: finds N M V N ✓", "ml-ok")
        s.raw("</g>")
    s.both(x0 + 18, 410, cth, cen, "nt-band-title")
    s.both(x0 + 18, 436, gth, gen, gcls)
s.both(20, 482, "ประโยคจริง 45 ป้าย 20 คำ:  1.2 × 10³³ เส้นทาง  ·  Viterbi 40,500 ขั้น  ·  beam (B = 5) 4,500 ขั้น",
       "A real sentence, 45 tags and 20 words:  1.2 × 10³³ paths  ·  Viterbi 40,500 steps  ·  beam (B = 5) 4,500 steps", "pl-label")
s.save("l15-search.svg", 498)

# ---------------------------------------------------------------- 10. CRF as a weighted sum, like linear regression (real weights)
s = Svg(W, "A CRF scores each possible tag like linear regression: score = sum of weight times feature. The features x are ones we "
           "design (feature engineering): for refuse in 'obtain the refuse permit', bias 1, word = refuse 1, last 3 letters use 1, "
           "last 2 letters se 1, capitalised 0, number 0, previous word the 1, next word permit 1, and the tag pair from DT 1. The CRF "
           "learned one weight per feature and tag: for NN 4.09, 0.00, 0.02, 1.71, -1.56, -2.00, 0.95, 0.00, 2.37, total 9.14; for "
           "JJ total 6.21; for VBP total 4.24. Softmax gives P(NN) = 0.615, P(JJ) = 0.349, P(VBP) = 0.003, so refuse is tagged NN.")
# data → features → score, left to right
s.box(20, 0, 350, 104, "ml-cell", 12)
s.both(36, 28, "① ข้อมูล: คำในประโยค", "① Data: a word in its sentence", "pl-label")
tx = 36
for w_, hi in [("obtain", 0), ("the", 0), ("refuse", 1), ("permit", 0)]:
    cw = width(w_) + 16
    s.box(tx, 46, cw, 34, "sw-chip-warn" if hi else "nt-bubble", 8)
    s.text(tx + cw / 2, 69, w_, "pl-text", "middle")
    tx += cw + 6
s.arrow(374, 52, 396, 52)
s.box(400, 0, 400, 104, "nt-band-a", 12)
s.both(416, 28, "② feature engineering: เราเขียน features()", "② Feature engineering: we write features()", "pl-label")
s.text(416, 58, "refuse → word=refuse, suffix3=use,", "dg-code")
s.text(416, 82, "  suffix2=se, prev=the, next=permit, …", "dg-code")
s.arrow(804, 52, 826, 52)
s.box(830, 0, 330, 104, "ml-cell", 12)
s.both(846, 28, "③ ให้คะแนนแบบ linear regression", "③ Score like linear regression", "pl-label")
s.text(846, 60, "ŷ = w₁x₁ + w₂x₂ + … + b", "pl-text")
s.text(846, 88, "score(tag) = Σ w·x", "pl-label")
s.both(20, 132, "x = feature ที่เราออกแบบเอง (feature engineering) · w = น้ำหนักที่ CRF เรียนจากข้อมูล · softmax เปลี่ยนคะแนนเป็น P",
       "x = features we design ourselves (feature engineering) · w = weights the CRF learns · softmax turns scores into P", "pl-text")
COLS = [560, 720, 870, 1020]
HEAD = ("feature ที่เราออกแบบ (x) สำหรับ refuse", "Feature we designed, for refuse", "x", "w ถ้าเป็น NN", "w if NN",
        "w ถ้าเป็น JJ", "w if JJ", "w ถ้าเป็น VBP", "w if VBP")
ROWS = [("bias (เป็น 1 เสมอ)", "bias (always 1)", 1, 4.09, 2.95, 1.63),
        ("คำ = refuse", "word = refuse", 1, 0.00, 0.00, 0.57),
        ("3 ตัวท้าย = use", "last 3 letters = use", 1, 0.02, -0.24, 0.69),
        ("2 ตัวท้าย = se", "last 2 letters = se", 1, 1.71, 1.17, 1.29),
        ("ขึ้นต้นตัวใหญ่ไหม", "starts with a capital?", 0, -1.56, -0.23, -1.44),
        ("เป็นตัวเลขไหม", "is a number?", 0, -2.00, -0.51, -0.18),
        ("คำก่อนหน้า = the", "previous word = the", 1, 0.95, 1.32, 0.00),
        ("คำถัดไป = permit", "next word = permit", 1, 0.00, 0.00, 0.00),
        ("คู่ป้าย: DT → ป้ายของคำ", "tag pair: DT → this tag", 1, 2.37, 1.02, 0.05)]
s.box(20, 144, 1140, 30, "nt-bubble", 6)
s.both(36, 165, HEAD[0], HEAD[1], "pl-label")
s.both(COLS[0], 165, "x จากข้อมูล", "x from data", "pl-label", "middle")
for c, k in enumerate((3, 5, 7)):
    s.both(COLS[c + 1], 165, HEAD[k], HEAD[k + 1], "pl-label", "middle")
for r, (th, en, x, *ws) in enumerate(ROWS):
    y = 180 + r * 32
    cls = "pl-chip-del" if x == 0 else ("nt-band-a" if r == len(ROWS) - 1 else "ml-cell")
    s.box(20, y, 1140, 30, cls, 6)
    s.both(36, y + 22, th, en, "pl-note" if x == 0 else "pl-text")
    s.text(COLS[0], y + 22, str(x), "ml-neg" if x == 0 else "pl-label", "middle")
    for c, w_ in enumerate(ws):
        s.text(COLS[c + 1], y + 22, f"{w_:+.2f}".replace("+0.00", "0.00"), "pl-note" if x == 0 else "dg-code", "middle")
y = 180 + len(ROWS) * 32 + 4
s.box(20, y, 1140, 30, "sw-chip-warn", 6)
s.both(36, y + 21, "คะแนน = Σ w·x", "score = Σ w·x", "pl-label")
for c, v in enumerate(["9.14", "6.21", "4.24"]):
    s.text(COLS[c + 1], y + 21, v, "pl-label", "middle")
y += 34
s.box(20, y, 1140, 30, "ml-cell", 6)
s.both(36, y + 21, "softmax → P", "softmax → P", "pl-label")
for c, v in enumerate(["0.615", "0.349", "0.003"]):
    s.text(COLS[c + 1], y + 21, v, "ml-ok" if c == 0 else "pl-text", "middle")
s.raw(f'<rect x="{COLS[1] - 62}" y="146" width="124" height="{y + 30 - 144}" rx="8" fill="none" stroke="var(--accent)" stroke-width="2.4"/>')
s.both(20, y + 62, "✓ refuse = NN แม้ใน training ไม่เคยเป็น NN (น้ำหนักคำ = 0.00): ท้ายคำ -se คำว่า the และคู่ป้าย DT → NN ตัดสินแทน",
       "✓ refuse = NN, though it was never NN in training (word weight 0.00): the -se ending, the word the and DT → NN decide", "ml-ok")
s.both(20, y + 88, "แถวเส้นประมี x = 0 จึงบวก 0 · ผลรวมใช้น้ำหนักก่อนปัดเศษ จึงอาจต่างจากการบวกในตาราง 0.01",
       "dashed rows have x = 0, so they add 0 · totals use unrounded weights, so hand sums can differ by 0.01", "pl-note")
s.save("l15-crf.svg", y + 104)

# ---------------------------------------------------------------- 11. accuracy of the statistical taggers (real)
ACC = [("always NN", 14.5), ("unigram", 87.9), ("unigram + rules", 92.5), ("HMM", 89.9), ("CRF", 96.2)]
s = Svg(W, "Accuracy on 414 held-out Penn Treebank sentences (10,329 words). Always NN: 14.5%. Unigram: 87.9%. Unigram with ending "
           "rules: 92.5%. HMM: 89.9%, below the unigram with rules because 953 test words (9.2%) were never seen in training. "
           "CRF: 96.2%. The state of the art, neural models trained on the full treebank, is about 97 to 98%.")
s.both(20, 30, "ความแม่นบนประโยคทดสอบ 414 ประโยค (10,329 คำ) · เทรนด้วย 3,500 ประโยค", "Accuracy on 414 test sentences (10,329 words) · trained on 3,500", "pl-label")
X0, X1 = 230, 1080
for k, (lab, v) in enumerate(ACC):
    y = 56 + k * 52
    s.text(X0 - 12, y + 26, lab, "pl-text", "end")
    s.box(X0, y + 6, (X1 - X0) * v / 100, 30, "ml-bar-top" if lab == "CRF" else "ml-bar", 4)
    s.text(X0 + (X1 - X0) * v / 100 + 10, y + 28, f"{v}%", "pl-label")
xs = X0 + (X1 - X0) * 0.97
s.raw(f'<path d="M{xs:.0f} 48 V320" class="pl-line" stroke-dasharray="6 5"/>')
s.both(xs - 8, 340, "state of the art ≈ 97% (neural)", "state of the art ≈ 97% (neural)", "pl-note", "end")
s.both(20, 376, "HMM แพ้ unigram + rules เพราะ 953 คำในชุดทดสอบ (9.2%) ไม่เคยเห็นตอนเทรน",
       "HMM loses to unigram + rules: 953 test words (9.2%) were never seen in training", "ml-neg")
s.both(20, 404, "CRF ใช้ท้ายคำและคำข้าง ๆ เป็น feature จึงรับมือคำใหม่ได้ดีกว่า", "CRF uses endings and neighbours as features, so it copes with new words", "ml-ok")
s.save("l15-accuracy.svg", 420)

# ---------------------------------------------------------------- 12. neural taggers: BiLSTM-CRF and BERT (subwords)
s = Svg(W, "Two neural taggers. A BiLSTM-CRF turns each word into a vector, reads the sentence left to right and right to left so every "
           "word sees both sides, and a CRF layer on top picks a valid tag sequence. BERT splits words into subwords (AMR becomes AM "
           "and ##R), reads all of them at once with self-attention, and puts one classifier on each token; the first subword's "
           "label is used for the whole word.")
s.box(20, 20, 560, 470, "ml-cell", 14)
s.both(40, 52, "A · BiLSTM-CRF (ก่อนยุค Transformer)", "A · BiLSTM-CRF (before Transformers)", "pl-label")
WS = ["spokesman", "Tim", "Wagner", "said"]; TGS = ["O", "B-PER", "I-PER", "O"]
xs = [168 + k * 100 for k in range(4)]
ROWY = {"tags": 112, "crf": 172, "bwd": 252, "fwd": 322, "vec": 392}
LABS = [("tags", "ป้าย", "tags"), ("crf", "CRF", "CRF"), ("bwd", "← LSTM", "← LSTM"), ("fwd", "→ LSTM", "→ LSTM"), ("vec", "vector", "vectors")]
for key, th, en in LABS:
    s.both(40, ROWY[key] + 24, th, en, "pl-note")
for x, w_, tg in zip(xs, WS, TGS):
    s.text(x + 44, 462, w_, "pl-text", "middle")
    s.box(x, ROWY["vec"], 88, 36, "ml-cell", 8)
    s.box(x, ROWY["fwd"], 88, 36, "nt-bubble", 8)
    s.box(x, ROWY["bwd"], 88, 36, "nt-bubble", 8)
    s.box(x, ROWY["tags"], 88, 36, "sw-chip-warn" if tg != "O" else "nt-bubble", 8)
    s.text(x + 44, ROWY["tags"] + 24, tg, "dg-code", "middle")
    s.arrow(x + 44, ROWY["vec"] - 2, x + 44, ROWY["fwd"] + 38)
for k in range(3):
    s.arrow(xs[k] + 88, ROWY["fwd"] + 18, xs[k + 1], ROWY["fwd"] + 18)
    s.arrow(xs[k + 1], ROWY["bwd"] + 18, xs[k] + 88, ROWY["bwd"] + 18)
s.box(xs[0], ROWY["crf"], xs[3] + 88 - xs[0], 40, "rc-res", 8)
s.both((xs[0] + xs[3] + 88) / 2, ROWY["crf"] + 26, "I-PER ต้องตามหลัง B-PER", "I-PER must follow B-PER", "pl-text", "middle")
s.both(40, 488, "word + char vector → อ่านสองทิศ → CRF เลือกป้าย", "word + char vectors → read both ways → CRF picks tags", "pl-note")
s.box(600, 20, 560, 470, "nt-band-a", 14)
s.both(620, 52, "B · BERT (Transformer) + ป้ายต่อ token", "B · BERT (Transformer) + one label per token", "pl-label")
SUB = ["American", "Airlines", "AM", "##R", "Corp"]; SL = ["B-ORG", "I-ORG", "B-ORG", "I-ORG", "I-ORG"]
xs = [624 + k * 104 for k in range(5)]
for x, w_, tg in zip(xs, SUB, SL):
    s.box(x, 408, 96, 36, "sw-chip-warn" if w_ in ("AM", "##R") else "ml-cell", 8)
    s.text(x + 48, 432, w_, "dg-code", "middle")
    s.box(x, 112, 96, 36, "sw-chip-warn", 8); s.text(x + 48, 136, tg, "dg-code", "middle")
    s.arrow(x + 48, 404, x + 48, 340)
    s.arrow(x + 48, 228, x + 48, 152)
s.box(624, 236, 512, 100, "nt-bubble", 12)
s.both(880, 280, "12 ชั้น self-attention", "12 layers of self-attention", "pl-label", "middle")
s.both(880, 306, "ทุก token เห็นทุก token พร้อมกัน", "every token sees every token at once", "pl-note", "middle")
s.both(620, 96, "ชั้นบนสุด: linear + softmax ต่อ token", "top layer: linear + softmax on each token", "pl-note")
s.both(620, 474, "AMR ถูกตัดเป็น AM + ##R: ใช้ป้ายของชิ้นแรก", "AMR is split into AM + ##R: use the first piece's label", "ml-ok")
s.save("l15-neural.svg", 504)

# ---------------------------------------------------------------- 12a. BERT NER, bottom to top (real tokens, tags and scores from dslim/bert-base-NER)
s = Svg(W, "How the BERT NER model tags '... a unit of AMR Corp., ... spokesman Tim Wagner said.', read from the bottom. 1: the text. "
           "2: the tokenizer splits it into pieces, AMR becomes AM and ##R, with [CLS] and [SEP] added. 3: BERT, 12 layers of "
           "self-attention, turns each piece into 768 numbers that depend on all the other pieces (about 108 million weights, "
           "pre-trained on books and Wikipedia, fine-tuned on CoNLL-2003). 4: a classifier on each piece picks one of 9 labels. "
           "5: the tags: AM B-ORG, ##R I-ORG, Corp I-ORG, Tim B-PER, Wagner I-PER, the rest O. 6: aggregation joins B and I "
           "pieces into names: ORG AMR Corp 0.999, PER Tim Wagner 1.000.")
TOK = ["[CLS]", "…", "AM", "##R", "Corp", ".", "…", "spokesman", "Tim", "Wagner", "said", "…", "[SEP]"]
TAG = ["–", "", "B-ORG", "I-ORG", "I-ORG", "O", "", "O", "B-PER", "I-PER", "O", "", "–"]
LX = 228
tw = [34 if t == "…" else max(width(t, 15), width(TAG[k], 15)) + 18 for k, t in enumerate(TOK)]
gap = (1160 - LX - sum(tw)) / (len(TOK) - 1)
tx, cx = LX, []
for w_ in tw:
    cx.append(tx + w_ / 2); tx += w_ + gap
ROW = {"ent": 22, "tag": 104, "cls": 166, "bert": 226, "tok": 352, "txt": 426}
LBL = [("ent", "⑥ รวมเป็นชื่อ", "⑥ Join into names"), ("tag", "⑤ ป้ายต่อชิ้น", "⑤ One tag per piece"),
       ("cls", "④ ตัวจำแนก", "④ Classifier"), ("bert", "③ BERT", "③ BERT"), ("tok", "② ตัดเป็นชิ้น", "② Tokenizer"),
       ("txt", "① ข้อความ", "① Text")]
for key, th, en in LBL:
    s.both(20, ROW[key] + 24, th, en, "pl-label")
# 1 · text
s.box(LX, ROW["txt"], 1160 - LX, 40, "ml-cell", 10)
s.text(LX + 16, ROW["txt"] + 27, "… a unit of AMR Corp., immediately matched the move, spokesman Tim Wagner said.", "pl-text")
# 2 · tokens, 5 · tags, arrows between
for k, t in enumerate(TOK):
    x0 = cx[k] - tw[k] / 2
    if t == "…":
        s.text(cx[k], ROW["tok"] + 24, "…", "pl-note", "middle")
        s.text(cx[k], ROW["tag"] + 24, "…", "pl-note", "middle")
        continue
    s.box(x0, ROW["tok"], tw[k], 36, "opt-b-box" if t in ("AM", "##R") else "nt-bubble", 8)
    s.text(cx[k], ROW["tok"] + 24, t, "dg-code", "middle")
    s.arrow(cx[k], ROW["tok"] - 2, cx[k], ROW["bert"] + 104)
    s.arrow(cx[k], ROW["cls"] - 2, cx[k], ROW["tag"] + 38)
    hot = TAG[k] not in ("O", "–")
    s.box(x0, ROW["tag"], tw[k], 34, ("nt-band-a" if "ORG" in TAG[k] else "sw-chip-warn") if hot else "ml-cell", 8)
    s.text(cx[k], ROW["tag"] + 23, TAG[k], "dg-code" if hot else "pl-note", "middle")
# 3 · BERT block with a few attention arcs
s.box(LX, ROW["bert"], 1160 - LX, 100, "nt-band-a", 12)
for a_, b_ in [(8, 9), (7, 8), (2, 4), (4, 8)]:
    xa, xb = cx[a_], cx[b_]
    s.raw(f'<path d="M{xa:g} {ROW["bert"] + 96} Q{(xa + xb) / 2:g} {ROW["bert"] + 52} {xb:g} {ROW["bert"] + 96}" fill="none" '
          f'stroke="var(--tag-concept-dot)" stroke-width="1.6" opacity=".8"/>')
s.both(LX + 16, ROW["bert"] + 28, "12 ชั้น self-attention: ทุกชิ้นมองทุกชิ้น · ชิ้นละ 768 ตัวเลข", "12 layers of self-attention: every piece looks at every piece · 768 numbers per piece", "pl-text")
s.both(LX + 16, ROW["bert"] + 58, "ราว 108 ล้านน้ำหนัก · pre-train กับหนังสือ + Wikipedia · fine-tune กับ CoNLL-2003", "≈ 108 M weights · pre-trained on books + Wikipedia · fine-tuned on CoNLL-2003", "pl-note")
# 4 · classifier band
s.box(LX, ROW["cls"], 1160 - LX, 34, "nt-bubble", 8)
s.both(LX + 16, ROW["cls"] + 23, "linear + softmax ทุกชิ้น: เลือก 1 จาก 9 ป้าย (O และ B-/I- ของ PER ORG LOC MISC)",
       "linear + softmax on every piece: pick 1 of 9 labels (O, B-/I- × PER, ORG, LOC, MISC)", "pl-note")
# 6 · entities spanning their pieces
for k0, k1, typ, name, sc in [(2, 4, "ORG", "AMR Corp", "0.999"), (8, 9, "PER", "Tim Wagner", "1.000")]:
    x0 = cx[k0] - tw[k0] / 2; x1 = cx[k1] + tw[k1] / 2
    label = f"{typ} · {name} · {sc}"
    bw = max(x1 - x0, width(label) + 28); bx = (x0 + x1) / 2 - bw / 2
    s.box(bx, ROW["ent"], bw, 40, "nt-band-a" if typ == "ORG" else "sw-chip-warn", 10)
    s.text((x0 + x1) / 2, ROW["ent"] + 26, label, "pl-label", "middle")
    s.arrow((x0 + x1) / 2, ROW["tag"] - 2, (x0 + x1) / 2, ROW["ent"] + 46)
s.save("l15-bert-ner.svg", ROW["txt"] + 48)

# ---------------------------------------------------------------- 12b. what is a named entity: our announcement highlighted, types as tiles
ETC = {"PER": "sw-chip-warn", "ORG": "nt-band-a", "LOC": "opt-a-box", "GPE": "opt-a-box",
       "DATE": "opt-b-box", "MONEY": "opt-b-box", "TIME": "opt-b-box", "PERCENT": "opt-b-box", "EVENT": "opt-b-box",
       "PRODUCT": "opt-b-box", "MISC": "ml-cell", "DISEASE": "ml-cell", "DRUG": "ml-cell"}
s = Svg(W, "Named entities in our airline announcement: United Airlines (ORG) said Friday (DATE) it increased fares by $6 (MONEY); "
           "American Airlines (ORG), a unit of AMR Corp. (ORG), matched the move, spokesman Tim Wagner (PER) said; routes such as "
           "Chicago (LOC) to Dallas (LOC). Core types are proper names: PER, ORG, LOC and GPE. Extended types are useful but not names: "
           "DATE, TIME, MONEY, PERCENT, EVENT, PRODUCT. Hard names: ordinary words used as names (Rich, Mars, Dean), Thai names with "
           "no capital letters, gene names (rpsL, polA), abbreviations (PN = penicillin, not pneumonia). Tagsets differ: CoNLL-2003 "
           "has 4 types, OntoNotes 18, medical data DISEASE and DRUG.")
s.both(20, 22, "ในประกาศของเรา: ชื่อเฉพาะถูกระบายสีตามชนิด", "In our announcement: every name, coloured by its type", "pl-label")
LINES = [[("United Airlines", "ORG"), (" said ", None), ("Friday", "DATE"), (" it has increased fares by ", None), ("$6", "MONEY"), (" …", None)],
         [("American Airlines", "ORG"), (", a unit of ", None), ("AMR Corp.", "ORG"), (", matched the move, spokesman ", None),
          ("Tim Wagner", "PER"), (" said.", None)],
         [("… routes such as ", None), ("Chicago", "LOC"), (" to ", None), ("Dallas", "LOC"), (" and ", None), ("Denver", "LOC"),
          (" to ", None), ("San Francisco", "LOC")]]
for r, line in enumerate(LINES):
    y, x = 44 + r * 58, 20
    for txt, typ in line:
        if typ:
            cw = width(txt) + 18
            s.box(x, y + 16, cw, 34, ETC[typ], 8)
            s.text(x + cw / 2, y + 39, txt, "pl-text", "middle")
            s.text(x + cw / 2, y + 11, typ, "dg-index", "middle")
            x += cw
        else:
            s.text(x + 6, y + 39, txt.strip(), "pl-text")
            x += width(txt.strip()) * 0.9 + 12
# core vs extended types as icon tiles
Y2 = 236
s.both(20, Y2, "ชนิดหลัก: ชื่อเฉพาะจริง ๆ", "Core types: proper names", "pl-label")
s.both(600, Y2, "ชนิดขยาย: ไม่ใช่ชื่อ แต่มีประโยชน์", "Extended types: not names, but useful", "pl-label")
CORE = [("profile", "PER", "Tim Wagner"), ("office", "ORG", "American Airlines"), ("flag", "LOC", "Chicago"),
        ("ballot", "GPE", "Thailand (as a state)")]
EXT = [("calendar", "DATE", "Friday"), ("moneybag", "MONEY", "$6"), ("clock", "TIME", "2 p.m."),
       ("chartup", "PERCENT", "5%"), ("stars", "EVENT", "World Cup"), ("shoppingbag", "PRODUCT", "iPhone")]
def tile(x, y, icon, typ, ex, w=272):
    s.box(x, y, w, 46, "ml-cell", 10)
    ic(s, icon, x + 24, y + 23, 30)
    cw = width(typ, 15) + 20
    s.box(x + 46, y + 9, cw, 28, ETC[typ], 6)
    s.text(x + 46 + cw / 2, y + 28, typ, "dg-code", "middle")
    s.text(x + 56 + cw, y + 29, ex, "pl-text")
for k, (icon, typ, ex) in enumerate(CORE):
    tile(20 + (k % 2) * 284, Y2 + 14 + (k // 2) * 54, icon, typ, ex)
s.both(20, Y2 + 148, "สิ่งที่เรียกด้วยชื่อเฉพาะได้: คน บริษัท สถานที่ ประเทศ",
       "anything you can call by a proper name: people, companies, places", "pl-note")
for k, (icon, typ, ex) in enumerate(EXT):
    tile(600 + (k % 2) * 284, Y2 + 14 + (k // 3 if False else k // 2) * 54, icon, typ, ex)
# hard names and differing tagsets
Y3 = Y2 + 186
s.box(20, Y3, 560, 152, "sw-warn-box", 12)
s.both(36, Y3 + 28, "✗ ชื่อที่ยาก", "✗ Hard names", "pl-label")
HARD = [("Rich · Mars · Dean", "เป็นคำธรรมดาด้วย", "also ordinary words"),
        ("สนธยา คุณปลื้ม", "ภาษาไทยไม่มีตัวพิมพ์ใหญ่ช่วย", "Thai: no capital letters to help"),
        ("rpsL · polA", "ชื่อยีน", "gene names"),
        ("PN", "= penicillin ไม่ใช่ pneumonia", "= penicillin, not pneumonia")]
for k, (ex, th, en) in enumerate(HARD):
    y = Y3 + 46 + k * 26
    s.text(36, y + 16, ex, "pl-label")
    s.both(236, y + 16, th, en, "pl-note")
s.box(600, Y3, 560, 152, "nt-band-a", 12)
s.both(616, Y3 + 28, "ชุดป้ายต่างกันในแต่ละชุดข้อมูล", "Each dataset has its own tagset", "pl-label")
SETS = [("CoNLL-2003", ["PER", "ORG", "LOC", "MISC"]), ("Medical", ["DISEASE", "DRUG"])]
for k, (name, tags) in enumerate(SETS):
    y = Y3 + 44 + k * 70
    s.text(616, y + 22, name, "pl-text")
    tx = 750
    for t in tags:
        cw = width(t, 15) + 18
        s.box(tx, y + 4, cw, 26, ETC[t], 6); s.text(tx + cw / 2, y + 22, t, "dg-code", "middle")
        tx += cw + 6
y = Y3 + 79
s.text(616, y + 22, "OntoNotes", "pl-text")
for k in range(18):
    s.box(750 + k * 17, y + 8, 13, 17, "ml-cell", 3)
s.both(1064, y + 22, "18 ชนิด", "18 types", "pl-label")
s.save("l15-entities.svg", Y3 + 158)

# ---------------------------------------------------------------- 13. BIO on the running sentence, and why IO is not enough
s = Svg(W, "NER as tagging. BERT's real output on 'American Airlines, a unit of AMR Corp., ... spokesman Tim Wagner said': "
           "American B-ORG, Airlines I-ORG, AMR B-ORG, Corp I-ORG, Tim B-PER, Wagner I-PER, every other word O. Why B and not just I: "
           "with IO tags, 'United States Air Force' read as two organisations, United States and Air Force, becomes I-ORG four times "
           "and merges into one; BIO marks the second start with B-ORG.")
s.both(20, 30, "ผลจริงจาก dslim/bert-base-NER", "Real output of dslim/bert-base-NER", "pl-note")
tagged(s, 20, 44, [("American", "B-ORG"), ("Airlines", "I-ORG"), (",", "O"), ("a", "O"), ("unit", "O"), ("of", "O"), ("AMR", "B-ORG"), ("Corp", "I-ORG"), (".", "O")], gap=8, hi=(0, 1, 6, 7))
tagged(s, 20, 144, [("immediately", "O"), ("matched", "O"), ("the", "O"), ("move", "O"), (",", "O"), ("spokesman", "O"), ("Tim", "B-PER"), ("Wagner", "I-PER"), ("said", "O")], gap=8, hi=(6, 7))
s.box(20, 250, 560, 210, "sw-warn-box", 14)
s.both(40, 282, "✗ ใช้แค่ I / O", "✗ Only I / O", "pl-label")
tagged(s, 40, 300, [("United", "I-ORG"), ("States", "I-ORG"), ("Air", "I-ORG"), ("Force", "I-ORG")], gap=8)
s.both(40, 438, "✗ แยกไม่ได้ว่าเป็น 1 หรือ 2 องค์กร", "✗ one entity or two? can't tell", "ml-neg")
s.box(600, 250, 560, 210, "nt-band-a", 14)
s.both(620, 282, "✓ B / I / O", "✓ B / I / O", "pl-label")
tagged(s, 620, 300, [("United", "B-ORG"), ("States", "I-ORG"), ("Air", "B-ORG"), ("Force", "I-ORG")], gap=8, hi=(2,))
s.both(620, 438, "✓ B ตัวที่สองบอกว่าชื่อใหม่เริ่มตรงนี้", "✓ the second B says a new name starts here", "ml-ok")
s.save("l15-bio.svg", 476)

# ---------------------------------------------------------------- 14. one word, three meanings: "Bangkok" (real BERT labels)
s = Svg(W, "The same word gets different entity types in context. Real output of dslim/bert-base-NER: in 'APEC 2022 will take place "
           "in Bangkok' Bangkok is LOC, right. In 'Bangkok Bank responds to BOT' the whole 'Bangkok Bank' is ORG, right. In 'The "
           "Central Administrative Court ordered Bangkok to repay the debt to BTS' Bangkok means the city government, an organisation, "
           "but the model says LOC: its four types (PER, ORG, LOC, MISC) have no geo-political entity.")
CASES = [("APEC 2022 will take place in", "Bangkok", ", where roads will be closed ...", "LOC", "สถานที่: ถูก", "a place: right", True),
         ("", "Bangkok Bank", " responds to BOT's relief measures.", "ORG", "ธนาคาร: ถูก", "a bank: right", True),
         ("The Court ordered", "Bangkok", " to repay the debt to BTS.", "LOC", "หมายถึง กทม. (หน่วยงาน) แต่ได้ LOC", "means the city government, yet LOC", False)]
for k, (pre, ent, post, lab, th, en, ok) in enumerate(CASES):
    y = 20 + k * 112
    s.box(20, y, W - 40, 100, "nt-band-a" if ok else "sw-warn-box", 12)
    x = 40
    if pre:
        s.text(x, y + 40, pre, "dg-code"); x += len(pre) * 8.4 + 10
    ew = len(ent) * 8.4 + 20
    s.box(x - 6, y + 18, ew, 32, "sw-chip-warn", 6); s.text(x + 4, y + 40, ent, "dg-code"); x += ew
    s.text(x, y + 40, post, "dg-code")
    s.box(40, y + 58, 70, 30, "nt-bubble", 8); s.text(75, y + 79, lab, "dg-code", "middle")
    s.both(126, y + 80, ("✓ " if ok else "✗ ") + th, ("✓ " if ok else "✗ ") + en, "ml-ok" if ok else "ml-neg")
s.both(20, 372, "โมเดลนี้รู้แค่ 4 ชนิด (PER, ORG, LOC, MISC) ไม่มี GPE, DATE, MONEY: “$34B” และ “2019” จึงไม่ถูกจับเลย",
       "This model knows only 4 types (PER, ORG, LOC, MISC): no GPE, DATE or MONEY, so “$34B” and “2019” are never found", "pl-text")
s.save("l15-bangkok.svg", 390)

# ---------------------------------------------------------------- 15. span-level vs token-level evaluation (real seqeval numbers)
s = Svg(W, "Evaluate NER by spans, not tokens. Gold: New York City is one LOC. Predicted: only New York. Token by token, 5 of 6 tags "
           "match: 0.83. But the entity is wrong, so span-level precision, recall and F1 are all 0. seqeval computes the span scores.")
s.both(20, 30, "Welcome to [New York City]LOC !", "Welcome to [New York City]LOC !", "pl-label")
s.both(20, 72, "gold", "gold", "pl-note"); s.both(20, 152, "ทำนาย", "predicted", "pl-note")
G = ["O", "O", "B-LOC", "I-LOC", "I-LOC", "O"]; P = ["O", "O", "B-LOC", "I-LOC", "O", "O"]; T = ["Welcome", "to", "New", "York", "City", "!"]
x = 130
for w_, g, p in zip(T, G, P):
    cw = max(width(w_), width(g, 17)) + 24
    s.box(x, 50, cw, 36, "ml-cell", 8); s.text(x + cw / 2, 74, w_, "pl-text", "middle")
    s.box(x, 92, cw, 30, "nt-bubble", 8); s.text(x + cw / 2, 113, g, "dg-code", "middle")
    s.box(x, 136, cw, 30, "nt-bubble" if g == p else "sw-chip-warn", 8); s.text(x + cw / 2, 157, p, "dg-code", "middle")
    s.text(x + cw / 2, 190, "✓" if g == p else "✗", "ml-ok" if g == p else "ml-neg", "middle")
    x += cw + 8
s.box(20, 214, 560, 150, "sw-warn-box", 14)
s.both(40, 246, "✗ นับทีละ token", "✗ Count token by token", "pl-label")
s.text(40, 290, "accuracy = 5 / 6 = 0.83", "pl-label")
s.both(40, 330, "ดูดี แต่ได้ชื่อเมืองผิด", "looks good, yet the city name is wrong", "ml-neg")
s.box(600, 214, 560, 150, "nt-band-a", 14)
s.both(620, 246, "✓ นับทีละชื่อ (span)", "✓ Count whole names (spans)", "pl-label")
s.text(620, 290, "precision = recall = F1 = 0", "pl-label")
s.both(620, 330, "[New York] ≠ [New York City]: ผิดทั้งชื่อ", "[New York] ≠ [New York City]: the name is wrong", "ml-ok")
s.save("l15-span-eval.svg", 380)

# ---------------------------------------------------------------- 15b. span evaluation, worked example 2 (real seqeval numbers)
s = Svg(W, "Second worked example on our announcement sentence. Gold names: American Airlines (ORG), AMR Corp. (ORG), Tim Wagner (PER). "
           "Predicted: American Airlines (ORG) correct, AMR (ORG) wrong boundary, spokesman (PER) not a name, Tim Wagner (PER) correct. "
           "2 correct, 2 wrong predictions, 1 gold name missed. Precision 2/4 = 0.50, recall 2/3 = 0.67, F1 = 0.57; token accuracy "
           "17/19 = 0.89 looks much better.")
WDS = "American Airlines , a unit of AMR Corp. , immediately matched the move , spokesman Tim Wagner said .".split()
GOLD = [(0, 1, "ORG"), (6, 7, "ORG"), (15, 16, "PER")]
PRED = [(0, 1, "ORG", True), (6, 6, "ORG", False), (14, 14, "PER", False), (15, 16, "PER", True)]
ww = [width(w_, 19) * 0.86 + 12 for w_ in WDS]
X0 = 112
xs = []
x = X0
for w_ in ww:
    xs.append(x); x += w_
assert x < W - 20, x
s.both(20, 22, "ตัวอย่างที่ 2 · ประโยคในประกาศของเรา", "Example 2 · a sentence from our announcement", "pl-label")
def span_row(y, spans, label_th, label_en):
    s.both(20, y + 30, label_th, label_en, "pl-note")
    for sp in spans:
        a_, b_, typ = sp[0], sp[1], sp[2]
        x1 = xs[a_] + 1; x2 = xs[b_] + ww[b_] - 1
        s.box(x1, y + 6, x2 - x1, 36, "nt-band-a" if typ == "ORG" else "sw-chip-warn", 8)
        s.text((x1 + x2) / 2, y - 4, typ, "dg-index", "middle")
        if len(sp) == 4 and not sp[3]:
            s.raw(f'<rect x="{x1 - 3:g}" y="{y + 3}" width="{x2 - x1 + 6:g}" height="42" rx="10" fill="none" stroke="var(--accent)" stroke-width="2" stroke-dasharray="5 3"/>')
    for k, w_ in enumerate(WDS):
        s.text(xs[k] + ww[k] / 2, y + 30, w_, "pl-text", "middle")
span_row(48, GOLD, "gold", "gold")
span_row(122, PRED, "ทำนาย", "predicted")
for a_, b_, typ, ok in PRED:
    cx_ = (xs[a_] + xs[b_] + ww[b_]) / 2
    s.text(cx_, 190, "✓" if ok else "✗", "ml-ok" if ok else "ml-neg", "middle")
# counts
Y = 212
CNT = [("opt-a-box", "✓ ถูก (true positive) = 2", "✓ Correct (true positives) = 2", "American Airlines · Tim Wagner", "American Airlines · Tim Wagner"),
       ("sw-warn-box", "✗ ทำนายผิด (false positive) = 2", "✗ Wrong predictions (false positives) = 2", "AMR (ขาด Corp.) · spokesman (ไม่ใช่ชื่อ)", "AMR (missing Corp.) · spokesman (not a name)"),
       ("opt-b-box", "✗ พลาด (false negative) = 1", "✗ Missed gold names (false negatives) = 1", "AMR Corp.", "AMR Corp.")]
for k, (cls, th, en, dth, den) in enumerate(CNT):
    y = Y + k * 70
    s.box(20, y, 560, 62, cls, 10)
    s.both(36, y + 26, th, en, "pl-label")
    s.both(36, y + 50, dth, den, "pl-note")
s.box(600, Y, 560, 202, "ml-cell", 10)
s.text(620, Y + 36, "Precision = correct / predicted = 2 / 4 = 0.50", "pl-text")
s.text(620, Y + 74, "Recall = correct / gold = 2 / 3 = 0.67", "pl-text")
s.text(620, Y + 112, "F1 = 2 × 0.50 × 0.67 / (0.50 + 0.67) = 0.57", "pl-label")
s.raw(f'<path d="M620 {Y + 132} H1140" class="pl-line"/>')
s.both(620, Y + 162, "เทียบ token accuracy = 17 / 19 = 0.89", "Token accuracy = 17 / 19 = 0.89", "ml-neg")
s.both(620, Y + 188, "ดูดีกว่ามาก แต่พลาดไปครึ่งหนึ่งของชื่อ", "looks much better, yet half the names are wrong", "pl-note")
s.save("l15-span-eval2.svg", Y + 214)

# ---------------------------------------------------------------- 16. how NER systems evolved
ERAS = [("Rules & lists", "กฎและรายชื่อ", "hand-made", "Mr. + Capital → PER", "province list → LOC"),
        ("HMM, CRF", "โมเดลสถิติ", "statistical", "features: suffix,", "capital, neighbours"),
        ("BiLSTM-CRF", "neural ยุคแรก", "early neural", "word + char vectors", "→ valid BIO"),
        ("BERT", "Transformer", "Transformer", "fine-tune on", "labelled sentences"),
        ("LLMs", "ไม่ต้องเทรน", "no training", "prompt + JSON,", "any entity types")]
s = Svg(W, "How NER systems evolved. Rules and lists: patterns like Mr. plus a capitalised word is a person, and gazetteers such as "
           "a list of provinces. Statistical models, HMM and CRF, with hand-made features. BiLSTM-CRF with word and character vectors. "
           "BERT fine-tuned on labelled sentences. LLMs that follow a prompt and return JSON for any entity types, with no training, "
           "but can hallucinate.")
for k, (en, th, en2, l1, l2) in enumerate(ERAS):
    x0 = 20 + k * 230
    s.box(x0, 40, 218, 200, "nt-band-a" if k == 4 else "ml-cell", 14)
    s.text(x0 + 16, 74, f"{k + 1} · {en}", "pl-label")
    s.both(x0 + 16, 100, th, en2, "pl-note")
    s.text(x0 + 16, 150, l1, "dg-code"); s.text(x0 + 16, 176, l2, "dg-code")
    if k < 4:
        s.arrow(x0 + 220, 140, x0 + 228, 140)
s.raw('<path d="M30 270 H1150" class="pl-line"/>')
s.both(30, 300, "← ต้องเขียนกฎ / ต้องมีข้อมูลติดป้ายมาก", "← hand-written rules / lots of labelled data", "pl-note")
s.both(1150, 300, "ไม่ต้องเทรน แต่ช้า แพง และอาจแต่งชื่อขึ้นมา →", "no training, but slower, costlier, may invent names →", "pl-note", "end")
s.save("l15-ner-evolution.svg", 316)

# ---------------------------------------------------------------- 17. LLM extraction: prompt → JSON → validate
s = Svg(W, "Information extraction with an LLM. The prompt has four parts: the task, the schema (entity types and relation labels), "
           "one or two examples, and the input. The LLM returns JSON. Code then checks it: does it parse, does every entity's text "
           "appear in the input, is every type allowed. In this example the LLM also returned 'Delta Air Lines', which is not in "
           "the text, so the check drops it.")
s.box(20, 20, 330, 400, "ml-cell", 14)
s.both(36, 52, "1 · Prompt", "1 · Prompt", "pl-label")
for k, (th, en) in enumerate([("งาน: ดึงชื่อและความสัมพันธ์", "Task: extract entities, relations"), ("Schema: PERSON ORG LOC", "Schema: PERSON ORG LOC"),
                               ("+ part_of, works_for", "+ part_of, works_for"), ("ตัวอย่าง 1–2 ข้อ", "1–2 examples"), ("ตอบเป็น JSON เท่านั้น", "JSON only, no extra text"),
                               ("Input: ข้อความ", "Input: the text")]):
    s.box(36, 74 + k * 54, 298, 42, "nt-bubble" if k != 5 else "sw-chip-warn", 8)
    s.both(48, 101 + k * 54, th, en, "pl-text")
s.arrow(352, 220, 384, 220)
s.box(388, 20, 380, 400, "ml-cell", 14)
s.both(404, 52, "2 · LLM ตอบ JSON", "2 · The LLM returns JSON", "pl-label")
JS = ['{"entities": [', ' {"text": "American Airlines",', '  "type": "ORG"},', ' {"text": "AMR Corp.",', '  "type": "ORG"},',
      ' {"text": "Tim Wagner",', '  "type": "PERSON"},', ' {"text": "Delta Air Lines",', '  "type": "ORG"}', ']}']
for k, ln in enumerate(JS):
    if k in (7, 8):
        s.box(400, 70 + k * 30 + 2, 356, 28, "sw-chip-warn", 4)
    s.text(410, 90 + k * 30, ln, "dg-code")
s.arrow(770, 220, 802, 220)
s.box(806, 20, 354, 400, "nt-band-a", 14)
s.both(822, 52, "3 · ตรวจด้วยโค้ด", "3 · Check it with code", "pl-label")
for k, (th, en) in enumerate([("อ่านเป็น JSON ได้ไหม", "parses as JSON?"), ("ข้อความอยู่ใน input ไหม", "text appears in the input?"), ("ชนิดอยู่ในรายการไหม", "type is allowed?")]):
    s.box(822, 74 + k * 54, 322, 42, "ml-cell", 8)
    s.both(836, 101 + k * 54, "✓ " + th, "✓ " + en, "pl-text")
s.box(822, 260, 322, 70, "sw-warn-box", 8)
s.both(836, 288, "✗ Delta Air Lines", "✗ Delta Air Lines", "ml-neg")
s.both(836, 314, "ไม่มีในข้อความ → ทิ้ง", "not in the text → dropped", "ml-neg")
s.both(822, 372, "✓ เหลือ 3 ชื่อที่มีอยู่จริง", "✓ 3 names that are really there", "ml-ok")
s.both(20, 450, "Delta Air Lines เป็นตัวอย่างที่เขียนขึ้นของการ “แต่งชื่อ” (hallucination)", "“Delta Air Lines” is a made-up example of a hallucinated entity", "pl-note")
s.save("l15-llm-extract.svg", 466)

# ---------------------------------------------------------------- 17b. relation methods: BERT with entity markers vs prompting an LLM (real Gemini answers)
s = Svg(W, "Two modern ways to find the relation between two names. A, BERT with entity markers (R-BERT): put $ around the first name "
           "and # around the second, BERT reads the marked sentence, then the vector for the whole sentence and the averaged vectors "
           "of the two names are joined and a classifier picks one relation from a fixed list, including no_relation; it needs "
           "labelled pairs to fine-tune. B, prompting an LLM: give the sentence, the two names and the allowed relations, and ask for "
           "JSON. Real Gemini answers at temperature 0: American Airlines and AMR Corp. gave part_of with confidence 0.95; AMR Corp. "
           "and Tim Wagner gave no_relation with confidence 0.9. No training, but check that the label is in the list.")
s.both(20, 22, "สองวิธีสมัยใหม่ในการจำแนกคู่ชื่อ", "Two modern ways to classify a pair of names", "pl-label")
# ---- A · BERT with entity markers
s.box(20, 36, 560, 436, "nt-band-a", 14)
s.both(36, 66, "A · BERT + เครื่องหมายครอบชื่อ (R-BERT)", "A · BERT with entity markers (R-BERT)", "pl-label")
PIECES = [("[CLS]", "nt-bubble"), ("$", "opt-b-box"), ("American Airlines", "sw-chip-warn"), ("$", "opt-b-box"), (", a unit of", None),
          ("#", "opt-b-box"), ("AMR Corp.", "opt-a-box"), ("#", "opt-b-box"), ("…", None)]
x, CX = 36, {}
for k, (t, cls) in enumerate(PIECES):
    cw = len(t) * 8.6 + (12 if cls else 2)
    if cls:
        s.box(x, 84, cw, 30, cls, 6)
    s.text(x + cw / 2, 104, t, "dg-code", "middle")
    CX[k] = x + cw / 2
    x += cw + 3
assert x < 570, x
s.both(36, 138, "$ ครอบชื่อแรก · # ครอบชื่อที่สอง", "$ marks the first name · # marks the second", "pl-note")
s.arrow(300, 146, 300, 162)
s.box(36, 166, 528, 50, "nt-bubble", 10)
s.both(300, 197, "BERT อ่านประโยคที่มีเครื่องหมาย", "BERT reads the marked sentence", "pl-text", "middle")
VEC = [("ทั้งประโยค [CLS]", "whole sentence [CLS]", "nt-bubble"), ("ค่าเฉลี่ยชื่อแรก", "first name, averaged", "sw-chip-warn"),
       ("ค่าเฉลี่ยชื่อที่สอง", "second name, averaged", "opt-a-box")]
for k, (th, en, cls) in enumerate(VEC):
    vx = 40 + k * 178
    s.arrow(vx + 80, 218, vx + 80, 236)
    for q in range(6):
        s.box(vx + 26 + q * 18, 240, 15, 22, cls, 3)
    s.both(vx + 80, 286, th, en, "pl-note", "middle")
s.raw('<path d="M120 296 L120 310 L476 310 L476 296 M300 310 L300 322" fill="none" class="pl-line"/>')
s.arrow(300, 318, 300, 326)
s.box(36, 330, 528, 44, "nt-bubble", 10)
s.both(300, 358, "ต่อกัน → ตัวจำแนก + softmax", "join them → classifier + softmax", "pl-text", "middle")
s.arrow(300, 376, 300, 392)
s.box(36, 396, 528, 36, "ml-cell", 8)
s.text(300, 420, "part_of · works_for · located_in · founder_of · no_relation", "dg-code", "middle")
s.both(36, 462, "ต้องมีคู่ชื่อที่ติดป้ายไว้ เพื่อ fine-tune · เทรนแล้วเร็วและฟรี", "needs labelled pairs to fine-tune · fast and free once trained", "pl-note")
# ---- B · prompt an LLM
s.box(600, 36, 560, 436, "ml-cell", 14)
s.both(616, 66, "B · ถาม LLM ด้วย prompt", "B · Prompt an LLM", "pl-label")
s.box(616, 82, 528, 136, "nt-bubble", 10)
for k, ln in enumerate(["Allowed: part_of, works_for, located_in,", "         founder_of, no_relation",
                        'Sentence: "American Airlines, a unit of', '          AMR Corp., ... Tim Wagner said."',
                        "E1 = American Airlines   E2 = AMR Corp.", "Return JSON: relation + confidence"]):
    s.text(630, 104 + k * 20, ln, "dg-code")
s.arrow(880, 220, 880, 236)
ic(s, "brain", 880, 260, 42)
s.text(912, 266, "Gemini", "pl-label")
s.arrow(880, 284, 880, 300)
s.both(616, 324, "คำตอบจริง (temperature 0)", "Real answers (temperature 0)", "pl-note")
ANS = [("American Airlines → AMR Corp.", '{"relation": "part_of", "confidence": 0.95}', "opt-a-box"),
       ("AMR Corp. → Tim Wagner", '{"relation": "no_relation", "confidence": 0.9}', "ml-cell")]
for k, (pair, js, cls) in enumerate(ANS):
    y = 330 + k * 54
    s.box(616, y, 528, 48, cls, 8)
    s.text(630, y + 20, pair, "pl-note")
    s.text(630, y + 41, js, "dg-code")
s.both(616, 462, "ไม่ต้องเทรน · ตรวจว่า label อยู่ในรายการ", "no training · check the label is in the list", "pl-note")
s.save("l15-re-methods.svg", 478)

# ---------------------------------------------------------------- 18. relation extraction on the running text
s = Svg(W, "Relation extraction links pairs of entities. From the announcement: American Airlines part_of AMR Corp., Tim Wagner "
           "works_for American Airlines, United part_of UAL Corp. Each relation is a triplet (head, relation, tail), and direction "
           "matters: (AMR Corp., part_of, American Airlines) would be wrong. The pipeline: find the entities (NER), pair them, "
           "classify each pair (or no_relation), output triplets.")
ENT = [("American Airlines", 40, "ORG"), ("AMR Corp.", 360, "ORG"), ("Tim Wagner", 640, "PER"), ("United", 900, "ORG"), ("UAL Corp.", 1040, "ORG")]
pos = {}
for n, x, tg in ENT:
    w_ = width(n) + 26
    s.box(x, 110, w_, 40, "sw-chip-warn", 8); s.text(x + w_ / 2, 136, n, "pl-text", "middle")
    s.text(x + w_ / 2, 172, tg, "dg-code", "middle")
    pos[n] = (x, w_)
def arc(a, b, lab, up=True, h=70):
    xa = pos[a][0] + pos[a][1] / 2; xb = pos[b][0] + pos[b][1] / 2
    y = 108
    s.raw(f'<path d="M{xa:.0f} {y} C{xa:.0f} {y - h} {xb:.0f} {y - h} {xb:.0f} {y}" class="pl-line" fill="none"/>')
    s.raw(f'<path d="M{xb - 7:.0f} {y - 10} L{xb:.0f} {y} L{xb + 7:.0f} {y - 10}" class="pl-line" fill="none"/>')
    s.box((xa + xb) / 2 - width(lab, 17) / 2 - 10, y - h * 0.75 - 16, width(lab, 17) + 20, 28, "nt-bubble", 8)
    s.text((xa + xb) / 2, y - h * 0.75 + 4, lab, "dg-code", "middle")
arc("American Airlines", "AMR Corp.", "part_of", h=80)
arc("Tim Wagner", "American Airlines", "works_for", h=110)
arc("United", "UAL Corp.", "part_of", h=70)
s.both(20, 216, "ผลลัพธ์: triplet (head, relation, tail)", "Output: triplets (head, relation, tail)", "pl-label")
TR = [("American Airlines", "part_of", "AMR Corp."), ("Tim Wagner", "works_for", "American Airlines"), ("United", "part_of", "UAL Corp.")]
for k, (h, r, t_) in enumerate(TR):
    s.box(20, 232 + k * 44, 640, 36, "ml-cell", 8)
    s.text(36, 256 + k * 44, f"({h}, {r}, {t_})", "dg-code")
s.box(690, 232, 470, 124, "sw-warn-box", 12)
s.both(706, 262, "ทิศทางสำคัญ", "Direction matters", "pl-label")
s.text(706, 294, "(AMR Corp., part_of, American Airlines)", "dg-code")
s.both(706, 330, "✗ กลับหัว: นับว่าผิด", "✗ reversed: counts as wrong", "ml-neg")
PIPE = [("1 NER", "1 NER", "หาชื่อ", "find entities"), ("2 จับคู่", "2 Pair", "ทุกคู่ชื่อ", "pair them"),
        ("3 จำแนก", "3 Classify", "แต่ละคู่: ความสัมพันธ์?", "classify each pair"), ("4 Triplets", "4 Triplets", "หรือ no_relation", "or no_relation")]
for k, (nth, nen, th, en) in enumerate(PIPE):
    x0 = 20 + k * 290
    s.box(x0, 380, 270, 64, "nt-band-a", 12)
    s.both(x0 + 16, 406, nth, nen, "pl-label")
    s.both(x0 + 16, 432, th, en, "pl-note")
    if k < 3:
        s.arrow(x0 + 272, 412, x0 + 288, 412)
s.save("l15-relations.svg", 460)
