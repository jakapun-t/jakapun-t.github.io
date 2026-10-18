"""Concept pictures for nlp-basic lesson 11 (data visualization), in the style of nlp l12-why-chunk.svg: the
running example's question on top, drawn objects, arrows at the exact spot, the real numbers attached to what they
describe. ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/basic_l11_concepts.py courses/nlp-basic/images

Every value is from data/airline_reviews.csv, checked in course/.venv: seat-type counts (Economy 140, Premium
Economy 12, Business 28, First 4), the ranges and medians of the numeric columns, and the ticket-price box plot
per seat type (seaborn's 1.5 × IQR whiskers). The S14 picture shows the exercise's columns and chart names only;
its answers stay behind Show answer.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from basic_svg import Svg, width  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
W = 1180


def svg(title):
    return Svg(OUT, W, title)


def bins_icon(s, cx, cy):
    for k in range(3):
        s.box(cx - 22 + k * 16, cy - 8, 12, 12, ["ml-bar-top", "ml-bar", "ml-model"][k], 3)


def ruler_icon(s, cx, cy):
    s.path(f"M{cx - 22} {cy + 4} H{cx + 22}", "dg-rule-strong")
    for k in range(5):
        s.path(f"M{cx - 22 + k * 11} {cy - 1} V{cy + 9}", "dg-rule-strong")
    s.raw(f'<circle cx="{cx + 6}" cy="{cy - 8}" r="6" class="pl-dot"/>')


def clock_icon(s, cx, cy):
    s.raw(f'<circle cx="{cx}" cy="{cy}" r="13" class="ml-cell"/>')
    s.path(f"M{cx} {cy} V{cy - 8} M{cx} {cy} H{cx + 7}", "pl-line")


def chart_icon(s, kind, x, y, w=150, h=84):
    """A small generic chart shape (not data) inside a frame at (x, y)."""
    s.box(x, y, w, h, "ml-cell", 8)
    bx, by, bw, bh = x + 14, y + 10, w - 28, h - 22
    s.path(f"M{bx} {by} V{by + bh} H{bx + bw}", "dg-rule-strong")
    if kind in ("count", "bar"):
        for k, v in enumerate([0.9, 0.35, 0.6, 0.2] if kind == "count" else [0.55, 0.7, 0.62, 0.8]):
            s.box(bx + 8 + k * (bw - 8) / 4, by + bh - v * bh, (bw - 8) / 4 - 8, v * bh, "ml-bar", 2)
        if kind == "bar":
            for k, v in enumerate([0.55, 0.7, 0.62, 0.8]):
                cx = bx + 8 + k * (bw - 8) / 4 + ((bw - 8) / 4 - 8) / 2
                s.path(f"M{cx} {by + bh - v * bh - 8} V{by + bh - v * bh + 6}", "dg-rule-strong")
    elif kind == "hist":
        for k, v in enumerate([0.2, 0.55, 0.9, 0.7, 0.4, 0.2, 0.1]):
            s.box(bx + 4 + k * (bw - 8) / 7, by + bh - v * bh, (bw - 8) / 7, v * bh, "ml-bar", 0)
    elif kind == "box":
        for k, (lo, q1, md, q3, hi) in enumerate([(0.1, 0.3, 0.42, 0.55, 0.8), (0.2, 0.45, 0.6, 0.75, 0.95)]):
            cx = bx + bw * (0.3 + k * 0.4)
            s.path(f"M{cx} {by + bh * (1 - hi)} V{by + bh * (1 - lo)}", "dg-rule-strong")
            s.box(cx - 14, by + bh * (1 - q3), 28, bh * (q3 - q1), "ml-cell-b", 2)
            s.path(f"M{cx - 14} {by + bh * (1 - md)} H{cx + 14}", "dg-rule-strong")
    elif kind == "scatter":
        for px, py in [(0.1, 0.2), (0.2, 0.35), (0.3, 0.3), (0.42, 0.5), (0.5, 0.45), (0.6, 0.62), (0.7, 0.58), (0.82, 0.8), (0.9, 0.72)]:
            s.raw(f'<circle cx="{bx + px * bw:.1f}" cy="{by + bh * (1 - py):.1f}" r="4" class="pl-dot"/>')
    elif kind == "line":
        pts = [(0.05, 0.3), (0.25, 0.5), (0.45, 0.42), (0.65, 0.7), (0.85, 0.62), (0.97, 0.85)]
        s.path("M" + " L".join(f"{bx + px * bw:.1f} {by + bh * (1 - py):.1f}" for px, py in pts), "pl-line")


# ================================================================ S02: the columns of this lesson by kind
s = svg("What kind is each column? Categorical: Airline Name (10 airlines), Seat Type (ordered Economy < Premium Economy < "
        "Business < First), Trip Type (5 kinds), Recommended (True / False): count per group with a count plot or bar plot. "
        "Numeric, with range and median: Rating 1 to 10 (median 6.5), Ticket Price 43.63 to 3,248.58 USD (median 268.95), "
        "Flight Duration 0.9 to 14.4 hours (median 2.45), Delay Minutes 0 to 217 (median 19): their spread, with a histogram "
        "or box plot. Time: Date Flown from 2019-02-21 to 2026-09-26: change over time, with a line chart.")
s.bubble(W / 2, 8, "แต่ละคอลัมน์เป็นข้อมูลชนิดไหน", "What kind is each column?", 420)
# categorical
s.box(20, 70, 470, 420, "nt-band-b", 14)
bins_icon(s, 62, 102)
s.text(94, 108, "Categorical", "pl-label")
s.both(218, 108, "ค่าเป็นกลุ่ม", "values are groups", "pl-note")
CATS = [("Airline Name", "10 สายการบิน: Garuda Indonesia, VietJet Air, …", "10 airlines: Garuda Indonesia, VietJet Air, …"),
        ("Seat Type", "ordinal: กลุ่มที่มีลำดับ", "ordinal: ordered groups"),
        ("Trip Type", "5 แบบ: Solo Travel, Couple Leisure, …", "5 kinds: Solo Travel, Couple Leisure, …"),
        ("Recommended", "True / False", "True / False")]
for k, (col, th, en) in enumerate(CATS):
    y = 146 + k * 78
    s.box(40, y - 22, 190, 34, "nt-out", 8)
    s.text(135, y + 1, col, "ml-box-h", "middle")
    s.both(40, y + 40, th, en, "pl-note")
    if col == "Seat Type":
        for j, lab in enumerate(["Econ.", "Prem.", "Bus.", "First"]):
            s.box(246 + j * 58, y + 6 - 8 - j * 8, 50, 8 + j * 8, "ml-bar", 2)
            s.text(271 + j * 58, y + 24, lab, "ml-i", "middle")
s.both(40, 470, "→ นับต่อกลุ่ม: countplot, barplot", "→ count or compare groups: count plot, bar plot", "ml-ok")
# numeric
s.box(510, 70, 400, 420, "nt-band-a", 14)
ruler_icon(s, 540, 104)
s.text(574, 108, "Numeric", "pl-label")
s.both(672, 108, "คำนวณได้", "you can calculate", "pl-note")
NUMS = [("Rating", 1, 10, 6.5, "1", "10", "6.5"), ("Ticket Price (USD)", 43.63, 3248.58, 268.95, "43.63", "3,248.58", "268.95"),
        ("Flight Duration (hours)", 0.9, 14.4, 2.45, "0.9", "14.4", "2.45"), ("Delay Minutes", 0, 217, 19, "0", "217", "19")]
for k, (col, lo, hi, med, slo, shi, smed) in enumerate(NUMS):
    y = 150 + k * 78
    s.text(530, y, col, "ml-box-h")
    x0, x1 = 548, 858
    s.path(f"M{x0} {y + 24} H{x1}", "dg-rule-strong")
    s.path(f"M{x0} {y + 18} V{y + 30} M{x1} {y + 18} V{y + 30}", "dg-rule-strong")
    xm = x0 + (med - lo) / (hi - lo) * (x1 - x0)
    s.raw(f'<circle cx="{xm:.1f}" cy="{y + 24}" r="7" class="pl-dot"/>')
    s.text(x0, y + 50, slo, "pl-note", "middle")
    s.text(x1, y + 50, shi, "pl-note", "middle")
    s.text(xm if xm > x0 + 90 else xm + 70, y + 50, f"median {smed}", "pl-note", "middle")
s.both(530, 470, "→ การกระจาย: histogram, box plot", "→ how it spreads: histogram, box plot", "ml-ok")
# time
s.box(930, 70, 230, 420, "rc-res", 14)
clock_icon(s, 960, 102)
s.text(990, 108, "Time", "pl-label")
s.text(950, 150, "Date Flown", "ml-box-h")
s.path("M1000 176 V420", "dg-rule-strong")
for k, yr in enumerate(range(2019, 2027)):
    y = 180 + k * 33
    s.path(f"M994 {y} H1006", "dg-rule-strong")
    s.text(1016, y + 6, str(yr), "pl-note")
s.text(950, 446, "2019-02-21 … 2026-09-26", "dg-code")
s.both(950, 470, "→ ตามเวลา: line chart", "→ over time: line chart", "ml-ok")
s.save("l11-column-kinds.svg", 506)


# ================================================================ S04: clicking vs code, on the same chart
COUNTS = [("Economy", 140), ("Premium Economy", 12), ("Business", 28), ("First", 4)]
s = svg("Reviews per seat type, and next month the data changes. Clicking (Excel, Tableau, Looker Studio): select the column, "
        "Insert, Chart, Bar; with new data you click every step again; good for one quick chart or a dashboard. Code "
        "(matplotlib, seaborn, plotly): 1 sns.countplot draws the bars from the table (Economy 140, Premium Economy 12, "
        "Business 28, First 4), 2 plt.title adds the title, 3 plt.show shows the chart; with new data you run the same code again.")
s.bubble(W / 2, 8, "จำนวนรีวิวต่อชั้นที่นั่ง แล้วเดือนหน้าข้อมูลเปลี่ยน", "Reviews per seat type, and next month the data changes", 600)
# clicking
s.box(20, 70, 560, 450, "sw-warn-box", 14)
s.both(40, 102, "✗ คลิกและลาก (Excel, Tableau, Looker Studio)", "✗ Click and drag (Excel, Tableau, Looker Studio)", "pl-label")
s.box(40, 124, 520, 270, "ml-cell", 8)
s.box(40, 124, 520, 34, "dg-xl-head", 8)
for k, (lab, x) in enumerate([("Insert", 60), ("Chart", 190), ("Bar", 320)]):
    s.box(x, 130, 80, 24, "ml-cell", 5)
    s.text(x + 40, 148, lab, "dg-cell", "middle")
    s.badge(x + 98, 142, k + 2)
for r in range(5):
    for c in range(4):
        x, y = 56 + c * 120, 172 + r * 34
        s.box(x, y, 116, 30, "dg-hl-col" if c == 2 else "ml-cell", 2)
        if r == 0:
            s.text(x + 58, y + 21, ["Airline Name", "Rating", "Seat Type", "Verified"][c], "dg-cell", "middle")
        elif c == 2:
            s.text(x + 58, y + 21, "Economy", "dg-cell", "middle")
s.badge(310, 221, 1)
s.both(56, 374, "1 เลือกคอลัมน์ · 2 Insert · 3 Chart · 4 Bar", "1 select the column · 2 Insert · 3 Chart · 4 Bar", "pl-note")
s.both(40, 432, "เหมาะกับ: กราฟเร็ว ๆ ครั้งเดียว หรือ dashboard", "Good for: one quick chart, or a dashboard", "pl-text")
s.both(40, 500, "✗ ข้อมูลใหม่ = คลิกใหม่ทุกขั้น", "✗ new data = click every step again", "ml-neg")
# code
s.box(600, 70, 560, 450, "nt-band-a", 14)
s.both(620, 102, "✓ เขียนโค้ด (matplotlib, seaborn, plotly)", "✓ Write code (matplotlib, seaborn, plotly)", "pl-label")
CODE = ['sns.countplot(data=reviews, x="Seat Type")', 'plt.title("Reviews per seat type")', "plt.show()"]
for k, line in enumerate(CODE):
    s.badge(634, 136 + k * 32, k + 1)
    s.text(656, 142 + k * 32, line, "dg-code")
# the chart these lines draw
cx0, cy0, cw, ch = 680, 268, 440, 160
s.box(624, 226, 516, 236, "ml-cell", 8)
s.text(cx0 + cw / 2, 252, "Reviews per seat type", "ml-box-h", "middle")
s.badge(cx0 + cw / 2 + 120, 246, 2)
s.path(f"M{cx0} {cy0} V{cy0 + ch} H{cx0 + cw}", "dg-rule-strong")
bw = cw / 4
for k, (seat, n) in enumerate(COUNTS):
    h = n / 140 * (ch - 14)
    s.box(cx0 + k * bw + 14, cy0 + ch - h, bw - 28, h, "ml-bar", 2)
    s.text(cx0 + k * bw + bw / 2, cy0 + ch - h - 6, str(n), "pl-note", "middle")
    s.text(cx0 + k * bw + bw / 2, cy0 + ch + 20, seat if seat != "Premium Economy" else "Premium Econ.", "dg-cell", "middle")
s.badge(cx0 + bw + bw / 2 + 30, cy0 + 40, 1)
s.badge(1120, 440, 3)
s.both(620, 500, "✓ ข้อมูลใหม่ = รันโค้ดเดิมอีกครั้ง", "✓ new data = run the same code again", "ml-ok")
s.save("l11-code-vs-click.svg", 536)


# ================================================================ S14 (exercise): the columns by kind and the six charts to choose from
s = svg("For the exercise: the columns it uses, by kind. Categorical: Airline Name, Trip Type, Verified, Recommended. Numeric: "
        "Rating, Flight Duration (hours), Delay Minutes. Time: Date Flown. And the six charts to choose from: count plot, bar plot, "
        "histogram, box plot, scatter plot, line chart. Which chart fits which question is left for you.")
GROUPS = [("Categorical", "nt-band-b", ["Airline Name", "Trip Type", "Verified", "Recommended"]),
          ("Numeric", "nt-band-a", ["Rating", "Flight Duration (hours)", "Delay Minutes"]),
          ("Time", "rc-res", ["Date Flown"])]
for k, (kind, band, cols) in enumerate(GROUPS):
    x = 20 + k * 196
    s.box(x, 14, 184, 300, band, 12)
    s.text(x + 16, 44, kind, "pl-label")
    for j, col in enumerate(cols):
        s.box(x + 12, 62 + j * 56, 160, 44, "nt-out", 8)
        lines = ["Flight Duration", "(hours)"] if col == "Flight Duration (hours)" else [col]
        for i, ln in enumerate(lines):
            s.text(x + 92, 62 + j * 56 + (28 if len(lines) == 1 else 19 + i * 19), ln, "ml-box-h", "middle")
s.both(620, 44, "เลือกจาก 6 แบบนี้", "Choose from these 6", "pl-label")
CHARTS = [("count", "countplot"), ("bar", "barplot"), ("hist", "histogram"), ("box", "box plot"), ("scatter", "scatter plot"), ("line", "line chart")]
for k, (kind, name) in enumerate(CHARTS):
    x, y = 620 + (k % 3) * 182, 62 + (k // 3) * 128
    chart_icon(s, kind, x, y, 166, 84)
    s.text(x + 83, y + 108, name, "pl-text", "middle")
s.save("l11-pick-chart-ex.svg", 328)


# ================================================================ S17: from a question to a chart, five steps on one example
BOX = [("Economy", 43.63, 94, 164, 407, 838.92, [901, 914, 942, 1021, 1048]),
       ("Premium Economy", 164.15, 208, 317, 846, 1533.21, []),
       ("Business", 289.71, 590, 1430, 1983, 3248.58, []),
       ("First", 342.33, 514, 751, 1419, 931.39, [2881])]
s = svg("From a question to a chart, five steps on one example. 1 The question: which seat type has the widest spread of ticket "
        "prices? 2 The columns: Seat Type (categorical) and Ticket Price (USD) (numeric). 3 The chart: numeric by group, comparing "
        "spreads, so a box plot. 4 The prompt: draw a boxplot of Ticket Price (USD) for each Seat Type. 5 The follow-up: order "
        "the seat types from Economy to First. The result: Business has the widest box, $590 to $1,983 (the middle half of its "
        "prices); Economy $94 to $407, Premium Economy $208 to $846, First $514 to $1,419.")
STEP17 = [("คำถาม", "Question", "ชั้นที่นั่งไหนราคาตั๋ว", "Which seat type has the", "กระจายกว้างที่สุด", "widest spread of prices?"),
          ("คอลัมน์", "Columns", "Seat Type (categorical)", "Seat Type (categorical)", "Ticket Price (USD) (numeric)", "Ticket Price (USD) (numeric)"),
          ("กราฟ", "Chart", "numeric แยกตามกลุ่ม", "numeric by group,", "เทียบการกระจาย → box plot", "compare spreads → box plot")]
for k, (th, en, l1th, l1en, l2th, l2en) in enumerate(STEP17):
    x = 20 + k * 386
    s.box(x, 14, 364, 118, "nt-band-a" if k < 2 else "rc-res", 12)
    s.badge(x + 28, 44, k + 1)
    s.both(x + 50, 51, th, en, "pl-label")
    s.both(x + 22, 86, l1th, l1en, "pl-text")
    s.both(x + 22, 114, l2th, l2en, "pl-text")
    if k < 2:
        s.arrow(x + 366, 72, x + 384, 72)
# 4. the prompt
s.box(20, 152, 364, 300, "nt-band-b", 12)
s.badge(48, 182, 4)
s.both(70, 189, "prompt: กราฟก่อน แล้วทีละส่วน", "Prompt: the chart, then each part", "pl-label")
PROMPT_TH = ["วาด boxplot ของ", "Ticket Price (USD)", "แยกตาม Seat Type", "แกน x = Seat Type", "แกน y = ราคา (USD)", "ตั้งชื่อกราฟเป็นภาษาอังกฤษ"]
PROMPT_EN = ["Draw a boxplot of", "Ticket Price (USD)", "for each Seat Type.", "x = Seat Type,", "y = price (USD),", "an English title."]
s.box(36, 204, 332, 232, "ml-cell", 8)
for k, (th, en) in enumerate(zip(PROMPT_TH, PROMPT_EN)):
    s.both(52, 236 + k * 34, th, en, "pl-text")
s.arrow(386, 300, 410, 300)
# the box plot it draws, after follow-up 5 (Economy → First)
s.box(414, 152, 746, 356, "ml-cell", 12)
s.badge(442, 182, 5)
s.both(464, 189, "ถามต่อ: \"เรียงชั้นที่นั่งจาก Economy ถึง First\"", "Follow-up: \"Order the seat types from Economy to First\"", "pl-label")
X0, X1, Y0, Y1, PMAX = 520, 1140, 220, 440, 3300
py = lambda v: Y1 - v / PMAX * (Y1 - Y0)
s.path(f"M{X0} {Y0 - 6} V{Y1} H{X1}", "dg-rule-strong")
for v in (0, 1000, 2000, 3000):
    s.path(f"M{X0 - 6} {py(v):.1f} H{X0}", "dg-rule-strong")
    s.text(X0 - 10, py(v) + 6, f"${v:,}", "pl-note", "end")
cw = (X1 - X0) / 4
for k, (seat, lo, q1, md, q3, hi, outs) in enumerate(BOX):
    cx = X0 + cw * (k + 0.5)
    wide = seat == "Business"
    s.path(f"M{cx} {py(hi):.1f} V{py(q3):.1f} M{cx} {py(q1):.1f} V{py(lo):.1f}", "dg-rule-strong")
    s.path(f"M{cx - 16} {py(hi):.1f} H{cx + 16} M{cx - 16} {py(lo):.1f} H{cx + 16}", "dg-rule-strong")
    s.box(cx - 40, py(q3), 80, py(q1) - py(q3), "ml-bar-top" if wide else "ml-cell-b", 4)
    s.path(f"M{cx - 40} {py(md):.1f} H{cx + 40}", "dg-rule-strong")
    for o in outs:
        s.raw(f'<circle cx="{cx}" cy="{py(o):.1f}" r="4" class="ml-cell"/>')
    s.text(cx, Y1 + 24, seat, "dg-cell", "middle")
    s.text(cx, Y1 + 48, f"${q1:,}–${q3:,}", "pl-label" if wide else "pl-note", "middle")
cxb = X0 + cw * 2.5
s.text(cxb + 48, py(1983) + 6, "$1,983", "pl-label")
s.text(cxb + 48, py(590) + 6, "$590", "pl-label")
s.both(414, 540, "✓ Business กว้างที่สุด: ราคาครึ่งกลาง $590 ถึง $1,983", "✓ Business is the widest: its middle half runs $590 to $1,983", "ml-ok")
s.save("l11-question-to-chart.svg", 556)
