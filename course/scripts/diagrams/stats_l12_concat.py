"""Pictures for stats-dh L12 (text as data: one row from text and numbers), in the stats-dh card style. The lesson's
point: turn the text into a vector, turn the other columns into numbers, join them into one row, train on the row.
  l12-mixed-everywhere.svg  S01  six apps whose rows mix free text, numbers and categories
  l12-one-row-vector.svg    S01  wine 1: note / price / country / grape → three blocks → one row of 541 → Ridge → points
  l12-one-wine.svg          S03  wine 1 as a card (features and target) and the points of all 1,000 wines
  l12-text-vectors.svg      S04  wine 1's note as TF-IDF (4,146 columns, ~34 non-zero) and as MiniLM (384 numbers)
  l12-other-columns.svg     S05  price → log → scaled (wine 1: −0.93); country and grape → one-hot (24 + 132)
  l12-concat-row.svg        S06  the 541-number row of wine 1, block by block, and the 1,000 × 541 table
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
y = wines["points"]
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
pred1 = cross_val_predict(make_pipeline(make_column_transformer(*blocks["minilm+"]), Ridge()), wines, y, cv=cv)[0]
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
    ("⭐", "แอปรีวิวไวน์", "Wine app", "คำบรรยายรสชาติ", "tasting note", "ราคา · ประเทศ", "price · country", "คะแนน", "points"),
]
s = Svg(W, "Six everyday apps whose rows mix text, numbers and categories: a shop listing (title, description; price, "
           "category → units sold), a holiday rental (room description; price, area → guest rating), a job advert (job "
           "description; city, experience → salary), food delivery (customer review; delivery time, shop → stars), a "
           "library catalogue (blurb; year, pages → genre), a wine app (tasting note; price, country → points).")
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

# ================================================================ S01 one wine → one row → points
s = Svg(W, f"Wine 1 as one row: tasting note (text), price ${w1.price:.0f} (number), {w1.country} and {w1.variety} "
           f"(categories). The note becomes 384 MiniLM numbers, the price 1 scaled number, country and grape "
           f"{n_country + n_grape} one-hot columns; joined they make one row of {ROW} numbers. Ridge, trained on rows "
           f"like it, predicts {pred1:.1f} points; the critic gave {w1.points}.")
s.bubble("ไวน์ขวดหนึ่งมีทั้งคำ ราคา และกลุ่ม โมเดลจะใช้ทั้งหมดได้อย่างไร", "A wine has words, a price and groups: how can one model use them all?")
cols = [(10, 520, "rc-ctx", "คำบรรยาย (ข้อความ)", "description (text)", w1.description[:62] + "…"),
        (540, 150, "ml-cell", "ราคา (ตัวเลข)", "price (number)", f"${w1.price:.0f}"),
        (700, 160, "ml-cell", "ประเทศ (กลุ่ม)", "country (group)", w1.country),
        (870, 220, "ml-cell", "องุ่น (กลุ่ม)", "variety (group)", w1.variety)]
for x, w, cls, th, en, val in cols:
    s.box(x, 72, w, 64, cls, 10)
    s.both(x + 14, 94, th, en, "mp-s")
    s.text(x + 14, 122, val, "hk-desc")
BX, BW, BY = 40, 1020, 214
seg = [(384, TXT, "MiniLM 384", "MiniLM 384"), (1, PRICE, "ราคา 1", "price 1"), (n_country, CTRY, f"ประเทศ {n_country}", f"country {n_country}"),
       (n_grape, GRAPE, f"องุ่น {n_grape}", f"grape {n_grape}")]
scale = BW / ROW
x = BX
starts = []
for n, col, th, en in seg:
    w = max(n * scale, 10)
    starts.append((x, w))
    s.fill(x, BY, w - 2, 40, col, 4)
    x += w
for (x0, w0), (cx, w, *_ ) in zip(starts, cols):
    s.arrow(cx + w / 2, 140, x0 + w0 / 2, BY - 6)
for (x0, w0), (n, col, th, en) in zip(starts, seg):
    if w0 > 120:
        s.both(x0 + w0 / 2, BY + 26, th, en, "pl-num", "middle")
    elif n == 1:
        s.both(x0 - 4, BY + 62, th, en, "mp-c", "end")
    else:
        s.both(x0 + 2, BY + 62, th, en, "mp-c")
s.both(BX, BY + 72, f"แถวเดียว {ROW} ตัวเลข (ราคาเป็นแถบบาง ๆ สีส้ม 1 ช่อง)", f"one row of {ROW} numbers (the price is the thin orange cell)", "pl-label")
s.arrow(550, BY + 82, 550, BY + 108)
s.box(470, BY + 112, 160, 46, "ml-model", 10)
s.text(550, BY + 142, "Ridge", "ml-model-text", "middle")
s.arrow(634, BY + 135, 690, BY + 135)
s.both(700, BY + 128, f"ทำนาย {pred1:.1f} คะแนน", f"predicts {pred1:.1f} points", "mp-t")
s.both(700, BY + 154, f"นักวิจารณ์ให้ {w1.points}", f"the critic gave {w1.points}", "mp-s")
s.save("l12-one-row-vector.svg", BY + 176)

# ================================================================ S03 wine 1 and all points
s = Svg(W, f"Wine 1 as a card: features (the tasting note, price ${w1.price:.0f}, {w1.country}, {w1.variety}) and the "
           f"target, {w1.points} points. Right: the points of all 1,000 wines, from 80 to 97, most between 85 and 92 "
           f"(mean {y.mean():.1f}).")
s.bubble("หนึ่งแถว = ไวน์หนึ่งขวด ทำนายคะแนนของนักวิจารณ์", "One row = one wine: predict the critic's points")
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
s.both(550, 292, "target", "target", "mp-s", "middle")
s.text(550, 320, f"{w1.points} pts", "mp-big", "middle")
s.panel(650, 70, 440, 320, "ml-cell", "คะแนนของไวน์ทั้ง 1,000 ขวด", "Points of all 1,000 wines", 2)
vc = y.value_counts().sort_index()
mx = vc.max()
for p_, c in vc.items():
    bx = 676 + (p_ - 80) * 22
    h = c / mx * 200
    s.fill(bx, 340 - h, 18, h, "var(--accent)" if p_ == w1.points else "var(--tag-concept-dot)", 2)
for p_ in (80, 85, 90, 95):
    s.text(676 + (p_ - 80) * 22 + 9, 362, str(p_), "mp-s", "middle")
s.both(676, 384, f"เฉลี่ย {y.mean():.1f} · ส้ม = ขวดที่ 1 ({w1.points})", f"mean {y.mean():.1f} · orange = wine 1 ({w1.points})", "mp-s")
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

# ================================================================ S08 column transformer + Ridge in each round
s = Svg(W, f"A column transformer inside a pipeline: description goes to MiniLM (384 columns), log_price to "
           f"StandardScaler (1), country and variety to OneHotEncoder ({n_country + n_grape}); the outputs are joined "
           f"side by side and Ridge learns points. In each of the 5 cross-validation rounds this is fitted on 800 wines "
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
s.text(992, 187, "Ridge → points", "ml-model-text", "middle")
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
s.bubble("ข้อความอย่างเดียว คอลัมน์อื่นอย่างเดียว หรือต่อกัน: อะไรทำนายคะแนนได้ดีที่สุด", "Text alone, other columns alone, or joined: which predicts points best?")
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
s.both(30, 418, "R² = สัดส่วนความต่างของคะแนนที่โมเดลอธิบายได้ (cross-validation 5 ส่วน, Ridge ตัวเดียวกัน) · 0.389 + 0.400 ≠ 0.529 เพราะสองส่วนบอกเรื่องเดียวกันบางส่วน",
       "R² = the share of the variation in points the model explains (5-fold CV, the same Ridge) · 0.389 + 0.400 ≠ 0.529: the parts overlap", "mp-s")
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
