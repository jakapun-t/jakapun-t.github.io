"""Gradient boosting, step by step, for stats-dh lesson 13 card S13. Three SVG frames shown by a ```stepper with Play:
0 every ball at the mean · 1 add tree 1 · 2 add tree 2.
Each frame: one golf row per person (A–D) on a weight track: a flag at the true weight, the ball at the current
guess, each tree's shot drawn as an arc; the round's tree rule in words; the total squared error so far.

    python3 scripts/diagrams/stats_l13_boost.py courses/stats-dh/images

Numbers (the lesson's code cell, DecisionTreeRegressor(max_depth=1), learning rate 1):
  heights 160, 175, 180, 190; weights 60, 80, 90, 100; mean 82.5 → residuals −22.5, −2.5, 7.5, 17.5, error 875
  tree 1: height ≤ 167.5 → −22.5, else +7.5 (mean of −2.5, 7.5, 17.5) → guess 60, 90, 90, 90, error 200
  tree 2 on residuals 0, −10, 0, 10: height ≤ 185 → −3.3 (mean of 0, −10, 0), else +10 → 56.7, 86.7, 86.7, 100, error 66.7
"""

from stats_svg import Svg

W = 1180
HT = [160, 175, 180, 190]
WT = [60, 80, 90, 100]
PEOPLE = ["A", "B", "C", "D"]
BLUE, ORANGE, GREEN = "var(--tag-concept-dot)", "var(--accent)", "var(--tag-exercise-dot)"
# guess as a step function: (upper bound of the height range, guessed weight)
ERR = [875, 200, 66.7]
# each person's guess after 0, 1, 2 trees, and the shot each tree adds
GUESSES = [[82.5] * 4, [60, 90, 90, 90], [56.7, 86.7, 86.7, 100]]
RULES = [None,
         ("ต้นที่ 1: ส่วนสูง ≤ 167.5?", "Tree 1: height ≤ 167.5?", "−22.5", "+7.5",
          ("ใช่ (A): ขาด −22.5", "yes (A): gap −22.5"),
          ("ไม่ (B, C, D): (−2.5 + 7.5 + 17.5) ÷ 3 = +7.5", "no (B, C, D): (−2.5 + 7.5 + 17.5) ÷ 3 = +7.5")),
         ("ต้นที่ 2: ส่วนสูง ≤ 185?", "Tree 2: height ≤ 185?", "−3.3", "+10",
          ("ใช่ (A, B, C): (0 − 10 + 0) ÷ 3 = −3.3", "yes (A, B, C): (0 − 10 + 0) ÷ 3 = −3.3"),
          ("ไม่ (D): ขาด +10", "no (D): gap +10"))]
SHOT_COL = [None, BLUE, ORANGE]
ROW_Y = [140, 214, 288, 362]


def gx(kg):
    return 220 + (kg - 50) / 55 * 540


def fmt(v):
    return f"{v:+.1f}".replace("-", "−").replace(".0", "")


for f in range(3):
    s = Svg(W, f"Gradient boosting as golf, one row per person, step {f + 1} of 3. Each row is a weight track with a "
               f"flag at the person's true weight (A 60, B 80, C 90, D 100 kg). Every ball starts at the mean, 82.5. "
               + ("" if f == 0 else f"Tree {f} moves every ball: " + ", ".join(
                   f"{PEOPLE[k]} {fmt(GUESSES[f][k] - GUESSES[f - 1][k])}" for k in range(4)) + ". ")
               + "Still missing: " + ", ".join(f"{PEOPLE[k]} {fmt(WT[k] - GUESSES[f][k])}" for k in range(4))
               + f". Total squared error {ERR[f]:g}.")
    s.box(10, 8, 840, 420, "ml-cell", 14)
    head = [("เริ่ม: ทุกลูกอยู่ที่ 82.5 กก. (ค่าเฉลี่ย)", "Start: every ball at 82.5 kg (the mean)"),
            ("บวกต้นที่ 1: ทุกลูกขยับเข้าหาธง", "Add tree 1: every ball moves toward its flag"),
            ("บวกต้นที่ 2: ขยับอีกนิด เข้าใกล้ธงกว่าเดิม", "Add tree 2: a smaller move, closer still")][f]
    s.both(30, 40, head[0], head[1], "pl-label")
    # legend
    s.raw(f'<circle cx="38" cy="62" r="7" style="fill:#fff;stroke:var(--ink-2);stroke-width:2.5"/>')
    s.both(52, 68, "ค่าที่ทาย", "the guess", "mp-s")
    s.raw('<path d="M160 70 V54 l12 4 l-12 4" style="fill:var(--accent);stroke:var(--ink-2);stroke-width:2"/>')
    s.both(180, 68, "น้ำหนักจริง (เป้า)", "true weight (target)", "mp-s")
    if f:
        s.raw(f'<path d="M340 66 q14 -14 28 0" style="fill:none;stroke:{BLUE};stroke-width:3"/>')
        s.both(376, 68, "ต้นที่ 1", "tree 1", "mp-s")
    if f == 2:
        s.raw(f'<path d="M448 66 q14 -14 28 0" style="fill:none;stroke:{ORANGE};stroke-width:3"/>')
        s.both(484, 68, "ต้นที่ 2", "tree 2", "mp-s")
    s.both(800, 68, "ยังขาด", "still missing", "mp-s", "end")
    # weight ticks
    for kg in (60, 80, 100):
        s.raw(f'<path d="M{gx(kg):.1f} 88 V386" style="stroke:var(--card-border);stroke-width:1.2;stroke-dasharray:4 4"/>')
        s.text(gx(kg), 404, f"{kg}", "mp-s", "middle")
    s.both(gx(77.5), 422, "น้ำหนัก (กก.)", "weight (kg)", "mp-s", "middle")
    for k in range(4):
        y = ROW_Y[k]
        s.text(30, y + 6, PEOPLE[k], "mp-big")
        s.both(62, y + 6, f"{HT[k]} ซม.", f"{HT[k]} cm", "mp-s")
        s.raw(f'<path d="M{gx(52):.1f} {y} H{gx(104):.1f}" style="stroke:var(--tag-exercise-dot);stroke-width:4;stroke-linecap:round;opacity:.55"/>')
        # flag at the true weight
        fx = gx(WT[k])
        s.raw(f'<path d="M{fx:.1f} {y} V{y - 34} l16 5 l-16 5" style="fill:var(--accent);stroke:var(--ink-2);stroke-width:2"/>')
        s.text(fx + 4, y + 22, f"{WT[k]}", "mp-s", "middle")
        # the shots so far
        for t in range(1, f + 1):
            a0, a1 = GUESSES[t - 1][k], GUESSES[t][k]
            x0, x1 = gx(a0), gx(a1)
            lift = max(10, min(22, abs(x1 - x0) * 0.25))
            new = t == f
            arc = (f'<path d="M{x0:.1f} {y - 6} Q{(x0 + x1) / 2:.1f} {y - 6 - 2 * lift:.1f} {x1:.1f} {y - 6}" '
                   f'style="fill:none;stroke:{SHOT_COL[t]};stroke-width:3"/>')
            if new:   # only this round's shot is labelled, high enough to clear the flags
                lab = (f'<text x="{(x0 + x1) / 2:.1f}" y="{min(y - 12 - lift, y - 44):.1f}" class="pl-label" '
                       f'text-anchor="middle" style="fill:{SHOT_COL[t]}" lang="en">{fmt(a1 - a0)}</text>')
                s.raw(f'<g class="grow-new">{arc}{lab}</g>')
            else:
                s.raw(f'<g style="opacity:.45">{arc}</g>')
        # the ball now
        s.raw(f'<circle cx="{gx(GUESSES[f][k]):.1f}" cy="{y}" r="8" style="fill:#fff;stroke:var(--ink-2);stroke-width:2.5"/>')
        gap = round(WT[k] - GUESSES[f][k], 1)
        s.text(800, y + 6, "0 ✓" if abs(gap) < 0.05 else fmt(gap), "ml-ok" if abs(gap) < 0.05 else "pl-label", "end")

    # right: this round's tree, in words, and the total error
    s.box(864, 8, 306, 420, "nt-band-a", 14)
    if f == 0:
        s.both(884, 40, "ยังไม่มีต้นไม้", "no tree yet", "pl-label")
        s.both(884, 76, "ทุกคนได้ 82.5", "everyone gets 82.5", "pl-text")
        s.both(884, 104, "(ค่าเฉลี่ยของน้ำหนัก)", "(the mean weight)", "pl-note")
        s.both(884, 150, "ต้นถัดไปเรียน \"ยังขาด\"", "the next tree learns", "pl-text")
        s.both(884, 178, "ไม่ได้เรียนน้ำหนัก", "\"still missing\", not weight", "pl-text")
    else:
        qth, qen, lv, rv, (lth, len_), (rth, ren) = RULES[f]
        s.both(884, 40, "กฎของต้นนี้", "this tree's rule", "pl-note")
        s.box(884, 52, 266, 38, "ml-model", 19)
        s.both(1017, 77, qth, qen, "ml-model-text", "middle")
        s.both(900, 122, "ใช่ →", "yes →", "pl-text")
        s.text(970, 122, lv, "mp-big")
        s.both(1040, 122, "ไม่ →", "no →", "pl-text")
        s.text(1100, 122, rv, "mp-big")
        s.both(884, 160, "ตัวเลข = ค่า \"ยังขาด\" เฉลี่ยของฝั่งนั้น", "number = average \"still missing\" on that side", "mp-s")
        s.both(884, 184, lth, len_, "mp-s")
        s.both(884, 206, rth, ren, "mp-s")
    s.both(884, 246, "ผิดรวม (squared error)", "total error (squared)", "pl-note")
    for k, e in enumerate(ERR):
        bx = 900 + k * 86
        hgt = e / 875 * 110
        on = k <= f
        s.fill(bx, 390 - hgt, 56, hgt, ORANGE if on else "var(--card-border)", 4)
        if on:
            s.text(bx + 28, 382 - hgt, f"{e:g}", "pl-label", "middle")
        s.both(bx + 28, 410, ["เริ่ม", "+ต้น 1", "+ต้น 2"][k], ["start", "+tree 1", "+tree 2"][k], "mp-s", "middle")
    s.save(f"l13-boost-{f}.svg", 436)


# ================================================================ the golf analogy, on person D: each shot aims at what is left
def mx(kg):
    return 70 + kg * 8.6


s = Svg(W, "The golf analogy on person D (190 cm, true weight 100 kg, the flag). Shot 1 is the start guess, the mean: "
           "82.5 kg, still 17.5 short. Shot 2 is tree 1: +7.5, to 90, still 10 short. Shot 3 is tree 2: +10, to 100, in "
           "the hole. D's guess = 82.5 + 7.5 + 10 = 100 = start + tree 1 + tree 2.")
s.bubble("ตีกอล์ฟให้ D: สูง 190 ซม. น้ำหนักจริง 100 กก. (ธง) ทายทีละช็อต", "Golf for D: 190 cm, true weight 100 kg (the flag), one shot at a time")
GROUND = 226
s.raw(f'<path d="M40 {GROUND} H1140" style="stroke:var(--tag-exercise-dot);stroke-width:6;stroke-linecap:round"/>')
s.raw(f'<path d="M{mx(0) - 6} {GROUND - 3} h12 l-4 -10 h-4 Z" style="fill:var(--muted)"/>')
s.text(mx(0), GROUND + 26, "0", "mp-s", "middle")
s.raw(f'<ellipse cx="{mx(100)}" cy="{GROUND + 1}" rx="14" ry="5" style="fill:var(--ink)"/>'
      f'<path d="M{mx(100)} {GROUND} V{GROUND - 92}" style="stroke:var(--ink-2);stroke-width:3"/>'
      f'<path d="M{mx(100)} {GROUND - 92} l40 12 l-40 12 Z" style="fill:var(--accent)"/>')
SHOTS = [(0, 82.5, "var(--tag-concept-dot)", 120, "①"), (82.5, 90, "var(--tag-example-dot)", 26, "②"),
         (90, 100, "var(--accent)", 30, "③")]
for a0, a1, col, h, mark in SHOTS:
    x1, x2 = mx(a0), mx(a1)
    s.raw(f'<path d="M{x1:.1f} {GROUND - 6} Q{(x1 + x2) / 2:.1f} {GROUND - 6 - 2 * h:.1f} {x2:.1f} {GROUND - 6}" '
          f'style="fill:none;stroke:{col};stroke-width:4;stroke-dasharray:2 9;stroke-linecap:round"/>')
    s.raw(f'<circle cx="{x2:.1f}" cy="{GROUND - 7}" r="8" style="fill:#fff;stroke:{col};stroke-width:3"/>')
    s.text((x1 + x2) / 2, GROUND - 6 - h - 10, mark, "pl-label", "middle")
for kg in (82.5, 90, 100):
    s.text(mx(kg), GROUND + 26, f"{kg:g}", "mp-s", "middle")
s.both(mx(50), GROUND + 26, "น้ำหนัก (กก.) →", "weight (kg) →", "mp-s", "middle")
for y, a0, left in ((GROUND + 52, 82.5, 17.5), (GROUND + 80, 90, 10)):
    s.raw(f'<path d="M{mx(a0):.1f} {y} H{mx(100):.1f} M{mx(a0):.1f} {y - 6} v12 M{mx(100):.1f} {y - 6} v12" '
          f'style="stroke:var(--accent);stroke-width:2"/>')
    s.both(mx(a0) - 10, y + 5, f"ยังขาด {left:g}", f"{left:g} still missing", "mp-acc", "end")
s.box(20, GROUND + 100, 1140, 50, "nt-band-a", 12)
s.both(590, GROUND + 132, "น้ำหนักที่ทายของ D = ① ค่าเริ่ม 82.5 + ② ต้นที่ 1 (+7.5) + ③ ต้นที่ 2 (+10) = 100 ✓",
       "D's guess = ① start 82.5 + ② tree 1 (+7.5) + ③ tree 2 (+10) = 100 ✓", "pl-label", "middle")
s.save("l13-golf.svg", GROUND + 160)


# ================================================================ the chain: each tree trains on the residuals the last one left
def mini(s, x, y, w, h, vals, lo, hi, fit=None, zero=False, show=False):
    """A small plot of A–D: height across, a value up; optional fitted step line; show=True writes each value."""
    s.box(x, y, w, h, "ml-cell", 8)
    px = lambda k: x + 22 + k * (w - 44) / 3
    py = lambda v: y + h - 12 - (v - lo) / (hi - lo) * (h - 40)
    if zero:
        s.raw(f'<path d="M{x + 8} {py(0):.1f} H{x + w - 8}" style="stroke:var(--card-border);stroke-width:1.5;stroke-dasharray:4 4"/>')
    if fit is not None:
        d = []
        for k, v in enumerate(fit):
            a = x + 8 if k == 0 else (px(k - 1) + px(k)) / 2
            b = x + w - 8 if k == 3 else (px(k) + px(k + 1)) / 2
            d.append(f"{'M' if k == 0 else 'L'}{a:.1f} {py(v):.1f} L{b:.1f} {py(v):.1f}")
        s.raw(f'<path d="{" ".join(d)}" style="fill:none;stroke:{ORANGE};stroke-width:3"/>')
    for k, v in enumerate(vals):
        s.raw(f'<circle cx="{px(k):.1f}" cy="{py(v):.1f}" r="6" style="fill:{BLUE}"/>')
        if show:
            s.text(px(k), py(v) - 11, f"{PEOPLE[k]} {v:g}".replace("-", "−"), "mp-s", "middle")


s = Svg(W, "Gradient boosting as a chain, with the 4 people. Start: the data (height, weight) is predicted by the mean, "
           "82.5; what is left is r1 = weight − 82.5 = −22.5, −2.5, 7.5, 17.5. Tree 1 trains on (height, r1) and "
           "predicts −22.5 or +7.5; r2 = r1 − tree 1 = 0, −10, 0, 10. Tree 2 trains on (height, r2) and predicts −3.3 or "
           "+10; r3 = 3.3, −6.7, 3.3, 0. … Tree N trains on what is still left. The guess = 82.5 + tree 1 + tree 2 + … + tree N.")
s.raw('<g transform="translate(0 52)">')
COLS = [  # centre x, model name (th, en), data label, data values, fit, residual formula, residual values
    (140, ("เริ่ม: ค่าเฉลี่ย", "Start: the mean"), "(ส่วนสูง, น้ำหนัก)", "(height, weight)", [60, 80, 90, 100], (55, 105), False,
     [82.5] * 4, "r₁ = น้ำหนัก − 82.5", "r₁ = weight − 82.5", "−22.5, −2.5, 7.5, 17.5", ("82.5 ทุกคน", "82.5 for all")),
    (430, ("ต้นที่ 1: สูง ≤ 167.5?", "Tree 1: height ≤ 167.5?"), "(ส่วนสูง, r₁)", "(height, r₁)", [-22.5, -2.5, 7.5, 17.5], (-25, 20), True,
     [-22.5, 7.5, 7.5, 7.5], "r₂ = r₁ − ต้นที่ 1", "r₂ = r₁ − tree 1", "0, −10, 0, 10", ("−22.5 หรือ +7.5", "−22.5 or +7.5")),
    (720, ("ต้นที่ 2: สูง ≤ 185?", "Tree 2: height ≤ 185?"), "(ส่วนสูง, r₂)", "(height, r₂)", [0, -10, 0, 10], (-25, 20), True,
     [-3.3, -3.3, -3.3, 10], "r₃ = r₂ − ต้นที่ 2", "r₃ = r₂ − tree 2", "3.3, −6.7, 3.3, 0", ("−3.3 หรือ +10", "−3.3 or +10")),
]
BW = 230
for i, (cx, (mth, men), dth, den, vals, (lo, hi), zero, fit, rth, ren, rv, (pth, pen)) in enumerate(COLS):
    # bottom: the data this model trains on, each value written
    mini(s, cx - BW / 2, 352, BW, 92, vals, lo, hi, zero=zero, show=True)
    s.both(cx, 470, dth, den, "pl-label", "middle")
    s.arrow(cx, 352, cx, 300)
    s.both(cx - 12, 334, "ฝึก", "train", "mp-acc", "end")
    # middle: the model
    s.box(cx - BW / 2, 252, BW, 46, "ml-model", 10)
    s.both(cx, 281, mth, men, "ml-model-text", "middle")
    s.arrow(cx, 252, cx, 202)
    s.both(cx - 12, 234, "ทาย", "predict", "mp-s", "end")
    s.both(cx + 12, 234, pth, pen, "mp-acc")
    # top: its prediction over the same points
    mini(s, cx - BW / 2, 108, BW, 92, vals, lo, hi, fit=fit, zero=zero)
    s.arrow(cx, 108, cx, 84)
    s.both(cx, 50, rth, ren, "pl-label", "middle")
    s.text(cx, 74, rv, "mp-acc", "middle")
    # what is left becomes the next column's data
    nx = COLS[i + 1][0] if i + 1 < len(COLS) else 1040
    if i + 1 < len(COLS):
        s.raw(f'<path d="M{cx + 95} 44 H{nx - BW / 2 - 18} V398 H{nx - BW / 2 - 4}" style="fill:none;stroke:var(--ink-2);stroke-width:2"/>'
              f'<path d="M{nx - BW / 2 - 12} 392 L{nx - BW / 2 - 2} 398 L{nx - BW / 2 - 12} 404 Z" style="fill:var(--ink-2)"/>')
# … and tree N
for y in (130, 275, 398):
    s.raw(f'<path d="M868 {y} H912" style="stroke:var(--muted);stroke-width:2;stroke-dasharray:6 6"/>')
s.box(930, 252, 220, 46, "ml-model", 10)
s.both(1040, 281, "ต้นที่ N", "Tree N", "ml-model-text", "middle")
s.box(930, 352, 220, 92, "ml-cell", 8)
s.both(1040, 392, "ส่วนที่ยังเหลือ", "what is still left", "mp-s", "middle")
s.both(1040, 416, "เล็กลงทุกรอบ", "smaller every round", "mp-s", "middle")
s.both(1040, 470, "(ส่วนสูง, rₙ)", "(height, rₙ)", "pl-label", "middle")
s.box(930, 108, 220, 92, "ml-cell", 8)
s.both(1040, 160, "r เกือบ 0", "r almost 0", "ml-ok-small", "middle")
s.box(20, 490, 1140, 46, "nt-band-a", 12)
s.both(590, 520, "ค่าที่ทาย = 82.5 + ต้นที่ 1 + ต้นที่ 2 + … + ต้นที่ N   (ผิดรวม 875 → 200 → 66.7 → …)",
       "guess = 82.5 + tree 1 + tree 2 + … + tree N   (total error 875 → 200 → 66.7 → …)", "pl-label", "middle")
s.raw("</g>")
s.box(20, 6, 1140, 42, "nt-bubble", 21)
s.both(590, 34, "เป้าหมาย: ทายน้ำหนัก (กก.) จากส่วนสูง · A 160 ซม. 60 กก. · B 175 ซม. 80 กก. · C 180 ซม. 90 กก. · D 190 ซม. 100 กก.",
       "Goal: predict weight (kg) from height · A 160 cm 60 kg · B 175 cm 80 kg · C 180 cm 90 kg · D 190 cm 100 kg", "pl-text", "middle")
s.save("l13-boost-chain.svg", 598)
