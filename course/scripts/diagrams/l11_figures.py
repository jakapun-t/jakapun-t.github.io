"""Draws the lesson 11 (nlp) hook: one search box, four job ads as results, and what keyword
search and semantic search each make of them. The cosine scores are real
(all-MiniLM-L6-v2, the same numbers as the lesson's util.cos_sim cell).

    python3 scripts/diagrams/l11_figures.py courses/nlp/images

Uses the nt-*, pl-*, ml-*, sw-* and hk-* classes in templates/page.css.
"""

import os
import sys
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp/images"
FS = 19


class Svg:
    def __init__(self, w, title):
        self.w, self.title, self.out = w, title, []

    def both(self, x, y, th, en, cls, anchor="start"):
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="th">{escape(th)}</text>')
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="en" lang="en">{escape(en)}</text>')

    def text(self, x, y, s, cls, anchor="start"):
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" lang="en">{escape(s)}</text>')

    def box(self, x, y, w, h, cls, rx=12):
        self.out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}"/>')

    def raw(self, s):
        self.out.append(s)

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


QUERY = "hiring a teacher"
MATCH = set(QUERY.split())
ADS = [
    # text, keyword verdict (th, en, kind), cosine with the query
    ("Hiring a teacher", ("ตรง 3 จาก 3 คำ", "3 of 3 words", "ok"), 1.00),
    ("Teacher wanted", ("ตรง 1 จาก 3 คำ", "1 of 3 words", "part"), 0.61),
    ("Looking for a high school teacher", ("ตรง 2 จาก 3 คำ", "2 of 3 words", "part"), 0.67),
    ("Recruiting secondary school instructor", ("0 คำ · ไม่แสดงเลย", "0 words · never shown", "bad"), 0.58),
]

s = Svg(900, "A search box with 'hiring a teacher' and four job ads that all mean 'we need a teacher'. Keyword search matches 3, 1, 2 and 0 of the query words, so it misses the last ad. Semantic search scores all four as close in meaning: 1.00, 0.61, 0.67 and 0.58.")

# the search box
s.box(20, 16, 600, 58, "ml-cell", rx=29)
s.raw('<circle cx="54" cy="43" r="10" class="nt-arrow"/><path d="M61 50 L69 58" class="nt-arrow"/>')
s.text(84, 51, QUERY, "pl-text")

# the two verdict columns
KX, SX = 640, 805
s.both(KX, 112, "keyword search", "Keyword search", "nt-head", "middle")
s.both(SX, 112, "semantic search", "Semantic search", "nt-head", "middle")
s.both(KX, 132, "(จับคู่คำ)", "(matches words)", "pl-note", "middle")
s.both(SX, 132, "(เทียบความหมาย)", "(compares meaning)", "pl-note", "middle")

y = 148
for text, (vth, ven, kind), cos in ADS:
    # the ad keyword search never shows gets the warning tint
    s.box(20, y, 860, 62, "sw-warn-box" if kind == "bad" else "ml-cell", rx=12)
    # the ad as one line of text (the browser spaces it); shared words in bold blue
    parts = [f'<tspan class="hk-hit">{escape(w)}</tspan>' if w.lower() in MATCH else escape(w) for w in text.split()]
    s.raw(f'<text x="40" y="{y + 39}" class="hk-ad" lang="en">{" ".join(parts)}</text>')
    mark = {"ok": ("✓", "ml-ok"), "part": ("◐", "pl-note"), "bad": ("✗", "sw-warn-text")}[kind]
    s.both(KX, y + 38, f"{mark[0]} {vth}", f"{mark[0]} {ven}", mark[1], "middle")
    s.text(SX, y + 38, f"✓ {cos:.2f}", "ml-ok", "middle")
    y += 74

# the bottom line
s.both(450, y + 30, "ค้นด้วยคำ: ประกาศที่ 4 หายไป · ค้นด้วยความหมาย: ครบทั้ง 4", "Matching words: ad 4 disappears · matching meaning: all 4 found", "nt-band-title", "middle")
s.save("l11-search-hook.svg", y + 46)


# ---------------------------------------------------------------- preprocessing, one sentence
MONO = 0.6 * 19  # IBM Plex Mono advance at 19px: chips can be measured exactly


def chips(s, x, y, words, changed=()):
    for w in words:
        cw = len(w) * MONO + 22
        s.box(x, y - 22, cw, 34, "sw-chip-warn" if w in changed else "pl-chip", rx=8)
        s.raw(f'<text x="{x + cw / 2:g}" y="{y + 1}" class="hk-mono" text-anchor="middle" lang="en">{escape(w)}</text>')
        x += cw + 10


s = Svg(900, "Preprocessing one sentence: lowercase it, cut it into words, then lemmatize. Pancakes, milkshakes and children become pancake, milkshake and child.")
rows = [
    ("ข้อความดิบ", "Raw text", None),
    ("1 ทำเป็นตัวพิมพ์เล็ก", "1 Lowercase", None),
    ("2 ตัดเป็นคำ", "2 Cut into words", ["pancakes", "and", "milkshakes", "for", "children"]),
    ("3 Lemmatize", "3 Lemmatize", ["pancake", "and", "milkshake", "for", "child"]),
]
y = 40
for th, en, words in rows:
    s.both(20, y + 1, th, en, "nt-head")
    if words is None:
        text = "Pancakes and milkshakes for children" if en == "Raw text" else "pancakes and milkshakes for children"
        s.raw(f'<text x="250" y="{y + 1}" class="hk-ad" lang="en">{escape(text)}</text>')
    else:
        chips(s, 250, y, words, changed={"pancake", "milkshake", "child"} if en.startswith("3") else ())
    y += 62
s.both(20, y - 8, "คำที่เปลี่ยนรูป (สีส้ม): ตอนนี้เอกสารที่เขียนว่า children จะตรงกับคำว่า child", "Changed words in orange: now a document that says children matches the word child.", "pl-note")
s.save("l11-preprocess.svg", y + 6)


# ---------------------------------------------------------------- BM25 on "romantic dinner for two"
QWORDS = [("romantic", 0), ("dinner", 0), ("for", 5), ("two", 0)]  # word, descriptions containing it (of 16)
RESULTS = [  # rank, name, description, BM25 score, words (real: bm25.get_scores)
    (1, "Kiddo Cafe", "Pancakes and milkshakes with a play corner for children.", 0.81, 9),
    (2, "Dim Sum Palace", "Steamed dumplings and roast duck for big family tables.", 0.81, 9),
    (3, "Pasta Express", "Quick pasta and pizza counter with cheap set lunches for office workers.", 0.71, 12),
    (4, "Book Nook Cafe", "A quiet cafe with books and power sockets for studying with good coffee.", 0.68, 13),
    (5, "Trattoria Luna", "Candle-lit Italian trattoria with handmade pasta and a quiet terrace for couples.", 0.68, 13),
]

s = Svg(1000, "BM25 on the query 'romantic dinner for two': romantic, dinner and two appear in no description; only 'for' appears, in 5. So the five places that say 'for' come first, the shortest descriptions highest, and the romantic Trattoria Luna ties for 5th.")
s.box(20, 14, 520, 54, "ml-cell", rx=27)
s.raw('<circle cx="52" cy="40" r="9" class="nt-arrow"/><path d="M58 46 L65 53" class="nt-arrow"/>')
s.text(80, 48, "romantic dinner for two", "pl-text")
s.both(20, 104, "แต่ละคำอยู่ในคำอธิบายกี่ร้าน (จาก 16):", "Each query word appears in how many descriptions (of 16):", "nt-head")
x = 20
for w, n in QWORDS:
    cw = len(w) * MONO + 22
    s.box(x, 120, cw, 34, "pl-chip" if n else "pl-chip-del", rx=8)
    s.raw(f'<text x="{x + cw / 2:g}" y="143" class="hk-mono" text-anchor="middle" lang="en">{escape(w)}</text>')
    s.text(x + cw / 2, 178, str(n), "ml-ok" if n else "ml-neg", "middle")
    x += cw + 26
s.both(x + 6, 143, "→ เหลือคำเดียวที่ใช้ให้คะแนน: for", "→ only one word left to score with: for", "pl-note")

s.both(20, 226, "ผลลัพธ์ของ BM25", "BM25 results", "nt-head")
s.both(980, 226, "คะแนน", "score", "nt-head", "end")
y = 240
for rank, name, desc, score, n in RESULTS:
    wanted = name == "Trattoria Luna"
    s.box(20, y, 960, 70, "sw-warn-box" if wanted else "ml-cell", rx=12)
    s.text(40, y + 30, f"{rank}  {name}", "nt-task")
    s.both(40 + len(f"{rank}  {name}") * 11 + 16, y + 30, f"({n} คำ)", f"({n} words)", "pl-note")
    parts = [f'<tspan class="hk-hit">{escape(w)}</tspan>' if w.lower().strip(".") == "for" else escape(w) for w in desc.split()]
    s.raw(f'<text x="40" y="{y + 56}" class="hk-desc" lang="en">{" ".join(parts)}</text>')
    s.box(790, y + 22, 120 * score / 0.81, 22, "ml-bar", rx=4)
    s.text(980, y + 40, f"{score:.2f}", "nt-task", "end")
    if wanted:
        s.both(760, y + 30, "← ร้านที่ผู้ใช้ต้องการ", "← the place the user wants", "sw-warn-text", "end")
    y += 80
s.both(20, y + 22, "ชนะเพราะคำว่า for และคำอธิบายสั้น ไม่ใช่เพราะโรแมนติก", "They win on the word for and a short description, not on romance.", "nt-band-title")
s.save("l11-bm25-romantic.svg", y + 40)


# ---------------------------------------------------------------- WordNet around "car" (real: nltk wordnet 3.0)
def chip_row(s, x, y, words, cls="pl-chip"):
    for w in words:
        cw = len(w) * MONO + 22
        s.box(x, y - 22, cw, 34, cls, rx=8)
        s.raw(f'<text x="{x + cw / 2:g}" y="{y + 1}" class="hk-mono" text-anchor="middle" lang="en">{escape(w)}</text>')
        x += cw + 10
    return x


def arrow_up(s, x, y1, y2):
    s.raw(f'<path d="M{x} {y1} L{x} {y2}" class="nt-arrow"/><path d="M{x - 7} {y2 + 9} L{x} {y2} L{x + 7} {y2 + 9}" class="nt-arrow"/>')


s = Svg(900, "WordNet around the word car. The synset car.n.01 holds the synonyms car, auto, automobile, machine and motorcar. It is a kind of motor vehicle (broader), and sedan, cab, convertible, jeep and minivan are kinds of it (narrower, 31 in all). The word car has 5 senses, each its own synset: a motor car, a railcar, an airship gondola, an elevator car and a cable car.")
# broader
s.both(30, 24, "กว้างกว่า (hypernym)", "Broader (hypernym)", "nt-head")
s.box(30, 34, 230, 46, "ml-cell", rx=10)
s.raw('<text x="145" y="64" class="hk-mono" text-anchor="middle" lang="en">motor vehicle</text>')
s.both(276, 64, "… ขึ้นไปถึง vehicle, entity", "… up to vehicle, entity", "pl-note")
arrow_up(s, 145, 116, 82)
s.both(160, 104, "เป็นชนิดหนึ่งของ", "is a kind of", "pl-note")
# the synset
s.box(20, 118, 560, 128, "nt-out", rx=14)
s.both(40, 148, "synset car.n.01: คำพ้องความหมาย อยู่กล่องเดียวกัน", "synset car.n.01: synonyms share one box", "nt-task")
chip_row(s, 40, 190, ["car", "auto", "automobile", "machine", "motorcar"])
s.both(40, 232, "\"รถยนต์สี่ล้อ ปกติใช้เครื่องยนต์สันดาปภายใน\"", "\"a motor vehicle with four wheels\"", "hk-desc")
# narrower
arrow_up(s, 145, 296, 248)
s.both(160, 278, "เป็นชนิดหนึ่งของ", "is a kind of", "pl-note")
chip_row(s, 30, 324, ["sedan", "cab", "convertible", "jeep", "minivan"], "ml-cell")
s.both(30, 370, "แคบกว่า (hyponym) · และอีก 26 คำ", "Narrower (hyponyms) · and 26 more", "nt-head")

# the other senses of the word
s.both(610, 24, "คำว่า car มี 5 ความหมาย", "car has 5 senses", "nt-head")
SENSES = [("car.n.01", "auto, automobile", "รถยนต์", "a motor car", True),
          ("car.n.02", "railcar", "ตู้รถไฟ", "a train carriage", False),
          ("car.n.03", "gondola", "ห้องใต้เรือเหาะ", "under an airship", False),
          ("car.n.04", "elevator car", "ห้องลิฟต์", "a lift cabin", False),
          ("cable_car.n.01", "cable car", "กระเช้า", "a cable car", False)]
y = 38
for name, syn, th, en, this in SENSES:
    s.box(610, y, 270, 58, "nt-out" if this else "ml-cell", rx=10)
    s.text(626, y + 24, name, "hk-mono")
    s.both(626, y + 47, f"{syn} · {th}", f"{syn} · {en}", "pl-note")
    y += 66
s.both(610, y + 16, "ขยายด้วยทุก synset", "Expanding with every synset", "sw-warn-text")
s.both(610, y + 38, "= ได้ทุกความหมายปนกัน", "mixes all 5 meanings.", "sw-warn-text")
s.save("l11-wordnet.svg", max(y + 50, 384))


# ---------------------------------------------------------------- the lesson map (big picture)
# Results on the running example are real: BM25 top 1 for "romantic dinner for two" is a 0.81 tie
# (Kiddo Cafe / Dim Sum Palace); WordNet's romantic synonyms (amorous, amatory) are in no description; dense
# retrieval puts it first at 0.447; hybrid search on "pasta" ranks it 2nd, ahead of the noodle place; the learned
# ranker of L11-S23 (5 features) scores it 0.598, first, and Kiddo Cafe last of the 5 candidates.
s = Svg(900, "Lesson map. The problem: keyword search answers 'romantic dinner for two' with Kiddo Cafe. Four ways to find what the user meant: 2 fix the query, 3 meaning as features, 4 combine both, 5 rank better with every score. Each shows its tools and its result on the restaurant data.")
s.box(20, 16, 300, 54, "ml-cell", rx=27)
s.raw('<circle cx="50" cy="42" r="9" class="nt-arrow"/><path d="M56 48 L63 55" class="nt-arrow"/>')
s.text(76, 50, "romantic dinner for two", "pl-text")
s.raw('<path d="M330 43 L366 43" class="nt-arrow"/><path d="M358 36 L367 43 L358 50" class="nt-arrow"/>')
s.box(376, 10, 504, 66, "sw-warn-box", rx=12)
s.both(394, 38, "1 ปัญหา: keyword search ตอบ Kiddo Cafe ✗", "1 The problem: keyword search answers Kiddo Cafe ✗", "nt-task")
s.both(394, 64, "romantic, dinner, two ไม่อยู่ในคำอธิบายร้านไหนเลย", "romantic, dinner and two match no description", "pl-note")
s.both(450, 112, "4 วิธีให้การค้นหาเจอสิ่งที่ผู้ใช้หมายถึง", "Four ways to find what the user meant", "nt-head", "middle")
WAYS = [
    ("2 แก้ query", "2 Fix the query", "เพิ่มคำที่ผู้ใช้หมายถึง", "Add the words the user meant",
     "WordNet synonyms · how far to expand", "romantic + amorous, amatory: ยังไม่ตรงร้านไหน ✗", "romantic + amorous, amatory: still no match ✗"),
    ("3 ความหมายเป็น feature", "3 Meaning as features", "โมเดลเปลี่ยนข้อความเป็น vector แล้วเทียบ vector", "A model turns text into vectors; compare those",
     "embeddings · cosine · dense retrieval", "Trattoria Luna อันดับ 1 (0.447) ✓", "Trattoria Luna first (0.447) ✓"),
    ("4 รวมสองวิธี", "4 Combine both", "รวมรายการผลของคำค้นกับของ vector", "Merge the keyword and the vector lists",
     "hybrid search (reciprocal rank fusion)", "pasta: Luna อันดับ 2 นำหน้าร้านก๋วยเตี๋ยว ✓", "pasta: Luna 2nd, ahead of the noodle place ✓"),
    ("5 จัดอันดับให้ดีขึ้น", "5 Rank better", "ให้คะแนนด้วยทุกสัญญาณ น้ำหนักเรียนจากการคลิก", "Score with every signal; learn weights from clicks",
     "query tags · two stages · learning to rank", "ทั้ง 5 คะแนน: Luna อันดับ 1, Kiddo Cafe ท้ายสุด ✓", "all 5 scores: Luna first, Kiddo Cafe last ✓"),
]
for k, (tth, ten, cth, cen, tools, exth, exen) in enumerate(WAYS):
    x = 20 + (k % 2) * 440
    y = 128 + (k // 2) * 162
    s.box(x, y, 420, 148, "ml-cell", rx=14)
    s.both(x + 20, y + 34, tth, ten, "nt-task")
    s.both(x + 20, y + 62, cth, cen, "hk-desc")
    s.text(x + 20, y + 92, tools, "pl-note")
    s.both(x + 20, y + 128, exth, exen, "ml-neg" if "✗" in exen else "ml-ok")
s.both(450, 466, "6 เลือกเครื่องมือให้ถูกงาน แล้วทบทวนคำศัพท์", "6 Choose the right tool for each search, then review", "pl-note", "middle")
s.save("l11-map-lesson.svg", 484)


# ---------------------------------------------------------------- two-stage search (like the deck's slide 29)
# Real numbers: area = Silom keeps 4 of the 16 places; the weighted sum of L11-S09 (0.5·text + 1.0·rating
# − 1.0·distance_km − 0.5·price, text = BM25 of "romantic pasta cheap") ranks them 5.27, 4.01, 2.90, 2.90.
s = Svg(900, "Two-stage search on the restaurant app. Stage 1, fast and rough: the area = Silom filter keeps 4 of the 16 places (a real app: hundreds out of millions). Stage 2, slow and careful: ranking features from the query, the user and the place score the 4: Pasta Express 5.27, Trattoria Luna 4.01, Book Nook Cafe 2.90, Curry House 2.90.")


def trapezoid(x, y, w, h, shrink, cls):
    s.raw(f'<path d="M{x} {y} L{x + w} {y + shrink} L{x + w} {y + h - shrink} L{x} {y + h} Z" class="{cls}"/>')


def arrow_right(x1, x2, y):
    s.raw(f'<path d="M{x1} {y} L{x2} {y}" class="nt-arrow"/><path d="M{x2 - 9} {y - 7} L{x2} {y} L{x2 - 9} {y + 7}" class="nt-arrow"/>')


def arrow_down(x, y1, y2):
    s.raw(f'<path d="M{x} {y1} L{x} {y2}" class="nt-arrow"/><path d="M{x - 7} {y2 - 9} L{x} {y2} L{x + 7} {y2 - 9}" class="nt-arrow"/>')


Y = 150  # middle line of the pipeline
# the items
for k in range(3):
    s.box(20 + k * 7, Y - 46 + k * 7, 120, 70, "ml-cell", rx=10)
s.both(94, Y - 2, "ร้าน 16 ร้าน", "16 places", "nt-task", "middle")
s.both(94, Y + 22, "(แอปจริง: เป็นล้าน)", "(real app: millions)", "pl-note", "middle")
arrow_right(160, 205, Y)
# stage 1
trapezoid(210, Y - 78, 170, 156, 34, "ml-cell-b")
s.both(295, Y - 22, "ขั้นที่ 1", "Stage 1", "nt-task", "middle")
s.both(295, Y + 4, "หาตัวเลือก", "find candidates", "hk-desc", "middle")
s.both(295, Y + 28, "เร็ว หยาบ", "fast, rough", "pl-note", "middle")
s.text(295, Y + 104, "area = Silom", "hk-mono", "middle")
arrow_right(388, 450, Y)
s.both(419, Y - 12, "4 ร้าน", "4 left", "pl-note", "middle")
# inputs to stage 2
for x, th, en, th2, en2 in [(420, "query", "query", "คะแนน text", "text score"),
                             (545, "ผู้ใช้", "user", "ระยะทาง", "distance"),
                             (670, "ร้าน", "place", "ดาว ราคา", "rating, price")]:
    s.box(x, 6, 115, 54, "nt-bubble", rx=10)
    s.both(x + 57, 28, th, en, "nt-task", "middle")
    s.both(x + 57, 50, th2, en2, "pl-note", "middle")
s.raw(f'<path d="M477 60 L520 {Y - 52}" class="nt-arrow"/><path d="M602 60 L560 {Y - 52}" class="nt-arrow"/>')
s.raw(f'<path d="M727 60 L585 {Y - 50}" class="nt-arrow"/>')
# stage 2
trapezoid(460, Y - 62, 170, 124, 26, "sw-chip-warn")
s.both(545, Y - 14, "ขั้นที่ 2", "Stage 2", "nt-task", "middle")
s.both(545, Y + 10, "จัดอันดับ", "rank", "hk-desc", "middle")
s.both(545, Y + 32, "ช้า ละเอียด", "slow, careful", "pl-note", "middle")
s.both(545, Y + 88, "ranking feature", "ranking features", "pl-note", "middle")
arrow_right(638, 666, Y)
# results
s.box(672, Y - 70, 218, 160, "nt-out", rx=12)
s.both(781, Y - 44, "ผลลัพธ์ที่แสดง", "results shown", "nt-head", "middle")
for k, (name, score) in enumerate([("Pasta Express", "5.27"), ("Trattoria Luna", "4.01"), ("Book Nook Cafe", "2.90"), ("Curry House", "2.90")]):
    yy = Y - 14 + k * 26
    s.text(686, yy, f"{k + 1} {name}", "hk-desc")
    s.text(878, yy, score, "pl-note", "end")
s.save("l11-two-stage.svg", 262)


# ---------------------------------------------------------------- part 3: meaning as features (pipeline)
# Real values: all-MiniLM-L6-v2, normalized; Trattoria Luna's vector starts -0.057, -0.006, 0.018, 0.085;
# its cosine with "romantic dinner for two" is 0.447, the highest of the 16 places.
s = Svg(900, "The part 3 pipeline. Step 1, encode: a model turns Trattoria Luna's description into a vector of 384 numbers, its features. Step 2, compare: cosine with the query's vector gives 0.447. Step 3, search: dense retrieval ranks all 16 places by that score, and Trattoria Luna comes first.")
BOX = [  # x, title th/en, lines th, lines en
    (20, "ข้อความ", "Text", ["Candle-lit Italian", "trattoria … for", "couples."], ["Candle-lit Italian", "trattoria … for", "couples."]),
    (200, "Encoder", "Encoder", ["โมเดล", "all-MiniLM-L6-v2"], ["a model:", "all-MiniLM-L6-v2"]),
    (380, "Vector (feature)", "Vector (features)", ["−0.057, −0.006,", "0.018, 0.085, …", "ตัวเลข 384 ตัว"], ["−0.057, −0.006,", "0.018, 0.085, …", "384 numbers"]),
    (560, "เทียบ", "Compare", ["cosine กับ vector", "ของ query", "= 0.447"], ["cosine with the", "query's vector", "= 0.447"]),
    (740, "ค้นหา", "Search", ["เรียงทั้ง 16 ร้าน", "Trattoria Luna", "อันดับ 1 ✓"], ["rank all 16:", "Trattoria Luna", "comes first ✓"]),
]
# the three steps above the boxes
s.box(20, 10, 520, 38, "ml-cell-b", rx=10)
s.both(280, 35, "ขั้นที่ 1 · encode: ข้อความ → vector", "Step 1 · encode: text → vector", "nt-task", "middle")
s.box(560, 10, 160, 38, "ml-cell-b", rx=10)
s.both(640, 35, "ขั้นที่ 2 · เทียบ", "Step 2 · compare", "nt-task", "middle")
s.box(740, 10, 140, 38, "ml-cell-b", rx=10)
s.both(810, 35, "ขั้นที่ 3 · ค้นหา", "Step 3 · search", "nt-task", "middle")
for k, (x, tth, ten, lth, len_) in enumerate(BOX):
    w = 140 if k == 4 else 160
    s.box(x, 62, w, 134, "nt-out" if k == 2 else "ml-cell", rx=12)
    s.both(x + w / 2, 90, tth, ten, "nt-task", "middle")
    for j, (a, b) in enumerate(zip(lth, len_)):
        s.both(x + w / 2, 118 + j * 24, a, b, "pl-note", "middle")
    if k < 4:
        nx = BOX[k + 1][0]
        s.raw(f'<path d="M{x + w + 2} 129 L{nx - 3} 129" class="nt-arrow"/><path d="M{nx - 10} 123 L{nx - 3} 129 L{nx - 10} 135" class="nt-arrow"/>')
s.both(280, 226, "word embedding · sentence encoder", "word embeddings · sentence encoder", "pl-note", "middle")
s.text(640, 226, "cosine similarity", "pl-note", "middle")
s.text(810, 226, "dense retrieval", "pl-note", "middle")
s.save("l11-features-pipeline.svg", 242)


# ---------------------------------------------------------------- hybrid search: reciprocal rank fusion on "pasta"
# Real lists (hybrid_search in L11-S18, top 5 of each, scores of 0 dropped): BM25 finds Pasta Express and
# Trattoria Luna; dense retrieval ranks Pasta Express, Pa Daeng Noodles, Trattoria Luna, Il Fiore, Som Tam Corner.
s = Svg(900, "Hybrid search on 'pasta' with reciprocal rank fusion. Each list gives a place 1/(60 + rank) points: BM25 gives Pasta Express 1/61 and Trattoria Luna 1/62; dense retrieval gives 1/61 to 1/65 to its five places. Adding the points: Pasta Express 0.0328, Trattoria Luna 0.0320, Pa Daeng Noodles 0.0161, Il Fiore 0.0156, Som Tam Corner 0.0154.")
BM = [("Pasta Express", 1), ("Trattoria Luna", 2)]
DE = [("Pasta Express", 1), ("Pa Daeng Noodles", 2), ("Trattoria Luna", 3), ("Il Fiore", 4), ("Som Tam Corner", 5)]
pts = lambda r: 1 / (60 + r)
tot = {}
for lst in (BM, DE):
    for n, r in lst:
        tot[n] = tot.get(n, 0) + pts(r)
order = sorted(tot, key=lambda n: -tot[n])
both = {n for n, _ in BM} & {n for n, _ in DE}

s.box(20, 10, 200, 46, "ml-cell", rx=23)
s.raw('<circle cx="46" cy="33" r="8" class="nt-arrow"/><path d="M52 39 L58 45" class="nt-arrow"/>')
s.text(70, 40, "pasta", "pl-text")
s.both(240, 40, "→ ค้น 2 วิธี แต่ละรายการให้คะแนน 1 / (60 + อันดับ)", "→ two searches; each list gives a place 1 / (60 + rank) points", "pl-note")

def col(x, w, th, en, rows, y0=88):
    s.both(x + 10, y0, th, en, "nt-head")
    pos = {}
    for k, (n, r) in enumerate(rows):
        y = y0 + 16 + k * 58
        s.box(x, y, w, 48, "nt-out" if n in both else "ml-cell", rx=10)
        s.text(x + 14, y + 22, f"{r}  {n}", "hk-desc")
        s.text(x + 14, y + 41, f"1/{60 + r} = {pts(r):.4f}", "pl-note")
        pos[n] = (x, y + 24)
    return pos

pb = col(20, 230, "Keyword search (BM25)", "Keyword search (BM25)", BM)
s.both(30, 236, "ร้านอื่นได้ 0 คะแนน", "The others score 0,", "pl-note")
s.both(30, 258, "จึงไม่อยู่ในรายการนี้", "so not in this list", "pl-note")
pd_ = col(280, 250, "Dense retrieval", "Dense retrieval", DE)
# the fused list
x0, w0 = 580, 300
s.both(x0 + 10, 88, "Hybrid: บวกคะแนนของร้านเดียวกัน", "Hybrid: add each place's points", "nt-head")
for k, n in enumerate(order):
    y = 104 + k * 58
    s.box(x0, y, w0, 48, "nt-out" if n in both else "ml-cell", rx=10)
    s.text(x0 + 14, y + 22, f"{k + 1}  {n}", "nt-task")
    parts = [f"{pts(r):.4f}" for lst in (BM, DE) for nn, r in lst if nn == n]
    s.text(x0 + 14, y + 41, (" + ".join(parts) + f" = {tot[n]:.4f}") if len(parts) > 1 else f"{tot[n]:.4f}", "pl-note")
    if n in both:
        s.both(x0 + w0 - 12, y + 22, "✓ ทั้งสองรายการ", "✓ both lists", "ml-ok", "end")
s.both(450, 420, "อยู่ในทั้งสองรายการ = ได้คะแนนสองทาง: Trattoria Luna แซงร้านก๋วยเตี๋ยวที่มีแค่ dense ชอบ",
       "In both lists = points twice: Trattoria Luna passes the noodle place that only dense retrieval liked", "nt-task", "middle")
s.save("l11-hybrid-rrf.svg", 438)


# ---------------------------------------------------------------- the whole search: hybrid candidates, learned ranker
# Real numbers for "romantic dinner for two" (L11-S23): hybrid_search(k=5) gives the 5 candidates and their RRF
# points; the pointwise LinearRegression on l11_clicks.csv (21 rows) learns the 5 weights; ltr.predict scores them.
s = Svg(900, "The whole search for 'romantic dinner for two'. Stage 1, hybrid search: BM25 and dense retrieval merged by reciprocal rank fusion keep 5 candidates, Trattoria Luna first. Stage 2, the learned ranker: weights text +0.063, dense +0.694, rating +0.517, distance -0.075, price -0.145. Results: Trattoria Luna 0.598, Pasta Express 0.329, Dim Sum Palace 0.092; Kiddo Cafe, keyword search's answer, comes last at -0.176.")
s.box(20, 10, 300, 46, "ml-cell", rx=23)
s.raw('<circle cx="46" cy="33" r="8" class="nt-arrow"/><path d="M52 39 L58 45" class="nt-arrow"/>')
s.text(70, 40, "romantic dinner for two", "pl-text")
s.both(340, 40, "→ (แก้ query ก่อนได้: ขยายคำ ติดป้าย) → ค้น 2 ขั้น", "→ (fix the query first if needed: expansion, tags) → two stages", "pl-note")
COLS = [
    (20, "ขั้นที่ 1 · hybrid search", "Stage 1 · hybrid search", "BM25 + dense รวมด้วย RRF", "BM25 + dense, merged by RRF",
     [("1 Trattoria Luna", "0.0320", True), ("2 Kiddo Cafe", "0.0164", False), ("3 Dim Sum Palace", "0.0161", False),
      ("4 Il Fiore", "0.0161", False), ("5 Pasta Express", "0.0159", False)]),
    (320, "ขั้นที่ 2 · ตัวจัดอันดับที่เรียนมา", "Stage 2 · learned ranker", "feature 5 ตัว × น้ำหนักที่เรียน", "5 features × learned weights",
     [("text", "+0.063", False), ("dense", "+0.694", True), ("rating", "+0.517", False), ("distance_km", "−0.075", False), ("price", "−0.145", False)]),
    (620, "ผลลัพธ์ที่แสดง", "Results shown", "score = b + Σ w · feature", "score = b + Σ w · feature",
     [("1 Trattoria Luna", "0.598", True), ("2 Pasta Express", "0.329", False), ("3 Dim Sum Palace", "0.092", False),
      ("4 Il Fiore", "−0.129", False), ("5 Kiddo Cafe", "−0.176", False)]),
]
for c, (x, hth, hen, nth, nen, rows) in enumerate(COLS):
    s.both(x + 10, 92, hth, hen, "nt-head")
    s.both(x + 10, 116, nth, nen, "pl-note")
    for k, (label, val, hot) in enumerate(rows):
        y = 130 + k * 50
        faded = c == 2 and k >= 3
        if not faded:
            s.box(x, y, 260, 42, "nt-out" if hot else "ml-cell", rx=10)
        cls = "hk-mono" if c == 1 else ("nt-task" if hot else "hk-desc")
        if faded:
            cls = "ml-neg" if "Kiddo" in label else "pl-note"
        s.text(x + 14, y + 27, label, cls)
        s.text(x + 246, y + 27, val, "ml-neg" if (faded and "Kiddo" in label) else "pl-note", "end")
    if c < 2:
        s.raw(f'<path d="M{x + 266} 230 L{x + 294} 230" class="nt-arrow"/><path d="M{x + 286} 223 L{x + 295} 230 L{x + 286} 237" class="nt-arrow"/>')
s.raw('<path d="M626 276 L874 276" class="nt-arrow" stroke-dasharray="4 5"/>')
s.both(880, 395, "คำตอบของ keyword search ตกไปท้ายสุด", "keyword search's answer drops to last", "pl-note", "end")
s.both(150, 395, "BM25 · embedding · cosine · RRF", "BM25 · embeddings · cosine · RRF", "pl-note", "middle")
s.both(450, 395, "feature · learning to rank", "features · learning to rank", "pl-note", "middle")
s.save("l11-whole-search.svg", 410)
