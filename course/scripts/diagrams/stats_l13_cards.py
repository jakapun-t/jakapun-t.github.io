"""Pictures added above the text of stats-dh L13 cards (other classifiers and information theory), in the stats-dh card
style: a student can skim the picture and read the card's text for the detail.
  l13-ideas-everywhere.svg  S01  apps that already work like this lesson's ideas (Akinator, Wordle, fans-also-like, ...)
  l13-cross-entropy.svg     S05  reality p vs a model that believes 25% each; one Obese person, model A vs B
  l13-555-split.svg         S07  10 group-chat messages split by "has 555?"
  l13-gini-vs-entropy.svg   S09  the 49-person node and its two candidate questions
  l13-bootstrap-bags.svg    S12  three bootstrap bags of rows 1–8 (default_rng(3)) and the rows each leaves out
  l13-forest-settings.svg   S14  the four settings of forests and boosting, each drawn
  l13-scoreboard.svg        S18  six tuned models, CV and test weighted F1
  l13-choose-model.svg      S19  the four steps for choosing a model
  l13-key-terms.svg         S20  eight key terms with small drawings

    course/.venv/bin/python scripts/diagrams/stats_l13_cards.py courses/stats-dh/images

Real numbers (course/.venv, the same as the lesson's code cells): label shares 0.435, 0.269, 0.185, 0.111, H(p) 1.83,
H(p, q) 2.00; −log2 0.8 = 0.32, −log2 0.2 = 2.32. Has 555 per chat message (made up): Pim #1–5 all yes;
Tae #6–10 → no, no, yes, yes, no; IG 0.40. Node of 49 (23 Normal, 16 Overweight, 10 Obese, Gini 0.631): BMI ≤ 24.6 →
Gini 0.335, entropy 0.794; Weight ≤ 97.5 → Gini 0.385, entropy 0.777. Bootstrap bags: [1 2 2 2 5 7 7 7],
[1 1 2 3 3 4 4 5], [1 1 4 4 5 6 6 8]. Scoreboard (CV / test): Logistic 0.846 / 0.953, Tree 0.977 / 0.953, Forest
0.989 / 0.953, Boosting 0.976 / 0.953, KNN 0.823 / 0.858, SVM 0.861 / 0.903. The app tiles are analogies, not claims
about how each app is built. Uses the mp-*, ml-*, nt-*, rc-*, dg-*, pl-* classes in templates/page.css.
"""

import math

from stats_svg import CLS, Svg, app_grid, circ, embed_png, emoji_or_icon, ring, term_grid, width

W = 1100
HAM, MAD = "var(--tag-concept-dot)", "var(--tag-example-dot)"

# ================================================================ S01 different models, good at different jobs
BLUE, AMB = "var(--tag-concept-dot)", "var(--tag-example-dot)"


def pic_lr(x, y):
    for dx, dy in ((14, 60), (26, 70), (34, 52), (20, 44)):
        circ(s, x + dx, y + dy, 5, BLUE)
    for dx, dy in ((70, 22), (84, 34), (92, 16), (78, 12)):
        circ(s, x + dx, y + dy, 5, AMB)
    s.raw(f'<path d="M{x + 8} {y + 12} L{x + 104} {y + 74}" class="pl-line"/>')


def pic_tree(x, y):
    s.box(x + 38, y + 4, 36, 18, "ml-model", 4)
    for lx in (14, 74):
        s.raw(f'<path d="M{x + 56} {y + 22} L{x + lx + 16} {y + 42}" class="mp-axis"/>')
        s.box(x + lx, y + 42, 32, 16, "ml-cell-b", 4)
    for lx, col in ((4, BLUE), (34, AMB), (64, BLUE), (94, AMB)):
        s.raw(f'<path d="M{x + (30 if lx < 50 else 90)} {y + 58} L{x + lx + 8} {y + 72}" class="mp-axis"/>')
        circ(s, x + lx + 8, y + 76, 5, col)


def mini_tree(x, y, col=BLUE):
    s.raw(f'<path d="M{x} {y + 30} L{x + 14} {y} L{x + 28} {y + 30} Z" style="fill:{col}"/>')
    s.fill(x + 11, y + 30, 6, 10, "var(--muted)", 1)


def pic_forest(x, y):
    for i in range(3):
        mini_tree(x + 4 + i * 36, y + 8)
    s.raw(f'<path d="M{x + 18} {y + 52} L{x + 56} {y + 66} L{x + 90} {y + 52}" class="mp-axis"/>')
    s.both(x + 56, y + 84, "โหวต", "vote", "mp-s", "middle")


def pic_boost(x, y):
    for i in range(3):
        mini_tree(x + 2 + i * 40, y + 14, (BLUE, AMB, "var(--accent)")[i])
        if i < 2:
            s.raw(f'<path d="M{x + 32 + i * 40} {y + 34} L{x + 40 + i * 40} {y + 34}" class="pl-line"/>')
    s.both(x + 56, y + 80, "แก้ที่ต้นก่อนผิด", "fix the last one", "mp-s", "middle")


def pic_knn(x, y):
    for dx, dy, col in ((20, 20, BLUE), (90, 70, AMB), (96, 20, AMB), (14, 70, BLUE), (48, 34, BLUE), (66, 48, BLUE), (52, 60, AMB)):
        circ(s, x + dx, y + dy, 5, col)
    ring(s, x + 56, y + 46, 22, "mp-ring-d")
    s.text(x + 56, y + 52, "?", "mp-n", "middle")


def pic_svm(x, y):
    for dx, dy in ((12, 64), (24, 76), (30, 56), (8, 48)):
        circ(s, x + dx, y + dy, 5, BLUE)
    for dx, dy in ((84, 18), (96, 30), (100, 10), (76, 8)):
        circ(s, x + dx, y + dy, 5, AMB)
    for off, cls in ((0, "pl-line"), (-14, "mp-guide"), (14, "mp-guide")):
        s.raw(f'<path d="M{x + 16 + off} {y + 4} L{x + 92 + off} {y + 84}" class="{cls}"/>')


MODELS = [
    (pic_lr, "Logistic regression", "ตัดกลุ่มด้วยเส้นตรง", "cuts groups with a straight line",
     "ข้อมูลง่าย อธิบายน้ำหนักได้", "simple data, readable weights", "สแปมหรือไม่", "spam or not"),
    (pic_tree, "Decision tree", "ถามใช่/ไม่ใช่ทีละข้อ", "asks yes/no, one at a time",
     "กฎที่คนอ่านเข้าใจ", "rules people can read", "เกณฑ์อนุมัติเงินกู้", "loan approval rules"),
    (pic_forest, "Random forest", "ต้นไม้หลายต้นโหวต", "many trees vote",
     "ข้อมูลตาราง ปรับน้อยก็ได้ผลดี", "tables, good with little tuning", "เสี่ยงเป็นโรคไหม", "disease risk"),
    (pic_boost, "Gradient boosting", "ต้นใหม่แก้ที่ต้นก่อนผิด", "each tree fixes the last one",
     "มักแม่นที่สุดกับข้อมูลตาราง", "often the most accurate on tables", "จับการโกงบัตรเครดิต", "card fraud"),
    (pic_knn, "KNN", "ถามตัวอย่างที่ใกล้ที่สุด", "asks the nearest examples",
     "หาของที่คล้ายกัน", "finding similar items", "เพลงที่คุณน่าจะชอบ", "songs you may like"),
    (pic_svm, "SVM", "เว้นทางกว้างที่สุดระหว่างกลุ่ม", "keeps the widest gap",
     "คอลัมน์เยอะ ข้อมูลไม่มาก", "many columns, little data", "จัดข่าวเข้าหมวด", "news by topic"),
]
s = Svg(W, "No model is best at everything; each kind is good at a different job. Logistic regression cuts groups with "
           "a straight line (simple data, readable weights; e.g. spam or not). A decision tree asks yes/no questions one "
           "at a time (rules people can read; loan approval rules). A random forest lets many trees vote (tables, good "
           "with little tuning; disease risk). Gradient boosting adds trees that fix the last one's mistakes (often the "
           "most accurate on tables; card fraud). KNN asks the nearest examples (finding similar items; songs you may "
           "like). An SVM keeps the widest gap between groups (many columns, little data; news by topic).")
s.bubble("ไม่มีโมเดลไหนเก่งทุกงาน: แต่ละแบบเก่งคนละเรื่อง", "No model is best at everything: each kind is good at a different job")
TW_, TH2 = 352, 196
for k, (pic, name, hth, hen, gth, gen, eth, een) in enumerate(MODELS):
    x, y = 10 + (k % 3) * (TW_ + 12), 72 + (k // 3) * (TH2 + 14)
    s.box(x, y, TW_, TH2, "ml-cell", 14)
    s.box(x + 12, y + 12, 112, 92, "dg-xl-head", 10)
    pic(x + 12, y + 12)
    s.text(x + 138, y + 40, name, "mp-t")
    s.both(x + 138, y + 68, hth, hen, "hk-desc")
    s.both(x + 16, y + 134, "เก่งเรื่อง", "good at", "mp-s")
    w = max(width(gth, 16), width(gen, 16)) + 24
    s.box(x + 90, y + 116, min(w, TW_ - 100), 28, "ml-cell-b", 14)
    s.both(x + 90 + min(w, TW_ - 100) / 2, y + 136, gth, gen, "mp-chip", "middle")
    s.both(x + 16, y + 176, "เช่น", "e.g.", "mp-s")
    s.both(x + 90, y + 176, eth, een, "hk-desc")
s.save("l13-ideas-everywhere.svg", 72 + 2 * TH2 + 14 + 10)

# ================================================================ S05 cross-entropy
P = [0.435, 0.269, 0.185, 0.111]
s = Svg(W, "Cross-entropy. Left: reality p (Underweight 0.435, Normal 0.269, Overweight 0.185, Obese 0.111) beside a model "
           "q that believes 0.25 for every group. Reality's own average surprise is 1.83 bits; measured with the model's "
           "beliefs it is 2.00 bits, 0.17 bits more. Right: one person who is truly Obese. Model A gives P(Obese) 0.8, a "
           "surprise of 0.32 bits; model B gives 0.2, a surprise of 2.32 bits. Training makes this surprise small.")
s.bubble("ถ้าโมเดลเชื่อว่าทุกกลุ่มมี 25% มันจะแปลกใจแค่ไหน", "If a model believes 25% for every group, how surprised is it?")
s.panel(10, 70, 560, 290, "ml-cell", "ความจริง p กับสิ่งที่โมเดลเชื่อ q", "Reality p vs the model's belief q", 1)
base, sc = 270, 300
for k, p in enumerate(P):
    gx = 46 + k * 128
    s.fill(gx, base - p * sc, 40, p * sc, CLS[k], 3)
    s.text(gx + 20, base - p * sc - 8, f"{p:.3f}".rstrip("0"), "mp-s", "middle")
    s.box(gx + 46, base - 0.25 * sc, 40, 0.25 * sc, "pl-chip-del", 3)
    s.text(gx + 66, base - 0.25 * sc - 8, "0.25", "mp-s", "middle")
    short = [("ผอม", "Under"), ("ปกติ", "Normal"), ("เกิน", "Over"), ("อ้วน", "Obese")][k]
    s.both(gx + 43, base + 22, *short, "mp-c", "middle")
s.line(34, base, 556, base, "mp-axis")
s.fill(380, 112, 16, 16, CLS[0], 3)
s.both(402, 125, "ความจริง p", "reality p", "mp-c")
s.box(470, 112, 16, 16, "pl-chip-del", 3)
s.both(492, 125, "โมเดล q", "model q", "mp-c")
s.both(30, 344, "ความจริง 1.83 bits · ตามโมเดล 2.00 bits: เชื่อผิดเสีย 0.17", "reality 1.83 bits · by the model 2.00 bits: 0.17 lost",
       "mp-acc")
s.panel(590, 70, 500, 290, "ml-cell", "คนหนึ่งที่อ้วนจริง", "One person who is truly Obese", 2)
embed_png(s, "cast-obese.png", 596, 104, 68, 100)
for i, (m, q, ok) in enumerate((("A", 0.8, True), ("B", 0.2, False))):
    y = 140 + i * 90
    s.both(670, y, f"โมเดล {m}: P(อ้วน) = {q}", f"model {m}: P(Obese) = {q}", "mp-t")
    bits = -math.log2(q)
    s.fill(670, y + 16, bits * 90, 22, "var(--tag-exercise-dot)" if ok else "var(--accent)", 4)
    s.text(678 + bits * 90, y + 33, f"{bits:.2f} bits {'✓' if ok else '✗'}", "ml-ok" if ok else "ml-neg")
s.both(610, 344, "ฝึกโมเดล = ทำให้ความแปลกใจนี้ต่ำ (log loss)", "training = make this surprise small (log loss)", "mp-s")
s.save("l13-cross-entropy.svg", 370)

# ================================================================ S07 "555" splits the chat messages
CHATS = [("1", "H", 1), ("2", "H", 1), ("3", "H", 1), ("4", "H", 1), ("5", "H", 1),   # 1 = has 555
         ("6", "M", 0), ("7", "M", 0), ("8", "M", 1), ("9", "M", 1), ("10", "M", 0)]


def chat(x, y, w, h, who, label=None):
    col = HAM if who == "H" else MAD
    s.raw(f'<path d="M{x + 10:g} {y:g} h{w - 20:g} a10 10 0 0 1 10 10 v{h - 20:g} a10 10 0 0 1 -10 10 '
          f'h{-(w - 26):g} l-12 9 l2 -9 a10 10 0 0 1 -10 -10 v{-(h - 20):g} a10 10 0 0 1 10 -10 Z" style="fill:{col}"/>')
    if label is not None:
        s.text(x + w / 2, y + h / 2 + 7, label, "pl-num", "middle")


s = Svg(W, "Who sent it? Ten group-chat messages, coloured by sender (Pim blue, Tae amber), marked 555 if it "
           "has '555' (Thai for hahaha) and – if not. The question 'has 555?' sends 7 messages to yes (5 Pim, 2 Tae; entropy 0.86) "
           "and 3 to no (all Tae; entropy 0, pure). Information gain = 1 − (0.7 × 0.86 + 0.3 × 0) = 0.40 bits.")
s.bubble("คำว่า 555 ช่วยเดาคนส่งได้แค่ไหน? Pim หรือ Tae", "How much does “555” help you guess the sender: Pim or Tae?")
for i, (no, a, n) in enumerate(CHATS):
    x = 76 + i * 96
    chat(x, 72, 60, 50, a, "555" if n else "–")
    s.text(x + 30, 150, f"#{no}", "mp-s", "middle")
s.fill(30, 166, 16, 16, HAM, 3)
s.text(52, 179, "Pim", "mp-c")
s.fill(120, 166, 16, 16, MAD, 3)
s.text(142, 179, "Tae", "mp-c")
s.both(1080, 179, "บนฟอง: 555 = ข้อความมี 555 · – = ไม่มี", "on a bubble: 555 = the message has 555 · – = it does not", "mp-s", "end")
s.box(450, 194, 200, 38, "ml-model", 19)
s.both(550, 219, "มี 555 ไหม", "has “555”?", "ml-model-text", "middle")
s.arrow(480, 234, 330, 256)
s.arrow(620, 234, 790, 256)
s.box(80, 260, 500, 92, "nt-band-a", 12)
s.both(100, 284, "ใช่: 7 ข้อความ", "yes: 7 messages", "mp-c")
for i, (no, a, n) in enumerate([c for c in CHATS if c[2] > 0]):
    chat(100 + i * 44, 298, 34, 30, a)
s.text(560, 330, "H = 0.86", "mp-n", "end")
s.box(640, 260, 380, 92, "rc-res", 12)
s.both(660, 284, "ไม่ใช่: 3 ข้อความ", "no: 3 messages", "mp-c")
for i, (no, a, n) in enumerate([c for c in CHATS if c[2] == 0]):
    chat(660 + i * 44, 298, 34, 30, a)
s.text(1000, 330, "H = 0 ✓", "ml-ok", "end")
s.text(550, 384, "IG = 1 − (0.7 × 0.86 + 0.3 × 0) = 0.40 bits", "mp-acc", "middle")
s.save("l13-555-split.svg", 396)

# ================================================================ S09 entropy first, Gini as the add-on
s = Svg(W, "Entropy or Gini. The second node has 49 people: 23 Normal, 16 Overweight, 10 Obese (entropy 1.51 bits, Gini "
           "0.631). Question 1, BMI ≤ 24.6: yes 20 Normal (pure), no 3 Normal, 16 Overweight, 10 Obese (entropy 1.34); "
           "entropy after = 20/49 × 0 + 29/49 × 1.34 = 0.794, IG 0.71; Gini after 0.335. Question 2, Weight ≤ 97.5: yes 23 "
           "Normal, 16 Overweight (entropy 0.98), no 10 Obese (pure); entropy after = 39/49 × 0.98 + 10/49 × 0 = 0.777, "
           "IG 0.73; Gini after 0.385. Entropy picks question 2; Gini would pick question 1; both trees end with the same "
           "4 leaves.")
s.bubble("โหนดนี้ควรถามคำถามไหนก่อน", "Which question should this node ask first?")
s.stack(400, 74, 300, 34, [0, 23, 16, 10])
s.both(550, 132, "49 คน · entropy 1.51 bits (Gini 0.631)", "49 people · entropy 1.51 bits (Gini 0.631)", "mp-c", "middle")
PX = 6
for k, (q, yes, no, ent, ig, g, win) in enumerate((
        ("BMI ≤ 24.6", [0, 20, 0, 0], [0, 3, 16, 10], "20/49 × 0 + 29/49 × 1.34 = 0.794", "0.71", "0.335", False),
        ("Weight ≤ 97.5", [0, 23, 16, 0], [0, 0, 0, 10], "39/49 × 0.98 + 10/49 × 0 = 0.777", "0.73", "0.385", True))):
    x = 10 + k * 550
    s.arrow(550, 140, x + 270, 160)
    s.box(x, 164, 530, 250, "ml-cell-b" if win else "ml-cell", 14)
    s.both(x + 20, 196, f"คำถาม {k + 1}: {q}", f"Question {k + 1}: {q}", "mp-t")
    s.both(x + 20, 236, "ใช่", "yes", "mp-s")
    s.stack(x + 70, 218, sum(yes) * PX, 28, yes)
    s.both(x + 20, 276, "ไม่ใช่", "no", "mp-s")
    s.stack(x + 70, 258, sum(no) * PX, 28, no)
    s.both(x + 20, 320, f"entropy หลังถาม = {ent}", f"entropy after = {ent}", "mp-t")
    s.both(x + 20, 352, f"IG = 1.51 − {ent[-5:]} = {ig} bits" + (" ✓ entropy เลือกข้อนี้" if win else ""),
           f"IG = 1.51 − {ent[-5:]} = {ig} bits" + (" ✓ entropy picks this" if win else ""), "ml-ok" if win else "mp-r")
    s.both(x + 20, 392, f"ทางเลือกเสริม: Gini หลังถาม {g}" + (" (Gini จะเลือกข้อนี้)" if not win else ""),
           f"add-on: Gini after {g}" + (" (Gini would pick this)" if not win else ""), "mp-s")
s.save("l13-gini-vs-entropy.svg", 424)

# ================================================================ S12 bootstrap bags
BAGS = [[1, 2, 2, 2, 5, 7, 7, 7], [1, 1, 2, 3, 3, 4, 4, 5], [1, 1, 4, 4, 5, 6, 6, 8]]


def ball(x, y, n, kind):
    cls = {"data": "ml-cell-b", "once": "ml-cell", "again": "rc-ctx", "out": "pl-chip-del"}[kind]
    s.raw(f'<circle cx="{x:g}" cy="{y:g}" r="19" class="{cls}"/>')
    s.text(x, y + 5, str(n), "mp-s" if kind == "out" else "mp-c", "middle")


s = Svg(W, "Bootstrap bags. The data is rows 1 to 8. Each tree draws 8 rows with replacement (numpy default_rng(3)): tree 1 "
           "gets 1 2 2 2 5 7 7 7 and leaves out 3 4 6 8; tree 2 gets 1 1 2 3 3 4 4 5 and leaves out 6 7 8; tree 3 gets "
           "1 1 4 4 5 6 6 8 and leaves out 2 3 7. Shaded balls were drawn more than once.")
s.bubble("สุ่มแถว 1–8 แบบใส่คืน 8 ครั้ง ได้แถวไหนบ้าง", "Draw rows 1–8 with replacement, 8 times: which rows come out?")
s.both(30, 108, "ข้อมูล", "the data", "mp-t")
for i in range(8):
    ball(180 + i * 46, 104, i + 1, "data")
s.both(560, 96, "ถุง 8 ลูก (ใส่คืนทุกครั้ง)", "8 rows in a bag", "mp-s")
s.both(560, 118, "หยิบแล้วใส่คืนก่อนหยิบใหม่", "put back before each draw", "mp-s")
s.both(700, 152, "ไม่ถูกหยิบ (out-of-bag)", "left out (out-of-bag)", "mp-s")
for r, bag in enumerate(BAGS):
    y = 190 + r * 58
    s.both(30, y + 6, f"ต้นที่ {r + 1}", f"tree {r + 1}", "mp-t")
    for i, n in enumerate(bag):
        ball(180 + i * 46, y, n, "again" if bag.count(n) > 1 else "once")
    s.arrow(536, y, 610, y)
    for i, n in enumerate(sorted(set(range(1, 9)) - set(bag))):
        ball(720 + i * 46, y, n, "out")
s.raw('<circle cx="178" cy="366" r="9" class="rc-ctx"/>')
s.both(194, 371, "สีเข้ม = ถูกหยิบซ้ำ", "shaded = drawn again", "mp-s")
s.both(460, 371, "ข้อมูลใหญ่: แต่ละต้นเห็นแถวไม่ซ้ำราว 63%", "on big data each tree sees ≈ 63% of the rows", "mp-s")
s.save("l13-bootstrap-bags.svg", 386)


# ================================================================ S14 forest and boosting settings
def mini_tree(x, y, depth, w=40, leaf=None):
    """A tiny tree glyph, depth levels, top at (x, y)."""
    pts = [(x, y)]
    for d in range(depth):
        nxt = []
        for px, py in pts:
            dx = w / (2 ** (d + 1))
            for cx in (px - dx, px + dx):
                s.line(px, py, cx, py + 16, "mp-axis")
                nxt.append((cx, py + 16))
        circ_list = pts
        for px, py in circ_list:
            circ(s, px, py, 3.5, "var(--ink-2)")
        pts = nxt
    for i, (px, py) in enumerate(pts):
        circ(s, px, py, 3.5, leaf or CLS[i % 4])


def d_trees(x, y, w, h):
    for i in range(2):
        mini_tree(x + 24 + i * 26, y + 22, 2, 18)
    s.arrow(x + 82, y + 42, x + 104, y + 42)
    for i in range(6):
        mini_tree(x + 120 + i * 20, y + 22, 2, 14)


def d_depth(x, y, w, h):
    mini_tree(x + 50, y + 18, 1, 40)
    s.arrow(x + 96, y + 42, x + 118, y + 42)
    mini_tree(x + 178, y + 10, 4, 96)


def d_features(x, y, w, h):
    for i in range(6):
        pick = i in (1, 4)
        s.fill(x + 24 + i * 32, y + 14, 20, 56, "var(--accent)" if pick else "var(--card-border)", 3)
    s.text(x + w - 12, y + 80, "sqrt(6) ≈ 2", "mp-s", "end")


def d_rate(x, y, w, h):
    s.line(x + 14, y + 66, x + w - 14, y + 66, "mp-axis")
    s.line(x + w - 40, y + 10, x + w - 40, y + 74, "mp-straight")
    for (a, b) in ((20, 150), (150, 230)):
        s.raw(f'<path d="M{x + a:g} {y + 60:g} Q{x + (a + b) / 2:g} {y + 12:g} {x + b:g} {y + 60:g}" class="mp-curve"/>')
    for i in range(6):
        a = 20 + i * 28
        s.raw(f'<path d="M{x + a:g} {y + 66:g} Q{x + a + 14:g} {y + 50:g} {x + a + 28:g} {y + 66:g}" class="mp-curve-b"/>')


s = Svg(W, "The settings of forests and boosting. n_estimators: how many trees (few or many). max_depth: how deep each tree "
           "grows (a stump or a deep tree). max_features: how many random columns each question may use (here 2 of 6, "
           "sqrt). learning_rate: how big each boosting correction is; big steps overshoot the target, small steps creep "
           "up to it.")
term_grid(s, [
    ("n_estimators", d_trees, "จำนวนต้นไม้", "number of trees", "มาก = นิ่งขึ้นแต่ช้าลง", "more = steadier, slower"),
    ("max_depth", d_depth, "ความลึกของแต่ละต้น", "how deep each tree is", "ลึก = จำละเอียด เสี่ยง overfit", "deep = detailed, may overfit"),
    ("max_features", d_features, "คอลัมน์ที่สุ่มให้เลือก", "random columns per question", "น้อย = ต้นไม้ต่างกันมาก", "fewer = more varied trees"),
    ("learning_rate", d_rate, "boosting แก้ทีละเท่าไร", "size of each correction", "เล็ก = ปลอดภัย ใช้ต้นมาก", "small = safer, needs more trees"),
])
s.save("l13-forest-settings.svg", 212)

# ================================================================ S18 scoreboard
SCORES = [("Logistic", 0.846, 0.953), ("Tree", 0.977, 0.953), ("Forest", 0.989, 0.953),
          ("Boosting", 0.976, 0.953), ("KNN", 0.823, 0.858), ("SVM", 0.861, 0.903)]
s = Svg(W, "Six tuned models on the same data, weighted F1. CV (5-fold on the 86 training people) / test (22 new people): "
           "Logistic 0.846 / 0.953, Tree 0.977 / 0.953, Forest 0.989 / 0.953, Boosting 0.976 / 0.953, KNN 0.823 / 0.858, "
           "SVM 0.861 / 0.903. Four models tie on the test set, so the CV column decides; the bars start at 0.80.")
s.bubble("ปรับทุกโมเดลให้ดีที่สุดแล้ว ใครชนะ", "Every model tuned at its best: who wins?")
LO, HI, X1, X2, BW = 0.80, 1.00, 190, 640, 300
s.both(X1, 92, "CV (5-fold บนชุด train 86 คน)", "CV (5-fold, 86 training people)", "mp-c")
s.both(X2, 92, "test (คนใหม่ 22 คน)", "test (22 new people)", "mp-c")
for r, (name, cv, te) in enumerate(SCORES):
    y = 108 + r * 42
    s.text(30, y + 24, name, "mp-t")
    best = name == "Forest"
    s.fill(X1, y + 6, (cv - LO) / (HI - LO) * BW, 26, "var(--accent)" if best else "var(--tag-concept-dot)", 4)
    s.text(X1 + (cv - LO) / (HI - LO) * BW + 8, y + 25, f"{cv:.3f}" + (" ✓" if best else ""), "mp-acc" if best else "mp-c")
    s.fill(X2, y + 6, (te - LO) / (HI - LO) * BW, 26, "var(--tag-example-dot)", 4)
    s.text(X2 + (te - LO) / (HI - LO) * BW + 8, y + 25, f"{te:.3f}", "mp-c")
s.raw(f'<path d="M{X2 + 300} 112 h14 v162 h-14" class="mp-ring"/>')
s.both(X2 + 324, 190, "4 โมเดลเสมอกัน", "4 models tie", "mp-acc")
s.both(X2 + 324, 212, "(ผิด 1 จาก 22)", "(1 wrong of 22)", "mp-s")
s.both(30, 382, "แท่งเริ่มที่ 0.80 · test เสมอกันจึงตัดสินด้วย CV: forest ชนะ แต่ tree, boosting ใกล้มาก",
       "bars start at 0.80 · the test set ties, so CV decides: the forest wins, tree and boosting close behind", "mp-s")
s.save("l13-scoreboard.svg", 396)

# ================================================================ S19 how to choose a model
STEPS = [("🐣", "เริ่มจากง่าย", "Start simple", "logistic หรือ tree", "logistic or a tree", "เป็น baseline", "as a baseline"),
         ("🔍", "รู้จักข้อมูล", "Know your data", "เล็กหรือใหญ่", "small or big?", "เส้นตรงหรือโค้ง", "straight or curved?"),
         ("🎯", "เลือกตามเป้าหมาย", "Choose for the goal", "แม่น · อธิบายได้", "accurate · explainable", "· ทายเร็ว", "· fast"),
         ("⚖️", "เทียบ แล้วปรับ", "Compare, then tune", "CV + F1", "CV + F1", "ปรับก่อนเปลี่ยน", "tune before switching")]
s = Svg(W, "Choosing a model in four steps: start simple (logistic regression or a tree as a baseline), know your data "
           "(small or big, straight or curved), choose for the goal (accurate, explainable or fast), then compare with "
           "cross-validation and F1, and tune a model before switching to another.")
s.bubble("โมเดลมีให้เลือกมาก เริ่มจากตรงไหน", "So many models: where do you start?")
for k, (icon, tth, ten, a_th, a_en, b_th, b_en) in enumerate(STEPS):
    x = 10 + k * 276
    s.box(x, 72, 252, 196, "ml-cell", 14)
    s.badge(x + 26, 98, k + 1)
    s.raw(f'<circle cx="{x + 126}" cy="134" r="30" style="fill:var(--tag-concept-bg)"/>')
    emoji_or_icon(s, icon, x + 126, 134, 54)
    s.both(x + 126, 198, tth, ten, "mp-t", "middle")
    s.both(x + 126, 226, a_th, a_en, "hk-desc", "middle")
    s.both(x + 126, 250, b_th, b_en, "hk-desc", "middle")
    if k < 3:
        s.arrow(x + 256, 170, x + 272, 170)
s.save("l13-choose-model.svg", 278)


# ================================================================ S20 key terms
def d_entropy(x, y, w, h):
    s.stack(x + 14, y + 22, 90, 24, [12, 0, 0, 0], labels=False)
    s.stack(x + 130, y + 22, 90, 24, [3, 3, 3, 3], labels=False)
    s.text(x + 59, y + 70, "0 bits", "mp-s", "middle")
    s.text(x + 175, y + 70, "2 bits", "mp-s", "middle")


def d_gain(x, y, w, h):
    s.stack(x + 12, y + 30, 80, 24, [4, 4, 0, 0], labels=False)
    s.arrow(x + 98, y + 42, x + 124, y + 42)
    s.stack(x + 132, y + 14, 40, 24, [4, 0, 0, 0], labels=False)
    s.stack(x + 132, y + 48, 40, 24, [0, 4, 0, 0], labels=False)
    s.text(x + 184, y + 48, "✓", "ml-ok")


def d_gini(x, y, w, h):
    s.stack(x + 14, y + 16, 120, 24, [5, 3, 2, 2], labels=False)
    s.text(x + 14, y + 70, "1 − Σp²", "mp-n")


def d_tree(x, y, w, h):
    mini_tree(x + w / 2, y + 14, 3, 120)


def d_forest(x, y, w, h):
    for i in range(5):
        mini_tree(x + 22 + i * 30, y + 12, 1, 18)
    s.stack(x + 12, y + 50, 150, 20, [0, 1, 1, 8], labels=False)
    s.text(x + 172, y + 66, "vote", "mp-s")


def d_boost(x, y, w, h):
    for i in range(3):
        mini_tree(x + 30 + i * 74, y + 24, 1, 22)
        if i < 2:
            s.arrow(x + 50 + i * 74, y + 32, x + 84 + i * 74, y + 32)
    s.both(x + w / 2, y + 74, "ต้นใหม่แก้จุดที่ผิด", "each fixes the last", "mp-s", "middle")


def d_knn(x, y, w, h):
    cx, cy = x + w / 2, y + 42
    ring(s, cx, cy, 30, "mp-ring")
    for (dx, dy), k in (((-14, -12), 3), ((16, -8), 3), ((4, 18), 2), ((-50, 10), 1), ((52, 16), 1), ((44, -26), 0)):
        circ(s, cx + dx, cy + dy, 5, CLS[k])
    circ(s, cx, cy, 5, "var(--ink)")


def d_svm(x, y, w, h):
    s.line(x + 60, y + 78, x + 160, y + 6, "mp-straight")
    s.line(x + 90, y + 78, x + 190, y + 6, "mp-straight")
    s.line(x + 75, y + 78, x + 175, y + 6, "mp-curve")
    for dx, dy in ((20, 20), (40, 40), (30, 60), (60, 30)):
        circ(s, x + dx, y + dy, 5, CLS[0])
    for dx, dy in ((190, 50), (210, 30), (200, 70), (175, 72)):
        circ(s, x + dx, y + dy, 5, CLS[3])


s = Svg(W, "Eight key terms with a picture each: entropy (0 bits pure, 2 bits for four even groups), information gain "
           "(entropy before minus after a question), Gini (1 − Σp²), a decision tree (one question at a time), a random "
           "forest (many trees vote), gradient boosting (each tree fixes the last one's mistakes), KNN (the k closest "
           "vote), SVM (the widest street between groups).")
bottom = term_grid(s, [
    ("Entropy", d_entropy, "ความแปลกใจเฉลี่ย", "average surprise", "0 = บริสุทธิ์ สูงสุด 2 bits", "0 = pure, 4 even = 2 bits"),
    ("Information gain", d_gain, "entropy ก่อน − หลังถาม", "entropy before − after", "เลือกคำถามที่ลดมากสุด", "pick the biggest drop"),
    ("Gini", d_gini, "โอกาสหยิบ 2 คนต่างกลุ่ม", "chance two picks differ", "คำนวณเร็วกว่า entropy", "quicker than entropy"),
    ("Decision tree", d_tree, "ถามทีละคำถาม", "one question at a time", "อ่านกฎได้", "rules you can read"),
    ("Random forest", d_forest, "หลายต้นจาก bootstrap", "many bootstrap trees", "แล้วโหวต", "then vote"),
    ("Gradient boosting", d_boost, "ต้นใหม่แก้ที่ต้นก่อนผิด", "each tree fixes the last", "ทีละนิด", "one's mistakes, bit by bit"),
    ("KNN", d_knn, "ถาม k คนที่ใกล้สุด", "ask the k closest", "แล้วโหวต", "people, then vote"),
    ("SVM", d_svm, "ถนนที่กว้างที่สุด", "the widest street", "ระหว่างกลุ่ม", "between the groups"),
])
s.save("l13-key-terms.svg", bottom + 10)
