"""Draws the lesson maps (big picture first) of nlp-basic lesson 10 (pandas) and lesson 11
(visualization): the problem, the parts, what each part changes, its tools, and a real result on
the airline reviews. Same look as the nlp lesson 11 map (scripts/diagrams/l11_figures.py).

    python3 scripts/diagrams/l10_l11_maps.py courses/nlp-basic/images

Every result is real: it is the output of the lesson's own code cells on data/airline_reviews.csv
(the numbers are repeated in the comments next to each part).

Uses the nt-*, pl-*, ml-*, sw-* and hk-* classes in templates/page.css.
"""

import os
import sys
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"


class Svg:
    def __init__(self, w, title):
        self.w, self.title, self.out = w, title, []

    def both(self, x, y, th, en, cls, anchor="start"):
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="th">{escape(th)}</text>')
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="en" lang="en">{escape(en)}</text>')

    def text(self, x, y, s, cls, anchor="start"):
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" lang="en">{escape(s)}</text>')

    def box(self, x, y, w, h, cls, rx=12):
        self.out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}"/>')

    def raw(self, s):
        self.out.append(s)

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


def part_box(s, x, y, w, part):
    tth, ten, cth, cen, tools, rth, ren = part
    s.box(x, y, w, 126, "ml-cell", rx=14)
    s.both(x + 20, y + 32, tth, ten, "nt-task")
    s.both(x + 20, y + 58, cth, cen, "hk-desc")
    s.text(x + 20, y + 84, tools, "pl-note")
    s.both(x + 20, y + 111, rth, ren, "ml-ok")


def draw_map(name, title, start, problem, heading, parts):
    """start: the pill on the left (a file name or a short label); problem: (th, en, note_th, note_en)."""
    s = Svg(900, title)
    s.box(20, 16, 300, 54, "ml-cell", rx=27)
    s.text(170, 50, start, "hk-mono", "middle")
    s.raw('<path d="M330 43 L366 43" class="nt-arrow"/><path d="M358 36 L367 43 L358 50" class="nt-arrow"/>')
    s.box(376, 10, 504, 66, "sw-warn-box", rx=12)
    s.both(394, 38, problem[0], problem[1], "nt-task")
    s.both(394, 64, problem[2], problem[3], "pl-note")
    s.both(450, 112, heading[0], heading[1], "nt-head", "middle")
    for k, part in enumerate(parts[:-1]):
        part_box(s, 20 + (k % 2) * 440, 128 + (k // 2) * 138, 420, part)
    part_box(s, 20, 128 + 2 * 138, 860, parts[-1])
    s.save(name, 128 + 2 * 138 + 126 + 14)


# ---------------------------------------------------------------- lesson 10: pandas
# 2: reviews.shape (200, 14); reviews["Rating"].count() 188          (S09, S21)
# 3: (reviews["Airline Name"] == "Thai Airways").sum() 26             (S02)
# 4: Delay Minutes missing before 14, after filling from the text 10  (S24)
# 5: groupby("Airline Name")["Rating"].mean(): Cathay Pacific 7.28 first, Japan Airlines 6.04 last (S29)
# 6: verified reviews by Country: Hong Kong 7.62, Thailand 6.92, Indonesia 6.36 (S39)
draw_map(
    "l10-map-lesson.svg",
    "Lesson map. The problem: 200 raw airline reviews in a CSV file, and the question which airline travellers rate "
    "best. Five parts: 2 load and look (200 rows, 14 columns, 188 ratings), 3 select (Thai Airways: 26 reviews), "
    "4 change and clean (delay gaps 14 to 10, read from the text), 5 summarise (Cathay Pacific best, 7.28), "
    "6 combine and reshape (by country, Hong Kong first, 7.62).",
    "airline_reviews.csv",
    ("1 ปัญหา: สายการบินไหนได้คะแนนดีที่สุด", "1 The problem: which airline is rated best?",
     "รีวิวดิบ 200 รายการ: คะแนนว่าง 12 ช่อง ข้อความไม่เรียบร้อย", "200 raw reviews: 12 ratings missing, messy text"),
    ("5 ขั้นจากไฟล์ดิบสู่คำตอบ", "Five steps from a raw file to the answer"),
    [
        ("2 โหลดและสำรวจ", "2 Load and look", "ไฟล์ CSV → DataFrame ที่สำรวจได้", "A CSV file becomes a DataFrame",
         "read_csv · shape · info · column types", "200 แถว × 14 คอลัมน์ · คะแนน 188 ค่า", "200 rows × 14 columns · 188 ratings"),
        ("3 เลือกแถวและคอลัมน์", "3 Select rows and columns", "เก็บเฉพาะส่วนที่คำถามต้องใช้", "Keep what the question needs",
         ".loc · .iloc · conditions with & | ~", "เฉพาะ Thai Airways: 26 รีวิว", "Thai Airways only: 26 reviews"),
        ("4 แก้และทำความสะอาด", "4 Change and clean", "เติมค่าว่าง แก้ข้อความ เพิ่มคอลัมน์ (บน copy)",
         "Fill gaps, tidy text, add columns (on a copy)", ".copy · isna · fillna · .str · apply",
         "Delay Minutes ว่าง 14 → 10 (อ่านจากข้อความ)", "Delay gaps 14 → 10, read from the text"),
        ("5 สรุป", "5 Summarise", "ตัวเลขเดียวต่อกลุ่ม ไม่ใช่ต่อแถว", "One number per group, not per row",
         "count · mean · groupby · agg", "อันดับ 1: Cathay Pacific 7.28 ✓", "Best rated: Cathay Pacific, 7.28 ✓"),
        ("6 รวมและจัดรูปตาราง", "6 Combine and reshape", "เพิ่มตารางที่สอง (ประเทศ) แล้วเปลี่ยนรูปตาราง",
         "Add a second table (countries), then reshape", "merge · concat · pivot_table · melt · explode",
         "ตามประเทศ (รีวิวที่ verified): Hong Kong 7.62 · Thailand 6.92 · Indonesia 6.36 ✓",
         "By country (verified reviews): Hong Kong 7.62 · Thailand 6.92 · Indonesia 6.36 ✓"),
    ],
)

# ---------------------------------------------------------------- lesson 11: visualization
# 1: Ticket Price mean 489.80, median 268.945                          (S09)
# 2: mean Rating by Seat Type: Premium Economy 7.40 highest             (S08)
# 3: price median $269, max $3,248.58 (AR0126)                         (S03, S09)
# 4: corr(duration, price) 0.73; reviews per year peak 2025, 32         (S12, S13)
# 5: Cathay Pacific 7.28, Japan Airlines 6.04: an axis from 6 hides it  (S16)
# 6: widest price spread by seat type (box plot): Business, IQR $1,393.82 (S17)
draw_map(
    "l11-map-lesson.svg",
    "Lesson map. The problem: summary numbers hide shape; the mean ticket is $489.80 but the median $268.95. "
    "Five parts: 2 questions about groups (Premium Economy rated highest, 7.40), 3 how one number spreads (median "
    "$269, tail to $3,248.58), 4 two numbers or time (longer flights cost more, most reviews in 2025), 5 clear and "
    "honest charts (a bar axis from 0), 6 from a question to a chart with AI (widest price spread: Business).",
    "reviews",
    ("1 ปัญหาและเครื่องมือ", "1 The problem and the tools",
     "ตัวเลขสรุปซ่อนรูปร่าง: ราคา mean $489.80 แต่ median $268.95", "A summary hides shape: mean $489.80, median $268.95"),
    ("เลือกกราฟจากคำถาม แล้ววาดให้ชัดและไม่หลอกตา", "Pick the chart from the question, then draw it clearly and honestly"),
    [
        ("2 คำถามเรื่องกลุ่ม", "2 Questions about groups", "หนึ่งแท่งต่อหนึ่งกลุ่ม", "One bar per group",
         "countplot · barplot · 100% stacked bar", "Premium Economy คะแนนเฉลี่ยสูงสุด 7.40", "Premium Economy rates highest: 7.40"),
        ("3 ตัวเลขหนึ่งคอลัมน์กระจายอย่างไร", "3 How one number spreads", "ค่าส่วนใหญ่อยู่ไหน กระจายกว้างแค่ไหน",
         "Where values sit, how far they spread", "histplot · kdeplot · ecdfplot · boxplot",
         "ราคา: median $269 หางยาวถึง $3,248.58", "Prices: median $269, tail to $3,248.58"),
        ("4 ตัวเลขสองคอลัมน์ หรือเวลา", "4 Two numbers, or time", "สองคอลัมน์ในกราฟเดียว", "Two columns on one chart",
         "scatterplot · lineplot", "บินนานยิ่งแพง · ปี 2025 รีวิวมากสุด (32)", "Longer flights cost more · 2025 peaks (32)"),
        ("5 กราฟที่ชัดและไม่หลอกตา", "5 Clear and honest charts", "ชื่อกราฟ ชื่อแกน แกนแท่งเริ่มที่ 0",
         "Titles, axis labels, a bar axis from 0", "plt.title · plt.xlabel · plt.ylabel",
         "Cathay 7.28 กับ JAL 6.04: เริ่มที่ 0 จึงได้สัดส่วน", "Cathay 7.28 vs JAL 6.04: from 0, in proportion"),
        ("6 จากคำถามสู่กราฟ ด้วย AI", "6 From a question to a chart, with AI",
         "คำถาม → คอลัมน์ → กราฟ → prompt → ตรวจ", "Question → columns → chart → prompt → check",
         "a 5-part prompt template · ask AI for a chart, then check its reasons",
         "ราคาชั้นไหนกระจายกว้างสุด? → box plot → Business (ครึ่งกลางกว้าง $1,394) ✓",
         "Which seat type's prices spread widest? → box plot → Business (middle half spans $1,394) ✓"),
    ],
)
