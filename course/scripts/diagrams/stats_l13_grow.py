"""Grow-the-tree frames for stats-dh lesson 13, card S10 (how deep should a tree grow?). One SVG per depth 0–6,
shown one at a time by a ```stepper with a Play button: the tree's questions in a row, each finished leaf hanging
under its question, the still-mixed leaf where the next question will go, and two small charts that draw up to the
current depth (entropy left in the leaves, train and test accuracy).

    python3 scripts/diagrams/stats_l13_grow.py courses/stats-dh/images

Real run in course/.venv, the same split as the lesson (obesity, 80/20 stratified, random_state=42; train 86 people:
Underweight 37, Normal 23, Overweight 16, Obese 10), DecisionTreeClassifier(max_depth=d, random_state=42):
  depth   leaves  train   test    entropy left (train, size-weighted over leaves)
  0       1       0.430   0.455   1.845   (no question: everyone is called Underweight, the largest group)
  1       2       0.698   0.727   0.859
  2       3       0.849   0.909   0.452
  3       4       0.965   1.000   0.139
  4       5       0.988   0.955   0.064
  5       6       0.988   0.955   0.042
  6       7       1.000   0.955   0.000
The tree is a chain: each depth adds one question on the still-mixed side.
"""

from stats_svg import CLS, NAMES, Svg, H  # noqa: F401

W = 1100
# question, which answer carries on, the leaf that answer-side ends in (counts Under, Normal, Over, Obese)
NODES = [
    ("BMI ≤ 20.6", "ไม่", "no", ("ใช่", "yes"), [37, 0, 0, 0]),
    ("BMI ≤ 24.6", "ไม่", "no", ("ใช่", "yes"), [0, 20, 0, 0]),
    ("Weight ≤ 97.5", "ใช่", "yes", ("ไม่", "no"), [0, 0, 0, 10]),
    ("Age ≤ 31.5", "ไม่", "no", ("ใช่", "yes"), [0, 2, 0, 0]),
    ("Weight ≤ 82.5", "ใช่", "yes", ("ไม่", "no"), [0, 0, 12, 0]),
    ("Weight ≤ 77.5", None, None, ("ใช่", "yes"), [0, 0, 4, 0]),
]
LAST_NO = [0, 1, 0, 0]  # node 6, "no" side
# the still-mixed leaf after depth d (where question d + 1 will go)
FRONT = [[37, 23, 16, 10], [0, 23, 16, 10], [0, 3, 16, 10], [0, 3, 16, 0], [0, 1, 16, 0], [0, 1, 4, 0]]
ENT = [1.845, 0.859, 0.452, 0.139, 0.064, 0.042, 0.0]
TRAIN = [0.430, 0.698, 0.849, 0.965, 0.988, 0.988, 1.000]
TEST = [0.455, 0.727, 0.909, 1.000, 0.955, 0.955, 0.955]

NW, NH = 156, 38           # question box
PX = 2.0                   # pixels per person in a leaf bar
BLUE, ORANGE = "var(--tag-concept-dot)", "var(--accent)"


def pos(k):
    """Centre of tree level k (question k, or the mixed leaf at depth k): a staircase down and to the right."""
    return 152 + k * 84, 32 + k * 60


def big(counts):
    k = max(range(4), key=lambda i: counts[i])
    return NAMES[k]


def leaf(s, cx, y, counts, mixed=False, new=False):
    """A leaf: a bar split by weight group (top at y), its size and class, and its entropy."""
    n = sum(counts)
    w = max(n * PX, 14)
    s.raw('<g class="grow-new">' if new else "<g>")
    if mixed:
        s.box(cx - w / 2 - 5, y - 4, w + 10, 30, "sw-warn-box", 6)
    s.stack(cx - w / 2, y, w, 22, counts)
    th, en = big(counts)
    h = H(counts)
    hs = f"H = {h:.2f}" if h else "H = 0 ✓"
    s.both(cx, y + 38, f"{n} คน → {th}", f"{n} → {en}", "mp-s", "middle")
    s.text(cx, y + 62, hs, "mp-acc" if mixed else "ml-ok-small", "middle")
    s.raw("</g>")


def edge(s, x1, y1, x2, y2, th, en):
    s.line(x1, y1, x2, y2)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    s.both(mx + (8 if x2 > x1 else -8), my, th, en, "mp-s", "start" if x2 > x1 else "end")


def chart(s, x, y, w, h, series, ymin, ymax, d, ticks, fmt):
    s.line(x, y + h, x + w, y + h, "mp-axis")
    s.line(x, y, x, y + h, "mp-axis")
    for t in ticks:
        ty = y + h - (t - ymin) / (ymax - ymin) * h
        s.line(x, ty, x + w, ty, "mp-guide")
        s.text(x - 8, ty + 5, fmt(t), "mp-s", "end")
    for k in range(7):
        s.text(x + k * w / 6, y + h + 20, str(k), "mp-s" if k != d else "mp-acc", "middle")
    for vals, col, dash, lab in series:
        pts = [(x + k * w / 6, y + h - (v - ymin) / (ymax - ymin) * h) for k, v in enumerate(vals)]
        ghost = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
        s.raw(f'<polyline points="{ghost}" style="fill:none;stroke:{col};stroke-width:2;opacity:.15"/>')
        if d > 0:
            done = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts[: d + 1])
            s.raw(f'<polyline points="{done}" style="fill:none;stroke:{col};stroke-width:3;'
                  f'stroke-dasharray:{dash}"/>')
        for k, (px, py) in enumerate(pts[: d + 1]):
            s.raw(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{6 if k == d else 4}" style="fill:{col}"/>')
        px, py = pts[d]
        others = [v[d] for v, *_ in series if v is not vals]
        above = not others or vals[d] >= max(others)
        right = px > x + w * 0.75            # near the right edge: write the value to the left of the point
        tx = px - 12 if right else px + 12
        ty = py - 10 if above else py + (22 if right else 8)
        s.raw(f'<text x="{tx:.1f}" y="{ty:.1f}" class="pl-label" text-anchor="{"end" if right else "start"}" '
              f'style="fill:{col}" lang="en">{fmt(vals[d])}</text>')


for d in range(7):
    s = Svg(W, f"Growing a decision tree, depth {d} of 6, on the 86 training people. Train accuracy {TRAIN[d]:.3f}, "
               f"test accuracy {TEST[d]:.3f}, entropy left in the leaves {ENT[d]:.2f} bits. "
               + ("No question yet: one mixed leaf of 86 people." if d == 0 else
                  f"Questions so far: {', '.join(q for q, *_ in NODES[:d])}."))
    # the tree, top-down: question k at level k; its finished leaf branches down-left, the rest carries on down-right
    for k, (q, cth, cen, br, lv) in enumerate(NODES):
        cx, cy = pos(k)
        if k < d:
            new = k == d - 1
            nx, ny = pos(k + 1)
            if k < 5:
                edge(s, cx + 20, cy + NH / 2, nx - 10, ny - NH / 2 + 2, cth, cen)
                edge(s, cx - 20, cy + NH / 2, cx - 74, ny - 8, br[0], br[1])
                leaf(s, cx - 74, ny - 6, lv, new=new)
            else:
                edge(s, cx - 20, cy + NH / 2, cx - 74, ny - 8, br[0], br[1])
                edge(s, cx + 20, cy + NH / 2, cx + 74, ny - 8, "ไม่", "no")
                leaf(s, cx - 74, ny - 6, lv, new=new)
                leaf(s, cx + 74, ny - 6, LAST_NO, new=new)
            s.raw('<g class="grow-new">' if new else "<g>")
            s.box(cx - NW / 2, cy - NH / 2, NW, NH, "ml-model", NH / 2)
            s.text(cx, cy + 6, q + "?", "ml-model-text", "middle")
            s.raw("</g>")
        elif k == d:
            w = sum(FRONT[d]) * PX
            leaf(s, cx, cy - 12, FRONT[d], mixed=True, new=d > 0)
            if d == 5:   # no room on the right next to the charts: say it under the leaf
                s.both(cx, cy + 76, "ยังปน → ถามต่อ", "still mixed → ask more", "mp-acc", "middle")
            else:
                s.both(cx + w / 2 + 14, cy + 6, "ยังปน → ถามต่อ", "still mixed → ask more", "mp-acc")
        else:
            s.raw('<g style="opacity:.22">')
            s.box(cx - NW / 2, cy - NH / 2, NW, NH, "ml-cell", NH / 2)
            s.text(cx, cy + 6, q + "?", "mp-s", "middle")
            s.raw("</g>")

    # the two charts on the right, drawn up to depth d
    s.box(716, 8, 376, 452, "ml-cell", 14)
    s.both(736, 38, "entropy ที่เหลือในใบ (bits) ↓", "entropy left in the leaves (bits) ↓", "pl-label")
    chart(s, 782, 66, 280, 110, [(ENT, BLUE, "none", "train")], 0, 2, d, [0, 1, 2], lambda v: f"{v:.2f}" if v % 1 else f"{v:.0f}")
    s.both(736, 246, "accuracy", "accuracy", "pl-label")
    s.fill(850, 234, 14, 14, BLUE, 3)
    s.both(870, 246, "train", "train", "pl-note")
    s.fill(930, 234, 14, 14, ORANGE, 3)
    s.both(950, 246, "test (คนใหม่)", "test (new)", "pl-note")
    chart(s, 782, 296, 280, 104, [(TRAIN, BLUE, "none", "train"), (TEST, ORANGE, "7 5", "test")], 0.4, 1.0, d,
          [0.4, 0.7, 1.0], lambda v: f"{v:.2f}")
    s.both(922, 446, "ความลึกของต้นไม้", "tree depth", "mp-s", "middle")
    s.save(f"l13-grow-{d}.svg", 468)
