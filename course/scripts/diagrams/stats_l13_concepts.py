"""Concept pictures for stats-dh lesson 13 (other classification models and information
theory), in the style of nlp l13-why-chunk.svg: the running example's question on top, panels answering that
same question, drawn objects (people coloured by weight group, stacked bars, a tree, bootstrap bags), arrows at
the exact spot, the real numbers attached to what they describe. ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/stats_l13_concepts.py courses/stats-dh/images

Every number is a real run in course/.venv (the same as the lesson's code cells), obesity data, 108 people:
  Label counts Underweight 47, Normal Weight 29, Overweight 20, Obese 12: entropy 1.834 bits, Gini 0.692.
  Gender split: Female 52 (32, 12, 8, 0) H 1.335; Male 56 (15, 17, 12, 12) H 1.984; weighted 1.671; IG 0.163.
  Weight <= 52.5 split: 47 Underweight (H 0) | 61 others (0, 29, 20, 12) H 1.499; weighted 0.847; IG 0.988.
  Depth-3 tree (80/20 stratified split, random_state=42; train 86 = U 37, N 23, Ov 16, Ob 10): BMI <= 20.6 →
      Underweight 37; BMI <= 24.6 → Normal 20; Weight <= 97.5 → Overweight (16 + 3 Normal); else Obese 10.
      Test: 22 of 22 right.
  Bootstrap draws (numpy default_rng(3), rows 1–8): {1,2,2,2,5,7,7,7}, {1,1,2,3,3,4,4,5}, {1,1,4,4,5,6,6,8}.
  Random forest (100 trees, Height and Weight, random_state=42) on a new person 186 cm, 100 kg: Obese 94,
      Overweight 6.
  Boosting toy (Height → Weight, 4 people 160/60, 175/80, 180/90, 190/100, depth-1 trees, learning rate 1):
      start 82.5 for all, squared error 875; round 1 (split 167.5) 60, 90, 90, 90 → 200; round 2 (split 185)
      56.7, 86.7, 86.7, 100 → 66.7.
  Model comparison (Worksheet 5: 5 features, MinMaxScaler, GridSearchCV f1_weighted, 22 test people):
      CV / test: LR 0.846 / 0.953, tree 0.977 / 0.953, RF 0.989 / 0.953, GB 0.976 / 0.953, SVM 0.861 / 0.903, KNN 0.823 / 0.858.

Uses the nt-*, pl-*, ml-*, sw-*, rc-*, dg-*, hk-* classes in templates/page.css.
"""

from stats_svg import CLS, NAMES, H, Svg, W, math, width  # noqa: F401



# ================================================================ L12 surprise: which ending tells you more?
s = Svg(W, "Information is surprise. Left: after 'The sun rises in the', the word 'east' has probability 0.99, so "
           "seeing it gives only 0.01 bits. Right: after 'The defendant, in a surprising turn, pleaded', guilty and "
           "not guilty have 0.45 each (1.15 bits), for mercy 0.09 (3.47 bits) and bananas 0.01 (6.64 bits). "
           "Surprise I(x) = −log2 p(x): the rarer the word, the more bits. Probabilities are made up for the example.")
s.bubble("ตอนจบแบบไหนให้ข้อมูลกับเรามากกว่ากัน", "Which ending tells you more?")
PW = 560
SIDES = [
    (20, "นักเดาคำถัดไปเห็น “The sun rises in the …”", "A next-word guesser sees “The sun rises in the …”",
     [("east", 0.99), ("west", 0.01)], 0, ("✗ แทบไม่แปลกใจ: 0.01 bits", "✗ almost no surprise: 0.01 bits")),
    (600, "เห็น “The defendant, in a surprising turn, pleaded …”", "It sees “The defendant, in a surprising turn, pleaded …”",
     [("guilty", 0.45), ("not guilty", 0.45), ("for mercy", 0.09), ("bananas", 0.01)], 3,
     ("✓ คำหายาก = ข้อมูลมาก: bananas 6.64 bits", "✓ a rare word = much information: bananas 6.64 bits")),
]
for x0, th, en, words, hl, (rth, ren) in SIDES:
    s.box(x0, 70, PW, 400, "nt-band-a" if x0 > 100 else "sw-warn-box", 14)
    s.both(x0 + 20, 106, th, en, "pl-label")
    s.both(x0 + 20, 140, "คำถัดไป · ความน่าจะเป็น p · ความแปลกใจ −log₂ p", "next word · probability p · surprise −log₂ p", "pl-note")
    for k, (wd, p) in enumerate(words):
        y = 168 + k * 56
        lit = k == hl
        s.text(x0 + 20, y + 24, wd, "pl-label" if lit else "pl-text")
        s.box(x0 + 150, y + 6, p * 230, 24, "ml-bar-top" if lit else "ml-bar", 4)
        s.text(x0 + 158 + p * 230, y + 25, f"{p:.2f}", "pl-note")
        bits = -math.log2(p)
        s.text(x0 + PW - 24, y + 25, f"{bits:.2f} bits", "pl-label" if lit else "pl-note", "end")
    s.both(x0 + 20, 448, rth, ren, "ml-neg" if x0 < 100 else "ml-ok")
s.both(20, 506, "ความแปลกใจ I(x) = −log₂ p(x): p = ½ → 1 bit · p = ⅛ → 3 bits · p = 1 → 0 bits",
       "Surprise I(x) = −log₂ p(x): p = ½ → 1 bit · p = ⅛ → 3 bits · p = 1 → 0 bits", "pl-label")
s.both(20, 538, "ความน่าจะเป็นในภาพเป็นตัวเลขสมมติเพื่ออธิบาย", "The probabilities in this picture are made up for the example", "pl-note")
s.save("l13-surprise.svg", 556)

# ================================================================ L12 entropy: three groups of people
GROUPS = [
    ("กลุ่มที่ 1: อ้วนทั้งหมด", "Group 1: all Obese", [0, 0, 0, 12], "H = 0 bits", ("✓ รู้คำตอบแน่นอน ไม่ต้องถาม", "✓ certain: no question needed")),
    ("กลุ่มที่ 2: ครึ่งต่อครึ่ง", "Group 2: half and half", [0, 0, 6, 6], "H = 1 bit", ("ถามคำถาม ใช่/ไม่ใช่ 1 ข้อ", "one yes/no question")),
    ("กลุ่มที่ 3: คน 108 คนจริง", "Group 3: the real 108 people", [47, 29, 20, 12], "H = 1.83 bits", ("✗ ปนมาก เดายาก (สูงสุด 2)", "✗ very mixed, hard to guess (max 2)")),
]
s = Svg(W, "Entropy is the average surprise of a group's labels. Group 1, 12 people all Obese: H = 0 bits. Group 2, "
           "6 Overweight and 6 Obese: H = 1 bit. Group 3, the real 108 people (47 Underweight, 29 Normal, 20 "
           "Overweight, 12 Obese): H = 1.83 bits; with 4 groups the maximum is 2 bits.")
s.bubble("ถ้าสุ่มคนหนึ่งคนจากกลุ่มนี้ เดากลุ่มน้ำหนักได้ง่ายแค่ไหน", "Pick one person from this group: how easy is it to guess their weight group?")
PW = 364
for i, (th, en, counts, hval, (rth, ren)) in enumerate(GROUPS):
    x0 = 20 + i * (PW + 24)
    s.box(x0, 70, PW, 420, "nt-band-a", 14)
    s.badge(x0 + 32, 96, i + 1)
    s.both(x0 + 54, 102, th, en, "pl-label")
    # the people: up to 36 drawn, coloured in proportion
    n = sum(counts)
    shown = 12 if n <= 12 else 36
    seq = []
    for k, c in enumerate(counts):
        seq += [k] * round(c * shown / n)
    seq = seq[:shown]
    cols, dx = (6, 52) if n <= 12 else (9, 34)
    for j, k in enumerate(seq):
        px = x0 + 46 + (j % cols) * dx
        py = 156 + (j // cols) * 40
        s.person(px, py, CLS[k])
    if n > 12:
        s.both(x0 + 20, 322, "(36 ตัวแทน 108 คน ตามสัดส่วนจริง)", "(36 stand for 108, in the real shares)", "pl-note")
    s.stack(x0 + 20, 350, PW - 40, 30, counts)
    s.text(x0 + 20, 428, hval, "pl-label")
    s.both(x0 + 20, 466, rth, ren, "ml-ok" if "✓" in ren else "ml-neg" if "✗" in ren else "pl-text")
s.legend(20, 524)
s.both(20, 560, "H = −Σ pᵢ log₂ pᵢ  ·  กลุ่ม 3: −(0.435 log₂ 0.435 + 0.269 log₂ 0.269 + 0.185 log₂ 0.185 + 0.111 log₂ 0.111) = 1.83",
       "H = −Σ pᵢ log₂ pᵢ  ·  group 3: −(0.435 log₂ 0.435 + 0.269 log₂ 0.269 + 0.185 log₂ 0.185 + 0.111 log₂ 0.111) = 1.83", "pl-label")
s.save("l13-entropy.svg", 578)

# ================================================================ L12 information gain: two questions compared
s = Svg(W, "Information gain compares two first questions for the 108 people (entropy 1.83 bits). Question A, "
           "'Is the person male?': Female 52 (32, 12, 8, 0) H 1.33 and Male 56 (15, 17, 12, 12) H 1.98; weighted "
           "1.67; gain 0.16 bits. Question B, 'Weight ≤ 52.5 kg?': yes 47, all Underweight, H 0; no 61 (29, 20, 12) "
           "H 1.50; weighted 0.85; gain 0.99 bits. B is the better question.")
s.bubble("ถามคำถามแรกข้อเดียว ข้อไหนช่วยแยกกลุ่มน้ำหนักได้ดีกว่า", "One first question: which one sorts the weight groups better?")
SPLITS = [
    (20, "sw-warn-box", "A", "เป็นผู้ชายไหม", "Is the person male?",
     [("หญิง 52", "Female 52", [32, 12, 8, 0]), ("ชาย 56", "Male 56", [15, 17, 12, 12])],
     "1.67", "0.16", ("✗ ทั้งสองฝั่งยังปน: ได้แค่ 0.16 bits", "✗ both sides still mixed: only 0.16 bits")),
    (600, "nt-band-a", "B", "น้ำหนัก ≤ 52.5 กก. ไหม", "Weight ≤ 52.5 kg?",
     [("ใช่ 47", "yes 47", [47, 0, 0, 0]), ("ไม่ใช่ 61", "no 61", [0, 29, 20, 12])],
     "0.85", "0.99", ("✓ ฝั่ง “ใช่” บริสุทธิ์: ได้ 0.99 bits", "✓ the yes side is pure: 0.99 bits")),
]
for x0, cls, letter, qth, qen, kids, wavg, gain, (rth, ren) in SPLITS:
    s.box(x0, 70, 560, 470, cls, 14)
    s.badge(x0 + 32, 96, letter)
    s.both(x0 + 54, 102, f"คำถาม: {qth}", f"Question: {qen}", "pl-label")
    s.both(x0 + 20, 138, "ก่อนถาม: 108 คน", "Before: 108 people", "pl-note")
    s.stack(x0 + 20, 150, 520, 30, [47, 29, 20, 12])
    s.text(x0 + 540, 206, "H = 1.83", "pl-note", "end")
    s.arrow(x0 + 160, 214, x0 + 130, 254)
    s.arrow(x0 + 400, 214, x0 + 430, 254)
    for j, (kth, ken, counts) in enumerate(kids):
        kx = x0 + 20 + j * 270
        s.both(kx, 280, kth, ken, "pl-label")
        bw = 250 * sum(counts) / 61
        s.stack(kx, 292, bw, 30, counts)
        hk = H(counts)
        s.text(kx, 350, f"H = {hk:.2f}".replace("-0.00", "0") if hk > 0.004 else "H = 0", "pl-label" if hk < 0.01 else "pl-text")
    s.both(x0 + 20, 400, f"เฉลี่ยถ่วงน้ำหนักหลังถาม = {wavg}", f"Weighted average after = {wavg}", "pl-text")
    s.both(x0 + 20, 436, f"information gain = 1.83 − {wavg} = {gain}", f"information gain = 1.83 − {wavg} = {gain}", "pl-label")
    s.both(x0 + 20, 512, rth, ren, "ml-neg" if "✗" in ren else "ml-ok")
s.legend(20, 572)
s.both(20, 606, "IG = H(ก่อนถาม) − Σ (nₖ / n) · H(กลุ่มย่อย k)  ·  ข้อ B: 47/108 × 0 + 61/108 × 1.50 = 0.85",
       "IG = H(before) − Σ (nₖ / n) · H(group k)  ·  question B: 47/108 × 0 + 61/108 × 1.50 = 0.85", "pl-label")
s.save("l13-info-gain.svg", 624)

# ================================================================ L12 the decision tree the data grew
s = Svg(W, "The depth-3 decision tree trained on 86 people. Root: BMI ≤ 20.6? yes → leaf Underweight (37). No → "
           "BMI ≤ 24.6? yes → leaf Normal Weight (20). No → Weight ≤ 97.5 kg? yes → leaf Overweight (16, plus 3 "
           "Normal Weight); no → leaf Obese (10). On the 22 test people it is right 22 times.")
s.bubble("ต้นไม้ถามคำถามทีละข้อ คนหนึ่งคนเดินจากบนลงล่างจนถึงใบ", "The tree asks one question at a time; a person walks down until a leaf")


def node(x, y, th, en, counts, kind):
    """kind: root / node / leaf; a box with the question (or the answer) and the people that reach it."""
    w = 300
    s.box(x - w / 2, y, w, 92, "ml-cell-b" if kind != "leaf" else "rc-res", 12)
    s.both(x, y + 30, th, en, "pl-label", "middle")
    s.stack(x - 130, y + 46, 260, 26, counts)
    s.text(x, y + 88 + 18, f"n = {sum(counts)}", "pl-note", "middle")


node(330, 74, "BMI ≤ 20.6 ?", "BMI ≤ 20.6 ?", [37, 23, 16, 10], "root")
node(150, 236, "→ ผอม", "→ Underweight", [37, 0, 0, 0], "leaf")
node(560, 236, "BMI ≤ 24.6 ?", "BMI ≤ 24.6 ?", [0, 23, 16, 10], "node")
node(380, 398, "→ ปกติ", "→ Normal Weight", [0, 20, 0, 0], "leaf")
node(780, 398, "น้ำหนัก ≤ 97.5 ?", "Weight ≤ 97.5 ?", [0, 3, 16, 10], "node")
node(620, 560, "→ น้ำหนักเกิน", "→ Overweight", [0, 3, 16, 0], "leaf")
node(960, 560, "→ อ้วน", "→ Obese", [0, 0, 0, 10], "leaf")
for (x1, y1, x2, y2, yes) in [(330, 166, 150, 236, True), (330, 166, 560, 236, False), (560, 328, 380, 398, True),
                              (560, 328, 780, 398, False), (780, 490, 620, 560, True), (780, 490, 960, 560, False)]:
    s.arrow(x1 + (-40 if yes else 40), y1 + 22, x2, y2 - 4)
    s.both((x1 + x2) / 2 + (-34 if yes else 34), (y1 + y2) / 2 + 18, "ใช่" if yes else "ไม่ใช่", "yes" if yes else "no", "pl-note", "middle")
# labels for the parts of a tree
s.line(500, 106, 600, 106, "dg-rule")
s.both(612, 112, "root node: คำถามแรก (ใช้ทุกคน)", "root node: the first question (everyone)", "pl-text")
s.both(880, 270, "internal node: คำถามต่อ", "internal node: a later question", "pl-text")
s.line(730, 266, 870, 266, "dg-rule")
s.both(150, 380, "↑ leaf: คำตอบ", "↑ leaf: the answer", "pl-text", "middle")
s.both(20, 704, "✓ คน test 22 คน: ทายถูก 22 คน · ต้นไม้หาเกณฑ์ BMI เองจากข้อมูล ไม่มีใครบอกมัน",
       "✓ 22 test people: 22 right · the tree found the BMI cut-offs from the data by itself", "ml-ok")
s.legend(20, 742)
s.save("l13-tree.svg", 760)

# ================================================================ L12 random forest: bootstrap bags and a vote
ROWS = [(1, 1), (2, 1), (3, 2), (4, 0), (5, 3), (6, 0), (7, 3), (8, 0)]  # row id, weight group
BAGS = [[1, 2, 2, 2, 5, 7, 7, 7], [1, 1, 2, 3, 3, 4, 4, 5], [1, 1, 4, 4, 5, 6, 6, 8]]
s = Svg(W, "A random forest. Top: 8 rows of the data. Each tree gets a bootstrap sample: 8 rows drawn with "
           "replacement, so some rows repeat and some are left out (tree 1: 2 and 7 three times, 3, 4, 6, 8 left "
           "out). Each tree also sees only a random subset of columns at each question. For a new person, 186 cm "
           "and 100 kg, a forest of 100 trees votes Obese 94, Overweight 6, so the forest says Obese.")
s.bubble("คนใหม่ สูง 186 ซม. หนัก 100 กก. ให้ต้นไม้หลายต้นช่วยกันตอบ", "A new person, 186 cm, 100 kg: let many trees answer together")
s.both(20, 100, "ข้อมูลฝึก 8 แถว (ตัวอย่าง)", "Training data, 8 rows (example)", "pl-label")
for j, (rid, k) in enumerate(ROWS):
    x = 300 + j * 66
    s.box(x, 76, 56, 40, "ml-cell", 8)
    s.fill(x + 6, 86, 10, 20, CLS[k], 2)
    s.text(x + 36, 103, str(rid), "pl-label", "middle")
for t, bag in enumerate(BAGS):
    x0 = 20 + t * 388
    s.box(x0, 150, 364, 330, "nt-band-a", 14)
    s.badge(x0 + 32, 176, t + 1)
    s.both(x0 + 54, 182, f"ต้นที่ {t + 1}: สุ่มแบบใส่คืน 8 ครั้ง", f"Tree {t + 1}: 8 draws with replacement", "pl-label")
    for j, rid in enumerate(bag):
        x = x0 + 18 + j * 42
        dup = bag.count(rid) > 1
        s.box(x, 206, 36, 36, "rc-ctx" if dup else "ml-cell", 6)
        s.text(x + 18, 230, str(rid), "pl-label", "middle")
    out = [r for r, _ in ROWS if r not in bag]
    s.both(x0 + 20, 272, "ไม่ถูกสุ่ม: " + ", ".join(map(str, out)), "left out: " + ", ".join(map(str, out)), "ml-neg")
    rep = sorted({r for r in bag if bag.count(r) > 1})
    s.both(x0 + 20, 302, "ซ้ำ: " + ", ".join(map(str, rep)), "repeated: " + ", ".join(map(str, rep)), "pl-note")
    # a little tree icon
    tx, ty = x0 + 182, 340
    s.raw(f'<path d="M{tx} {ty} L{tx - 50} {ty + 50} M{tx} {ty} L{tx + 50} {ty + 50} M{tx + 50} {ty + 50} L{tx + 20} {ty + 96} M{tx + 50} {ty + 50} L{tx + 80} {ty + 96}" class="dg-rule-strong" fill="none"/>')
    for (cx, cy) in [(tx, ty), (tx - 50, ty + 50), (tx + 50, ty + 50), (tx + 20, ty + 96), (tx + 80, ty + 96)]:
        s.raw(f'<circle cx="{cx}" cy="{cy}" r="9" class="ml-cell-b"/>')
s.both(20, 520, "แต่ละต้นเห็นข้อมูลต่างกันเล็กน้อย และแต่ละคำถามเลือกได้จากคอลัมน์ที่สุ่มมาบางส่วน ต้นไม้จึงไม่เหมือนกัน",
       "Each tree sees slightly different rows, and each question may use only a random few columns, so the trees differ", "pl-text")
s.box(20, 544, 1140, 70, "rc-res", 12)
s.both(40, 572, "forest 100 ต้นโหวตให้คนใหม่: อ้วน 94 เสียง · น้ำหนักเกิน 6 เสียง", "100 trees vote on the new person: Obese 94 · Overweight 6", "pl-label")
s.fill(640, 556, 94 * 4.8, 22, CLS[3], 3)
s.fill(640 + 94 * 4.8, 556, 6 * 4.8, 22, CLS[2], 3)
s.both(40, 602, "✓ เสียงข้างมาก → อ้วน", "✓ majority → Obese", "ml-ok")
s.save("l13-forest.svg", 630)

# ================================================================ L12 gradient boosting: each tree fixes the leftovers
PEOPLE = [(160, 60), (175, 80), (180, 90), (190, 100)]
ROUNDS = [("เริ่ม: ทายค่าเฉลี่ย", "Start: guess the mean", [82.5] * 4, 875.0),
          ("รอบ 1: + ต้นที่แบ่งที่ 167.5 ซม.", "Round 1: + a tree split at 167.5 cm", [60, 90, 90, 90], 200.0),
          ("รอบ 2: + ต้นที่แบ่งที่ 185 ซม.", "Round 2: + a tree split at 185 cm", [56.67, 86.67, 86.67, 100], 66.7)]
s = Svg(W, "Gradient boosting on 4 people, predicting weight from height. Start by guessing the mean, 82.5 kg, for "
           "everyone: residuals −22.5, −2.5, 7.5, 17.5, squared error 875. Round 1 adds a small tree trained on those "
           "residuals (split at 167.5 cm): predictions 60, 90, 90, 90, squared error 200. Round 2 adds a tree "
           "trained on the new residuals (split at 185 cm): 56.7, 86.7, 86.7, 100, squared error 66.7.")
s.bubble("ทายน้ำหนักจากส่วนสูง: ต้นใหม่แต่ละต้นเรียนจาก “ส่วนที่ยังผิด”", "Predict weight from height: each new tree learns the part still wrong")
PW = 364
for r, (th, en, pred, sse) in enumerate(ROUNDS):
    x0 = 20 + r * (PW + 24)
    s.box(x0, 70, PW, 440, "nt-band-a" if r else "sw-warn-box", 14)
    s.badge(x0 + 32, 96, r)
    s.both(x0 + 54, 102, th, en, "pl-label")
    base = 420
    for j, ((h, w), p) in enumerate(zip(PEOPLE, pred)):
        x = x0 + 48 + j * 80
        sc = 2.6
        s.box(x, base - (w - 40) * sc, 30, (w - 40) * sc, "ml-bar", 4)            # true weight
        s.line(x - 8, base - (p - 40) * sc, x + 38, base - (p - 40) * sc, "ml-cut")  # prediction
        res = w - p
        if abs(res) > 0.5:
            s.line(x + 15, base - (p - 40) * sc, x + 15, base - (w - 40) * sc, "pl-line")
        s.text(x + 15, base + 24, f"{h}", "pl-note", "middle")
        s.text(x + 15, base - (max(w, p) - 40) * sc - 10, f"{res:+.1f}".replace("+0.0", "0").replace("-", "−"), "pl-label" if abs(res) > 0.5 else "ml-ok", "middle")
    s.line(x0 + 30, base, x0 + PW - 20, base, "dg-rule-strong")
    s.both(x0 + 20, 478, f"squared error = {sse:g}", f"squared error = {sse:g}", "ml-neg" if r == 0 else "ml-ok")
s.both(20, 548, "แท่ง = น้ำหนักจริง · เส้นแดง = ค่าที่ทาย · ตัวเลข = residual (จริง − ทาย) ที่ต้นถัดไปต้องเรียน · ส่วนสูงใต้แท่ง (ซม.)",
       "bar = true weight · red line = prediction · number = residual (true − predicted) the next tree learns · height under each bar (cm)", "pl-note")
s.both(20, 582, "ค่าทายสุดท้าย = ค่าเริ่ม + ต้นที่ 1 + ต้นที่ 2 + …  (งานจริงคูณแต่ละต้นด้วย learning rate เช่น 0.1)",
       "Final prediction = start + tree 1 + tree 2 + …  (in practice each tree is scaled by a learning rate such as 0.1)", "pl-label")
s.save("l13-boosting.svg", 600)

# ================================================================ L12 SVM: the widest street, and the kernel trick
s = Svg(W, "Support vector machine. Panel 1: many lines separate the two groups, but a line that passes close to "
           "the points is fragile. Panel 2: SVM picks the line with the widest margin (the empty street between the "
           "groups); the points on the edge of the street are the support vectors. Panel 3: points on one line, "
           "group B in the middle, cannot be split by one cut; adding x² as a second axis lifts the outer points "
           "up, and now a straight line separates them. That is the kernel trick.")
s.bubble("เส้นแบ่งสองกลุ่มมีได้หลายเส้น เส้นไหนดีที่สุด", "Many lines split two groups: which one is best?")
A = [(70, 300), (100, 250), (130, 330), (150, 280), (90, 360)]
B = [(240, 180), (270, 230), (300, 160), (230, 130), (290, 120)]


def dots(x0, extra=None):
    for (x, y) in A:
        s.raw(f'<circle cx="{x0 + x}" cy="{y}" r="9" style="fill:var(--tag-concept-dot)"/>')
    for (x, y) in B:
        s.raw(f'<rect x="{x0 + x - 8}" y="{y - 8}" width="16" height="16" style="fill:var(--accent)"/>')


PW = 364
for i in range(3):
    s.box(20 + i * (PW + 24), 70, PW, 420, "sw-warn-box" if i == 0 else "nt-band-a", 14)
# 1 a fragile line
x0 = 20
s.badge(x0 + 32, 96, 1)
s.both(x0 + 54, 102, "เส้นที่เฉียดจุด", "A line that grazes the points", "pl-label")
dots(x0)
s.line(x0 + 60, 140, x0 + 330, 400, "ml-cut-guess")
s.line(x0 + 30, 200, x0 + 340, 300, "ml-cut-guess")
s.line(x0 + 120, 120, x0 + 230, 420, "ml-cut")
s.both(x0 + 20, 452, "✗ จุดใหม่ขยับนิดเดียวก็ข้ามเส้น", "✗ a point nudged a little crosses it", "ml-neg")
# 2 the widest street: a real linear SVM (sklearn SVC, kernel="linear", C=1e6) fitted on these 10 points gives
#   w = (0.013333, −0.008002), b = −0.75946; support vectors (150, 280), (240, 180), (270, 230); margin 128.6
x0 = 20 + PW + 24
s.badge(x0 + 32, 96, 2)
s.both(x0 + 54, 102, "ถนนที่กว้างที่สุด (margin)", "The widest street (the margin)", "pl-label")
WV, BV = (0.013333, -0.008002), -0.75946
xat = lambda c, yy: (c - BV - WV[1] * yy) / WV[0]   # x on the line w·p + b = c at height yy
Y1, Y2 = 124, 436
s.raw(f'<path d="M{x0 + xat(-1, Y1):.1f} {Y1} L{x0 + xat(1, Y1):.1f} {Y1} L{x0 + xat(1, Y2):.1f} {Y2} L{x0 + xat(-1, Y2):.1f} {Y2} Z" style="fill:var(--card);opacity:.85"/>')
for c in (-1, 1):
    s.line(x0 + xat(c, Y1), Y1, x0 + xat(c, Y2), Y2, "ml-cut-guess")
s.line(x0 + xat(0, Y1), Y1, x0 + xat(0, Y2), Y2, "ml-cut")
dots(x0)
for (x, y) in [(150, 280), (240, 180), (270, 230)]:
    s.raw(f'<circle cx="{x0 + x}" cy="{y}" r="16" fill="none" class="pl-line"/>')
s.both(x0 + 24, 404, "◯ = support vectors", "◯ = support vectors", "pl-label")
s.both(x0 + 20, 452, "✓ จุดที่ขอบถนนเท่านั้นที่กำหนดเส้น", "✓ the edge points alone decide it", "ml-ok")
# 3 the kernel trick
x0 = 20 + 2 * (PW + 24)
s.badge(x0 + 32, 96, 3)
s.both(x0 + 54, 102, "kernel: เพิ่มมิติ", "Kernel: add a dimension", "pl-label")
s.both(x0 + 20, 136, "จุดบนเส้นเดียว: B อยู่ตรงกลาง", "points on one line: B in the middle", "pl-note")
XS = [(-3, "A"), (-2.4, "A"), (-0.8, "B"), (0, "B"), (0.7, "B"), (2.2, "A"), (2.9, "A")]
for xv, g in XS:
    px = x0 + 182 + xv * 50
    if g == "A":
        s.raw(f'<circle cx="{px}" cy="176" r="8" style="fill:var(--tag-concept-dot)"/>')
    else:
        s.raw(f'<rect x="{px - 7}" y="169" width="14" height="14" style="fill:var(--accent)"/>')
s.line(x0 + 20, 196, x0 + PW - 20, 196, "dg-rule-strong")
s.both(x0 + 20, 222, "✗ ตัดครั้งเดียวไม่ได้", "✗ no single cut works", "ml-neg")
s.arrow(x0 + 182, 232, x0 + 182, 254)
s.both(x0 + 196, 250, "เพิ่มแกน x²", "add an x² axis", "pl-note")
for xv, g in XS:
    px = x0 + 182 + xv * 50
    py = 420 - xv * xv * 15
    if g == "A":
        s.raw(f'<circle cx="{px}" cy="{py}" r="8" style="fill:var(--tag-concept-dot)"/>')
    else:
        s.raw(f'<rect x="{px - 7}" y="{py - 7}" width="14" height="14" style="fill:var(--accent)"/>')
s.line(x0 + 20, 420, x0 + PW - 20, 420, "dg-rule-strong")
s.line(x0 + 30, 378, x0 + PW - 30, 378, "ml-cut")
s.both(x0 + 20, 452, "✓ ตอนนี้เส้นตรงแบ่งได้", "✓ now a straight line splits them", "ml-ok")
s.both(20, 528, "จุดในภาพเป็นตัวอย่างสมมติ  ·  SVC(kernel=\"linear\") = เส้นตรง · SVC(kernel=\"rbf\") = เส้นโค้งผ่าน kernel",
       "The points are a made-up example  ·  SVC(kernel=\"linear\") = a straight line · SVC(kernel=\"rbf\") = curves through a kernel", "pl-note")
s.save("l13-svm.svg", 546)
