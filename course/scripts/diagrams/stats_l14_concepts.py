"""Concept pictures for stats-dh lesson 14 (Monte Carlo simulation, bootstrapping and permutation
tests), in the style of nlp l13-why-chunk.svg. ไทย/EN labels follow the language switch.

    course/.venv/bin/python scripts/diagrams/stats_l14_concepts.py courses/stats-dh/images

Every number is a real run in course/.venv with the same seeds as the lesson's code cells:
  Dice (numpy default_rng(42), 5 dice per run): runs 1–4 roll 0, 1, 1, 1 sixes, run 10 rolls 6 3 6 5 5 (2 sixes).
      Estimates of P(at least 2 sixes) with 10, 100, 1,000, 10,000, 100,000 runs: 0.100, 0.180, 0.209, 0.194,
      0.196; the exact answer is 0.196.
  News spread A→B→C→D→E with p 0.3, 0.2, 0.5, 0.1 (default_rng(42), 100,000 runs): reached B 30.1%, C 5.9%,
      D 3.0%, E 0.29% (exact 30%, 6%, 3%, 0.3%).
  Persuasion (Jane Austen, Project Gutenberg #105), words per chapter, 24 chapters: median 3,189.5. Bootstrap
      (default_rng(42), 10,000 resamples): first three medians 2,870.5, 2,958, 3,358.5; 95% CI 2,775 to 3,518.
      Volume I (ch. 1–12) mean 3,225, volume II (ch. 13–24) mean 3,783, difference +557. Permutation
      (default_rng(42), 10,000 shuffles): first three differences +1,039, −287, −49; 3,594 of 10,000 at least
      557 away from 0, p = 0.36.
"""

import numpy as np

from stats_svg import Svg, W, math, width  # noqa: F401

CH = np.array([2625, 1993, 2854, 1817, 3350, 3844, 3467, 3367, 2887, 3881, 3029, 5589,
               2775, 2550, 2837, 2420, 3518, 4159, 2410, 3518, 7036, 5942, 6625, 1601])
VOL = ["var(--tag-concept-dot)", "var(--tag-example-dot)"]  # volume I, volume II



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

# ================================================================ L13 news spread along a chain
NODES = ["A", "B", "C", "D", "E"]
P = [0.3, 0.2, 0.5, 0.1]
REACH = ["100%", "30.1%", "5.9%", "3.0%", "0.29%"]
EXAMPLES = [(1, 0), (2, 1), (22, 2), (182, 4)]   # run number, last community reached (index): from default_rng(42)
s = Svg(W, "News spreading along a chain of 5 communities, A to E. A has the news; it passes A→B with "
           "probability 0.3, B→C 0.2, C→D 0.5, D→E 0.1. Example runs: run 1 stops at A, run 2 reaches B, run 22 "
           "reaches C, run 182 is the first to reach E. Out of 100,000 runs the news reached B in 30.1%, C 5.9%, D 3.0% and E 0.29%.")
s.bubble("ข่าวจากชุมชน A จะไปถึงชุมชน E บ่อยแค่ไหน", "How often does news from community A reach community E?")
for k, name in enumerate(NODES):
    x = 120 + k * 235
    s.raw(f'<circle cx="{x}" cy="130" r="34" class="ml-cell-b"/>')
    s.text(x, 140, name, "pl-label", "middle")
    s.text(x, 196, REACH[k], "pl-label" if k else "pl-note", "middle")
    if k < 4:
        s.arrow(x + 40, 130, x + 195, 130)
        s.text(x + 117, 118, f"p = {P[k]}", "pl-label", "middle")
s.both(20, 196, "ไปถึง:", "reached:", "pl-note")
s.box(20, 222, 1140, 260, "nt-band-a", 14)
s.both(40, 256, "ตัวอย่างรอบจำลอง: สุ่มเลข 0–1 ทุกลูกศร ถ้าน้อยกว่า p ข่าวก็ผ่าน", "Example runs: a random number 0–1 at every arrow; below p, the news passes", "pl-label")
for k, (run, last) in enumerate(EXAMPLES):
    y = 300 + k * 44
    s.both(40, y + 6, f"รอบ {run}", f"run {run}", "pl-text")
    for j in range(5):
        x = 200 + j * 120
        got = j <= last
        s.raw(f'<circle cx="{x}" cy="{y}" r="14" style="fill:{"var(--accent)" if got else "var(--card)"};stroke:var(--card-border)"/>')
        if j < 4:
            s.line(x + 18, y, x + 102, y, "pl-line" if j < last else "dg-rule")
    s.both(820, y + 6, f"ถึง {NODES[last]}", f"reached {NODES[last]}", "pl-text")
s.both(40, 468, "ทำ 100,000 รอบ แล้วนับว่ากี่รอบไปถึงแต่ละชุมชน", "Do 100,000 runs, then count how many reached each community", "pl-note")
s.both(20, 516, "✓ ไปถึง E แค่ 0.29% (คิดมือ: 0.3 × 0.2 × 0.5 × 0.1 = 0.003)  ·  เครือข่ายจริงมีหลายทาง จึงคิดมือไม่ได้ ต้องจำลอง",
       "✓ only 0.29% reach E (by hand: 0.3 × 0.2 × 0.5 × 0.1 = 0.003)  ·  real networks branch, so simulation is the only way", "ml-ok")
s.save("l14-news.svg", 534)

# ================================================================ L13 bootstrap of the median
rng = np.random.default_rng(42)
idx = rng.choice(np.arange(1, 25), size=(10000, 24), replace=True)
meds = np.median(CH[idx - 1], axis=1)
lo, hi = np.percentile(meds, [2.5, 97.5])
s = Svg(W, f"Bootstrapping the median chapter length of Persuasion. Top: the 24 real chapters (median 3,189.5 "
           f"words; chapter 21 has 7,036). Middle: three bootstrap samples of 24 chapters drawn with replacement "
           f"(repeats shaded), medians 2,870.5, 2,958 and 3,358.5. Bottom: the medians of 10,000 samples; the middle "
           f"95% runs from {lo:,.0f} to {hi:,.0f} words: the 95% confidence interval.")
s.bubble("median ความยาวบทของ Persuasion คือ 3,190 คำ ค่าจริงน่าจะอยู่ช่วงไหน", "Persuasion's median chapter is 3,190 words: where could the true value lie?")
s.both(20, 96, "ข้อมูลจริง 24 บท (คำต่อบท)", "The real 24 chapters (words each)", "pl-label")
for k, v in enumerate(CH):
    x = 300 + k * 35
    h = v / 7036 * 70
    s.box(x, 150 - h, 26, h, "ml-bar-top" if k == 20 else "ml-bar", 3)
    s.text(x + 13, 168, str(k + 1), "pl-note", "middle")
mid = 150 - 3189.5 / 7036 * 70
s.line(292, mid, 1140, mid, "ml-cut-guess")
s.both(20, 130, "median 3,189.5 · บท 21 ยาว 7,036", "median 3,189.5 · ch. 21 is 7,036", "pl-note")
s.box(20, 186, 1140, 196, "nt-band-a", 14)
s.both(40, 216, "สุ่มบทแบบใส่คืน 24 ครั้ง (เลขคือบทที่ถูกสุ่ม · สีเข้ม = ซ้ำ) แล้วหา median", "Draw 24 chapters with replacement (numbers = chapters drawn · shaded = repeated), take the median", "pl-label")
for r in range(3):
    y = 236 + r * 46
    bag = sorted(idx[r])
    for j, c in enumerate(bag):
        x = 40 + j * 38
        rep = list(bag).count(c) > 1
        s.box(x, y, 32, 32, "rc-ctx" if rep else "ml-cell", 6)
        s.text(x + 16, y + 22, str(c), "pl-note" if not rep else "pl-label", "middle")
    s.text(1140, y + 22, f"median {meds[r]:,.1f}".replace(".0", ""), "pl-label", "end")
# histogram of the 10,000 medians
counts, edges = np.histogram(meds, bins=np.arange(2200, 4800, 100))
HX0, HY0, HW = 120, 600, 940
xs = lambda v: HX0 + (v - 2200) / (4800 - 2200) * HW
for c, e in zip(counts, edges):
    hh = c / counts.max() * 130
    inside = lo <= e + 50 <= hi
    s.box(xs(e) + 1, HY0 - hh, HW / 26 - 2, hh, "ml-bar-top" if inside else "ml-bar", 2)
s.line(HX0, HY0, HX0 + HW, HY0, "dg-rule-strong")
for v in (2500, 3000, 3500, 4000, 4500):
    s.text(xs(v), HY0 + 22, f"{v:,}", "pl-note", "middle")
for v, th, en in [(lo, "2.5%", "2.5%"), (hi, "97.5%", "97.5%")]:
    s.line(xs(v), HY0 - 150, xs(v), HY0, "ml-cut")
    s.text(xs(v), HY0 - 158, f"{v:,.0f}", "pl-label", "middle")
s.both(20, 410, "median ของ 10,000 ชุดที่สุ่มใหม่", "The medians of 10,000 resamples", "pl-label")
s.both(20, 664, f"✓ 95% CI ของ median = {lo:,.0f} ถึง {hi:,.0f} คำ (ตัด 2.5% ซ้ายและขวาออก) · ไม่ต้องใช้สูตรใด ๆ",
       f"✓ 95% CI of the median = {lo:,.0f} to {hi:,.0f} words (cut 2.5% off each end) · no formula needed", "ml-ok")
s.save("l14-bootstrap.svg", 682)

# ================================================================ L13 permutation test, volume I vs volume II
rng = np.random.default_rng(42)
perms = [rng.permutation(np.arange(1, 25)) for _ in range(10000)]
diffs = np.array([CH[p[12:] - 1].mean() - CH[p[:12] - 1].mean() for p in perms])
obs = CH[12:].mean() - CH[:12].mean()
extreme = int((np.abs(diffs) >= obs).sum())
s = Svg(W, f"A permutation test: is volume II of Persuasion wordier than volume I? The real split (chapters 1–12 vs "
           f"13–24) gives means 3,225 and 3,783, a difference of +557 words. If the volume labels meant nothing, any 12 "
           f"chapters could be volume I: three shuffles give +1,039, −287 and −49. Over 10,000 shuffles, {extreme:,} "
           f"differences are at least 557 away from 0, so p = {extreme / 10000:.2f}: the difference is easily chance.")
s.bubble("เล่ม 2 ของ Persuasion ยาวกว่าเล่ม 1 จริง หรือแค่บังเอิญ", "Is volume II of Persuasion really wordier, or is it chance?")


def split_row(y, vol1, label_th, label_en, diff, real=False):
    s.both(40, y + 22, label_th, label_en, "pl-label" if real else "pl-text")
    v1 = sorted(vol1)
    v2 = sorted(set(range(1, 25)) - set(v1))
    for j, c in enumerate(v1 + v2):
        x = 180 + j * 34 + (14 if j >= 12 else 0)
        orig = 0 if c <= 12 else 1
        s.box(x, y, 30, 32, "ml-cell", 6)
        s.fill(x + 3, y + 26, 24, 4, VOL[orig], 2)
        s.text(x + 15, y + 21, str(c), "pl-note", "middle")
    s.text(1150, y + 22, f"{diff:+,.1f}".replace("-", "−"), "pl-label" if real else "pl-text", "end")


s.both(180, 96, "“เล่ม 1” (12 บท)", "“volume I” (12 chapters)", "pl-note")
s.both(602, 96, "“เล่ม 2” (12 บท)", "“volume II” (12 chapters)", "pl-note")
s.both(1150, 96, "เล่ม 2 − เล่ม 1", "II − I", "pl-note", "end")
split_row(110, list(range(1, 13)), "จริง", "real", obs, True)
s.box(20, 158, 1140, 170, "nt-band-a", 14)
for k in range(3):
    split_row(172 + k * 50, list(perms[k][:12]), f"สลับครั้ง {k + 1}", f"shuffle {k + 1}", diffs[k])
s.both(40, 322, "แถบสีใต้เลขบอกว่าบทนั้นมาจากเล่มไหนจริง: สลับแล้วปนกัน", "The coloured strip shows each chapter's real volume: after shuffling they mix", "pl-note")
counts, edges = np.histogram(diffs, bins=np.arange(-2000, 2001, 125))
HX0, HY0, HW = 120, 590, 940
xs = lambda v: HX0 + (v + 2000) / 4000 * HW
for c, e in zip(counts, edges):
    hh = c / counts.max() * 140
    far = abs(e + 62.5) >= obs
    s.box(xs(e) + 1, HY0 - hh, HW / 32 - 2, hh, "ml-bar-top" if far else "ml-bar", 2)
s.line(HX0, HY0, HX0 + HW, HY0, "dg-rule-strong")
for v in (-1500, -1000, -500, 0, 500, 1000, 1500):
    s.text(xs(v), HY0 + 22, f"{v:+,}".replace("+0", "0").replace("-", "−"), "pl-note", "middle")
for v in (obs, -obs):
    s.line(xs(v), HY0 - 160, xs(v), HY0, "ml-cut")
s.text(xs(obs), HY0 - 168, "+557", "pl-label", "middle")
s.text(xs(-obs), HY0 - 168, "−557", "pl-label", "middle")
s.both(20, 372, "ผลต่างจากการสลับ 10,000 ครั้ง (สีเข้ม = ห่างจาก 0 อย่างน้อย 557)", "Differences from 10,000 shuffles (dark = at least 557 from 0)", "pl-label")
s.both(20, 646, f"✗ {extreme:,} จาก 10,000 ครั้งห่างจาก 0 อย่างน้อยเท่าของจริง → p = {extreme / 10000:.2f} > 0.05: ไม่มีหลักฐานว่าเล่ม 2 ยาวกว่า",
       f"✗ {extreme:,} of 10,000 shuffles are at least as far from 0 → p = {extreme / 10000:.2f} > 0.05: no evidence volume II is longer", "ml-neg")
s.save("l14-permutation.svg", 664)

# ================================================================ L13 three kinds of alternative world
s = Svg(W, "Three kinds of alternative world. Monte Carlo builds worlds from probabilities you set and answers "
           "'how likely is this outcome?' (news reaches E in 0.29% of runs). Bootstrap builds worlds by resampling your "
           "data with replacement and answers 'how sure am I of this statistic?' (median 95% CI 2,775 to 3,518). "
           "Permutation builds worlds where the group labels mean nothing and answers 'could this difference be "
           "chance?' (p = 0.36).")
s.bubble("ถ้าคิดด้วยสูตรไม่ได้ ก็สร้างโลกคู่ขนานหลายพันโลก", "If you can't solve it with a formula, build thousands of other worlds")
WORLDS = [
    ("Monte Carlo", "สุ่มจาก: ความน่าจะเป็นที่เรากำหนด", "From: probabilities you set", "ถาม: ผลนี้เกิดบ่อยแค่ไหน", "Asks: how likely is this outcome?",
     "ได้: ความน่าจะเป็น หรือการกระจายของผล", "Gives: a probability", "ข่าวไปถึง E: 0.29%", "news reaches E: 0.29%"),
    ("Bootstrap", "สุ่มจาก: ข้อมูลของเราเอง แบบใส่คืน", "From: your data, put back", "ถาม: ค่าสถิตินี้แม่นแค่ไหน", "Asks: how sure am I of this statistic?",
     "ได้: ช่วงความเชื่อมั่น (CI)", "Gives: a confidence interval", "median: 2,775 ถึง 3,518 คำ", "median: 2,775 to 3,518 words"),
    ("Permutation", "สุ่มจาก: การสลับป้ายกลุ่ม", "From: shuffled group labels", "ถาม: ความต่างนี้บังเอิญได้ไหม", "Asks: could this difference be chance?",
     "ได้: p-value", "Gives: a p-value", "เล่ม 2 − เล่ม 1: p = 0.36", "volume II − I: p = 0.36"),
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
