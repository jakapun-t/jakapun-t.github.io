"""Concept pictures for nlp-basic lesson 10 (pandas), in the style of nlp l12-why-chunk.svg: the running
example's question on top, drawn objects, arrows at the exact spot, the real numbers attached to what they
describe. ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/basic_l10_concepts.py courses/nlp-basic/images

Every value is from the lesson's own data (data/airline_reviews.csv, airline_small.csv, my_reviews.csv,
my_airlines.csv), checked in course/.venv. The three timings of L10-S26 are read from the lesson's own
```output blocks, so rerun this script after `npm run outputs -- nlp-basic lesson10`.

Exercise pictures (S27, S32, S41) show the task and its data only; the answers stay behind Show answer.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from basic_svg import Svg, width  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
LESSON = os.path.join(OUT, "..", "lesson10-pandas.md")
W = 1180


def svg(title):
    return Svg(OUT, W, title)


# ---------------------------------------------------------------- small drawn icons (about 44 x 36)
def icon(s, kind, cx, cy):
    if kind == "id":  # a barcode
        x = cx - 20
        for k, bw in enumerate([3, 1, 2, 1, 3, 2, 1, 3, 1, 2, 3, 1]):
            if k % 2 == 0:
                s.box(x, cy - 15, bw * 2, 30, "ml-model", 0)
            x += bw * 2 + 1
    elif kind == "cat":  # three separate bins
        for k in range(3):
            s.box(cx - 22 + k * 16, cy - 8, 12, 12, ["ml-bar-top", "ml-bar", "ml-model"][k], 3)
        s.path(f"M{cx - 24} {cy + 10} H{cx + 24}", "dg-rule")
    elif kind == "ord":  # a staircase
        for k in range(3):
            s.box(cx - 21 + k * 15, cy + 12 - (k + 1) * 9, 13, (k + 1) * 9, "ml-bar", 2)
        s.box(cx + 9, cy - 15, 13, 27, "ml-bar-top", 2)
    elif kind == "text":  # a speech bubble with lines
        s.box(cx - 22, cy - 15, 44, 26, "ml-cell", 6)
        s.path(f"M{cx - 12} {cy + 11} L{cx - 16} {cy + 18} L{cx - 4} {cy + 11}", "ml-cell")
        for k in range(3):
            s.box(cx - 16, cy - 10 + k * 7, 32 - k * 8, 3, "ml-bar", 1)
    elif kind == "date":  # a calendar
        s.box(cx - 19, cy - 14, 38, 30, "ml-cell", 4)
        s.box(cx - 19, cy - 14, 38, 9, "ml-bar-top", 3)
        for r in range(2):
            for c in range(4):
                s.box(cx - 14 + c * 8, cy - 1 + r * 7, 5, 4, "ml-bar", 1)
    elif kind == "num":  # a ruler with a dot on it
        s.path(f"M{cx - 22} {cy + 6} H{cx + 22}", "dg-rule-strong")
        for k in range(5):
            s.path(f"M{cx - 22 + k * 11} {cy + 1} V{cy + 11}", "dg-rule-strong")
        s.raw(f'<circle cx="{cx + 6}" cy="{cy - 6}" r="6" class="pl-dot"/>')
    elif kind == "bool":  # a switch
        s.box(cx - 20, cy - 10, 40, 20, "rc-res", 10)
        s.raw(f'<circle cx="{cx + 10}" cy="{cy}" r="8" class="ml-cell"/>')


# ================================================================ S03: one review as a boarding pass
s = svg("Review AR0001 drawn as a boarding pass, each field labelled with its column name and kind: Airline Name Garuda Indonesia "
        "(categorical), Origin Bali and Destination Jakarta (categorical), Trip Type Solo Travel (categorical), Date Flown 2026-01-14 "
        "(date), Seat Type Economy (ordinal), Flight Duration 2.2 hours, Ticket Price 109.77 USD and Delay Minutes NaN "
        "(quantitative), the Review text (text), Review ID AR0001 (identifier), Rating 3.5 of 10 (ordinal / numeric), "
        "Verified True and Recommended False (boolean).")
s.bubble(W / 2, 8, "รีวิว AR0001 หนึ่งแถว: แต่ละคอลัมน์บอกอะไร", "One row, review AR0001: what does each column say?", 560)
s.box(20, 70, W - 40, 470, "ml-cell", 18)
s.path("M880 82 V528", "dg-rule-strong", ' stroke-dasharray="7 6"')


def field(x, y, col, kind, value, vcls="pl-label", note=None):
    """Column name, the value from AR0001, and a chip with the kind."""
    s.text(x, y, col, "pl-note")
    s.text(x, y + 30, value, vcls)
    if note:
        s.both(x + width(value, 19) + 12, y + 30, note[0], note[1], "pl-note")
    w = width(kind, 16) + 18
    s.box(x, y + 40, w, 24, "pl-chip", 7)
    s.text(x + w / 2, y + 58, kind, "ml-b", "middle")


field(44, 102, "Airline Name", "categorical", "Garuda Indonesia", "nt-band-title")
field(560, 102, "Trip Type", "categorical", "Solo Travel")
field(44, 190, "Origin", "categorical", "Bali")
s.path("M120 212 Q260 172 400 212", "pl-line", ' stroke-dasharray="6 5"')
s.head(330, 192, 400, 212)
field(420, 190, "Destination", "categorical", "Jakarta")
field(44, 278, "Date Flown", "date", "2026-01-14")
field(280, 278, "Seat Type", "ordinal", "Economy")
for k, lab in enumerate(["E", "PE", "B", "F"]):  # Economy < Premium Economy < Business < First
    s.box(392 + k * 34, 332 - 12 - k * 8, 28, 12 + k * 8, "ml-bar-top" if k == 0 else "ml-bar", 2)
    s.text(406 + k * 34, 350, lab, "ml-i", "middle")
field(560, 278, "Flight Duration (hours)", "quantitative", "2.2")
field(44, 366, "Ticket Price (USD)", "quantitative", "109.77")
field(280, 366, "Delay Minutes", "quantitative", "NaN", "pl-label", ("(ว่างในแถวนี้)", "(empty in this row)"))
# the review text in a speech bubble
s.text(44, 454, "Review", "pl-note")
w = width("text", 16) + 18
s.box(110, 438, w, 24, "pl-chip", 7)
s.text(110 + w / 2, 456, "text", "ml-b", "middle")
s.box(44, 470, 812, 58, "nt-band-b", 10)
s.text(60, 495, "“On my Bali to Jakarta trip, the ticket seemed cheap until I paid the additional fees.", "dg-cell")
s.text(60, 516, "The journey was part of a longer itinerary. … We arrived around 189 minutes late.”", "dg-cell")
# the stub: identifier, rating, booleans
field(904, 102, "Review ID", "identifier", "AR0001", "hk-mono")
icon(s, "id", 1100, 128)
field(904, 206, "Rating", "ordinal / numeric", "3.5")
s.box(960, 222, 140, 12, "ml-cell", 6)
s.box(960, 222, 140 * 3.5 / 10, 12, "ml-bar-top", 6)
s.text(1108, 233, "/ 10", "pl-note")
field(904, 310, "Verified", "boolean", "True")
s.box(1100, 322, 24, 24, "rc-res", 5)
s.path("M1105 334 L1111 340 L1120 328", "pl-line")
field(904, 414, "Recommended", "boolean", "False")
s.box(1100, 426, 24, 24, "ml-cell", 5)
s.save("l10-data-dictionary.svg", 552)


# ================================================================ S06: a Series, its index, .loc and .iloc
s = svg("What is AR0006's rating? The Series scores holds 9.0, 2.5 and 8.0 with the index AR0005, AR0006, AR0007 and the "
        "positions 0, 1, 2. scores.loc[\"AR0006\"] finds the label AR0006; scores.iloc[1] finds position 1; both reach 2.5. "
        "A DataFrame is several Series side by side sharing one index: its Rating column is the same Series.")
s.bubble(W / 2, 8, "คะแนนของ AR0006 คือเท่าไร", "What is AR0006's rating?", 420)
s.box(20, 70, 660, 400, "nt-band-a", 14)
s.both(40, 102, "Series: หนึ่งคอลัมน์ พร้อม index", "A Series: one column, with its index", "pl-label")
IDS, VALS = ["AR0005", "AR0006", "AR0007"], ["9.0", "2.5", "8.0"]
X_IDX, X_VAL, X_POS, Y0, RH = 170, 310, 446, 200, 54
s.both(X_IDX + 64, Y0 - 14, "index (ป้ายชื่อ)", "index (labels)", "pl-note", "middle")
s.both(X_VAL + 55, Y0 - 14, "ค่า", "values", "pl-note", "middle")
s.both(X_POS, Y0 - 14, "ตำแหน่ง", "position", "pl-note", "middle")
for k in range(3):
    y = Y0 + k * RH
    hit = k == 1
    s.box(X_IDX, y, 128, RH - 8, "dg-hl-index", 6)
    s.text(X_IDX + 64, y + 30, IDS[k], "hk-mono", "middle")
    s.box(X_VAL, y, 110, RH - 8, "rc-res" if hit else "ml-cell", 6)
    s.text(X_VAL + 55, y + 31, VALS[k], "pl-label", "middle")
    s.text(X_POS, y + 31, str(k), "pl-label" if hit else "pl-note", "middle")
s.text(X_VAL + 55, Y0 + 3 * RH + 16, "dtype: float64", "dg-code", "middle")
# .loc comes in from the left, at the label; .iloc from the right, at the position
yh = Y0 + RH + 23
s.text(40, 150, 'scores.loc["AR0006"]', "hk-mono")
s.curve(80, 160, 80, yh, X_IDX - 6, yh)
s.both(40, yh + 40, "หาด้วยป้ายชื่อ", "by label", "pl-note")
s.text(500, yh + 6, "scores.iloc[1]", "hk-mono")
s.arrow(494, yh, X_POS + 16, yh)
s.both(500, yh + 34, "หาด้วยตำแหน่ง", "by position", "pl-note")
s.both(500, yh + 58, "(นับจาก 0)", "(from 0)", "pl-note")
s.both(40, 448, "✓ ได้ 2.5 ทั้งคู่ คนละกติกา: ป้ายชื่อ กับ ตำแหน่ง", "✓ both give 2.5, by two rules: label and position", "ml-ok")
# a DataFrame: Series side by side
s.box(700, 70, 460, 400, "nt-band-b", 14)
s.both(720, 102, "DataFrame: หลาย Series", "A DataFrame: Series side by side,", "pl-label")
s.both(720, 128, "ที่ใช้ index ชุดเดียวกัน", "sharing one index", "pl-label")
COLS = [("", 92), ("Airline Name", 150), ("Rating", 70), ("Seat Type", 104)]
ROWS = [["AR0005", "Thai Airways", "9.0", "Economy"], ["AR0006", "Japan Airlines", "2.5", None],
        ["AR0007", "Japan Airlines", "8.0", "Economy"]]
x0, y0 = 720, 190
x = x0
for c, (name, cw) in enumerate(COLS):
    if name:
        s.text(x + cw / 2, y0 - 12, name, "ml-box-h", "middle")
    for r, row in enumerate(ROWS):
        y = y0 + r * RH
        v = row[c]
        if c == 0:
            s.box(x, y, cw - 6, RH - 8, "dg-hl-index", 6)
            s.text(x + (cw - 6) / 2, y + 30, v, "dg-index", "middle")
        else:
            s.box(x, y, cw - 6, RH - 8, "rc-res" if (c == 2 and r == 1) else "ml-cell", 6)
            if v is None:
                s.text(x + (cw - 6) / 2, y + 30, "NaN", "dg-nan", "middle")
            else:
                s.text(x + (cw - 6) / 2, y + 30, v, "dg-cell", "middle")
    x += cw
xr = x0 + 92 + 150  # the Rating column
s.box(xr - 6, y0 - 34, 76, 3 * RH + 36, "dg-row", 10)
s.both(xr + 32, y0 + 3 * RH + 26, "คอลัมน์ Rating = Series", "the Rating column = a Series", "pl-note", "middle")
s.both(720, 448, "reviews[\"Rating\"] ได้ Series หนึ่งตัว", "reviews[\"Rating\"] gives one Series", "ml-ok")
s.save("l10-series-index.svg", 486)


# ================================================================ S08: what is inside a CSV file
MONO = 11.4  # IBM Plex Mono 600 at 19px: 0.6em per character


def mono_line(x, y, parts):
    """parts: (text, cls) pieces of one line of a file, drawn left to right in mono."""
    for t, cls in parts:
        s.text(x, y, t, cls)
        x += len(t) * MONO
    return x


s = svg("What is inside a CSV file? It is plain text: a comma starts the next column and \\n (a line break) starts the next "
        "row; pd.read_csv turns it into a table of 200 rows by 14 columns. A review with commas inside must be wrapped in "
        "quotes: without them, the comma after 'trip' splits one review into two cells and every later column shifts; "
        "with them (as in our file) it stays one cell. A TSV uses a tab instead: pd.read_csv(..., sep='\\t').")
s.bubble(W / 2, 8, "ไฟล์ airline_reviews.csv ข้างในหน้าตาเป็นอย่างไร", "What is inside airline_reviews.csv?", 560)
s.box(20, 70, W - 40, 262, "nt-band-a", 14)
s.box(40, 92, 610, 220, "ml-cell", 8)
s.box(40, 92, 610, 30, "dg-xl-head", 8)
s.text(56, 113, "airline_reviews.csv", "dg-code")
COMMA, NL = "hk-mono ml-neg", "hk-mono ml-neg"
LINES = [[("Airline Name", "hk-mono"), (",", COMMA), ("Rating", "hk-mono"), (",", COMMA), ("Seat Type", "hk-mono"), (",…", "hk-mono"), ("\\n", NL)],
         [("Garuda Indonesia", "hk-mono"), (",", COMMA), ("3.5", "hk-mono"), (",", COMMA), ("Economy", "hk-mono"), (",…", "hk-mono"), ("\\n", NL)],
         [("VietJet Air", "hk-mono"), (",", COMMA), ("6.5", "hk-mono"), (",", COMMA), ("Economy", "hk-mono"), (",…", "hk-mono"), ("\\n", NL)]]
ends = [mono_line(56, 160 + k * 40, L) for k, L in enumerate(LINES)]
xc = 56 + len("Garuda Indonesia") * MONO + MONO / 2  # the first comma of line 2
s.arrow(xc, 268, xc, 210)
s.both(xc - 16, 292, "จุลภาค , = ขึ้นคอลัมน์ใหม่", "a comma , = the next column", "pl-note")
s.arrow(ends[1] + 44, 256, ends[2] + 4, 236)
s.both(ends[1] + 50, 280, "\\n = ขึ้นแถวใหม่", "\\n = the next row", "pl-note")
# the table pandas makes from it
s.arrow(668, 200, 746, 200)
s.text(707, 186, "pd.read_csv", "dg-code", "middle")
TCOL = [("Airline Name", 170), ("Rating", 74), ("Seat Type", 110)]
TROW = [["Garuda Indonesia", "3.5", "Economy"], ["VietJet Air", "6.5", "Economy"]]
x = 760
for c, (name, cw) in enumerate(TCOL):
    s.box(x, 128, cw - 4, 40, "dg-xl-head", 4)
    s.text(x + (cw - 4) / 2, 154, name, "ml-box-h", "middle")
    for r, row in enumerate(TROW):
        s.box(x, 172 + r * 44, cw - 4, 40, "ml-cell", 4)
        s.text(x + (cw - 4) / 2, 198 + r * 44, row[c], "dg-cell", "middle")
    x += cw
s.text(x + 8, 198, "…", "pl-label")
s.both(760, 300, "ได้ตาราง 200 แถว × 14 คอลัมน์", "a table of 200 rows × 14 columns", "ml-ok")
# commas inside the text: without quotes vs with quotes
for x0, band, th, en, line, cells, res_th, res_en, rcls in (
        (20, "sw-warn-box", "✗ ข้อความมีจุลภาค แต่ไม่มีเครื่องหมายคำพูด", "✗ A comma in the text, no quotes",
         [(",", COMMA), ("On my Bali to Jakarta trip", "hk-mono"), (",", COMMA), (" the ticket…", "hk-mono"), (",", COMMA)],
         ["On my Bali to Jakarta trip", "the ticket…"],
         "✗ รีวิวเดียวกลายเป็น 2 ช่อง คอลัมน์ถัดไปเลื่อนหมด", "✗ one review becomes 2 cells; every later column shifts", "ml-neg"),
        (600, "nt-band-a", "✓ มีเครื่องหมายคำพูด (แบบในไฟล์ของเรา)", "✓ Wrapped in quotes (as in our file)",
         [(",", COMMA), ('"On my Bali to Jakarta trip, the ticket…"', "hk-mono"), (",", COMMA)],
         ["On my Bali to Jakarta trip, the ticket…"],
         "✓ จุลภาคในเครื่องหมายคำพูดเป็นแค่ตัวอักษร: 1 ช่อง", "✓ a comma inside quotes is just a letter: 1 cell", "ml-ok")):
    s.box(x0, 348, 560, 210, band, 14)
    s.both(x0 + 20, 380, th, en, "pl-label")
    mono_line(x0 + 20, 422, line)
    if len(cells) == 2:
        xin = x0 + 20 + MONO * (1 + len("On my Bali to Jakarta trip")) + MONO / 2
        s.arrow(xin, 470, xin, 436)
        s.both(xin + 10, 468, "pandas ตัดตรงนี้", "pandas cuts here", "ml-neg")
        s.box(x0 + 20, 484, 300, 38, "ml-cell", 4)
        s.text(x0 + 170, 509, cells[0], "dg-cell", "middle")
        s.box(x0 + 326, 484, 140, 38, "sw-chip-warn", 4)
        s.text(x0 + 396, 509, cells[1], "dg-cell", "middle")
    else:
        s.box(x0 + 20, 484, 446, 38, "rc-res", 4)
        s.text(x0 + 243, 509, cells[0], "dg-cell", "middle")
    s.both(x0 + 20, 546, res_th, res_en, rcls)
s.both(20, 590, "TSV ใช้แท็บแทนจุลภาค: pd.read_csv(\"reviews.tsv\", sep=\"\\t\") · Excel: pd.read_excel(..., sheet_name=\"Reviews\")",
       "A TSV uses a tab instead of a comma: pd.read_csv(\"reviews.tsv\", sep=\"\\t\") · Excel: pd.read_excel(..., sheet_name=\"Reviews\")",
       "pl-note")
s.save("l10-csv-file.svg", 606)


# ================================================================ S04: dtype vs what a column really is
STRIPS = [  # column, its first 3 values (AR0001-AR0003), dtype, kind, icon, gloss th / en
    ("Review ID", ["AR0001", "AR0002", "AR0003"], "object", "Identifier", "id", "รหัส ไม่ใช่เลข", "a code"),
    ("Airline Name", ["Garuda Indonesia", "VietJet Air", "VietJet Air"], "object", "Categorical", "cat", "กลุ่ม ไม่มีลำดับ", "no order"),
    ("Seat Type", ["Economy", "Economy", "Economy"], "object", "Ordinal", "ord", "E < B < F", "E < B < F"),
    ("Review", ["On my Bali to…", "I flew from Ho…", "I flew from Ho…"], "object", "Text", "text", "ข้อความอิสระ", "free text"),
    ("Date Flown", ["2026-01-14", "2025-01-18", "2020-06-07"], "object", "Date", "date", "เก็บเป็นข้อความ", "kept as text"),
    ("Rating", ["3.5", "6.5", "6.0"], "float64", "Quantitative", "num", "คำนวณได้", "a quantity"),
    ("Delay Minutes", [None, "0.0", "84.0"], "float64", "Quantitative", "num", "มี NaN → float", "NaN → float"),
    ("Verified", ["True", "False", "False"], "bool", "Boolean", "bool", "จริง หรือ เท็จ", "True / False"),
]
s = svg("Can you average Review ID? The first three rows of eight columns with the dtype pandas stores each as. Review ID, "
        "Airline Name, Seat Type, Review and Date Flown are all object, yet they mean five different things: an identifier, "
        "categorical, ordinal, text and a date. Rating is float64, a quantity; Delay Minutes holds whole minutes but is float64 "
        "because of NaN; Verified is bool. reviews['Review ID'].mean() glues the codes into 'AR0001AR0002…' and stops with a "
        "TypeError; reviews['Rating'].mean() gives 6.47 from 188 ratings.")
s.bubble(W / 2, 8, "หาค่าเฉลี่ยของ Review ID ได้ไหม", "Can you average Review ID?", 440)
SW, GAP, X0 = 136, 7, 20
for k, (col, vals, dt, kind, ic, gth, gen) in enumerate(STRIPS):
    x = X0 + k * (SW + GAP)
    cx = x + SW / 2
    s.box(x, 72, SW, 36, "dg-xl-head", 6)
    s.text(cx, 96, col, "ml-box-h", "middle")
    for r, v in enumerate(vals):
        s.box(x, 112 + r * 32, SW, 30, "ml-cell", 4)
        s.text(cx, 132 + r * 32, "NaN" if v is None else v, "dg-nan" if v is None else "dg-cell", "middle")
    s.box(x + 18, 216, SW - 36, 32, "nt-out" if dt == "object" else "ml-cell", 8)
    s.text(cx, 238, dt, "hk-mono", "middle")
    # down to what it really is
    s.arrow(cx, 302 if k < 5 else 254, cx, 314)
    s.box(x, 318, SW, 122, "nt-band-a", 10)
    s.badge(x + 18, 336, k + 1)
    icon(s, ic, cx + 10, 346)
    s.text(cx, 392, kind, "pl-label", "middle")
    s.both(cx, 420, gth, gen, "pl-note", "middle")
# the five columns that share `object`
x5 = X0 + 5 * (SW + GAP) - GAP
s.path(f"M{X0 + 18} 252 V258 H{x5 - 18} V252", "pl-line")
s.path(f"M{(X0 + x5) / 2} 258 V266", "pl-line")
s.box(X0 + 60, 266, x5 - X0 - 120, 36, "sw-chip-warn", 10)
s.both((X0 + x5) / 2, 291, "dtype เดียวกัน 5 คอลัมน์ แต่ความหมายต่างกันทั้ง 5", "one dtype for 5 columns, 5 different meanings",
       "ml-neg", "middle")
# the answer to the question: Review ID vs Rating
s.box(20, 456, 560, 120, "sw-warn-box", 14)
s.text(40, 490, 'reviews["Review ID"].mean()', "hk-mono")
s.text(40, 522, "→ 'AR0001AR0002AR0003…' → TypeError", "pl-text")
s.both(40, 558, "✗ ต่อรหัสเป็นข้อความยาว แล้วหยุดทำงาน", "✗ it glues the codes together, then stops", "ml-neg")
s.box(600, 456, 560, 120, "nt-band-a", 14)
s.text(620, 490, 'reviews["Rating"].mean()', "hk-mono")
s.both(620, 522, "→ 6.47 (จาก 188 คะแนน ข้าม NaN 12 ค่า)", "→ 6.47 (from 188 ratings; 12 NaN skipped)", "pl-text")
s.both(620, 558, "✓ ตัวเลขที่คำนวณได้จริง จึงหาค่าเฉลี่ยได้", "✓ a real quantity, so the mean makes sense", "ml-ok")
s.save("l10-column-types.svg", 592)


# ================================================================ S12: .iloc stops before the end, .loc includes it
NAMES = ["Garuda Indonesia", "VietJet Air", "VietJet Air", "Singapore Airlines", "Thai Airways", "Japan Airlines"]
s = svg("How many rows does [2:4] give? reviews.iloc[2:4, 0] counts positions, like a Python list: it starts at cut 2 and "
        "stops before cut 4, so it gives rows 2 and 3 (VietJet Air, Singapore Airlines): 4 − 2 = 2 rows; Thai Airways at 4 "
        "is left out. reviews.loc[2:4, 'Airline Name'] uses labels and includes the end label, so it gives rows 2, 3 and 4: "
        "3 rows.")
s.bubble(W / 2, 8, "[2:4] ได้กี่แถว", "How many rows does [2:4] give?", 380)
RH, Y0 = 44, 186
for x0, band, th, en, code, mode in (
        (20, "nt-band-b", "ตำแหน่ง: หยุดก่อนตัวปลาย (เหมือน list)", "Position: stops before the end (like a list)",
         "reviews.iloc[2:4, 0]", "iloc"),
        (600, "nt-band-a", "ป้ายชื่อ: รวมตัวปลายด้วย", "Label: includes the end", 'reviews.loc[2:4, "Airline Name"]', "loc")):
    s.box(x0, 70, 560, 456, band, 14)
    s.both(x0 + 20, 102, th, en, "pl-label")
    s.text(x0 + 20, 140, code, "hk-mono")
    tx = x0 + 110  # the table
    for r, name in enumerate(NAMES):
        y = Y0 + r * RH
        keep = 2 <= r <= 3 or (mode == "loc" and r == 4)
        s.box(tx, y + 2, 56, RH - 4, "dg-hl-index", 4)
        s.text(tx + 28, y + 29, str(r), "dg-index", "middle")
        s.box(tx + 60, y + 2, 230, RH - 4, "rc-res" if keep else ("pl-chip-del" if (mode == "iloc" and r == 4) else "ml-cell"), 4)
        s.text(tx + 76, y + 29, name, "pl-text" if keep else "pl-note")
    s.both(tx + 28, Y0 - 12, "ป้ายชื่อ", "label", "pl-note", "middle")
    if mode == "iloc":
        s.both(x0 + 16, Y0 - 12, "ตำแหน่ง", "position", "pl-note")
        for cut in range(7):  # positions are the cuts between rows
            y = Y0 + cut * RH
            s.text(x0 + 70, y + 6, str(cut), "pl-label" if cut in (2, 4) else "pl-note", "end")
            s.path(f"M{x0 + 78} {y} H{tx + 300}", "ml-cut" if cut in (2, 4) else "dg-rule")
        s.both(tx + 310, Y0 + 2 * RH + 6, "← เริ่มที่ 2", "← start at 2", "pl-label")
        s.both(tx + 310, Y0 + 4 * RH + 6, "← หยุดก่อน 4", "← stop before 4", "ml-neg")
        s.both(tx + 330, Y0 + 4 * RH + 34, "ไม่รวมแถว 4", "row 4 is out", "pl-note")
        s.both(x0 + 20, 506, "= 2 แถว (2, 3) · ได้ 4 − 2 ตัว", "= 2 rows (2, 3) · 4 − 2 items", "pl-label")
    else:
        yb, ye = Y0 + 2 * RH + 4, Y0 + 5 * RH - 4
        s.path(f"M{tx + 302} {yb} H{tx + 314} V{ye} H{tx + 302}", "pl-line")
        s.both(tx + 326, (yb + ye) / 2 + 6, "2, 3, 4", "2, 3, 4", "pl-label")
        s.both(tx + 326, (yb + ye) / 2 + 34, "รวม 4 ✓", "4 included ✓", "ml-ok")
        s.both(x0 + 20, 506, "= 3 แถว (2, 3, 4)", "= 3 rows (2, 3, 4)", "pl-label")
s.save("l10-slice-ends.svg", 540)


# ================================================================ S19: new columns from whole-column rules
ROWS19 = [("AR0001", "2026-01-14", "3.5"), ("AR0002", "2025-01-18", "6.5"), ("AR0003", "2020-06-07", "6.0"),
          ("AR0004", "2026-05-10", "8.0"), ("AR0005", "2023-11-15", "9.0"), None, ("AR0013", None, "6.0")]
s = svg("Which reviews rate 8 or more, and in which year did they fly? One rule makes a whole new column at once: "
        "work['Rating'] >= 8 gives is_high_rating (True for AR0004 at 8.0 and AR0005 at 9.0); pd.to_datetime turns the text "
        "Date Flown into flight_date; .dt.year takes its year. AR0013 has no date: it becomes NaT and its year NaN, and "
        "because 8 reviews have no date the years show as 2026.0.")
s.bubble(W / 2, 8, "รีวิวไหนคะแนนสูง (≥ 8) และบินปีไหน", "Which reviews rate 8 or more, and in which year did they fly?", 640)
OLD = [("Review ID", 20, 120), ("Date Flown", 140, 160), ("Rating", 300, 96)]
NEW = [("is_high_rating", 560, 170), ("flight_date", 730, 160), ("year", 890, 110)]
HY, RY, RH = 214, 244, 40


def colx(cols, name):
    for n, x, w in cols:
        if n == name:
            return x + w / 2


for n, x, w in OLD + NEW:
    s.box(x, HY - 26, w - 6, 36, "dg-xl-head" if (n, x, w) in OLD else "nt-out", 6)
    s.text(x + (w - 6) / 2, HY - 2, n, "ml-box-h", "middle")
# rule 1: Rating >= 8 → is_high_rating (the inner arrow)
xr, xh = colx(OLD, "Rating"), colx(NEW, "is_high_rating")
s.path(f"M{xr} {HY - 30} V150 H420 M540 150 H{xh} V{HY - 34}", "pl-line")
s.head(xh, 150, xh, HY - 30)
s.box(420, 132, 120, 36, "nt-bubble", 10)
s.text(480, 157, ">= 8", "hk-mono", "middle")
# rule 2: Date Flown → flight_date → year (the outer arrow)
xd, xf, xy = colx(OLD, "Date Flown"), colx(NEW, "flight_date"), colx(NEW, "year")
s.path(f"M{xd} {HY - 30} V90 H330 M550 90 H{xf} V{HY - 34}", "pl-line")
s.head(xf, 90, xf, HY - 30)
s.box(330, 72, 220, 36, "nt-bubble", 10)
s.text(440, 97, "pd.to_datetime", "hk-mono", "middle")
s.path(f"M{xf + 30} {HY - 30} Q{(xf + xy) / 2} 120 {xy} {HY - 34}", "pl-line")
s.head((xf + xy) / 2, 150, xy, HY - 30)
s.box((xf + xy) / 2 - 2, 122, 112, 34, "nt-bubble", 10)
s.text((xf + xy) / 2 + 54, 145, ".dt.year", "hk-mono", "middle")
for k, row in enumerate(ROWS19):
    y = RY + k * RH
    if row is None:
        s.text(70, y + 26, "…", "pl-label", "middle")
        continue
    rid, date, rating = row
    high = float(rating) >= 8
    cells = [(OLD[0], rid, "dg-index"), (OLD[1], f"'{date}'" if date else "NaN", "dg-cell" if date else "dg-nan"),
             (OLD[2], rating, "dg-cell"), (NEW[0], str(high), "pl-label" if high else "dg-cell"),
             (NEW[1], date or "NaT", "dg-cell" if date else "dg-nan"),
             (NEW[2], f"{date[:4]}.0" if date else "NaN", "dg-cell" if date else "dg-nan")]
    for (n, x, w), v, cls in cells:
        tint = "rc-res" if (n == "is_high_rating" and high) else ("sw-chip-warn" if not date and n in ("flight_date", "year") else "ml-cell")
        s.box(x, y + 2, w - 6, RH - 4, tint, 4)
        s.text(x + (w - 6) / 2, y + 26, v, cls, "middle")
yb = RY + len(ROWS19) * RH + 10
s.path(f"M20 {yb} H410", "dg-rule-strong")
s.both(20, yb + 26, "ตาราง work (copy ของ reviews)", "the table work (a copy of reviews)", "pl-note")
s.path(f"M560 {yb} H994", "pl-line")
s.both(560, yb + 26, "3 คอลัมน์ใหม่: กฎเดียวทำทั้งคอลัมน์ในครั้งเดียว", "3 new columns: one rule fills a whole column at once", "ml-ok")
s.both(20, yb + 56, "8 รีวิวไม่มีวันที่ → NaT (errors=\"coerce\") → ปีเป็น NaN ปีอื่นจึงเป็น 2026.0",
       "8 reviews have no date → NaT (errors=\"coerce\") → year NaN, so years show as 2026.0", "pl-note")
s.save("l10-new-columns.svg", yb + 70)


# ================================================================ S22: isna() and notna() on Seat Type
GAPS = [("Ticket Price (USD)", 22), ("Seat Type", 16), ("Delay Minutes", 14), ("Rating", 12),
        ("Flight Duration (hours)", 10), ("Date Flown", 8), ("Trip Type", 8), ("Review", 5)]
SEAT = [("AR0004", "Economy"), ("AR0005", "Economy"), ("AR0006", None), ("AR0007", "Economy"),
        ("AR0008", "Economy"), ("AR0009", "Economy"), ("AR0010", None), ("AR0011", "Economy")]
s = svg("Which reviews have no Seat Type? reviews.isna().sum() counts the gaps per column: Ticket Price 22, Seat Type 16, "
        "Delay Minutes 14, Rating 12, Flight Duration 10, Date Flown 8, Trip Type 8, Review 5, the other 6 columns 0. "
        "On Seat Type, .isna() is True for the empty rows (AR0006, AR0010 here) and keeps 16 rows; .notna() is the opposite "
        "and keeps 184 = 200 − 16.")
s.bubble(W / 2, 8, "รีวิวไหนไม่มี Seat Type", "Which reviews have no Seat Type?", 420)
s.box(20, 70, 380, 450, "ml-cell", 14)
s.text(36, 104, "reviews.isna().sum()", "hk-mono")
s.both(36, 132, "ค่าว่างในแต่ละคอลัมน์", "gaps in each column", "pl-note")
for k, (col, n) in enumerate(GAPS):
    y = 160 + k * 36
    hit = col == "Seat Type"
    s.text(236, y + 21, col, "pl-label" if hit else "pl-note", "end")
    s.box(246, y + 6, n * 5, 22, "ml-bar-top" if hit else "ml-bar", 3)
    s.text(252 + n * 5, y + 23, str(n), "pl-label" if hit else "pl-note")
s.both(236, 160 + 8 * 36 + 21, "อีก 6 คอลัมน์", "the other 6", "pl-note", "end")
s.text(252, 160 + 8 * 36 + 23, "0", "pl-note")
for x0, band, code, th, en, keep_nan, n_th, n_en in (
        (420, "nt-band-b", '.isna()', "หาแถวที่ว่าง", "Find the empty rows", True, "✓ เก็บ 16 แถว (Seat Type ว่าง)", "✓ keeps 16 rows (no Seat Type)"),
        (800, "nt-band-a", '.notna()', "หาแถวที่ไม่ว่าง", "Find the filled rows", False, "✓ เก็บ 184 แถว (200 − 16)", "✓ keeps 184 rows (200 − 16)")):
    s.box(x0, 70, 360, 450, band, 14)
    s.both(x0 + 20, 102, th, en, "pl-label")
    s.text(x0 + 20, 136, 'reviews["Seat Type"]' + code, "hk-mono")
    s.text(x0 + 168, 172, "Seat Type", "ml-box-h", "middle")
    s.text(x0 + 300, 172, code, "ml-box-h", "middle")
    for r, (rid, seat) in enumerate(SEAT):
        y = 184 + r * 36
        mask = (seat is None) == keep_nan
        if mask:
            s.box(x0 + 12, y, 336, 32, "rc-res", 6)
        s.text(x0 + 24, y + 22, rid, "dg-index")
        s.text(x0 + 168, y + 22, seat or "NaN", "dg-cell" if seat else "dg-nan", "middle")
        s.text(x0 + 300, y + 22, str(mask), "pl-label" if mask else "pl-note", "middle")
    s.both(x0 + 20, 500, n_th, n_en, "ml-ok")
s.save("l10-isna.svg", 534)


# ================================================================ S26: loop vs apply vs whole column, with the lesson's timings
def timing(label):
    with open(LESSON, encoding="utf-8") as f:
        m = re.search(rf"^{label}: ([\d.]+) ms$", f.read(), re.M)
    return float(m.group(1))


T_LOOP, T_APPLY, T_VEC = timing("loop"), timing("apply"), timing("vectorized")
PRICE, DUR = ["109.77", "92.39", "58.24", "221.37"], ["2.2", "2.2", "2.4", "2.8"]
PER = [f"{float(p) / float(d):.2f}".rstrip("0").rstrip(".") for p, d in zip(PRICE, DUR)]
s = svg(f"Price per hour for 20,000 rows, three ways. 1: a loop with iterrows works one row at a time: {T_LOOP:g} ms. "
        f"2: .apply with axis=1 is shorter but still works row by row inside: {T_APPLY:g} ms. 3: whole-column (vectorized) "
        f"code divides the price column by the duration column in one operation: {T_VEC:g} ms, about "
        f"{round(T_LOOP / T_VEC, -2):,.0f} times faster than the loop. The first rows: 109.77 / 2.2 = 49.9, 92.39 / 2.2 = 42, "
        "58.24 / 2.4 = 24.27.")
s.bubble(W / 2, 8, "ราคาต่อชั่วโมง ของตาราง 20,000 แถว", "Price per hour, on a 20,000-row table", 500)
PW = 366
for k, (band, th, en, code) in enumerate((
        ("sw-warn-box", "วน loop ทีละแถว", "Loop over the rows", "for … in big.iterrows()"),
        ("nt-band-b", ".apply() ทีละแถว", ".apply() row by row", ".apply(lambda row: …)"),
        ("nt-band-a", "ทั้งคอลัมน์ทีเดียว", "The whole column at once", "price / duration"))):
    x0 = 20 + k * (PW + 21)
    s.box(x0, 70, PW, 500, band, 14)
    s.badge(x0 + 30, 100, k + 1)
    s.both(x0 + 52, 107, th, en, "pl-label")
    s.text(x0 + 20, 142, code, "hk-mono")
for k in range(4):  # 1. a row at a time, a pointer on row 3
    y = 168 + k * 50
    x0 = 20
    s.box(x0 + 60, y, 280, 40, "rc-res" if k < 2 else ("nt-out" if k == 2 else "ml-cell"), 6)
    s.text(x0 + 76, y + 26, f"{PRICE[k]} ÷ {DUR[k]}", "dg-cell")
    if k < 2:
        s.text(x0 + 326, y + 26, f"= {PER[k]} ✓", "dg-cell", "end")
s.arrow(x0 + 20, 168 + 2 * 50 + 20, x0 + 54, 168 + 2 * 50 + 20)
s.both(x0 + 60, 384, "ทีละแถว: แถว 3 จาก 20,000", "one row at a time: row 3 of 20,000", "pl-note")
s.both(x0 + 60, 410, "ทุกรอบสร้าง row ใหม่ทั้งแถว", "each turn builds a whole row object", "pl-note")
x0 = 20 + PW + 21  # 2. rows go into a function, one by one
for k in range(4):
    y = 168 + k * 50
    s.box(x0 + 20, y, 120, 40, "rc-res" if k < 2 else "ml-cell", 6)
    s.text(x0 + 80, y + 26, f"{PRICE[k]}, {DUR[k]}", "dg-cell", "middle")
s.box(x0 + 200, 222, 140, 84, "ml-model", 12)
s.text(x0 + 270, 258, "lambda row:", "ml-model-text", "middle")
s.text(x0 + 270, 284, "price / dur", "ml-model-sub", "middle")
s.arrow(x0 + 146, 288, x0 + 194, 270)
s.both(x0 + 20, 384, "สั้นกว่า แต่ข้างใน pandas", "shorter, but inside pandas still", "pl-note")
s.both(x0 + 20, 410, "ยังเรียกฟังก์ชันทีละแถว", "calls the function once per row", "pl-note")
x0 = 20 + 2 * (PW + 21)  # 3. one operation on two whole columns
for c, (vals, head) in enumerate(((PRICE, "price"), (DUR, "duration"), (PER, "per_hour"))):
    x = x0 + 20 + c * 118
    s.text(x + 44, 172, head, "ml-box-h", "middle")
    s.box(x, 182, 88, 4 * 44 + 40, "rc-res" if c == 2 else "nt-out", 8)
    for r, v in enumerate(vals):
        s.text(x + 44, 210 + r * 44, v, "dg-cell", "middle")
    s.text(x + 44, 210 + 4 * 44, "…", "dg-cell", "middle")
s.text(x0 + 118, 300, "÷", "ml-plus", "middle")
s.text(x0 + 236, 300, "=", "ml-plus", "middle")
s.both(x0 + 20, 428, "หารทั้ง 20,000 แถวในคำสั่งเดียว", "all 20,000 rows in one operation", "pl-note")
# the timings, one shared scale
for k, (t, use_th, use_en, cls) in enumerate((
        (T_LOOP, "ใช้เมื่อ: แทบไม่ควรใช้", "use it: almost never", "ml-neg"),
        (T_APPLY, "ใช้เมื่อ: ไม่มีคำสั่งสำเร็จรูป เช่น def ของเรา", "use it: no built-in, e.g. your own def", "pl-label"),
        (T_VEC, "ใช้เมื่อ: บวกลบคูณหาร เปรียบเทียบ .str", "use it: arithmetic, comparisons, .str", "ml-ok"))):
    x0 = 20 + k * (PW + 21)
    s.box(x0 + 20, 456, PW - 40, 18, "ml-cell", 4)
    s.box(x0 + 20, 456, max(3, (PW - 40) * t / T_LOOP), 18, "ml-bar-top" if k == 0 else "ml-bar", 4)
    s.text(x0 + 20, 506, f"{t:g} ms", cls)
    s.both(x0 + 20, 546, use_th, use_en, "pl-note")
s.both(20, 596, f"เวลาจากการรันในบทนี้ (ต่างกันได้ในแต่ละเครื่อง) · ทั้งคอลัมน์เร็วกว่า loop ประมาณ {round(T_LOOP / T_VEC, -2):,.0f} เท่า",
       f"Timings from this lesson's run (they vary by computer) · the whole column is about {round(T_LOOP / T_VEC, -2):,.0f}× faster than the loop",
       "pl-note")
s.save("l10-three-ways.svg", 612)


# ================================================================ S27 (exercise): what each step does to real rows; the count stays hidden
s = svg("The task on three real rows of reviews. Step 1 works on a copy. Step 2: review_clean is Review with outer spaces "
        "removed, in lower case ('On my Bali…' becomes 'on my bali…'). Step 3: AR0006 has no review text, so its row is dropped. "
        "Step 4: AR0009 has text but no rating; its NaN stays. Step 5: the index is renumbered 0, 1, 2… "
        "How many rows usable_text has is left for you to predict.")
s.both(20, 34, "reviews (200 แถว)", "reviews (200 rows)", "pl-label")
s.both(640, 34, "usable_text (? แถว)", "usable_text (? rows)", "pl-label")
COLS27 = [("", 50), ("Review ID", 100), ("Review", 280), ("Rating", 84)]
LEFT27 = [(0, "AR0001", "On my Bali to Jakarta trip, …", "3.5"), None, (5, "AR0006", None, "2.5"), None,
          (8, "AR0009", "Tokyo to Singapore. The …", None)]
RIGHT27 = [(0, "AR0001", "on my bali to jakarta trip, …", "3.5"), None, ("?", "AR0009", "tokyo to singapore. the …", None)]
HY, RH = 70, 44


def table27(x0, rows, clean):
    x = x0
    for c, (name, cw) in enumerate(COLS27):
        name = "review_clean" if (clean and c == 2) else name
        if name:
            s.box(x, HY, cw - 4, 36, "nt-out" if (clean and c == 2) else "dg-xl-head", 6)
            s.text(x + (cw - 4) / 2, HY + 25, name, "ml-box-h", "middle")
        for r, row in enumerate(rows):
            y = HY + 44 + r * RH
            if row is None:
                if c == 0:
                    s.text(x + 23, y + 22, "…", "pl-label", "middle")
                continue
            v = row[c]
            drop = row[1] == "AR0006"
            s.box(x, y, cw - 4, 38, "sw-chip-warn" if drop else ("dg-hl-index" if c == 0 else "ml-cell"), 5)
            s.text(x + (cw - 4) / 2, y + 25, "NaN" if v is None else str(v),
                   "dg-nan" if v is None else ("pl-label" if v == "?" else ("dg-index" if c == 0 else "dg-cell")), "middle")
        x += cw


table27(20, LEFT27, False)
table27(640, RIGHT27, True)
s.arrow(546, HY + 63, 628, HY + 63)
s.badge(587, HY + 38, 1)
s.badge(800, 50, 2)
s.text(820, 56, "strip() + lower()", "dg-code")
s.badge(548, HY + 44 + 2 * RH + 19, 3)
s.badge(548, HY + 44 + 4 * RH + 19, 4)
s.badge(624, HY + 44 + 2 * RH + 19, 5)
NOTES27 = [("copy: ไม่แก้ตาราง reviews เดิม", "copy: the original reviews stays as it is"),
           ("review_clean: ตัดช่องว่างหัวท้าย และเป็นตัวพิมพ์เล็ก", "review_clean: outer spaces removed, lower case"),
           ("ไม่มีข้อความรีวิว: ตัดแถวนี้ทิ้ง", "no review text: drop this row"),
           ("มีข้อความ แต่ไม่มีคะแนน: ปล่อย NaN ไว้", "text but no rating: leave the NaN"),
           ("เรียง index ใหม่ 0, 1, 2, … (AR0009 ได้เลขอะไร?)", "renumber the index 0, 1, 2, … (AR0009 gets which?)")]
for k, (th, en) in enumerate(NOTES27):
    x, y = (20, 362 + k * 34) if k < 3 else (640, 362 + (k - 3) * 34)
    s.badge(x + 13, y - 6, k + 1)
    s.both(x + 34, y, th, en, "ml-neg" if k == 2 else "pl-note")
s.save("l10-usable-text-task.svg", 440)


# ================================================================ S32 (exercise): the 8 rows tinted by airline, and the 3 steps
SMALL = [("AR0005", "Thai Airways", "9.0"), ("AR0006", "Japan Airlines", "2.5"), ("AR0007", "Japan Airlines", "8.0"),
         ("AR0009", "Japan Airlines", None), ("AR0015", "Bangkok Airways", "6.5"), ("AR0024", "AirAsia", "7.0"),
         ("AR0044", "Thai Airways", "4.0"), ("AR0046", "AirAsia", "4.5")]
TINT = {"Thai Airways": "rc-role", "Japan Airlines": "rc-ctx", "Bangkok Airways": "rc-res", "AirAsia": "rc-con"}
s = svg("The 8 rows of small as cards, one colour per airline: Thai Airways AR0005 9.0 and AR0044 4.0; Japan Airlines AR0006 "
        "2.5, AR0007 8.0 and AR0009 NaN; Bangkok Airways AR0015 6.5; AirAsia AR0024 7.0 and AR0046 4.5. Then the three steps: "
        "1 group by Airline Name and find size and mean, 2 keep airlines with at least 2 reviews, 3 sort the mean from high to "
        "low. The results are left for you to predict.")
for k, (rid, air, rating) in enumerate(SMALL):
    x, y = 20 + (k % 4) * 286, 14 + (k // 4) * 82
    s.box(x, y, 270, 70, TINT[air], 10)
    s.text(x + 16, y + 28, rid, "dg-index")
    s.text(x + 254, y + 29, rating or "NaN", "pl-label" if rating else "dg-nan", "end")
    s.text(x + 16, y + 56, air, "pl-text")
STEPS = [("group by Airline Name", "size · mean", "size · mean"),
         ("keep size ≥ 2", "สายการบินไหนเหลือ", "which airlines stay?"),
         ("sort mean ↓", "เรียงอย่างไร", "in what order?")]
for k, (code, th, en) in enumerate(STEPS):
    x = 20 + k * 386
    s.box(x, 196, 364, 96, "nt-band-a", 12)
    s.badge(x + 28, 226, k + 1)
    s.text(x + 50, 233, code, "hk-mono")
    s.both(x + 50, 270, th + " = ?", en + " = ?", "pl-note")
    if k < 2:
        s.arrow(x + 366, 244, x + 384, 244)
s.save("l10-report-task.svg", 306)


# ================================================================ S41: which keys find a partner
LEFT = [("R1", "VietJet Air", "6.0"), ("R2", "Garuda Indonesia", "7.5"), ("R3", "VietJet Air", "8.0"), ("R4", "Lion Air", "5.0")]
RIGHT = [("VietJet Air", "Vietnam"), ("Garuda Indonesia", "Indonesia"), ("Scoot", "Singapore")]
s = svg("The two practice tables joined on the key Airline Name. my_reviews: R1 VietJet Air, R2 Garuda Indonesia, R3 VietJet Air, "
        "R4 Lion Air. my_airlines: VietJet Air Vietnam, Garuda Indonesia Indonesia, Scoot Singapore. R1 and R3 meet VietJet Air, "
        "R2 meets Garuda Indonesia; Lion Air has no partner on the right, and Scoot has no partner on the left.")
s.bubble(W / 2, 8, "รีวิวไหนหาประเทศของสายการบินเจอ (key = Airline Name)", "Which reviews find their airline's country? (key = Airline Name)", 680)
LX, RX, Y0, RH = 40, 700, 130, 56
s.text(LX, Y0 - 40, "my_reviews", "hk-mono")
s.text(RX, Y0 - 40, "my_airlines", "hk-mono")
s.text(LX + 286, Y0 - 12, "key", "pl-note", "middle")
s.text(RX + 105, Y0 - 12, "key", "pl-note", "middle")
for k, (rid, air, rating) in enumerate(LEFT):  # Review ID | Rating | Airline Name: the key faces the other table
    y = Y0 + k * RH
    s.box(LX, y, 60, RH - 10, "dg-hl-index", 6)
    s.text(LX + 30, y + 30, rid, "dg-index", "middle")
    s.box(LX + 66, y, 110, RH - 10, "ml-cell", 6)
    s.text(LX + 121, y + 30, rating, "dg-cell", "middle")
    s.box(LX + 182, y, 210, RH - 10, "sw-chip-warn" if air == "Lion Air" else "nt-out", 6)
    s.text(LX + 287, y + 30, air, "pl-text", "middle")
for k, (air, country) in enumerate(RIGHT):
    y = Y0 + k * RH
    s.box(RX, y, 210, RH - 10, "sw-chip-warn" if air == "Scoot" else "nt-out", 6)
    s.text(RX + 105, y + 30, air, "pl-text", "middle")
    s.box(RX + 216, y, 130, RH - 10, "ml-cell", 6)
    s.text(RX + 281, y + 30, country, "dg-cell", "middle")
for k, (rid, air, _) in enumerate(LEFT):
    for j, (air2, _) in enumerate(RIGHT):
        if air == air2:
            s.line(LX + 396, Y0 + k * RH + 23, RX - 4, Y0 + j * RH + 23)
s.both(LX + 404, Y0 + 3 * RH + 30, "← ไม่มีคู่ในตารางขวา", "← no partner on the right", "ml-neg")
s.both(RX + 10, Y0 + 3 * RH + 30, "↑ Scoot: ไม่มีรีวิวในตารางซ้าย", "↑ Scoot: no review on the left", "ml-neg")
s.save("l10-join-keys.svg", Y0 + 4 * RH + 20)
