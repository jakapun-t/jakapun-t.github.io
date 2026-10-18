"""Concept pictures for nlp-basic lesson 12 (tokenization), in the style of nlp l12-why-chunk.svg: the running
example's question on top, drawn objects (token chips, review cards), arrows at the exact spot, the real numbers
attached to what they describe. ไทย/EN labels follow the language switch; Thai language data shows in both.

    python3 scripts/diagrams/basic_l12_concepts.py courses/nlp-basic/images

Every token list and count is the lesson's own (data/l12_reviews_th.csv with pythainlp 5 newmm and attacut,
tiktoken o200k_base, nltk PorterStemmer), checked in course/.venv: กาแฟ in 7 reviews by reading, 1 by split(),
6 by newmm (it misses R07); กก counted 5 times before shortening stretched letters and 0 after; the top bigrams
(กาแฟ อร่อย, ขนม อร่อย, รอ นาน, นาน มาก, บรรยากาศ ดี) 2 each; อร่อย 5 times as a single word. "555" in S12 is a
labelled example.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from basic_svg import Svg  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
W = 1180
CHIP = {"keep": ("pl-chip", "pl-chip-text"), "bad": ("sw-chip-warn", "sw-warn-text"),
        "good": ("rc-res", "ml-ok"), "del": ("pl-chip-del", "pl-del"), "plain": ("ml-cell", "pl-text")}


def svg(title):
    return Svg(OUT, W, title)


def chips(s, x, y, items, gap=6, pad=10, thai=True):
    """items: (text, kind) chips left to right; returns the x of each chip's left edge and the right end."""
    lefts = []
    for t, kind in items:
        cls, tcls = CHIP[kind]
        lefts.append(x)
        x = s.chip(x, y, t, cls, tcls, pad=pad, thai=thai) + gap
    return lefts, x - gap


# ================================================================ S01: who cuts R07, and how many reviews mention กาแฟ
MENTION = {"R01", "R02", "R03", "R05", "R06", "R07", "R09"}  # a reader finds กาแฟ in these 7
FOUND = {"person": MENTION, "split": {"R05"}, "newmm": MENTION - {"R07"}}
s = svg("How many reviews in reviews_th mention กาแฟ (coffee)? 1 A person reading cuts R07's กาแฟก็ธรรมดา into กาแฟ | ก็ | "
        "ธรรมดา and finds กาแฟ in 7 reviews (R01, R02, R03, R05, R06, R07, R09). 2 split() cuts only at spaces, so กาแฟก็ธรรมดา "
        "stays one lump; it finds กาแฟ only in R05 (กาแฟ ok): 1. 3 word_tokenize (newmm) cuts with a dictionary: right in most "
        "reviews, but R07 becomes กา | แฟก็ธรรม | ดา, so it finds 6 and misses R07.")
s.bubble(W / 2, 8, "ใน reviews_th มีกี่รีวิวที่พูดถึง กาแฟ", "How many reviews in reviews_th mention กาแฟ (coffee)?", 620)
PANELS = [("person", "nt-band-a", "คนอ่านเอง", "A person reading", [("กาแฟ", "good"), ("ก็", "keep"), ("ธรรมดา", "keep")],
           "เห็น กาแฟ เป็นคำ", "sees กาแฟ as a word", "= 7 รีวิว ✓", "= 7 reviews ✓", "ml-ok"),
          ("split", "sw-warn-box", "split()", "split()", [("กาแฟก็ธรรมดา", "bad")],
           "ไม่มีช่องว่าง: ทั้งก้อนเป็นคำเดียว", "no space: it stays one lump", "= 1 รีวิว ✗ (แค่ R05: กาแฟ ok)", "= 1 review ✗ (only R05: กาแฟ ok)", "ml-neg"),
          ("newmm", "sw-warn-box", "word_tokenize (newmm)", "word_tokenize (newmm)", [("กา", "bad"), ("แฟก็ธรรม", "bad"), ("ดา", "bad")],
           "กาแฟ ถูกตัดแยก", "กาแฟ is cut apart", "= 6 รีวิว ✗ (พลาด R07)", "= 6 reviews ✗ (misses R07)", "ml-neg")]
PW = 366
for k, (key, band, th, en, toks, nth, nen, rth, ren, rcls) in enumerate(PANELS):
    x0 = 20 + k * (PW + 21)
    s.box(x0, 70, PW, 400, band, 14)
    s.badge(x0 + 30, 102, k + 1)
    s.both(x0 + 52, 109, th, en, "pl-label")
    s.both(x0 + 20, 150, "R07: …กาแฟก็ธรรมดา ถูกตัดเป็น", "R07: …กาแฟก็ธรรมดา is cut into", "pl-note")
    lefts, right = chips(s, x0 + 20, 188, toks)
    s.arrow(x0 + 40, 238, x0 + 40, 210)
    s.both(x0 + 52, 240, nth, nen, "ml-ok" if key == "person" else "ml-neg")
    s.both(x0 + 20, 286, "รีวิวที่นับได้ว่ามี กาแฟ", "reviews counted as mentioning กาแฟ", "pl-note")
    for j in range(10):
        rid = f"R{j + 1:02d}"
        x, y = x0 + 20 + (j % 5) * 66, 300 + (j // 5) * 52
        hit, missed = rid in FOUND[key], rid in MENTION and rid not in FOUND[key]
        s.box(x, y, 58, 42, "rc-res" if hit else ("sw-chip-warn" if missed else "ml-cell"), 8)
        s.text(x + 29, y + 27, rid, "ml-ok" if hit else ("sw-warn-text" if missed else "pl-note"), "middle")
    s.both(x0 + 20, 446, rth, ren, rcls)
s.both(20, 500, "สีเขียว = นับได้ · สีส้ม = มี กาแฟ แต่โปรแกรมนับพลาด · สีขาว = ไม่มี กาแฟ",
       "green = counted · orange = mentions กาแฟ but the program missed it · white = no กาแฟ", "pl-note")
s.save("l12-why-tokenize.svg", 516)


# ================================================================ S12: what each regex removes, on real posts
s = svg("What clean() removes from real posts. R01: ^RT @\\w+: removes 'RT @cafe_lover: ', (.)\\1{2,} shortens มากกกก to มาก, "
        "https?://\\S+ removes the link. R02: #\\S+ removes the hashtag #ไม่ไปซ้ำ. R06: via @\\w+ removes 'via @foodie_th'. "
        "The result for R01: กาแฟอร่อยมาก ร้านสวย บรรยากาศดี 😍. A side effect, on a made-up example: (.)\\1{2,} also turns 555, "
        "Thai for laughing, into 5.")
ROWS12 = [("R01", [("RT @cafe_lover:", "del", "^RT @\\w+: "), ("กาแฟอร่อยมาก", "keep", None), ("กกก", "del", "(.)\\1{2,}"),
                   ("ร้านสวย บรรยากาศดี 😍", "keep", None), ("https://t.co/a1B2c3", "del", "https?://\\S+")]),
          ("R02", [("รอกาแฟนานมาก พนักงานไม่สนใจลูกค้าเลย", "keep", None), ("#ไม่ไปซ้ำ", "del", "#\\S+")]),
          ("R06", [("พนักงานบริการดี ยิ้มแย้ม กาแฟอร่อย ☕️", "keep", None), ("via @foodie_th", "del", "via @\\w+")])]
s.both(20, 30, "ส่วนที่ขีดฆ่า = ส่วนที่ regex จับได้แล้วลบทิ้ง · ข้างใต้คือ pattern ที่จับ",
       "Struck out = what a regex matched and removed · under it, the pattern that matched", "pl-note")
for k, (rid, parts) in enumerate(ROWS12):
    y = 84 + k * 112
    s.text(20, y + 7, rid, "dg-index")
    x = 64
    for t, kind, pat in parts:
        cls, tcls = CHIP[kind]
        x1 = s.chip(x, y, t, cls, tcls, thai=True)
        if pat:
            s.arrow((x + x1) / 2, y + 46, (x + x1) / 2, y + 22)
            s.text((x + x1) / 2, y + 68, pat, "hk-mono", "middle")
        x = x1 + 8
s.box(20, 404, 700, 96, "nt-band-a", 14)
s.text(40, 438, "clean(R01)", "hk-mono")
chips(s, 40, 474, [("กาแฟอร่อยมาก ร้านสวย บรรยากาศดี 😍", "good")])
s.both(500, 480, "✓ เหลือแต่ภาษา", "✓ only language is left", "ml-ok")
s.box(740, 404, 420, 96, "sw-warn-box", 14)
s.both(760, 436, "✗ ผลข้างเคียง (ตัวอย่างสมมติ)", "✗ A side effect (made-up example)", "pl-label")
s.both(760, 476, "ตลกมาก 555 → ตลกมาก 5", "ตลกมาก 555 → ตลกมาก 5", "pl-text")
s.both(980, 476, "หัวเราะหายไป", "the laugh is gone", "ml-neg")
s.save("l12-regex-clean.svg", 516)


# ================================================================ S14: four ways to tokenize R07
ROWS14 = [
    ("sw-warn-box", "อิงกฎ: split()", "Rules: split()", "ใช้: ช่องว่าง, regex", "uses: spaces, regex",
     [("ที่จอดรถหายาก", "bad"), ("รอนาน", "bad"), ("กาแฟก็ธรรมดา", "bad")],
     "✗ ตัดแค่ตรงช่องว่าง: ได้ 3 วลี ไม่ใช่คำ", "✗ cuts only at spaces: 3 phrases, not words"),
    ("sw-warn-box", "อิงพจนานุกรม: newmm", "Dictionary: newmm", "ใช้: รายการคำ", "uses: a word list",
     [("ที่จอดรถ", "keep"), ("หา", "keep"), ("ยาก", "keep"), ("รอ", "keep"), ("นาน", "keep"), ("กา", "bad"), ("แฟก็ธรรม", "bad"), ("ดา", "bad")],
     "✗ กาแฟก็ธรรมดา → กา | แฟก็ธรรม | ดา: กาแฟ หายไป", "✗ กาแฟก็ธรรมดา → กา | แฟก็ธรรม | ดา: กาแฟ is lost"),
    ("nt-band-a", "เรียนรู้จากข้อมูล: attacut", "Learned: attacut", "ใช้: โมเดลที่ฝึกแล้ว", "uses: a trained model",
     [("ที่", "keep"), ("จอด", "keep"), ("รถ", "keep"), ("หา", "keep"), ("ยาก", "keep"), ("รอ", "keep"), ("นาน", "keep"),
      ("กาแฟ", "good"), ("ก็", "keep"), ("ธรรมดา", "keep")],
     "✓ ตัดถูกในรีวิวนี้ (มี กาแฟ) แต่ช้ากว่า", "✓ right on this review (กาแฟ is there), but slower"),
    ("sw-warn-box", "หน่วยย่อย: BPE (GPT-4o)", "Subword: BPE (GPT-4o)", "ใช้: ชิ้นที่พบบ่อยในข้อมูลมหาศาล", "uses: frequent pieces of huge data",
     [(t, "plain") for t in ["ที่", "จ", "อด", "รถ", "ห", "าย", "าก", "␣ร", "อน", "าน", "␣ก", "า", "แฟ", "ก็", "ธรรม", "ด", "า"]],
     "✗ 17 ชิ้น ส่วนใหญ่ไม่ใช่คำ (จ | อด) · ␣ = ช่องว่างที่ติดมา", "✗ 17 pieces, most not words (จ | อด) · ␣ = a space kept in the piece"),
]
s = svg("How does each method cut R07, ที่จอดรถหายาก รอนาน กาแฟก็ธรรมดา? 1 Rules, split(): 3 phrases, not words. 2 Dictionary, "
        "newmm: กาแฟก็ธรรมดา becomes กา | แฟก็ธรรม | ดา, so กาแฟ is lost. 3 Learned, attacut: ที่ | จอด | รถ | หา | ยาก | รอ | "
        "นาน | กาแฟ | ก็ | ธรรมดา, right here but slower. 4 Subword, GPT-4o's BPE: 17 pieces, most of them not words.")
s.bubble(W / 2, 8, "R07 “ที่จอดรถหายาก รอนาน กาแฟก็ธรรมดา” แต่ละวิธีตัดอย่างไร", "How does each method cut R07, “ที่จอดรถหายาก รอนาน กาแฟก็ธรรมดา”?", 700)
for k, (band, th, en, uth, uen, toks, rth, ren) in enumerate(ROWS14):
    y0 = 70 + k * 116
    s.box(20, y0, W - 40, 104, band, 12)
    s.badge(46, y0 + 30, k + 1)
    s.both(68, y0 + 37, th, en, "pl-label")
    s.both(40, y0 + 72, uth, uen, "pl-note")
    chips(s, 330, y0 + 34, toks, gap=5, pad=9 if k == 3 else 10)
    s.both(330, y0 + 86, rth, ren, "ml-ok" if band == "nt-band-a" else "ml-neg")
s.save("l12-three-ways.svg", 70 + 4 * 116)


# ================================================================ S04: stretched letters, before and after (.)\1{2,}
ROWS04 = [("R01", "อร่อยมากกกก", [("อร่อย", "keep"), ("มา", "bad"), ("กก", "bad"), ("กก", "bad")], "อร่อยมาก", [("อร่อย", "keep"), ("มาก", "good")]),
          ("R04", "ดีมากกก", [("ดีมาก", "keep"), ("กก", "bad")], "ดีมาก", [("ดีมาก", "good")]),
          ("R10", "นานมากกกกก", [("นาน", "keep"), ("มาก", "keep"), ("กก", "bad"), ("กก", "bad")], "นานมาก", [("นาน", "keep"), ("มาก", "good")])]
s = svg("มากกกก, มากกก, มากกกกก: one word or three? Tokenized as written, newmm makes odd pieces: R01 อร่อยมากกกก → อร่อย | มา | "
        "กก | กก, R04 ดีมากกก → ดีมาก | กก, R10 นานมากกกกก → นาน | มาก | กก | กก, so the 'word' กก is counted 5 times. After "
        "(.)\\1{2,} shortens the stretched letters: อร่อย | มาก, ดีมาก, นาน | มาก, and กก is counted 0 times.")
s.bubble(W / 2, 8, "มากกกก · มากกก · มากกกกก นับเป็นคำเดียว หรือสามคำ", "มากกกก · มากกก · มากกกกก: one word or three?", 600)
for x0, band, th, en, idx, rth, ren, rcls in (
        (20, "sw-warn-box", "✗ ตัดคำทันที (ยังไม่ปรับรูป)", "✗ Tokenized as written", 2, "✗ “คำ” กก ถูกนับ 5 ครั้ง (2 + 1 + 2)", "✗ the “word” กก is counted 5 times (2 + 1 + 2)", "ml-neg"),
        (600, "nt-band-a", "✓ ลดตัวอักษรยืดก่อน แล้วค่อยตัด", "✓ Shorten stretched letters first", 4, "✓ กก 0 ครั้ง เหลือ มาก ตามที่คนอ่าน", "✓ กก 0 times; มาก is left, as a reader sees it", "ml-ok")):
    s.box(x0, 70, 560, 380, band, 14)
    s.both(x0 + 20, 102, th, en, "pl-label")
    if idx == 4:
        s.text(x0 + 20, 136, "(.)\\1{2,} → \\1", "hk-mono")
    for k, row in enumerate(ROWS04):
        y = 170 + k * 80
        s.text(x0 + 20, y + 7, row[0], "dg-index")
        s.thai(x0 + 66, y + 7, row[idx - 1], "pl-text")
        s.arrow(x0 + 210, y, x0 + 236, y)
        chips(s, x0 + 246, y, row[idx])
    s.both(x0 + 20, 428, rth, ren, rcls)
s.both(20, 476, "newmm เก็บ ดีมาก เป็นคำเดียว เพราะอยู่ในพจนานุกรมของมัน", "newmm keeps ดีมาก as one word: it is in its dictionary", "pl-note")
s.save("l12-stretched.svg", 492)


# ================================================================ S04: stem vs lemma on the same five words
WORDS = [("seeks", "seek", True, "seek", True), ("sought", "sought", False, "seek", True), ("seeking", "seek", True, "seek", True),
         ("seeker", "seeker", True, "seeker", True), ("studies", "studi", False, "study", True)]
s = svg("seeks, sought, seeking, seeker, studies: the same word? The Porter stemmer cuts endings by rule: seek, sought, seek, "
        "seeker, studi; sought is not joined to seek and studi is not a real word. Lemmas are dictionary forms: seek, seek, seek, "
        "seeker, study; that needs the word's meaning and grammar. seeker stays seeker in both: it is a different word, a person.")
s.bubble(W / 2, 8, "seeks · sought · seeking · seeker · studies เป็นคำเดียวกันไหม", "seeks · sought · seeking · seeker · studies: the same word?", 640)
for x0, band, th, en, sub_th, sub_en, idx in (
        (20, "sw-warn-box", "Stem (Porter): ตัดส่วนท้ายตามกฎ", "Stem (Porter): cut the ending by rule", "อาจไม่ใช่คำจริง", "may not be a real word", 1),
        (600, "nt-band-a", "Lemma: รูปพจนานุกรม", "Lemma: the dictionary form", "ต้องรู้ความหมายและไวยากรณ์", "needs meaning and grammar", 3)):
    s.box(x0, 70, 560, 400, band, 14)
    s.both(x0 + 20, 102, th, en, "pl-label")
    s.both(x0 + 20, 130, sub_th, sub_en, "pl-note")
    for k, w in enumerate(WORDS):
        y = 172 + k * 56
        s.chip(x0 + 20, y, w[0], "ml-cell", "pl-text", thai=False)
        s.arrow(x0 + 150, y, x0 + 186, y)
        ok = w[idx + 1]
        s.chip(x0 + 196, y, w[idx], "rc-res" if (ok and w[idx] in ("seek", "study")) else ("sw-chip-warn" if not ok else "pl-chip"),
               "ml-ok" if (ok and w[idx] in ("seek", "study")) else ("sw-warn-text" if not ok else "pl-chip-text"), thai=False)
        if w[0] == "sought" and idx == 1:
            s.both(x0 + 310, y + 6, "✗ ไม่ถูกรวมกับ seek", "✗ not joined to seek", "ml-neg")
        if w[0] == "studies" and idx == 1:
            s.both(x0 + 310, y + 6, "✗ ไม่ใช่คำจริง", "✗ not a real word", "ml-neg")
        if w[0] == "seeker":
            s.both(x0 + 330, y + 6, "คนละคำ: ผู้แสวงหา", "another word: a person", "pl-note")
    if idx == 1:
        s.both(x0 + 20, 450, "✗ seek 2 ตัว · sought · seeker · studi", "✗ seek ×2 · sought · seeker · studi", "ml-neg")
    else:
        s.both(x0 + 20, 450, "✓ seek 3 ตัว · seeker · study", "✓ seek ×3 · seeker · study", "ml-ok")
s.save("l12-stem-lemma.svg", 486)


# ================================================================ S22: single words vs bigrams
WORD_TOP = [("กาแฟ", 6), ("อร่อย", 5), ("มาก", 3), ("รอ", 3), ("นาน", 3)]
PAIR_TOP = [("กาแฟ อร่อย", 2), ("ขนม อร่อย", 2), ("รอ นาน", 2), ("นาน มาก", 2), ("บรรยากาศ ดี", 2)]
R10 = ["รอ", "นาน", "มาก", "แต่", "ขนม", "อร่อย", "จริง"]
s = svg("What do customers call tasty, and what do they complain about? Single words: กาแฟ 6, อร่อย 5, มาก 3, รอ 3, นาน 3; อร่อย "
        "says something is tasty but not what, and รอ and นาน are counted apart. Bigrams pair each token with the next: R10's 7 "
        "tokens รอ นาน มาก แต่ ขนม อร่อย จริง give 6 pairs with zip(toks, toks[1:]). The top pairs over all reviews: กาแฟ อร่อย, "
        "ขนม อร่อย, รอ นาน, นาน มาก, บรรยากาศ ดี, 2 each: customers praise both the coffee and the desserts and complain about "
        "waiting a long time.")
s.bubble(W / 2, 8, "ลูกค้าชมว่าอะไรอร่อย และบ่นเรื่องอะไร", "What do customers call tasty, and what do they complain about?", 600)
# single words
s.box(20, 70, 400, 450, "sw-warn-box", 14)
s.both(40, 102, "✗ นับคำเดี่ยว", "✗ Count single words", "pl-label")
for k, (wd, n) in enumerate(WORD_TOP):
    y = 140 + k * 50
    s.thai(110, y + 22, wd, "pl-text", "end")
    s.box(122, y + 4, n * 34, 26, "ml-bar-top" if wd == "อร่อย" else "ml-bar", 4)
    s.text(130 + n * 34, y + 24, str(n), "pl-label")
s.both(40, 418, "อร่อย 5 ครั้ง: แต่อะไรอร่อย", "อร่อย 5 times: but what is tasty?", "ml-neg")
s.both(40, 450, "รอ 3 กับ นาน 3 ถูกนับแยกกัน", "รอ 3 and นาน 3 are counted apart", "ml-neg")
s.both(40, 500, "✗ เห็นคำ แต่ไม่เห็นบริบท", "✗ words, but no context", "ml-neg")
# bigrams: how zip pairs neighbours, then the counts
s.box(440, 70, 720, 450, "nt-band-a", 14)
s.both(460, 102, "✓ นับคู่คำติดกัน (bigram)", "✓ Count neighbouring pairs (bigrams)", "pl-label")
s.text(460, 136, "zip(toks, toks[1:])", "hk-mono")
s.both(760, 136, "R10 หลัง clean: 7 คำ", "R10 after clean: 7 tokens", "pl-note")
for row, (toks, y) in enumerate(((R10, 172), (R10[1:], 222))):  # fixed-width cells, so zip's pairs stand in columns
    for i, tok in enumerate(toks):
        x = 460 + i * 84
        s.box(x, y - 17, 76, 34, "pl-chip", 8)
        s.thai(x + 38, y + 6, tok, "pl-chip-text", "middle")
for i in range(6):
    s.box(456 + i * 84, 148, 84, 98, "dg-row", 10)
s.both(1150, 178, "toks", "toks", "pl-note", "end")
s.both(1150, 228, "toks[1:]", "toks[1:]", "pl-note", "end")
s.both(460, 270, "แต่ละคำจับคู่กับคำถัดไป: 7 คำ ได้ 6 คู่", "each word pairs with the next: 7 tokens, 6 pairs", "pl-note")
for k, (pair, n) in enumerate(PAIR_TOP):
    y = 288 + k * 36
    s.thai(640, y + 21, pair, "pl-text", "end")
    s.box(652, y + 5, n * 60, 24, "ml-bar-top" if "อร่อย" in pair else "ml-bar", 4)
    s.text(660 + n * 60, y + 23, str(n), "pl-label")
s.both(800, 322, "← ชมทั้งกาแฟและขนม", "← both coffee and desserts", "ml-ok")
s.both(800, 394, "← บ่นเรื่องรอนาน", "← complaints about long waits", "ml-ok")
s.both(460, 504, "✓ คู่คำบอกบริบท (ไม่ตัด stop words เพราะ นาน กับ ไม่ ให้ความหมาย)", "✓ pairs show context (stop words kept: นาน and ไม่ carry meaning)", "ml-ok")
s.save("l12-bigrams.svg", 536)
