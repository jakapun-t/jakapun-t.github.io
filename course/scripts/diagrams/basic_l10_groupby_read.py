"""nlp-basic L10 S29 opening picture: the question "which airline is rated best?" said in words, the groupby
chain piece by piece, and what you hold after each piece (Cathay Pacific's real numbers).
  l10-groupby-read.svg  S29

    course/.venv/bin/python scripts/diagrams/basic_l10_groupby_read.py courses/nlp-basic/images

Every number is computed here from courses/nlp-basic/data/airline_reviews.csv.
"""

import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from basic_svg import Svg  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
reviews = pd.read_csv(os.path.join(OUT, "..", "data", "airline_reviews.csv"))
g = reviews.groupby("Airline Name")["Rating"]
means = g.mean().sort_values(ascending=False)
cp = reviews.loc[reviews["Airline Name"] == "Cathay Pacific", "Rating"]
top, top_mean = means.index[0], means.iloc[0]
assert top == "Cathay Pacific"
first5 = ", ".join("NaN" if pd.isna(v) else f"{v:.1f}" for v in cp.head(5))

ROWS = [
    ("แยกรีวิวตามสายการบิน", "split the reviews by airline", 'reviews.groupby("Airline Name")',
     f"{len(reviews)} รีวิว → {g.ngroups} กลุ่ม (Cathay Pacific {len(cp)} รีวิว)",
     f"{len(reviews)} reviews → {g.ngroups} groups (Cathay Pacific: {len(cp)})"),
    ("ในแต่ละกลุ่ม ดูคอลัมน์คะแนน", "in each group, take the ratings", '["Rating"]',
     f"Cathay Pacific: {first5} …", f"Cathay Pacific: {first5} …"),
    ("หาค่าเฉลี่ย", "average them", ".mean()",
     f"Cathay Pacific {top_mean:g} ({cp.count()} คะแนน ข้าม NaN)",
     f"Cathay Pacific {top_mean:g} (skips NaN: {cp.count()} ratings)"),
    ("ปัดทศนิยม 2 ตำแหน่ง", "round to 2 decimals", ".round(2)", f"{top_mean:g} → {top_mean:.2f}", f"{top_mean:g} → {top_mean:.2f}"),
    ("เรียงจากมากไปน้อย", "best first", ".sort_values(ascending=False)",
     f"{top} {top_mean:.2f} อยู่บนสุด = คำตอบ", f"{top} {top_mean:.2f} on top: the answer"),
]

W = 1180
s = Svg(OUT, W, "The question 'which airline do travellers rate best?' in five pieces, each with its piece of code and "
                "what you hold after it: " + "; ".join(f"{en}: {code} gives {res}" for _, en, code, _, res in ROWS) + ".")
s.bubble(W / 2, 8, "คำถาม: สายการบินไหนได้คะแนนเฉลี่ยดีที่สุด?", "The question: which airline do travellers rate best?", 560)

XW, XC, XR = 20, 400, 790          # columns: the question in words, the code, what you hold now
s.both(XW + 44, 92, "คำถามเป็นคำพูด", "the question in words", "pl-note")
s.both(XC, 92, "โค้ด (อ่านจากบนลงล่าง)", "code (read top to bottom)", "pl-note")
s.both(XR, 92, "ตอนนี้ได้อะไร", "what you hold now", "pl-note")
for k, (th, en, code, rth, ren) in enumerate(ROWS):
    y = 106 + k * 60
    last = k == len(ROWS) - 1
    s.box(10, y, W - 20, 50, "rc-ctx" if last else "ml-cell", 10)
    s.badge(XW + 18, y + 25, k + 1)
    s.both(XW + 44, y + 32, th, en, "pl-label")
    s.arrow(XC - 34, y + 25, XC - 10, y + 25)
    s.text(XC, y + 32, code, "hk-mono")
    s.arrow(XR - 34, y + 25, XR - 10, y + 25)
    s.both(XR, y + 32, rth, ren, "pl-label" if last else "pl-note")
s.save("l10-groupby-read.svg", 106 + len(ROWS) * 60 + 6)
