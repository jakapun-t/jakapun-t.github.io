"""Pictures added above the text of stats-dh L14 cards (Monte Carlo, bootstrap, permutation tests), in the stats-dh card
style: a student can skim the picture and read the card's text for the detail.
  l14-sim-everywhere.svg    S01  questions with no direct formula, so apps simulate or resample (each tile says why)
  l14-more-runs.svg         S05  the P(at least 2 sixes) estimate closing in on 0.196 as runs grow
  l14-manuscript.svg        S08  an ambiguous chat reply (5 parts with two readings) and the spread of 10,000 readings
  l14-click-tree.svg        S09  the click exercise drawn as a probability tree (no answer)
  l14-bootstrap-uses.svg    S13  three more uses of the bootstrap: kind comments (14/20, CI 50–90%), screen time vs sleep
                                 (r −0.66, CI −0.90 to −0.20; bootstrap of rows, default_rng(42)), random-forest bags
  l14-fullstop-permutation.svg  S18  yes/no: chat ends with ".", Gen Z 2/10 vs parents 8/10, scipy permutation_test random_state=42
  l14-q75-ci.svg            S12  the 75th percentile's lopsided CI next to the median's
  l14-mad-exercise.svg      S15  two TikTok creators, 2 clips each: 4 view counts pooled, how many ways to split? (no answer)
  l14-upon-permutation.svg  S17  😭 per 100 messages, 5 Gen-Z friends vs 5 parents (made up), and all 252 splits
  l14-when-permutation.svg  S18  four situations where a permutation test fits
  l14-key-terms.svg         S20  six key terms with small drawings

    course/.venv/bin/python scripts/diagrams/stats_l14_cards.py courses/stats-dh/images

Real numbers (the lesson's code cells, course/.venv): P(≥ 2 sixes in 5 dice) estimates 0.100, 0.180, 0.209, 0.194, 0.196
for 10 … 100,000 runs (exact 0.196); ambiguous-chat scores −3: 304, −1: 1,566, 1: 3,138, 3: 3,144, 5: 1,543, 7: 305, 81%
positive; delivery waits (made-up, 24 orders) median 25 (95% CI 23 to 28), 75th percentile 29.25 (95% CI 25.5 to 40);
😭 per 100 messages Gen Z 3.73, 1.85, 4.82, 1.49, 2.00 (mean 2.78), parents 0, 0, 0.36, 1.19, 0 (mean 0.31), the 252
splits are computed here; only the real split reaches +2.47, p = 1/252 = 0.004. Exercise pictures show the story, not
the answer. The app tiles are analogies. Uses the mp-*, ml-*, nt-*, rc-*, dg-*, pl-* classes in templates/page.css.
"""

import math
from itertools import combinations

import numpy as np

from stats_svg import Svg, app_grid, circ, emoji_or_icon, poly, term_grid, width  # noqa: F401

W = 1100
WAIT = [18, 22, 25, 21, 27, 24, 31, 19, 23, 26, 48, 20,
        24, 28, 22, 35, 25, 55, 30, 21, 60, 26, 25, 29]   # minutes; 1–12 dry days, 13–24 rainy days
BLUE, GOLD = "var(--tag-concept-dot)", "var(--tag-example-dot)"

# ================================================================ S01 simulation in everyday apps
s = Svg(W, "Questions with no direct formula, so apps simulate or resample. Weather: millions of linked variables, no "
           "equation, so Monte Carlo. Gacha pulls: pity and rate-up rules are too messy, so Monte Carlo. Election "
           "forecast: districts move together, no single formula, so Monte Carlo. A 4.3-star rating from 12 reviews: "
           "too few reviews for textbook formulas, so bootstrap. Delivery time, median 25 minutes: no CI formula for a "
           "median, so bootstrap. A/B test of a new button: no formula says how big a gap is just luck, so a "
           "permutation test.")
s.bubble("คำถามพวกนี้ไม่มีสูตรตอบตรง ๆ แอปจึง “จำลองโลก” แทน", "These questions have no direct formula, so apps “simulate worlds”")
bottom = app_grid(s, [
    ("🌦️", "แอปพยากรณ์อากาศ", "Weather app", "พรุ่งนี้ฝนตกกี่ %", "chance of rain tomorrow?", "Monte Carlo", "Monte Carlo",
     "✗ ตัวแปรพันกันเป็นล้าน แก้สมการไม่ได้", "✗ millions of linked variables"),
    ("🎰", "กาชาในเกม", "Gacha pulls", "สุ่มกี่ครั้งถึงได้การ์ดหายาก", "pulls to get a rare card?", "Monte Carlo", "Monte Carlo",
     "✗ มีการันตี + rate-up สูตรยุ่งเกิน", "✗ pity + rate-up: too messy"),
    ("🗳️", "พยากรณ์เลือกตั้ง", "Election forecast", "ใครจะชนะ โอกาสกี่ %", "who wins, how likely?", "Monte Carlo", "Monte Carlo",
     "✗ แต่ละเขตขึ้นต่อกัน ไม่มีสูตรรวม", "✗ districts move together"),
    ("⭐", "4.3 ดาวจาก 12 รีวิว", "4.3★ from 12 reviews", "คะแนนนี้เชื่อได้แค่ไหน", "how sure is that score?", "bootstrap", "bootstrap",
     "✗ รีวิวน้อย สูตรตามตำราไม่แม่น", "✗ too few for textbook formulas"),
    ("🍽", "ส่งอาหาร median 25 นาที", "Delivery: median 25 min", "ปกติรอนานแค่ไหน", "how long is the usual wait?", "bootstrap", "bootstrap",
     "✗ median ไม่มีสูตรช่วงความเชื่อมั่น", "✗ no CI formula for a median"),
    ("🔀", "A/B test ปุ่มใหม่", "A/B test", "ปุ่มใหม่ดีกว่าจริงหรือฟลุก", "new button better, or luck?", "permutation test", "permutation test",
     "✗ ไม่มีสูตรบอกว่าต่างแค่ไหนคือฟลุก", "✗ no formula for “just luck”"),
], th_=184)
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

# ================================================================ S08 an ambiguous chat: good vibe or bad?
COUNTS = [(-3, 304), (-1, 1566), (1, 3138), (3, 3144), (5, 1543), (7, 305)]
AMBIG = [("ก็ได้", "fine", "ยินดี", "fine by me", "ประชด", "sarcastic"),
         ("555", "lol", "ขำจริง", "real laugh", "ขำแห้ง", "dry laugh"),
         ("😅", "😅", "เขิน", "shy", "อึดอัด", "awkward"),
         ("เดี๋ยวค่อยคุย", "talk later", "ยุ่งอยู่", "busy now", "ตัดบท", "brushing off"),
         ("ok.", "ok.", "ตกลง", "agreed", "งอน", "sulking")]
s = Svg(W, "An ambiguous chat: good vibe or bad? A friend replies 'had so much fun today, thanks' (clear: +2), then "
           "'fine, lol 😅 talk later ok.' Five parts can be read two ways, +1 or −1: 'fine' (fine by me / sarcastic), "
           "'lol' (real laugh / dry laugh), 😅 (shy / awkward), 'talk later' (busy now / brushing off), 'ok.' (agreed / "
           "sulking). Ten thousand random readings give scores −3: 304, −1: 1,566, +1: 3,138, +3: 3,144, +5: 1,543, "
           "+7: 305. 81% of the readings are a good vibe.")
s.bubble("แชทนี้ vibe ดีหรือแย่? บางคำอ่านได้สองแบบ", "Good vibe or bad? Some parts can be read two ways")
s.panel(10, 70, 470, 300, "ml-cell", "แชทจากเพื่อน", "A friend's reply", 1)
s.box(30, 112, 300, 34, "ml-cell-b", 17)
s.both(46, 135, "วันนี้สนุกมาก ขอบคุณนะ", "had so much fun today, thanks", "pl-text")
s.both(344, 135, "ชัด: +2", "clear: +2", "ml-ok-small")
s.box(30, 154, 430, 34, "rc-ctx", 17)
s.both(46, 177, "ก็ได้ 555 😅 เดี๋ยวค่อยคุย ok.", "fine lol 😅 talk later ok.", "pl-label")
s.both(30, 214, "5 ส่วนที่อ่านได้สองแบบ", "5 two-way parts", "pl-note")
s.both(222, 214, "อ่านแบบดี +1", "good +1", "ml-ok-small")
s.both(352, 214, "อ่านแบบแย่ −1", "bad −1", "mp-acc")
for k, (th, en, gth, gen, bth, ben) in enumerate(AMBIG):
    y = 226 + k * 28
    s.box(30, y, 150, 24, "rc-ctx", 12)
    s.both(105, y + 18, th, en, "mp-c", "middle")
    s.both(222, y + 18, gth, gen, "mp-s")
    s.both(352, y + 18, bth, ben, "mp-s")
s.panel(500, 70, 590, 300, "ml-cell", "สุ่มการตีความ 10,000 แบบ", "10,000 random readings", 2)
base, mx = 320, 3144
for i, (sc, n) in enumerate(COUNTS):
    x = 540 + i * 86
    h = n / mx * 170
    s.fill(x, base - h, 60, h, "var(--tag-exercise-dot)" if sc > 0 else "var(--accent)", 4)
    s.text(x + 30, base - h - 8, f"{n:,}", "mp-s", "middle")
    s.text(x + 30, base + 22, f"{sc:+d}", "mp-c", "middle")
s.line(526, base, 1066, base, "mp-axis")
s.both(540, 362, "← แย่", "← bad vibe", "mp-s")
s.both(1066, 362, "ดี →", "good vibe →", "mp-s", "end")
s.both(1066, 128, "vibe ดี 81% ✓", "good vibe 81% ✓", "ml-ok", "end")
# how a reading is scored
s.box(10, 384, 1080, 108, "nt-band-a", 14)
s.both(30, 414, "วิธีให้คะแนน:  คำบวกที่ชัดคำละ +1 (สนุกมาก +1, ขอบคุณ +1 = +2)  ·  ส่วนกำกวม อ่านแบบดี +1 แบบแย่ −1",
       "How a reading is scored:  each clearly positive word +1 (fun +1, thanks +1 = +2)  ·  each ambiguous part: good +1, bad −1",
       "pl-label")
s.both(30, 444, "คะแนนรวม = +2 + ทั้ง 5 ส่วน  →  มากกว่า 0 = vibe ดี · น้อยกว่า 0 = vibe แย่ (รวมได้แต่เลขคี่ จึงไม่มีเสมอ)",
       "score = +2 + all 5 parts  →  above 0 = good vibe · below 0 = bad vibe (the total is always odd, never 0)", "pl-text")
s.both(30, 474, "ตัวอย่างการอ่านหนึ่งแบบ: ยินดี +1 · ขำแห้ง −1 · เขิน +1 · ตัดบท −1 · งอน −1  →  2 + 1 − 1 + 1 − 1 − 1 = +1  →  vibe ดี",
       "one reading, for example: fine by me +1 · dry laugh −1 · shy +1 · brushing off −1 · sulking −1  →  2 + 1 − 1 + 1 − 1 − 1 = +1  →  good vibe",
       "mp-s")
s.save("l14-manuscript.svg", 500)

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


# ================================================================ S13 three more uses of the bootstrap
KIND = [1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1]   # 20 comments, 1 = kind (made up)
SCREEN = [2, 3, 4, 4, 5, 6, 6, 7, 8, 9]                                # 10 friends, hours of screen time a day
SLEEP = [8.0, 7.0, 7.6, 6.5, 7.4, 6.0, 7.2, 6.8, 5.5, 6.6]             # the same 10 friends, hours of sleep


def d_comments(x, y, w, h):
    for i, k in enumerate(KIND):
        cx, cy = x + 30 + (i % 10) * 30, y + 26 + (i // 10) * 34
        s.raw(f'<rect x="{cx - 11}" y="{cy - 10}" width="22" height="18" rx="5" '
              f'style="fill:{"var(--tag-exercise-bg)" if k else "var(--card)"};stroke:{"var(--tag-exercise-fg)" if k else "var(--muted)"};stroke-width:1.2"/>')
        s.text(cx, cy + 4, "✓" if k else "✗", "mp-s", "middle")


def d_scatter(x, y, w, h):
    sx = lambda v: x + 24 + (v - 2) / 7 * (w - 60)
    sy = lambda v: y + 78 - (v - 5.5) / 2.5 * 64
    s.line(x + 16, y + 80, x + w - 20, y + 80, "mp-straight")
    s.line(x + 16, y + 80, x + 16, y + 8, "mp-straight")
    m, c = np.polyfit(SCREEN, SLEEP, 1)
    s.line(sx(2), sy(m * 2 + c), sx(9), sy(m * 9 + c), "ml-cut-guess")
    for a_, b_ in zip(SCREEN, SLEEP):
        circ(s, sx(a_), sy(b_), 5, "var(--tag-concept-dot)")


def d_bagging(x, y, w, h):
    for i in range(3):
        bx = x + 18 + i * 70
        s.raw(f'<path d="M{bx} {y + 20} q24 -14 48 0 l-6 36 h-36 Z" style="fill:var(--tag-example-bg);stroke:var(--tag-example-dot);stroke-width:1.5"/>')
        s.arrow(bx + 24, y + 58, bx + 24, y + 70)
    s.text(x + w / 2, y + 82, "→ vote", "mp-s", "middle")


s = Svg(W, "Three more uses of the bootstrap, same steps, different statistic (made-up numbers). How kind are the comments "
           "under my clip: 14 of 20 are kind, 70%, 95% CI 50% to 90%. Do friends who spend more time on their phone sleep "
           "less: screen time against sleep for 10 friends, correlation r = −0.66, 95% CI −0.90 to −0.20. Random forest: "
           "each tree trains on its own bootstrap bag of orders, then the trees vote.")
term_grid(s, [
    (("คอมเมนต์ใจดีกี่ %", "How kind are comments?"), d_comments, "14 จาก 20 = 70%", "14 of 20 = 70%", "95% CI: 50% ถึง 90%", "95% CI: 50% to 90%"),
    (("เล่นมือถือมาก นอนน้อย?", "More screen, less sleep?"), d_scatter, "r = −0.66 (10 คน)", "r = −0.66 (10 friends)", "95% CI: −0.90 ถึง −0.20", "95% CI: −0.90 to −0.20"),
    (("random forest", "Random forest"), d_bagging, "แต่ละต้นใช้ bootstrap", "each tree: a bootstrap bag", "bagging = bootstrap + โหวต", "bagging = bootstrap + vote"),
], cols=3, tw=352)
s.save("l14-bootstrap-uses.svg", 212)

# ================================================================ S12 the 75th percentile's lopsided CI
s = Svg(W, "Bootstrapping a different statistic. The 24 delivery waits on a line from 15 to 65 minutes. The median is 25 with "
           "a 95% CI of 23 to 28, fairly tight. The 75th percentile is 29.25 with a 95% CI of 25.5 to 40: very wide and "
           "lopsided, because the three very slow orders (48, 55, 60) may or may not land in each resampled set.")
s.bubble("ออเดอร์ที่ “ช้า” ช้าแค่ไหน", "How slow are the slow orders?")
LO, HI, XL, XR = 15, 65, 80, 1040
X = lambda v: XL + (v - LO) / (HI - LO) * (XR - XL)
s.line(XL, 150, XR, 150, "mp-axis")
for v in range(15, 66, 5):
    s.line(X(v), 146, X(v), 154, "mp-axis")
    s.text(X(v), 174, f"{v}", "mp-s", "middle")
seen = {}
for c in sorted(WAIT):
    k = seen.get(c, 0)
    seen[c] = k + 1
    circ(s, X(c), 132 - k * 15, 7, "var(--accent)" if c > 40 else "var(--tag-concept-dot)")
s.both(X(54), 104, "3 ออเดอร์ที่ช้ามาก", "3 very slow orders", "mp-acc", "middle")
s.both(XL, 72, "24 ออเดอร์ (นาที · จุดซ้อน = ค่าเท่ากัน)", "24 orders (minutes · stacked dots = same value)", "mp-s")
for row, (th, en, est, lo, hi, cls) in enumerate((("median", "median", 25, 23, 28, "mp-curve-b"),
                                                   ("percentile ที่ 75", "75th percentile", 29.25, 25.5, 40, "mp-curve"))):
    y = 226 + row * 74
    s.both(XL, y - 18, f"{th}: 95% CI {lo:g}–{hi:g} นาที", f"{en}: 95% CI {lo:g}–{hi:g} min", "mp-t")
    s.line(X(lo), y + 10, X(hi), y + 10, cls)
    s.line(X(lo), y, X(lo), y + 20, cls)
    s.line(X(hi), y, X(hi), y + 20, cls)
    circ(s, X(est), y + 10, 7, "var(--ink)")
s.both(XR, 296, "กว้างและเบ้ไปทางบน", "wide and lopsided", "mp-acc", "end")
s.save("l14-q75-ci.svg", 340)

# ================================================================ S15 the creators exercise (story only)
s = Svg(W, "The creators exercise: TikTok creator A's two clips got 10 and 12 thousand views, creator B's got 18 and 20. "
           "Pool the four view counts, then list every way to choose two of them as a fake creator A; the question marks "
           "are what the exercise asks for.")
s.bubble("ครีเอเตอร์ B ได้วิวมากกว่า A จริงไหม (พันวิวต่อคลิป)", "Does creator B really get more views than A? (thousand views per clip)")
for k, (name, vals, col) in enumerate((("A", (10, 12), BLUE), ("B", (18, 20), GOLD))):
    y = 96 + k * 70
    s.both(40, y + 30, f"ครีเอเตอร์ {name}", f"creator {name}", "mp-t")
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
s.both(550, 252, "ค่าสถิติ = วิวเฉลี่ย B − วิวเฉลี่ย A", "statistic = mean views of B − mean views of A", "mp-s", "middle")
s.save("l14-mad-exercise.svg", 268)

# ================================================================ S17 😭 in chats: a real difference
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
s = Svg(W, f"A real difference. Left: how often each person uses the crying-laughing emoji 😭, per 100 chat messages; 5 "
           f"Gen-Z friends (blue) 3.73, 1.85, 4.82, 1.49, 2.00, mean 2.78; 5 parents (amber) 0, 0, 0.36, 1.19, 0, mean 0.31 "
           f"(made-up numbers). Right: all 252 ways to split the 10 values "
           f"into 5 + 5; only {n_ext} split, the real one, reaches the real difference of +2.47, so p = 1/252 = 0.004.")
s.bubble("ถ้าความต่างเป็นของจริง permutation test เห็นอะไร", "When a difference is real, what does a permutation test see?")
s.panel(10, 70, 420, 300, "ml-cell", "😭 ต่อ 100 ข้อความ (คนละจุด)", "😭 per 100 messages (one dot = one person)", 1)
for k, (name, vals, col) in enumerate(((("Gen Z", "Gen Z"), HAM, BLUE), (("พ่อแม่", "parents"), MAD, GOLD))):
    x = 120 + k * 180
    for i, v in enumerate(vals):
        circ(s, x + (i - 2) * 14, 330 - v * 38, 8, col)
    m = sum(vals) / 5
    s.line(x - 50, 330 - m * 38, x + 50, 330 - m * 38, "mp-straight")
    s.text(x + 56, 330 - m * 38 + 5, f"{m:.2f}", "mp-n")
    s.both(x, 356, name[0], name[1], "mp-c", "middle")
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

# ================================================================ S18 a yes/no answer: who ends a chat with "."
from scipy import stats as _st  # noqa: E402

DOT_GENZ = np.array([1, 1, 0, 0, 0, 0, 0, 0, 0, 0])   # 1 = last message ends with "." (made up)
DOT_PAR = np.array([1, 1, 1, 1, 1, 1, 1, 1, 0, 0])
_res = _st.permutation_test((DOT_PAR, DOT_GENZ), lambda a, b: np.mean(a) - np.mean(b), alternative="greater",
                            permutation_type="independent", n_resamples=10_000, random_state=42)
_null = np.round(_res.null_distribution, 1)
_real = DOT_PAR.mean() - DOT_GENZ.mean()
_n_ext = int((_null >= _real - 1e-9).sum())
s = Svg(W, f"A yes/no answer. Left: the last chat message of 10 Gen-Z friends and 10 parents (made up); 2 of 10 Gen-Z "
           f"messages end with a full stop (20%), 8 of 10 parents' do (80%), a difference of +0.6. Right: 10,000 random "
           f"shuffles of the 20 people into two groups of 10; {_n_ext} of them reach +0.6 or more, so p = "
           f"{_res.pvalue:.2f}: parents really do end messages with a full stop more often.")
s.bubble("ถ้าคำตอบเป็น ใช่/ไม่ใช่ สลับป้ายได้ไหม", "Can we shuffle labels when the answer is yes/no?")
s.panel(10, 70, 420, 300, "ml-cell", "ข้อความล่าสุดลงท้ายด้วย “.” ไหม", "Does the last message end with “.”?", 1)
for k, (name, vals, col) in enumerate(((("Gen Z", "Gen Z"), DOT_GENZ, BLUE), (("พ่อแม่", "parents"), DOT_PAR, GOLD))):
    y = 150 + k * 104
    s.both(30, y - 12, name[0], name[1], "pl-label")
    for i, v in enumerate(vals):
        x = 30 + i * 38
        s.raw(f'<rect x="{x}" y="{y}" width="34" height="26" rx="10" style="fill:var(--card);stroke:{col if v else "var(--card-border)"};stroke-width:{2.2 if v else 1.2}"/>')
        s.text(x + 17, y + 18, "ok." if v else "ok", "mp-s", "middle")
    s.both(30, y + 52, f"{vals.sum()} จาก 10 = {vals.mean():.0%}", f"{vals.sum()} of 10 = {vals.mean():.0%}", "mp-n")
s.both(30, 352, "ใช่ = 1 ไม่ใช่ = 0 → ค่าเฉลี่ย = สัดส่วน", "yes = 1, no = 0 → the mean is the share", "pl-note")
s.panel(450, 70, 640, 300, "ml-cell", "สลับป้าย 20 คน 10,000 ครั้ง: พ่อแม่ − Gen Z", "Shuffle 20 people 10,000 times: parents − Gen Z", 2)
vals_ = np.round(np.arange(-0.8, 0.81, 0.2), 1)   # with a fixed number of "yes", the difference moves in steps of 0.2
cnt = [int((_null == v).sum()) for v in vals_]
mx = max(cnt)
bx = lambda i: 486 + i * 64
for i, (v, c) in enumerate(zip(vals_, cnt)):
    s.fill(bx(i), 330 - c / mx * 170, 52, max(c / mx * 170, 2), "var(--accent)" if v >= _real - 1e-9 else "var(--tag-concept-dot)", 2)
xr = bx(7) - 6
s.line(xr, 128, xr, 336, "mp-curve")
s.both(xr - 8, 124, f"ของจริง +0.6 ({_n_ext} จาก 10,000)", f"real +0.6 ({_n_ext} of 10,000)", "mp-acc", "end")
s.line(470, 330, 1062, 330, "mp-axis")
for i in (1, 4, 7):
    s.text(bx(i) + 26, 354, {1: "−0.6", 4: "0", 7: "+0.6"}[i], "mp-s", "middle")
s.text(1070, 354, f"p = {_res.pvalue:.2f} ✓", "ml-ok", "end")
s.save("l14-fullstop-permutation.svg", 380)


# ================================================================ S18 when to use a permutation test
def d_small(x, y, w, h):
    for i in range(3):
        circ(s, x + 40 + i * 22, y + 34, 7, BLUE)
        circ(s, x + 40 + i * 22, y + 58, 7, GOLD)


def d_skew(x, y, w, h):
    for i, hh in enumerate([62, 44, 30, 20, 13, 8, 5, 3]):
        s.fill(x + 30 + i * 20, y + 76 - hh, 16, hh, BLUE, 2)


def d_unknown(x, y, w, h):
    poly(s, [(x + 20 + i * 5, y + 74 - 50 * math.exp(-((i - 20) / 7) ** 2)) for i in range(41)], "mp-straight")
    s.text(x + w / 2, y + 48, "?", "mp-big", "middle")


def d_custom(x, y, w, h):
    s.both(x + w / 2, y + 36, "สัดส่วนคำอังกฤษ =", "English share =", "mp-c", "middle")
    s.both(x + w / 2, y + 64, "คำอังกฤษ ÷ คำทั้งหมด", "English ÷ all words", "mp-c", "middle")


s = Svg(W, "Four situations where a permutation test fits, numbered to match the cards: 1 small samples (3 clips per "
           "group), 2 skewed data (chat message length, use the median), 3 an unknown shape (story replies, mostly 0 with a "
           "few spikes), 4 a statistic you made up yourself (the share of English words in a Thai caption).")
term_grid(s, [
    (("① ตัวอย่างน้อย", "① Small sample"), d_small, "เช่น กลุ่มละ 3 คลิป", "e.g. 3 clips per group", "ไล่ครบทุกวิธีแบ่งได้", "list every split"),
    (("② ข้อมูลเบ้", "② Skewed data"), d_skew, "เช่น ความยาวข้อความแชท", "e.g. chat message length", "ใช้ median ได้เลย", "use the median directly"),
    (("③ ไม่รู้รูปร่าง", "③ Unknown shape"), d_unknown, "เช่น คนตอบสตอรี่ (0 เยอะ)", "e.g. story replies (many 0s)", "สลับป้ายแทนสูตร", "shuffle labels, no formula"),
    (("④ ค่าสถิติที่คิดเอง", "④ Your own statistic"), d_custom, "เช่น % คำอังกฤษในแคปชัน", "e.g. % English in captions", "ใช้ค่าอะไรก็ได้", "any statistic works"),
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

# ================================================================ S07 will the project finish on time? (infographic)
TASKS = [("A สแกนเอกสาร", "A scanning", 5, 15, "var(--tag-concept-dot)"),
         ("B ทำความสะอาด", "B cleaning", 3, 5, "var(--tag-example-dot)"),
         ("C กำกับข้อมูล", "C annotation", 10, 20, "var(--tag-exercise-dot)")]
RUNS = [(12.7, 4.8, 19.4), (9.4, 3.8, 19.5), (13.6, 4.2, 15.4), (12.0, 3.3, 12.5), (5.9, 4.1, 17.4)]  # default_rng(42), runs 1–5
s = Svg(W, "Will a 3-task project finish in 30 days? The plan with middle values, 10 + 4 + 15 = 29 days, looks on time. "
           "But each task has a range: A scanning 5–15 days, B cleaning 3–5, C annotation 10–20. Five simulated futures "
           "(the first 5 of 50,000): 36.9, 32.7 and 33.2 days are late; 27.8 and 27.4 are on time. Over 50,000 runs, 59% "
           "finish within 30 days; to be 90% sure, allow 34.5 days.")
s.bubble("3 งานทำต่อกัน ส่งทันใน 30 วันไหม", "3 tasks in a row: done within 30 days?")
X0, PXD = 250, 18                       # x of day 0, pixels per day
DX = lambda d: X0 + d * PXD


def stack(y, parts, h=26):
    x = X0
    for (_, _, _, _, col), d in zip(TASKS, parts):
        s.fill(x, y, d * PXD - 2, h, col, 4)
        if d * PXD > 40:
            s.text(x + d * PXD / 2, y + h / 2 + 6, f"{d:g}", "pl-num", "middle")
        x += d * PXD


# deadline
s.raw(f'<path d="M{DX(30)} 70 V472" style="stroke:var(--accent);stroke-width:3;stroke-dasharray:7 6"/>')
s.both(DX(30) + 6, 86, "กำหนดส่ง 30 วัน", "deadline: 30 days", "mp-acc")
# 1 the plan with middle values
s.both(20, 128, "แผนแบบค่ากลาง", "plan with middle values", "pl-label")
stack(108, (10, 4, 15))
s.both(DX(30) + 12, 128, "29 วัน ดูทัน?", "29 days: on time?", "pl-text")
# 2 the ranges
s.both(20, 176, "แต่ละงานกินเวลาไม่แน่นอน", "each task's time varies", "pl-label")
for k, (th, en, lo, hi, col) in enumerate(TASKS):
    y = 196 + k * 26
    s.both(X0 - 12, y + 14, th, en, "mp-s", "end")
    s.raw(f'<path d="M{DX(lo)} {y + 9} H{DX(hi)}" style="stroke:{col};stroke-width:10;stroke-linecap:round;opacity:.85"/>')
    s.text(DX(hi) + 12, y + 14, f"{lo}–{hi}", "mp-s")
# 3 possible futures
s.box(10, 286, 1080, 190, "nt-band-a", 14)
s.both(20, 314, "สุ่มอนาคตที่เป็นไปได้ (5 รอบแรกจาก 50,000)", "possible futures (the first 5 of 50,000 runs)", "pl-label")
for i, parts in enumerate(RUNS):
    y = 328 + i * 28
    s.both(X0 - 12, y + 17, f"รอบ {i + 1}", f"run {i + 1}", "mp-s", "end")
    stack(y, parts, 22)
    tot = sum(parts)
    late = tot > 30
    s.both(DX(tot) + 10, y + 17, f"{tot:.1f} วัน {'✗ ช้า' if late else '✓ ทัน'}", f"{tot:.1f} days {'✗ late' if late else '✓ on time'}",
           "ml-neg" if late else "ml-ok-small")
for d in (0, 10, 20, 30, 40):
    s.text(DX(d), 494, f"{d}", "mp-s", "middle")
s.both(DX(20), 516, "วัน", "days", "mp-s", "middle")
s.box(10, 530, 1080, 52, "rc-res", 12)
s.both(550, 563, "จาก 50,000 รอบ: เสร็จใน 30 วันแค่ 59%  ·  ถ้าอยากมั่นใจ 90% ต้องให้เวลา 34.5 วัน",
       "Over 50,000 runs: only 59% finish within 30 days  ·  to be 90% sure, allow 34.5 days", "pl-label", "middle")
s.save("l14-project-info.svg", 592)
