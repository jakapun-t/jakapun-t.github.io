"""Concept pictures for lesson 11 of the international NLP course (dense retrieval), in the style of
nlp l12-why-chunk.svg: the running example's question on top, drawn objects, arrows at the exact spot,
the real numbers attached to what they describe. ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/nlp_l11_concepts.py courses/nlp/images

Every number is the lesson's own (BM25 results and MiniLM / GloVe cosines from its code cells; the
weighted-sum table from its `silom` cell). The cosine picture uses its own small vectors so it does not
give away the card's exercise.

Uses the nt-*, pl-*, ml-*, sw-*, dg-* classes in templates/page.css.
"""

import math
import os
import sys
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp/images"


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

    def arrow(self, x1, y1, x2, y2, dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="pl-line"{dash}/>')
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 10 * math.cos(a - 0.55), y2 - 10 * math.sin(a - 0.55))
        p2 = (x2 - 10 * math.cos(a + 0.55), y2 - 10 * math.sin(a + 0.55))
        self.out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2:g} {y2:g} L{p2[0]:.1f} {p2[1]:.1f}" class="pl-line"/>')

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


W = 1180

# ---------------------------------------------------------------- S04: the "bad query" problem, three search bars
# Real BM25 results on the restaurants data (the card's table).
ROWS = [
    ("สั้นเกินไป", "Too short", "cafe", "คาเฟ่ที่พาลูกไปได้", "a cafe for my kids",
     "Book Nook Cafe: a quiet place for studying", "Kiddo Cafe never says “cafe”", "Kiddo Cafe ไม่มีคำว่า cafe เลย"),
    ("กำกวม", "Ambiguous", "light", "อาหารเบา ๆ", "a light meal",
     "Rooftop 52: steak and cocktails", "its description says “city lights”", "คำอธิบายมีคำว่า city lights"),
    ("ใช้คำต่างกัน", "Different words", "vegetarian food", "Green Bowl (plant-based)", "Green Bowl (plant-based)",
     "nothing: every score is 0", "Green Bowl says “plant-based … no meat”", "Green Bowl เขียนว่า plant-based … no meat"),
]
s = Svg(W, "The bad-query problem in our restaurant app. Too short: typed cafe, meant a cafe for kids, BM25 returned Book Nook Cafe, "
           "a study cafe, because Kiddo Cafe never says cafe. Ambiguous: typed light, meant a light meal, BM25 returned Rooftop 52, "
           "because its description says city lights. Different words: typed vegetarian food, meant Green Bowl, BM25 returned nothing, "
           "every score 0, because Green Bowl says plant-based.")
s.both(214, 30, "พิมพ์ว่า", "Typed", "nt-head")
s.both(430, 30, "หมายถึง", "Meant", "nt-head")
s.both(690, 30, "keyword search (BM25) คืนมา", "Keyword search (BM25) returned", "nt-head")
for k, (pth, pen, typed, mth, men, ret, why_en, why_th) in enumerate(ROWS):
    y = 44 + k * 120
    s.box(20, y, W - 40, 106, "sw-warn-box", 14)
    s.both(36, y + 58, pth, pen, "pl-label")
    # the search bar with a magnifier
    s.box(206, y + 30, 196, 44, "nt-bubble", 22)
    s.raw(f'<circle cx="{228}" cy="{y + 51}" r="7" class="pl-line" fill="none"/><path d="M233 {y + 56} L239 {y + 62}" class="pl-line"/>')
    s.text(246, y + 59, typed, "pl-text")
    # what they meant: a thought bubble
    s.box(426, y + 26, 230, 52, "ml-cell", 26)
    s.raw(f'<circle cx="418" cy="{y + 72}" r="5" class="ml-bar"/><circle cx="410" cy="{y + 82}" r="3" class="ml-bar"/>')
    s.both(541, y + 58, mth, men, "pl-text", "middle")
    # what BM25 returned
    s.arrow(662, y + 52, 682, y + 52)
    s.box(688, y + 14, 458, 44, "sw-chip-warn", 10)
    s.text(702, y + 42, "✗ " + ret, "pl-text")
    s.both(702, y + 88, why_th, why_en, "ml-neg")
s.both(20, 410, "BM25 ทำงานถูกแล้ว (มันจับคู่คำ) ปัญหาอยู่ที่คำค้น: คำที่พิมพ์ไม่ใช่คำที่บรรยายสิ่งที่ต้องการ",
       "BM25 did its job (it matched the words); the problem is the query: the typed words are not the words that describe what is wanted", "pl-note")
s.save("l11-bad-query.svg", 426)

# ---------------------------------------------------------------- S12: averaged word vectors vs a sentence encoder
# Cosine with "Hiring a teacher" (the card's table): GloVe average / MiniLM.
ADS = [("Teacher wanted", 0.83, 0.61), ("Looking for a high school teacher", 0.90, 0.67),
       ("Recruiting secondary school instructor", 0.76, 0.58), ("Hiring a chef", 0.89, 0.37),
       ("Teacher of the year award", 0.79, 0.44)]
SHORT = {"Looking for a high school teacher": "High school teacher", "Recruiting secondary school instructor": "Secondary instructor",
         "Teacher of the year award": "Teacher award"}
s = Svg(W, "Compared with Hiring a teacher. Averaged GloVe word vectors put Hiring a chef at 0.89, as close as the real teacher ads "
           "(0.76 to 0.90), because two of its three words are the same. The MiniLM sentence encoder reads the whole ad and puts "
           "Hiring a chef farthest, at 0.37, while the teacher ads score 0.58 to 0.67.")
s.box(W / 2 - 200, 8, 400, 46, "nt-bubble", 23)
s.text(W / 2, 38, "compared with: Hiring a teacher", "pl-text", "middle")
for x0, band, th, en, idx, res_th, res_en, rcls in (
        (20, "sw-warn-box", "✗ เฉลี่ย vector ของคำ (GloVe ไม่ดูบริบท)", "✗ Averaged word vectors (GloVe, no context)", 1,
         "✗ ประกาศรับเชฟดูเหมือนรับครู (0.89)", "✗ the chef ad looks like a teacher ad (0.89)", "ml-neg"),
        (600, "nt-band-a", "✓ sentence embedding (MiniLM ดูบริบท)", "✓ Sentence embedding (MiniLM, with context)", 2,
         "✓ ประกาศรับเชฟไกลที่สุด (0.37)", "✓ the chef ad is the farthest (0.37)", "ml-ok")):
    s.box(x0, 70, 560, 400, band, 14)
    s.both(x0 + 20, 102, th, en, "pl-label")
    ax0, ax1 = x0 + 196, x0 + 536  # cosine 0.3 .. 1.0
    pos = lambda v: ax0 + (v - 0.3) / 0.7 * (ax1 - ax0)
    for k, row in enumerate(ADS):
        name, v = row[0], row[idx]
        y = 160 + k * 52
        chef = name == "Hiring a chef"
        s.both(x0 + 20, y + 6, SHORT.get(name, name), SHORT.get(name, name), "pl-label" if chef else "pl-note")
        s.raw(f'<path d="M{ax0} {y} H{ax1}" class="dg-rule"/>')
        s.raw(f'<circle cx="{pos(v):.1f}" cy="{y}" r="8" class="{"ml-bar-top" if chef else "ml-bar"}"/>')
        s.text(pos(v), y - 14, f"{v:.2f}", "pl-label" if chef else "pl-note", "middle")
    for v in (0.3, 0.5, 0.7, 0.9):
        s.text(pos(v), 432, f"{v:.1f}", "pl-note", "middle")
    s.both((ax0 + ax1) / 2, 412, "cosine กับ Hiring a teacher →", "cosine with Hiring a teacher →", "pl-note", "middle")
    s.both(x0 + 20, 458, res_th, res_en, rcls)
s.both(20, 500, "เฉลี่ยคำ: hiring + a + chef ใกล้ hiring + a + teacher เพราะซ้ำกัน 2 ใน 3 คำ · encoder อ่านทั้งประโยคจึงเห็นว่าเป็นงานอื่น",
       "Averaging: hiring + a + chef is close to hiring + a + teacher (2 of 3 words shared) · the encoder reads the whole ad and sees another job",
       "pl-note")
s.save("l11-sentence-vs-words.svg", 516)

# ---------------------------------------------------------------- S13: cosine = direction, not length
# Small 2-number vectors (not the exercise's): q = (3, 1); d1 = (6, 2) cos 1; d2 = (1, 2) cos 0.71; d3 = (-1, 3) cos 0.
s = Svg(W, "Cosine similarity compares directions. The query q = (3, 1). d1 = (6, 2) is twice as long but points the same way: "
           "cosine 1. d2 = (1, 2) points a little away: cosine 0.71. d3 = (−1, 3) is at a right angle: cosine 0.")
U, ox, oy = 50, 200, 380
s.box(20, 20, 560, 460, "ml-cell", 14)
for gx in range(-3, 8):
    s.raw(f'<path d="M{ox + gx * U} 40 V460" class="dg-rule"/>')
for gy in range(-1, 7):
    s.raw(f'<path d="M40 {oy - gy * U} H560" class="dg-rule"/>')
s.raw(f'<path d="M40 {oy} H560 M{ox} 40 V460" class="dg-rule-strong"/>')
VEC = [("q = (3, 1)", 3, 1, "pl-label", 10, 22, "start"), ("d1 = (6, 2)", 6, 2, "ml-ok", 0, -14, "end"),
       ("d2 = (1, 2)", 1, 2, "pl-text", 10, -6, "start"), ("d3 = (−1, 3)", -1, 3, "ml-neg", 10, -10, "start")]
for lab, vx, vy, cls, dx, dy, anchor in VEC:
    tx, ty = ox + vx * U, oy - vy * U
    s.arrow(ox, oy, tx, ty)
    s.text(tx + dx, ty + dy, lab, cls, anchor)
s.raw(f'<path d="M{ox} {oy} L{ox + 3 * U} {oy - U}" class="pl-line" stroke-width="7" opacity=".35"/>')
s.box(600, 20, 560, 460, "nt-band-a", 14)
s.both(620, 54, "cosine ดูแค่ทิศ ไม่ดูความยาว", "Cosine looks only at direction, not length", "pl-label")
s.text(620, 92, "cos(q, d) = q·d / (|q| · |d|)", "pl-label")
RES = [("d1 = (6, 2)", "(18 + 2) / (√10 · √40) = 20 / 20", "1", "ยาวกว่า 2 เท่า แต่ทิศเดียวกัน", "twice as long, same direction", "ml-ok"),
       ("d2 = (1, 2)", "(3 + 2) / (√10 · √5) = 5 / 7.07", "0.71", "เอียงออกไปนิดหนึ่ง", "points a little away", "pl-text"),
       ("d3 = (−1, 3)", "(−3 + 3) / (√10 · √10) = 0 / 10", "0", "ตั้งฉาก: ไม่เกี่ยวกัน", "at a right angle: unrelated", "ml-neg")]
for k, (lab, calc, val, th, en, cls) in enumerate(RES):
    y = 120 + k * 104
    s.box(620, y, 520, 92, "ml-cell", 10)
    s.text(636, y + 28, lab, "pl-label")
    s.text(1124, y + 28, f"cos = {val}", cls, "end")
    s.text(636, y + 54, calc, "dg-code")
    s.both(636, y + 80, th, en, "pl-note")
s.both(620, 464, "ตัวเลขจริงยาว 384 ตัว (MiniLM) สูตรเดียวกัน", "Real vectors have 384 numbers (MiniLM); same formula", "pl-note")
s.save("l11-cosine.svg", 492)

# ---------------------------------------------------------------- S09: the weighted sum as stacked bars
# The card's silom table: final = 0.5·text + 1.0·rating − 1.0·distance_km − 0.5·price.
PLACES = [("Pasta Express", 3.94, 4.0, 0.2, 1, 5.27), ("Trattoria Luna", 1.63, 4.6, 0.4, 2, 4.01),
          ("Book Nook Cafe", 0.00, 4.2, 0.3, 2, 2.90), ("Curry House", 0.00, 4.0, 0.6, 1, 2.90)]
PARTS = [("0.5 · text", "pl-chip"), ("1.0 · rating", "rc-res"), ("−1.0 · distance", "sw-chip-warn"), ("−0.5 · price", "pl-chip-del")]
s = Svg(W, "The weighted sum for 'romantic pasta cheap' in Silom, as stacked bars: each restaurant's final score is 0.5 times text "
           "plus 1.0 times rating, minus 1.0 times distance and 0.5 times price. Pasta Express 5.27, Trattoria Luna 4.01, "
           "Book Nook Cafe 2.90, Curry House 2.90.")
s.box(W / 2 - 230, 8, 460, 46, "nt-bubble", 23)
s.text(W / 2, 38, "romantic pasta cheap · Silom", "pl-text", "middle")
s.text(20, 90, "final = 0.5·text + 1.0·rating − 1.0·distance_km − 0.5·price", "pl-label")
lx = 20
for lab, cls in PARTS:
    s.box(lx, 108, 22, 18, cls, 4)
    s.text(lx + 30, 123, lab, "pl-note")
    lx += 30 + len(lab) * 10 + 28
Z, SC = 430, 100  # x of zero, pixels per point
s.raw(f'<path d="M{Z} 146 V{150 + len(PLACES) * 70}" class="dg-rule-strong"/>')
s.text(Z, 144, "0", "pl-note", "middle")
for k, (name, text, rating, dist, price, final) in enumerate(PLACES):
    y = 160 + k * 70
    s.text(20, y + 30, name, "pl-label" if k == 0 else "pl-text")
    pos = [(0.5 * text, "pl-chip"), (1.0 * rating, "rc-res")]
    neg = [(1.0 * dist, "sw-chip-warn"), (0.5 * price, "pl-chip-del")]
    x = Z
    for v, cls in pos:
        if v > 0:
            s.box(x, y + 8, v * SC, 32, cls, 4)
            if v * SC > 46:
                s.text(x + v * SC / 2, y + 30, f"{v:.2f}", "pl-note", "middle")
            x += v * SC
    x = Z
    for v, cls in neg:
        s.box(x - v * SC, y + 8, v * SC, 32, cls, 4)
        if v * SC > 40:
            s.text(x - v * SC / 2, y + 30, f"−{v:.1f}", "pl-note", "middle")
        x -= v * SC
    s.text(Z + (0.5 * text + rating) * SC + 12, y + 31, f"= {final:.2f}", "ml-ok" if k == 0 else "pl-label")
s.both(20, 456, "ส่วนบวก (text, rating) ไปทางขวา ส่วนลบ (ระยะทาง ราคา) ดึงกลับทางซ้าย · ผลรวมคือคะแนนสุดท้าย",
       "Positive parts (text, rating) go right; negative parts (distance, price) pull back left · the sum is the final score", "pl-note")
s.save("l11-weighted-sum.svg", 472)

# ---------------------------------------------------------------- S10: the weights learned from clicks
# The card's LinearRegression on l11_clicks.csv: text 0.063, dense 0.694, rating 0.517, distance_km -0.075, price -0.145.
WEIGHTS = [("text", 0.063, "คำที่ตรงมากขึ้นช่วยได้", "more matching words help"),
           ("dense", 0.694, "ความหมายใกล้ขึ้น ถูกคลิกมากขึ้น", "a closer meaning gets more clicks"),
           ("rating", 0.517, "ดาวเพิ่มทีละดวงช่วยได้", "each extra star helps"),
           ("distance_km", -0.075, "ไกลขึ้นทีละกิโลเมตร คะแนนลด", "each km farther hurts"),
           ("price", -0.145, "แพงขึ้นทีละระดับ คะแนนลด", "each price level up hurts")]
s = Svg(W, "The weights learning to rank found in the clicks: dense +0.694 and rating +0.517 push a place up, text +0.063 a little; "
           "price -0.145 and distance_km -0.075 pull it down. Nobody chose these numbers; the regression found them.")
s.text(20, 34, "clicked ≈ b + w₁·text + w₂·dense + w₃·rating + w₄·distance_km + w₅·price", "pl-label")
Z, SC = 420, 300  # zero line, pixels per unit of weight
s.raw(f'<path d="M{Z} 56 V{70 + len(WEIGHTS) * 58}" class="dg-rule-strong"/>')
s.both(Z - 10, 62, "← ดึงลง", "← pulls down", "ml-neg", "end")
s.both(Z + 10, 62, "ดันขึ้น →", "pushes up →", "ml-ok")
for k, (f, w, th, en) in enumerate(WEIGHTS):
    y = 82 + k * 58
    s.text(20, y + 26, f, "pl-label")
    if w > 0:
        s.box(Z, y + 6, w * SC, 30, "rc-res", 4)
        s.text(Z + w * SC + 10, y + 27, f"+{w:.3f}", "ml-ok")
        s.both(Z + w * SC + 92, y + 27, th, en, "pl-note")
    else:
        s.box(Z + w * SC, y + 6, -w * SC, 30, "sw-chip-warn", 4)
        s.text(Z + w * SC - 10, y + 27, f"−{-w:.3f}", "ml-neg", "end")
        s.both(Z + 10, y + 27, th, en, "pl-note")
s.both(20, 384, "ไม่มีใครเลือกตัวเลขเหล่านี้ regression หาเองจากการคลิก (ข้อมูลฝึกหัด l11_clicks.csv)",
       "Nobody chose these numbers: the regression found them in the clicks (practice data, l11_clicks.csv)", "pl-note")
s.save("l11-learned-weights.svg", 400)
