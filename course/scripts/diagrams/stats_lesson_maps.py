"""Draws the lesson maps (the big-picture card) of stats-dh lessons 10–15 as picture tiles: the problem on the lesson's
running data with a small drawing, then one tile per part (a drawing of what the part does, a short title, its real
result), then the last part. Few words: the drawing carries the idea, the number sits on the drawing.

    course/.venv/bin/python scripts/diagrams/stats_lesson_maps.py courses/stats-dh/images

Every number is a real run in course/.venv (the same numbers as the lessons' code cells):
  L10 students (357, 80/20 split, random_state=42): LinearRegression on all 10 columns test R² 0.801; SFS keeps age,
      absences, term1_grade: 0.807; Lasso grid search best alpha 0.1, test R² 0.805. Checklist table: student_id is an
      ID, term2_grade leaks (r 0.97), course is one value.
  L11 obesity (108; 70/30 split, random_state=42): a straight line on Weight gives 120 kg 0.51 and the lightest −0.21;
      100 kg p̂ 0.93; test accuracy 0.82 (27 of 33); Overweight recall 0.44 (4 of 9); Overweight AUC 0.94.
  L12 wine reviews (1,000; Ridge, KFold(5, shuffle, 42)): R² text alone (TF-IDF) 0.389, other columns 0.400, joined
  0.529; row = 384 + 1 + 156 = 541; wine 1 scaled log price −0.93.
  L13 obesity: 5-fold accuracy of logistic regression on height and weight 0.88; labels 47/29/20/12, entropy 1.83 bits;
      depth-3 tree root BMI ≤ 20.6 → Underweight 37, then BMI ≤ 24.6 → Normal 20, 22 of 22 test right; a forest of 100
      votes Obese 94, Overweight 6; CV random forest 0.989, tree 0.977; KNN k = 3: 2 Obese 1 Overweight → Obese,
      k = 7: 4 Overweight 3 Obese → Overweight.
  L14 Persuasion: words per chapter (24), median 3,189.5; news A→E with p 0.3, 0.2, 0.5, 0.1 reaches E in 0.3% of
      runs; bootstrap rows from default_rng(3) on 1–8; median 95% CI 2,775 to 3,518; volume II +557, p = 0.36.
  L15 letters: letter 3 formality A 1, B 9, C 8; emotion alpha 0.375, formality ICC 0.418; "Anxiety or not" A vs B
      agree 72%, chance 56.9%, kappa 0.35; after revising: alpha 0.684, ICC 0.807.
Schematic drawings (the scatter of curved groups, the sigmoid and ROC shapes, the histogram of simulated worlds) carry
no numbers of their own.

Uses the mp-* classes (and ml-*, rc-*, pl-*, dg-*) in templates/page.css.
"""

import math
import random

from stats_svg import CLS, Svg, chip, circ, embed_png, person, poly, ring, width

W, H = 1100, 510
TW, GAP, TY, TH_ = 252, 24, 170, 272     # tiles: width, gap, top, height
PW, PH = TW - 28, 120                    # picture area inside a tile


def pill(s, x, y, th, en):
    w = max(width(th, 15), width(en, 15)) + 26
    s.box(x, y, w, 28, "ml-cell-b", 14)
    s.both(x + w / 2, y + 19, th, en, "mp-p", "middle")
    return w


def rcls(en):
    return "ml-ok" if "✓" in en else "ml-neg" if "✗" in en else "mp-r"


def lines(s, x, y, th, en, cls, lh=24):
    ths, ens = th.split("\n"), en.split("\n")
    for i in range(max(len(ths), len(ens))):
        s.both(x, y + i * lh, ths[i] if i < len(ths) else "", ens[i] if i < len(ens) else "", cls)


def info_map(name, title, data, q, note, problem_pic, tiles, last):
    """data, q, note: (th, en); problem_pic(s, x, y, w, h); tiles: 4 × (part, title th, en, pic, result th, en),
    a result may have two lines split by \\n; last: (part or None, th, en)."""
    s = Svg(W, title)
    s.box(10, 10, 1080, 140, "sw-warn-box", 16)
    s.box(24, 22, 300, 116, "mp-pic", 12)
    problem_pic(s, 24, 22, 300, 116)
    pw = pill(s, 346, 26, "ส่วนที่ 1 · ปัญหา", "Part 1 · The problem")
    s.both(346 + pw + 14, 46, data[0], data[1], "pl-note")
    s.both(346, 96, q[0], q[1], "mp-q")
    s.both(346, 130, note[0], note[1], rcls(note[1]))
    for k, (part, tth, ten, pic, rth, ren) in enumerate(tiles):
        x = 10 + k * (TW + GAP)
        s.box(x, TY, TW, TH_, "ml-cell", 14)
        pill(s, x + 14, TY + 12, f"ส่วนที่ {part}", f"Part {part}")
        s.box(x + 14, TY + 50, PW, PH, "dg-xl-head", 10)
        pic(s, x + 14, TY + 50, PW, PH)
        s.both(x + 16, TY + 200, tth, ten, "mp-t")
        lines(s, x + 16, TY + 228, rth, ren, rcls(ren))
        if k < len(tiles) - 1:
            s.arrow(x + TW + 4, TY + 110, x + TW + GAP - 4, TY + 110)
    part, lth, len_ = last
    s.box(10, 456, 1080, 44, "rc-ctx", 14)
    x = 26
    if part:
        x += pill(s, 26, 464, f"ส่วนที่ {part}", f"Part {part}") + 14
    s.both(x, 485, lth, len_, "pl-text")
    s.save(name, H)


# ================================================================ L10 model tuning (students)
def l10_problem(s, x, y, w, h):
    for i in range(10):
        s.fill(x + 14 + i * 10, y + 24, 7, 60, "var(--tag-concept-dot)", 2)
    s.both(x + 62, y + 104, "10 คอลัมน์", "10 columns", "mp-s", "middle")
    s.arrow(x + 112, y + 54, x + 130, y + 54)
    s.box(x + 134, y + 34, 62, 40, "ml-model", 8)
    s.text(x + 165, y + 60, "linear", "ml-model-text", "middle")
    s.arrow(x + 200, y + 54, x + 218, y + 54)
    s.text(x + 258, y + 64, "0.801", "mp-big", "middle")
    s.text(x + 258, y + 96, "test R²", "mp-s", "middle")


def l10_hand(s, x, y, w, h):
    rows = [("student_id", "✗ รหัส", "✗ an ID"), ("term2_grade", "✗ รั่ว", "✗ leak"), ("course", "✗ ค่าเดียว", "✗ one value")]
    for k, (col, th, en) in enumerate(rows):
        yy = y + 32 + k * 34
        s.text(x + 12, yy, col, "mp-mono")
        s.both(x + w - 12, yy, th, en, "mp-acc", "end")
        if k:
            s.line(x + 10, yy - 22, x + w - 10, yy - 22, "mp-guide")


def l10_algo(s, x, y, w, h):
    keep = {0, 8, 9}   # age, absences, term1_grade
    for i in range(10):
        bx = x + 11 + i * 21
        s.fill(bx, y + 14, 14, 56, "var(--accent)" if i in keep else "var(--card-border)", 3)
    s.both(x + w / 2, y + 94, "เก็บ 3 จาก 10", "keep 3 of 10", "mp-n", "middle")
    s.text(x + w / 2, y + 113, "age · absences · term1_grade", "mp-mono", "middle")


def l10_tune(s, x, y, w, h):
    x0, x1, top, bot = x + 26, x + w - 14, y + 24, y + 82
    s.line(x0, bot, x1, bot, "mp-axis")
    s.line(x0, top - 8, x0, bot, "mp-axis")
    s.text(x0 + 6, y + 18, "CV R²", "mp-s")
    pts = [(x0 + t / 40 * (x1 - x0), bot - (1 - 3.2 * (t / 40 - 0.42) ** 2) * (bot - top)) for t in range(41)]
    poly(s, pts, "mp-curve-b")
    xp = x0 + 0.42 * (x1 - x0)
    s.line(xp, top, xp, bot, "mp-guide")
    circ(s, xp, top, 6, "var(--accent)")
    s.text(xp, y + 104, "α 0.1", "mp-acc", "middle")
    s.text(x0, y + 104, "0.01", "mp-s", "middle")
    s.text(x1, y + 104, "3", "mp-s", "middle")


def l10_review(s, x, y, w, h):
    s.fill(x + 14, y + 42, 157, 30, "var(--tag-concept-dot)", 4)
    s.box(x + 173, y + 42, 37, 30, "mp-area", 4)
    s.raw(f'<path d="M{x + 185:g} {y + 24:g} v-5 a6.5 6.5 0 0 1 13 0 v5" style="fill:none;stroke:var(--ink);stroke-width:2.4"/>')
    s.fill(x + 181, y + 23, 21, 15, "var(--ink)", 3)
    s.text(x + 92, y + 96, "train 80%", "mp-c", "middle")
    s.text(x + 191, y + 96, "test 20%", "mp-c", "middle")


info_map(
    "l10-map-lesson.svg",
    "Lesson map. The problem: a linear model on 10 columns about 357 students predicts their final grade with test R² "
    "0.801. Part 2, way 1, pick features by hand with a checklist (student_id is an ID, term2_grade leaks, course is one "
    "value). Part 3, way 2, let code pick: keep age, absences, term1_grade, test R² 0.807. Part 4, way 3, tune the "
    "settings: Lasso alpha 0.1, test R² 0.805. Part 5, review: the test set is used once, at the end.",
    ("นักเรียน 357 คน · 10 คอลัมน์", "357 students · 10 columns"),
    ("ข้อมูลเดิม โมเดลเดิม ทำได้ดีกว่า 0.801 ไหม", "Same data, same model: can we beat 0.801?"),
    ("linear model ใช้ทั้ง 10 คอลัมน์: test R² 0.801", "A linear model on all 10 columns: test R² 0.801"),
    l10_problem,
    [
        (2, "วิธีที่ 1: เลือกเอง", "Way 1: pick by hand", l10_hand, "ของเราผ่านทั้ง 10\nตัดเองไม่ออก", "our 10 all pass:\nnothing to drop"),
        (3, "วิธีที่ 2: ให้โค้ดเลือก", "Way 2: let code pick", l10_algo, "test R² 0.807 ✓", "test R² 0.807 ✓"),
        (4, "วิธีที่ 3: ปรับค่าตั้ง", "Way 3: tune settings", l10_tune, "test R² 0.805 ✓", "test R² 0.805 ✓"),
        (5, "ทบทวน", "Review", l10_review, "ใช้ชุด test ครั้งเดียว\nตอนท้ายสุด", "test set used once,\nat the very end"),
    ],
    (None, "feature คือโมเดลเรียนจาก “อะไร” · hyperparameter คือเรียน “อย่างไร”",
     "Features: what the model learns from · hyperparameters: how it learns"),
)


# ================================================================ L11 logistic regression (obesity)
def l11_problem(s, x, y, w, h):
    x0, x1, y1, y0 = x + 44, x + w - 56, y + 22, y + 82
    Y = lambda p: y0 - p * (y0 - y1)
    s.line(x0, y1, x1, y1, "mp-guide")
    s.line(x0, y0, x1, y0, "mp-guide")
    s.text(x0 - 12, y1 + 5, "1", "mp-s", "end")
    s.text(x0 - 12, y0 + 5, "0", "mp-s", "end")
    for f in (0.02, 0.12, 0.22, 0.3, 0.4, 0.5, 0.58):
        circ(s, x0 + f * (x1 - x0), y0, 5, "var(--muted)")
    for f in (0.55, 0.68, 0.8, 0.9, 1.0):
        circ(s, x0 + f * (x1 - x0), y1, 5, "var(--accent)")
    s.line(x0, Y(-0.21), x1, Y(0.51), "mp-curve-b")
    s.text(x1 + 8, Y(0.51) + 6, "0.51", "mp-acc")
    s.text(x0 + 6, y + 110, "−0.21", "mp-acc")
    s.text(x1, y + 108, "120 kg", "mp-s", "middle")


def l11_sigmoid(s, x, y, w, h):
    x0, x1, y1, y0 = x + 34, x + w - 14, y + 18, y + 88
    Y = lambda p: y0 - p * (y0 - y1)
    for p, lab in ((1, "1"), (0.5, "0.5"), (0, "0")):
        s.line(x0, Y(p), x1, Y(p), "mp-guide")
        s.text(x0 - 8, Y(p) + 5, lab, "mp-s", "end")
    for f in (0.04, 0.16, 0.3, 0.42):
        circ(s, x0 + f * (x1 - x0), y0, 4.5, "var(--muted)")
    for f in (0.66, 0.8, 0.94):
        circ(s, x0 + f * (x1 - x0), y1, 4.5, "var(--accent)")
    sig = lambda t: 1 / (1 + math.exp(-12 * (t - 0.55)))
    poly(s, [(x0 + t / 40 * (x1 - x0), Y(sig(t / 40))) for t in range(41)], "mp-curve-b")
    xm, pm = x0 + 0.77 * (x1 - x0), sig(0.77)
    s.line(xm, y0, xm, Y(pm), "mp-straight")
    circ(s, xm, Y(pm), 6, "var(--accent)")
    s.text(xm + 10, Y(pm) + 24, "0.93", "mp-acc")
    s.both(xm, y + 110, "100 กก.", "100 kg", "mp-s", "middle")


def l11_softmax(s, x, y, w, h):
    probs = [0.06, 0.14, 0.22, 0.58]
    names = [("ผอม", "Under"), ("ปกติ", "Normal"), ("เกิน", "Over"), ("อ้วน", "Obese")]
    for k, p in enumerate(probs):
        bx = x + 17 + k * 52
        bh = p / 0.58 * 66
        s.fill(bx, y + 90 - bh, 34, bh, CLS[k], 3)
        s.both(bx + 17, y + 110, *names[k], "mp-s", "middle")
    s.text(x + 17 + 3 * 52 + 17, y + 18, "✓", "ml-ok", "middle")
    s.both(x + 14, y + 22, "รวม = 1", "sum = 1", "mp-s")


def l11_recall(s, x, y, w, h):
    s.both(x + w / 2, y + 20, "คนน้ำหนักเกินในชุด test 9 คน", "9 Overweight people in test", "mp-s", "middle")
    for i in range(9):
        person(s, x + 20 + i * 23, y + 56, CLS[2], outline=i >= 4)
    s.line(x + 12, y + 80, x + 98, y + 80, "mp-axis")
    s.both(x + 55, y + 102, "จับได้ 4", "caught 4", "mp-acc", "middle")
    s.both(x + 158, y + 102, "พลาด 5", "missed 5", "mp-s", "middle")


def l11_roc(s, x, y, w, h):
    x0, x1, y1, y0 = x + 22, x + 118, y + 12, y + 106
    s.raw(f'<path d="M{x0} {y0} C{x0} {y1 + 14} {x0 + 14} {y1} {x1} {y1} L{x1} {y0} Z" class="mp-area"/>')
    s.raw(f'<path d="M{x0} {y0} C{x0} {y1 + 14} {x0 + 14} {y1} {x1} {y1}" class="mp-curve"/>')
    s.line(x0, y0, x1, y1, "mp-guide")
    s.line(x0, y1, x0, y0, "mp-axis")
    s.line(x0, y0, x1, y0, "mp-axis")
    s.text(x + 170, y + 50, "AUC", "mp-s", "middle")
    s.text(x + 170, y + 82, "0.94", "mp-big", "middle")


info_map(
    "l11-map-lesson.svg",
    "Lesson map. The problem: predict which of 4 weight groups each of 108 people is in; a straight line gives no "
    "probability (120 kg gets only 0.51, the lightest −0.21). Four steps: 2 a line inside a sigmoid (100 kg: 0.93, "
    "obese), 3 four groups with softmax (test accuracy 0.82, 27 of 33), 4 count the mistakes (Overweight: 4 of 9 "
    "caught, recall 0.44), 5 move the threshold (Overweight AUC 0.94), then 6 evaluate and review.",
    ("obesity · 108 คน · 4 กลุ่ม", "obesity · 108 people · 4 groups"),
    ("แต่ละคนอยู่กลุ่มน้ำหนักไหน", "Which weight group is each person in?"),
    ("✗ เส้นตรงไม่ใช่ความน่าจะเป็น: 120 กก. → 0.51", "✗ A straight line is no probability: 120 kg → 0.51"),
    l11_problem,
    [
        (2, "เส้นตรงใน sigmoid", "Line → sigmoid", l11_sigmoid, "100 กก. → อ้วน ✓", "100 kg → Obese ✓"),
        (3, "4 กลุ่ม: softmax", "Four groups: softmax", l11_softmax, "ถูก 0.82 ✓\n(27 จาก 33 คน)", "accuracy 0.82 ✓\n(27 of 33 people)"),
        (4, "นับว่าผิดแบบไหน", "Count the mistakes", l11_recall, "recall 4/9 = 0.44 ✗", "recall 4/9 = 0.44 ✗"),
        (5, "เลื่อน threshold", "Move the threshold", l11_roc, "เรียงคะแนนคนได้ดี ✓", "scores rank well ✓"),
    ],
    (6, "ประเมินโมเดลภาวะน้ำหนักด้วยทุกเครื่องมือ แล้วทบทวน", "Evaluate the obesity model with every tool, then review"),
)


# ================================================================ L12 text as data (wine reviews)
def l12_problem(s, x, y, w, h):
    for i, (lab, cls) in enumerate([("“Fresh and fragrant…”", "rc-ctx"), ("$15", "ml-cell-b"), ("Italy", "ml-cell-b")]):
        bw = (150, 56, 66)[i]
        bx = x + 12 + sum((150, 56, 66)[:i]) + i * 6
        s.box(bx, y + 16, bw, 36, cls, 6)
        s.text(bx + bw / 2, y + 39, lab, "mp-c", "middle")
    s.text(x + 24, y + 84, "text + number + group → ?", "hk-mono")
    s.both(x + 24, y + 106, "โมเดลต้องการตัวเลขแถวเดียว", "a model needs one row of numbers", "mp-s")


def l12_text(s, x, y, w, h):
    s.box(x + 14, y + 14, w - 28, 30, "rc-ctx", 6)
    s.text(x + w / 2, y + 34, "tasting note", "mp-c", "middle")
    s.arrow(x + w / 2, y + 48, x + w / 2, y + 62)
    for i in range(24):
        s.fill(x + 16 + i * 8, y + 68, 6, 30, CLS[0], 1)
    s.text(x + w / 2, y + 116, "384 numbers", "mp-s", "middle")


def l12_others(s, x, y, w, h):
    s.text(x + 18, y + 30, "$15 → log →", "mp-c")
    s.fill(x + 120, y + 14, 22, 24, "var(--accent)", 3)
    s.text(x + 150, y + 31, "−0.93", "mp-acc")
    for i in range(14):
        s.box(x + 18 + i * 13, y + 58, 11, 24, "ml-cell-b" if i == 4 else "ml-cell", 2)
    s.text(x + 18, y + 106, "one-hot: 24 + 132", "mp-s")


def l12_join(s, x, y, w, h):
    for i, (bw, col) in enumerate([(110, CLS[0]), (8, "var(--accent)"), (24, CLS[1]), (52, CLS[2])]):
        bx = x + 14 + sum((110, 8, 24, 52)[:i]) + i * 3
        s.fill(bx, y + 34, bw, 40, col, 3)
    s.text(x + w / 2, y + 100, "384 + 1 + 156", "mp-c", "middle")


def l12_compare(s, x, y, w, h):
    for k, (lab, v, col) in enumerate([("text", 0.389, CLS[0]), ("others", 0.400, "var(--accent)"), ("both", 0.529, CLS[1])]):
        bx, bh = x + 22 + k * 66, v / 0.53 * 72
        s.fill(bx, y + 92 - bh, 44, bh, col, 3)
        s.text(bx + 22, y + 86 - bh, f"{v:.2f}".lstrip("0"), "mp-c", "middle")
        s.text(bx + 22, y + 110, lab, "mp-s", "middle")


info_map(
    "l12-map-lesson.svg",
    "Lesson map. The problem: predict the points of 1,000 wines from a tasting note (text), a price (number) and a "
    "country and grape (groups); a model needs one row of numbers. Part 2 the note becomes a vector (MiniLM, 384 "
    "numbers). Part 3 price is logged and scaled (wine 1: −0.93), country and grape are one-hot (24 + 132). Part 4 the "
    "blocks join into one row of 541 numbers. Part 5 Ridge with 5-fold CV: text alone R² 0.389, other columns 0.400, "
    "both 0.529. Part 6 review.",
    ("รีวิวไวน์ 1,000 ขวด · คะแนน 80–100", "1,000 wine reviews · points 80–100"),
    ("คำ ราคา และกลุ่ม ทำนายคะแนนได้แค่ไหน", "Words, price and groups: how well do they predict points?"),
    ("✗ ข้อความกับตัวเลขคนละชนิด: ต้องเป็นแถวเดียวก่อน", "✗ Text and numbers differ: make them one row first"),
    l12_problem,
    [
        (2, "ข้อความ → vector", "Text → vector", l12_text, "1,000 × 384", "1,000 × 384"),
        (3, "คอลัมน์อื่น → ตัวเลข", "Others → numbers", l12_others, "1 + 156 คอลัมน์", "1 + 156 columns"),
        (4, "ต่อเป็นแถวเดียว", "Join into one row", l12_join, "541 ตัวเลขต่อขวด ✓", "541 numbers a wine ✓"),
        (5, "ฝึกและเปรียบเทียบ", "Train and compare", l12_compare, "R² 0.39 / 0.40 → 0.53 ✓", "R² 0.39 / 0.40 → 0.53 ✓"),
    ],
    (6, "ขั้นตอนทั้งหมด คำศัพท์ และคำถามท้ายบท", "Steps, key terms and exit ticket"),
)


# ================================================================ L13 other classifiers (obesity)
def l13_problem(s, x, y, w, h):
    rnd = random.Random(7)
    X = lambda t: x + 18 + t * 264
    Y = lambda v: y + 106 - v * 96
    band = lambda k, t: 0.08 + 0.22 * k + 0.18 * math.sin(math.pi * t)
    for k in range(4):
        for i in range(7):
            t = (i + rnd.uniform(0.1, 0.9)) / 7
            v = band(k, t) + rnd.uniform(-0.04, 0.04)
            circ(s, X(t), Y(v), 4.5, CLS[k])
    poly(s, [(X(t / 30), Y(band(1, t / 30) + 0.11)) for t in range(31)], "mp-curve")
    s.line(X(0), Y(0.42), X(1), Y(0.42), "mp-straight")


def l13_entropy(s, x, y, w, h):
    s.stack(x + 12, y + 22, 200, 34, [47, 29, 20, 12])
    s.text(x + w / 2, y + 92, "1.83 bits", "mp-big", "middle")
    s.both(x + w / 2, y + 112, "สูงสุด 2 bits", "max 2 bits", "mp-s", "middle")


def l13_tree(s, x, y, w, h):
    def node(cx, cy, label):
        s.box(cx - 50, cy - 12, 100, 24, "ml-cell", 6)
        s.text(cx, cy + 5, label, "mp-mono", "middle")

    def leaf(cx, cy, k, n):
        s.fill(cx - 18, cy - 12, 36, 24, CLS[k], 5)
        if n:
            s.text(cx, cy + 6, str(n), "pl-num", "middle")

    s.line(x + 112, y + 32, x + 40, y + 50, "mp-axis")
    s.line(x + 112, y + 32, x + 160, y + 50, "mp-axis")
    s.line(x + 160, y + 74, x + 116, y + 90, "mp-axis")
    s.line(x + 160, y + 74, x + 186, y + 90, "mp-axis")
    node(x + 112, y + 20, "BMI ≤ 20.6")
    leaf(x + 40, y + 62, 0, 37)
    node(x + 160, y + 62, "BMI ≤ 24.6")
    leaf(x + 116, y + 102, 1, 20)
    s.fill(x + 164, y + 90, 21, 24, CLS[2], 5)
    s.fill(x + 188, y + 90, 21, 24, CLS[3], 5)


def l13_forest(s, x, y, w, h):
    for i in range(5):
        cx = x + 30 + i * 41
        s.line(cx, y + 16, cx - 9, y + 34, "mp-axis")
        s.line(cx, y + 16, cx + 9, y + 34, "mp-axis")
        circ(s, cx, y + 16, 5.5, "var(--ink-2)")
        circ(s, cx - 9, y + 34, 4.5, CLS[3] if i != 2 else CLS[2])
        circ(s, cx + 9, y + 34, 4.5, CLS[1])
    s.arrow(x + 112, y + 44, x + 112, y + 60)
    s.stack(x + 12, y + 64, 200, 26, [0, 0, 6, 94])
    s.both(x + w / 2, y + 112, "อ้วน 94 · น้ำหนักเกิน 6", "Obese 94 · Overweight 6", "mp-s", "middle")


def l13_knn(s, x, y, w, h):
    cx, cy = x + 130, y + 62
    ring(s, cx, cy, 25, "mp-ring")
    ring(s, cx, cy, 47, "mp-ring-d")
    near = [((-15, -9), 3), ((14, -12), 3), ((4, 17), 2)]
    mid = [((-38, 12), 2), ((37, 14), 2), ((-6, -38), 3), ((27, -30), 2)]
    far = [((-68, 30), 1), ((72, 34), 3), ((70, -36), 1)]
    for (dx, dy), k in near + mid + far:
        circ(s, cx + dx, cy + dy, 5, CLS[k])
    star = " L".join(f"{cx + (8 if i % 2 == 0 else 3.4) * math.sin(i * math.pi / 5):.1f} "
                     f"{cy - (8 if i % 2 == 0 else 3.4) * math.cos(i * math.pi / 5):.1f}" for i in range(10))
    s.raw(f'<path d="M{star} Z" style="fill:var(--ink)"/>')
    s.line(x + 10, y + 18, x + 28, y + 18, "mp-ring")
    s.text(x + 34, y + 23, "k = 3", "mp-s")
    s.line(x + 10, y + 40, x + 28, y + 40, "mp-ring-d")
    s.text(x + 34, y + 45, "k = 7", "mp-s")


info_map(
    "l13-map-lesson.svg",
    "Lesson map. The problem: the 4 weight groups of 108 people are separated by curves, but logistic regression cuts "
    "with straight lines (5-fold accuracy 0.88). Four parts: 2 measure the mix with entropy (labels 47, 29, 20, 12: 1.83 "
    "bits of a possible 2), 3 grow a decision tree (BMI ≤ 20.6 gives 37 Underweight; 22 of 22 test people right), "
    "4 let many trees vote (a forest of 100: Obese 94, Overweight 6; CV 0.989 vs one tree 0.977), 5 ask the neighbours "
    "(k = 3 says Obese, k = 7 says Overweight), then 6 compare and choose a model.",
    ("obesity · 108 คน · 4 กลุ่ม", "obesity · 108 people · 4 groups"),
    ("โมเดลตามเส้นแบ่งที่โค้งได้ไหม", "Can a model follow curved borders?"),
    ("✗ logistic regression ตัดได้แค่เส้นตรง: ถูก 0.88", "✗ Logistic regression cuts only straight: 0.88 right"),
    l13_problem,
    [
        (2, "วัดความปน: entropy", "Measure the mix", l13_entropy, "ยิ่งปน ยิ่งเดายาก", "mixed = hard to guess"),
        (3, "ปลูกต้นไม้ตัดสินใจ", "Grow a tree", l13_tree, "test ถูก 22 จาก 22 ✓", "22 of 22 test right ✓"),
        (4, "หลายต้นช่วยกันโหวต", "Many trees vote", l13_forest, "CV 0.989 ✓\n(ต้นเดียว 0.977)", "CV 0.989 ✓\n(one tree 0.977)"),
        (5, "ถามเพื่อนบ้าน", "Ask the neighbours", l13_knn, "k = 3 → อ้วน\nk = 7 → น้ำหนักเกิน", "k = 3 → Obese\nk = 7 → Overweight"),
    ],
    (6, "เทียบทุกโมเดลกับข้อมูลชุดเดียวกัน แล้วเลือกให้เหมาะกับงาน", "Compare every model on the same data, then choose for the job"),
)


# ================================================================ L14 simulation (Persuasion)
CH = [2625, 1993, 2854, 1817, 3350, 3844, 3467, 3367, 2887, 3881, 3029, 5589,
      2775, 2550, 2837, 2420, 3518, 4159, 2410, 3518, 7036, 5942, 6625, 1601]
VOL = ["var(--tag-concept-dot)", "var(--tag-example-dot)"]


def l14_problem(s, x, y, w, h):
    base, top = y + 92, 80 / 7036
    for i, c in enumerate(CH):
        s.fill(x + 20 + i * 11, base - c * top, 8, c * top, VOL[i // 12], 2)
    ym = base - 3189.5 * top
    s.line(x + 14, ym, x + 286, ym, "mp-straight")
    s.both(x + w / 2, y + 110, "เส้นประ: median 3,190 คำ", "dashed: median 3,190 words", "mp-s", "middle")


def l14_mc(s, x, y, w, h):
    reach = ["100%", "30%", "6%", "3%", "0.3%"]
    for i, (n, p) in enumerate(zip("ABCDE", [0.3, 0.2, 0.5, 0.1, None])):
        cx = x + 24 + i * 44
        if p is not None:
            s.arrow(cx + 15, y + 52, cx + 29, y + 52)
            s.text(cx + 22, y + 32, f"{p:g}", "mp-s", "middle")
        ring(s, cx, y + 52, 14, "mp-ring" if n == "E" else "mp-axis")
        s.text(cx, y + 58, n, "mp-n", "middle")
        s.text(cx, y + 90, reach[i], "mp-acc" if n == "E" else "mp-s", "middle")
    s.both(x + w / 2, y + 113, "จำลอง 100,000 รอบ", "100,000 runs", "mp-s", "middle")


def l14_boot(s, x, y, w, h):
    rows = [[1, 2, 2, 2, 5, 7, 7, 7], [1, 1, 2, 3, 3, 4, 4, 5], [1, 1, 4, 4, 5, 6, 6, 8]]
    for i in range(8):
        chip(s, x + 10 + i * 26, y + 6, 22, 22, str(i + 1), "ml-cell-b")
    s.arrow(x + w / 2, y + 30, x + w / 2, y + 42)
    for r, row in enumerate(rows):
        for i, v in enumerate(row):
            chip(s, x + 10 + i * 26, y + 46 + r * 24, 22, 20, str(v), "rc-ctx" if row.count(v) > 1 else "ml-cell")


def l14_perm(s, x, y, w, h):
    order = [3, 6, 0, 5, 1, 7, 2, 4]
    for i in range(8):
        s.fill(x + 10 + i * 26, y + 12, 22, 22, VOL[i // 4], 4)
        s.fill(x + 10 + i * 26, y + 70, 22, 22, VOL[order[i] // 4], 4)
        j = order.index(i)
        s.line(x + 21 + i * 26, y + 36, x + 21 + j * 26, y + 68, "mp-axis")
    s.both(x + w / 2, y + 112, "สลับป้าย 10,000 ครั้ง", "shuffle the labels 10,000×", "mp-s", "middle")


def l14_review(s, x, y, w, h):
    for i in range(13):
        bh = 70 * math.exp(-((i - 6) / 2.6) ** 2 / 2)
        s.box(x + 8 + i * 16, y + 92 - bh, 14, bh, "ml-bar", 2)
    xr = x + 8 + 10.5 * 16
    s.line(xr, y + 30, xr, y + 92, "mp-curve")
    s.both(xr, y + 22, "ผลจริง", "real", "mp-acc", "middle")
    s.both(x + w / 2, y + 112, "โลกจำลองหลายพันโลก", "thousands of simulated worlds", "mp-s", "middle")


info_map(
    "l14-map-lesson.svg",
    "Lesson map. The problem: some questions have no formula, such as how sure we can be of the median chapter length of "
    "Persuasion (24 chapters, median 3,190 words). Three ways to answer by simulating other worlds: 2 Monte Carlo (news "
    "passed A to E with chances 0.3, 0.2, 0.5, 0.1 reaches E in 0.3% of 100,000 runs), 3 bootstrap (resample the "
    "chapters: median 95% CI 2,775 to 3,518 words), 4 permutation test (shuffle the volume labels: volume II is 557 "
    "words longer per chapter, but p = 0.36), then 5 review: compare the real result with thousands of simulated worlds.",
    ("Persuasion · 24 บท · คำต่อบท", "Persuasion · 24 chapters · words each"),
    ("median 3,190 คำ เชื่อได้แค่ไหน", "How sure is the median, 3,190 words?"),
    ("✗ ไม่มีสูตรหาช่วงของ median", "✗ No formula gives a median's range"),
    l14_problem,
    [
        (2, "วิธีที่ 1: Monte Carlo", "Way 1: Monte Carlo", l14_mc, "ข่าวถึง E\nแค่ 0.3% ของรอบ", "news reaches E\nin 0.3% of runs"),
        (3, "วิธีที่ 2: Bootstrap", "Way 2: Bootstrap", l14_boot, "95% CI ของ median:\n2,775–3,518 คำ ✓", "median 95% CI:\n2,775–3,518 words ✓"),
        (4, "วิธีที่ 3: Permutation", "Way 3: Permutation", l14_perm, "เล่ม 2 ยาวกว่า 557 คำ\nแต่ p = 0.36", "volume II +557 words\nbut p = 0.36"),
        (5, "ทบทวน", "Review", l14_review, "ไม่มีสูตร?\nก็จำลองเอา", "no formula?\nsimulate it"),
    ],
    (None, "ทั้งสามวิธีสร้างโลกคู่ขนานหลายพันโลก แล้วดูว่าผลจริงแปลกแค่ไหน",
     "All three build thousands of other worlds, then ask how unusual the real result is"),
)


# ================================================================ L15 data reliability (letters)
def l15_problem(s, x, y, w, h):
    s.raw(f'<path d="M{x + 16} {y + 16} h44 l14 14 v68 h-58 Z" class="ml-cell"/>')
    for k in range(5):
        s.line(x + 24, y + 42 + k * 11, x + 66, y + 42 + k * 11, "mp-guide")
    s.both(x + 45, y + 110, "จดหมายฉบับที่ 3", "letter 3", "mp-s", "middle")
    s.both(x + 190, y + 18, "ความเป็นทางการ 1–10", "formality 1–10", "mp-s", "middle")
    for (n, v), cx in zip((("A", 1), ("B", 9), ("C", 8)), (x + 130, x + 190, x + 250)):
        embed_png(s, {"A": "cast-ra-a.png", "B": "cast-ra-b.png", "C": "cast-ra-c.png"}[n], cx - 20, y + 20, 40, 54)
        s.text(cx - 18, y + 52, n, "mp-c", "end")
        chip(s, cx - 16, y + 76, 32, 26, str(v), "rc-con", "mp-n")


def l15_quality(s, x, y, w, h):
    for cx, (dx, dy), col in ((x + 60, (16, -14), "var(--accent)"), (x + 164, (0, 0), "var(--tag-exercise-dot)")):
        for r in (32, 21, 10):
            ring(s, cx, y + 46, r, "mp-axis")
        for ox, oy in ((0, 0), (4, 3), (-3, 4), (3, -4), (-4, -2)):
            circ(s, cx + dx + ox, y + 46 + dy + oy, 3, col)
    s.both(x + 60, y + 92, "ตรงกัน", "consistent", "mp-s", "middle")
    s.both(x + 60, y + 114, "แต่ผิด", "but wrong", "mp-acc", "middle")
    s.both(x + 164, y + 92, "ตรงกัน", "consistent", "mp-s", "middle")
    s.both(x + 164, y + 114, "และถูก", "and right", "mp-s", "middle")


def l15_guide(s, x, y, w, h):
    s.box(x + 12, y + 12, 58, 96, "ml-cell", 6)
    s.fill(x + 20, y + 22, 40, 8, "var(--tag-concept-dot)", 2)
    for k in range(6):
        s.line(x + 20, y + 42 + k * 11, x + 62, y + 42 + k * 11, "mp-guide")
    chip(s, x + 80, y + 18, 136, 28, "“It wasn't bad.”", "ml-cell")
    s.arrow(x + 148, y + 50, x + 148, y + 70)
    s.box(x + 98, y + 76, 100, 28, "rc-res", 6)
    s.both(x + 148, y + 96, "เป็นกลาง ✓", "Neutral ✓", "ml-ok", "middle")


def l15_agree(s, x, y, w, h):
    s.both(x + 12, y + 18, "ตรงกัน", "agree", "mp-s")
    s.fill(x + 12, y + 24, 144, 20, "var(--tag-concept-dot)", 4)
    s.text(x + 162, y + 40, "72%", "mp-n")
    s.both(x + 12, y + 62, "ตรงกันเพราะบังเอิญ", "by chance", "mp-s")
    s.box(x + 12, y + 68, 114, 20, "mp-area", 4)
    s.text(x + 132, y + 84, "57%", "mp-n")
    s.text(x + w - 12, y + 113, "κ = 0.35", "mp-big", "end")


def l15_scale(s, x, y, w, h):
    for k in range(3):
        s.box(x + 18 + k * 6, y + 26 + k * 6, 40, 52, "ml-cell", 4)
    s.both(x + 44, y + 108, "200 ฉบับ", "200 gold", "mp-n", "middle")
    s.arrow(x + 80, y + 56, x + 104, y + 56)
    for r in range(6):
        for c in range(10):
            s.fill(x + 112 + c * 10, y + 22 + r * 10, 8, 8, "var(--tag-concept-dot)", 1)
    s.text(x + 161, y + 108, "20,000", "mp-n", "middle")


info_map(
    "l15-map-lesson.svg",
    "Lesson map. The problem: three research assistants label 100 letters (1840–1890) for emotion and formality, and their "
    "labels disagree (letter 3 gets formality 1, 9 and 8; emotion alpha 0.375, formality ICC 0.418). Four parts: 2 know "
    "what quality means (consistent is not the same as correct), 3 write clear guidelines with examples (“It wasn't bad.” "
    "is Neutral), 4 measure agreement beyond chance (72% agree, 57% expected by chance, kappa 0.35), 5 scale up from 200 "
    "hand-labelled letters to 20,000, then 6 the case study: after revising the guidelines, alpha 0.684 and ICC 0.807.",
    ("จดหมาย 100 ฉบับ · ผู้ช่วยวิจัย 3 คน", "100 letters · 3 research assistants"),
    ("ป้ายจากผู้ช่วยวิจัยเชื่อได้ไหม", "Can we trust the assistants' labels?"),
    ("✗ ไม่ตรงกัน: อารมณ์ α 0.375 · ความเป็นทางการ ICC 0.418", "✗ They disagree: emotion α 0.375 · formality ICC 0.418"),
    l15_problem,
    [
        (2, "คุณภาพคืออะไร", "What quality means", l15_quality, "ตรงกัน ≠ ถูกต้อง", "consistent ≠ correct"),
        (3, "เขียนคู่มือให้ชัด", "Clear guidelines", l15_guide, "นิยาม + ตัวอย่าง ✓", "rules + examples ✓"),
        (4, "วัดความตรงกัน", "Measure agreement", l15_agree, "ตรงกันแค่พอใช้ ✗", "only fair agreement ✗"),
        (5, "ขยายเป็นหลายหมื่น", "Scale up", l15_scale, "ติดป้ายเองแค่น้อย\nแล้วใช้ให้คุ้ม", "label a little by hand,\nuse it well"),
    ],
    (6, "กรณีศึกษา: แก้คู่มือแล้ววัดใหม่ α 0.375 → 0.684 · ICC 0.418 → 0.807",
     "Case study: revise the guidelines, measure again: α 0.375 → 0.684 · ICC 0.418 → 0.807"),
)
