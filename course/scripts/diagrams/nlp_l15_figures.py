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


def bubble(s, W, text, y=8, w=None):
    w = w or width(text) + 60
    s.box(W / 2 - w / 2, y, w, 46, "nt-bubble", 23)
    s.text(W / 2, y + 30, text, "pl-text", "middle")


W = 1180

# ---------------------------------------------------------------- 1. hook: an announcement as text vs as a table
s = Svg(W, "From text to a table. The airline announcement is three sentences of text: a computer cannot sort or count what it says. "
           "Information extraction turns it into a table: United Airlines, parent UAL Corp., raised fares by $6 per round trip; "
           "American Airlines, parent AMR Corp., matched the move, spokesman Tim Wagner. Three steps get there: tag each word, "
           "find the names (NER), link the names (relation extraction).")
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
s.both(566, 344, "3 ขั้นที่ทำให้ได้ตารางนี้:", "Three steps get there:", "pl-label")
s.both(566, 374, "1 ติดป้ายทุกคำ  →  2 หาชื่อ (NER)  →  3 โยงชื่อ (RE)", "1 tag each word → 2 find the names (NER) → 3 link them (RE)", "ml-ok")
s.save("l15-hook.svg", 456)


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
    ("7 NER ด้วย LLM", "7 NER with LLMs", "ขอ JSON แล้วตรวจ", "Ask for JSON, then check it", "ชนิดไหนก็ได้ ไม่ต้องเทรน ✓", "any types, no training ✓"),
    ("8 Relation extraction", "8 Relation extraction", "โยงชื่อเป็นคู่", "Link the names in pairs", "(American Airlines, part_of, AMR Corp.) ✓", "(American Airlines, part_of, AMR Corp.) ✓"),
]
s = Svg(W, "Lesson map: one airline announcement followed through eight parts: the problem (facts buried in text), sequence tagging "
           "(one label per word), part-of-speech tagging (is 'refuse' a noun or a verb?), statistical taggers (a CRF tags 'the refuse "
           "permit' as nouns, 96.2% accuracy), neural taggers (about 97%), named entities with BIO tags, NER with LLMs, and "
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

# ---------------------------------------------------------------- 4. four tagging tasks
s = Svg(W, "Four tasks that are all sequence tagging. Part-of-speech: I will book a flight → PRP MD VB DT NN. Named entities with BIO: "
           "spokesman Tim Wagner said → O B-PER I-PER O. Chunking: They refuse to permit us → B-NP B-VP I-VP I-VP B-NP. Grammar "
           "correction: He eat food → KEEP, REPLACE with eats, KEEP.")
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
s.both(20, 438, "ทุกงาน: input n คำ → output n ป้าย และป้ายขึ้นกับป้ายข้าง ๆ (เช่น I-PER ต้องตามหลัง B-PER)",
       "Every task: n words in → n labels out, and labels depend on their neighbours (I-PER must follow B-PER)", "ml-ok")
s.save("l15-tasks.svg", 454)

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
           "words (pronouns, determiners, particles) are a small fixed set. Thai uses its own tagset, such as ORCHID (about 47 tags).")
bubble(s, W, "They refuse to permit us to obtain the refuse permit .", w=660)
x = 128
s.both(20, 116, "คำ", "word", "pl-note")
s.both(20, 170, "Penn Treebank", "Penn Treebank", "pl-note")
s.both(20, 222, "Universal POS", "Universal POS", "pl-note")
for w_, ptb, upos in SENT:
    cw = max(width(w_), width(ptb, 17), width(upos, 17)) + 18
    op = upos in OPEN
    s.box(x, 92, cw, 36, "sw-chip-warn" if op else "ml-cell", 8)
    s.text(x + cw / 2, 116, w_, "pl-text", "middle")
    s.box(x, 148, cw, 32, "nt-bubble", 8)
    s.text(x + cw / 2, 170, ptb, "dg-code", "middle")
    s.box(x, 200, cw, 32, "nt-band-a" if op else "ml-cell", 8)
    s.text(x + cw / 2, 222, upos, "dg-code", "middle")
    x += cw + 8
TS = [("Penn Treebank (PTB)", "≈ 45 ป้าย กริยาอย่างเดียวมี 6 ป้าย", "≈ 45 tags; 6 just for verbs"),
      ("Universal POS (UD)", "17 ป้าย ใช้ได้ทุกภาษา", "17 tags, the same for every language"),
      ("ORCHID (ไทย)", "≈ 47 ป้าย คลังภาษาไทยรุ่นแรก ๆ", "≈ 47 tags, an early Thai corpus")]
for k, (n, th, en) in enumerate(TS):
    x0 = 20 + k * 384
    s.box(x0, 256, 372, 84, "ml-cell", 12)
    s.text(x0 + 16, 286, n, "pl-label")
    s.both(x0 + 16, 316, th, en, "pl-note")
s.box(20, 360, 18, 18, "sw-chip-warn", 4)
s.both(46, 375, "open class: นาม กริยา คุณศัพท์ กริยาวิเศษณ์ มีคำใหม่เพิ่มได้เรื่อย ๆ", "open class: nouns, verbs, adjectives, adverbs; new words keep arriving", "pl-text")
s.box(20, 392, 18, 18, "ml-cell", 4)
s.both(46, 407, "closed class: คำไวยากรณ์ชุดเล็ก ๆ (the, to, they) แทบไม่เปลี่ยน", "closed class: a small fixed set of function words (the, to, they)", "pl-text")
s.save("l15-tagsets.svg", 424)

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

# ---------------------------------------------------------------- 8. HMM: hidden tags emit words (slide corpus, real probabilities)
s = Svg(W, "A hidden Markov model for 'Will can spot Mary'. The tags are hidden (white circles); the words are seen (dark boxes). "
           "Transition probabilities link one tag to the next: start to N 3/4, N to M 3/9, M to V 3/4, V to N 4/4, N to end 4/9. "
           "Emission probabilities give a word from its tag: Will from N 1/9, can from M 1/4, spot from V 1/4, Mary from N 4/9. "
           "Multiplying all of them gives P = 1/3888, about 0.000257.")
s.both(20, 30, "เรียนจาก 4 ประโยค: Mary Jane can see Will · Spot will see Mary · Will Jane spot Mary · Mary will pat Spot",
       "Learned from 4 sentences: Mary Jane can see Will · Spot will see Mary · Will Jane spot Mary · Mary will pat Spot", "pl-note")
TAGS = ["N", "M", "V", "N"]; WORDS = ["Will", "can", "spot", "Mary"]
TR = ["3/4", "3/9", "3/4", "4/4"]; EM = ["1/9", "1/4", "1/4", "4/9"]
xs = [240 + k * 210 for k in range(4)]
s.box(60, 92, 90, 50, "ml-cell", 25); s.text(105, 123, "start", "pl-text", "middle")
s.box(1060, 92, 90, 50, "ml-cell", 25); s.text(1105, 123, "end", "pl-text", "middle")
prev = 150
for k, (x, tg, w_) in enumerate(zip(xs, TAGS, WORDS)):
    s.raw(f'<circle cx="{x}" cy="117" r="34" class="nt-bubble"/>')
    s.text(x, 125, tg, "pl-label", "middle")
    s.arrow(prev + 2, 117, x - 36, 117)
    s.box((prev + x - 36) / 2 - 26, 76, 52, 26, "ml-cell", 6)
    s.text((prev + x - 36) / 2, 95, TR[k], "dg-code", "middle")
    prev = x + 34
    s.arrow(x, 152, x, 222)
    s.box(x + 8, 172, 52, 26, "ml-cell", 6); s.text(x + 34, 191, EM[k], "dg-code", "middle")
    s.box(x - 50, 226, 100, 44, "nt-out", 10)
    s.text(x, 254, w_, "pl-label", "middle")
s.arrow(prev + 2, 117, 1058, 117)
s.box((prev + 1058) / 2 - 26, 76, 52, 26, "ml-cell", 6); s.text((prev + 1058) / 2, 95, "4/9", "dg-code", "middle")
s.both(20, 318, "ซ่อนอยู่ (hidden): ป้าย t  ·  มองเห็น (observed): คำ w", "hidden: the tags t  ·  observed: the words w", "pl-text")
s.both(20, 350, "transition P(tᵢ | tᵢ₋₁): ป้ายนี้ตามหลังป้ายก่อนหน้าบ่อยแค่ไหน (N→M = 3 จาก 9)",
       "transition P(tᵢ | tᵢ₋₁): how often this tag follows the last one (N→M = 3 of 9)", "pl-text")
s.both(20, 380, "emission P(wᵢ | tᵢ): ป้ายนี้ “ปล่อย” คำนี้บ่อยแค่ไหน (N → Mary = 4 จาก 9)",
       "emission P(wᵢ | tᵢ): how often this tag produces this word (N → Mary = 4 of 9)", "pl-text")
s.text(20, 420, "P(T, W) = 3/4 · 1/9 · 3/9 · 1/4 · 3/4 · 1/4 · 4/4 · 4/9 · 4/9 = 1/3888 ≈ 0.000257", "pl-label")
s.save("l15-hmm.svg", 440)

# ---------------------------------------------------------------- 9. Viterbi trellis (real values, slide corpus)
V = {("N", 0): "1/12", ("M", 0): "3/16", ("V", 0): "0", ("N", 1): "0", ("M", 1): "1/144", ("V", 1): "0",
     ("N", 2): "1/2592", ("M", 2): "0", ("V", 2): "1/768", ("N", 3): "1/1728", ("M", 3): "0", ("V", 3): "0"}
BEST = [("N", 0), ("M", 1), ("V", 2), ("N", 3)]
s = Svg(W, "Viterbi decoding of 'Will can spot Mary'. Each column keeps, for each tag, only the best score of any path that ends "
           "there. After Will, M scores 3/16 and N only 1/12, but M cannot be followed by M, so the best path to can goes through "
           "N (1/144). The best path is N M V N, score 1/1728 times 4/9 for the end = 1/3888. Trying every path takes 3 to the 4th "
           "= 81 paths; Viterbi needs 4 × 3 × 3 = 36 steps. For 20 words and 45 tags: 1.2 × 10^33 paths versus 40,500 steps.")
TG = ["N", "M", "V"]
cx = [260 + k * 230 for k in range(4)]; cy = {"N": 110, "M": 200, "V": 290}
for k, w_ in enumerate(WORDS):
    s.text(cx[k], 50, w_, "pl-label", "middle")
for t_ in TG:
    s.text(150, cy[t_] + 6, t_, "pl-label", "end")
for (a, i), (b, j) in zip(BEST, BEST[1:]):
    s.raw(f'<path d="M{cx[i] + 52} {cy[a]} L{cx[j] - 52} {cy[b]}" class="pl-line" style="stroke-width:3"/>')
s.raw(f'<path d="M{cx[0] + 52} {cy["M"]} L{cx[1] - 52} {cy["M"]}" class="pl-line" stroke-dasharray="6 5"/>')
s.both((cx[0] + cx[1]) / 2, cy["M"] + 24, "M→M = 0", "M→M = 0", "ml-neg", "middle")
for (t_, k), v in V.items():
    best = (t_, k) in BEST
    s.box(cx[k] - 52, cy[t_] - 22, 104, 44, "sw-chip-warn" if best else ("ml-cell" if v != "0" else "pl-chip-del"), 10)
    s.text(cx[k], cy[t_] + 6, v, "pl-label" if v != "0" else "pl-note", "middle")
s.both(cx[0], 340, "M นำอยู่ (3/16)", "M leads (3/16)", "pl-note", "middle")
s.both(cx[0], 368, "แต่ไปต่อไม่ได้", "but goes nowhere", "ml-neg", "middle")
s.both(20, 412, "เส้นทางที่ดีที่สุด: N M V N = 1/1728 × 4/9 (ไป end) = 1/3888 ✓", "Best path: N M V N = 1/1728 × 4/9 (to end) = 1/3888 ✓", "ml-ok")
s.box(20, 432, 560, 92, "sw-warn-box", 12)
s.both(36, 462, "✗ ลองทุกเส้นทาง: Kⁿ", "✗ Try every path: Kⁿ", "pl-label")
s.both(36, 490, "3 ป้าย 4 คำ: 3⁴ = 81 เส้นทาง", "3 tags, 4 words: 3⁴ = 81 paths", "pl-text")
s.both(36, 514, "45 ป้าย 20 คำ: 45²⁰ ≈ 1.2 × 10³³", "45 tags, 20 words: 45²⁰ ≈ 1.2 × 10³³", "ml-neg")
s.box(600, 432, 560, 92, "nt-band-a", 12)
s.both(616, 462, "✓ Viterbi: n · K²", "✓ Viterbi: n · K²", "pl-label")
s.both(616, 490, "3 ป้าย 4 คำ: 4 × 3 × 3 = 36 ขั้น", "3 tags, 4 words: 4 × 3 × 3 = 36 steps", "pl-text")
s.both(616, 514, "45 ป้าย 20 คำ: 20 × 45² = 40,500 ขั้น", "45 tags, 20 words: 20 × 45² = 40,500 steps", "ml-ok")
s.save("l15-viterbi.svg", 540)

# ---------------------------------------------------------------- 10. HMM vs CRF on "the refuse permit" (real weights)
s = Svg(W, "HMM versus CRF on 'obtain the refuse permit'. The HMM generates each word from its tag alone and looks back one tag, "
           "so it tags refuse JJ and permit NNS, both wrong. The CRF scores features of the whole sentence with learned weights: "
           "for refuse as NN, the features give 6.77 and the tag pair DT then NN adds 2.37, total 9.14, against 6.21 for JJ and 4.23 "
           "for VBP. Normalised, P(NN) = 0.615. Both words come out NN.")
s.box(20, 20, 480, 440, "sw-warn-box", 14)
s.both(40, 52, "✗ HMM: P(T, W)", "✗ HMM: P(T, W)", "pl-label")
s.both(40, 78, "คำขึ้นกับป้ายของตัวเองเท่านั้น", "a word depends only on its own tag;", "pl-note")
s.both(40, 104, "ป้ายดูย้อนแค่ 1 ป้าย", "a tag looks back one tag", "pl-note")
tagged(s, 40, 124, [("the", "DT"), ("refuse", "JJ"), ("permit", "NNS")], hi=(1, 2))
s.both(40, 246, "refuse ไม่เคยเป็นนามใน training", "refuse was never a noun in training", "pl-text")
s.both(40, 272, "(VBP 2 ครั้ง) จึงเดาจาก smoothing", "(VBP twice), so smoothing guesses", "pl-text")
s.both(40, 428, "✗ refuse = JJ, permit = NNS", "✗ refuse = JJ, permit = NNS", "ml-neg")
s.box(520, 20, 640, 440, "nt-band-a", 14)
s.both(540, 52, "✓ CRF: P(T | W) จาก feature ทั้งประโยค", "✓ CRF: P(T | W) from features of the whole sentence", "pl-label")
s.both(540, 78, "คะแนน = Σ λₖ fₖ (น้ำหนัก × feature) แล้ว softmax", "score = Σ λₖ fₖ (weight × feature), then softmax", "pl-note")
FE = [("bias", "+4.09"), ("ends in -se", "+1.71"), ("prev word = the", "+0.95"), ("other features", "+0.02"), ("tag pair DT → NN", "+2.37")]
s.both(540, 116, "refuse เป็น NN:", "refuse as NN:", "pl-label")
for k, (f, w_) in enumerate(FE):
    y = 126 + k * 34
    s.box(540, y, 330, 28, "ml-cell", 8); s.text(552, y + 20, f, "dg-code")
    s.text(940, y + 20, w_, "pl-label", "end")
s.line(540, 298, 950, 298)
s.both(540, 320, "รวม (NN)", "total (NN)", "pl-text"); s.text(940, 320, "9.14", "pl-label", "end")
for k, (lab, v, p) in enumerate([("NN", 9.14, "0.615"), ("JJ", 6.21, "0.349"), ("VBP", 4.23, "")]):
    y = 332 + k * 32
    s.text(580, y + 20, lab, "dg-code", "end")
    s.box(590, y + 4, 300 * v / 9.14, 24, "ml-bar-top" if k == 0 else "ml-bar", 4)
    s.text(590 + 300 * v / 9.14 + 8, y + 22, f"{v}" + (f"  → P = {p}" if p else ""), "pl-note")
s.both(540, 446, "✓ refuse = NN, permit = NN (P = 0.965)", "✓ refuse = NN, permit = NN (P = 0.965)", "ml-ok")
s.save("l15-crf.svg", 474)

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
PIPE = [("1 NER", "หาชื่อ", "find entities"), ("2 จับคู่", "ทุกคู่ชื่อ", "pair them"), ("3 จำแนก", "แต่ละคู่: ความสัมพันธ์?", "classify each pair"), ("4 Triplets", "หรือ no_relation", "or no_relation")]
for k, (n, th, en) in enumerate(PIPE):
    x0 = 20 + k * 290
    s.box(x0, 380, 270, 64, "nt-band-a", 12)
    s.text(x0 + 16, 406, n, "pl-label")
    s.both(x0 + 16, 432, th, en, "pl-note")
    if k < 3:
        s.arrow(x0 + 272, 412, x0 + 288, 412)
s.save("l15-relations.svg", 460)
