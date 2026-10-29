"""stats-dh L12 S04 recap picture: text → TF (word counts) × IDF (how rare each word is) = TF-IDF, on three short
made-up wine notes, laid out as one equation with the same word columns all the way down.
  l12-tfidf-steps.svg  S04

    course/.venv/bin/python scripts/diagrams/stats_l12_tfidf.py courses/stats-dh/images

Every number comes from sklearn: CountVectorizer() for TF, TfidfVectorizer(norm=None) for IDF and TF × IDF, and the
default TfidfVectorizer() for the last line (each row scaled to length 1), the same settings as the lesson.
"""

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from stats_svg import Svg

NOTES = ["Fresh citrus wine, fresh finish.", "Ripe cherry wine.", "Fresh cherry wine."]
cv = CountVectorizer().fit(NOTES)
words = list(cv.get_feature_names_out())
tf = cv.transform(NOTES).toarray()
raw = TfidfVectorizer(norm=None).fit(NOTES)
idf = raw.idf_
tfidf = raw.transform(NOTES).toarray()
unit = TfidfVectorizer().fit_transform(NOTES).toarray()
df = (tf > 0).sum(0)
n = len(NOTES)
assert words == ["cherry", "citrus", "finish", "fresh", "ripe", "wine"], words

W = 1100
TXT, HOT = "var(--tag-concept-dot)", "var(--accent)"
FRESH, WINE = words.index("fresh"), words.index("wine")
CW, LW = 68, 78                     # word column width, row-label width
PX = (10, 574)                      # left (TF) and right (TF-IDF) panels
PW = LW + 6 * CW + 30


def cx(p, j):
    return PX[p] + 20 + LW + j * CW + CW / 2


def grid(s, p, y, vals, fmt, hot):
    for j, w in enumerate(words):
        s.box(cx(p, j) - CW / 2 + 3, y, CW - 6, 26, "pl-chip", 6)
        s.text(cx(p, j), y + 18, w, "mp-c", "middle")
    for i in range(n):
        yy = y + 32 + i * 32
        s.line(PX[p] + 20, yy, PX[p] + PW - 10, yy, "mp-guide")
        s.both(PX[p] + 20, yy + 22, f"โน้ต {i + 1}", f"note {i + 1}", "mp-s")
        for j in range(len(words)):
            v = vals[i][j]
            if (i, j) in hot:
                s.box(cx(p, j) - CW / 2 + 8, yy + 3, CW - 16, 26, "rc-ctx", 6)
            s.text(cx(p, j), yy + 22, fmt(v), "mp-n" if v else "mp-s", "middle")


s = Svg(W, f"Three short wine notes made into numbers, one row per note, six word columns ({', '.join(words)}). "
           f"TF counts each word in each note (note 1: fresh 2, citrus 1, finish 1, wine 1). IDF weighs each word by how "
           f"rare it is across the notes: in 1 of 3 notes 1.69, in 2 of 3 1.29, in all 3 (wine) 1.00. TF-IDF = TF × IDF: "
           f"note 1 fresh 2 × 1.29 = 2.58, citrus 1.69, finish 1.69, wine 1.00.")
s.bubble("ข้อความ → TF → TF-IDF: คำทุกคำได้คอลัมน์ของตัวเอง", "Text → TF → TF-IDF: every word gets its own column")

# ① the text
s.badge(32, 86, 1)
x = 56
for i, note in enumerate(NOTES):
    w = 50 + len(note) * 9.4
    s.box(x, 68, w, 36, "rc-ctx", 8)
    s.both(x + 12, 92, f"โน้ต {i + 1}:", f"note {i + 1}:", "mp-s")
    s.text(x + 66, 92, note, "hk-desc")
    x += w + 14

# ② TF and the IDF row
Y = 120
s.panel(PX[0], Y, PW, 262, "ml-cell", "TF: นับว่าแต่ละคำอยู่ในโน้ตกี่ครั้ง", "TF: count each word in each note", 2)
grid(s, 0, Y + 50, tf, lambda v: f"{v}", {(0, FRESH)})
yi = Y + 50 + 32 + 3 * 32 + 8
s.box(PX[0] + 14, yi, PW - 28, 66, "nt-band-a", 8)
s.both(PX[0] + 22, yi + 24, "× IDF", "× IDF", "mp-acc")
s.both(PX[0] + 22, yi + 50, "อยู่ในกี่โน้ต", "in … notes", "mp-s")
for j in range(len(words)):
    if j == FRESH:
        s.box(cx(0, j) - CW / 2 + 8, yi + 5, CW - 16, 26, "rc-ctx", 6)
    s.text(cx(0, j), yi + 24, f"{idf[j]:.2f}", "mp-n", "middle")
    s.fill(cx(0, j) - 26, yi + 34, 52 * idf[j] / idf.max(), 5, HOT if df[j] == n else TXT, 2)
    s.text(cx(0, j), yi + 56, f"{df[j]} / {n}", "mp-s", "middle")

# arrow
s.arrow(PX[0] + PW + 6, Y + 130, PX[1] - 8, Y + 130)
s.text((PX[0] + PW + PX[1]) / 2, Y + 118, "=", "mp-acc", "middle")

# ③ TF-IDF
s.panel(PX[1], Y, PW, 262, "ml-cell", "TF-IDF = TF × IDF", "TF-IDF = TF × IDF", 3)
grid(s, 1, Y + 50, tfidf, lambda v: f"{v:.2f}" if v else "0", {(0, FRESH)})
s.both(PX[1] + 20, yi + 24, f"โน้ต 1, fresh: {tf[0][FRESH]} × {idf[FRESH]:.2f} = {tfidf[0][FRESH]:.2f}",
       f"note 1, fresh: {tf[0][FRESH]} × {idf[FRESH]:.2f} = {tfidf[0][FRESH]:.2f}", "mp-acc")
s.both(PX[1] + 20, yi + 52, "wine อยู่ทุกโน้ต ได้น้ำหนักน้อยสุด 1.00", "wine is in every note: lowest weight, 1.00", "mp-s")
s.save("l12-tfidf-steps.svg", Y + 262 + 10)
