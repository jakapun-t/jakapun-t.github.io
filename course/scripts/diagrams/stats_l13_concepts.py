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
s.bubble("ตอนจบแบบไหนให้สารสนเทศกับเรามากกว่ากัน", "Which ending carries more information?")
PW = 560
SIDES = [
    (20, "นักเดาคำถัดไปเห็น “The sun rises in the …”", "A next-word guesser sees “The sun rises in the …”",
     [("east", 0.99), ("west", 0.01)], 0, ("✗ แทบไม่แปลกใจ: 0.01 bits", "✗ almost no surprise: 0.01 bits")),
    (600, "เห็น “The defendant, in a surprising turn, pleaded …”", "It sees “The defendant, in a surprising turn, pleaded …”",
     [("guilty", 0.45), ("not guilty", 0.45), ("for mercy", 0.09), ("bananas", 0.01)], 3,
     ("✓ คำหายาก = สารสนเทศมาก: bananas 6.64 bits", "✓ a rare word = much information: bananas 6.64 bits")),
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

# ================================================================ why log base 2: guess the bubble tea (one bit = one yes/no question)
TEAS = [("ชาไทย", "Thai tea", "#d9822b"), ("มัทฉะ", "Matcha", "#6a9a4a"), ("ชานม", "Milk tea", "#c8a882"),
        ("เอิร์ลเกรย์", "Earl Grey", "#9a7b5a"), ("เผือก", "Taro", "#8b6bb5"), ("มะม่วง", "Mango", "#e8b93a"),
        ("สตรอว์เบอร์รี", "Strawberry", "#e07a8a"), ("บราวน์ชูการ์", "Brown sugar", "#7a4a2a")]
ROWS_Q = [(None, None, None, range(8)),
          ("ข้อ 1: มีชาไหม?", "Q1: has tea in it?", "ไม่", range(4, 8)),
          ("ข้อ 2: เป็นรสผลไม้ไหม?", "Q2: fruity?", "ไม่", (4, 7)),
          ("ข้อ 3: สีม่วงไหม?", "Q3: purple?", "ใช่", (4,))]


def cup(x, y, col, alive):
    op = "1" if alive else ".18"
    s.raw(f'<g style="opacity:{op}"><path d="M{x - 17} {y} L{x + 17} {y} L{x + 13} {y + 44} L{x - 13} {y + 44} Z" '
          f'style="fill:{col}"/><rect x="{x - 20}" y="{y - 6}" width="40" height="7" rx="3" style="fill:var(--ink-2)"/>'
          f'<path d="M{x + 4} {y - 6} L{x + 10} {y - 22}" style="stroke:var(--ink-2);stroke-width:4;stroke-linecap:round"/>'
          + "".join(f'<circle cx="{x - 8 + k * 8}" cy="{y + 36}" r="3" style="fill:var(--ink)"/>' for k in range(3)) + "</g>")


s = Svg(W, "Why log base 2, with bubble tea. A friend secretly picked 1 of 8 drinks: Thai tea, matcha, milk tea, Earl "
           "Grey, taro, mango, strawberry, brown sugar. Q1 has tea in it? no: 4 left (taro, mango, strawberry, brown "
           "sugar). Q2 fruity? no: 2 left (taro, brown sugar). Q3 purple? yes: taro. Each yes/no question halves the "
           "options, so 8 options take 3 questions: 3 bits = −log2(1/8). Twice as many options need one more question: "
           "2 → 1, 4 → 2, 8 → 3, 1,024 → 10.")
s.bubble("เพื่อนแอบเลือกชานมไข่มุก 1 แก้วจาก 8 รส ถาม ใช่/ไม่ใช่ กี่ข้อถึงรู้?", "Your friend secretly picked 1 of 8 bubble teas. How many yes/no questions?")
CX0, CW = 360, 100
for r, (qth, qen, ans, alive) in enumerate(ROWS_Q):
    y = 96 + r * 104
    if qth is None:
        s.both(20, y + 30, "เริ่ม: 8 แก้ว", "start: 8 drinks", "pl-label")
    else:
        s.both(20, y + 22, qth, qen, "pl-label")
        s.both(20, y + 50, f"ตอบ: {ans} → เหลือ {len(alive)} แก้ว", f"answer: {'no' if ans == 'ไม่' else 'yes'} → {len(alive)} left",
               "mp-acc" if len(alive) == 1 else "mp-c")
    for i, (th, en, col) in enumerate(TEAS):
        x = CX0 + i * CW
        cup(x, y + 6, col, i in alive)
        if i in alive:
            s.both(x, y + 74, th, en, "mp-s", "middle")
s.box(10, 520, 1160, 94, "nt-band-a", 14)
s.both(30, 556, "3 คำถาม = 3 bits = −log₂(1/8)", "3 questions = 3 bits = −log₂(1/8)", "mp-q")
s.both(30, 594, "ตัวเลือกเพิ่ม 2 เท่า → ถามเพิ่ม 1 ข้อ: 2 แก้ว 1 ข้อ · 4 แก้ว 2 ข้อ · 8 แก้ว 3 ข้อ · 1,024 แก้ว แค่ 10 ข้อ",
       "twice the options → one more question: 2 drinks 1 · 4 drinks 2 · 8 drinks 3 · 1,024 drinks only 10", "pl-text")
s.save("l13-why-log2.svg", 626)

# ================================================================ why base 2: a yes/no answer is one binary digit
s = Svg(W, "Why base 2: a yes/no answer is one binary digit. 1: taro's answers no, no, yes become the code 0 0 1 "
           "(yes = 1, no = 0); bit is short for binary digit. 2: one more digit doubles the codes: 1 digit 0, 1 "
           "(2 codes); 2 digits 00 to 11 (2 × 2 = 4); 3 digits 000 to 111 (2 × 2 × 2 = 8), with taro's 0, 00, 001 "
           "lit. 3: a computer stores numbers the same way, each digit an off/on switch worth 4, 2, 1: 001 = 1, "
           "101 = 4 + 1 = 5, 111 = 4 + 2 + 1 = 7; 3 bits hold 0 to 7, which is 8 numbers. log2 asks back: how many "
           "2s multiply to 8? 2 × 2 × 2 = 2³ = 8, so log2 8 = 3 and −log2(1/8) = 3 bits.")
s.bubble("ทำไมต้อง log ฐาน 2? เพราะคำตอบ ใช่/ไม่ใช่ หนึ่งข้อ คือเลขฐานสอง 1 หลัก",
         "Why log base 2? Because one yes/no answer is one binary digit")
s.panel(20, 66, 500, 252, "ml-cell", "คำตอบของเผือก = รหัส 3 หลัก", "Taro's answers = a 3-digit code", 1)
for k, (qth, qen, ath, aen, d) in enumerate([("มีชาไหม?", "has tea?", "ไม่", "no", "0"),
                                              ("ผลไม้ไหม?", "fruity?", "ไม่", "no", "0"),
                                              ("สีม่วงไหม?", "purple?", "ใช่", "yes", "1")]):
    y = 112 + k * 48
    s.both(44, y + 26, qth, qen, "pl-text")
    s.both(214, y + 26, ath, aen, "pl-label")
    s.arrow(262, y + 19, 312, y + 19)
    s.box(322, y, 46, 38, "ml-cell-b", 8)
    s.text(345, y + 29, d, "mp-big", "middle")
cup(452, 126, "#8b6bb5", True)
s.text(452, 210, "001", "mp-big", "middle")
s.both(452, 234, "รหัสของเผือก", "taro's code", "pl-note", "middle")
s.both(44, 278, "ใช่ = 1 · ไม่ = 0 → หนึ่งคำตอบ = เลขฐานสอง 1 หลัก", "yes = 1 · no = 0 → one answer = one binary digit", "pl-note")
s.both(44, 304, "bit ย่อมาจาก binary digit (เลขฐานสอง 1 หลัก)", "bit is short for binary digit", "pl-label")

s.panel(540, 66, 620, 252, "ml-cell", "เพิ่ม 1 หลัก = รหัสมากขึ้น 2 เท่า", "One more digit = twice as many codes", 2)
for k, (n, how) in enumerate([(1, "2"), (2, "2×2 = 4"), (3, "2×2×2 = 8")]):
    y = 108 + k * 56
    s.both(560, y + 20, f"{n} หลัก", f"{n} digit{'s' if n > 1 else ''}", "pl-label")
    s.both(560, y + 42, f"{how} แบบ", how, "pl-note")
    for i in range(2 ** n):
        code = format(i, f"0{n}b")
        x = 700 + i * 56
        lit = code == "001"[:n]
        s.box(x, y + 4, 50, 36, "ml-cell-b" if lit else "ml-cell", 8)
        s.text(x + 25, y + 28, code, "mp-chip", "middle")
s.both(560, 300, "เพิ่ม 1 หลัก → รหัส × 2 · ตอบ 1 ข้อ → ตัวเลือก ÷ 2 · ช่องสีคือทางไปเผือก",
       "+1 digit → codes × 2 · +1 answer → options ÷ 2 · lit = taro's path", "pl-note")

s.panel(20, 330, 1140, 170, "ml-cell", "คอมพิวเตอร์ก็เก็บตัวเลขแบบนี้: แต่ละหลักคือสวิตช์ ปิด/เปิด (0/1) = 1 bit",
        "Computers store numbers the same way: each digit is an off/on switch (0/1) = 1 bit", 3)
for k, (bits, th, en) in enumerate([("001", "001 = 1 (รหัสของเผือก)", "001 = 1 (taro's code)"),
                                    ("101", "101 = 4 + 1 = 5", "101 = 4 + 1 = 5"),
                                    ("111", "111 = 4 + 2 + 1 = 7", "111 = 4 + 2 + 1 = 7")]):
    x0 = 44 + k * 250
    for j, (bit, val) in enumerate(zip(bits, (4, 2, 1))):
        x = x0 + j * 56
        s.text(x + 23, 384, f"×{val}", "pl-note", "middle")
        on = bit == "1"
        s.box(x, 392, 46, 40, "ml-cell-b" if on else "ml-cell", 8)
        s.text(x + 23, 422, bit, "mp-big" if on else "mp-chip", "middle")
    s.both(x0, 470, th, en, "pl-label")
s.both(800, 398, "3 bits เก็บได้ 000 ถึง 111", "3 bits hold 000 to 111", "pl-text")
s.both(800, 428, "= เลข 0 ถึง 7 = 8 ตัว = 2³", "= the numbers 0 to 7 = 8 = 2³", "pl-label")
s.both(800, 458, "ชานม 8 แก้วจึงต้องใช้ 3 bits", "so 8 bubble teas need 3 bits", "pl-text")
s.both(800, 484, "(ฐานสิบ: แต่ละหลักมี 10 แบบ 0–9)", "(base 10: each digit has 10 values, 0–9)", "pl-note")

s.box(10, 512, 1160, 90, "nt-band-a", 14)
s.both(30, 546, "log₂ 8 ถามกลับว่า: ต้องเอา 2 มาคูณกันกี่ตัวถึงได้ 8?  2 × 2 × 2 = 2³ = 8 → log₂ 8 = 3",
       "log₂ 8 asks back: how many 2s multiply to 8?  2 × 2 × 2 = 2³ = 8 → log₂ 8 = 3", "mp-q")
s.both(30, 582, "เผือกมีโอกาส p = ⅛ → −log₂(⅛) = log₂ 8 = 3 bits = รหัสฐานสอง 3 หลัก = 3 คำถาม",
       "taro has p = ⅛ → −log₂(⅛) = log₂ 8 = 3 bits = a 3-digit binary code = 3 questions", "pl-text")
s.save("l13-base2.svg", 614)

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

# ================================================================ cross-entropy for one person = the loss that trains a model
# Real run: LogisticRegression(max_iter=2000) on Height + Weight, all 108 people. Person ID 5 (male, 190 cm, 100 kg,
# Obese): q = Underweight 7.8e-34, Normal 5.3e-9, Overweight 0.102, Obese 0.898; −log2 0.898 = 0.155 bits.
# Mean over 108 people: −log2 q(true) = 0.073 bits; −ln q(true) = 0.051 = sklearn log_loss.
s = Svg(W, "Cross-entropy for one person is the loss that trains a model. Person 5 (male, 190 cm, 100 kg) is really "
           "Obese, so reality p is 0, 0, 0, 1. The logistic regression gives q = 0.000, 0.000, 0.102, 0.898. Each term "
           "is p × (−log2 q): 0 × 110 = 0, 0 × 27.5 = 0, 0 × 3.29 = 0, 1 × 0.155 = 0.155, so H(p, q) = 0.16 bits = "
           "−log2 P(true group). With two groups, p = (y, 1 − y) and q = (p̂, 1 − p̂) give −[y log p̂ + (1 − y) "
           "log(1 − p̂)], the log loss (binary cross-entropy). Training makes the average over all people as low as "
           "possible: 0.073 bits, or log loss 0.051 with log base e.")
s.bubble("cross-entropy ของคนหนึ่งคน = loss ที่ใช้ฝึกโมเดล", "Cross-entropy for one person = the loss that trains a model")
s.panel(20, 66, 650, 318, "ml-cell", "คนที่ 5 (ชาย 190 ซม. 100 กก.) อ้วนจริง", "Person 5 (male, 190 cm, 100 kg) is really Obese", 1)
for x, th, en in [(44, "กลุ่ม", "group"), (240, "จริง p", "real p"), (330, "โมเดล q", "model q"), (450, "p × (−log₂ q)", "p × (−log₂ q)")]:
    s.both(x, 132, th, en, "pl-note")
CE_ROWS = [("Underweight", 0, "0.000", "0 × 110 = 0"), ("Normal", 0, "0.000", "0 × 27.5 = 0"),
           ("Overweight", 0, "0.102", "0 × 3.29 = 0"), ("Obese", 1, "0.898", "1 × 0.155 = 0.155")]
for k, (g, pv, qv, term) in enumerate(CE_ROWS):
    y = 142 + k * 42
    lit = pv == 1
    if lit:
        s.box(32, y, 626, 38, "ml-cell-b", 8)
    s.text(44, y + 26, g, "pl-label" if lit else "pl-text")
    s.text(262, y + 26, str(pv), "pl-label" if lit else "pl-note", "middle")
    s.text(360, y + 26, qv, "pl-label" if lit else "pl-note", "middle")
    s.text(450, y + 26, term, "pl-label" if lit else "pl-note")
s.both(44, 338, "H(p, q) = 0.16 bits = −log₂ P(กลุ่มที่ถูก)", "H(p, q) = 0.16 bits = −log₂ P(true group)", "mp-q")
s.both(44, 368, "กลุ่มที่ไม่ได้เกิดคูณด้วย p = 0 จึงหายไป เหลือแค่กลุ่มที่ถูก",
       "groups that did not happen are multiplied by p = 0 and vanish", "pl-note")

s.panel(690, 66, 470, 318, "ml-cell", "ถ้ามีแค่ 2 กลุ่ม: อ้วน / ไม่อ้วน", "Only 2 groups: Obese / not Obese", 2)
s.both(714, 134, "ความจริง p = (y, 1 − y)", "reality p = (y, 1 − y)", "pl-text")
s.both(714, 166, "โมเดล q = (p̂, 1 − p̂)", "model q = (p̂, 1 − p̂)", "pl-text")
s.text(714, 214, "H(p, q) = −[ y log p̂ + (1 − y) log(1 − p̂) ]", "pl-label")
s.both(714, 252, "✓ นี่คือ log loss (binary cross-entropy)", "✓ this is log loss (binary cross-entropy)", "ml-ok")
s.both(714, 300, "คนที่ 5: y = 1, p̂ = 0.898", "person 5: y = 1, p̂ = 0.898", "pl-text")
s.both(714, 330, "→ −log₂ 0.898 = 0.16 bits เท่ากับ ①", "→ −log₂ 0.898 = 0.16 bits, same as ①", "pl-label")

s.box(10, 398, 1160, 100, "nt-band-a", 14)
s.both(30, 436, "ฝึกโมเดล = ปรับให้ cross-entropy เฉลี่ยของทุกคนต่ำที่สุด",
       "Training = make the average cross-entropy over everyone as low as possible", "mp-q")
s.both(30, 476, "logistic regression ของเรา (ส่วนสูง + น้ำหนัก, 108 คน): เฉลี่ย 0.073 bits = log loss 0.051 (scikit-learn ใช้ log ฐาน e)",
       "our logistic regression (height + weight, 108 people): 0.073 bits on average = log loss 0.051 (scikit-learn uses log base e)", "pl-text")
s.save("l13-ce-logloss.svg", 510)

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

# ================================================================ random forest: each tree's sample, column, vote → majority
# Bags: numpy default_rng(3), 4 draws of 8 rows. Trees: RandomForestClassifier(100, random_state=42) on Height and
# Weight, all 108 people; first question and vote for 186 cm, 100 kg: tree 1 Weight ≤ 52.5 Obese, tree 2
# Height ≤ 167.5 Obese, tree 3 Height ≤ 185 Obese, tree 7 Height ≤ 167.5 Overweight; all 100: Obese 94, Overweight 6.
ROWS = [(1, 1), (2, 1), (3, 2), (4, 0), (5, 3), (6, 0), (7, 3), (8, 0)]  # row id, weight group
FOREST = [(1, [1, 2, 2, 2, 5, 7, 7, 7], ("น้ำหนัก", "Weight"), "Weight ≤ 52.5?", 3),
          (2, [1, 1, 2, 3, 3, 4, 4, 5], ("ส่วนสูง", "Height"), "Height ≤ 167.5?", 3),
          (3, [1, 1, 4, 4, 5, 6, 6, 8], ("ส่วนสูง", "Height"), "Height ≤ 185?", 3),
          (7, [2, 4, 4, 5, 6, 6, 7, 8], ("ส่วนสูง", "Height"), "Height ≤ 167.5?", 2)]
s = Svg(W, "A random forest for a new person, 186 cm and 100 kg. Top: 8 example rows of training data. Each tree gets "
           "its own bootstrap sample (8 rows drawn with replacement: some repeat, some are left out) and, at each "
           "question, only a random column to choose from. Tree 1 first asks Weight ≤ 52.5 and votes Obese; tree 2 "
           "asks Height ≤ 167.5, Obese; tree 3 Height ≤ 185, Obese; tree 7 Height ≤ 167.5, Overweight. All 100 trees "
           "vote: Obese 94, Overweight 6. Majority vote: the forest answers Obese.")
s.bubble("คนใหม่ สูง 186 ซม. หนัก 100 กก. ให้ต้นไม้หลายต้นช่วยกันตอบ", "A new person, 186 cm, 100 kg: let many trees answer together")
s.both(20, 98, "ข้อมูลฝึก 8 แถว (ตัวอย่าง)", "Training data, 8 rows (example)", "pl-label")
for j, (rid, k) in enumerate(ROWS):
    x = 300 + j * 66
    s.box(x, 72, 56, 38, "ml-cell", 8)
    s.fill(x + 6, 81, 10, 20, CLS[k], 2)
    s.text(x + 36, 98, str(rid), "pl-label", "middle")
PW = 272
for t, (no, bag, (cth, cen), q, vote) in enumerate(FOREST):
    x0 = 20 + t * 290
    s.box(x0, 128, PW, 318, "nt-band-a", 14)
    s.badge(x0 + 28, 154, no)
    s.both(x0 + 50, 160, f"ต้นที่ {no}" + (" (เห็นต่าง)" if vote != 3 else ""), f"Tree {no}" + (" (disagrees)" if vote != 3 else ""), "pl-label")
    s.both(x0 + 14, 192, "① สุ่มแถวแบบใส่คืน:", "① rows, with replacement:", "pl-note")
    for j, rid in enumerate(bag):
        x = x0 + 14 + j * 31
        s.box(x, 202, 27, 30, "rc-ctx" if bag.count(rid) > 1 else "ml-cell", 6)
        s.text(x + 13.5, 223, str(rid), "mp-c", "middle")
    s.both(x0 + 14, 262, f"② สุ่มคอลัมน์ได้: {cth}", f"② random column: {cen}", "pl-note")
    s.box(x0 + 14, 274, PW - 28, 36, "ml-model", 18)
    s.text(x0 + PW / 2, 298, q, "ml-model-text", "middle")
    # a little tree, the new person's path lit
    tx, ty = x0 + PW / 2, 330
    pts = [(tx, ty), (tx - 46, ty + 30), (tx + 46, ty + 30), (tx + 20, ty + 60), (tx + 72, ty + 60)]
    s.raw(f'<path d="M{tx} {ty} L{tx - 46} {ty + 30} M{tx} {ty} L{tx + 46} {ty + 30} M{tx + 46} {ty + 30} '
          f'L{tx + 20} {ty + 60} M{tx + 46} {ty + 30} L{tx + 72} {ty + 60}" class="dg-rule-strong" fill="none"/>')
    lit = {0, 2, 4} if vote == 3 else {0, 2, 3}
    for i, (cx, cy) in enumerate(pts):
        s.raw(f'<circle cx="{cx}" cy="{cy}" r="8" ' + (f'style="fill:{CLS[vote]}"' if i in lit else 'class="ml-cell-b"') + "/>")
    s.box(x0 + 40, 400, PW - 80, 34, "ml-model", 8)
    s.fill(x0 + 40, 400, PW - 80, 34, CLS[vote], 8)
    s.both(x0 + PW / 2, 423, "③ โหวต: " + NAMES[vote][0], "③ vote: " + NAMES[vote][1], "pl-num", "middle")
    s.line(x0 + PW / 2, 446, 590, 478)
s.both(1160, 470, "… และอีก 96 ต้น", "… and 96 more trees", "pl-note", "end")
s.box(250, 478, 680, 68, "ml-cell-b", 12)
s.both(270, 504, "โหวตเสียงข้างมาก (100 ต้น)", "majority vote (100 trees)", "pl-label")
s.both(270, 534, "อ้วน 94 · น้ำหนักเกิน 6", "Obese 94 · Overweight 6", "pl-note")
s.fill(560, 500, 94 * 3.4, 24, CLS[3], 3)
s.fill(560 + 94 * 3.4, 500, 6 * 3.4, 24, CLS[2], 3)
s.arrow(590, 548, 590, 572)
s.box(390, 574, 400, 46, "rc-res", 12)
s.both(590, 604, "คำตอบของ forest: อ้วน ✓", "the forest answers: Obese ✓", "ml-ok", "middle")
s.save("l13-forest.svg", 632)

# gradient boosting: drawn frame by frame in stats_l13_boost.py (an animated ```stepper on card S13)

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
