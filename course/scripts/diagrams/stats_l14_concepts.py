"""Concept pictures for stats-dh lesson 14 (Monte Carlo simulation, bootstrapping and permutation
tests), in the style of nlp l13-why-chunk.svg. ไทย/EN labels follow the language switch.

    course/.venv/bin/python scripts/diagrams/stats_l14_concepts.py courses/stats-dh/images

Every number is a real run in course/.venv with the same seeds as the lesson's code cells:
  Dice (numpy default_rng(42), 5 dice per run): runs 1–4 roll 0, 1, 1, 1 sixes, run 10 rolls 6 3 6 5 5 (2 sixes).
      Estimates of P(at least 2 sixes) with 10, 100, 1,000, 10,000, 100,000 runs: 0.100, 0.180, 0.209, 0.194,
      0.196; the exact answer is 0.196.
  Rumour shared A→B→C→D→E (friends' chat → class group → faculty group → uni page → viral) with p 0.3, 0.2, 0.5, 0.1 (default_rng(42), 100,000 runs): reached B 30.1%, C 5.9%,
      D 3.0%, E 0.29% (exact 30%, 6%, 3%, 0.3%).
  Food-delivery waits (made-up example data), minutes, 24 orders: 1–12 on dry days, 13–24 on rainy days; median 25.
      Bootstrap (default_rng(42), 10,000 resamples): first three medians 28, 27, 25; 95% CI 23 to 28 minutes.
      Why-bootstrap picture: the left rows are made up (default_rng(7)) to show the impossible 're-order' dream.
      Dry mean 25.3, rainy mean 31.7, difference +6.3. Permutation (default_rng(42), 10,000 shuffles): first three
      differences −2.7, +8.0, +0.2; 1,751 of 10,000 at least 6.3 away from 0, p = 0.18.
"""

import numpy as np

from stats_svg import Svg, W, math, width  # noqa: F401

# minutes from order to door; orders 1–12 on dry days, 13–24 on rainy days (made-up example data)
WAIT = np.array([18, 22, 25, 21, 27, 24, 31, 19, 23, 26, 48, 20,
                 24, 28, 22, 35, 25, 55, 30, 21, 60, 26, 25, 29])
VOL = ["var(--tag-concept-dot)", "var(--tag-example-dot)"]  # dry days, rainy days



def die(s, x, y, v, lit):
    """A die face 40 × 40 with v pips; lit = a six (the thing we count)."""
    s.box(x, y, 40, 40, "rc-res" if lit else "ml-cell", 8)
    PIPS = {1: [(20, 20)], 2: [(11, 11), (29, 29)], 3: [(11, 11), (20, 20), (29, 29)], 4: [(11, 11), (29, 11), (11, 29), (29, 29)],
            5: [(11, 11), (29, 11), (20, 20), (11, 29), (29, 29)], 6: [(11, 10), (29, 10), (11, 20), (29, 20), (11, 30), (29, 30)]}
    for (px, py) in PIPS[v]:
        s.raw(f'<circle cx="{x + px}" cy="{y + py}" r="3.6" class="pl-keep"/>')


# ================================================================ L13 Monte Carlo on dice
RUNS = [(1, [1, 5, 4, 3, 3]), (2, [6, 1, 5, 2, 1]), (3, [4, 6, 5, 5, 5]), (10, [6, 3, 6, 5, 5])]
EST = [(10, 0.100), (100, 0.180), (1000, 0.209), (10000, 0.194), (100000, 0.196)]
s = Svg(W, "Monte Carlo on dice: what is the chance of at least 2 sixes when rolling 5 dice? Panel 1: each run "
           "rolls 5 random dice and checks for at least 2 sixes (runs 1 to 3: no; run 10: 6 3 6 5 5, yes). "
           "Panel 2: the share of yes runs, for 10, 100, 1,000, 10,000 and 100,000 runs: 0.100, 0.180, 0.209, "
           "0.194, 0.196, closing in on the exact answer 0.196.")
s.bubble("ทอยลูกเต๋า 5 ลูก โอกาสได้เลข 6 อย่างน้อย 2 ลูกเป็นเท่าไร", "Roll 5 dice: what is the chance of at least two sixes?")
s.panel(20, 70, 520, 430, "nt-band-a", "1 รอบ = ทอยสุ่ม 5 ลูก แล้วนับ 6", "One run = roll 5 random dice, count the sixes", 1)
for k, (run, vals) in enumerate(RUNS):
    y = 130 + k * 82
    s.both(40, y + 27, f"รอบ {run}", f"run {run}", "pl-text")
    for j, v in enumerate(vals):
        die(s, 130 + j * 50, y, v, v == 6)
    sixes = vals.count(6)
    ok = sixes >= 2
    s.both(400, y + 27, f"6 × {sixes} {'✓' if ok else '✗'}", f"6 × {sixes} {'✓' if ok else '✗'}", "ml-ok" if ok else "ml-neg")
    if k == 2:
        s.text(280, y + 66, "⋮", "pl-note", "middle")
s.both(40, 482, "สุ่ม → ตรวจ → จด ✓ หรือ ✗ แล้วทำซ้ำ", "random → check → note ✓ or ✗, then repeat", "pl-label")
s.panel(560, 70, 600, 430, "nt-band-a", "ทำซ้ำหลายรอบ แล้วนับสัดส่วน ✓", "Repeat many times, take the share of ✓", 2)
X0, X1, YB, YT = 620, 1120, 380, 170     # 0.08 at YB, 0.24 at YT
ys = lambda p: YB - (p - 0.08) / (0.24 - 0.08) * (YB - YT)
s.line(X0, YB + 20, X1, YB + 20, "dg-rule-strong")
s.line(X0, ys(0.1962), X1, ys(0.1962), "ml-cut-guess")
s.both(X1, ys(0.1962) + 26, "คำตอบจริง 0.196", "exact 0.196", "pl-note", "end")
for k, (n, p) in enumerate(EST):
    x = X0 + 40 + k * 105
    s.line(x, YB + 20, x, ys(p), "dg-rule")
    s.raw(f'<circle cx="{x}" cy="{ys(p):.1f}" r="9" class="pl-dot"/>')
    s.text(x, ys(p) - 16 if p < 0.2 else ys(p) + 30, f"{p:.3f}", "pl-label", "middle")
    s.text(x, YB + 44, f"{n:,}", "pl-note", "middle")
s.both(X0, YB + 66, "จำนวนรอบ", "number of runs", "pl-note")
s.both(580, 482, "✓ ยิ่งทำซ้ำมาก ค่าประมาณยิ่งเข้าใกล้คำตอบจริง", "✓ the more runs, the closer the estimate", "ml-ok")
s.save("l14-dice.svg", 520)

# ================================================================ dice: the exact formula next to the simulation
from math import comb
EX = [comb(5, k) * (1 / 6) ** k * (5 / 6) ** (5 - k) for k in range(6)]
_rolls = np.random.default_rng(42).integers(1, 7, size=(100_000, 5))
_six = (_rolls == 6).sum(axis=1)
SIM = [(_six == k).mean() for k in range(6)]
s = Svg(W, "The formula and the simulation side by side. Left: the exact way. The chance of exactly k sixes with 5 dice "
           "is C(5, k) × (1/6)^k × (5/6)^(5−k): ways to choose which dice show a six, times the chance those are sixes, "
           "times the chance the rest are not. For k = 2: 10 × 0.0278 × 0.5787 = 0.1608. At least 2 sixes = 0.1608 + "
           "0.0322 + 0.0032 + 0.0001 = 0.1962, or 1 − 0.4019 − 0.4019. Right: for every k, the formula's chance and the "
           "share of 100,000 simulated runs (0: 0.4019 vs 0.4025, 1: 0.4019 vs 0.4007, 2: 0.1608 vs 0.1621, 3: 0.0322 vs "
           "0.0316, 4: 0.0032 vs 0.0030, 5: 0.0001 vs 0.0002). Formula 0.1962, simulation 0.1968.")
s.bubble("สูตรกับการจำลองได้คำตอบเดียวกันไหม", "Do the formula and the simulation agree?")
s.panel(20, 70, 560, 330, "ml-cell", "วิธีสูตร: คิดทีละกรณี", "The formula: case by case", 1)
s.both(44, 140, "P(ได้ 6 พอดี k ลูก) =", "P(exactly k sixes) =", "pl-text")
s.text(44, 176, "C(5, k) × (1/6)ᵏ × (5/6)⁵⁻ᵏ", "mp-q")
s.both(44, 206, "เลือกลูกที่ได้ 6 · ลูกพวกนั้นได้ 6 · ลูกที่เหลือไม่ได้ 6", "which dice · those are sixes · the rest are not", "pl-note")
s.both(44, 248, "เช่น k = 2: 10 วิธี × 0.0278 × 0.5787 = 0.1608", "e.g. k = 2: 10 ways × 0.0278 × 0.5787 = 0.1608", "pl-text")
s.both(44, 290, "อย่างน้อย 2 ลูก = รวม k = 2, 3, 4, 5", "at least 2 = add k = 2, 3, 4, 5", "pl-text")
s.text(44, 320, "0.1608 + 0.0322 + 0.0032 + 0.0001 = 0.1962", "pl-label")
s.both(44, 356, "ทางลัด: 1 − P(0) − P(1) = 1 − 0.4019 − 0.4019", "shortcut: 1 − P(0) − P(1) = 1 − 0.4019 − 0.4019", "pl-note")
s.both(44, 382, "ยุ่ง: ต้องรู้สูตรและคิดหลายกรณี", "fiddly: you must know the formula", "pl-note")
s.panel(600, 70, 560, 330, "ml-cell", "เทียบทีละกรณี: สูตร กับ จำลอง 100,000 รอบ", "Case by case: formula vs 100,000 runs", 2)
GX0, GW, BASE, TOPH = 690, 76, 262, 120
s.box(GX0 + 2 * GW - 6, 112, 4 * GW + 4, 286, "nt-band-b", 10)
s.both(GX0 + 4 * GW - 4, 132, "นับรวม = อย่างน้อย 2 ลูก", "added up = at least 2", "pl-note", "middle")
for k in range(6):
    x = GX0 + k * GW
    for j, (v, col) in enumerate(((EX[k], "var(--tag-concept-dot)"), (SIM[k], "var(--accent)"))):
        hh = max(v / 0.41 * TOPH, 1.5)
        s.fill(x + 8 + j * 26, BASE - hh, 24, hh, col, 3)
    s.text(x + 33, BASE + 22, str(k), "pl-label", "middle")
    s.text(x + 33, BASE + 54, f"{EX[k]:.4f}", "mp-s", "middle")
    s.text(x + 33, BASE + 80, f"{SIM[k]:.4f}", "mp-s", "middle")
s.line(GX0, BASE, GX0 + 6 * GW, BASE, "mp-axis")
s.both(GX0 - 8, BASE + 22, "ได้ 6", "sixes", "pl-note", "end")
s.fill(616, BASE + 42, 14, 14, "var(--tag-concept-dot)", 3)
s.both(GX0 - 8, BASE + 54, "สูตร", "formula", "mp-s", "end")
s.fill(616, BASE + 68, 14, 14, "var(--accent)", 3)
s.both(GX0 - 8, BASE + 80, "จำลอง", "simulated", "mp-s", "end")
s.box(20, 414, 1140, 56, "nt-band-a", 12)
s.both(590, 449, f"อย่างน้อย 2 ลูก: สูตร {sum(EX[2:]):.4f} · จำลอง {(_six >= 2).mean():.4f} · ต่างกันแค่ {(_six >= 2).mean() - sum(EX[2:]):.4f} ✓ จึงเชื่อการจำลองได้ในปัญหาที่ไม่มีสูตร",
       f"At least 2 sixes: formula {sum(EX[2:]):.4f} · simulation {(_six >= 2).mean():.4f} · off by only {(_six >= 2).mean() - sum(EX[2:]):.4f} ✓ so we can trust simulation where there is no formula",
       "pl-label", "middle")
s.save("l14-dice-formula.svg", 480)

# ================================================================ a rumour shared along a chain of groups
NODES = ["A", "B", "C", "D", "E"]
WHERE = [("แชทแก๊งเพื่อน", "friends' chat"), ("กรุ๊ปห้อง", "class group"), ("กรุ๊ปคณะ", "faculty group"),
         ("เพจมหาลัย", "uni page"), ("ไวรัลทั้งประเทศ", "viral nationwide")]
P = [0.3, 0.2, 0.5, 0.1]
REACH = ["100%", "30.1%", "5.9%", "3.0%", "0.29%"]
EXAMPLES = [(1, 0), (2, 1), (22, 2), (182, 4)]   # run number, last group reached (index): from default_rng(42)
s = Svg(W, "A rumour shared along a chain of 5 groups: A a friends' group chat, B the class group, C the faculty group, "
           "D the university page, E viral nationwide. At each step someone shares it on with probability 0.3, 0.2, "
           "0.5, 0.1. Example runs: run 1 stops at A, run 2 reaches B, run 22 reaches C, run 182 is the first to go "
           "viral. Out of 100,000 runs the rumour reached B in 30.1%, C 5.9%, D 3.0% and E 0.29%.")
s.bubble("ข่าวลือจากแชทแก๊งเพื่อน (A) จะไวรัลทั้งประเทศ (E) บ่อยแค่ไหน", "How often does a rumour from a friends' chat (A) go viral (E)?")
for k, name in enumerate(NODES):
    x = 120 + k * 235
    s.raw(f'<circle cx="{x}" cy="122" r="32" class="ml-cell-b"/>')
    s.text(x, 131, name, "pl-label", "middle")
    s.both(x, 178, WHERE[k][0], WHERE[k][1], "mp-s", "middle")
    s.text(x, 208, REACH[k], "pl-label" if k else "pl-note", "middle")
    if k < 4:
        s.arrow(x + 38, 122, x + 197, 122)
        s.text(x + 117, 110, f"p = {P[k]}", "pl-label", "middle")
s.both(117 + 120, 146, "โอกาสมีคนแชร์ต่อ", "chance it's shared on", "pl-note", "middle")
s.both(20, 208, "ไปถึง:", "reached:", "pl-note")
s.box(20, 232, 1140, 260, "nt-band-a", 14)
s.both(40, 266, "ตัวอย่างรอบจำลอง: สุ่มเลข 0–1 ทุกลูกศร ถ้าน้อยกว่า p ก็มีคนแชร์ต่อ", "Example runs: a random number 0–1 at every arrow; below p, someone shares it on", "pl-label")
for k, (run, last) in enumerate(EXAMPLES):
    y = 310 + k * 44
    s.both(40, y + 6, f"รอบ {run}", f"run {run}", "pl-text")
    for j in range(5):
        x = 200 + j * 120
        got = j <= last
        s.raw(f'<circle cx="{x}" cy="{y}" r="14" style="fill:{"var(--accent)" if got else "var(--card)"};stroke:var(--card-border)"/>')
        if j < 4:
            s.line(x + 18, y, x + 102, y, "pl-line" if j < last else "dg-rule")
    s.both(820, y + 6, f"ถึง {NODES[last]} ({WHERE[last][0]})", f"reached {NODES[last]} ({WHERE[last][1]})", "pl-text")
s.both(40, 478, "ทำ 100,000 รอบ แล้วนับว่ากี่รอบไปถึงแต่ละกลุ่ม", "Do 100,000 runs, then count how many reached each group", "pl-note")
s.both(20, 526, "✓ ไวรัลถึง E แค่ 0.29% (คิดมือ: 0.3 × 0.2 × 0.5 × 0.1 = 0.003)  ·  โซเชียลจริงแชร์ได้หลายทาง จึงคิดมือไม่ได้ ต้องจำลอง",
       "✓ only 0.29% go viral (by hand: 0.3 × 0.2 × 0.5 × 0.1 = 0.003)  ·  real social media branches, so simulation is the only way", "ml-ok")
s.save("l14-news.svg", 544)

# ================================================================ why bootstrap: the dream vs what we can do
def mini_row(x, y, vals, cls="ml-bar"):
    """24 tiny bars, one per order (height = minutes, 60 min = 30 px)."""
    for j, v in enumerate(vals):
        h = v / 60 * 30
        s.box(x + j * 12, y + 30 - h, 9, h, cls, 2)


rng = np.random.default_rng(7)
dream = [np.clip(rng.choice(WAIT, 24) + rng.integers(-3, 4, 24), 15, 60) for _ in range(3)]
rng = np.random.default_rng(42)
boot = rng.choice(np.arange(1, 25), size=(10000, 24), replace=True)
bmed = np.median(WAIT[boot - 1], axis=1)
blo, bhi = np.percentile(bmed, [2.5, 97.5])
s = Svg(W, f"Why bootstrap? We want to know how much the median wait (25 minutes from 24 orders) could change. Left, "
           f"the dream: order 24 meals again, hundreds of times, and look at the medians (made-up rows, medians "
           f"{np.median(dream[0]):g}, {np.median(dream[1]):g}, {np.median(dream[2]):g}); that is 24,000 orders and months of "
           f"waiting, and an old novel or archive cannot be collected again at all. Right, bootstrap: let the 24 orders we "
           f"have stand in for the world and redraw from them with replacement (medians {bmed[0]:g}, {bmed[1]:g}, "
           f"{bmed[2]:g}); 10,000 rounds take under a second and give the range {blo:g} to {bhi:g} minutes.")
s.bubble("median 25 นาทีจาก 24 ออเดอร์ เชื่อได้แค่ไหน", "A median of 25 min from 24 orders: how sure can we be?")
s.panel(20, 70, 560, 330, "ml-cell", "✗ ในฝัน: สั่งใหม่จริง ๆ อีกหลายร้อยรอบ", "✗ The dream: order 24 meals again, many times", 1)
s.both(44, 132, "แต่ละแถว = 24 ออเดอร์ใหม่ (แท่ง = นาทีที่รอ)", "Each row = 24 new orders (bar = minutes waited)", "pl-note")
for r in range(3):
    y = 146 + r * 44
    s.both(44, y + 24, f"รอบ {r + 1}", f"round {r + 1}", "pl-text")
    mini_row(120, y, dream[r])
    s.text(556, y + 24, f"median {np.median(dream[r]):g}", "pl-label", "end")
s.both(120, 300, "⋮ อีกหลายร้อยรอบ", "⋮ hundreds more rounds", "pl-note")
s.both(44, 344, "✗ ออเดอร์เป็นหมื่น รอหลายเดือน: ทำจริงไม่ได้", "✗ tens of thousands of orders, months: not doable", "ml-neg")
s.both(44, 376, "งาน DH ยิ่งยาก: นิยายหรือจดหมายเก่ามีชุดเดียว เก็บใหม่ไม่ได้", "In DH it's worse: an old novel or archive exists only once", "pl-note")
s.panel(600, 70, 560, 330, "nt-band-a", "✓ bootstrap: ใช้ 24 ออเดอร์ที่มีแทนโลก", "✓ Bootstrap: the 24 orders stand in for the world", 2)
s.both(624, 132, "ข้อมูลจริงชุดเดียวที่เรามี", "The one real dataset we have", "pl-note")
mini_row(700, 146, WAIT, "ml-bar-top")
s.both(624, 170, "จริง", "real", "pl-label")
s.text(1136, 170, "median 25", "pl-label", "end")
s.arrow(844, 182, 844, 206)
s.both(858, 199, "สุ่มแบบใส่คืน", "draw with replacement", "pl-note")
for r in range(3):
    y = 210 + r * 40
    s.both(624, y + 24, f"ชุด {r + 1}", f"set {r + 1}", "pl-text")
    mini_row(700, y, WAIT[np.sort(boot[r]) - 1])
    s.text(1136, y + 24, f"median {bmed[r]:g}", "pl-label", "end")
s.both(700, 344, "⋮ 10,000 ชุด คอมพิวเตอร์ทำไม่ถึง 1 วินาที", "⋮ 10,000 sets in under a second", "pl-note")
s.both(624, 380, f"✓ median น่าจะอยู่ช่วง {blo:g} ถึง {bhi:g} นาที", f"✓ the median likely lies between {blo:g} and {bhi:g} min", "ml-ok")
s.box(20, 414, 1140, 56, "nt-band-b", 12)
s.both(590, 449, "ใช้เมื่อ: มีข้อมูลชุดเดียว · ค่าสถิติไม่มีสูตร (median, percentile) · ข้อมูลน้อยหรือเบ้",
       "Use it when: you have one dataset · the statistic has no formula (median, percentile) · data is small or skewed", "pl-label", "middle")
s.save("l14-why-bootstrap.svg", 484)

# ================================================================ bootstrap of the median wait
rng = np.random.default_rng(42)
idx = rng.choice(np.arange(1, 25), size=(10000, 24), replace=True)
meds = np.median(WAIT[idx - 1], axis=1)
lo, hi = np.percentile(meds, [2.5, 97.5])
s = Svg(W, f"Bootstrapping the median food-delivery wait. Top: the 24 real orders (median 25 minutes; order 21 took "
           f"60). Middle: three bootstrap samples of 24 orders drawn with replacement (repeats shaded), medians "
           f"{meds[0]:g}, {meds[1]:g} and {meds[2]:g}. Bottom: the medians of 10,000 samples; the middle 95% runs from "
           f"{lo:g} to {hi:g} minutes: the 95% confidence interval.")
s.bubble("median เวลารอของ 24 ออเดอร์คือ 25 นาที ค่าจริงน่าจะอยู่ช่วงไหน", "The median wait over 24 orders is 25 min: where could the true value lie?")
s.both(20, 96, "ข้อมูลจริง 24 ออเดอร์ (นาที)", "The real 24 orders (minutes)", "pl-label")
for k, v in enumerate(WAIT):
    x = 300 + k * 35
    h = v / 60 * 70
    s.box(x, 150 - h, 26, h, "ml-bar-top" if k == 20 else "ml-bar", 3)
    s.text(x + 13, 168, str(k + 1), "pl-note", "middle")
mid = 150 - 25 / 60 * 70
s.line(292, mid, 1140, mid, "ml-cut-guess")
s.both(20, 130, "median 25 · ออเดอร์ 21 รอ 60", "median 25 · order 21 took 60", "pl-note")
s.box(20, 186, 1140, 196, "nt-band-a", 14)
s.both(40, 216, "สุ่มออเดอร์แบบใส่คืน 24 ครั้ง (เลขคือออเดอร์ที่ถูกสุ่ม · สีเข้ม = ซ้ำ) แล้วหา median",
       "Draw 24 orders with replacement (numbers = orders drawn · shaded = repeated), take the median", "pl-label")
for r in range(3):
    y = 236 + r * 46
    bag = sorted(idx[r])
    for j, c in enumerate(bag):
        x = 40 + j * 38
        rep = list(bag).count(c) > 1
        s.box(x, y, 32, 32, "rc-ctx" if rep else "ml-cell", 6)
        s.text(x + 16, y + 22, str(c), "pl-note" if not rep else "pl-label", "middle")
    s.text(1140, y + 22, f"median {meds[r]:g}", "pl-label", "end")
# histogram of the 10,000 medians
counts, edges = np.histogram(meds, bins=np.arange(20, 32.01, 0.5))
HX0, HY0, HW = 120, 600, 940
xs = lambda v: HX0 + (v - 20) / 12 * HW
for c, e in zip(counts, edges):
    hh = c / counts.max() * 130
    inside = lo <= e + 0.25 <= hi
    s.box(xs(e) + 1, HY0 - hh, HW / 24 - 2, hh, "ml-bar-top" if inside else "ml-bar", 2)
s.line(HX0, HY0, HX0 + HW, HY0, "dg-rule-strong")
for v in (20, 22, 24, 26, 28, 30, 32):
    s.text(xs(v), HY0 + 22, f"{v}", "pl-note", "middle")
for v in (lo, hi):
    s.line(xs(v), HY0 - 150, xs(v), HY0, "ml-cut")
    s.text(xs(v), HY0 - 158, f"{v:g}", "pl-label", "middle")
s.both(20, 410, "median ของ 10,000 ชุดที่สุ่มใหม่ (นาที)", "The medians of 10,000 resamples (minutes)", "pl-label")
s.both(20, 664, f"✓ 95% CI ของ median = {lo:g} ถึง {hi:g} นาที (ตัด 2.5% ซ้ายและขวาออก) · ไม่ต้องใช้สูตรใด ๆ",
       f"✓ 95% CI of the median = {lo:g} to {hi:g} minutes (cut 2.5% off each end) · no formula needed", "ml-ok")
s.save("l14-bootstrap.svg", 682)

# ================================================================ permutation test, dry vs rainy days
rng = np.random.default_rng(42)
perms = [rng.permutation(np.arange(1, 25)) for _ in range(10000)]
diffs = np.array([WAIT[p[12:] - 1].mean() - WAIT[p[:12] - 1].mean() for p in perms])
obs = WAIT[12:].mean() - WAIT[:12].mean()
extreme = int((np.abs(diffs) >= obs - 1e-9).sum())
s = Svg(W, f"A permutation test: does rain really slow delivery down? The real split (orders 1–12 on dry days, 13–24 "
           f"on rainy days) gives mean waits {WAIT[:12].mean():.1f} and {WAIT[12:].mean():.1f} minutes, a difference of "
           f"+{obs:.1f}. If the dry/rainy labels meant nothing, any 12 orders could be the 'dry' ones: three shuffles give "
           f"{diffs[0]:+.1f}, {diffs[1]:+.1f} and {diffs[2]:+.1f}. Over 10,000 shuffles, {extreme:,} differences are at "
           f"least {obs:.1f} away from 0, so p = {extreme / 10000:.2f}: a difference this size can easily be chance.")
s.bubble("วันฝนตกส่งช้ากว่าจริง หรือแค่บังเอิญ", "Is delivery really slower on rainy days, or is it chance?")


def split_row(y, dry, label_th, label_en, diff, real=False):
    s.both(40, y + 22, label_th, label_en, "pl-label" if real else "pl-text")
    v1 = sorted(dry)
    v2 = sorted(set(range(1, 25)) - set(v1))
    for j, c in enumerate(v1 + v2):
        x = 180 + j * 34 + (14 if j >= 12 else 0)
        orig = 0 if c <= 12 else 1
        s.box(x, y, 30, 32, "ml-cell", 6)
        s.fill(x + 3, y + 26, 24, 4, VOL[orig], 2)
        s.text(x + 15, y + 21, str(c), "pl-note", "middle")
    s.text(1150, y + 22, f"{diff:+.1f}".replace("-", "−"), "pl-label" if real else "pl-text", "end")


s.both(180, 96, "“วันฝนไม่ตก” (12 ออเดอร์)", "“dry days” (12 orders)", "pl-note")
s.both(602, 96, "“วันฝนตก” (12 ออเดอร์)", "“rainy days” (12 orders)", "pl-note")
s.both(1150, 96, "ฝน − ไม่ฝน", "rain − dry", "pl-note", "end")
split_row(110, list(range(1, 13)), "จริง", "real", obs, True)
s.box(20, 158, 1140, 170, "nt-band-a", 14)
for k in range(3):
    split_row(172 + k * 50, list(perms[k][:12]), f"สลับครั้ง {k + 1}", f"shuffle {k + 1}", diffs[k])
s.both(40, 322, "แถบสีใต้เลขบอกว่าออเดอร์นั้นมาจากวันแบบไหนจริง: สลับแล้วปนกัน",
       "The coloured strip shows each order's real day type: after shuffling they mix", "pl-note")
counts, edges = np.histogram(diffs, bins=np.arange(-12, 12.01, 1))
HX0, HY0, HW = 120, 590, 940
xs = lambda v: HX0 + (v + 12) / 24 * HW
for c, e in zip(counts, edges):
    hh = c / counts.max() * 140
    far = abs(e + 0.5) >= obs
    s.box(xs(e) + 1, HY0 - hh, HW / 24 - 2, hh, "ml-bar-top" if far else "ml-bar", 2)
s.line(HX0, HY0, HX0 + HW, HY0, "dg-rule-strong")
for v in (-10, -5, 0, 5, 10):
    s.text(xs(v), HY0 + 22, f"{v:+}".replace("+0", "0").replace("-", "−"), "pl-note", "middle")
for v in (obs, -obs):
    s.line(xs(v), HY0 - 160, xs(v), HY0, "ml-cut")
s.text(xs(obs), HY0 - 168, f"+{obs:.1f}", "pl-label", "middle")
s.text(xs(-obs), HY0 - 168, f"−{obs:.1f}", "pl-label", "middle")
s.both(20, 372, f"ผลต่างจากการสลับ 10,000 ครั้ง (นาที · สีเข้ม = ห่างจาก 0 อย่างน้อย {obs:.1f})",
       f"Differences from 10,000 shuffles (minutes · dark = at least {obs:.1f} from 0)", "pl-label")
s.both(20, 646, f"✗ {extreme:,} จาก 10,000 ครั้งห่างจาก 0 อย่างน้อยเท่าของจริง → p = {extreme / 10000:.2f} > 0.05: ยังสรุปไม่ได้ว่าฝนทำให้ช้า",
       f"✗ {extreme:,} of 10,000 shuffles are at least as far from 0 → p = {extreme / 10000:.2f} > 0.05: no clear evidence that rain slows it", "ml-neg")
s.save("l14-permutation.svg", 664)

# ================================================================ L13 three kinds of alternative world
s = Svg(W, "Three kinds of alternative world. Monte Carlo builds worlds from probabilities you set and answers "
           "'how likely is this outcome?' (a rumour goes viral in 0.29% of runs). Bootstrap builds worlds by resampling your "
           "data with replacement and answers 'how sure am I of this statistic?' (median wait 95% CI 23 to 28 minutes). "
           "Permutation builds worlds where the group labels mean nothing and answers 'could this difference be "
           "chance?' (rain vs dry, p = 0.18).")
s.bubble("ถ้าคิดด้วยสูตรไม่ได้ ก็สร้างโลกคู่ขนานหลายพันโลก", "If you can't solve it with a formula, build thousands of other worlds")
WORLDS = [
    ("Monte Carlo", "สุ่มจาก: ความน่าจะเป็นที่เรากำหนด", "From: probabilities you set", "ถาม: ผลนี้เกิดบ่อยแค่ไหน", "Asks: how likely is this outcome?",
     "ได้: ความน่าจะเป็น หรือการกระจายของผล", "Gives: a probability", "ข่าวลือไวรัล: 0.29%", "rumour goes viral: 0.29%"),
    ("Bootstrap", "สุ่มจาก: ข้อมูลของเราเอง แบบใส่คืน", "From: your data, put back", "ถาม: ค่าสถิตินี้แม่นแค่ไหน", "Asks: how sure am I of this statistic?",
     "ได้: ช่วงความเชื่อมั่น (CI)", "Gives: a confidence interval", "median: 23 ถึง 28 นาที", "median: 23 to 28 min"),
    ("Permutation", "สุ่มจาก: การสลับป้ายกลุ่ม", "From: shuffled group labels", "ถาม: ความต่างนี้บังเอิญได้ไหม", "Asks: could this difference be chance?",
     "ได้: p-value", "Gives: a p-value", "ฝน − ไม่ฝน: p = 0.18", "rain − dry: p = 0.18"),
]
PW = 364
for i, (name, rth, ren, qth, qen, gth, gen, exth, exen) in enumerate(WORLDS):
    x0 = 20 + i * (PW + 24)
    s.box(x0, 70, PW, 330, "nt-band-a", 14)
    s.badge(x0 + 32, 96, i + 1)
    s.text(x0 + 54, 102, name, "pl-label")
    s.both(x0 + 20, 150, rth, ren, "pl-text")
    s.both(x0 + 20, 196, qth, qen, "pl-text")
    s.both(x0 + 20, 242, gth, gen, "pl-text")
    s.line(x0 + 20, 272, x0 + PW - 20, 272, "dg-rule")
    s.both(x0 + 20, 310, "ตัวอย่างในบทนี้", "In this lesson", "pl-note")
    s.both(x0 + 20, 346, exth, exen, "ml-ok")
s.both(20, 444, "ทั้งสามวิธี: (1) สร้างโลก (2) คำนวณค่าสถิติในแต่ละโลก (3) ทำซ้ำหลายพันครั้ง (4) ดูการกระจาย",
       "All three: (1) build a world (2) compute the statistic in it (3) repeat thousands of times (4) look at the spread", "pl-label")
s.save("l14-three-worlds.svg", 462)
