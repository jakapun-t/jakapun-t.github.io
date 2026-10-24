"""Pictures added above the text of stats-dh L14 cards (Monte Carlo, bootstrap, permutation tests), in the stats-dh card
style: a student can skim the picture and read the card's text for the detail.
  l14-sim-everywhere.svg    S01  apps that already simulate or resample (weather, gacha, elections, ratings, A/B tests)
  l14-more-runs.svg         S05  the P(at least 2 sixes) estimate closing in on 0.196 as runs grow
  l14-manuscript.svg        S08  a letter with 5 ambiguous words and the spread of 10,000 readings
  l14-click-tree.svg        S09  the click exercise drawn as a probability tree (no answer)
  l14-bootstrap-uses.svg    S12  three more uses of the bootstrap
  l14-q75-ci.svg            S13  the 75th percentile's lopsided CI next to the median's
  l14-mad-exercise.svg      S15  the "mad" exercise: 4 chapter counts pooled, how many ways to split? (no answer)
  l14-upon-permutation.svg  S17  upon per 1,000 words in 10 Federalist papers, and all 252 splits
  l14-when-permutation.svg  S18  four situations where a permutation test fits
  l14-key-terms.svg         S20  six key terms with small drawings

    course/.venv/bin/python scripts/diagrams/stats_l14_cards.py courses/stats-dh/images

Real numbers (the lesson's code cells, course/.venv): P(≥ 2 sixes in 5 dice) estimates 0.100, 0.180, 0.209, 0.194, 0.196
for 10 … 100,000 runs (exact 0.196); manuscript scores −3: 304, −1: 1,566, 1: 3,138, 3: 3,144, 5: 1,543, 7: 305, 81%
positive; Persuasion median 3,189.5 (95% CI 2,775 to 3,518), 75th percentile 3,853.25 (95% CI 3,354.25 to 5,681.5);
upon per 1,000 words Hamilton 3.73, 1.85, 4.82, 1.49, 2.00 (mean 2.78), Madison 0, 0, 0.36, 1.19, 0 (mean 0.31), the 252
splits are computed here; only the real split reaches +2.47, p = 1/252 = 0.004. Exercise pictures show the story, not
the answer. The app tiles are analogies. Uses the mp-*, ml-*, nt-*, rc-*, dg-*, pl-* classes in templates/page.css.
"""

import math
from itertools import combinations

from stats_svg import Svg, app_grid, circ, emoji_or_icon, poly, term_grid, width  # noqa: F401

W = 1100
CH = [2625, 1993, 2854, 1817, 3350, 3844, 3467, 3367, 2887, 3881, 3029, 5589,
      2775, 2550, 2837, 2420, 3518, 4159, 2410, 3518, 7036, 5942, 6625, 1601]
BLUE, GOLD = "var(--tag-concept-dot)", "var(--tag-example-dot)"

# ================================================================ S01 simulation in everyday apps
s = Svg(W, "Apps that already simulate or resample: a weather app's chance of rain comes from many simulated forecasts, a "
           "gacha game's odds can be checked by simulating pulls, an election forecast simulates the vote thousands of "
           "times (all Monte Carlo); how sure a 4.3-star rating from 12 reviews is, and a poll's margin of error (both "
           "like the bootstrap); an A/B test asks whether a new button is better or lucky (a permutation test).")
s.bubble("แอปที่คุณใช้ก็ “จำลองโลก” อยู่ทุกวัน", "The apps you use “simulate worlds” every day")
bottom = app_grid(s, [
    ("🌦️", "แอปพยากรณ์อากาศ", "Weather app", "ฝน 70% จากหลายแบบจำลอง", "70% rain from many runs", "Monte Carlo", "Monte Carlo"),
    ("🎰", "กาชาในเกม", "Gacha pulls", "สุ่มกี่ครั้งถึงได้การ์ดหายาก", "pulls to get a rare card?", "Monte Carlo", "Monte Carlo"),
    ("🗳️", "พยากรณ์เลือกตั้ง", "Election forecast", "จำลองผลโหวตหลายพันครั้ง", "simulate the vote 1,000s×", "Monte Carlo", "Monte Carlo"),
    ("⭐", "4.3 ดาวจาก 12 รีวิว", "4.3★ from 12 reviews", "คะแนนนี้เชื่อได้แค่ไหน", "how sure is that score?", "bootstrap", "bootstrap"),
    ("📊", "โพลบอก ±3%", "A poll's ±3%", "ค่าจริงน่าจะอยู่ช่วงไหน", "where the truth may lie", "bootstrap", "bootstrap"),
    ("🔀", "A/B test ปุ่มใหม่", "A/B test", "ปุ่มใหม่ดีกว่าจริงหรือฟลุก", "new button better, or luck?", "permutation test", "permutation test"),
])
s.save("l14-sim-everywhere.svg", bottom + 10)

# ================================================================ S05 more runs, a better estimate
EST = [(10, 0.100), (100, 0.180), (1000, 0.209), (10000, 0.194), (100000, 0.196)]
s = Svg(W, "More runs, a better estimate. The Monte Carlo estimate of P(at least 2 sixes with 5 dice) for 10, 100, 1,000, "
           "10,000 and 100,000 runs: 0.100, 0.180, 0.209, 0.194, 0.196. The dashed line is the exact answer, 0.196. Few "
           "runs swing far from it; 100,000 runs match it to 3 decimals.")
s.bubble("ต้องทำกี่รอบจึงพอ", "How many runs are enough?")
X0, X1, Y0, Y1 = 160, 1000, 330, 90     # plot box: x for runs (log), y for 0.08 … 0.22
Y = lambda v: Y0 - (v - 0.08) / 0.14 * (Y0 - Y1)
s.line(X0, Y0, X1, Y0, "mp-axis")
s.line(X0, Y1, X0, Y0, "mp-axis")
for v in (0.10, 0.15, 0.20):
    s.text(X0 - 10, Y(v) + 5, f"{v:.2f}", "mp-s", "end")
s.line(X0, Y(0.196), X1, Y(0.196), "mp-straight")
s.both(X0 + 12, Y(0.196) - 10, "คำตอบจริง 0.196", "exact 0.196", "mp-acc")
pts = []
for i, (n, v) in enumerate(EST):
    x = X0 + 60 + i * 190
    pts.append((x, Y(v)))
    s.text(x, Y0 + 24, f"{n:,}", "mp-c", "middle")
poly(s, pts, "mp-curve-b")
for i, ((x, y), (n, v)) in enumerate(zip(pts, EST)):
    circ(s, x, y, 8, "var(--accent)" if n == 100000 else "var(--tag-concept-dot)")
    s.text(x, y - 16 if v >= 0.19 or n == 10 else y + 28, f"{v:.3f}", "mp-n", "middle")
s.both(570, 380, "จำนวนรอบ (ยิ่งมาก ยิ่งใกล้คำตอบจริง)", "number of runs (more runs, closer to the truth)", "mp-s", "middle")
s.both(40, 120, "ค่าประมาณ", "estimate", "mp-s")
s.save("l14-more-runs.svg", 392)

# ================================================================ S08 an ambiguous manuscript
COUNTS = [(-3, 304), (-1, 1566), (1, 3138), (3, 3144), (5, 1543), (7, 305)]
s = Svg(W, "An old letter with 5 words that can be read two ways (+1 or −1 each); the clear words add +2. Ten thousand "
           "random readings give scores −3: 304, −1: 1,566, +1: 3,138, +3: 3,144, +5: 1,543, +7: 305. 81% of the readings "
           "are positive, so the letter is probably positive, and we can say how sure we are.")
s.bubble("จดหมายที่อ่านได้หลายแบบ น้ำเสียงบวกหรือลบ", "A letter you can read many ways: positive or negative?")
s.panel(10, 70, 470, 300, "ml-cell", "คำกำกวม 5 คำ", "5 ambiguous words", 1)
s.raw('<path d="M40 112 h260 l24 24 v214 h-284 Z" class="ml-cell"/>')
for r in range(7):
    y = 140 + r * 28
    s.line(56, y, 290, y, "mp-guide")
for k, (x, y) in enumerate(((90, 140), (210, 168), (140, 224), (240, 252), (110, 308))):
    s.box(x - 26, y - 18, 52, 24, "rc-ctx", 6)
    s.text(x, y, "?", "mp-n", "middle")
s.both(336, 160, "อ่านแบบ A: +1", "reading A: +1", "ml-ok")
s.both(336, 190, "อ่านแบบ B: −1", "reading B: −1", "mp-acc")
s.both(336, 230, "คำชัด: +2", "clear words: +2", "mp-c")
s.panel(500, 70, 590, 300, "ml-cell", "สุ่มการอ่าน 10,000 แบบ", "10,000 random readings", 2)
base, mx = 320, 3144
for i, (sc, n) in enumerate(COUNTS):
    x = 540 + i * 86
    h = n / mx * 170
    s.fill(x, base - h, 60, h, "var(--tag-exercise-dot)" if sc > 0 else "var(--accent)", 4)
    s.text(x + 30, base - h - 8, f"{n:,}", "mp-s", "middle")
    s.text(x + 30, base + 22, f"{sc:+d}", "mp-c", "middle")
s.line(526, base, 1066, base, "mp-axis")
s.both(1066, 128, "บวก 81% ✓", "81% positive ✓", "ml-ok", "end")
s.save("l14-manuscript.svg", 380)

# ================================================================ S09 the click exercise as a tree (story only)
s = Svg(W, "The click exercise as a tree: a top result is relevant with probability 0.6 or not with 0.4. If relevant, the "
           "user clicks with 0.7 (does not with 0.3); if not, clicks with 0.1 (does not with 0.9). The question mark is "
           "the overall click rate the exercise asks for.")
s.bubble("ผู้ใช้คลิกผลลัพธ์อันดับ 1 บ่อยแค่ไหน", "How often does the user click the top result?")
s.box(40, 190, 150, 50, "ml-model", 12)
s.both(115, 221, "ผลลัพธ์อันดับ 1", "top result", "ml-model-text", "middle")
for k, (yy, th, en, p, kids) in enumerate(((120, "ตรงคำค้น", "relevant", "0.6", (("คลิก", "click", "0.7"), ("ไม่คลิก", "no click", "0.3"))),
                                         (310, "ไม่ตรง", "not relevant", "0.4", (("คลิก", "click", "0.1"), ("ไม่คลิก", "no click", "0.9"))))):
    s.arrow(192, 215, 380, yy + 20)
    s.text(286, yy + 52 if k == 0 else yy - 4, p, "mp-acc", "middle")
    s.box(384, yy, 170, 44, "nt-band-a", 10)
    s.both(469, yy + 28, th, en, "mp-t", "middle")
    for j, (cth, cen, cp) in enumerate(kids):
        ky = yy - 34 + j * 68
        s.arrow(556, yy + 22, 720, ky + 18)
        s.text(640, ky + (8 if j == 0 else 46), cp, "mp-acc", "middle")
        click = j == 0
        s.box(724, ky, 150, 38, "rc-res" if click else "ml-cell", 10)
        s.both(799, ky + 25, cth, cen, "mp-chip", "middle")
s.box(930, 172, 140, 86, "rc-con", 12)
s.both(1000, 198, "คลิกรวม", "click rate", "mp-s", "middle")
s.text(1000, 240, "= ?", "mp-big", "middle")
s.save("l14-click-tree.svg", 400)


# ================================================================ S12 three more uses of the bootstrap
def d_tone(x, y, w, h):
    for row, (spread, lab) in enumerate(((4, "narrow"), (16, "wide"))):
        yy = y + 22 + row * 40
        s.box(x + 14, yy - spread / 2 - 3, w - 28, spread + 6, "mp-area", 4)
        poly(s, [(x + 14 + i * (w - 28) / 9, yy + math.sin(i * 1.3 + row) * spread / 2) for i in range(10)], "mp-curve-b")


def d_speech(x, y, w, h):
    heights = [60, 52, 38, 26, 18, 12, 8, 6, 4, 3, 2]
    for i, hh in enumerate(heights):
        s.fill(x + 14 + i * 18, y + 74 - hh, 14, hh, "var(--tag-concept-dot)", 2)
    s.line(x + 14 + 6.5 * 18, y + 6, x + 14 + 6.5 * 18, y + 78, "mp-straight")
    s.text(x + 14 + 6.5 * 18 + 6, y + 18, "90th", "mp-s")


def d_bagging(x, y, w, h):
    for i in range(3):
        bx = x + 18 + i * 70
        s.raw(f'<path d="M{bx} {y + 20} q24 -14 48 0 l-6 36 h-36 Z" style="fill:var(--tag-example-bg);stroke:var(--tag-example-dot);stroke-width:1.5"/>')
        s.arrow(bx + 24, y + 58, bx + 24, y + 70)
    s.text(x + w / 2, y + 82, "→ vote", "mp-s", "middle")


s = Svg(W, "Three more uses of the bootstrap, same steps, different statistic: is a novel's tone steady (the CI of mean "
           "sentiment per chapter: narrow = steady, wide = shifting), does a character speak at length (the CI of the 90th "
           "percentile of speech length), and random forests (each tree trains on a bootstrap bag, then they vote).")
term_grid(s, [
    (("น้ำเสียงคงที่ไหม", "Is the tone steady?"), d_tone, "CI ของ sentiment เฉลี่ย", "CI of mean sentiment", "แคบ = คงที่ กว้าง = เปลี่ยน", "narrow = steady, wide = shifting"),
    (("ตัวละครพูดยาวไหม", "Long speeches?"), d_speech, "CI ของ percentile ที่ 90", "CI of the 90th percentile", "ข้อมูลเบ้ ไม่มีสูตร", "skewed data, no formula"),
    (("random forest", "Random forest"), d_bagging, "แต่ละต้นใช้ bootstrap", "each tree: a bootstrap bag", "bagging = bootstrap + โหวต", "bagging = bootstrap + vote"),
], cols=3, tw=352)
s.save("l14-bootstrap-uses.svg", 212)

# ================================================================ S13 the 75th percentile's lopsided CI
s = Svg(W, "Bootstrapping a different statistic. The 24 chapter lengths of Persuasion on a line from 1,500 to 7,500 words. The "
           "median is 3,190 with a 95% CI of 2,775 to 3,518, fairly tight. The 75th percentile is 3,853 with a 95% CI of "
           "3,354 to 5,682: very wide and lopsided, because the three long chapters (5,942, 6,625, 7,036) may or may not "
           "land in each resampled set.")
s.bubble("“บทยาว” ของ Austen ยาวแค่ไหน", "How long are Austen's long chapters?")
LO, HI, XL, XR = 1500, 7500, 80, 1040
X = lambda v: XL + (v - LO) / (HI - LO) * (XR - XL)
s.line(XL, 150, XR, 150, "mp-axis")
for v in range(2000, 7501, 1000):
    s.line(X(v), 146, X(v), 154, "mp-axis")
    s.text(X(v), 174, f"{v:,}", "mp-s", "middle")
for c in sorted(CH):
    long = c > 5000
    circ(s, X(c), 128 - (8 if CH.count(c) > 1 and c == 3518 else 0), 7, "var(--accent)" if long else "var(--tag-concept-dot)")
s.both(X(6500), 104, "3 บทยาว", "3 long chapters", "mp-acc", "middle")
s.both(XL, 104, "24 บท (คำต่อบท)", "24 chapters (words each)", "mp-s")
for row, (th, en, est, lo, hi, cls) in enumerate((("median", "median", 3189.5, 2775, 3518, "mp-curve-b"),
                                                   ("percentile ที่ 75", "75th percentile", 3853.25, 3354.25, 5681.5, "mp-curve"))):
    y = 226 + row * 74
    s.both(XL, y - 18, f"{th}: 95% CI {lo:,.0f}–{hi:,.0f}", f"{en}: 95% CI {lo:,.0f}–{hi:,.0f}", "mp-t")
    s.line(X(lo), y + 10, X(hi), y + 10, cls)
    s.line(X(lo), y, X(lo), y + 20, cls)
    s.line(X(hi), y, X(hi), y + 20, cls)
    circ(s, X(est), y + 10, 7, "var(--ink)")
s.both(XR, 296, "กว้างและเบ้ไปทางบน", "wide and lopsided", "mp-acc", "end")
s.save("l14-q75-ci.svg", 340)

# ================================================================ S15 the "mad" exercise (story only)
s = Svg(W, "The 'mad' exercise: author A uses 'mad' 10 and 12 times in two chapters, author B 18 and 20. Pool the four "
           "counts, then list every way to choose two of them as a fake author A; the question marks are what the exercise "
           "asks for.")
s.bubble("ผู้เขียน B ใช้คำว่า “mad” มากกว่า A จริงไหม", "Does author B really use “mad” more than author A?")
for k, (name, vals, col) in enumerate((("A", (10, 12), BLUE), ("B", (18, 20), GOLD))):
    y = 96 + k * 70
    s.both(40, y + 30, f"ผู้เขียน {name}", f"author {name}", "mp-t")
    for i, v in enumerate(vals):
        s.fill(170 + i * 70, y, 56, 44, col, 10)
        s.text(198 + i * 70, y + 29, str(v), "ml-model-text", "middle")
s.arrow(330, 152, 420, 152)
s.both(375, 136, "รวมกัน", "pool", "mp-s", "middle")
for i, (v, col) in enumerate(((10, BLUE), (12, BLUE), (18, GOLD), (20, GOLD))):
    circ(s, 470 + i * 64, 152, 26, col)
    s.text(470 + i * 64, 159, str(v), "ml-model-text", "middle")
s.arrow(700, 152, 760, 152)
s.box(770, 100, 310, 104, "rc-con", 12)
s.both(925, 134, "เลือก 2 ค่าเป็น “A ปลอม”", "choose 2 as a “fake A”", "mp-t", "middle")
s.both(925, 168, "มีกี่วิธี? p = ?", "how many ways? p = ?", "mp-big", "middle")
s.both(550, 252, "ค่าสถิติ = mean(B) − mean(A)", "statistic = mean(B) − mean(A)", "mp-s", "middle")
s.save("l14-mad-exercise.svg", 268)

# ================================================================ S17 upon: a real difference
HAM = [3.73, 1.85, 4.82, 1.49, 2.00]
MAD = [0.00, 0.00, 0.36, 1.19, 0.00]
allv = HAM + MAD
diffs = []
for idx in combinations(range(10), 5):
    a = [allv[i] for i in idx]
    b = [allv[i] for i in range(10) if i not in idx]
    diffs.append(round(sum(a) / 5 - sum(b) / 5, 4))
real = round(sum(HAM) / 5 - sum(MAD) / 5, 4)
n_ext = sum(d >= real - 1e-9 for d in diffs)
s = Svg(W, f"A real difference. Left: upon per 1,000 words in 10 Federalist papers; Hamilton (blue) 3.73, 1.85, 4.82, 1.49, "
           f"2.00, mean 2.78; Madison (amber) 0, 0, 0.36, 1.19, 0, mean 0.31. Right: all 252 ways to split the 10 values "
           f"into 5 + 5; only {n_ext} split, the real one, reaches the real difference of +2.47, so p = 1/252 = 0.004.")
s.bubble("ถ้าความต่างเป็นของจริง permutation test เห็นอะไร", "When a difference is real, what does a permutation test see?")
s.panel(10, 70, 420, 300, "ml-cell", "upon ต่อ 1,000 คำ", "upon per 1,000 words", 1)
for k, (name, vals, col) in enumerate((("Hamilton", HAM, BLUE), ("Madison", MAD, GOLD))):
    x = 120 + k * 180
    for i, v in enumerate(vals):
        circ(s, x + (i - 2) * 14, 330 - v * 38, 8, col)
    m = sum(vals) / 5
    s.line(x - 50, 330 - m * 38, x + 50, 330 - m * 38, "mp-straight")
    s.text(x + 56, 330 - m * 38 + 5, f"{m:.2f}", "mp-n")
    s.text(x, 356, name, "mp-c", "middle")
s.panel(450, 70, 640, 300, "ml-cell", "ทั้ง 252 วิธีแบ่ง 5 + 5", "All 252 ways to split 5 + 5", 2)
lo, hi, nb = -2.6, 2.6, 26
bins = [0] * nb
for d in diffs:
    bins[min(nb - 1, int((d - lo) / (hi - lo) * nb))] += 1
mx = max(bins)
for i, c in enumerate(bins):
    if c:
        s.fill(480 + i * 22, 330 - c / mx * 170, 18, c / mx * 170, "var(--accent)" if lo + i * (hi - lo) / nb >= real - 0.2 else "var(--tag-concept-dot)", 2)
xr = 480 + (real - lo) / (hi - lo) * nb * 22
s.line(xr, 128, xr, 336, "mp-curve")
s.both(xr - 8, 124, f"ของจริง +2.47 ({n_ext} จาก 252)", f"real +2.47 ({n_ext} of 252)", "mp-acc", "end")
s.line(470, 330, 1062, 330, "mp-axis")
s.text(480 + (0 - lo) / (hi - lo) * nb * 22, 354, "0", "mp-s", "middle")
s.text(1070, 354, "p = 0.004 ✓", "ml-ok", "end")
s.save("l14-upon-permutation.svg", 380)


# ================================================================ S18 when to use a permutation test
def d_small(x, y, w, h):
    for i in range(4):
        circ(s, x + 40 + i * 22, y + 34, 7, BLUE)
        circ(s, x + 40 + i * 22, y + 58, 7, GOLD)


def d_skew(x, y, w, h):
    for i, hh in enumerate([62, 44, 30, 20, 13, 8, 5, 3]):
        s.fill(x + 30 + i * 20, y + 76 - hh, 16, hh, BLUE, 2)


def d_unknown(x, y, w, h):
    poly(s, [(x + 20 + i * 5, y + 74 - 50 * math.exp(-((i - 20) / 7) ** 2)) for i in range(41)], "mp-straight")
    s.text(x + w / 2, y + 48, "?", "mp-big", "middle")


def d_custom(x, y, w, h):
    s.text(x + w / 2, y + 40, "TTR · topic share", "mp-c", "middle")
    s.text(x + w / 2, y + 66, "median · ...", "mp-c", "middle")


s = Svg(W, "Four situations where a permutation test fits: small samples, skewed data, a distribution you don't know, and a "
           "statistic you made up yourself (type-token ratio, a topic share, a median).")
term_grid(s, [
    (("ตัวอย่างน้อย", "Small samples"), d_small, "4–6 ค่าต่อกลุ่ม", "4–6 values per group", "ไล่ทุกวิธีแบ่งได้", "you can list every split"),
    (("ข้อมูลเบ้", "Skewed data"), d_skew, "เช่น ความยาวบทพูด", "e.g. dialogue length", "ไม่ต้องสมมติ normal", "no normal curve needed"),
    (("ไม่รู้การแจกแจง", "Unknown shape"), d_unknown, "ไม่รู้ว่าข้อมูลมาจากไหน", "no known distribution", "สลับป้ายแทนสูตร", "shuffle labels instead"),
    (("ค่าสถิติที่คิดเอง", "Your own statistic"), d_custom, "ไม่มีการทดสอบสำเร็จรูป", "no ready-made test", "ใช้ค่าอะไรก็ได้", "any statistic works"),
])
s.save("l14-when-permutation.svg", 212)


# ================================================================ S20 key terms
def d_mc(x, y, w, h):
    emoji_or_icon(s, "🎲", x + 52, y + 42, 60)
    s.text(x + 160, y + 50, "× 10,000", "mp-n", "middle")


def d_boot(x, y, w, h):
    for i, (n, again) in enumerate(((1, True), (1, True), (4, False), (6, True), (6, True))):
        s.raw(f'<circle cx="{x + 40 + i * 40}" cy="{y + 42}" r="15" class="{"rc-ctx" if again else "ml-cell"}"/>')
        s.text(x + 40 + i * 40, y + 47, str(n), "mp-c", "middle")


def d_pci(x, y, w, h):
    for i in range(15):
        hh = 60 * math.exp(-((i - 7) / 3.2) ** 2 / 2)
        tail = i < 2 or i > 12
        s.fill(x + 20 + i * 20, y + 74 - hh, 16, hh, "var(--card-border)" if tail else BLUE, 2)
    s.text(x + 24, y + 18, "2.5%", "mp-s")
    s.text(x + w - 20, y + 18, "2.5%", "mp-s", "end")


def d_null(x, y, w, h):
    for i, col in enumerate((BLUE, GOLD, BLUE, BLUE, GOLD, GOLD)):
        s.fill(x + 26 + i * 34, y + 16, 26, 22, col, 4)
    for i, col in enumerate((GOLD, BLUE, GOLD, BLUE, BLUE, GOLD)):
        s.fill(x + 26 + i * 34, y + 56, 26, 22, col, 4)
    s.text(x + w - 14, y + 52, "⇅", "mp-n", "end")


def d_pval(x, y, w, h):
    for i in range(15):
        hh = 60 * math.exp(-((i - 7) / 3.2) ** 2 / 2)
        s.fill(x + 20 + i * 20, y + 74 - hh, 16, hh, "var(--accent)" if i >= 12 else BLUE, 2)
    s.line(x + 258, y + 6, x + 258, y + 78, "mp-curve")


def d_nonpar(x, y, w, h):
    poly(s, [(x + 30 + i * 5, y + 72 - 50 * math.exp(-((i - 20) / 7) ** 2)) for i in range(41)], "mp-curve-b")
    s.line(x + 40, y + 14, x + 220, y + 76, "mp-curve")


s = Svg(W, "Six key terms with a picture each: Monte Carlo (draw thousands of times and count), a bootstrap sample (drawn "
           "with replacement, some rows repeat), a percentile CI (cut 2.5% from each end), the permutation null hypothesis "
           "(labels mean nothing, so shuffle them), the permutation p-value (the share of shuffles at least as extreme as "
           "the real result), non-parametric (no normal curve assumed).")
bottom = term_grid(s, [
    ("Monte Carlo", d_mc, "สุ่มซ้ำหลายพันครั้ง", "draw thousands of times", "แล้วนับสัดส่วน", "and count the outcomes"),
    ("Bootstrap sample", d_boot, "สุ่มแบบใส่คืน", "drawn with replacement", "บางแถวซ้ำ บางแถวหาย", "some rows repeat, some vanish"),
    ("Percentile CI", d_pci, "ตัดหัวท้ายข้างละ 2.5%", "cut 2.5% off each end", "ได้ 95% CI ไม่ต้องใช้สูตร", "a 95% CI with no formula"),
    (("H₀ ของ permutation", "Permutation H₀"), d_null, "ป้ายกลุ่มไม่มีความหมาย", "the labels mean nothing", "จึงสลับป้ายได้", "so they can be swapped"),
    (("p-value จากการสลับ", "Permutation p-value"), d_pval, "สัดส่วนที่สุดโต่งเท่าของจริง", "share as extreme as real", "p < 0.05 → ปฏิเสธ H₀", "p < 0.05 → reject H₀"),
    ("Non-parametric", d_nonpar, "ไม่สมมติการแจกแจง", "assumes no distribution", "bootstrap, permutation", "bootstrap, permutation"),
], cols=3, tw=352)
s.save("l14-key-terms.svg", bottom + 10)
