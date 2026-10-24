"""Concept pictures for stats-dh lessons 10 (model tuning) and 11 (logistic regression), in the style of
nlp l12-why-chunk.svg: the running example's question on top, panels answering that same question, drawn
objects (column strips, a slider, score curves, S-curves, confusion matrices of people), arrows at the
exact spot, the real numbers attached to what they describe. ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/stats_l10_l11_concepts.py courses/stats-dh/images

Every number is a real run in course/.venv, the same as the lessons' code cells:
  L10 students (UCI Student Performance, math course, the 357 students who sat the final exam; 10 columns age, Medu,
      Fedu, studytime, failures, goout, Dalc, Walc, absences, term1_grade; target final_grade; 80/20 split, random_state=42; train 285):
      LinearRegression test R² 0.801 on all 10 columns, 0.807 on age, absences, term1_grade. r with final_grade on the training set:
      term1_grade .89, failures −.29, absences −.20, Walc −.20, goout −.17, Medu .16, Fedu .15, Dalc −.15, studytime .13,
      age −.13. Forward SFS (cv=5): term1_grade 0.794, + absences 0.804, + age 0.809 (10 + 9 + 8 = 27 sets × 5 folds = 135
      trainings); the filter's top 3 (term1_grade, failures, absences) score 0.800. Lasso on standardised columns, alpha 0.3:
      β term1_grade 2.60, absences −0.06, age −0.05, the other 7 exactly 0, CV R² 0.788. Lasso CV R²: alpha 0.001 0.796,
      0.01 0.798, 0.1 0.803, 1 0.700, 10 and 100 −0.011; the curve is 41 alphas on a log grid. RandomizedSearchCV
      (loguniform(0.001, 100), n_iter=10, random_state=1) tries 0.001 0.003 0.005 0.009 0.032 0.053 0.096 0.122
      0.494 3.996, best 0.096 (CV R² 0.803); both searches give test R² 0.805.
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
s = Svg(W, "Model tuning on the student data, same linear model. 1 Feature selection changes which columns it learns from: "
           "keep age, absences and term1_grade and drop the other 7, and the test R² rises from 0.801 (all 10) to 0.807. 2 "
           "Hyperparameter tuning changes how it learns: Lasso with all 10 columns scores CV R² 0.796, 0.798, 0.803, 0.700, "
           "−0.011 and −0.011 for alpha 0.001, 0.01, 0.1, 1, 10 and 100; the best is alpha 0.1.")
s.bubble("นักเรียน 357 คน โมเดล linear เดิม: ทายเกรดปลายปีให้แม่นขึ้นได้ไหม",
         "357 students, the same linear model: can we predict the final grade better?")
# 1. feature selection: ten column strips, three kept
s.panel(20, 70, 560, 370, "nt-band-a", "Feature selection: เรียนจากคอลัมน์ไหน", "Feature selection: which columns it learns from", 1)
s.both(40, 128, "10 คอลัมน์ = 10 feature", "10 columns = 10 features", "pl-note")
COLS = ["age", "Medu", "Fedu", "studytime", "failures", "goout", "Dalc", "Walc", "absences", "term1_grade"]
KEEP = {"age", "absences", "term1_grade"}
for k, c in enumerate(COLS):
    x = 46 + k * 51
    keep = c in KEEP
    s.box(x, 190, 42, 136, "rc-res" if keep else "pl-chip-del", 6)
    for yy in range(204, 320, 16):
        if keep:
            s.box(x + 8, yy, 26, 4, "ml-bar", 2)
        else:
            s.raw(f'<path d="M{x + 8} {yy + 2} H{x + 34}" class="dg-rule"/>')
    s.text(x + 21, 182 if k % 2 == 0 else 160, c, "ml-b" if keep else "ml-i", "middle")
    s.text(x + 21, 352, "✓" if keep else "✗", "ml-ok" if keep else "ml-neg", "middle")
s.both(40, 392, "✓ เก็บ age, absences, term1_grade ตัดอีก 7", "✓ keep age, absences, term1_grade; drop the other 7", "ml-ok")
s.both(40, 420, "test R² 0.801 (10 คอลัมน์) → 0.807 (3 คอลัมน์)", "test R² 0.801 (10 columns) → 0.807 (3 columns)", "pl-text")
# 2. hyperparameter tuning: a slider for alpha, a CV R² bar under each stop
s.panel(600, 70, 560, 370, "nt-band-b", "Hyperparameter: เรียนอย่างไร", "Hyperparameter: how it learns", 2)
s.both(620, 128, "ครบ 10 คอลัมน์ · Lasso(alpha=…) · แท่ง = CV R²", "all 10 columns · Lasso(alpha=…) · bars = CV R²", "pl-note")
ALPHAS = [(0.001, 0.796), (0.01, 0.798), (0.1, 0.803), (1, 0.700), (10, -0.011), (100, -0.011)]
ax = lambda a: logx(a, 670, 90)
s.raw(f'<path d="M{ax(0.001) - 14:g} 176 H{ax(100) + 14:g}" class="dg-rule-strong" stroke-width="6" stroke-linecap="round"/>')
for a, r2 in ALPHAS:
    x = ax(a)
    s.line(x, 168, x, 184, "dg-rule-strong")
    s.text(x, 206, f"{a:g}", "pl-note", "middle")
    best = a == 0.1
    base, sc = 400, 190
    hgt = r2 * sc
    s.box(x - 18, base - max(hgt, 0), 36, max(abs(hgt), 2), "ml-bar-top" if best else "ml-bar", 3)
    s.text(x, base - max(hgt, 0) - 8, f"{r2:.3f}".replace("-", "−"), "pl-label" if best else "pl-note", "middle")
s.line(650, 400, 1140, 400, "dg-rule-strong")
s.raw(f'<circle cx="{ax(0.1):g}" cy="176" r="12" class="ml-bar-top"/>')
s.both(ax(0.1) + 18, 160, "alpha = 0.1", "alpha = 0.1", "pl-label")
s.both(620, 424, "✓ alpha 0.1 ดีที่สุด (0.803) · alpha 10 พัง (−0.011)", "✓ alpha 0.1 is best (0.803) · alpha 10 fails (−0.011)", "ml-ok")
s.both(20, 472, "ทั้งสองแบบเปลี่ยนสิ่งเดียว ไม่เปลี่ยนชนิดของโมเดล และวัดกับข้อมูลที่โมเดลไม่เคยเห็น (CV หรือชุด test)",
       "Each changes one thing, never the kind of model, and is scored on data the model has not seen (CV or the test set)", "pl-note")
s.save("l10-two-tools.svg", 488)

# ================================================================ L10-S03: the checklist on the student table
# The first 4 students of the lesson's data (UCI Student Performance, math class, final_grade > 0) with more of their real columns
# (reason, Mjob, term2_grade) and two added ones: student_id (a row number) and course ("math": the file holds only the math class).
# Over the 357 students: final_grade mean 11.3–11.8 for every reason; r(term2_grade, final_grade) = 0.97; r(Dalc, Walc) = 0.64.
STUD = [  # column, width, verdict (keep/drop/flag/target), badge, values
    ("student_id", 104, "drop", 2, ["1", "2", "3", "4"]),
    ("reason", 80, "drop", 1, ["course", "course", "other", "home"]),
    ("studytime", 98, "keep", None, ["2", "2", "2", "3"]),
    ("absences", 92, "keep", None, ["6", "4", "10", "2"]),
    ("Mjob", 84, "keep", 4, ["at_home", "at_home", "at_home", "health"]),
    ("course", 70, "drop", 5, ["math", "math", "math", "math"]),
    ("Dalc", 52, "flag", 6, ["1", "1", "2", "1"]),
    ("Walc", 52, "flag", 6, ["1", "1", "3", "1"]),
    ("term1_grade", 112, "keep", None, ["5", "5", "7", "15"]),
    ("term2_grade", 112, "drop", 3, ["6", "5", "8", "14"]),
    ("final_grade", 106, "target", None, ["6", "6", "10", "15"]),
]
s = Svg(W, "The six-question checklist on the student table, predicting the final grade final_grade at the end of term 1. reason fails "
           "question 1 (about the school, not the student; grades barely differ by reason); student_id fails question 2 "
           "(noise: a row number); term2_grade fails question 3 (the term 2 grade is not known yet: it leaks the answer); Mjob passes "
           "but is text, so question 4 turns it into 0/1 columns; course fails question 5 (math in every row); Dalc and Walc "
           "overlap (question 6, r = 0.64), so an algorithm should decide; studytime, absences and term1_grade are kept.")
s.bubble("จบเทอม 1 อยากทาย final_grade: คอลัมน์ไหนเป็น feature ได้", "End of term 1, predicting final_grade: which columns can be features?")
GAP = 4
total = sum(c[1] for c in STUD) + GAP * (len(STUD) - 1)
x = (W - total) / 2
TOP = 124
VERD = {"keep": ("✓", "✓", "ml-ok", "rc-res"), "drop": ("✗", "✗", "ml-neg", "sw-warn-box"),
        "flag": ("?", "?", "pl-label", "rc-ctx"), "target": ("y", "y", "pl-label", "ml-cell-b")}
s.both(W - 20, 76, "✓ เก็บ · ✗ ตัด · ? ดูต่อ · y = target", "✓ keep · ✗ drop · ? check · y = target", "pl-note", "end")
xs = {}
for name, w, verdict, badge, vals in STUD:
    th, en, tcls, fill = VERD[verdict]
    xs[name] = x + w / 2
    s.both(x + w / 2, 100, th, en, tcls, "middle")
    s.box(x, TOP, w, 200, fill, 8)
    s.raw(f'<path d="M{x + 6:g} {TOP + 40} H{x + w - 6:g}" class="dg-rule"/>')
    s.text(x + w / 2, TOP + 27, name, "pl-del" if verdict == "drop" else "pl-label", "middle")
    for k, v in enumerate(vals):
        s.text(x + w / 2, TOP + 68 + k * 38, v, "pl-note" if len(v) > 5 else "pl-text", "middle")
    if badge:
        s.line(x + w / 2, TOP + 204, x + w / 2, TOP + 230)
        s.badge(x + w / 2, TOP + 244, badge)
    x += w + GAP
NOTES = [
    (1, "ไม่เกี่ยวกับการเรียนของนักเรียน: reason คือเหตุผลที่ครอบครัวเลือกโรงเรียน (เกรดเฉลี่ย 11.3–11.8 ทุกเหตุผล)",
        "Not about the student's learning: reason = why the family chose the school (grades 11.3–11.8 for every reason)"),
    (2, "noise: student_id เป็นแค่เลขแถว ไม่ซ้ำกันเลยทุกแถว", "Noise: student_id is only a row number, different in every row"),
    (3, "รั่วคำตอบ: term2_grade คือเกรดเทอม 2 ได้มาหลายเดือนหลังจบเทอม 1 (r = 0.97 กับ final_grade)", "Leaks the answer: term2_grade, the term 2 grade, arrives months after term 1 (r = 0.97 with final_grade)"),
    (4, "ชนิดข้อมูล: Mjob (อาชีพแม่) เป็นข้อความ แปลงเป็นคอลัมน์ 0/1 ก่อน", "Type: Mjob (mother's job) is text, so turn it into 0/1 columns first"),
    (5, "ค่าคงที่: course เป็น math ทุกแถว (ไฟล์นี้มีแต่ชั้นคณิต)", "Constant: course is math in every row (this file is only the math class)"),
    (6, "ซ้ำกันบางส่วน: Dalc กับ Walc (r = 0.64) เก็บไว้ก่อน ให้อัลกอริทึมช่วยตัดสิน", "Overlap: Dalc and Walc (r = 0.64): keep both for now, let an algorithm decide"),
]
for k, (b, th, en) in enumerate(NOTES):
    y = 432 + k * 32
    s.badge(46, y - 6, b)
    s.both(68, y, th, en, "pl-note")
s.both(20, 636, "✓ feature: studytime, absences, Mjob (เป็น 0/1), Dalc, Walc, term1_grade · ✗ ตัด student_id, reason, course, term2_grade",
       "✓ features: studytime, absences, Mjob (as 0/1), Dalc, Walc, term1_grade · ✗ drop student_id, reason, course, term2_grade", "ml-ok")
s.save("l10-checklist-students.svg", 654)

# ================================================================ L10-S06: three families answer the same question
R = [("term1_grade", .89), ("failures", .29), ("absences", .20), ("Walc", .20), ("goout", .17), ("Medu", .16), ("Fedu", .15),
     ("Dalc", .15), ("studytime", .13), ("age", .13)]
LASSO = {"term1_grade": 2.60, "absences": -0.06, "age": -0.05}
s = Svg(W, "Three ways an algorithm picks student columns. 1 Filter ranks the columns by |r| with the final grade, no model, "
           "and keeps the top k = 3: term1_grade, failures, absences, CV R² 0.800, 0 trainings. 2 Wrapper (forward SFS) trains a "
           "model on each candidate set and adds the best column each round: term1_grade 0.794, + absences 0.804, + age 0.809, 135 "
           "trainings. 3 Embedded (Lasso, alpha 0.3, standardised columns) trains once and sets the β of 7 columns to "
           "exactly 0, keeping term1_grade 2.60, absences −0.06, age −0.05, CV R² 0.788.")
s.bubble("นักเรียน: ควรเก็บคอลัมน์ไหนจาก 10 ตัว", "Students: which of the 10 columns should we keep?")
PW, PT, PH = 364, 70, 450
ROW0, RH = 162, 25
for i in range(3):
    s.box(20 + i * (PW + 24), PT, PW, PH, "nt-band-a", 14)
# 1 filter
X0 = 20
s.badge(X0 + 32, PT + 26, 1)
s.both(X0 + 54, PT + 32, "Filter: ใช้สถิติอย่างเดียว", "Filter: statistics only", "pl-label")
s.both(X0 + 20, PT + 60, "|r| กับเกรดปลายปี ไม่ต้องฝึกโมเดล", "|r| with the final grade, no model", "pl-note")
for k, (c, r) in enumerate(R):
    y = ROW0 + k * RH
    top = k < 3
    s.text(X0 + 20, y + 17, c, "ml-b" if top else "ml-i")
    s.box(X0 + 128, y + 5, r * 170, 15, "ml-bar-top" if top else "ml-bar", 3)
    s.text(X0 + 134 + r * 170, y + 17, f"{r:.2f}", "ml-b" if top else "ml-i")
cut = ROW0 + 3 * RH + 1
s.line(X0 + 14, cut, X0 + PW - 14, cut, "ml-cut-guess")
s.text(X0 + PW - 16, cut + 20, "k = 3 ✂", "ml-neg", "end")
# 2 wrapper
X0 = 20 + PW + 24
s.badge(X0 + 32, PT + 26, 2)
s.both(X0 + 54, PT + 32, "Wrapper: ฝึกจริงแล้ววัดผล", "Wrapper: train and score", "pl-label")
s.both(X0 + 20, PT + 60, "SFS: ทุกรอบเพิ่มตัวที่ช่วยมากที่สุด", "SFS: one best column per round", "pl-note")
ROUNDS = [(["term1_grade"], 0.794, 10, "term1_grade"), (["term1_grade", "absences"], 0.804, 9, "absences"), (["term1_grade", "absences", "age"], 0.809, 8, "age")]
for k, (cols, cv, tried, new) in enumerate(ROUNDS):
    y = 168 + k * 84
    cx = X0 + 18
    for c in cols:
        w = width(c, 16) + 14
        s.box(cx, y, w, 30, "rc-res" if c == new else "ml-cell-b", 8)
        s.text(cx + w / 2, y + 21, c, "ml-b", "middle")
        cx += w + 4
    s.both(X0 + 20, y + 58, f"รอบ {k + 1}: เก็บ {new}", f"round {k + 1}: kept {new}", "ml-i")
    s.text(X0 + PW - 16, y + 58, f"CV {cv:.3f}", "ml-b", "end")
# 3 embedded
X0 = 20 + 2 * (PW + 24)
s.badge(X0 + 32, PT + 26, 3)
s.both(X0 + 54, PT + 32, "Embedded: เลือกระหว่างฝึก", "Embedded: picks while training", "pl-label")
s.both(X0 + 20, PT + 60, "Lasso (alpha = 0.3): ค่า β ของแต่ละคอลัมน์", "Lasso (alpha = 0.3): each column's β", "pl-note")
for k, (c, _) in enumerate(R):
    y = ROW0 + k * RH
    b = LASSO.get(c, 0)
    if b:
        s.text(X0 + 20, y + 17, c, "ml-b")
        bw = max(abs(b) / 2.6 * 140, 4)
        s.box(X0 + 128, y + 5, bw, 15, "ml-bar-top", 3)
        s.text(X0 + 134 + bw, y + 17, f"{b:.2f}".replace("-", "−"), "ml-b")
    else:
        s.text(X0 + 20, y + 17, c, "ml-i")
        s.raw(f'<path d="M{X0 + 17} {y + 12} H{X0 + 22 + width(c, 16)}" class="ml-cut"/>')
        s.text(X0 + 128, y + 17, "0", "ml-i")
s.arrow(X0 + 204, ROW0 + 5 * RH + 13, X0 + 148, ROW0 + 5 * RH + 13)
s.both(X0 + 210, ROW0 + 5 * RH + 6, "7 ตัว β = 0", "7 columns: β = 0", "ml-neg")
s.both(X0 + 210, ROW0 + 5 * RH + 34, "= ตัดทิ้ง", "= dropped", "ml-neg")
# results
RES = (("✓ เก็บ term1_grade, failures, absences", "✓ keeps term1_grade, failures, absences", "ฝึก 0 ครั้ง", "0 trainings", "0.800"),
       ("✓ เก็บ term1_grade, absences, age", "✓ keeps term1_grade, absences, age", "27 ชุด × cv 5 = ฝึก 135 ครั้ง", "27 sets × cv 5 = 135 trainings", "0.809"),
       ("✓ เก็บ term1_grade, absences, age", "✓ keeps term1_grade, absences, age", "ฝึกครั้งเดียว", "1 training", "0.788"))
for i, (kth, ken, th, en, cv) in enumerate(RES):
    X0 = 20 + i * (PW + 24)
    s.both(X0 + 20, 446, kth, ken, "ml-ok")
    s.both(X0 + 20, 476, th, en, "pl-note")
    s.text(X0 + 20, 504, f"CV R² {cv}", "pl-note")
s.both(20, 556, "① ดูทีละคอลัมน์ จึงเก็บ failures ซึ่งซ้ำกับ term1_grade · ② ③ ดูหลายคอลัมน์พร้อมกัน จึงเก็บ age แทน",
       "① one column at a time: keeps failures, which repeats term1_grade · ② ③ see columns together, keep age",
       "pl-note")
s.save("l10-three-families.svg", 572)

# ================================================================ L10-S09: grid vs random search on Lasso's alpha
CURVE = [(0.001, 0.7961), (0.0013, 0.7961), (0.0018, 0.7962), (0.0024, 0.7963), (0.0032, 0.7964), (0.0042, 0.7966),
         (0.0056, 0.7969), (0.0075, 0.7971), (0.01, 0.7975), (0.0133, 0.798), (0.0178, 0.7985), (0.0237, 0.7991),
         (0.0316, 0.7998), (0.0422, 0.8009), (0.0562, 0.8018), (0.075, 0.8028), (0.1, 0.8032), (0.1334, 0.8025),
         (0.1778, 0.8002), (0.2371, 0.7945), (0.3162, 0.7863), (0.4217, 0.7777), (0.5623, 0.7651), (0.7499, 0.7419),
         (1.0, 0.7003), (1.3335, 0.6261), (1.7783, 0.4936), (2.3714, 0.2573), (3.1623, -0.0106), (4.217, -0.0106),
         (5.6234, -0.0106), (7.4989, -0.0106), (10.0, -0.0106), (13.3352, -0.0106), (17.7828, -0.0106), (23.7137, -0.0106),
         (31.6228, -0.0106), (42.1697, -0.0106), (56.2341, -0.0106), (74.9894, -0.0106), (100.0, -0.0106)]
GRID = [(0.001, 0.796), (0.01, 0.798), (0.1, 0.803), (1, 0.700), (10, -0.011), (100, -0.011)]
RAND = [(0.001, 0.796), (0.003, 0.796), (0.005, 0.797), (0.009, 0.797), (0.032, 0.800), (0.053, 0.802), (0.096, 0.803),
        (0.122, 0.803), (0.494, 0.772), (3.996, -0.011)]
s = Svg(W, "Choosing Lasso's alpha on the student data. Both panels show the same CV R² curve. Grid search tries the 6 listed "
           "values 0.001 to 100 and finds 0.1 (CV R² 0.803), but never tries anything between 0.01 and 0.1. Random search "
           "draws 10 values on a log scale and finds 0.096 (CV R² 0.803). Both give test R² 0.805. With 4 hyperparameters "
           "of 5 values each, a grid needs 625 models; random search always needs only N.")
s.bubble("Lasso กับข้อมูลนักเรียน: ควรลอง alpha ค่าไหนบ้าง (ลอง 1 ค่า = ฝึก 1 โมเดล)", "Lasso on the students: which alphas should we try? (1 try = 1 model)")
py = lambda v: 341 - v * 230


def score_plot(x0, tried, best):
    px = lambda a: logx(a, x0 + 80, 90)
    s.line(x0 + 66, 341, x0 + 540, 341, "dg-rule-strong")
    s.text(x0 + 60, 347, "0", "pl-note", "end")
    for g in (0.4, 0.8):
        s.text(x0 + 60, py(g) + 6, f"{g}", "pl-note", "end")
        s.line(x0 + 66, py(g), x0 + 540, py(g), "dg-rule")
    s.text(x0 + 16, 192, "CV R²", "pl-note")
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
s.arrow(mid, 286, mid, 336)
s.both(mid, 270, "ระหว่าง 0.01 กับ 0.1: ไม่เคยลอง", "between 0.01 and 0.1: never tried", "ml-neg", "middle")
s.both(40, 462, "✓ ได้ alpha 0.1 · CV R² 0.803 · test R² 0.805", "✓ best alpha 0.1 · CV R² 0.803 · test R² 0.805", "ml-ok")
s.both(40, 494, "เขียนรายการเอง: ลองแค่ค่าที่เราเดา", "you write the list: it tries only your guesses", "pl-note")
s.panel(600, 70, 560, 450, "nt-band-a", "Random search: สุ่ม 10 ค่าในช่วง", "Random search: 10 random values in a range", 2)
px = score_plot(600, RAND, 0.096)
s.arrow(px(0.096) - 30, 250, px(0.096) - 4, py(0.803) + 12)
s.text(px(0.096) - 34, 270, "alpha 0.096 → 0.803", "pl-label", "middle")
s.text(px(3.996), py(-0.011) - 16, "−0.011", "pl-note", "middle")
s.both(620, 462, "✓ ได้ alpha 0.096 · CV R² 0.803 · test R² 0.805", "✓ best alpha 0.096 · CV R² 0.803 · test R² 0.805", "ml-ok")
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
# the formula as real math: superscripts and subscripts drawn with tspans (a plain "e^(z_j)" string read as code)
parts = [("P(group ", 0, None, False), ("j", 0, None, True), (") = ", 0, None, False)]
for i, k in enumerate(["j", "1", "2", "3", "4"]):
    if i == 1:
        parts.append((" / (", 0, None, False))
    elif i > 1:
        parts.append((" + ", 0, None, False))
    parts += [("e", 0, None, False), ("z", -13, 19, True), (k, 6, 14, k == "j"), ("\u200a", 7, None, False)]
parts.append((")", 0, None, False))
spans = "".join(f'<tspan dy="{dy}"{f' font-size="{fs}"' if fs else ''}{' font-style="italic"' if it else ''}>{txt}</tspan>'
                for txt, dy, fs, it in parts)
s.raw(f'<text x="{W / 2}" y="94" text-anchor="middle" class="mp-math" lang="en">{spans}</text>')
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

# ================================================================ L11-S12: the confusion matrix as four illustrated cards
# Test people by real group: Underweight 13, Normal 6, Overweight 9, Obese 5. With Overweight positive: TP 4, FN 5 (all
# called Normal Weight), FP 0, TN 24 (13 Underweight, 6 Normal, 5 Obese). Cards follow the matrix: rows = real group,
# columns = the model's guess. A person's build and shirt colour show their real group. The characters were generated
# with ElevenLabs (gpt-image-2.5) for this course; see assets/LICENSES.md.
from stats_svg import embed_png  # noqa: E402

GCOL = {"U": "var(--tag-concept-dot)", "N": "var(--tag-exercise-dot)", "Ov": "var(--tag-example-dot)", "Ob": "var(--accent)"}


def fig_person(x, y, color, k=1.0):
    s.raw(f'<g transform="translate({x:g} {y:g}) scale({k:g})" style="fill:{color}"><circle cx="0" cy="-9" r="7"/>'
          f'<path d="M-10 16 Q-10 1 0 1 Q10 1 10 16 Z"/></g>')


s = Svg(W, "The confusion matrix of the weight model on its 33 test people, with Overweight as the positive class, as four "
           "illustrated cards. True positive, 4 people: an Overweight person, the AI says 'You're Overweight!': caught. "
           "False negative, 5 people: an Overweight person, the AI says 'Normal Weight': missed, a Type II error. False "
           "positive, 0 people: a person who is not Overweight, the AI says 'You're Overweight!': a false alarm, a Type I "
           "error. True negative, 24 people: not Overweight, the AI says 'not Overweight': rightly left out. Right: the same "
           "counts as a 2 × 2 matrix.")
CW, CH, GX, GY = 404, 256, 14, 12
CARDS = [  # col, row, true?, title th/en, n, actual th/en, said th/en, bubble th/en, person build/shirt/mood/mark, caption th/en, people
    (0, 0, True, ("True Positive (TP) = 4", "True Positive (TP) = 4"), ("จริง: น้ำหนักเกิน", "Actual: Overweight"),
     ("ทาย: น้ำหนักเกิน", "Predicted: Overweight"), ("คุณน้ำหนักเกิน", "You're Overweight!"), ("ai-over-calm.png", "Ov", None),
     ("จับได้ถูกคน", "caught: rightly flagged"), ["Ov"] * 4),
    (1, 0, False, ("False Negative (FN) = 5", "False Negative (FN) = 5"), ("จริง: น้ำหนักเกิน", "Actual: Overweight"),
     ("ทาย: ปกติ", "Predicted: Normal"), ("คุณน้ำหนักปกติ", "You're Normal Weight."), ("ai-over-worried.png", "Ov", None),
     ("พลาด (Type II)", "missed (Type II error)"), ["Ov"] * 5),
    (0, 1, False, ("False Positive (FP) = 0", "False Positive (FP) = 0"), ("จริง: ไม่ใช่น้ำหนักเกิน", "Actual: not Overweight"),
     ("ทาย: น้ำหนักเกิน", "Predicted: Overweight"), ("คุณน้ำหนักเกิน", "You're Overweight!"), ("ai-normal-puzzled.png", "N", "?"),
     ("เตือนผิด (Type I)", "false alarm (Type I error)"), []),
    (1, 1, True, ("True Negative (TN) = 24", "True Negative (TN) = 24"), ("จริง: ไม่ใช่น้ำหนักเกิน", "Actual: not Overweight"),
     ("ทาย: กลุ่มอื่น ไม่ใช่เกิน", "Predicted: another group"), ("คุณน้ำหนักปกติ", "You're Normal Weight."), ("ai-normal-happy.png", "N", None),
     ("ไม่นับ ถูกแล้ว", "rightly left out"), ["U"] * 13 + ["N"] * 6 + ["Ob"] * 5),
]
for col, row, ok, (tth, ten), (ath, aen), (pth, pen), (bth, ben), (peep, g, mark), (cth, cen), people in CARDS:
    x, y = 10 + col * (CW + GX), 10 + row * (CH + GY)
    s.box(x, y, CW, CH, "rc-res" if ok else "rc-con", 16)
    s.box(x + 12, y + 10, CW - 24, 38, "ml-cell", 19)
    s.both(x + CW / 2, y + 36, tth, ten, "ct-head-tp" if ok else "ct-head-f", "middle")
    s.both(x + CW / 2, y + 70, f"{ath}  |  {pth}", f"{aen}  |  {pen}", "mp-c", "middle")
    embed_png(s, peep, x + 16, y + 78, 134, 126)
    if mark:
        s.text(x + 146, y + 112, mark, "ct-mark")
    embed_png(s, "ai-robot.png", x + 324, y + 92, 74, 112)
    bw = 168
    s.box(x + 156, y + 92, bw, 46, "ml-cell", 14)
    s.raw(f'<path d="M{x + 156 + bw - 18:g} {y + 136:g} L{x + 332:g} {y + 140:g} L{x + 156 + bw - 40:g} {y + 137:g} Z" class="ml-cell"/>')
    s.both(x + 156 + bw / 2, y + 121, bth, ben, "mp-chip", "middle")
    s.box(x + 12, y + 204, CW - 24, 42, "ml-cell", 12)
    s.both(x + 26, y + 231, cth, cen, "ct-head-tp" if ok else "ct-head-f")
    n = len(people)
    if 0 < n <= 9:
        for i, gg in enumerate(people):
            fig_person(x + CW - 30 - (n - 1 - i) * 16, y + 228, GCOL[gg], 0.55)
    elif n > 9:     # TN: one small person per real group, with its count
        for i, gg in enumerate(("U", "N", "Ob")):
            px = x + CW - 150 + i * 46
            fig_person(px, y + 228, GCOL[gg], 0.6)
            s.text(px + 10, y + 232, f"×{people.count(gg)}", "mp-c")
    else:
        s.both(x + CW - 26, y + 231, "0 คน", "0 people", "pl-note", "end")
# the same counts as a matrix, what "negative" means with 4 groups, and who is inside TN and FN
X0, Y0 = 10 + 2 * CW + GX + 20, 10
PWD = 1170 - X0
s.box(X0, Y0, PWD, 2 * CH + GY, "ml-cell", 16)
s.both(X0 + 18, Y0 + 34, "ชุด test 33 คน", "33 test people", "pl-label")
s.both(X0 + 18, Y0 + 64, "บวก = น้ำหนักเกิน", "positive = Overweight", "pl-note")
s.both(X0 + 18, Y0 + 94, "ลบ = ทายกลุ่มอื่นกลุ่มไหนก็ได้", "negative = any other group", "ct-head-f")
mx, my, cw2, ch2 = X0 + 104, Y0 + 156, 100, 82
s.both(mx + cw2, my - 32, "โมเดลทาย →", "predicted →", "ml-i", "middle")
s.both(mx + cw2 / 2, my - 8, "เกิน", "Over", "ml-b", "middle")
s.both(mx + 1.5 * cw2, my - 8, "อื่น", "other", "ml-b", "middle")
s.both(mx - 10, my + ch2 / 2 + 6, "เกิน", "Over", "ml-b", "end")
s.both(mx - 10, my + 1.5 * ch2 + 6, "อื่น", "other", "ml-b", "end")
s.both(X0 + 18, my + ch2 + 6, "จริง ↓", "real ↓", "ml-i")
for (c, r, lab, n, ok, sub) in ((0, 0, "TP", 4, True, ""), (1, 0, "FN", 5, False, "Type II"), (0, 1, "FP", 0, False, "Type I"), (1, 1, "TN", 24, True, "")):
    cx, cy = mx + c * cw2, my + r * ch2
    s.box(cx + 3, cy + 3, cw2 - 6, ch2 - 6, "rc-res" if ok else "rc-con", 10)
    s.text(cx + cw2 / 2, cy + 25, lab, "pl-label", "middle")
    s.text(cx + cw2 / 2, cy + 56, str(n), "mp-big-ok" if ok else "mp-big", "middle")
    if sub:
        s.text(cx + cw2 / 2, cy + 75, sub, "mp-s", "middle")
# who is inside: real group → what the model said (the real 4×4 test matrix)
by = my + 2 * ch2 + 8
s.box(X0 + 10, by, PWD - 20, 2 * CH + GY - (by - Y0) - 10, "rc-ctx", 12)
s.both(X0 + 22, by + 24, "ข้างในมีใคร: กลุ่มจริง → โมเดลทาย", "who is inside: real → model said", "mp-c")
ROWS = [("TN", "U", "ผอม 13 → ผอม 12 · ปกติ 1", "Under 13 → Under 12 · Normal 1"),
        ("TN", "N", "ปกติ 6 → ปกติ 6", "Normal 6 → Normal 6"),
        ("TN", "Ob", "อ้วน 5 → อ้วน 5", "Obese 5 → Obese 5"),
        ("FN", "Ov", "เกิน 5 → ปกติ 5", "Over 5 → Normal 5")]
for i, (cell, g, th, en) in enumerate(ROWS):
    yy = by + 48 + i * 23
    s.text(X0 + 22, yy, cell, "ct-head-tp" if cell == "TN" else "ct-head-f")
    s.raw(f'<rect x="{X0 + 62}" y="{yy - 12}" width="14" height="14" rx="3" style="fill:{GCOL[g]}"/>')
    s.both(X0 + 84, yy, th, en, "mp-s")
s.both(X0 + 22, by + 148, "ทาย “ปกติ” ผิด 1 คน แต่ยังนับเป็น TN", "1 Under called Normal is wrong,", "mp-s")
s.both(X0 + 22, by + 168, "เพราะโมเดลไม่ได้บอกว่า “เกิน”", "yet still a TN: it didn't say Over", "mp-s")
s.save("l11-confusion-people.svg", 2 * CH + GY + 20)

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

# ================================================================ L11-S16: per-class counts in the obesity model's 4×4 matrix
# The lesson's 4-group model (70/30 split, random_state=42, StandardScaler, LogisticRegression) on its 33 test people;
# rows = real group, columns = predicted, in the order Underweight, Normal, Overweight, Obese.
M = [[12, 1, 0, 0], [0, 6, 0, 0], [0, 5, 4, 0], [0, 0, 0, 5]]
GRP = [("ผอม", "Underweight", "U"), ("ปกติ", "Normal", "N"), ("น้ำหนักเกิน", "Overweight", "Ov"), ("อ้วน", "Obese", "Ob")]
STATS = [(12, 0, 1, "12/12 = 1.00", "12/13 = 0.92"), (6, 6, 0, "6/12 = 0.50", "6/6 = 1.00"),
         (4, 0, 5, "4/4 = 1.00", "4/9 = 0.44"), (5, 0, 0, "5/5 = 1.00", "5/5 = 1.00")]
s = Svg(W, "The obesity model's 4 × 4 confusion matrix for its 33 test people, read once per weight group. For each group, TP is "
           "its diagonal cell, FP the rest of its column, FN the rest of its row. Underweight: TP 12, FP 0, FN 1, precision "
           "1.00, recall 0.92. Normal: TP 6, FP 6, FN 0, precision 0.50, recall 1.00. Overweight: TP 4, FP 0, FN 5, precision "
           "1.00, recall 0.44. Obese: TP 5, FP 0, FN 0, precision 1.00, recall 1.00. Macro average precision (1.00 + 0.50 + "
           "1.00 + 1.00) / 4 = 0.88; micro average pools TP 27, FP 6, FN 6: 27 / 33 = 0.82, the accuracy.")
s.bubble("คน test 33 คน 4 กลุ่ม: โมเดลเก่งกับแต่ละกลุ่มแค่ไหน", "33 test people, 4 groups: how good is the model for each group?")
PW = 273
for k in range(4):
    X0 = 20 + k * (PW + 16)
    s.box(X0, 70, PW, 360, "nt-band-a", 14)
    s.both(X0 + 18, 100, GRP[k][0], GRP[k][1], "pl-label")
    s.both(X0 + 18, 124, "เป็นกลุ่มบวก", "as the positive class", "pl-note")
    mx, my, cw, ch = X0 + 62, 182, 48, 36
    s.both(mx + 2 * cw, 148, "ทาย →", "predicted →", "ml-i", "middle")
    s.both(X0 + 14, my - 8, "จริง ↓", "real ↓", "ml-i")
    for j in range(4):
        s.text(mx + j * cw + cw / 2, my - 8, GRP[j][2], "ml-b", "middle")
        s.text(mx - 10, my + j * ch + ch / 2 + 6, GRP[j][2], "ml-b", "end")
    for r in range(4):
        for c in range(4):
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
    s.text(X0 + 18, 344, f"TP {tp} · FP {fp} · FN {fn}", "pl-label")
    s.text(X0 + 18, 374, f"precision = {prec}", "pl-text")
    s.text(X0 + 18, 404, f"recall = {rec}", "pl-text")
LEG = [("rc-res", "TP: ช่องทแยงของกลุ่มนั้น", "TP: the group's diagonal cell"),
       ("sw-chip-warn", "FP: ที่เหลือในคอลัมน์ (ทายว่าใช่ แต่ผิด)", "FP: rest of its column (said it, wrong)"),
       ("rc-ctx", "FN: ที่เหลือในแถว (ใช่จริง แต่พลาด)", "FN: rest of its row (really it, missed)")]
lx = 20
for cls, th, en in LEG:
    s.box(lx, 452, 22, 22, cls, 4)
    s.both(lx + 30, 470, th, en, "pl-note")
    lx += 30 + max(width(th, 18), width(en, 18)) + 34
s.both(20, 512, "macro: เฉลี่ยของ 4 กลุ่ม precision = (1.00 + 0.50 + 1.00 + 1.00) / 4 = 0.88 · ทุกกลุ่มนับเท่ากัน",
       "Macro: the mean of the 4 groups, precision = (1.00 + 0.50 + 1.00 + 1.00) / 4 = 0.88 · every group counts the same", "pl-text")
s.both(20, 544, "micro: รวมตัวนับก่อน TP 27 · FP 6 · FN 6 → 27 / 33 = 0.82 = accuracy",
       "Micro: pool the counts first, TP 27 · FP 6 · FN 6 → 27 / 33 = 0.82 = accuracy", "pl-text")
s.save("l11-multiclass-metrics.svg", 560)

# ================================================================ L10-S01: meet the data, one student = one row
# UCI Student Performance (math course), first row: age 18, Medu 4, Fedu 4, studytime 2, failures 0, goout 4, Dalc 1, Walc 1,
# absences 6, term1_grade 5, final_grade 6. Final grades of the 357 students who sat the exam run 4–20; 25.8% are below the pass mark 10.
LEFT = [("age", "18", "อายุ (ปี)", "age (years)"), ("studytime", "2", "อ่านหนังสือ 2–5 ชม./สัปดาห์", "study: 2–5 hours a week"),
        ("failures", "0", "เคยสอบตกกี่วิชา", "past classes failed"), ("goout", "4", "เที่ยวกับเพื่อน (1–5)", "going out (1–5)"),
        ("absences", "6", "ขาดเรียน (วัน)", "absences (days)")]
RIGHT = [("Medu", "4", "แม่จบปริญญา", "mother: a degree"), ("Fedu", "4", "พ่อจบปริญญา", "father: a degree"),
         ("Dalc", "1", "ดื่มวันธรรมดา (1–5)", "weekday drinks (1–5)"), ("Walc", "1", "ดื่มเสาร์อาทิตย์ (1–5)", "weekend drinks (1–5)"),
         ("term1_grade", "5", "เกรดเทอม 1 (0–20)", "term 1 grade (0–20)")]
G3HIST = {4: 1, 5: 7, 6: 15, 7: 9, 8: 32, 9: 28, 10: 56, 11: 47, 12: 31, 13: 31, 14: 27, 15: 33, 16: 16, 17: 6, 18: 12, 19: 5, 20: 1}
s = Svg(W, "The student data: one row is one student. At the end of term 1 we know 10 things about student 1: age 18, studies "
           "2–5 hours a week, failed 0 classes before, goes out 4 (on 1–5), 6 days absent, mother's and father's education "
           "level 4 (a degree), weekday alcohol 1 and weekend alcohol 1 (on 1–5), and the term 1 grade term1_grade = 5 out of 20. "
           "These are the features. At the end of the year the school gives the final grade final_grade, out of 20 with 10 to pass: "
           "student 1 got 6. Over the 357 students final_grade runs from 4 to 20, and 25.8% are below 10. final_grade is the target.")
s.bubble("ข้อมูลนักเรียน: หนึ่งแถว = นักเรียนหนึ่งคน", "The student data: one row = one student")
s.panel(20, 70, 830, 430, "nt-band-a", "จบภาคเรียนที่ 1: นักเรียนคนที่ 1", "End of term 1: student 1", 1)
s.both(40, 126, "10 คอลัมน์ที่รู้แล้ว = feature (สิ่งที่โมเดลใช้ทาย)", "10 columns we already know = features (what the model predicts from)", "pl-note")


def row(x, y, name, val, th, en, lit=False):
    s.box(x, y, 390, 46, "rc-ctx" if lit else "ml-cell", 10)
    s.text(x + 12, y + 30, name, "ml-b")
    s.text(x + 146, y + 30, val, "pl-label", "end")
    s.both(x + 160, y + 30, th, en, "pl-note")


s.both(40, 166, "ตัวนักเรียน", "The student", "pl-label")
for k, r in enumerate(LEFT):
    row(40, 180 + k * 54, *r)
s.both(440, 166, "ครอบครัว · การดื่ม · เกรดเทอม 1", "Family · alcohol · term 1 grade", "pl-label")
for k, r in enumerate(RIGHT):
    row(440, 180 + k * 54, *r, lit=(r[0] == "term1_grade"))
s.both(40, 476, "เลข 1–5 คือระดับที่นักเรียนตอบในแบบสอบถาม (1 = น้อยมาก 5 = มากมาก)", "1–5 values are survey answers (1 = very low, 5 = very high)", "pl-note")
s.arrow(856, 290, 872, 290)
s.panel(878, 70, 282, 430, "rc-res", "ปลายปี: target", "Year end: target", 2)
s.text(898, 126, "final_grade", "ml-b")
s.both(898, 152, "เกรดทั้งปี · เต็ม 20 · ผ่านที่ 10", "year grade · of 20 · pass 10", "pl-note")
s.raw('<text x="1019" y="216" text-anchor="middle" style="font: 700 56px var(--font-head); fill: var(--ink)">6</text>')
HX0, HX1, HB = 900, 1140, 370
hx = lambda v: HX0 + (v - 3.5) / 17 * (HX1 - HX0)
for v, c in G3HIST.items():
    h = c / 56 * 96
    s.box(hx(v - 0.5) + 1, HB - h, (HX1 - HX0) / 17 - 2, h, "ml-bar-top" if v == 6 else "ml-bar", 2)
s.line(hx(9.5), HB - 104, hx(9.5), HB, "ml-cut-guess")
s.text(hx(9.5) + 6, HB - 92, "10", "pl-note")
s.line(HX0, HB, HX1, HB, "dg-rule-strong")
for v in (4, 10, 20):
    s.text(hx(v), HB + 22, str(v), "pl-note", "middle")
s.both(898, 254, "นักเรียน 357 คน:", "the 357 students:", "pl-note")
s.both(898, 420, "6 < 10 → สอบตก", "6 < 10 → failed", "pl-text")
s.both(898, 452, "ตก 25.8% · ค่าเฉลี่ย 11.5", "25.8% fail · mean 11.5", "pl-note")
s.both(898, 482, "นี่คือสิ่งที่โมเดลต้องทาย", "this is what we predict", "pl-note")
s.both(20, 540, "× นักเรียน 357 คน  ·  งาน: จบเทอม 1 ใช้ 10 คอลัมน์ทายเกรดทั้งปี final_grade (regression เพราะคำตอบเป็นตัวเลข)",
       "× 357 students  ·  The task: at the end of term 1, predict the year grade final_grade from 10 columns (regression)", "pl-label")
s.save("l10-students-data.svg", 558)

# ================================================================ L10-S07: SFS round by round, like the lecture slide
# Real forward SFS on the student data (LinearRegression, cv=5, 285 training students): the 3 best tries of each round.
SFS_ROUNDS = [
    ([["term1_grade"], ["failures"], ["Walc"]], [0.794, 0.062, 0.025], 7),
    ([["term1_grade", "absences"], ["term1_grade", "age"], ["term1_grade", "goout"]], [0.804, 0.802, 0.795], 6),
    ([["term1_grade", "absences", "age"], ["term1_grade", "absences", "goout"], ["term1_grade", "absences", "Medu"]],
     [0.809, 0.804, 0.804], 5),
]
s = Svg(W, "Forward SFS on the student data, round by round. Round 1 tries each of the 10 columns alone; term1_grade is best "
           "(CV R² 0.794), failures 0.062, Walc 0.025, 7 more lower. Round 2 adds one more column to term1_grade: absences is "
           "best (0.804), age 0.802, goout 0.795, 6 more. Round 3 adds one more to term1_grade + absences: age is best (0.809), "
           "goout 0.804, Medu 0.804, 5 more. Result: term1_grade, absences, age. 10 + 9 + 8 = 27 sets tried; trying every set "
           "of 3 would take 120.")
COLX = [150, 430, 710]
PILL_W, PILL_H = 134, 28
BOX_W = PILL_W + 16
SPACING = [96, 122, 150]
TOP = 132


def set_box(cx, y, cols, win, cv, new_last=True):
    h = len(cols) * (PILL_H + 6) + 10
    s.box(cx - BOX_W / 2, y, BOX_W, h, "ml-cell", 10)
    if win:
        s.raw(f'<rect x="{cx - BOX_W / 2 - 3:g}" y="{y - 3:g}" width="{BOX_W + 6:g}" height="{h + 6:g}" rx="12" fill="none" class="pl-line"/>')
    for j, c in enumerate(cols):
        py = y + 8 + j * (PILL_H + 6)
        s.box(cx - PILL_W / 2, py, PILL_W, PILL_H, "rc-res" if win else "sw-warn-box", 14)
        s.text(cx, py + 20, c, "ml-b" if win else "ml-i", "middle")
    s.text(cx, y + h + 22, f"CV R² {cv:.3f}" + (" ✓" if win else ""), "pl-label" if win else "pl-note", "middle")
    return y, h


boxes = []
for r, (sets, cvs, more) in enumerate(SFS_ROUNDS):
    cx = COLX[r]
    s.both(cx, 100, f"รอบ {r + 1}: ลอง {10 - r} ชุด", f"Round {r + 1}: {10 - r} sets tried", "pl-label", "middle")
    col = []
    for k, (cols, cv) in enumerate(zip(sets, cvs)):
        y, h = set_box(cx, TOP + k * SPACING[r], cols, k == 0, cv)
        col.append((y, h))
    last_y = col[-1][0] + col[-1][1] + 50
    s.both(cx, last_y, f"+ อีก {more} ชุด (CV ต่ำกว่า)", f"+ {more} more (lower CV)", "pl-note", "middle")
    boxes.append(col)
# arrows: from the kept set of each round to every tried set of the next round
for r in range(2):
    y0, h0 = boxes[r][0]
    for (y1, h1) in boxes[r + 1]:
        s.arrow(COLX[r] + BOX_W / 2 + 6, y0 + h0 / 2, COLX[r + 1] - BOX_W / 2 - 8, y1 + h1 / 2)
# result
RX = 1020
s.both(RX, 100, "ผลลัพธ์", "Result", "pl-label", "middle")
y0, h0 = boxes[2][0]
ry = 300
s.arrow(COLX[2] + BOX_W / 2 + 6, y0 + h0 / 2, RX - BOX_W / 2 - 8, ry + 55)
s.box(RX - BOX_W / 2, ry, BOX_W, 3 * (PILL_H + 6) + 10, "rc-res", 10)
for j, c in enumerate(["term1_grade", "absences", "age"]):
    py = ry + 8 + j * (PILL_H + 6)
    s.box(RX - PILL_W / 2, py, PILL_W, PILL_H, "ml-cell", 14)
    s.text(RX, py + 20, c, "ml-b", "middle")
s.text(RX, ry + 3 * (PILL_H + 6) + 34, "CV R² 0.809", "pl-label", "middle")
s.both(RX, ry + 3 * (PILL_H + 6) + 62, "k = 3 ครบแล้ว หยุด", "k = 3 reached: stop", "pl-note", "middle")
# legend + counts
LY = 668
s.box(20, LY - 16, 22, 20, "rc-res", 6)
s.both(50, LY, "ชุดที่ดีที่สุดของรอบ → เก็บ แล้วต่อยอดรอบถัดไป", "the round's best set → kept, and the next round builds on it", "pl-note")
s.box(600, LY - 16, 22, 20, "sw-warn-box", 6)
s.both(630, LY, "ลองแล้วแพ้ → ไม่ใช้ต่อ", "tried and lost → not used again", "pl-note")
s.both(20, 708, "SFS ลอง 10 + 9 + 8 = 27 ชุด · ถ้าลองทุกชุด 3 คอลัมน์จาก 10 ต้องลอง 120 ชุด",
       "SFS tries 10 + 9 + 8 = 27 sets · trying every set of 3 columns out of 10 would take 120", "pl-label")
s.save("l10-sfs-rounds.svg", 726)

# ================================================================ L10-S07: SFS vs brute force on 4 columns f1–f4
s = Svg(W, "SFS versus brute force on 4 columns f1 to f4. SFS: step 1 tries [f1], [f2], [f3], [f4] and keeps f2; step 2 tries "
           "[f2, f1], [f2, f3], [f2, f4] and keeps f2, f4; step 3 tries [f2, f4, f1], [f2, f4, f3] and keeps f2, f4, f3; step 4 has "
           "only [f2, f4, f3, f1]: 4 + 3 + 2 + 1 = 10 experiments. Brute force tries every set: 4 of size 1, 6 of size 2, 4 of "
           "size 3 and 1 of size 4: 15 experiments.")
s.bubble("มี 4 คอลัมน์ f1–f4: ต้องฝึกโมเดลกี่ครั้ง", "4 columns, f1–f4: how many models do we train?")


def chip_row(x0, y, sets, win=None):
    x = x0
    for k, st in enumerate(sets):
        label = ", ".join(st)
        w = width(label, 17) + 22
        s.box(x, y - 22, w, 32, "rc-res" if k == win else "ml-cell", 8)
        s.text(x + w / 2, y, label, "ml-b" if k == win else "ml-i", "middle")
        x += w + 8


s.panel(20, 70, 560, 520, "nt-band-a", "SFS: ฝึก 10 ครั้ง", "SFS: 10 experiments", 1)
STEPS = [("ขั้น 1: ลองทีละตัว", "Step 1: each column alone", [["f1"], ["f2"], ["f3"], ["f4"]], 1, "เก็บ f2", "keep f2"),
         ("ขั้น 2: เพิ่มอีกตัวให้ f2", "Step 2: add one more to f2", [["f2", "f1"], ["f2", "f3"], ["f2", "f4"]], 2, "เก็บ f2, f4", "keep f2, f4"),
         ("ขั้น 3: เพิ่มอีกตัวให้ f2, f4", "Step 3: add one more to f2, f4", [["f2", "f4", "f1"], ["f2", "f4", "f3"]], 1, "เก็บ f2, f4, f3", "keep f2, f4, f3"),
         ("ขั้น 4: เหลือตัวเดียว", "Step 4: only one left", [["f2", "f4", "f3", "f1"]], 0, "ครบ 4 ตัว", "all 4")]
for k, (th, en, sets, win, kth, ken) in enumerate(STEPS):
    y = 132 + k * 110
    s.both(40, y, th, en, "pl-text")
    chip_row(40, y + 42, sets, win)
    s.both(560, y, f"{len(sets)} ชุด · {kth}", f"{len(sets)} set{'s' if len(sets) > 1 else ''} · {ken}", "pl-note", "end")
s.both(40, 566, "4 + 3 + 2 + 1 = 10 ✓ เร็ว แต่ไม่รับประกันว่าได้ชุดที่ดีที่สุด", "4 + 3 + 2 + 1 = 10 ✓ fast, but the best set isn't guaranteed", "ml-ok")
s.panel(600, 70, 560, 520, "sw-warn-box", "ลองทุกชุด (brute force): ฝึก 15 ครั้ง", "Brute force: 15 experiments", 2)
SIZES = [("ขนาด 1", "Size 1", [["f1"], ["f2"], ["f3"], ["f4"]]),
         ("ขนาด 2", "Size 2", [["f1", "f2"], ["f1", "f3"], ["f1", "f4"], ["f2", "f3"], ["f2", "f4"], ["f3", "f4"]]),
         ("ขนาด 3", "Size 3", [["f1", "f2", "f3"], ["f1", "f2", "f4"], ["f1", "f3", "f4"], ["f2", "f3", "f4"]]),
         ("ขนาด 4", "Size 4", [["f1", "f2", "f3", "f4"]])]
y = 128
for th, en, sets in SIZES:
    s.both(620, y, th, en, "pl-text")
    s.both(1140, y, f"{len(sets)} ชุด", f"{len(sets)} set{'s' if len(sets) > 1 else ''}", "pl-note", "end")
    rows = [sets[:3], sets[3:]] if len(sets) > 4 else [sets]
    for rset in rows:
        chip_row(620, y + 38, rset)
        y += 40
    y += 56
s.both(620, 566, "4 + 6 + 4 + 1 = 15 ✗ ได้ชุดที่ดีที่สุดแน่นอน แต่โตเร็วมาก", "4 + 6 + 4 + 1 = 15 ✗ finds the best for sure, but explodes", "ml-neg")
s.save("l10-sfs-vs-brute.svg", 610)
