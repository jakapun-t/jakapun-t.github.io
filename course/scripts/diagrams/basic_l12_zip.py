"""nlp-basic L12-S22: how zip(toks, toks[1:]) makes bigrams, as a picture.
toks on top, toks[1:] (the same list without its first word) underneath, lined up by position; each column becomes one
pair, and the last word has no partner, so zip stops.
  l12-zip.svg  S22

    python3 scripts/diagrams/basic_l12_zip.py courses/nlp-basic/images
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from basic_svg import Svg  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
TOKS = ["รอ", "นาน", "มาก", "แต่"]
W = 1180
X0, DX, CW, CH = 380, 170, 130, 44      # first column x, column step, chip width/height
YA, YB, YR = 150, 250, 400              # rows: toks, toks[1:], result

s = Svg(OUT, W, "How zip(toks, toks[1:]) makes bigrams. toks is รอ นาน มาก แต่; toks[1:] is the same list without its first "
                "word: นาน มาก แต่. Lined up by position, each column is one pair: (รอ, นาน), (นาน, มาก), (มาก, แต่). The last "
                "word แต่ has no partner underneath, so zip stops: 4 words give 3 pairs.")
s.bubble(W / 2, 8, "zip เดินไปบนสองลิสต์พร้อมกัน แล้วจับของตำแหน่งเดียวกันเป็นคู่",
         "zip walks two lists together and pairs the items at the same position", 760)


def cx(i):
    return X0 + i * DX + CW / 2


def chip(i, y, word, cls="pl-chip"):
    s.box(cx(i) - CW / 2, y - CH / 2, CW, CH, cls, 10)
    s.thai(cx(i), y + 8, word, "pl-chip-text", "middle")


# column frames for the 3 pairs, and the lonely 4th column
for i in range(3):
    s.box(cx(i) - CW / 2 - 12, YA - CH / 2 - 34, CW + 24, YB - YA + CH + 46, "dg-row", 14)
    s.both(cx(i), YA - CH / 2 - 14, f"คู่ที่ {i + 1}", f"pair {i + 1}", "pl-note", "middle")
s.box(cx(3) - CW / 2 - 12, YA - CH / 2 - 34, CW + 24, YB - YA + CH + 46, "sw-warn-box", 14)
s.both(cx(3), YA - CH / 2 - 14, "ไม่มีคู่", "no partner", "ml-neg", "middle")

# row labels
s.text(40, YA + 8, "toks", "hk-mono")
s.text(40, YB + 8, "toks[1:]", "hk-mono")
s.both(40, YB + 36, "ตัดคำแรกออก", "first word cut off", "pl-note")

# the two lists
for i, w in enumerate(TOKS):
    chip(i, YA, w)
for i, w in enumerate(TOKS[1:]):
    chip(i, YB, w)
# the word that toks[1:] drops, shown crossed out to the left of the lower row
gx, gw = 285, 90
s.box(gx - gw / 2, YB - CH / 2, gw, CH, "pl-chip", 10, ' style="opacity:.35"')
s.thai(gx, YB + 8, TOKS[0], "pl-chip-text", "middle")
s.line(gx - gw / 2 - 4, YB + CH / 2 + 2, gx + gw / 2 + 4, YB - CH / 2 - 2, "pl-line")
s.both(cx(3), YB + 8, "(หมดแล้ว)", "(empty)", "pl-note", "middle")

# arrows down to the pairs
for i in range(3):
    s.arrow(cx(i), YB + CH / 2 + 18, cx(i), YR - 30)
    s.box(cx(i) - 78, YR - 22, 156, 44, "nt-band-a", 10)
    s.text(cx(i), YR + 8, f"('{TOKS[i]}', '{TOKS[i + 1]}')", "hk-mono", "middle")
s.both(cx(3), YR + 8, "zip หยุดที่นี่", "zip stops here", "ml-neg", "middle")
s.text(40, YR + 8, "zip(...)", "hk-mono")
s.both(W / 2, YR + 64, "4 คำ → 3 คู่ (เท่ากับ range(len(toks) - 1) ในแบบวน for)",
       "4 words → 3 pairs (the same as range(len(toks) - 1) in the for-loop version)", "pl-label", "middle")
s.save("l12-zip.svg", YR + 84)
