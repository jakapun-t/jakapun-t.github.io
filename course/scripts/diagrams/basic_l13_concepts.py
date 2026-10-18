"""Concept pictures for nlp-basic lesson 13 (text classification and LLMs), in the style of nlp l12-why-chunk.svg:
the running example's question on top, drawn objects, arrows at the exact spot. ไทย/EN labels follow the language
switch; Thai review text is language data and shows in both.

    python3 scripts/diagrams/basic_l13_concepts.py courses/nlp-basic/images

The reviews are the lesson's own (data/l13_reviews_cls.csv: C02 positive, C10 negative; the running example
ร้านนี้ราคาแพงแต่อร่อย) and the prompt is the lesson's FEW_SHOT. Gemini's answer is left as "?": students run the
code and fill it in (the card's exercise). 100 reviews × time.sleep(6) = 600 s = 10 minutes.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from basic_svg import Svg  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
W = 1180


def svg(title):
    return Svg(OUT, W, title)


# ================================================================ S01: one text in, one label out, from a fixed list
s = svg("Which review praises, which complains? A text classifier reads each text and gives it one label from a list fixed "
        "in advance, the classes positive and negative: C02 ส้มตำอร่อยมาก บรรยากาศดี goes to positive, C10 ร้านสกปรก "
        "แกงเขียวหวานรสชาติแย่ goes to negative. The lesson's hard case, ร้านนี้ราคาแพงแต่อร่อย (pricey but tasty), is "
        "the one this lesson tries several ways.")
s.bubble(W / 2, 8, "รีวิวไหนชม รีวิวไหนติ", "Which review praises, which complains?", 420)
CARDS = [("C02", "ส้มตำอร่อยมาก บรรยากาศดี", "ml-cell"), ("C10", "ร้านสกปรก แกงเขียวหวานรสชาติแย่", "ml-cell"),
         ("?", "ร้านนี้ราคาแพงแต่อร่อย", "pl-chip-del")]
s.badge(34, 92, 1)
s.both(56, 98, "ข้อความเข้า", "A text goes in", "pl-label")
for k, (rid, text, cls) in enumerate(CARDS):
    y = 116 + k * 92
    s.box(20, y, 400, 74, cls, 12)
    s.text(38, y + 30, rid if rid != "?" else "", "dg-index")
    if rid == "?":
        s.both(38, y + 30, "รีวิวของบทนี้ (ยากกว่า)", "this lesson's hard case", "pl-note")
    s.thai(38, y + 58, text, "pl-text")
# the classifier
s.box(500, 176, 230, 116, "ml-model", 16)
s.both(615, 222, "ตัวจัดกลุ่ม", "text classifier", "ml-model-text", "middle")
s.both(615, 252, "อ่าน แล้วเลือก 1 ป้าย", "reads, picks 1 label", "ml-model-sub", "middle")
s.badge(615, 160, 2)
for k in range(3):
    s.arrow(424, 153 + k * 92, 494, 214 + k * 20, dashed=k == 2)
# the classes: bins fixed in advance
s.badge(792, 92, 3)
s.both(814, 98, "class: รายการป้ายที่กำหนดไว้ก่อน", "Classes: a list fixed in advance", "pl-label")
s.box(770, 116, 390, 108, "rc-res", 14)
s.text(790, 148, "positive", "ml-ok")
s.box(782, 164, 366, 42, "ml-cell", 8)
s.text(796, 192, "C02", "dg-index")
s.thai(840, 192, "ส้มตำอร่อยมาก บรรยากาศดี", "pl-text")
s.box(770, 244, 390, 108, "sw-warn-box", 14)
s.text(790, 276, "negative", "ml-neg")
s.box(782, 292, 366, 42, "ml-cell", 8)
s.text(796, 320, "C10", "dg-index")
s.thai(840, 320, "ร้านสกปรก แกงเขียวหวานรสชาติแย่", "pl-text")
s.arrow(736, 214, 764, 176)
s.arrow(736, 254, 764, 292)
s.both(748, 404, "ร้านนี้ราคาแพงแต่อร่อย ไปกล่องไหน? บทนี้ลองหลายวิธีกับรีวิวนี้", "Which box for ร้านนี้ราคาแพงแต่อร่อย? This lesson tries several ways on it",
       "pl-note", "middle")
s.both(20, 456, "✓ ข้อความ 1 ชิ้นเข้า → ป้าย (class) 1 ป้ายออก จากรายการที่ตั้งไว้ก่อน", "✓ One text in → one label (class) out, from a list set beforehand", "ml-ok")
s.save("l13-what-classify.svg", 472)


# ================================================================ S19: the few-shot prompt classify() builds, and one call per review
s = svg("Classify reviews with Gemini, no training. classify(text) builds one prompt: 1 the instruction (sort restaurant "
        "reviews into positive or negative, answer in one word), 2 three examples, few-shot (ต้มยำอร่อยมาก ร้านสะอาด → "
        "positive, รอนานมาก ผัดไทยจืดมาก → negative, ส้มตำเค็มเกินไป พนักงานบริการดี จะกลับมาอีก → positive), 3 the new review "
        "with an arrow and nothing after it. Gemini answers one word, which classify strips and lowercases; that answer is "
        "yours to run and fill in. Each review is one API call: our 100 reviews with time.sleep(6) take about 10 minutes.")
s.bubble(W / 2, 8, "ให้ Gemini จัดกลุ่มรีวิว โดยไม่ต้องเทรน", "Classify reviews with Gemini, no training", 520)
s.box(20, 70, 660, 330, "ml-cell", 10)
s.box(20, 70, 660, 36, "dg-xl-head", 10)
s.both(40, 95, "prompt ที่ classify(text) สร้าง", "The prompt classify(text) builds", "ml-box-h")
LINES = [(1, "จัดกลุ่มรีวิวร้านอาหารเป็น positive หรือ negative ตอบคำเดียว", "pl-text", None),
         (2, "\"ต้มยำอร่อยมาก ร้านสะอาด\" → positive", "pl-text", None),
         (None, "\"รอนานมาก ผัดไทยจืดมาก\" → negative", "pl-text", None),
         (None, "\"ส้มตำเค็มเกินไป พนักงานบริการดี จะกลับมาอีก\" → positive", "pl-text", None),
         (3, "\"ร้านนี้ราคาแพงแต่อร่อย\" →", "pl-label", "rc-con")]
for k, (badge, text, cls, band) in enumerate(LINES):
    y = 146 + k * 46
    if band:
        s.box(56, y - 28, 604, 40, band, 8)
    if badge:
        s.badge(40, y - 7, badge)
    s.thai(68, y, text, cls)
s.both(40, 384, "1 คำสั่ง · 2 ตัวอย่าง 3 ข้อ (few-shot) · 3 รีวิวใหม่ต่อท้าย", "1 the instruction · 2 three examples (few-shot) · 3 the new review",
       "pl-note")
# Gemini and its one-word answer
s.arrow(684, 236, 740, 236)
s.box(744, 180, 200, 112, "ml-model", 16)
s.text(844, 228, "Gemini", "ml-model-text", "middle")
s.text(844, 256, "flash-lite", "ml-model-sub", "middle")
s.arrow(948, 236, 1000, 236)
s.box(1004, 206, 156, 60, "nt-out", 12)
s.text(1082, 245, "?", "pl-label", "middle")
s.both(1082, 296, "คำตอบ 1 คำ", "a one-word answer", "pl-note", "middle")
s.both(1082, 322, "positive / negative", "positive / negative", "pl-note", "middle")
s.text(1082, 350, ".strip().lower()", "dg-code", "middle")
s.both(1082, 384, "รันแล้วเติมเอง", "run it and fill it in", "ml-ok", "middle")
# one call per review
s.box(20, 420, W - 40, 112, "nt-band-b", 14)
s.both(40, 452, "1 รีวิว = เรียก API 1 ครั้ง", "1 review = 1 API call", "pl-label")
s.both(1140, 452, "100 รีวิวของเรา + time.sleep(6) ≈ 600 วินาที = 10 นาที", "our 100 reviews + time.sleep(6) ≈ 600 seconds = 10 minutes",
       "pl-label", "end")
for k, text in enumerate(["อาหารอร่อย บรรยากาศดี", "ผัดไทยไม่อร่อยเลย", "ร้านนี้ราคาแพงแต่อร่อย"]):
    x = 40 + k * 376
    s.box(x, 470, 230, 42, "ml-cell", 8)
    s.thai(x + 115, 498, text, "pl-text", "middle")
    s.arrow(x + 234, 491, x + 262, 491)
    s.box(x + 266, 472, 76, 38, "ml-model", 8)
    s.text(x + 304, 497, f"call {k + 1}", "ml-model-sub", "middle")
s.save("l13-gemini-classify.svg", 548)
