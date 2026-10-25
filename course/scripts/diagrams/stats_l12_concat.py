"""Pictures for stats-dh L12 (text as data: one row from text and numbers), in the stats-dh card style. The lesson's
point: turn the text into a vector, turn the other columns into numbers, join them into one row, train on the row.
  l12-mixed-everywhere.svg  S01  six apps whose rows mix free text, numbers and categories
  l12-one-row-vector.svg    S01  three wines as a table (X features, y stars) → the same rows as numbers → Ridge
  l12-one-wine.svg          S03  wine 1 as a card (features and target) and the stars of all 1,000 wines
  l12-text-vectors.svg      S04  wine 1's note as TF-IDF (4,146 columns, ~34 non-zero) and as MiniLM (384 numbers)
  l12-sparse-vs-dense.svg   S04  sparse TF-IDF vs dense MiniLM: size, explainable, field words, synonyms, few labels, speed, R²
  l12-other-columns.svg     S05  price → log → scaled (wine 1: −0.93); country and grape → one-hot (24 + 132)
  l12-concat-row.svg        S06  the 541-number row of wine 1, block by block, and the 1,000 × 541 table
  l12-row-exercise.svg      S07  exercise: wines 1 and 3 and an empty shortened 10-column row to fill in
  l12-column-pipeline.svg   S08  the column transformer and Ridge inside each cross-validation round (R² 0.518)
  l12-r2-compare.svg        S09  R² of text alone, other columns alone and the joined rows
  l12-key-terms.svg         S11  six key terms with small drawings

    course/.venv/bin/python scripts/diagrams/stats_l12_concat.py courses/stats-dh/images

Every number is computed here from courses/stats-dh/data/l12_wines.csv with the lesson's settings: log price scaled,
OneHotEncoder(handle_unknown="ignore") on country and variety, all-MiniLM-L6-v2 or TfidfVectorizer() on description,
Ridge(), KFold(5, shuffle=True, random_state=42). The app tiles are everyday examples, not claims about how each app is
built. Uses the mp-*, ml-*, nt-*, rc-*, pl-*, hk-*, sw-*, dg-* classes in templates/page.css.
"""

import os
import warnings

import numpy as np
import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold, cross_val_predict, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from stats_svg import OUT, Svg, emoji_or_icon, term_grid, width

warnings.filterwarnings("ignore")
W = 1100
TXT, PRICE, CTRY, GRAPE = "var(--tag-concept-dot)", "var(--accent)", "var(--tag-exercise-dot)", "var(--tag-example-dot)"

# ---------------------------------------------------------------- data and models, as in the lesson
wines = pd.read_csv(os.path.join(os.path.dirname(OUT.rstrip("/")), "data", "l12_wines.csv"))
wines["log_price"] = np.log(wines["price"])
y = wines["stars"]
cv = KFold(5, shuffle=True, random_state=42)

from sentence_transformers import SentenceTransformer  # noqa: E402

minilm = SentenceTransformer("all-MiniLM-L6-v2")
emb = minilm.encode(wines["description"].tolist())
tfidf = TfidfVectorizer().fit(wines["description"])
T = tfidf.transform(wines["description"])
price_scaled = StandardScaler().fit_transform(wines[["log_price"]])[:, 0]
onehot = OneHotEncoder().fit(wines[["country", "variety"]])
n_country, n_grape = len(onehot.categories_[0]), len(onehot.categories_[1])

embed = FunctionTransformer(lambda notes: minilm.encode(list(notes)))
others = [(StandardScaler(), ["log_price"]), (OneHotEncoder(handle_unknown="ignore"), ["country", "variety"])]
blocks = {"tfidf": [(TfidfVectorizer(), "description")], "minilm": [(embed, "description")], "others": others}
blocks["tfidf+"] = blocks["tfidf"] + others
blocks["minilm+"] = blocks["minilm"] + others
r2 = {k: cross_val_score(make_pipeline(make_column_transformer(*b), Ridge()), wines, y, cv=cv, scoring="r2").mean()
      for k, b in blocks.items()}
preds = cross_val_predict(make_pipeline(make_column_transformer(*blocks["minilm+"]), Ridge()), wines, y, cv=cv)
pred1 = preds[0]
print({k: round(v, 3) for k, v in r2.items()}, "wine 1 predicted", round(pred1, 1))
w1 = wines.iloc[0]
ROW = 384 + 1 + n_country + n_grape


def chip_both(s, x, y, th, en, cls="ml-cell", fs=15):
    w = max(width(th, fs), width(en, fs)) + 20
    s.box(x, y, w, 28, cls, 14)
    s.both(x + w / 2, y + 19, th, en, "mp-chip", "middle")
    return w


def wrap(text, maxw, fs=17):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if width(t, fs) > maxw and line:
            out.append(line)
            line = w
        else:
            line = t
    return out + ([line] if line else [])


def strip(s, x, y, w, h, n, color, lit=(), values=None):
    """A block of n columns drawn as a strip w wide; values (−1..1) shade the cells, lit cells are solid."""
    cw = w / n
    s.box(x, y, w, h, "ml-cell", 3)
    for i in range(n):
        if values is not None:
            a = min(1, abs(values[i]) / 0.12)
            s.raw(f'<rect x="{x + i * cw:.2f}" y="{y}" width="{cw + 0.05:.2f}" height="{h}" '
                  f'style="fill:{color};fill-opacity:{0.08 + 0.85 * a:.2f}"/>')
        elif i in lit:
            s.fill(x + i * cw, y, max(cw, 2.5), h, color, 0)


def brace(s, x1, x2, y, th, en, cls="mp-c"):
    s.raw(f'<path d="M{x1:.1f} {y} v8 H{x2:.1f} v-8" class="mp-axis"/>')
    s.both((x1 + x2) / 2, y + 30, th, en, cls, "middle")


# ================================================================ S01 apps that mix text and numbers
APPS = [
    ("🛍", "ประกาศขายของ", "Shop listing", "ชื่อ · คำบรรยาย", "title · description", "ราคา · หมวด", "price · category", "ขายได้กี่ชิ้น", "units sold"),
    ("🔑", "ที่พักให้เช่า", "Holiday rental", "คำบรรยายห้อง", "room description", "ราคา · ทำเล", "price · area", "คะแนนรีวิว", "guest rating"),
    ("🏢", "ประกาศงาน", "Job advert", "รายละเอียดงาน", "job description", "เมือง · ประสบการณ์", "city · experience", "เงินเดือน", "salary"),
    ("🍽", "แอปส่งอาหาร", "Food delivery", "รีวิวของลูกค้า", "customer review", "เวลาส่ง · ร้าน", "delivery time · shop", "ดาว", "stars"),
    ("📚", "คลังห้องสมุด", "Library catalogue", "คำโปรยหนังสือ", "a book's blurb", "ปี · จำนวนหน้า", "year · pages", "หมวดหนังสือ", "genre"),
    ("⭐", "แอปรีวิวไวน์", "Wine app", "คำบรรยายรสชาติ", "tasting note", "ราคา · ประเทศ", "price · country", "ดาว", "stars"),
]
s = Svg(W, "Six everyday apps whose rows mix text, numbers and categories: a shop listing (title, description; price, "
           "category → units sold), a holiday rental (room description; price, area → guest rating), a job advert (job "
           "description; city, experience → salary), food delivery (customer review; delivery time, shop → stars), a "
           "library catalogue (blurb; year, pages → genre), a wine app (tasting note; price, country → stars).")
s.bubble("ข้อมูลจริงมีทั้งข้อความ ตัวเลข และกลุ่มในแถวเดียวกัน", "Real rows hold text, numbers and categories side by side")
TW, TG, TH_ = 352, 12, 196
for k, (ic, nth, nen, tth, ten, oth, oen, pth, pen) in enumerate(APPS):
    x, yy = 10 + (k % 3) * (TW + TG), 72 + (k // 3) * (TH_ + 14)
    s.box(x, yy, TW, TH_, "ml-cell", 14)
    s.raw(f'<circle cx="{x + 42}" cy="{yy + 42}" r="28" style="fill:var(--tag-concept-bg)"/>')
    emoji_or_icon(s, ic, x + 42, yy + 42, 48)
    s.both(x + 84, yy + 50, nth, nen, "mp-t")
    for j, (lth, len_, a, b, cls) in enumerate([("ข้อความ", "text", tth, ten, "rc-ctx"),
                                                ("คอลัมน์อื่น", "other columns", oth, oen, "ml-cell-b"),
                                                ("ทำนาย", "predicts", pth, pen, "ml-cell")]):
        yj = yy + 86 + j * 36
        s.both(x + 18, yj + 19, lth, len_, "mp-s")
        chip_both(s, x + 126, yj, a, b, cls)
s.save("l12-mixed-everywhere.svg", 72 + 2 * TH_ + 14 + 10)

# ================================================================ S01 a few wines → X and y → Ridge
SHOW = wines.head(3)
s = Svg(W, "Three real wines as a table: the tasting note, price, country and grape are the features X; stars is the "
           "target y. " + "; ".join(f"wine {r.wine_id}: {r.country}, {r.variety}, ${r.price:.0f}, {r.stars} stars"
                                    for r in SHOW.itertuples()) +
        f". Each feature column becomes numbers (384 MiniLM numbers, 1 scaled log price, {n_country} country and "
        f"{n_grape} grape one-hot columns), joined into one row of {ROW} numbers per wine: X is 1,000 × {ROW}, y is the "
        f"1,000 star ratings. Ridge learns X → y; with cross-validation it predicts " +
        ", ".join(f"{p_:.1f}" for p_ in preds[:3]) + " for these three wines.")
s.bubble("ไวน์แต่ละขวดมีทั้งคำ ราคา และกลุ่ม โมเดลจะใช้ทั้งหมดได้อย่างไร", "Each wine has words, a price and groups: how can one model use them all?")
# ① the data
TX = [(10, 470, "คำบรรยาย", "description"), (488, 86, "ราคา", "price"), (582, 110, "ประเทศ", "country"),
      (700, 190, "องุ่น", "variety")]
YX, YW = 920, 170
s.box(4, 66, 894, 34, "nt-band-a", 8)
s.both(18, 89, "X = feature: สิ่งที่รู้ของแต่ละขวด", "X = features: what we know about each wine", "mp-p")
s.box(YX - 6, 66, YW + 12, 34, "rc-ctx", 8)
s.both(YX + YW / 2, 89, "y = target: คำตอบ", "y = target: the answer", "mp-p", "middle")
for x, w, th, en in TX:
    s.both(x + 6, 124, th, en, "mp-s")
s.both(YX + 6, 124, "stars", "stars", "mp-s")
for i, r in enumerate(SHOW.itertuples()):
    yy = 132 + i * 38
    s.line(4, yy, 1094, yy, "mp-guide")
    s.text(x0 := 16, yy + 25, r.description[:52] + "…", "hk-desc")
    s.text(494, yy + 25, f"${r.price:.0f}", "hk-desc")
    s.text(588, yy + 25, r.country, "hk-desc")
    s.text(706, yy + 25, r.variety, "hk-desc")
    s.text(YX + YW / 2, yy + 25, f"{r.stars:.1f}", "mp-n", "middle")
s.both(16, 268, "… รวม 1,000 ขวด", "… 1,000 wines in all", "mp-s")
s.arrow(450, 258, 450, 290)
s.both(470, 282, "แปลงแต่ละคอลัมน์เป็นตัวเลข แล้วต่อกันเป็นแถวเดียว", "turn each column into numbers, then join them into one row", "mp-acc")
# ② the same rows as numbers
SEG = [(10, 470, "MiniLM 384"), (488, 86, "1"), (582, 110, f"{n_country}"), (700, 190, f"{n_grape}")]
s.both(16, 316, "MiniLM: 384 ตัวเลข", "MiniLM: 384 numbers", "mp-s")
s.both(494, 316, "ราคา: 1", "price: 1", "mp-s")
s.both(588, 316, f"ประเทศ: {n_country}", f"country: {n_country}", "mp-s")
s.both(706, 316, f"องุ่น: {n_grape}", f"grape: {n_grape}", "mp-s")
for i, r in enumerate(SHOW.itertuples()):
    yy = 326 + i * 38
    k = r.Index
    strip(s, 10, yy, 470, 28, 384, TXT, values=emb[k])
    s.box(488, yy, 86, 28, "ml-cell-b", 4)
    s.text(531, yy + 20, f"{price_scaled[k]:.2f}", "mp-c", "middle")
    strip(s, 582, yy, 110, 28, n_country, CTRY, lit={list(onehot.categories_[0]).index(r.country)})
    strip(s, 700, yy, 190, 28, n_grape, GRAPE, lit={list(onehot.categories_[1]).index(r.variety)})
    s.box(YX, yy, YW, 28, "rc-ctx", 4)
    s.text(YX + YW / 2, yy + 20, f"{r.stars:.1f}", "mp-n", "middle")
s.raw('<path d="M10 446 v8 H890 v-8" class="mp-axis"/>')
s.both(450, 476, f"X: 1,000 แถว × {ROW} ตัวเลข", f"X: 1,000 rows × {ROW} numbers", "pl-label", "middle")
s.raw(f'<path d="M{YX} 446 v8 H{YX + YW} v-8" class="mp-axis"/>')
s.both(YX + YW / 2, 476, "y: คะแนนดาว 1,000 ค่า", "y: 1,000 star ratings", "pl-label", "middle")
# ③ train
s.box(380, 496, 220, 46, "ml-model", 10)
s.both(490, 526, "Ridge เรียน X → y", "Ridge learns X → y", "ml-model-text", "middle")
s.arrow(604, 519, 650, 519)
s.both(660, 514, "ทำนาย (cross-validation): " + " · ".join(f"{p_:.1f}" for p_ in preds[:3]),
       "predicted (cross-validation): " + " · ".join(f"{p_:.1f}" for p_ in preds[:3]), "mp-t")
s.both(660, 538, "จริง: " + " · ".join(f"{v:.1f}" for v in SHOW.stars), "actual: " + " · ".join(f"{v:.1f}" for v in SHOW.stars), "mp-s")
s.save("l12-one-row-vector.svg", 556)

# ================================================================ S03 wine 1 and all stars
s = Svg(W, f"Wine 1 as a card: features (the tasting note, price ${w1.price:.0f}, {w1.country}, {w1.variety}) and the "
           f"target, {w1.stars} stars ({w1.points} points out of 100). Right: the stars of all 1,000 wines, from "
           f"{y.min():.1f} to {y.max():.1f}, most between 3.5 and 4.2 (mean {y.mean():.2f}).")
s.bubble("หนึ่งแถว = ไวน์หนึ่งขวด ทำนายคะแนนดาวของนักวิจารณ์", "One row = one wine: predict the critic's stars")
s.panel(10, 70, 620, 320, "ml-cell", "ไวน์ขวดที่ 1", "Wine 1", 1)
s.box(30, 112, 580, 150, "nt-band-a", 10)
s.both(46, 138, "feature: คำบรรยาย ราคา ประเทศ องุ่น", "features: note, price, country, grape", "mp-p")
for i, ln in enumerate(wrap(w1.description, 550)):
    s.text(46, 166 + i * 24, ln, "hk-desc")
for i, (th, en, v) in enumerate([("ราคา", "price", f"${w1.price:.0f}"), ("ประเทศ", "country", w1.country), ("องุ่น", "variety", w1.variety)]):
    x = 30 + i * 150
    s.box(x, 274, 140, 52, "ml-cell", 8)
    s.both(x + 70, 294, th, en, "mp-s", "middle")
    s.text(x + 70, 318, v, "mp-n", "middle")
s.box(490, 274, 120, 52, "rc-ctx", 8)
s.both(550, 292, "target: stars", "target: stars", "mp-s", "middle")
s.text(550, 320, f"{w1.stars:.1f} ★", "mp-big", "middle")
s.both(30, 360, f"{w1.points} คะแนนจาก 100 → ({w1.points} − 50) / 10 = {w1.stars:.1f} ดาว", f"{w1.points} points out of 100 → ({w1.points} − 50) / 10 = {w1.stars:.1f} stars", "mp-s")
s.panel(650, 70, 440, 320, "ml-cell", "คะแนนดาวของไวน์ทั้ง 1,000 ขวด", "Stars of all 1,000 wines", 2)
vc = y.round(1).value_counts().sort_index()
mx = vc.max()
for v, c in vc.items():
    bx = 676 + (v - 3.0) * 10 * 22
    h = c / mx * 200
    s.fill(bx, 340 - h, 18, h, "var(--accent)" if abs(v - w1.stars) < 1e-9 else "var(--tag-concept-dot)", 2)
for v in (3.0, 3.5, 4.0, 4.5):
    s.text(676 + (v - 3.0) * 220 + 9, 362, f"{v:.1f}", "mp-s", "middle")
s.both(676, 384, f"เฉลี่ย {y.mean():.2f} ดาว · ส้ม = ขวดที่ 1 ({w1.stars:.1f})", f"mean {y.mean():.2f} stars · orange = wine 1 ({w1.stars:.1f})", "mp-s")
s.save("l12-one-wine.svg", 402)

# ================================================================ S04 the note as two vectors
row1 = T[0].toarray()[0]
nz = np.nonzero(row1)[0]
names = tfidf.get_feature_names_out()
top = sorted(nz, key=lambda i: -row1[i])[:6]
s = Svg(W, f"Wine 1's note as two vectors. TF-IDF: {len(names):,} columns, one per word in all the notes; this note has "
           f"{len(nz)} non-zero columns, the highest {', '.join(f'{names[i]} {row1[i]:.2f}' for i in top[:4])}. MiniLM: "
           f"384 numbers, every one with a value (shown as shades).")
s.bubble("คำบรรยายหนึ่งชิ้น เป็นตัวเลขได้สองแบบ", "One tasting note, two ways to make it numbers")
s.box(10, 66, 1080, 50, "rc-ctx", 10)
s.text(26, 97, w1.description[:118] + "…", "hk-desc")
s.panel(10, 130, 1080, 150, "ml-cell", f"TF-IDF: {len(names):,} คอลัมน์ (หนึ่งคอลัมน์ต่อคำ)", f"TF-IDF: {len(names):,} columns (one per word)")
strip(s, 30, 176, 1040, 30, len(names), TXT, lit=set(nz))
x = 30
for i in top:
    w = width(f"{names[i]} {row1[i]:.2f}", 15) + 20
    s.box(x, 220, w, 28, "pl-chip", 6)
    s.text(x + w / 2, 239, f"{names[i]} {row1[i]:.2f}", "mp-c", "middle")
    x += w + 8
s.both(1070, 239, f"… มีค่าแค่ {len(nz)} คอลัมน์ ที่เหลือ 0", f"… only {len(nz)} have a value", "mp-acc", "end")
s.panel(10, 296, 1080, 120, "ml-cell", "MiniLM: 384 ตัวเลข (สีเข้ม = ค่าห่างจาก 0)", "MiniLM: 384 numbers (darker = further from 0)")
strip(s, 30, 342, 1040, 30, 384, TXT, values=emb[0])
s.both(30, 400, "ทุกตัวมีค่า และขวดที่ความหมายใกล้กันได้ vector ใกล้กัน", "every number has a value; wines with close meanings get close vectors", "mp-s")
s.save("l12-text-vectors.svg", 428)

# ================================================================ S04 sparse TF-IDF vs dense MiniLM
nnz_avg = T.nnz / T.shape[0]
ROWS_CMP = [  # (label th, en, tfidf th, en, ok?, minilm th, en, ok?)
    ("ขนาด", "size", f"{len(names):,} คอลัมน์ มีค่าราว {nnz_avg:.0f}", f"{len(names):,} columns, about {nnz_avg:.0f} non-zero",
     None, "384 ตัวเลข มีค่าทุกตัว", "384 numbers, all filled", None),
    ("อธิบายได้ไหม", "explainable?", "ได้: หนึ่งคอลัมน์ = หนึ่งคำ", "yes: one column = one word", True,
     "ไม่ได้: ตัวเลขไม่มีชื่อ", "no: the numbers have no names", False),
    ("คำเฉพาะทาง (tannins)", "field words (tannins)", "เรียนจากข้อมูลของเราเอง", "learns your data's own words", True,
     "รู้ภาษาทั่วไปมากกว่า", "knows general language better", False),
    ("คำพ้อง (fresh ≈ crisp)", "synonyms (fresh ≈ crisp)", "คนละคอลัมน์ ไม่เกี่ยวกัน", "separate, unrelated columns", False,
     "vector ใกล้กัน", "close vectors", True),
    ("ข้อมูลติดป้ายน้อย", "few labelled rows", "ต้องมีข้อมูลพอให้เรียนคำ", "needs enough rows to learn words", False,
     "ฝึกมาแล้วกว่า 1,000 ล้านคู่ประโยค", "pretrained on > 1 billion pairs", True),
    ("ความเร็ว (1,000 ขวด)", "speed (1,000 notes)", "0.02 วินาที", "0.02 s", True, "1.29 วินาที", "1.29 s", False),
]
s = Svg(W, f"Sparse TF-IDF against dense MiniLM on the 1,000 wine notes. Size: {len(names):,} columns with about "
           f"{nnz_avg:.0f} non-zero per note, against 384 numbers all filled. TF-IDF is explainable (one column per word), "
           "learns the data's own field words and is fast (0.02 s against 1.29 s for 1,000 notes); MiniLM puts synonyms "
           "close and works with few labelled rows because it is pretrained, but its numbers have no names. On these "
           f"notes alone R² is {r2['tfidf']:.3f} (TF-IDF) against {r2['minilm']:.3f} (MiniLM); joined with price, "
           f"country and grape {r2['tfidf+']:.3f} against {r2['minilm+']:.3f}.")
s.bubble("TF-IDF (sparse) หรือ MiniLM (dense): แบบไหนเหมาะกับงานไหน", "TF-IDF (sparse) or MiniLM (dense): which suits which job?")
C0, C1, C2 = 10, 250, 680
s.box(C1 - 6, 66, 420, 74, "nt-band-a", 12)
s.box(C2 - 6, 66, 416, 74, "rc-ctx", 12)
s.text(C1 + 10, 94, "TF-IDF (sparse)", "mp-t")
s.text(C2 + 10, 94, "MiniLM (dense)", "mp-t")
strip(s, C1 + 10, 106, 390, 22, len(names), TXT, lit=set(nz))
strip(s, C2 + 10, 106, 390, 22, 384, TXT, values=emb[0])
for i, (lth, len_, ath, aen, aok, bth, ben, bok) in enumerate(ROWS_CMP):
    yy = 152 + i * 40
    s.line(C0, yy - 6, 1090, yy - 6, "mp-guide")
    s.both(C0 + 10, yy + 20, lth, len_, "mp-c")
    for x, th, en, ok in ((C1, ath, aen, aok), (C2, bth, ben, bok)):
        mark = "" if ok is None else ("✓ " if ok else "✗ ")
        cls = "hk-desc" if ok is None else ("ml-ok" if ok else "ml-neg")
        s.both(x + 10, yy + 20, mark + th, mark + en, cls)
yy = 152 + len(ROWS_CMP) * 40
s.line(C0, yy - 6, 1090, yy - 6, "mp-guide")
s.box(C0, yy + 2, 1080, 84, "ml-cell", 12)
s.both(C0 + 10, yy + 32, "R² ในบทนี้: คำบรรยายอย่างเดียว", "R² in this lesson: note alone", "mp-c")
s.text(C1 + 10, yy + 32, f"{r2['tfidf']:.3f}", "mp-n")
s.text(C2 + 10, yy + 32, f"{r2['minilm']:.3f}", "mp-n")
s.both(C0 + 10, yy + 66, "ต่อกับราคา ประเทศ องุ่น", "joined with price, country, grape", "mp-c")
s.text(C1 + 10, yy + 66, f"{r2['tfidf+']:.3f}", "mp-n")
s.text(C2 + 10, yy + 66, f"{r2['minilm+']:.3f}", "mp-n")
s.both(1080, yy + 66, "ต่างกันนิดเดียว: การต่อสำคัญกว่า", "a small gap: joining matters more", "mp-acc", "end")
s.save("l12-sparse-vs-dense.svg", yy + 98)

# ================================================================ S05 price and categories to numbers
s = Svg(W, f"Price runs from ${wines.price.min():.0f} to ${wines.price.max():.0f}; on a log axis each doubling is one "
           f"step; wine 1 (${w1.price:.0f}) becomes {price_scaled[0]:.2f} after log and StandardScaler. Country becomes "
           f"{n_country} one-hot columns (wine 1: {w1.country}), variety {n_grape} columns (wine 1: {w1.variety}).")
s.bubble("ราคาและกลุ่มจะเป็นตัวเลขแบบไหน", "How do price and groups become numbers?")
s.panel(10, 70, 1080, 168, "ml-cell", "ราคา → log → ปรับสเกล = 1 คอลัมน์", "price → log → scale = 1 column", 1)
X0, X1 = 60, 760
lp = lambda p_: X0 + (np.log(p_) - np.log(5)) / (np.log(300) - np.log(5)) * (X1 - X0)
s.line(X0, 168, X1, 168, "mp-axis")
for p_ in (5, 10, 20, 40, 80, 160, 300):
    s.line(lp(p_), 162, lp(p_), 174, "mp-axis")
    s.text(lp(p_), 196, f"${p_}", "mp-s", "middle")
for p_ in wines.price.sample(200, random_state=1):
    s.raw(f'<circle cx="{lp(p_):.1f}" cy="{150 + (hash(p_) % 7)}" r="3" style="fill:var(--tag-concept-dot);fill-opacity:.35"/>')
s.raw(f'<circle cx="{lp(w1.price):.1f}" cy="150" r="7" style="fill:{PRICE}"/>')
s.both(lp(w1.price), 136, f"ขวดที่ 1: ${w1.price:.0f}", f"wine 1: ${w1.price:.0f}", "mp-acc", "middle")
s.both(X0, 222, "แกน log: ราคาเพิ่มสองเท่า = หนึ่งก้าวเท่ากัน", "log axis: each doubling of price = one equal step", "mp-s")
s.arrow(800, 168, 860, 168)
s.box(866, 136, 200, 64, "ml-cell-b", 10)
s.both(966, 160, "หลัง StandardScaler", "after StandardScaler", "mp-s", "middle")
s.text(966, 190, f"{price_scaled[0]:.2f}", "mp-big", "middle")
for k, (th, en, n, lit, val, col) in enumerate([
        ("ประเทศ → one-hot", "country → one-hot", n_country, list(onehot.categories_[0]).index(w1.country), w1.country, CTRY),
        ("องุ่น → one-hot", "variety → one-hot", n_grape, list(onehot.categories_[1]).index(w1.variety), w1.variety, GRAPE)]):
    yy = 254 + k * 92
    s.panel(10, yy, 1080, 80, "ml-cell", f"{th} = {n} คอลัมน์", f"{en} = {n} columns", k + 2)
    sw = 24 * n if n < 40 else 1040 * 0.62
    strip(s, 30, yy + 42, sw, 26, n, col, lit={lit})
    s.both(48 + sw, yy + 61, f"1 เฉพาะช่อง {val} ที่เหลือ 0", f"1 only in {val}, 0 elsewhere", "mp-acc")
s.save("l12-other-columns.svg", 446)

# ================================================================ S06 the joined row
s = Svg(W, f"The row representation of wine 1: 384 MiniLM numbers, 1 scaled log price ({price_scaled[0]:.2f}), "
           f"{n_country} country columns (one 1: {w1.country}) and {n_grape} grape columns (one 1: {w1.variety}), "
           f"{ROW} numbers in total. Every wine gets the same blocks in the same order, giving a 1,000 × {ROW} table.")
s.bubble("ต่อทุกก้อนข้างกัน ได้ไวน์หนึ่งขวด = ตัวเลขแถวเดียว", "Put the blocks side by side: one wine = one row of numbers")
BX, BW = 30, 1040
scale = BW / ROW
parts = [(384, TXT, None, emb[0]), (1, PRICE, None, None),
         (n_country, CTRY, {list(onehot.categories_[0]).index(w1.country)}, None),
         (n_grape, GRAPE, {list(onehot.categories_[1]).index(w1.variety)}, None)]
x = BX
spans = []
for n, col, lit, vals in parts:
    w = max(n * scale, 8)
    if vals is not None:
        strip(s, x, 120, w - 3, 54, n, col, values=vals)
    elif n == 1:
        s.fill(x, 120, w - 3, 54, col, 2)
    else:
        strip(s, x, 120, w - 3, 54, n, col, lit=lit)
    spans.append((x, x + w - 3))
    x += w
labels = [("MiniLM ของคำบรรยาย: 384", "MiniLM of the note: 384", "คอลัมน์ 0–383", "columns 0–383"),
          ("ราคา: 1", "price: 1", f"คอลัมน์ 384 = {price_scaled[0]:.2f}", f"column 384 = {price_scaled[0]:.2f}"),
          (f"ประเทศ: {n_country}", f"country: {n_country}", "", ""),
          (f"องุ่น: {n_grape}", f"grape: {n_grape}", f"คอลัมน์ 385–{ROW - 1}", f"columns 385–{ROW - 1}")]
for (x1, x2), (th, en, th2, en2) in zip(spans, labels):
    if th.startswith("ราคา"):
        s.raw(f'<path d="M{(x1 + x2) / 2:.1f} 116 L{(x1 + x2) / 2:.1f} 96" class="mp-axis"/>')
        s.both((x1 + x2) / 2 - 8, 90, f"{th} · {th2}", f"{en} · {en2}", "mp-acc", "end")
    else:
        brace(s, x1, x2, 182, th, en)
        if th2:
            s.both((x1 + x2) / 2, 234, th2, en2, "mp-s", "middle")
s.both(BX, 108, "ไวน์ขวดที่ 1", "wine 1", "mp-t")
s.box(10, 300, 1080, 92, "rc-ctx", 14)
s.both(30, 332, f"384 + 1 + {n_country} + {n_grape} = {ROW} ตัวเลขต่อขวด", f"384 + 1 + {n_country} + {n_grape} = {ROW} numbers per wine", "pl-label")
s.both(30, 364, f"ทำแบบเดียวกันทุกขวด เรียงก้อนเหมือนกัน → ตาราง 1,000 × {ROW} = X ของโมเดล",
       f"the same blocks in the same order for every wine → a 1,000 × {ROW} table = the model's X", "pl-text")
s.save("l12-concat-row.svg", 404)

# ================================================================ S07 exercise: build a shortened row by hand (no answers drawn)
EX = [0, 2]                                             # wine 1 and wine 3
COLS_EX = [("t1", TXT), ("t2", TXT), ("t3", TXT), ("price", PRICE), ("France", CTRY), ("Italy", CTRY), ("US", CTRY),
           ("Glera", GRAPE), ("Pinot Grigio", GRAPE), ("Pinot Noir", GRAPE)]
s = Svg(W, "Two real wines and a shortened row to fill in. Wine 1: Italy, Pinot Grigio, scaled log price "
           f"{price_scaled[0]:.2f}, note vector starting {', '.join(f'{v:.2f}' for v in emb[0][:3])}, {wines.stars[0]} "
           f"stars. Wine 3: US, Pinot Noir, {price_scaled[2]:.2f}, {', '.join(f'{v:.2f}' for v in emb[2][:3])}, "
           f"{wines.stars[2]} stars. The row has 10 columns in a fixed order: t1–t3 (the first 3 of the 384 text "
           "numbers), price, France, Italy, US, Glera, Pinot Grigio, Pinot Noir. The cells are left empty.")
s.bubble("เติมแถวตัวเลขของไวน์ 2 ขวด (แบบย่อ)", "Fill in the number rows of 2 wines (shortened)")
for j, i in enumerate(EX):
    x = 10 + j * 550
    s.box(x, 70, 530, 122, "rc-ctx", 12)
    s.both(x + 18, 98, f"ไวน์ขวดที่ {wines.wine_id[i]}", f"wine {wines.wine_id[i]}", "mp-t")
    cx = x + 140
    for lab in (wines.country[i], wines.variety[i], f"${wines.price[i]:.0f}"):
        w = width(lab, 16) + 24
        s.box(cx, 80, w, 28, "ml-cell", 14)
        s.text(cx + w / 2, 99, lab, "mp-chip", "middle")
        cx += w + 8
    s.both(x + 18, 134, f"ราคาหลัง log + ปรับสเกล: {price_scaled[i]:.2f}", f"price after log + scale: {price_scaled[i]:.2f}", "mp-c")
    s.both(x + 18, 160, "vector คำบรรยาย 3 ตัวแรก: " + ", ".join(f"{v:.2f}" for v in emb[i][:3]),
           "note vector, first 3: " + ", ".join(f"{v:.2f}" for v in emb[i][:3]), "mp-c")
    s.both(x + 18, 184, f"y = {wines.stars[i]} ดาว (ไม่อยู่ในแถว X)", f"y = {wines.stars[i]} stars (not in the X row)", "mp-s")
GX, CWX = 150, 93
groups = [("ข้อความ (3 จาก 384)", "text (3 of 384)", 0, 3, TXT), ("ราคา", "price", 3, 4, PRICE),
          ("ประเทศ", "country", 4, 7, CTRY), ("องุ่น", "grape", 7, 10, GRAPE)]
for th, en, a_, b_, col in groups:
    s.raw(f'<rect x="{GX + a_ * CWX + 2}" y="214" width="{(b_ - a_) * CWX - 4}" height="28" rx="6" '
          f'style="fill:{col};fill-opacity:.18"/>')
    s.both(GX + (a_ + b_) / 2 * CWX, 233, th, en, "mp-c", "middle")
for c, (name, col) in enumerate(COLS_EX):
    s.text(GX + c * CWX + CWX / 2, 266, name, "mp-s", "middle")
for r, i in enumerate(EX):
    yy = 278 + r * 52
    s.both(20, yy + 30, f"ขวดที่ {wines.wine_id[i]}", f"wine {wines.wine_id[i]}", "mp-t")
    for c in range(10):
        s.box(GX + c * CWX + 4, yy, CWX - 8, 42, "ml-cell", 6)
s.both(20, 410, "ลำดับคอลัมน์เหมือนกันทุกขวด · ประเทศและองุ่น: 1 ในช่องของตัวเอง ที่เหลือ 0",
       "the same column order for every wine · country and grape: 1 in the wine's own cell, 0 elsewhere", "mp-acc")
s.save("l12-row-exercise.svg", 424)

# ================================================================ S08 column transformer + Ridge in each round
s = Svg(W, f"A column transformer inside a pipeline: description goes to MiniLM (384 columns), log_price to "
           f"StandardScaler (1), country and variety to OneHotEncoder ({n_country + n_grape}); the outputs are joined "
           f"side by side and Ridge learns stars. In each of the 5 cross-validation rounds this is fitted on 800 wines "
           f"and scored on the other 200; mean R² {r2['minilm+']:.3f}.")
s.bubble("ให้ pipeline ต่อแถวให้เองในทุกรอบของ cross-validation", "Let a pipeline build the rows in every round of cross-validation")
s.box(10, 72, 220, 240, "ml-cell", 12)
s.both(24, 98, "ตาราง wines", "the wines table", "mp-t")
for i, (c, cls) in enumerate([("description", "rc-ctx"), ("log_price", "ml-cell-b"), ("country", "ml-cell-b"), ("variety", "ml-cell-b")]):
    s.box(24, 112 + i * 48, 192, 38, cls, 8)
    s.text(36, 137 + i * 48, c, "hk-mono")
targets = [(131, "SentenceTransformer", "MiniLM → 384"), (179, "StandardScaler", "→ 1"), (227, "OneHotEncoder", f"→ {n_country + n_grape}")]
for i, (yy, name, out) in enumerate(targets):
    s.box(300, yy - 22, 236, 44, "ml-model-done", 10)
    s.text(418, yy + 6, name, "ml-model-text", "middle")
    s.text(546, yy + 6, out, "mp-acc")
s.arrow(218, 131, 296, 131)
s.arrow(218, 179, 296, 179)
s.arrow(218, 227, 296, 227)
s.arrow(218, 275, 296, 238)
for yy in (131, 179, 227):
    s.arrow(676, yy, 700, 180 + (yy - 179) * 0.3)
s.box(704, 152, 150, 58, "ml-cell", 10)
s.both(779, 176, "ต่อข้างกัน", "side by side", "mp-c", "middle")
s.text(779, 200, f"{ROW} columns", "mp-acc", "middle")
s.arrow(858, 181, 900, 181)
s.box(904, 156, 176, 50, "ml-model", 10)
s.text(992, 187, "Ridge → stars", "ml-model-text", "middle")
s.text(300, 290, "make_column_transformer", "hk-mono")
s.box(10, 330, 1080, 96, "nt-band-a", 14)
for k in range(5):
    x = 30 + k * 132
    for j in range(5):
        s.fill(x + j * 22, 352, 20, 26, "var(--accent)" if j == k else "var(--tag-concept-dot)", 3)
    s.both(x + 55, 400, f"รอบ {k + 1}", f"round {k + 1}", "mp-s", "middle")
s.both(700, 362, "สีฟ้า: fit ทุกขั้นกับ 800 ขวด", "blue: fit every step on 800 wines", "mp-c")
s.both(700, 386, "สีส้ม: วัด R² กับอีก 200 ขวด", "orange: score R² on the other 200", "mp-c")
s.both(700, 412, f"R² เฉลี่ย {r2['minilm+']:.3f}", f"mean R² {r2['minilm+']:.3f}", "mp-acc")
s.save("l12-column-pipeline.svg", 438)

# ================================================================ S09 R² comparison
BARS = [("tfidf", "คำบรรยาย TF-IDF", "note: TF-IDF", TXT), ("minilm", "คำบรรยาย MiniLM", "note: MiniLM", TXT),
        ("others", "ราคา ประเทศ องุ่น", "price, country, grape", PRICE),
        ("tfidf+", "TF-IDF + คอลัมน์อื่น", "TF-IDF + others", "var(--tag-exercise-dot)"),
        ("minilm+", "MiniLM + คอลัมน์อื่น", "MiniLM + others", "var(--tag-exercise-dot)")]
s = Svg(W, "R² from 5-fold cross-validation with the same Ridge model: " +
        ", ".join(f"{en} {r2[k]:.3f}" for k, th, en, c in BARS) +
        f". Text alone and the other columns alone each explain about 0.3–0.4; joined rows explain about 0.52–0.53. "
        f"0.389 + 0.400 would be 0.789, but the parts overlap.")
s.bubble("ข้อความอย่างเดียว คอลัมน์อื่นอย่างเดียว หรือต่อกัน: อะไรทำนายคะแนนดาวได้ดีที่สุด", "Text alone, other columns alone, or joined: which predicts stars best?")
B0, BH = 340, 400
for gx, th, en in ((40, "ข้อความอย่างเดียว", "text alone"), (440, "คอลัมน์อื่น", "other columns"), (660, "ต่อกันเป็นแถวเดียว", "joined into one row")):
    s.both(gx, 380, th, en, "mp-t")
s.line(30, B0, 1070, B0, "mp-axis")
for k, (key, th, en, col) in enumerate(BARS):
    x = [40, 220, 440, 660, 860][k]
    h = r2[key] * BH
    s.fill(x, B0 - h, 160, h, col, 6)
    s.text(x + 80, B0 - h - 12, f"{r2[key]:.3f}" + (" ✓" if "+" in key else ""), "mp-big-ok" if "+" in key else "mp-n", "middle")
    s.both(x + 80, B0 - 14, th, en, "pl-num", "middle")
s.both(30, 418, "R² = สัดส่วนความต่างของคะแนนดาวที่โมเดลอธิบายได้ (cross-validation 5 ส่วน, Ridge ตัวเดียวกัน) · 0.389 + 0.400 ≠ 0.529 เพราะสองส่วนบอกเรื่องเดียวกันบางส่วน",
       "R² = the share of the variation in stars the model explains (5-fold CV, the same Ridge) · 0.389 + 0.400 ≠ 0.529: the parts overlap", "mp-s")
s.save("l12-r2-compare.svg", 432)


# ================================================================ S11 key terms
def t_vec(x, yy, w, h):
    strip(s, x + 14, yy + 26, w - 28, 30, 48, TXT, values=emb[0][:48])
    s.text(x + w / 2, yy + 76, "384 numbers", "mp-c", "middle")


def t_onehot(x, yy, w, h):
    for i in range(8):
        s.box(x + 20 + i * 36, yy + 24, 30, 34, "ml-cell-b" if i == 2 else "ml-cell", 4)
        s.text(x + 35 + i * 36, yy + 47, "1" if i == 2 else "0", "mp-c", "middle")


def t_row(x, yy, w, h):
    for i, (n, col) in enumerate([(160, TXT), (10, PRICE), (40, CTRY), (80, GRAPE)]):
        xs = x + 16 + sum(m for m, _ in [(160, 0), (10, 0), (40, 0), (80, 0)][:i]) + i * 4
        s.fill(xs, yy + 26, n, 34, col, 3)
    s.text(x + w / 2, yy + 78, f"{ROW} numbers", "mp-c", "middle")


def t_ct(x, yy, w, h):
    for i, c in enumerate(["text", "price", "group"]):
        s.box(x + 16, yy + 8 + i * 25, 70, 21, "ml-cell", 4)
        s.text(x + 51, yy + 23 + i * 25, c, "mp-c", "middle")
        s.raw(f'<path d="M{x + 90} {yy + 18 + i * 25} L{x + 180} {yy + 43}" class="pl-line"/>')
    s.box(x + 184, yy + 28, 110, 30, "ml-model", 6)
    s.text(x + 239, yy + 48, "join", "ml-model-text", "middle")


def t_ridge(x, yy, w, h):
    for i, v in enumerate([0.9, 0.5, 0.3, 0.6, 0.2, 0.4, 0.15, 0.35]):
        s.fill(x + 24 + i * 34, yy + 70 - v * 50, 22, v * 50, "var(--tag-concept-dot)", 2)
    s.text(x + w - 16, yy + 22, "small weights", "mp-s", "end")


def t_log(x, yy, w, h):
    for i, p_ in enumerate([5, 10, 20, 40, 80, 160]):
        s.line(x + 24 + i * 52, yy + 40, x + 24 + i * 52, yy + 52, "mp-axis")
        s.text(x + 24 + i * 52, yy + 72, f"${p_}", "mp-s", "middle")
    s.line(x + 24, yy + 46, x + 24 + 5 * 52, yy + 46, "mp-axis")


s = Svg(W, "Six key terms with small drawings: text vector, one-hot, row representation, column transformer, Ridge, "
           "log transform.")
bottom = term_grid(s, [
    ("Text vector", t_vec, "ข้อความ → ตัวเลขยาวเท่ากัน", "text → numbers of equal length", "TF-IDF หรือ MiniLM", "TF-IDF or MiniLM"),
    ("One-hot", t_onehot, "หนึ่งคอลัมน์ต่อหนึ่งค่า", "one column per value", "1 ช่องเดียว ที่เหลือ 0", "a single 1, the rest 0"),
    ("Row representation", t_row, "ทุกก้อนต่อข้างกัน", "all blocks side by side", "เรียงเหมือนกันทุกแถว", "same order in every row"),
    ("Column transformer", t_ct, "แปลงแต่ละคอลัมน์แล้วต่อ", "convert each column, then join", "เรียนใหม่ทุกรอบของ CV", "relearns in every CV round"),
    ("Ridge", t_ridge, "regression ที่คุมน้ำหนัก", "regression that limits weights", "เมื่อคอลัมน์เยอะ", "for many columns"),
    ("Log transform", t_log, "สองเท่า = หนึ่งก้าว", "a doubling = one step", "ใช้กับตัวเลขที่เบ้", "for skewed numbers"),
], cols=3, tw=352)
s.save("l12-key-terms.svg", bottom + 10)
