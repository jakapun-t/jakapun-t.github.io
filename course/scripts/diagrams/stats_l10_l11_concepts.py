"""Concept pictures for stats-dh lessons 10 (model tuning) and 11 (logistic regression), in the style of
nlp l12-why-chunk.svg: the running example's question on top, panels answering that same question, drawn
objects (column strips, a slider, score curves, S-curves, confusion matrices of people), arrows at the
exact spot, the real numbers attached to what they describe. ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/stats_l10_l11_concepts.py courses/stats-dh/images

Every number is a real run in course/.venv, the same as the lessons' code cells:
  L10 diabetes (load_diabetes, 80/20 split, random_state=42): LinearRegression test R² 0.453 on all 10
      columns, 0.454 on bmi, bp, s5. |r| with y on the training set: bmi .60, s5 .55, bp .44, s4 .43,
      s6 .39, s3 .38, s1 .20, age .20, s2 .15, sex .01. Forward SFS (cv=5): bmi 0.322, + s5 0.415,
      + bp 0.440 (10 + 9 + 8 = 27 candidate sets × 5 folds = 135 trainings). Lasso alpha=1: β bmi 413,
      s5 258, bp 35, the other 7 exactly 0, CV R² 0.324. Ridge CV R²: alpha 0.001 0.450, 0.01 0.453,
      0.1 0.456, 1 0.380, 10 0.109, 100 −0.012; the curve is 41 alphas on a log grid. RandomizedSearchCV
      (loguniform(0.001, 100), n_iter=10, random_state=1) tries 0.001 0.003 0.005 0.009 0.032 0.053
      0.096 0.122 0.494 3.996, best 0.096 (CV R² 0.457); both searches give test R² 0.461.
  L11 obesity (108 rows): Weight-only model b0 −109.42, b1 1.1195; 100 kg → z 2.53, p̂ 0.926.
      4-class model (70/30 split, random_state=42, StandardScaler, LogisticRegression): train 75, test 33;
      Height on train mean 165.3, sd 27.0 (175 cm → 0.36); first test person (60, 120 cm, 70 kg, female)
      p̂ Normal 0.552, Obese 0.003, Overweight 0.360, Underweight 0.085; accuracy 0.818 (27 of 33).
      The 36-year-old man (190 cm, 75 kg): z 1.78, −0.57, 0.34, −1.55; e^z 5.93, 0.56, 1.41, 0.21
      (sum 8.11); p̂ 0.73, 0.07, 0.17, 0.03. Overweight vs rest on the test set: TP 4, FN 5 (all 5 called
      Normal Weight), FP 0, TN 24. Authors A/B/C: the lesson's 14-text confusion matrix.

Uses the nt-*, pl-*, ml-*, sw-*, rc-*, dg-* classes in templates/page.css.
"""

import math
import os
import sys
import unicodedata
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/stats-dh/images"
W = 1180


def width(s, fs=19):
    return sum(0 if unicodedata.category(c) == "Mn" else fs * (1.1 if ord(c) > 0x1F000 else 0.58) for c in s)


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

    def line(self, x1, y1, x2, y2, cls="pl-line", dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="{cls}"{dash}/>')

    def arrow(self, x1, y1, x2, y2, dashed=False):
        self.line(x1, y1, x2, y2, dashed=dashed)
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 10 * math.cos(a - 0.55), y2 - 10 * math.sin(a - 0.55))
        p2 = (x2 - 10 * math.cos(a + 0.55), y2 - 10 * math.sin(a + 0.55))
        self.out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2:g} {y2:g} L{p2[0]:.1f} {p2[1]:.1f}" class="pl-line"/>')

    def badge(self, x, y, k):
        self.out.append(f'<g class="dg-badge"><circle cx="{x:g}" cy="{y:g}" r="13"/>'
                        f'<text x="{x:g}" y="{y + 5:g}" text-anchor="middle">{k}</text></g>')

    def bubble(self, th, en, y=8):
        w = max(width(th), width(en)) + 56
        self.box(self.w / 2 - w / 2, y, w, 46, "nt-bubble", 23)
        self.both(self.w / 2, y + 30, th, en, "pl-text", "middle")

    def panel(self, x, y, w, h, cls, th, en, k=None):
        self.box(x, y, w, h, cls, 14)
        if k is None:
            self.both(x + 20, y + 32, th, en, "pl-label")
        else:
            self.badge(x + 32, y + 26, k)
            self.both(x + 54, y + 32, th, en, "pl-label")

    def person(self, x, y, cls):
        """A small person: head and shoulders, about 14 × 22."""
        self.out.append(f'<circle cx="{x:g}" cy="{y - 6:g}" r="5" class="{cls}"/>'
                        f'<path d="M{x - 7:g} {y + 12:g} Q{x - 7:g} {y + 1:g} {x:g} {y + 1:g} Q{x + 7:g} {y + 1:g} {x + 7:g} {y + 12:g} Z" class="{cls}"/>')

    def save(self, name, h, sized=False):
        # sized: width/height attributes give the picture an intrinsic size, so it keeps its width inside an
        # exercise's projector frame (a shrink-to-fit box); the page CSS still sets its width everywhere else
        size = f' width="{self.w}" height="{h}"' if sized else ""
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}"{size} class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


def logx(a, x0, per_decade, lo=-3):
    return x0 + (math.log10(a) - lo) * per_decade


# ================================================================ L10-S01: two ways to score better
s = Svg(W, "Model tuning on the diabetes data, same linear model. 1 Feature selection changes which columns it learns from: "
           "keep bmi, bp and s5 and drop the other 7, and the test R² stays at 0.454 (0.453 with all 10). 2 Hyperparameter "
           "tuning changes how it learns: Ridge with all 10 columns scores CV R² 0.450, 0.453, 0.456, 0.380, 0.109 and −0.012 "
           "for alpha 0.001, 0.01, 0.1, 1, 10 and 100; the best is alpha 0.1.")
s.bubble("ข้อมูล diabetes 442 คน โมเดล linear เดิม: ทำคะแนนให้ดีขึ้นได้ไหม",
         "Diabetes, 442 patients, the same linear model: can we score better?")
# 1. feature selection: ten column strips, three kept
s.panel(20, 70, 560, 370, "nt-band-a", "Feature selection: เรียนจากคอลัมน์ไหน", "Feature selection: which columns it learns from", 1)
s.both(40, 128, "ค่าที่วัด 10 อย่าง = 10 คอลัมน์", "10 measurements = 10 columns", "pl-note")
COLS = ["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]
KEEP = {"bmi", "bp", "s5"}
for k, c in enumerate(COLS):
    x = 46 + k * 51
    keep = c in KEEP
    s.box(x, 176, 42, 150, "rc-res" if keep else "pl-chip-del", 6)
    for yy in range(192, 320, 16):
        if keep:
            s.box(x + 8, yy, 26, 4, "ml-bar", 2)
        else:
            s.raw(f'<path d="M{x + 8} {yy + 2} H{x + 34}" class="dg-rule"/>')
    s.text(x + 21, 166, c, "pl-label" if keep else "pl-del", "middle")
    s.text(x + 21, 352, "✓" if keep else "✗", "ml-ok" if keep else "ml-neg", "middle")
s.both(40, 392, "✓ เก็บ bmi, bp, s5 ตัดอีก 7", "✓ keep bmi, bp, s5; drop the other 7", "ml-ok")
s.both(40, 420, "test R² 0.453 (10 คอลัมน์) → 0.454 (3 คอลัมน์)", "test R² 0.453 (10 columns) → 0.454 (3 columns)", "pl-text")
# 2. hyperparameter tuning: a slider for alpha, a CV R² bar under each stop
s.panel(600, 70, 560, 370, "nt-band-b", "Hyperparameter: เรียนอย่างไร", "Hyperparameter: how it learns", 2)
s.both(620, 128, "ครบ 10 คอลัมน์ · Ridge(alpha=…) · แท่ง = CV R²", "all 10 columns · Ridge(alpha=…) · bars = CV R²", "pl-note")
ALPHAS = [(0.001, 0.450), (0.01, 0.453), (0.1, 0.456), (1, 0.380), (10, 0.109), (100, -0.012)]
ax = lambda a: logx(a, 670, 90)
s.raw(f'<path d="M{ax(0.001) - 14:g} 176 H{ax(100) + 14:g}" class="dg-rule-strong" stroke-width="6" stroke-linecap="round"/>')
for a, r2 in ALPHAS:
    x = ax(a)
    s.line(x, 168, x, 184, "dg-rule-strong")
    s.text(x, 206, f"{a:g}", "pl-note", "middle")
    best = a == 0.1
    base, sc = 392, 260
    hgt = r2 * sc
    s.box(x - 18, base - max(hgt, 0), 36, max(abs(hgt), 2), "ml-bar-top" if best else "ml-bar", 3)
    s.text(x, base - max(hgt, 0) - 8, f"{r2:.3f}".replace("-", "−"), "pl-label" if best else "pl-note", "middle")
s.line(650, 392, 1140, 392, "dg-rule-strong")
s.raw(f'<circle cx="{ax(0.1):g}" cy="176" r="12" class="ml-bar-top"/>')
s.both(ax(0.1) + 18, 160, "alpha = 0.1", "alpha = 0.1", "pl-label")
s.both(620, 420, "✓ alpha 0.1 ดีที่สุด (0.456) · alpha 100 พัง (−0.012)", "✓ alpha 0.1 is best (0.456) · alpha 100 fails (−0.012)", "ml-ok")
s.both(20, 472, "ทั้งสองแบบเปลี่ยนสิ่งเดียว ไม่เปลี่ยนชนิดของโมเดล และวัดกับข้อมูลที่โมเดลไม่เคยเห็น (CV หรือชุด test)",
       "Each changes one thing, never the kind of model, and is scored on data the model has not seen (CV or the test set)", "pl-note")
s.save("l10-two-tools.svg", 488)

# ================================================================ L10-S03: the checklist on the houses table
HOUSE = [  # column, width, verdict (keep/drop/target), badge, values
    ("id", 54, "drop", 1, ["1", "2", "3", "4"]),
    ("name", 84, "drop", 2, ["A123", "B456", "C789", "D012"]),
    ("size_sqft", 112, "keep", None, ["1800", "2400", "1500", "3000"]),
    ("bedrooms", 112, "keep", None, ["3", "4", "2", "5"]),
    ("location", 118, "keep", 4, ["Suburb", "Downtown", "Suburb", "Suburb"]),
    ("year_built", 118, "keep", None, ["2005", "2010", "1995", "2018"]),
    ("owner_name", 138, "drop", 1, ["John Doe", "Jane Smith", "Mark Lee", "Emily Chen"]),
    ("price", 106, "target", None, ["350000", "500000", "300000", "600000"]),
]
s = Svg(W, "The six-question checklist on the houses table, predicting price. id and owner_name fail question 1 (not about "
           "the house); name fails question 2 (noise: a different code in every row); location passes but is text, so "
           "question 4 turns it into a 0/1 column; size_sqft, bedrooms and year_built are kept; price is the target. "
           "Questions 3, 5 and 6 find nothing in this table.")
s.bubble("ทำนาย price: คอลัมน์ไหนเป็น feature ได้", "Predict price: which columns can be features?")
GAP = 6
total = sum(c[1] for c in HOUSE) + GAP * (len(HOUSE) - 1)
x = (W - total) / 2
TOP = 124
VERD = {"keep": ("✓ เก็บ", "✓ keep", "ml-ok", "rc-res"), "drop": ("✗ ตัด", "✗ drop", "ml-neg", "sw-warn-box"),
        "target": ("y", "target y", "pl-label", "rc-ctx")}
xs = {}
for name, w, verdict, badge, vals in HOUSE:
    th, en, tcls, fill = VERD[verdict]
    xs[name] = x + w / 2
    s.both(x + w / 2, 100, th, en, tcls, "middle")
    s.box(x, TOP, w, 200, fill, 8)
    s.raw(f'<path d="M{x + 6:g} {TOP + 40} H{x + w - 6:g}" class="dg-rule"/>')
    s.text(x + w / 2, TOP + 27, name, "pl-del" if verdict == "drop" else "pl-label", "middle")
    for k, v in enumerate(vals):
        s.text(x + w / 2, TOP + 68 + k * 38, v, "pl-text", "middle")
    if badge:
        s.line(x + w / 2, TOP + 204, x + w / 2, TOP + 230)
        s.badge(x + w / 2, TOP + 244, badge)
    x += w + GAP
s.both(xs["location"], TOP + 282, "→ location_Suburb 1/0", "→ location_Suburb 1/0", "pl-note", "middle")
NOTES = [
    (1, "ไม่เกี่ยวกับตัวบ้าน: id เป็นแค่เลขแถว owner_name เป็นชื่อคน", "Not about the house: id is only a row number; owner_name is a person"),
    (2, "noise: name เป็นรหัสที่ไม่ซ้ำกันเลยทุกแถว (A123, B456 …)", "Noise: name is a different code in every row (A123, B456 …)"),
    (4, "ชนิดข้อมูล: location เป็นข้อความ แปลงเป็น 0/1 ก่อน (Suburb = 1, Downtown = 0)", "Type: location is text, so turn it into 0/1 first (Suburb = 1, Downtown = 0)"),
]
for k, (b, th, en) in enumerate(NOTES):
    y = 446 + k * 34
    s.badge(64, y - 6, b)
    s.both(86, y, th, en, "pl-text")
s.raw('<g class="dg-badge" opacity=".45">' + "".join(
    f'<circle cx="{64 + j * 30}" cy="{544}" r="13"/><text x="{64 + j * 30}" y="549" text-anchor="middle">{b}</text>'
    for j, b in enumerate((3, 5, 6))) + "</g>")
s.both(146, 550, "รั่วคำตอบไหม · ค่าเหมือนกันทุกแถวไหม · ซ้ำกับคอลัมน์อื่นไหม: ตารางนี้ไม่มีคอลัมน์ที่ต้องตัดด้วยสามข้อนี้",
       "Leaks the answer? Same value in every row? Repeats another column? Nothing in this table fails these three", "pl-note")
s.both(20, 596, "✓ feature: size_sqft, bedrooms, location (เป็น 0/1), year_built · ✗ ตัด id, name, owner_name",
       "✓ features: size_sqft, bedrooms, location (as 0/1), year_built · ✗ drop id, name, owner_name", "ml-ok")
s.save("l10-checklist-houses.svg", 612)

# ================================================================ L10-S06: three families answer the same question
R = [("bmi", .60), ("s5", .55), ("bp", .44), ("s4", .43), ("s6", .39), ("s3", .38), ("s1", .20), ("age", .20), ("s2", .15), ("sex", .01)]
LASSO = {"bmi": 413, "s5": 258, "bp": 35}
s = Svg(W, "Three ways an algorithm picks diabetes columns. 1 Filter ranks the columns by |r| with y, no model, and keeps "
           "the top k = 3: bmi, s5, bp, CV R² 0.440, 0 trainings. 2 Wrapper (forward SFS) trains a model on each candidate "
           "set and adds the best column each round: bmi 0.322, + s5 0.415, + bp 0.440, 135 trainings. 3 Embedded (Lasso, "
           "alpha 1) trains once and sets the β of 7 columns to exactly 0, keeping bmi 413, s5 258, bp 35, CV R² 0.324.")
s.bubble("diabetes: ควรเก็บคอลัมน์ไหนจาก 10 ตัว", "Diabetes: which of the 10 columns should we keep?")
PW, PT, PH = 364, 70, 450
ROW0, RH = 162, 25
for i in range(3):
    s.box(20 + i * (PW + 24), PT, PW, PH, "nt-band-a", 14)
# 1 filter
X0 = 20
s.badge(X0 + 32, PT + 26, 1)
s.both(X0 + 54, PT + 32, "Filter: ใช้สถิติอย่างเดียว", "Filter: statistics only", "pl-label")
s.both(X0 + 20, PT + 60, "|r| กับ y ของแต่ละคอลัมน์ ไม่ต้องฝึกโมเดล", "|r| of each column with y, no model", "pl-note")
for k, (c, r) in enumerate(R):
    y = ROW0 + k * RH
    top = k < 3
    s.text(X0 + 20, y + 17, c, "ml-b" if top else "ml-i")
    s.box(X0 + 66, y + 5, r * 300, 15, "ml-bar-top" if top else "ml-bar", 3)
    s.text(X0 + 72 + r * 300, y + 17, f"{r:.2f}", "ml-b" if top else "ml-i")
cut = ROW0 + 3 * RH + 1
s.line(X0 + 14, cut, X0 + PW - 14, cut, "ml-cut-guess")
s.text(X0 + PW - 16, cut + 20, "k = 3 ✂", "ml-neg", "end")
# 2 wrapper
X0 = 20 + PW + 24
s.badge(X0 + 32, PT + 26, 2)
s.both(X0 + 54, PT + 32, "Wrapper: ฝึกจริงแล้ววัดผล", "Wrapper: train and score", "pl-label")
s.both(X0 + 20, PT + 60, "SFS: ทุกรอบเพิ่มตัวที่ช่วยมากที่สุด", "SFS: one best column per round", "pl-note")
ROUNDS = [(["bmi"], 0.322, 10, "bmi"), (["bmi", "s5"], 0.415, 9, "s5"), (["bmi", "s5", "bp"], 0.440, 8, "bp")]
for k, (cols, cv, tried, new) in enumerate(ROUNDS):
    y = 168 + k * 84
    cx = X0 + 18
    for c in cols:
        w = width(c, 16) + 16
        s.box(cx, y, w, 30, "rc-res" if c == new else "ml-cell-b", 8)
        s.text(cx + w / 2, y + 21, c, "ml-b", "middle")
        cx += w + 4
    s.arrow(X0 + 160, y + 15, X0 + 186, y + 15)
    s.box(X0 + 192, y - 4, 154, 38, "ml-model-done" if k == 2 else "ml-model", 8)
    s.text(X0 + 269, y + 22, f"CV R² {cv:.3f}", "ml-model-text", "middle")
    s.both(X0 + 20, y + 58, f"รอบ {k + 1}: ลอง {tried} ชุด เก็บ {new}", f"round {k + 1}: tried {tried} sets, kept {new}", "ml-i")
# 3 embedded
X0 = 20 + 2 * (PW + 24)
s.badge(X0 + 32, PT + 26, 3)
s.both(X0 + 54, PT + 32, "Embedded: เลือกระหว่างฝึก", "Embedded: picks while training", "pl-label")
s.both(X0 + 20, PT + 60, "Lasso (alpha = 1): ค่า β ของแต่ละคอลัมน์", "Lasso (alpha = 1): each column's β", "pl-note")
for k, (c, _) in enumerate(R):
    y = ROW0 + k * RH
    b = LASSO.get(c, 0)
    if b:
        s.text(X0 + 20, y + 17, c, "ml-b")
        s.box(X0 + 66, y + 5, b / 413 * 200, 15, "ml-bar-top", 3)
        s.text(X0 + 72 + b / 413 * 200, y + 17, str(b), "ml-b")
    else:
        s.text(X0 + 20, y + 17, c, "ml-i")
        s.raw(f'<path d="M{X0 + 17} {y + 12} H{X0 + 22 + width(c, 16)}" class="ml-cut"/>')
        s.text(X0 + 66, y + 17, "0", "ml-i")
s.arrow(X0 + 156, ROW0 + 6 * RH + 13, X0 + 92, ROW0 + 6 * RH + 13)
s.both(X0 + 164, ROW0 + 6 * RH + 6, "7 ตัว β = 0", "7 columns: β = 0", "ml-neg")
s.both(X0 + 164, ROW0 + 6 * RH + 34, "= ตัดทิ้ง", "= dropped", "ml-neg")
# results
for i, (th, en, cv) in enumerate((("ฝึก 0 ครั้ง", "0 trainings", "0.440"), ("27 ชุด × cv 5 = ฝึก 135 ครั้ง", "27 sets × cv 5 = 135 trainings", "0.440"),
                                  ("ฝึกครั้งเดียว", "1 training", "0.324"))):
    X0 = 20 + i * (PW + 24)
    s.both(X0 + 20, 446, "✓ เก็บ bmi, s5, bp", "✓ keeps bmi, s5, bp", "ml-ok")
    s.both(X0 + 20, 476, th, en, "pl-note")
    s.text(X0 + 20, 504, f"CV R² {cv}", "pl-note")
s.both(20, 556, "ข้อมูลนี้ทั้งสามแบบเลือกชุดเดียวกัน · ต่างกันที่ความเร็ว (ฝึก 0 / 135 / 1 ครั้ง) และ ① ดูทีละคอลัมน์ ส่วน ② ③ ดูหลายคอลัมน์พร้อมกัน",
       "Here all three pick the same set · they differ in speed (0 / 135 / 1 trainings), and ① looks at one column at a time while ② ③ see them together",
       "pl-note")
s.save("l10-three-families.svg", 572)

# ================================================================ L10-S09: grid vs random search on Ridge's alpha
CURVE = [(0.001, 0.4504), (0.0013, 0.4507), (0.0018, 0.451), (0.0024, 0.4513), (0.0032, 0.4516), (0.0042, 0.4519),
         (0.0056, 0.4522), (0.0075, 0.4524), (0.01, 0.4527), (0.0133, 0.4531), (0.0178, 0.4535), (0.0237, 0.454),
         (0.0316, 0.4546), (0.0422, 0.4553), (0.0562, 0.4559), (0.075, 0.4564), (0.1, 0.4565), (0.1334, 0.4558),
         (0.1778, 0.4539), (0.2371, 0.4502), (0.3162, 0.4439), (0.4217, 0.4343), (0.5623, 0.4208), (0.7499, 0.4029),
         (1.0, 0.3802), (1.3335, 0.353), (1.7783, 0.3216), (2.3714, 0.2868), (3.1623, 0.2498), (4.217, 0.2119),
         (5.6234, 0.1749), (7.4989, 0.14), (10.0, 0.1085), (13.3352, 0.081), (17.7828, 0.0577), (23.7137, 0.0385),
         (31.6228, 0.023), (42.1697, 0.0106), (56.2341, 0.0009), (74.9894, -0.0066), (100.0, -0.0123)]
GRID = [(0.001, 0.450), (0.01, 0.453), (0.1, 0.456), (1, 0.380), (10, 0.109), (100, -0.012)]
RAND = [(0.001, 0.450), (0.003, 0.452), (0.005, 0.452), (0.009, 0.453), (0.032, 0.455), (0.053, 0.456), (0.096, 0.457),
        (0.122, 0.456), (0.494, 0.427), (3.996, 0.219)]
s = Svg(W, "Choosing Ridge's alpha on the diabetes data. Both panels show the same CV R² curve. Grid search tries the 6 listed "
           "values 0.001 to 100 and finds 0.1 (CV R² 0.456), but never tries anything between 0.01 and 0.1. Random search "
           "draws 10 values on a log scale and finds 0.096 (CV R² 0.457). Both give test R² 0.461. With 4 hyperparameters "
           "of 5 values each, a grid needs 625 models; random search always needs only N.")
s.bubble("Ridge กับ diabetes: ควรลอง alpha ค่าไหนบ้าง (ลอง 1 ค่า = ฝึก 1 โมเดล)", "Ridge on diabetes: which alphas should we try? (1 try = 1 model)")
py = lambda v: 341 - v * 380


def score_plot(x0, tried, best):
    px = lambda a: logx(a, x0 + 80, 90)
    s.line(x0 + 66, 341, x0 + 540, 341, "dg-rule-strong")
    s.text(x0 + 60, 347, "0", "pl-note", "end")
    s.text(x0 + 60, py(0.4) + 6, "0.4", "pl-note", "end")
    s.line(x0 + 66, py(0.4), x0 + 540, py(0.4), "dg-rule")
    s.text(x0 + 16, 270, "CV R²", "pl-note")
    pts = " ".join(f"{px(a):.1f},{py(v):.1f}" for a, v in CURVE)
    s.raw(f'<polyline points="{pts}" class="pl-line" opacity=".35"/>')
    for a in (0.001, 0.01, 0.1, 1, 10, 100):
        s.line(px(a), 362, px(a), 372, "dg-rule-strong")
        s.text(px(a), 394, f"{a:g}", "pl-note", "middle")
    s.both(x0 + 300, 420, "alpha (สเกล log)", "alpha (log scale)", "pl-note", "middle")
    for a, v in tried:
        s.raw(f'<path d="M{px(a):.1f} 362 V{py(v) + 8:.1f}" class="dg-rule"/>')
    for a, v in tried:
        s.raw(f'<circle cx="{px(a):.1f}" cy="{py(v):.1f}" r="{9 if a == best else 7}" class="{"ml-bar-top" if a == best else "pl-dot"}"/>')
    return px


s.panel(20, 70, 560, 450, "nt-band-a", "Grid search: ลองทุกค่าในรายการ (6 ค่า)", "Grid search: every value in your list (6)", 1)
px = score_plot(20, GRID, 0.1)
for a, v in GRID:
    s.text(px(a), py(v) - 16, f"{v:.3f}".replace("-", "−"), "pl-label" if a == 0.1 else "pl-note", "middle")
mid = (px(0.01) + px(0.1)) / 2
s.box(px(0.01) + 10, 336, px(0.1) - px(0.01) - 20, 10, "sw-chip-warn", 4)
s.arrow(mid, 262, mid, 196)
s.both(mid, 284, "ระหว่าง 0.01 กับ 0.1: ไม่เคยลอง", "between 0.01 and 0.1: never tried", "ml-neg", "middle")
s.both(40, 462, "✓ ได้ alpha 0.1 · CV R² 0.456 · test R² 0.461", "✓ best alpha 0.1 · CV R² 0.456 · test R² 0.461", "ml-ok")
s.both(40, 494, "เขียนรายการเอง: ลองแค่ค่าที่เราเดา", "you write the list: it tries only your guesses", "pl-note")
s.panel(600, 70, 560, 450, "nt-band-a", "Random search: สุ่ม 10 ค่าในช่วง", "Random search: 10 random values in a range", 2)
px = score_plot(600, RAND, 0.096)
s.arrow(px(0.096) - 40, 236, px(0.096) - 4, 180)
s.text(px(0.096) - 44, 256, "alpha 0.096 → 0.457", "pl-label", "middle")
s.text(px(3.996), py(0.219) - 16, "0.219", "pl-note", "middle")
s.both(620, 462, "✓ ได้ alpha 0.096 · CV R² 0.457 · test R² 0.461", "✓ best alpha 0.096 · CV R² 0.457 · test R² 0.461", "ml-ok")
s.both(620, 494, "ให้ช่วง 0.001–100 และจำนวนครั้ง N = 10", "you give the range 0.001–100 and N = 10 tries", "pl-note")
s.both(20, 560, "ต้องฝึกกี่โมเดล · grid: จำนวนค่าคูณกัน hyperparameter 4 ตัว ตัวละ 5 ค่า = 5⁴ = 625 โมเดล (cv=5 คือฝึก 3,125 ครั้ง)",
       "How many models? Grid: the lists multiply: 4 hyperparameters × 5 values = 5⁴ = 625 models (3,125 trainings with cv=5)", "pl-text")
s.both(20, 590, "random: เท่ากับ N ที่เราเลือกเสมอ ไม่ว่าจะมี hyperparameter กี่ตัว",
       "Random: always the N you choose, however many hyperparameters there are", "pl-text")
s.save("l10-grid-vs-random.svg", 606)

# ================================================================ L11-S06: a line inside a sigmoid (100 kg)
B0, B1 = -109.42, 1.1195
s = Svg(W, "Logistic regression for a person weighing 100 kg. 1 The straight line: z = −109.42 + 1.1195 × 100 = 2.53, and z can be "
           "any number. 2 The sigmoid squeezes it: σ(2.53) = 0.93, always between 0 and 1. 3 The threshold: 0.93 is at least "
           "0.5, so the model predicts obese.")
s.bubble("คนหนัก 100 กก. อ้วนไหม", "A person weighs 100 kg. Obese?")
PW = 364
for i in range(3):
    s.box(20 + i * (PW + 24), 70, PW, 380, "nt-band-a", 14)
# 1 the line
X0 = 20
s.badge(X0 + 32, 96, 1)
s.both(X0 + 54, 102, "เส้นตรง: z = b₀ + b₁ × น้ำหนัก", "Line: z = b₀ + b₁ × weight", "pl-label")
gx = lambda w: X0 + 60 + (w - 90) / 20 * 270
gz = lambda z: 320 - (z + 10) / 24 * 170
s.line(X0 + 50, gz(0), X0 + 340, gz(0), "dg-rule")
s.text(X0 + 44, gz(0) + 6, "0", "pl-note", "end")
s.line(X0 + 50, 330, X0 + 340, 330, "dg-rule-strong")
s.line(X0 + 50, 140, X0 + 50, 330, "dg-rule-strong")
s.text(X0 + 44, 150, "z", "pl-label", "end")
s.raw(f'<path d="M{gx(90):.1f} {gz(B0 + B1 * 90):.1f} L{gx(110):.1f} {gz(B0 + B1 * 110):.1f}" class="pl-line"/>')
for w in (90, 100, 110):
    s.text(gx(w), 352, f"{w} kg" if w == 100 else str(w), "pl-label" if w == 100 else "pl-note", "middle")
z100 = B0 + B1 * 100
s.line(gx(100), 330, gx(100), gz(z100), dashed=True)
s.line(X0 + 50, gz(z100), gx(100), gz(z100), dashed=True)
s.raw(f'<circle cx="{gx(100):.1f}" cy="{gz(z100):.1f}" r="8" class="ml-bar-top"/>')
s.text(X0 + 58, gz(z100) - 10, "z = 2.53", "pl-label")
s.text(X0 + 20, 390, "−109.42 + 1.1195 × 100 = 2.53", "pl-text")
s.both(X0 + 20, 420, "z เป็นเลขอะไรก็ได้ (−∞ ถึง +∞)", "z can be any number (−∞ to +∞)", "pl-note")
# 2 the sigmoid
X0 = 20 + PW + 24
s.badge(X0 + 32, 96, 2)
s.both(X0 + 54, 102, "sigmoid: p̂ = σ(z)", "Sigmoid: p̂ = σ(z)", "pl-label")
s.text(X0 + 20, 132, "σ(z) = 1 / (1 + e^(−z))", "dg-code")
sx = lambda z: X0 + 60 + (z + 6) / 12 * 280
sp = lambda p: 320 - p * 170
s.line(X0 + 50, 330, X0 + 350, 330, "dg-rule-strong")
s.line(X0 + 50, 140, X0 + 50, 330, "dg-rule-strong")
s.line(X0 + 50, sp(1), X0 + 350, sp(1), "dg-rule")
s.line(X0 + 50, sp(0), X0 + 350, sp(0), "dg-rule")
s.text(X0 + 44, sp(1) + 6, "1", "pl-note", "end")
s.text(X0 + 44, sp(0) + 6, "0", "pl-note", "end")
pts = " ".join(f"{sx(z / 10):.1f},{sp(1 / (1 + math.exp(-z / 10))):.1f}" for z in range(-60, 61, 3))
s.raw(f'<polyline points="{pts}" class="pl-line"/>')
p100 = 1 / (1 + math.exp(-z100))
for z in (-6, 0, 6):
    s.text(sx(z), 352, str(z).replace("-", "−"), "pl-note", "middle")
s.line(sx(z100), 330, sx(z100), sp(p100), dashed=True)
s.line(X0 + 50, sp(p100), sx(z100), sp(p100), dashed=True)
s.raw(f'<circle cx="{sx(z100):.1f}" cy="{sp(p100):.1f}" r="8" class="ml-bar-top"/>')
s.text(sx(z100) - 10, 290, "z = 2.53", "pl-label", "end")
s.text(X0 + 58, sp(p100) + 26, "p̂ = 0.93", "pl-label")
s.text(X0 + 20, 390, "σ(2.53) = 0.93", "pl-text")
s.both(X0 + 20, 420, "อยู่ระหว่าง 0 ถึง 1 เสมอ", "always between 0 and 1", "pl-note")
# 3 the threshold
X0 = 20 + 2 * (PW + 24)
s.badge(X0 + 32, 96, 3)
s.both(X0 + 54, 102, "threshold 0.5", "Threshold 0.5", "pl-label")
gy = lambda p: 320 - p * 170
s.box(X0 + 60, gy(1), 50, 170, "ml-cell", 8)
s.box(X0 + 60, gy(p100), 50, gy(0) - gy(p100), "ml-bar", 8)
s.line(X0 + 46, gy(0.5), X0 + 124, gy(0.5), "ml-cut")
s.text(X0 + 40, gy(0.5) + 6, "0.5", "pl-label", "end")
s.text(X0 + 40, gy(1) + 6, "1", "pl-note", "end")
s.text(X0 + 40, gy(0) + 6, "0", "pl-note", "end")
s.arrow(X0 + 156, gy(p100), X0 + 116, gy(p100))
s.text(X0 + 162, gy(p100) + 6, "p̂ = 0.93", "pl-label")
s.both(X0 + 132, gy(0.5) - 34, "≥ 0.5 → กลุ่ม 1 (อ้วน)", "≥ 0.5 → class 1 (obese)", "pl-text")
s.both(X0 + 132, gy(0.5) + 34, "< 0.5 → กลุ่ม 0", "< 0.5 → class 0", "pl-note")
s.both(X0 + 20, 390, "✓ 0.93 ≥ 0.5 → ทำนายว่าอ้วน", "✓ 0.93 ≥ 0.5 → predict obese", "ml-ok")
s.both(X0 + 20, 420, "ค่าตั้งต้นของ threshold คือ 0.5", "0.5 is the default threshold", "pl-note")
for i in range(2):
    xa = 20 + (i + 1) * (PW + 24) - 24
    s.arrow(xa - 2, 240, xa + 22, 240)
s.both(20, 488, "การฝึก (fit) หาค่า b₀ = −109.42 และ b₁ = 1.1195 จากคน 108 คน · ขั้น ① ② ③ ทำซ้ำได้กับทุกน้ำหนัก",
       "Training (fit) finds b₀ = −109.42 and b₁ = 1.1195 from the 108 people · steps ① ② ③ work for any weight", "pl-note")
s.save("l11-line-in-sigmoid.svg", 504)

# ================================================================ L11-S09: softmax for one real person
CLS = [("Normal Weight", 1.78, 5.93, 0.73), ("Obese", -0.57, 0.56, 0.07), ("Overweight", 0.34, 1.41, 0.17), ("Underweight", -1.55, 0.21, 0.03)]
s = Svg(W, "Softmax for a 36-year-old man, 190 cm, 75 kg, really Normal Weight. 1 The model gives each group a score z: "
           "Normal Weight 1.78, Obese −0.57, Overweight 0.34, Underweight −1.55. 2 e to the power z makes them positive: "
           "5.93, 0.56, 1.41, 0.21, sum 8.11. 3 Dividing by the sum gives probabilities that add up to 1: 0.73, 0.07, 0.17, 0.03. "
           "Normal Weight wins, which is right.")
s.bubble("ชาย 36 ปี สูง 190 ซม. หนัก 75 กก.: อยู่กลุ่มไหน", "A man, 36, 190 cm, 75 kg: which weight group?")
s.text(W / 2, 92, "P(group j) = e^(z_j) / (e^(z_1) + e^(z_2) + e^(z_3) + e^(z_4))", "pl-label", "middle")
HEADS = [(250, "คะแนน z ของแต่ละกลุ่ม", "Score z of each group"), (580, "ยก e กำลัง z", "Raise e to z"), (880, "หารด้วยผลรวม 8.11", "Divide by the sum 8.11")]
for k, (x, th, en) in enumerate(HEADS):
    s.badge(x + 12, 128, k + 1)
    s.both(x + 34, 134, th, en, "pl-label")
Z0, ZS = 370, 56
s.line(Z0, 152, Z0, 392, "dg-rule-strong")
for k, (name, z, ez, p) in enumerate(CLS):
    y = 176 + k * 56
    win = k == 0
    if win:
        s.box(14, y - 22, W - 28, 52, "rc-res", 10)
    s.text(30, y + 10, name, "pl-label" if win else "pl-text")
    cls = "ml-bar-top" if win else "ml-bar"
    if z >= 0:
        s.box(Z0, y - 8, z * ZS, 26, cls, 3)
        s.text(Z0 + z * ZS + 8, y + 11, f"{z:.2f}", "pl-label" if win else "pl-text")
    else:
        s.box(Z0 + z * ZS, y - 8, -z * ZS, 26, cls, 3)
        s.text(Z0 + z * ZS - 8, y + 11, f"{z:.2f}".replace("-", "−"), "pl-text", "end")
    s.box(600, y - 8, ez * 30, 26, cls, 3)
    s.text(608 + ez * 30, y + 11, f"{ez:.2f}", "pl-label" if win else "pl-text")
    s.box(900, y - 8, p * 260, 26, cls, 3)
    s.text(908 + p * 260, y + 11, f"{p:.2f}", "pl-label" if win else "pl-text")
for xa in (520, 830):
    s.arrow(xa, 270, xa + 40, 270)
s.both(250, 418, "ติดลบได้", "can be negative", "pl-note")
s.both(600, 418, "เป็นบวกเสมอ · รวม = 8.11", "always positive · sum = 8.11", "pl-note")
s.both(900, 418, "รวมกันได้ 1.00", "add up to 1.00", "pl-note")
s.both(20, 462, "✓ Normal Weight ได้สูงสุด 5.93 / 8.11 = 0.73 โมเดลตอบ Normal Weight ซึ่งถูก",
       "✓ Normal Weight is highest, 5.93 / 8.11 = 0.73: the model answers Normal Weight, which is right", "ml-ok")
s.save("l11-softmax.svg", 478)

# ================================================================ L11-S10: the four training steps on the obesity data
s = Svg(W, "Training the obesity model in four steps. 1 Encode: Gender Male, Female, Male becomes Gender_Male 1, 0, 1. "
           "2 Split the 108 people into 75 for training and 33 for testing. 3 Scale: fit the scaler on the training set only "
           "(Height mean 165.3, sd 27.0), then use it on both; 175 cm becomes 0.36. Fitting it on all 108 would leak the test "
           "set. 4 Fit on train and predict a test person (60, 120 cm, 70 kg, female): Normal Weight 0.552, Overweight 0.360, "
           "Underweight 0.085, Obese 0.003, so Normal Weight, which is right. 27 of the 33 test people are right (0.82).")
s.bubble("ฝึกด้วย 75 คน แล้วทายภาวะน้ำหนักของอีก 33 คน", "Train on 75 people, then predict the other 33")
P = [(20, 70), (600, 70), (20, 300), (600, 300)]
PW, PH = 560, 214
TITLES = [("แปลงข้อความเป็นตัวเลข", "Turn text into numbers"), ("แบ่ง train / test", "Split train / test"),
          ("ปรับสเกล: fit กับ train เท่านั้น", "Scale: fit on train only"), ("ฝึก แล้วทาย", "Fit, then predict")]
for k, ((x, y), (th, en)) in enumerate(zip(P, TITLES)):
    s.panel(x, y, PW, PH, "nt-band-a", th, en, k + 1)
# 1 encode
x, y = P[0]
for j, (head, vals, cx, w) in enumerate((("Gender", ["Male", "Female", "Male"], x + 30, 116), ("Gender_Male", ["1", "0", "1"], x + 206, 146))):
    s.box(cx, y + 58, w, 140, "ml-cell", 8)
    s.raw(f'<path d="M{cx + 6} {y + 94} H{cx + w - 6}" class="dg-rule"/>')
    s.text(cx + w / 2, y + 83, head, "pl-label", "middle")
    for i, v in enumerate(vals):
        s.text(cx + w / 2, y + 122 + i * 30, v, "pl-text", "middle")
s.arrow(x + 154, y + 128, x + 198, y + 128)
s.text(x + 372, y + 90, "get_dummies", "dg-code")
s.both(x + 372, y + 124, "1 = Male", "1 = Male", "pl-note")
s.both(x + 372, y + 152, "0 = Female", "0 = Female", "pl-note")
s.both(x + 372, y + 186, "คอลัมน์เดียวพอ", "one column is enough", "pl-note")
# 2 split
x, y = P[1]
tw = 75 / 108 * 500
s.box(x + 30, y + 64, tw, 50, "rc-res", 8)
s.box(x + 30 + tw, y + 64, 500 - tw, 50, "rc-ctx", 8)
for i in range(1, 108, 4):
    xx = x + 30 + i / 108 * 500
    s.raw(f'<path d="M{xx:.1f} {y + 70} V{y + 108}" class="dg-rule"/>')
s.both(x + 30 + tw / 2, y + 96, "train 75 คน", "train: 75 people", "pl-label", "middle")
s.both(x + 30 + tw + (500 - tw) / 2, y + 96, "test 33 คน", "test: 33", "pl-label", "middle")
s.both(x + 30, y + 146, "โมเดลเรียนจากชุดนี้", "the model learns from these", "pl-note")
s.both(x + 530, y + 146, "เก็บไว้วัดผล", "kept for scoring", "pl-note", "end")
s.text(x + 30, y + 186, "train_test_split(X, y, test_size=0.3)", "dg-code")
# 3 scale
x, y = P[2]
s.box(x + 24, y + 58, 108, 40, "rc-res", 8)
s.text(x + 78, y + 84, "train", "pl-label", "middle")
s.box(x + 196, y + 54, 168, 48, "ml-cell-b", 10)
s.text(x + 280, y + 84, "StandardScaler", "ml-b", "middle")
s.box(x + 428, y + 58, 108, 40, "rc-ctx", 8)
s.text(x + 482, y + 84, "test", "pl-label", "middle")
s.arrow(x + 136, y + 78, x + 192, y + 78)
s.text(x + 164, y + 70, "fit", "dg-code", "middle")
s.arrow(x + 368, y + 78, x + 424, y + 78)
s.both(x + 396, y + 122, "ใช้ตัวเดิม", "same scaler", "dg-code", "middle")
s.both(x + 24, y + 144, "Height ใน train: mean 165.3 · sd 27.0", "Height in train: mean 165.3 · sd 27.0", "pl-note")
s.text(x + 24, y + 172, "175 cm → (175 − 165.3) / 27.0 = 0.36", "pl-text")
s.both(x + 24, y + 200, "✗ fit กับทั้ง 108 คน = ชุด test รั่วเข้ามา", "✗ fit on all 108 = the test set leaks in", "ml-neg")
# 4 fit and predict
x, y = P[3]
s.box(x + 24, y + 54, 166, 140, "rc-ctx", 10)
s.both(x + 38, y + 80, "คนใน test", "a test person", "pl-label")
for i, (th, en) in enumerate((("อายุ 60 · หญิง", "60, female"), ("120 ซม. · 70 กก.", "120 cm, 70 kg"), ("จริง: Normal", "really: Normal"))):
    s.both(x + 38, y + 112 + i * 28, th, en, "pl-text" if i < 2 else "pl-note")
s.arrow(x + 196, y + 120, x + 216, y + 120)
PROBA = [("Normal Weight", 0.552), ("Overweight", 0.360), ("Underweight", 0.085), ("Obese", 0.003)]
for i, (name, p) in enumerate(PROBA):
    yy = y + 62 + i * 30
    s.text(x + 222, yy + 16, name, "ml-b" if i == 0 else "ml-i")
    s.box(x + 348, yy + 3, max(p * 280, 2), 18, "ml-bar-top" if i == 0 else "ml-bar", 3)
    s.text(x + 354 + max(p * 280, 2), yy + 17, f"{p:.3f}", "ml-b" if i == 0 else "ml-i")
s.both(x + 222, y + 200, "✓ ทาย Normal Weight: ถูก", "✓ predicts Normal Weight: right", "ml-ok")
s.both(20, 548, "ผลกับ 33 คนใน test: ทายถูก 27 คน (accuracy 0.82)", "On the 33 test people: 27 right (accuracy 0.82)", "ml-ok")
s.save("l11-train-steps.svg", 564)

# ================================================================ L11-S12: the confusion matrix as people
s = Svg(W, "The confusion matrix of the weight model on its 33 test people, with Overweight as the positive class. "
           "TP 4: said Overweight and right. FN 5: really Overweight but said other (all 5 were called Normal Weight), a "
           "Type II error. FP 0: said Overweight but wrong, a Type I error. TN 24: said other and right.")
s.bubble("โมเดลภาวะน้ำหนัก ชุด test 33 คน: ใครเป็น Overweight", "The weight model, 33 test people: who is Overweight?")
C1, C2, CW = 250, 590, 330
R1, R2, RH = 128, 300, 162
s.both(C1 + CW / 2, 116, "ทายว่า Overweight", "said Overweight", "pl-label", "middle")
s.both(C2 + CW / 2, 116, "ทายว่ากลุ่มอื่น", "said another group", "pl-label", "middle")
s.both(C1 - 18, R1 + RH / 2 - 4, "Overweight จริง", "really Overweight", "pl-label", "end")
s.both(C1 - 18, R1 + RH / 2 + 22, "9 คน", "9 people", "pl-note", "end")
s.both(C1 - 18, R2 + RH / 2 - 4, "จริงเป็นกลุ่มอื่น", "really another group", "pl-label", "end")
s.both(C1 - 18, R2 + RH / 2 + 22, "24 คน", "24 people", "pl-note", "end")
CELLS = [  # x, y, fill, key, n, dot, th, en
    (C1, R1, "rc-res", "TP = 4", 4, "ml-ok", "ทายว่าบวก และถูก", "said positive, right"),
    (C2, R1, "sw-warn-box", "FN = 5", 5, "ml-bar-top", "ทายว่าลบ แต่ผิด · Type II", "said negative, wrong · Type II"),
    (C1, R2, "sw-warn-box", "FP = 0", 0, "ml-bar-top", "ทายว่าบวก แต่ผิด · Type I", "said positive, wrong · Type I"),
    (C2, R2, "ml-cell", "TN = 24", 24, "ml-bar", "ทายว่าลบ และถูก", "said negative, right"),
]
for x, y, fill, key, n, dot, th, en in CELLS:
    s.box(x, y, CW, RH - 10, fill, 12)
    s.text(x + 18, y + 32, key, "rc-key")
    s.both(x + 18, y + 58, th, en, "pl-note")
    for i in range(n):
        r, c = divmod(i, 12)
        s.person(x + 30 + c * 25, y + 92 + r * 30, dot)
    if n == 0:
        s.both(x + 18, y + 100, "ไม่มีเลย", "nobody", "pl-text")
s.arrow(C2 + CW + 30, R1 + 86, C2 + CW - 8, R1 + 86)
for i, (th, en, cls) in enumerate((("Overweight 5 คน", "5 Overweight people", "ml-neg"), ("ถูกทายว่า", "were called", "pl-text"),
                                  ("Normal Weight", "Normal Weight", "pl-text"), ("= พลาด", "= missed", "ml-neg"))):
    s.both(C2 + CW + 36, R1 + 60 + i * 26, th, en, cls)
s.both(20, 500, "อ่านชื่อช่อง: คำแรก (True / False) = ทายถูกไหม · คำหลัง (Positive / Negative) = โมเดลทายว่าอะไร",
       "Read a cell's name: the 1st word (True / False) = was the guess right? · the 2nd (Positive / Negative) = what the model said", "pl-note")
s.save("l11-confusion-people.svg", 516)

# ================================================================ L11-S13: precision looks down a column, recall along a row
s = Svg(W, "Precision and recall of the weight model for Overweight (TP 4, FN 5, FP 0, TN 24). Precision looks down the "
           "'said Overweight' column: 4 / (4 + 0) = 1.00, every yes was right. Recall looks along the 'really Overweight' "
           "row: 4 / (4 + 5) = 0.44, it caught only 4 of 9. F1 = 0.615. Accuracy (4 + 24) / 33 = 0.848 hides the 5 misses.")
s.bubble("Overweight = กลุ่มบวก: TP 4 · FN 5 · FP 0 · TN 24", "Overweight is positive: TP 4 · FN 5 · FP 0 · TN 24")


def matrix(x0, hi):
    """A 2×2 matrix; hi = 'col' lights the predicted-positive column, 'row' the actually-positive row."""
    mx, my, cw, ch = x0 + 196, 168, 160, 84
    s.both(mx + cw / 2, my - 12, "ทาย Overweight", "said Overweight", "ml-b", "middle")
    s.both(mx + cw + 8 + cw / 2, my - 12, "ทายกลุ่มอื่น", "said other", "ml-i", "middle")
    s.both(mx - 12, my + ch / 2 + 6, "Overweight จริง", "really Overweight", "ml-b", "end")
    s.both(mx - 12, my + ch + 8 + ch / 2 + 6, "จริงเป็นกลุ่มอื่น", "really other", "ml-i", "end")
    for (r, c), key in {(0, 0): "TP 4", (0, 1): "FN 5", (1, 0): "FP 0", (1, 1): "TN 24"}.items():
        lit = (hi == "col" and c == 0) or (hi == "row" and r == 0)
        x, y = mx + c * (cw + 8), my + r * (ch + 8)
        cls = "ml-cell"
        if lit:
            cls = "rc-res" if key == "TP 4" else "sw-chip-warn"
        s.box(x, y, cw, ch, cls, 10)
        s.text(x + cw / 2, y + ch / 2 + 8, key, "rc-key" if lit else "pl-note", "middle")
    s.raw(f'<rect x="{mx - 5}" y="{my - 5}" width="{(cw + 10) if hi == "col" else (2 * cw + 18)}" height="{(2 * ch + 18) if hi == "col" else (ch + 10)}" rx="14" fill="none" class="pl-line"/>')


s.panel(20, 70, 560, 420, "nt-band-a", "Precision: ที่ทายว่าใช่ ถูกกี่ส่วน", "Precision: of its yeses, how many right?")
matrix(20, "col")
s.text(40, 402, "4 / (4 + 0) = 1.00", "pl-label")
s.both(40, 436, "TP / (TP + FP) · ดูคอลัมน์ “ทาย Overweight”", "TP / (TP + FP) · down the “said Overweight” column", "pl-note")
s.both(40, 470, "✓ ทุกครั้งที่บอก Overweight ถูกหมด", "✓ every “Overweight” it said was right", "ml-ok")
s.panel(600, 70, 560, 420, "sw-warn-box", "Recall: ที่ใช่จริง จับได้กี่ส่วน", "Recall: of the real ones, how many caught?")
matrix(600, "row")
s.text(620, 402, "4 / (4 + 5) = 0.44", "pl-label")
s.both(620, 436, "TP / (TP + FN) · ดูแถว “Overweight จริง”", "TP / (TP + FN) · along the “really Overweight” row", "pl-note")
s.both(620, 470, "✗ จับได้แค่ 4 จาก 9 คน", "✗ caught only 4 of the 9", "ml-neg")
s.text(20, 530, "F1 = 2 × 1.00 × 0.444 / (1.00 + 0.444) = 0.615", "pl-label")
s.both(520, 530, "ค่าหนึ่งต่ำ F1 ก็ต่ำตาม", "one low value pulls F1 down", "pl-note")
s.text(20, 562, "accuracy = (4 + 24) / 33 = 0.848", "pl-label")
s.both(370, 562, "ดูดี แต่ไม่บอกเลยว่าพลาดไป 5 คน", "looks good and says nothing about the 5 misses", "pl-note")
s.save("l11-precision-recall.svg", 578)

# ================================================================ L11-S15: the ATK question (no answers)
s = Svg(W, "A rapid antigen test as a classifier. Columns: the person has COVID, or not. Rows: the test shows 2 lines "
           "(says infected) or 1 line (says not infected). Each of the four cells is a question mark: which is TP, FP, FN, TN?")
s.bubble("กลุ่มบวก = เป็นโควิด · แต่ละช่องคือ TP, FP, FN หรือ TN", "Positive class = has COVID · is each cell TP, FP, FN or TN?")


def virus(cx, cy):
    for a in range(0, 360, 45):
        r = math.radians(a)
        s.raw(f'<path d="M{cx + 14 * math.cos(r):.1f} {cy + 14 * math.sin(r):.1f} L{cx + 22 * math.cos(r):.1f} {cy + 22 * math.sin(r):.1f}" class="pl-line"/>'
              f'<circle cx="{cx + 23 * math.cos(r):.1f}" cy="{cy + 23 * math.sin(r):.1f}" r="3" class="pl-dot"/>')
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="14" class="sw-chip-warn"/>')


def cassette(x, y, lines):
    s.box(x, y, 170, 70, "ml-cell", 18)
    s.box(x + 56, y + 28, 70, 30, "nt-bubble", 6)
    s.raw(f'<circle cx="{x + 28}" cy="{y + 43}" r="9" class="ml-cell"/>')
    s.text(x + 72, y + 22, "C", "ml-i", "middle")
    s.text(x + 106, y + 22, "T", "ml-i", "middle")
    s.raw(f'<path d="M{x + 72} {y + 32} V{y + 54}" class="ml-cut"/>')
    if lines == 2:
        s.raw(f'<path d="M{x + 106} {y + 32} V{y + 54}" class="ml-cut"/>')


C1, C2, CW = 420, 720, 280
R1, R2, RH = 150, 280, 120
s.person(C1 + CW / 2 - 50, 102, "pl-dot")
virus(C1 + CW / 2 - 18, 96)
s.both(C1 + CW / 2 + 14, 104, "เป็นโควิด", "has COVID", "pl-label")
s.person(C2 + CW / 2 - 40, 102, "ml-ok")
s.both(C2 + CW / 2 - 18, 104, "ไม่เป็นโควิด", "no COVID", "pl-label")
for (y, lines, th, en) in ((R1, 2, "2 ขีด: บอกว่าติดเชื้อ", "2 lines: says infected"), (R2, 1, "1 ขีด: บอกว่าไม่ติด", "1 line: says not infected")):
    cassette(40, y + 6, lines)
    s.both(40, y + 102, th, en, "pl-label")
    for cx in (C1, C2):
        s.box(cx, y, CW, RH - 10, "ml-cell", 12)
        s.text(cx + CW / 2, y + RH / 2 + 6, "?", "ml-plus", "middle")
s.save("l11-atk-question.svg", 410, sized=True)

# ================================================================ L11-S16: per-class counts in a 3×3 matrix
M = [[4, 1, 0], [0, 3, 1], [1, 1, 3]]
NAMES = "ABC"
STATS = [(4, 1, 1, "4/5 = 0.80", "4/5 = 0.80"), (3, 2, 1, "3/5 = 0.60", "3/4 = 0.75"), (3, 1, 2, "3/4 = 0.75", "3/5 = 0.60")]
s = Svg(W, "Per-author counts in the 3 × 3 confusion matrix of 14 texts. For each author, TP is its diagonal cell, FP the rest "
           "of its column, FN the rest of its row. Author A: TP 4, FP 1, FN 1, precision 0.80, recall 0.80. Author B: TP 3, "
           "FP 2, FN 1, precision 0.60, recall 0.75. Author C: TP 3, FP 1, FN 2, precision 0.75, recall 0.60. Macro average "
           "precision (0.80 + 0.60 + 0.75) / 3 = 0.72; micro average pools TP 10, FP 4, FN 4: 10 / 14 = 0.71, the accuracy.")
s.bubble("ข้อความ 14 ชิ้น ผู้แต่ง 3 คน: โมเดลเก่งกับผู้แต่งแต่ละคนแค่ไหน", "14 texts, 3 authors: how good is the model for each author?")
PW = 364
for k in range(3):
    X0 = 20 + k * (PW + 24)
    s.box(X0, 70, PW, 360, "nt-band-a", 14)
    s.both(X0 + 20, 102, f"ผู้แต่ง {NAMES[k]} เป็นกลุ่มบวก", f"Author {NAMES[k]} as positive", "pl-label")
    mx, my, cw, ch = X0 + 126, 162, 66, 44
    s.both(mx + 1.5 * cw, 132, "ทาย →", "predicted →", "ml-i", "middle")
    s.both(X0 + 20, my + 1.5 * ch + 6, "จริง ↓", "real ↓", "ml-i")
    for j in range(3):
        s.text(mx + j * cw + cw / 2, my - 8, NAMES[j], "ml-b", "middle")
        s.text(mx - 14, my + j * ch + ch / 2 + 6, NAMES[j], "ml-b", "end")
    for r in range(3):
        for c in range(3):
            if r == k and c == k:
                cls = "rc-res"
            elif c == k:
                cls = "sw-chip-warn"
            elif r == k:
                cls = "rc-ctx"
            else:
                cls = "ml-cell"
            s.box(mx + c * cw + 2, my + r * ch + 2, cw - 4, ch - 4, cls, 6)
            s.text(mx + c * cw + cw / 2, my + r * ch + ch / 2 + 7, str(M[r][c]), "pl-label" if cls != "ml-cell" else "pl-note", "middle")
    tp, fp, fn, prec, rec = STATS[k]
    s.text(X0 + 20, 346, f"TP {tp} · FP {fp} · FN {fn}", "pl-label")
    s.text(X0 + 20, 378, f"precision = {prec}", "pl-text")
    s.text(X0 + 20, 408, f"recall = {rec}", "pl-text")
LEG = [("rc-res", "TP: ช่องทแยงของกลุ่มนั้น", "TP: the class's diagonal cell"),
       ("sw-chip-warn", "FP: ที่เหลือในคอลัมน์ (ทายว่าใช่ แต่ผิด)", "FP: rest of its column (said it, wrong)"),
       ("rc-ctx", "FN: ที่เหลือในแถว (ใช่จริง แต่พลาด)", "FN: rest of its row (really it, missed)")]
lx = 20
for cls, th, en in LEG:
    s.box(lx, 452, 22, 22, cls, 4)
    s.both(lx + 30, 470, th, en, "pl-note")
    lx += 30 + max(width(th, 18), width(en, 18)) + 34
s.both(20, 512, "macro: เฉลี่ยของ 3 คน precision = (0.80 + 0.60 + 0.75) / 3 = 0.72 · ทุกคนนับเท่ากัน",
       "Macro: the mean of the 3 authors, precision = (0.80 + 0.60 + 0.75) / 3 = 0.72 · every author counts the same", "pl-text")
s.both(20, 544, "micro: รวมตัวนับก่อน TP 10 · FP 4 · FN 4 → 10 / 14 = 0.71 = accuracy",
       "Micro: pool the counts first, TP 10 · FP 4 · FN 4 → 10 / 14 = 0.71 = accuracy", "pl-text")
s.save("l11-multiclass-metrics.svg", 560)
