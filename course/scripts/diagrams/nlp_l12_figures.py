"""Draws the infographics of lesson 12 of the international NLP course (Gemini API and RAG):
SVG, inlined into the page; ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/nlp_l12_figures.py courses/nlp/images

Real numbers: the retrieval scores (all-MiniLM-L6-v2, computed in course/.venv) and the
bi-encoder / cross-encoder scores (all-MiniLM-L6-v2, cross-encoder/ms-marco-MiniLM-L6-v2).
The before/after reranking lists are real scores too (query 'What is taught on 19 October?').

Uses the nt-*, pl-*, sw-*, ml-* and dg-* classes in templates/page.css.
"""

import math
import os
import sys
import unicodedata
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp/images"
FS = 19


def width(s, fs=FS):
    return sum(0 if unicodedata.category(c) == "Mn" else fs * (1.1 if ord(c) > 0x1F000 else 0.58) for c in s)


class Svg:
    def __init__(self, w, title):
        self.w, self.title, self.out = w, title, []

    def both(self, x, y, th, en, cls, anchor="start"):
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="th">{escape(th)}</text>')
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="en" lang="en">{escape(en)}</text>')

    def text(self, x, y, s, cls, anchor="start"):
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}">{escape(s)}</text>')

    def chip(self, x, y, t, cls="pl-chip", tcls="pl-chip-text"):
        w = width(t) + 24
        self.out.append(f'<rect x="{x:g}" y="{y - 17:g}" width="{w:g}" height="34" rx="9" class="{cls}"/>')
        self.text(x + w / 2, y + 6, t, tcls, "middle")
        return x + w

    def box(self, x, y, w, h, cls, rx=12):
        self.out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}"/>')

    def arrow(self, x1, y1, x2, y2, dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="pl-line"{dash}/>')
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 10 * math.cos(a - 0.55), y2 - 10 * math.sin(a - 0.55))
        p2 = (x2 - 10 * math.cos(a + 0.55), y2 - 10 * math.sin(a + 0.55))
        self.out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2:g} {y2:g} L{p2[0]:.1f} {p2[1]:.1f}" class="pl-line"/>')

    def node(self, x, y, w, h, th, en, cls="nt-bubble", sub_th=None, sub_en=None, tcls="pl-label"):
        """A box with a label (and an optional note under it), both centred."""
        self.box(x, y, w, h, cls, 12)
        cy = y + h / 2 + (6 if sub_th is None else -6)
        self.both(x + w / 2, cy, th, en, tcls, "middle")
        if sub_th is not None:
            self.both(x + w / 2, cy + 24, sub_th, sub_en, "pl-note", "middle")

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


# ---------------------------------------------------------------- 1. an API call from Colab
s = Svg(900, "An API call: your Python code in Colab sends a request with the prompt and an API key over the internet; Gemini's server sends back a response.")
s.box(20, 30, 230, 120, "nt-band-a", 14)
s.both(135, 62, "โค้ด Python ของเรา", "Our Python code", "pl-label", "middle")
s.text(135, 100, "Google Colab", "pl-note", "middle")
s.box(650, 30, 230, 120, "nt-band-b", 14)
s.both(765, 62, "เซิร์ฟเวอร์ของโมเดล", "The model's server", "pl-label", "middle")
s.text(765, 100, "Gemini", "pl-note", "middle")
s.arrow(258, 70, 642, 70)
s.text(450, 52, "request: prompt + API key (JSON)", "pl-note", "middle")
s.arrow(642, 118, 258, 118)
s.both(450, 142, "response: ข้อความคำตอบ", "response: the answer text", "pl-note", "middle")
s.both(20, 190, "ต้องมี 2 อย่าง: ที่อยู่ของ API (endpoint) และ API key ซึ่งต้องเก็บเป็นความลับเหมือนรหัสผ่าน",
       "You need 2 things: the API's address (endpoint) and an API key, which you keep secret like a password", "sw-warn-text")
s.save("l12-api.svg", 206)

# ---------------------------------------------------------------- 2. a Gemini key into Colab Secrets
s = Svg(900, "Four steps: create a key in Google AI Studio, open Colab's Secrets panel, save the key as GOOGLE_API_KEY with notebook access on, then read it with userdata.get.")
steps = [
    ("สร้าง key", "Create a key", "aistudio.google.com", "/apikey → Create", "/apikey → Create"),
    ("เปิด Secrets", "Open Secrets", "แถบซ้ายของ Colab: 🔑", "Colab's left bar: 🔑", None),
    ("ตั้งชื่อ secret", "Name the secret", "GOOGLE_API_KEY", "เปิด Notebook access", "turn on Notebook access"),
    ("อ่านในโค้ด", "Read it in code", "userdata.get(", '"GOOGLE_API_KEY")', '"GOOGLE_API_KEY")'),
]
for i, (th, en, l1, l2th, l2en) in enumerate(steps):
    x = 10 + i * 224
    s.box(x, 14, 204, 150, "nt-band-a" if i % 2 == 0 else "nt-band-b", 14)
    s.out.append(f'<circle cx="{x + 30}" cy="44" r="15" class="pl-dot"/>')
    s.text(x + 30, 49, str(i + 1), "pl-num", "middle")
    s.both(x + 54, 50, th, en, "pl-label")
    if i == 1:
        s.both(x + 102, 100, l1, l2th, "pl-note", "middle")
        s.both(x + 102, 126, "+ Add new secret", "+ Add new secret", "pl-note", "middle")
    else:
        cls = "dg-code" if i >= 2 else "pl-note"
        s.text(x + 102, 100, l1, cls, "middle")
        s.both(x + 102, 126, l2th, l2en, "dg-code" if i == 3 else "pl-note", "middle")
    if i < 3:
        s.arrow(x + 206, 89, x + 222, 89)
s.both(10, 196, "key อยู่ใน Secrets ไม่อยู่ในโค้ด แชร์ notebook ได้โดย key ไม่ติดไปด้วย",
       "The key lives in Secrets, not in the code: share the notebook and the key stays with you", "ml-ok")
s.save("l12-colab-key.svg", 212)

# ---------------------------------------------------------------- 3. closed-book vs open-book exam
s = Svg(900, "An LLM alone is like a closed-book exam: it answers from memory and may make an answer up. RAG is an open-book exam: it looks up the course facts first and cites them.")
panels = [
    (10, "nt-band-b", "LLM อย่างเดียว = สอบปิดตำรา", "LLM alone = closed-book exam",
     "🧠", "ตอบจากความจำ (ข้อมูลตอนเทรน)", "answers from memory (training data)",
     None, None, "“น่าจะกลางเดือนธันวาคม”", "“Probably mid-December.”", "sw-chip-warn",
     "✗ เดาเอง ไม่มีที่มา", "✗ made up, no source", "ml-neg"),
    (460, "nt-band-a", "RAG = สอบเปิดตำรา", "RAG = open-book exam",
     "🔎", "ค้นข้อมูลของวิชาก่อน", "looks up the course facts first",
     "fact 7: final exam, Monday 30 November 2026", None, "“Monday 30 November 2026 [fact 7]”", None, "pl-chip",
     "✓ ตรงกับเอกสาร บอกที่มา", "✓ matches the source, cites it", "ml-ok"),
]
for x, band, hth, hen, icon, nth, nen, fact, _, ath, aen, acls, vth, ven, vcls in panels:
    s.box(x, 10, 430, 290, band, 14)
    s.both(x + 20, 44, hth, hen, "pl-label")
    s.box(x + 20, 62, 390, 44, "nt-bubble", 22)
    s.text(x + 38, 91, "When is the 2190519 final exam?", "pl-text")
    s.text(x + 30, 146, icon, "nt-icon")
    s.both(x + 66, 144, nth, nen, "pl-note")
    if fact:
        s.box(x + 20, 160, 390, 34, "ml-cell", 8)
        s.text(x + 30, 183, fact, "dg-code")
    aen = aen or ath
    w = max(width(ath), width(aen)) + 24
    s.out.append(f'<rect x="{x + 20}" y="{226 - 17}" width="{w:g}" height="34" rx="9" class="{acls}"/>')
    s.both(x + 32, 232, ath, aen, "pl-text")
    s.both(x + 20, 280, vth, ven, vcls)
s.both(10, 330, "ตัวอย่างคำตอบที่เดาเอง เป็นภาพประกอบ ไม่ใช่คำตอบจริงของโมเดล",
       "The made-up answer is an illustration, not a real model output", "pl-note")
s.save("l12-closed-open.svg", 344)

# ---------------------------------------------------------------- 4. the RAG pipeline
s = Svg(900, "The RAG pipeline. Indexing, once: documents are split into chunks, embedded and saved in a vector store. Retrieval, per question: the question is embedded and the closest chunks are found. Generation: the question and the chunks go into the prompt, and the LLM writes the answer.")
rows = [
    (10, "nt-band-a", "1 Indexing", "ทำครั้งเดียว ก่อนมีคำถาม", "once, before any question",
     [("เอกสาร", "Documents"), ("ตัดเป็น chunk", "Split into chunks"), ("Embed", "Embed"), ("Vector store", "Vector store")]),
    (150, "nt-band-b", "2 Retrieval", "ทุกครั้งที่มีคำถาม", "for every question",
     [("คำถาม", "Question"), ("Embed คำถาม", "Embed the question"), ("หา vector ใกล้สุด", "Find closest vectors"), ("chunk top-k", "Top-k chunks")]),
]
for y, band, title, th, en, nodes in rows:
    s.box(10, y, 880, 126, band, 14)
    s.text(26, y + 30, title, "pl-label")
    s.both(160, y + 30, th, en, "pl-note")
    for i, (nth, nen) in enumerate(nodes):
        x = 26 + i * 218
        s.node(x, y + 50, 194, 56, nth, nen, "nt-bubble", tcls="pl-text")
        if i < 3:
            s.arrow(x + 196, y + 78, x + 216, y + 78)
s.arrow(680 + 70, 116, 462 + 110, 198, dashed=True)  # the store is searched
s.both(700, 176, "ค้นใน store", "search the store", "pl-note")
y = 290
s.box(10, y, 880, 126, "nt-band-a", 14)
s.text(26, y + 30, "3 Generation", "pl-label")
s.both(180, y + 30, "ส่งให้ LLM เขียนคำตอบ", "the LLM writes the answer", "pl-note")
s.node(26, y + 50, 412, 56, "Prompt = คำถาม + chunk top-k", "Prompt = question + top-k chunks", "nt-out", tcls="pl-text")
s.node(462, y + 50, 194, 56, "LLM (Gemini)", "LLM (Gemini)", "nt-bubble", tcls="pl-text")
s.node(680, y + 50, 194, 56, "คำตอบ + ที่มา", "Answer + source", "nt-out", tcls="pl-text")
s.arrow(440, y + 78, 460, y + 78)
s.arrow(658, y + 78, 678, y + 78)
# the chunks go into the prompt: down from "Top-k chunks", left under the row title, down into the prompt
s.out.append(f'<path d="M777 258 L777 {y + 41} L380 {y + 41} L380 {y + 46}" class="pl-line" stroke-dasharray="6 5"/>')
s.arrow(380, y + 40, 380, y + 48)
s.save("l12-pipeline.svg", 426)

# ---------------------------------------------------------------- 5. fixed-size chunks with overlap
TEXT = "Class meets on Mondays in room 501. The final exam is on 30 November."
SIZE, OVERLAP = 30, 8
step = SIZE - OVERLAP
chunks = [(i, TEXT[i:i + SIZE]) for i in range(0, len(TEXT) - OVERLAP, step)]
CW = 14 * 0.6  # IBM Plex Mono at 14px: 0.6em per character
X0 = 30
s = Svg(900, f"Fixed-size chunking of a {len(TEXT)}-character text: chunk_size {SIZE}, chunk_overlap {OVERLAP}, so each chunk starts {step} characters after the last and repeats its last {OVERLAP} characters.")
s.both(X0, 30, "ข้อความเต็ม", "The whole text", "nt-head")
s.box(X0 - 8, 44, len(TEXT) * CW + 16, 34, "ml-cell", 8)
s.out.append(f'<text x="{X0}" y="67" class="dg-code" xml:space="preserve">{escape(TEXT)}</text>')
y = 120
for k, (start, piece) in enumerate(chunks):
    x = X0 + start * CW
    s.box(x - 4, y - 22, len(piece) * CW + 8, 34, "pl-chip", 8)
    ov = min(OVERLAP, len(piece)) if k > 0 else 0
    if ov:
        s.box(x - 4, y - 22, ov * CW + 4, 34, "sw-chip-warn", 8)
    s.out.append(f'<text x="{x:g}" y="{y:g}" class="dg-code" xml:space="preserve">{escape(piece)}</text>')
    s.text(x + len(piece) * CW + 14, y, f"chunk {k + 1}", "pl-note")
    y += 46
s.box(X0, y - 4, 22, 20, "sw-chip-warn", 4)
s.both(X0 + 32, y + 12, f"overlap: {OVERLAP} ตัวอักษรที่ซ้ำกับท้าย chunk ก่อนหน้า", f"overlap: {OVERLAP} characters repeated from the end of the previous chunk", "pl-note")
s.both(X0, y + 46, "chunk ตัดกลางคำได้ overlap ช่วยให้คำหรือประโยคที่ถูกตัดยังอยู่ครบใน chunk ใด chunk หนึ่ง",
       "Chunks can cut through words; the overlap keeps a cut word or sentence whole in one of them", "sw-warn-text")
s.save("l12-chunks.svg", y + 66)

# ---------------------------------------------------------------- 9. hybrid search + reranking
s = Svg(900, "Hybrid search: the query goes to BM25 keyword search and to dense vector search; their top-20 lists are merged with reciprocal rank fusion, a cross-encoder reranks the merged list, and the top 5 go to the LLM.")
s.node(10, 120, 120, 56, "Query", "Query", "nt-bubble", tcls="pl-text")
s.node(170, 30, 190, 80, "BM25", "BM25", "ml-cell-b", "ตรงคำ (keyword)", "exact keywords")
s.node(170, 186, 190, 80, "Dense", "Dense", "ml-cell-b", "ใกล้ความหมาย", "close in meaning")
s.arrow(132, 140, 168, 80)
s.arrow(132, 156, 168, 216)
s.text(400, 76, "top 20", "pl-note", "middle")
s.text(400, 232, "top 20", "pl-note", "middle")
s.arrow(362, 70, 440, 136)
s.arrow(362, 226, 440, 160)
s.node(442, 112, 120, 72, "RRF", "RRF", "nt-out", "รวมลำดับ", "fuse ranks")
s.arrow(564, 148, 590, 148)
s.node(592, 112, 150, 72, "Rerank", "Rerank", "ml-cell-b", "cross-encoder", "cross-encoder")
s.arrow(744, 148, 770, 148)
s.node(772, 112, 118, 72, "LLM", "LLM", "nt-bubble", "top 5", "top 5")
s.both(10, 312, "Hybrid เพิ่มความครอบคลุมของผู้สมัคร (coverage)  ·  Rerank จัดลำดับให้ดีขึ้น (ordering)",
       "Hybrid improves candidate coverage  ·  Reranking improves candidate ordering", "ml-ok")
s.save("l12-hybrid.svg", 330)

# ---------------------------------------------------------------- 12. before / after reranking (real scores)
# query "What is taught on 19 October?" on the 7 course facts: stage 1 keeps the bi-encoder's top 4
# (all-MiniLM-L6-v2 cosine), stage 2 rescores them (cross-encoder/ms-marco-MiniLM-L6-v2); computed in course/.venv
s = Svg(900, "Real scores for 'What is taught on 19 October?': the bi-encoder ranks fact 4, the answer, 4th; the cross-encoder moves it to 1st.")
before = [("fact 5 · 26 Oct: agents", "0.428"), ("fact 3 · 12 Oct: no class", "0.418"),
          ("fact 2 · 21 Sep: midterm", "0.355"), ("fact 4 · 19 Oct: RAG ★", "0.347")]
after = [("fact 4 · 19 Oct: RAG ★", "3.974"), ("fact 3 · 12 Oct: no class", "−3.440"),
         ("fact 5 · 26 Oct: agents", "−5.287"), ("fact 2 · 21 Sep: midterm", "−10.742")]
s.box(10, 10, 880, 54, "nt-bubble", 27)
s.text(30, 44, "Query: What is taught on 19 October?", "pl-text")
for x, th, en, items in [(10, "ก่อน: bi-encoder (cosine)", "Before: bi-encoder (cosine)", before),
                         (510, "หลัง: cross-encoder (คะแนน)", "After: cross-encoder (score)", after)]:
    s.both(x, 100, th, en, "pl-label")
    for k, (t, score) in enumerate(items):
        y = 132 + k * 50
        s.box(x, y - 22, 380, 40, "sw-chip-warn" if "★" in t else "ml-cell", 8)
        s.text(x + 14, y + 4, f"{k + 1}. {t}", "pl-text")
        s.text(x + 366, y + 4, score, "pl-text", "end")
s.arrow(392, 282, 508, 132)
s.both(10, 352, "คะแนนจริงจากข้อเท็จจริง 7 ข้อ  ·  ถ้าใช้ k = 2 จาก bi-encoder อย่างเดียว fact 4 จะไม่ถึง LLM",
       "Real scores on the 7 course facts · with k = 2 from the bi-encoder alone, fact 4 never reaches the LLM", "pl-note")
s.save("l12-rerank-before-after.svg", 368)

# ---------------------------------------------------------------- 13. the hook: what Gemini learned vs our course page
# Gemini's "7 December 2026" is an illustration of a made-up answer, and the figure says so.
s = Svg(900, "Ask Gemini 'When is the final exam of 2190519?'. Gemini learned from public text such as Wikipedia, books, news and public websites, "
             "up to a cutoff date. Our course page, with the real date (Monday 30 November 2026), is behind a password and was written this semester, "
             "so Gemini never saw it. It may still answer confidently with a made-up date: a hallucination.")


def chip_row(x, y, labels_th, labels_en, cls="pl-chip", tcls="pl-chip-text"):
    for lang, labels in (("th", labels_th), ("en", labels_en)):
        s.out.append(f'<g data-only="{lang}"' + (' lang="en"' if lang == "en" else "") + ">")
        xx = x
        for t in labels:
            xx = s.chip(xx, y, t, cls, tcls) + 10
        s.out.append("</g>")


s.box(225, 10, 450, 48, "nt-bubble", 24)
s.text(450, 41, "When is the final exam of 2190519?", "pl-text", "middle")
s.arrow(450, 60, 450, 84)
# what Gemini learned
s.box(20, 90, 520, 220, "nt-band-a", 14)
s.both(40, 124, "🧠 สิ่งที่ Gemini เรียนมา (ข้อมูลที่ใช้เทรน)", "🧠 What Gemini learned (its training data)", "pl-label")
s.both(40, 152, "ข้อความสาธารณะ เก็บถึงวันหนึ่ง (knowledge cutoff)", "public text, collected up to a cutoff date", "pl-note")
chip_row(40, 196, ["Wikipedia", "หนังสือ", "ข่าว", "เว็บสาธารณะ"], ["Wikipedia", "books", "news", "public websites"])
chip_row(40, 250, ["หน้าเว็บวิชาของเรา"], ["our course page"], "pl-chip-del", "pl-del")
s.both(40, 292, "✗ วันสอบไม่ได้อยู่ในนี้", "✗ the exam date is not in here", "ml-neg")
# our course page
s.box(560, 90, 320, 220, "nt-band-b", 14)
s.both(580, 124, "🔒 หน้าเว็บวิชาของเรา", "🔒 Our course page", "pl-label")
s.both(580, 152, "ต้องใช้รหัสผ่าน · เขียนเทอมนี้", "password-only · new this term", "pl-note")
s.box(580, 172, 280, 76, "ml-cell", 10)
s.text(596, 202, "The final exam is on", "pl-text")
s.text(596, 230, "Monday 30 November 2026.", "pl-text")
s.both(580, 292, "Gemini ไม่เคยเห็นหน้านี้", "Gemini never saw this page", "pl-note")
s.out.append('<path d="M550 98 L550 302" class="pl-line" stroke-dasharray="6 6"/>')
# what happens
s.both(20, 352, "Gemini อาจตอบว่า", "Gemini may answer", "pl-note")
w = s.chip(190, 346, "“The final exam is on 7 December 2026.”", "sw-chip-warn", "pl-text")
s.both(w + 14, 352, "✗ มั่นใจ ไม่มีที่มา ผิด", "✗ sure, no source, wrong", "ml-neg")
s.both(20, 396, "คำตอบที่แต่งขึ้นแบบนี้เรียกว่า hallucination", "A made-up answer like this is called a hallucination", "sw-warn-text")
s.both(20, 430, "คำตอบของ Gemini ในรูปเป็นตัวอย่าง ไม่ใช่ผลรันจริง", "Gemini's answer here is an example, not a real model run", "pl-note")
s.save("l12-hook.svg", 444)

# ---------------------------------------------------------------- 15. limits of LLM question answering with no outside documents (from the slides)
GROUPS = [
    ("ปัญหาความถูกต้อง (accuracy issues)", "Accuracy issues", [
        ("📅 Knowledge cutoff", "📅 Knowledge cutoff", "ค่าพารามิเตอร์อัปเดตถึงวันหนึ่งเท่านั้น", "updated only up to a certain date",
         "ตารางปี 2026 มาหลังการเทรน", "the 2026 schedule came after training"),
        ("🔒 ข้อมูลส่วนตัว", "🔒 Private data", "ข้อมูลส่วนตัวไม่ได้ถูกใช้เทรน", "private files are not used for training",
         "หน้าเว็บวิชาต้องใช้รหัสผ่าน", "our course page needs a password"),
        ("🧩 เรียนรู้ไม่สำเร็จ", "🧩 Learning failures", "เคยเห็นตอนเทรน แต่น้อยเกินจะจำได้", "seen in training, but too rarely to learn",
         "2190519 มีในเว็บแค่ไม่กี่หน้า", "2190519 is on very few web pages"),
    ]),
    ("ปัญหาการตรวจสอบ (verifiability issues)", "Verifiability issues", [
        ("🔍 ตรวจสอบยาก", "🔍 Hard to check", "ไม่มีที่มา จึงแยกไม่ออกว่าถูกหรือผิด", "no source, so right and wrong look alike",
         "\"7 December 2026\" ฟังดูมั่นใจพอกัน", "\"7 December 2026\" sounds just as sure"),
    ]),
]
W = 1180
s = Svg(W, "Limits of question answering with an LLM alone, with no outside documents. Accuracy issues: knowledge cutoff, private data, "
           "learning failures. Verifiability issues: no source, so a wrong answer looks as sure as a right one. Each with its example in our course.")
s.both(36, 30, "ข้อจำกัด", "Limit", "nt-head")
s.both(330, 30, "หมายความว่า", "What it means", "nt-head")
s.both(790, 30, "ในวิชาของเรา", "In our course", "nt-head")
y = 44
for gth, gen, rows in GROUPS:
    s.box(20, y, W - 40, 34 + 54 * len(rows), "sw-warn-box" if gen.startswith("Verif") else "nt-band-b", 14)
    s.both(36, y + 25, gth, gen, "pl-label")
    y += 38
    for nth, nen, mth, men, eth, een in rows:
        s.box(30, y, W - 60, 46, "ml-cell", 10)
        s.both(46, y + 30, nth, nen, "nt-task")
        s.both(330, y + 30, mth, men, "hk-desc")
        s.both(790, y + 30, eth, een, "ml-neg")
        y += 54
    y += 14
s.save("l12-llm-limits.svg", y - 4)

# ---------------------------------------------------------------- 16. the RAG app flow (after the teacher's reference picture)
# 1 the user asks our app; 2 the app sends the question to search; 3 relevant facts come back;
# 4 prompt + question + context go to the LLM; 5 the generated answer comes back. Facts are the lesson's real top 2.
s = Svg(900, "How a RAG app answers. 1 The user asks our app: When is the final exam? 2 The app sends the question to search, "
             "which looks in the knowledge sources (the 7 course facts in a vector store). 3 The relevant information comes back: "
             "fact 7 and fact 2. 4 The app sends the prompt, the question and this context to the LLM (Gemini). "
             "5 The LLM sends back the generated answer: 30 November 2026 [fact 7].")


def badge(x, y, k):
    s.out.append(f'<circle cx="{x}" cy="{y}" r="13" class="pl-dot"/>')
    s.text(x, y + 5, str(k), "pl-num", "middle")


def path(d, arrow_to=None):
    s.out.append(f'<path d="{d}" class="pl-line"/>')
    if arrow_to:
        (x1, y1), (x2, y2) = arrow_to
        s.arrow(x1, y1, x2, y2)


# the user
s.box(20, 180, 190, 120, "nt-band-b", 14)
s.out.append('<circle cx="115" cy="208" r="14" class="pl-line"/><path d="M89 248 Q115 214 141 248" class="pl-line"/>')
s.both(115, 272, "“When is the", "“When is the", "pl-note", "middle")
s.both(115, 292, "final exam?”", "final exam?”", "pl-note", "middle")
# our app: a laptop
s.out.append('<rect x="352" y="200" width="100" height="66" rx="6" class="pl-line"/>'
             '<rect x="362" y="210" width="30" height="46" rx="2" class="pl-line"/>'
             '<path d="M400 216 H442 M400 228 H442 M400 240 H442 M400 252 H430" class="pl-line"/>'
             '<path d="M334 274 H470 L460 286 H344 Z" class="pl-line"/>')
s.both(402, 312, "แอป RAG ของเรา", "Our RAG app", "pl-label", "middle")
s.text(402, 334, "Python + LangChain", "pl-note", "middle")
# 1 question in
s.arrow(212, 240, 330, 240)
badge(232, 214, 1)
s.both(252, 220, "คำถาม", "Question", "pl-note")
# search
s.box(272, 36, 316, 70, "nt-bubble", 12)
s.both(430, 64, "ค้นข้อมูลที่เกี่ยวข้อง", "Search relevant information", "pl-label", "middle")
s.both(430, 90, "embed + หา vector ที่ใกล้สุด", "embed + find closest vectors", "pl-note", "middle")
# 2 query up
s.arrow(372, 196, 372, 110)
badge(286, 150, 2)
s.both(362, 156, "Query", "Query", "pl-note", "end")
# knowledge sources
s.arrow(590, 71, 610, 71)
s.out.append('<path d="M632 14 H616 V128 H632" class="pl-line"/>')
s.out.append('<path d="M652 20 H672 L682 30 V62 H652 Z M672 20 V30 H682 M658 38 H676 M658 46 H676 M658 54 H670" class="pl-line"/>')
s.out.append('<ellipse cx="667" cy="86" rx="15" ry="5" class="pl-line"/><path d="M652 86 V114 C652 121 682 121 682 114 V86 M652 100 C652 107 682 107 682 100" class="pl-line"/>')
s.both(698, 47, "ข้อเท็จจริง 7 ข้อของวิชา", "the 7 course facts", "pl-note")
s.text(698, 106, "vector store", "pl-note")
s.both(616, 156, "แหล่งความรู้", "Knowledge sources", "pl-label")
# 3 relevant information back down
path("M522 110 V240 H458")
s.arrow(470, 240, 456, 240)
badge(546, 196, 3)
s.both(566, 202, "ข้อมูลที่เกี่ยวข้อง", "Relevant information", "pl-label")
s.text(566, 226, "fact 7, fact 2", "pl-note")
# the LLM
s.box(690, 400, 190, 110, "nt-band-a", 14)
s.out.append('<circle cx="760" cy="424" r="6" class="pl-line"/><circle cx="760" cy="456" r="6" class="pl-line"/>'
             '<circle cx="790" cy="440" r="6" class="pl-line"/><circle cx="818" cy="440" r="6" class="pl-line"/>'
             '<path d="M765 427 L785 437 M765 453 L785 443 M796 440 H812" class="pl-line"/>')
s.text(785, 494, "LLM (Gemini)", "pl-label", "middle")
# 4 prompt + question + context to the LLM
path("M372 342 V480 H676")
s.arrow(660, 480, 688, 480)
badge(150, 426, 4)
s.both(170, 432, "Prompt + คำถาม", "Prompt + question", "pl-label")
s.both(170, 456, "+ context (fact 7, fact 2)", "+ context (fact 7, fact 2)", "pl-note")
# 5 the generated answer back
path("M688 424 H440 V346")
s.arrow(440, 360, 440, 344)
badge(470, 366, 5)
s.both(490, 372, "คำตอบที่สร้างขึ้น", "Generated answer", "pl-label")
s.text(490, 396, "30 November 2026 [fact 7]", "pl-note")
s.save("l12-rag-app.svg", 520)

# ---------------------------------------------------------------- 17. why chunk? one long page vs small pieces (the Odyssey, BOOK IX)
# Real (all-MiniLM-L6-v2, LangChain RecursiveCharacterTextSplitter 800/100, Butler's Odyssey from Gutenberg):
# BOOK IX is 29,509 characters (about 15 pages); a small model reads its first 256 tokens = the first 1,036 characters.
# The Cyclops eats Ulysses' men halfway through (50%). Searching books read that way picks BOOK II.
# "Reads it all" (the average of BOOK IX's 55 chunk vectors): BOOK IX 0.52, barely ahead of BOOK XXIV 0.49;
# the Cyclops chunk alone scores 0.62. Whole poem = about 330 pages; the top 4 chunks = about 1 page.
W = 1180
s = Svg(W, "Why chunk? Question: What did the Cyclops eat? Without chunking there are two problems. A small embedding model reads only "
           "the first 1,000 characters of BOOK IX, so the Cyclops scene halfway down is never read and search picks the wrong book. "
           "A big model can read all of it, but 55 scenes blur into one vector, so the match is weak, and the LLM then gets 15 pages "
           "for one scene. With chunking, BOOK IX becomes 55 small pieces, each read in full, and the Cyclops piece matches; "
           "the prompt gets about 1 page instead of a 330-page book.")
s.box(W / 2 - 200, 8, 400, 46, "nt-bubble", 23)
s.text(W / 2, 38, "What did the Cyclops eat?", "pl-text", "middle")
TOP, PH = 160, 270


def page(x, shade=None, read_top=False):
    s.box(x, TOP, 120, PH, "ml-cell", 6)
    if shade:
        s.box(x, TOP, 120, PH, shade, 6)
    for y in range(TOP + 16, TOP + PH - 6, 11):
        s.box(x + 10, y, 100, 4, "ml-bar", 2)
    if read_top:
        s.box(x, TOP, 120, 10, "ml-bar-top", 4)
    yc = TOP + PH * 0.50
    s.box(x + 3, yc - 8, 114, 16, "sw-chip-warn", 4)
    return yc


# ---- without chunking: two ways it fails
s.box(20, 70, 680, 420, "sw-warn-box", 14)
s.both(40, 102, "✗ ไม่ตัด: ทั้ง BOOK IX เป็นชิ้นเดียว", "✗ Without chunking: BOOK IX is one piece", "pl-label")
# A: a small model reads only the start
s.both(40, 140, "โมเดลเล็ก", "A small model", "pl-label")
yc = page(40, read_top=True)
s.arrow(186, TOP + 5, 164, TOP + 5)
s.both(192, TOP + 10, "อ่านแค่", "reads only the", "ml-neg")
s.both(192, TOP + 32, "1,000 ตัวอักษร", "first 1,000", "ml-neg")
s.both(192, TOP + 54, "แรก", "characters", "ml-neg")
s.both(192, TOP + 76, "(จาก 29,509)", "(of 29,509)", "pl-note")
s.arrow(186, yc, 164, yc)
s.both(192, yc + 5, "เรื่อง Cyclops:", "the Cyclops scene:", "pl-text")
s.both(192, yc + 27, "ไม่เคยถูกอ่าน", "never read", "ml-neg")
s.both(40, 462, "✗ ได้ BOOK II ผิดบท (0.50)", "✗ wrong book: BOOK II (0.50)", "ml-neg")
# B: a big model reads it all, but the vector is a blur
s.both(370, 140, "โมเดลใหญ่ (ถึง 1 ล้าน token)", "A big model (up to 1M tokens)", "pl-label")
yc = page(370, shade="rc-res")
s.arrow(516, TOP + 40, 494, TOP + 40)
s.both(522, TOP + 45, "อ่านครบ แต่", "reads it all, but", "pl-text")
s.both(522, TOP + 67, "55 ฉากถูกบีบ", "55 scenes blur", "pl-text")
s.both(522, TOP + 89, "เป็น vector เดียว", "into one vector", "pl-text")
s.arrow(516, yc, 494, yc)
s.both(522, yc + 5, "Cyclops เป็นแค่", "the Cyclops is", "pl-text")
s.both(522, yc + 27, "1 ใน 55 ฉาก", "1 scene of 55", "ml-neg")
s.both(370, 462, "✗ 0.52 vs 0.49 + 15 หน้า", "✗ 0.52 vs 0.49, and 15 pages", "ml-neg")
# ---- with chunking: 55 small pieces
s.box(720, 70, 440, 420, "nt-band-a", 14)
s.both(740, 102, "✓ ตัดเป็น chunk: 55 ชิ้นเล็ก", "✓ With chunking: 55 small pieces", "pl-label")
cols, rows = 5, 11
cw, ch = 30, PH / rows - 4
hit = 47  # 85% through BOOK IX
for k in range(cols * rows):
    r, c = divmod(k, cols)
    x, y = 740 + c * (cw + 4), TOP + r * (ch + 4)
    s.box(x, y, cw, ch, "ml-bar-top" if k == hit else "ml-cell", 3)
hy = TOP + (hit // cols) * (ch + 4) + ch / 2
s.both(926, TOP + 10, "แต่ละชิ้นอ่านครบ", "each piece is read", "ml-ok")
s.both(926, TOP + 32, "ชิ้นละ 1 ฉาก", "in full: one scene", "ml-ok")
s.arrow(920, hy, 910, hy)
s.text(926, hy - 18, "“…eating up his", "dg-code")
s.text(926, hy + 2, "comrades…”", "dg-code")
s.both(926, hy + 28, "ตรงกับคำถาม ✓", "matches ✓", "ml-ok")
s.both(740, 462, "✓ ชิ้น Cyclops (0.62), ½ หน้า", "✓ the Cyclops piece (0.62), ½ page", "ml-ok")
# ---- the prompt
y0 = 516
s.both(20, y0, "แล้วส่งอะไรเข้า prompt", "And what goes into the prompt?", "pl-label")
for k in range(4):
    s.box(40 + k * 6, y0 + 32 - k * 6, 40, 52, "ml-cell", 3)
s.both(110, y0 + 48, "ทั้งเล่ม ≈ 330 หน้า ✗", "the whole book ≈ 330 pages ✗", "ml-neg")
s.both(110, y0 + 72, "ต่อให้โมเดลรับได้ 1 ล้าน token ก็ช้า แพง และหาข้อมูลกลางเล่มพลาด",
       "even if a 1M-token model takes it: slow, costly, and facts in the middle get missed", "pl-note")
s.box(900, y0 + 24, 40, 52, "rc-res", 3)
s.both(956, y0 + 56, "4 ชิ้น ≈ 1 หน้า ✓", "4 pieces ≈ 1 page ✓", "ml-ok")
s.save("l12-why-chunk.svg", y0 + 96)

# ---------------------------------------------------------------- 18. five chunking strategies on one small document
# Real cuts: fixed = text[i:i+45]; recursive = RecursiveCharacterTextSplitter(70, 0); structure = MarkdownHeaderTextSplitter("##");
# semantic = all-MiniLM-L6-v2 similarity of neighbouring sentences 0.59, 0.35, 0.32, new chunk below 0.5.
# The LLM-based chunks are an example of what an LLM might write, and the figure says so.
DOC = "## Exams\nMidterm: Monday 21 September.\nFinal: Monday 30 November.\n\n## Classes\n19 October: dense retrieval and RAG.\n26 October: workflows and LLM agents."
PANELS = [
    ("เอกสารต้นฉบับ (152 ตัวอักษร)", "The document (152 characters)", [("", DOC)], [("หน้าเว็บวิชาแบบย่อ", "a short course page", "pl-note"), ("มี 2 หัวข้อ: Exams, Classes", "with 2 headings: Exams, Classes", "pl-note")]),
    ("1 Fixed-size: ทุก 45 ตัวอักษร", "1 Fixed-size: every 45 characters", [("", DOC[i:i + 45]) for i in range(0, len(DOC), 45)],
     [("✗ ตัดกลางคำ", "✗ cuts through words:", "ml-neg"), ("workflow | s", "workflow | s", "ml-neg")]),
    ("2 Recursive: ไม่เกิน 70 ตัวอักษร", "2 Recursive: up to 70 characters",
     [("", "## Exams\nMidterm: Monday 21 September.\nFinal: Monday 30 November."), ("", "## Classes\n19 October: dense retrieval and RAG."), ("", "26 October: workflows and LLM agents.")],
     [("✓ ตัดที่บรรทัดว่างก่อน", "✓ cuts at blank lines first,", "ml-ok"), ("แล้วค่อยตัดที่ขึ้นบรรทัด", "then at line breaks", "ml-ok")]),
    ("3 Document structure: ตามหัวข้อ", "3 Document structure: by heading",
     [("section: Exams", "Midterm: Monday 21 September.\nFinal: Monday 30 November."), ("section: Classes", "19 October: dense retrieval and RAG.\n26 October: workflows and LLM agents.")],
     [("✓ 1 chunk ต่อ 1 หัวข้อ", "✓ one chunk per heading,", "ml-ok"), ("เก็บหัวข้อไว้เป็น metadata", "the heading kept as metadata", "ml-ok")]),
    ("4 Semantic: ตามความหมาย", "4 Semantic: by meaning",
     [("", "Midterm: Monday 21 September.\nFinal: Monday 30 November."), ("", "19 October: dense retrieval and RAG."), ("", "26 October: workflows and LLM agents.")],
     [("✓ รวมประโยคที่ติดกันเมื่อ cosine ≥ 0.5", "✓ joins neighbours while cosine ≥ 0.5", "ml-ok"), ("0.59 รวม · 0.35, 0.32 แยก", "0.59 joins · 0.35, 0.32 split", "ml-ok")]),
    ("5 LLM-based: ให้ LLM เขียน chunk", "5 LLM-based: an LLM writes the chunks",
     [("", "The 2190519 midterm was on 21 Sep 2026."), ("", "The 2190519 final is on 30 Nov 2026."), ("", "On 19 Oct 2026, 2190519 covers RAG."), ("", "On 26 Oct 2026, 2190519 covers agents.")],
     [("✓ chunk อ่านรู้เรื่องในตัว (ตัวอย่าง)", "✓ chunks stand alone (example)", "ml-ok"), ("✗ ช้า เรียก LLM ทุกชิ้น", "✗ slow: one LLM call per piece", "ml-neg")]),
]


def strategy_figure(name, panels, title):
    W = 1180
    s = Svg(W, title)
    PW, LH = 376, 19
    heights = []
    for _, _, chunks, *_ in panels:
        h = sum((1 if m else 0) * 22 + len(t.split("\n")) * LH + 14 for m, t in chunks) + 8 * (len(chunks) - 1)
        heights.append(h)
    PH = max(heights) + 130
    for k, (th, en, chunks, notes) in enumerate(panels):
        x = 20 + k * (PW + 16)
        s.box(x, 10, PW, PH, "ml-cell", 14)
        s.both(x + 16, 40, th, en, "pl-label")
        y = 58
        for j, (meta, t) in enumerate(chunks):
            lines = t.split("\n")
            h = (22 if meta else 0) + len(lines) * LH + 14
            s.box(x + 14, y, PW - 28, h, "pl-chip" if j % 2 == 0 else "nt-band-b", 8)
            yy = y + 8
            if meta:
                s.text(x + 24, yy + 15, meta, "pl-note")
                yy += 22
            for ln in lines:
                s.out.append(f'<text x="{x + 24}" y="{yy + 14}" class="dg-code" xml:space="preserve">{escape(ln)}</text>')
                yy += LH
            y += h + 8
        for j, (nth, nen, ncls) in enumerate(notes):
            s.both(x + 16, 10 + PH - 48 + 27 * j, nth, nen, ncls)
    s.save(name, PH + 20)
    return PH


strategy_figure("l12-chunk-strategies-a.svg", PANELS[:3],
                "The same course page cut two ways. Fixed-size, every 45 characters, cuts through words (workflow | s). "
                "Recursive, up to 70 characters, cuts at blank lines first, then at line breaks.")
strategy_figure("l12-chunk-strategies-b.svg", PANELS[3:],
                "Document structure: one chunk per heading (Exams, Classes), kept as metadata. Semantic: sentences join while their cosine "
                "similarity stays at or above 0.5 (0.59, then 0.35 and 0.32 start new chunks). LLM-based: an LLM rewrites the page into chunks "
                "that each make sense alone (example), but it is slow and costs LLM calls.")

# ---------------------------------------------------------------- 19. multimodal RAG with a multi-vector retriever (slides 81-83)
# A course syllabus PDF -> extract text, table, image -> an LLM writes a summary of each (examples) ->
# summaries in the vector store (searched), raw parts in the doc store (returned), linked by id.
W = 1180
s = Svg(W, "Multimodal RAG with a multi-vector retriever. A real-world document, our course syllabus PDF, holds text, a schedule table and a diagram. "
           "Extract the three parts; an LLM writes a short text summary of each. The summaries go into the vector store for searching; "
           "the raw parts go into a doc store, linked by id. The question When is the final exam? matches the schedule summary, "
           "and the retriever returns the raw table to the LLM.")
LN = 'class="pl-line"'
# 1 the document
s.both(30, 34, "เอกสารจริง (PDF)", "A real document (PDF)", "pl-label")
s.box(30, 50, 200, 300, "ml-cell", 10)
s.text(130, 76, "2190519 syllabus", "pl-note", "middle")
for yy in (92, 106, 120, 134):
    s.out.append(f'<path d="M44 {yy} H{216 if yy != 134 else 170}" {LN} stroke-width="3"/>')
s.out.append(f'<rect x="44" y="152" width="80" height="62" rx="4" {LN}/><circle cx="62" cy="168" r="6" {LN}/><path d="M48 208 L76 182 L94 198 L104 190 L120 208" {LN}/>')
for yy in (160, 174, 188, 202):
    s.out.append(f'<path d="M136 {yy} H216" {LN} stroke-width="3"/>')
s.out.append(f'<rect x="44" y="232" width="172" height="102" rx="2" {LN}/>')
for xx in (101, 158):
    s.out.append(f'<path d="M{xx} 232 V334" {LN}/>')
for yy in (258, 283, 308):
    s.out.append(f'<path d="M44 {yy} H216" {LN}/>')
# 2 extract
s.arrow(236, 200, 292, 200)
s.both(264, 186, "แยกส่วน", "Extract", "pl-note", "middle")
items = [(80, "text", "ข้อความ", "Text"), (200, "table", "ตาราง", "Table"), (320, "image", "รูป", "Image")]
for y, kind, th, en in items:
    s.box(300, y - 36, 150, 72, "nt-bubble", 10)
    if kind == "text":
        for k in range(3):
            s.out.append(f'<path d="M314 {y - 16 + 12 * k} H{360 if k == 2 else 376}" {LN} stroke-width="3"/>')
    elif kind == "table":
        s.out.append(f'<rect x="314" y="{y - 20}" width="62" height="40" rx="2" {LN}/><path d="M335 {y - 20} V{y + 20} M355 {y - 20} V{y + 20} M314 {y - 7} H376 M314 {y + 7} H376" {LN}/>')
    else:
        s.out.append(f'<rect x="314" y="{y - 20}" width="62" height="40" rx="3" {LN}/><circle cx="328" cy="{y - 8}" r="5" {LN}/><path d="M316 {y + 18} L338 {y - 2} L352 {y + 10} L360 {y + 4} L374 {y + 18}" {LN}/>')
    s.both(390, y + 6, th, en, "pl-label")
# 3 summarise with an LLM
s.arrow(456, 200, 520, 200)
s.out.append(f'<circle cx="474" cy="160" r="5" {LN}/><circle cx="474" cy="180" r="5" {LN}/><circle cx="494" cy="170" r="5" {LN}/><path d="M478 162 L490 168 M478 178 L490 172" {LN}/>')
s.both(488, 140, "LLM สรุป", "LLM", "pl-note", "middle")
summaries = [(80, "Summary 1", "class: Mondays, EN100 room 501"), (200, "Summary 2", "schedule: lessons and exam dates"), (320, "Summary 3", "diagram of the RAG pipeline")]
for y, tag, txt in summaries:
    s.box(528, y - 30, 286, 60, "pl-chip", 10)
    s.text(542, y - 6, tag, "pl-label")
    s.text(542, y + 18, txt, "pl-note")
# 4 the multi-vector retriever
s.arrow(820, 200, 846, 200)
s.box(852, 20, 316, 360, "nt-band-a", 18)
s.both(1010, 46, "Multi-vector retriever", "Multi-vector retriever", "pl-label", "middle")
for cx, th, en in ((930, "Vector store", "Vector store"), (1090, "Doc store", "Doc store")):
    s.out.append(f'<ellipse cx="{cx}" cy="76" rx="66" ry="12" {LN}/><path d="M{cx - 66} 76 V350 C{cx - 66} 366 {cx + 66} 366 {cx + 66} 350 V76" {LN}/>')
    s.both(cx, 104, th, en, "pl-note", "middle")
    s.both(cx, 124, "ใช้ค้น" if cx < 1000 else "ส่งให้ LLM", "searched" if cx < 1000 else "returned", "pl-note", "middle")
for k, (y, raw) in enumerate([(170, "raw text"), (240, "raw table"), (310, "raw image")]):
    s.box(878, y - 20, 104, 40, "pl-chip", 8)
    s.text(930, y + 6, f"Summary {k + 1}", "pl-note", "middle")
    s.box(1038, y - 20, 104, 40, "sw-chip-warn" if k == 1 else "ml-cell", 8)
    s.text(1090, y + 6, raw, "pl-note", "middle")
    s.out.append(f'<path d="M984 {y} H1036" {LN} stroke-dasharray="4 4"/>')
s.both(1010, 146, "id เดียวกัน", "same id", "pl-note", "middle")
# in / out
s.arrow(930, 452, 930, 386)
s.box(820, 456, 220, 40, "nt-bubble", 20)
s.text(930, 482, "When is the final exam?", "pl-note", "middle")
s.both(812, 482, "เข้า: คำถาม", "In: question", "pl-label", "end")
s.arrow(1090, 386, 1090, 452)
s.both(1168, 522, "ออก: ตารางตัวจริง → LLM", "Out: the raw table → LLM", "ml-ok", "end")
s.both(30, 410, "คำถามตรงกับ Summary 2 แต่สิ่งที่ส่งให้ LLM คือตารางตัวเต็ม จึงไม่มีข้อมูลหาย", "The question matches Summary 2, but the LLM gets the full table, so nothing is lost", "pl-label")
s.both(30, 440, "สรุปในรูปเป็นตัวอย่างที่ LLM อาจเขียน", "The summaries are examples of what an LLM might write", "pl-note")
s.save("l12-multimodal.svg", 536)

# ---------------------------------------------------------------- 20. how recursive chunking works (chunk_size 70, the same course page)
# Real lengths: page 152; blank-line cut -> 65 and 85; line-break cut of the 85 -> 10, 36, 37; small neighbours joined
# while the result stays <= 70 -> 47 and 37. LangChain RecursiveCharacterTextSplitter(70, 0) gives exactly these 3 chunks.
W = 1180
s = Svg(W, "How recursive chunking works, with a limit of 70 characters. The 152-character page is too long, so it is cut at the blank line: "
           "Exams (65, fits) and Classes (85, too long). Only the Classes piece is cut again, at line breaks: 10, 36 and 37 characters. "
           "Small neighbours are joined back while they stay within 70: 47 and 37. The result is 3 chunks: 65, 47 and 37 characters.")
# the separator ladder
s.box(20, 20, 250, 300, "nt-band-b", 14)
s.both(36, 52, "ลองตัดที่ไหนก่อน", "Where to cut, in order", "pl-label")
for k, (sep, th, en, used) in enumerate([("\\n\\n", "บรรทัดว่าง", "blank line", True), ("\\n", "ขึ้นบรรทัด", "line break", True),
                                         ("\" \"", "ช่องว่าง", "space", False), ("\"\"", "ตัวอักษรไหนก็ได้", "any character", False)]):
    y = 92 + k * 52
    s.box(36, y - 22, 218, 38, "pl-chip" if used else "ml-cell", 8)
    s.text(50, y + 3, f"{k + 1}", "pl-label")
    s.text(74, y + 3, sep, "dg-code")
    s.both(126, y + 3, th, en, "pl-note")
s.both(36, 282, "ใช้แบบถัดไป", "the next one only for", "pl-note")
s.both(36, 306, "เฉพาะชิ้นที่ยังยาวเกิน", "pieces still too long", "pl-note")


def piece(x, y, w, label, n, ok):
    s.box(x, y, w, 44, "pl-chip" if ok else "sw-chip-warn", 8)
    s.text(x + 10, y + 28, label, "dg-code")
    s.text(x + w - 10, y + 28, f"{n} {'✓' if ok else '✗'}", "ml-ok" if ok else "ml-neg", "end")


X0 = 300
# step 0
piece(X0, 20, 860, "## Exams … Final … ## Classes … 26 October …", 152, False)
s.both(X0, 88, "ยาวเกิน 70 → ตัดที่บรรทัดว่าง (1)", "longer than 70 → cut at the blank line (1)", "ml-neg")
s.arrow(500, 96, 500, 118)
s.arrow(960, 96, 960, 118)
# step 1
piece(X0, 120, 400, "## Exams · Midterm · Final", 65, True)
piece(760, 120, 400, "## Classes · 19 Oct · 26 Oct", 85, False)
s.both(X0, 188, "พอดีแล้ว เก็บไว้", "fits: keep it", "ml-ok")
s.both(760, 188, "ยังยาว → ตัดชิ้นนี้ที่ขึ้นบรรทัด (2)", "too long → cut it at line breaks (2)", "ml-neg")
s.arrow(960, 196, 960, 218)
# step 2
piece(760, 220, 150, "## Classes", 10, True)
piece(914, 220, 122, "19 Oct", 36, True)
piece(1040, 220, 122, "26 Oct", 37, True)
s.both(760, 288, "รวมชิ้นเล็กที่ติดกันกลับ ตราบที่ไม่เกิน 70", "join small neighbours back while ≤ 70", "pl-note")
# result
s.both(X0, 340, "ผลลัพธ์: 3 chunk", "Result: 3 chunks", "pl-label")
piece(X0, 356, 400, "## Exams · Midterm · Final", 65, True)
piece(760, 356, 250, "## Classes · 19 Oct", 47, True)
piece(1016, 356, 144, "26 Oct…", 37, True)
s.both(20, 432, "\"Recursive\" = ทำขั้นเดิมซ้ำกับชิ้นที่ยังยาวเกิน ด้วยจุดตัดที่เล็กลง จนทุกชิ้นพอดี",
       "\"Recursive\" = repeat the same step on any piece that is still too long, with a smaller cut, until every piece fits", "pl-label")
s.save("l12-recursive.svg", 448)


# ================================================================ redrawn in the l12-why-chunk style (2026-10-18):
# drawn objects, arrows at the exact spot, a one-line result per panel, few numbers.
import math as _m


def magnifier(s, cx, cy, r):
    s.out.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" class="pl-line" stroke-width="4"/>')
    s.out.append(f'<path d="M{cx + r * .7:g} {cy + r * .7:g} L{cx + r * 1.5:g} {cy + r * 1.5:g}" class="pl-line" stroke-width="6"/>')


# ---------------------------------------------------------------- 6. retrieval as a meaning map
# Distance from the question = 1 - cosine (all-MiniLM-L6-v2, "When is the final exam?"):
# fact 7 0.89, fact 2 0.68, fact 5 0.42, fact 4 0.41, fact 3 0.34, fact 1 0.27, fact 6 0.23. Angles are only for layout.
W = 1180
s = Svg(W, "Retrieval as a meaning map: the question sits in the middle and each course fact is a dot; the closer the dot, the closer "
           "the meaning. The final exam fact (0.89) and the midterm fact (0.68) are the two closest, so with top-k = 2 they go to the LLM.")
s.box(W / 2 - 200, 8, 400, 46, "nt-bubble", 23)
s.text(W / 2, 38, "When is the final exam?", "pl-text", "middle")
cx, cy, K = 320, 310, 270
for r in (70, 140, 210):
    s.out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="dg-rule" fill="none"/>')
s.out.append(f'<circle cx="{cx}" cy="{cy}" r="104" class="pl-line" stroke-width="2.5" stroke-dasharray="8 6" fill="none"/>')
s.both(cx, cy - 112, "top-k = 2", "top-k = 2", "pl-label", "middle")
s.out.append(f'<circle cx="{cx}" cy="{cy}" r="11" class="pl-dot"/>')
s.text(cx, cy + 5, "?", "pl-num", "middle")
FACTS = [  # (fact, cosine, angle in degrees, en label, th label, label on the left?)
    (7, 0.89, 40, "final exam", "สอบปลายภาค", False),
    (2, 0.68, 165, "midterm", "สอบกลางภาค", True),
    (5, 0.42, 25, "26 Oct: agents", "26 ต.ค.: agent", False),
    (4, 0.41, -30, "19 Oct: RAG", "19 ต.ค.: RAG", False),
    (3, 0.34, 120, "no class 12 Oct", "งดเรียน 12 ต.ค.", False),
    (1, 0.27, 215, "room 501", "ห้อง 501", True),
    (6, 0.23, -105, "2 Nov: NER", "2 พ.ย.: NER", False),
]
for n, cos, ang, en, th, left in FACTS:
    r = (1 - cos) * K
    x, y = cx + r * _m.cos(_m.radians(ang)), cy - r * _m.sin(_m.radians(ang))
    top = n in (7, 2)
    s.out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" class="{"ml-bar-top" if top else "ml-bar"}"/>')
    k0 = len(s.out)
    s.both(x - 14 if left else x + 14, y + 6, f"{th} {cos:.2f}", f"{en} {cos:.2f}", "ml-ok" if top else "pl-note", "end" if left else "start")
    halo = ' style="paint-order: stroke; stroke: var(--card); stroke-width: 6px; stroke-linejoin: round"'
    s.out[k0:] = [t.replace("<text ", "<text" + halo + " ", 1) for t in s.out[k0:]]
s.both(20, 590, "ยิ่งใกล้จุดกลาง ความหมายยิ่งใกล้คำถาม", "The closer to the middle, the closer the meaning", "pl-note")
# right: what goes on
s.box(660, 80, 500, 470, "nt-band-a", 14)
s.both(680, 114, "ใกล้ที่สุด 2 ข้อไปที่ LLM", "The 2 closest facts go to the LLM", "pl-label")
s.both(680, 146, "แต่ละจุด = ข้อเท็จจริง 1 ข้อ", "each dot = one course fact", "pl-note")
s.both(680, 172, "ระยะห่าง = 1 − cosine", "distance = 1 − cosine", "pl-note")
s.text(680, 204, "cos(q, d) = q·d / (‖q‖ ‖d‖)", "pl-label")
for k, (lab_en, lab_th, sc) in enumerate([("fact 7 · final exam: 30 Nov", "fact 7 · สอบปลายภาค 30 พ.ย.", "0.89"),
                                          ("fact 2 · midterm: 21 Sep", "fact 2 · สอบกลางภาค 21 ก.ย.", "0.68")]):
    y = 226 + k * 58
    s.box(680, y, 460, 46, "pl-chip", 10)
    s.both(696, y + 30, lab_th, lab_en, "pl-text")
    s.text(1124, y + 30, sc, "pl-label", "end")
s.arrow(910, 338, 910, 372)
s.box(840, 376, 140, 50, "nt-out", 12)
s.text(910, 408, "LLM", "pl-label", "middle")
s.both(680, 470, "LLM เลือก fact 7 เพราะกติกา", "the LLM picks fact 7, because the rule", "ml-ok")
s.both(680, 496, "\"ตอบจาก context เท่านั้น\"", "says \"answer only from the context\"", "ml-ok")
s.both(680, 530, "คะแนนจริงจาก all-MiniLM-L6-v2 (1 = ความหมายเดียวกัน)", "real scores, all-MiniLM-L6-v2 (1 = same meaning)", "pl-note")
s.save("l12-retrieve.svg", 606)

# ---------------------------------------------------------------- 7. two-stage retrieval: a careful reader on everything vs fast, then careful
W = 1180
s = Svg(W, "Two-stage retrieval. Without it, a careful reranker would read every one of 100,000 chunks with the question: far too slow. "
           "With it, a fast search keeps 50 chunks, the careful reranker reads only those 50, and the best 5 go to the LLM.")
s.box(W / 2 - 220, 8, 440, 46, "nt-bubble", 23)
s.both(W / 2, 38, "1 คำถาม · 100,000 chunk", "One question · 100,000 chunks", "pl-text", "middle")
# left: careful reader on everything
s.box(20, 70, 560, 400, "sw-warn-box", 14)
s.both(40, 102, "✗ ให้ตัวอ่านละเอียดอ่านทุก chunk", "✗ The careful reader reads every chunk", "pl-label")
for r in range(14):
    for c in range(22):
        s.box(44 + c * 13, 130 + r * 13, 9, 9, "ml-cell", 2)
magnifier(s, 186, 214, 44)
s.both(350, 160, "อ่านทุก chunk", "reads every chunk", "pl-text")
s.both(350, 184, "คู่กับคำถาม", "together with", "pl-text")
s.both(350, 208, "", "the question", "pl-text")
s.both(350, 262, "100,000 คู่ × 1 ms", "100,000 pairs × 1 ms", "ml-neg")
s.both(350, 286, "≈ 100 วินาที", "≈ 100 seconds", "ml-neg")
s.both(350, 310, "ต่อ 1 คำถาม", "per question", "ml-neg")
s.both(40, 452, "✗ รอคำตอบเกือบ 2 นาที", "✗ almost 2 minutes per answer", "ml-neg")
# right: fast, then careful
s.box(600, 70, 560, 400, "nt-band-a", 14)
s.both(620, 102, "✓ ค้นเร็วก่อน แล้วค่อยอ่านละเอียด", "✓ Fast first, then careful", "pl-label")
for r in range(5):
    for c in range(18):
        s.box(630 + c * 9, 128 + r * 9, 6, 6, "ml-cell", 1)
s.both(810, 150, "100,000 chunk", "100,000 chunks", "pl-note")
s.arrow(700, 178, 700, 210)
s.both(716, 200, "ค้นเร็ว (BM25 / vector) เก็บ 50", "fast search (BM25 / vectors) keeps 50", "pl-text")
for r in range(5):
    for c in range(10):
        s.box(636 + c * 13, 220 + r * 13, 10, 10, "pl-chip", 2)
magnifier(s, 700, 252, 22)
s.both(810, 246, "ตัวอ่านละเอียด (reranker)", "the careful reranker", "pl-text")
s.both(810, 270, "อ่านแค่ 50 ชิ้นนี้", "reads only these 50", "ml-ok")
s.arrow(700, 290, 700, 322)
s.both(716, 312, "เก็บ 5 ชิ้นที่ดีที่สุด", "keeps the best 5", "pl-text")
for k in range(5):
    s.box(640 + k * 30, 334, 22, 30, "ml-bar-top", 3)
s.arrow(796, 349, 830, 349)
s.box(836, 326, 100, 46, "nt-out", 12)
s.text(886, 356, "LLM", "pl-label", "middle")
s.both(620, 452, "✓ ค้น ≈ 0.01 วิ + อ่าน 50 คู่ ≈ 0.05 วิ", "✓ search ≈ 0.01 s + 50 pairs ≈ 0.05 s", "ml-ok")
s.both(20, 500, "จับเวลาจริง: reranker ms-marco-MiniLM-L6-v2 บน CPU ของ laptop ≈ 1 ms ต่อคู่ · 50 และ 5 เป็นค่าที่ใช้บ่อย ปรับได้",
       "timed: the ms-marco-MiniLM-L6-v2 reranker on a laptop CPU ≈ 1 ms per pair · 50 and 5 are common settings, not rules", "pl-note")
s.save("l12-two-stage.svg", 514)

# ---------------------------------------------------------------- 8. bi-encoder vs cross-encoder: alone vs together
# Example pair (lesson 12): "What is taught on 19 October?" and fact 4 "On 19 October 2026 the class covers dense retrieval and RAG."
W = 1180
s = Svg(W, "Bi-encoder versus cross-encoder. A bi-encoder turns the question and the document into an arrow each, separately, and compares "
           "their directions: fast, because document arrows are made once in advance, but it never reads the two texts together. "
           "A cross-encoder reads the question and the document together and sees that 19 October appears in both: more precise, "
           "but it must re-read every pair. Search with the fast one; rerank the short list with the precise one.")
# left: bi-encoder
s.box(20, 20, 560, 430, "nt-band-a", 14)
s.both(40, 52, "Bi-encoder: อ่านทีละข้อความ", "Bi-encoder: reads each text alone", "pl-label")
s.both(40, 80, "แต่ละข้อความกลายเป็นลูกศร (vector) ของตัวเอง", "each text becomes its own arrow (a vector)", "pl-note")
ox, oy = 110, 330
s.out.append(f'<circle cx="{ox}" cy="{oy}" r="5" class="pl-dot"/>')
for (tx, ty, en, th) in ((370, 160, "question", "คำถาม"), (410, 236, "document", "เอกสาร")):
    s.arrow(ox, oy, tx, ty)
    s.both(tx + 10, ty + 6, th, en, "pl-text")
a1, a2 = _m.atan2(oy - 160, 370 - ox), _m.atan2(oy - 236, 410 - ox)
R = 90
p1 = (ox + R * _m.cos(a1), oy - R * _m.sin(a1)); p2 = (ox + R * _m.cos(a2), oy - R * _m.sin(a2))
s.out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} A{R} {R} 0 0 1 {p2[0]:.1f} {p2[1]:.1f}" class="pl-line" stroke-dasharray="4 4" fill="none"/>')
s.both(216, 300, "มุมเล็ก = ความหมายใกล้", "small angle = close meaning", "pl-note")
s.text(40, 116, "s(q, d) = cos(E(q), E(d)) = 0.35", "pl-label")
s.both(40, 380, "✓ เร็ว: ลูกศรของเอกสารทำไว้ก่อนได้", "✓ fast: document arrows are made in advance", "ml-ok")
s.both(40, 406, "✗ ไม่เคยอ่านสองข้อความพร้อมกัน", "✗ never reads the two texts together", "ml-neg")
s.both(40, 436, "→ ใช้ค้นใน chunk ทั้งหมด", "→ used to search all the chunks", "pl-label")
# right: cross-encoder
s.box(600, 20, 560, 430, "nt-band-b", 14)
s.both(620, 52, "Cross-encoder: อ่านสองข้อความพร้อมกัน", "Cross-encoder: reads both together", "pl-label")
s.box(620, 80, 520, 150, "ml-cell", 10)
QX, CW = 636, 8.4
s.box(QX + 18 * CW - 3, 104, 10 * CW + 6, 26, "sw-chip-warn", 5)
s.text(QX, 122, "What is taught on 19 October?", "dg-code")
s.box(QX + 3 * CW - 3, 178, 10 * CW + 6, 26, "sw-chip-warn", 5)
s.text(QX, 196, "On 19 October 2026 the class covers dense…", "dg-code")
s.out.append(f'<path d="M{QX + 23 * CW:.1f} 131 C{QX + 23 * CW:.1f} 160 {QX + 8 * CW:.1f} 150 {QX + 8 * CW:.1f} 177" class="pl-line" fill="none"/>')
s.both(QX + 26 * CW, 160, "เห็นว่าคำตรงกัน", "sees the words match", "pl-note")
s.arrow(880, 234, 880, 262)
s.box(700, 268, 360, 22, "ml-cell", 6)
s.box(700, 268, 360 * 0.85, 22, "ml-bar-top", 6)
s.both(880, 314, "ความเกี่ยวข้อง: สูง ✓", "relevance: high ✓", "ml-ok", "middle")
s.text(880, 346, "s(q, d) = f(q, d) = 3.97", "pl-label", "middle")
s.both(620, 380, "✓ แม่นกว่า: เห็นว่าคำไหนตรงกับคำไหน", "✓ more precise: sees which words match", "ml-ok")
s.both(620, 406, "✗ ช้า: ต้องอ่านใหม่ทุกคู่", "✗ slow: must re-read every pair", "ml-neg")
s.both(620, 436, "→ ใช้เรียงใหม่ในรายการสั้น", "→ used to rerank a short list", "pl-label")
s.both(20, 482, "ค้นด้วยตัวที่เร็ว แล้วเรียงรายการสั้นด้วยตัวที่แม่น", "Search with the fast one, then rerank the short list with the precise one", "pl-label")
s.both(20, 510, "คะแนนจริงของ fact 4: all-MiniLM-L6-v2 (cosine, −1 ถึง 1) · ms-marco-MiniLM-L6-v2 (ไม่ใช่ความน่าจะเป็น)",
       "real scores for fact 4: all-MiniLM-L6-v2 (cosine, −1 to 1) · ms-marco-MiniLM-L6-v2 (not a probability)", "pl-note")
s.save("l12-bi-cross.svg", 524)

# ---------------------------------------------------------------- 10. reranking cannot recover a chunk the search missed
W = 1180
s = Svg(W, "Reranking cannot fix a missed chunk. If the right chunk is ranked 120th, below the top-50 cut, the reranker never sees it. "
           "Fix the search first (hybrid search, a rewritten question) so it gets into the top 50; then the reranker moves it to the top.")


def ranked(x0, gold, cut=6, n=14):
    for k in range(n):
        y = 130 + k * 20
        s.box(x0, y, 220, 14, "sw-chip-warn" if k == gold else "ml-cell", 4)
    yl = 130 + cut * 20 - 3
    s.out.append(f'<path d="M{x0 - 10} {yl} H{x0 + 230}" class="pl-line" stroke-dasharray="7 5"/>')
    return yl


s.box(20, 20, 560, 450, "sw-warn-box", 14)
s.both(40, 52, "✗ chunk ที่ถูกอยู่อันดับ 120", "✗ The right chunk is ranked 120th", "pl-label")
s.both(40, 84, "อันดับจากการค้น", "ranked by the search", "pl-note")
yl = ranked(60, gold=12)
s.both(300, yl - 8, "↑ top 50: ส่งให้ reranker", "↑ top 50: kept for the reranker", "pl-note")
s.both(300, yl + 22, "↓ ที่เหลือ: ทิ้ง", "↓ the rest: dropped", "pl-note")
gy = 130 + 12 * 20 + 7
s.arrow(300, gy, 286, gy)
s.both(308, gy + 6, "chunk ที่ถูก: อันดับ 120", "the right chunk: rank 120", "ml-neg")
s.both(308, gy + 30, "reranker ไม่เคยเห็น", "the reranker never sees it", "ml-neg")
s.both(40, 452, "✗ Recall@50 = 0 → rerank ช่วยไม่ได้", "✗ Recall@50 = 0 → reranking can't help", "ml-neg")
s.box(600, 20, 560, 450, "nt-band-a", 14)
s.both(620, 52, "✓ แก้การค้นก่อน", "✓ Fix the search first", "pl-label")
s.both(620, 84, "hybrid search หรือเขียนคำถามใหม่", "hybrid search, or rewrite the question", "pl-note")
yl = ranked(640, gold=4)
s.box(640, 130, 220, 14, "nt-out", 4)
gy = 130 + 4 * 20 + 7
s.out.append(f'<path d="M866 {gy} C900 {gy} 900 137 868 137" class="pl-line" fill="none"/><path d="M876 131 L868 137 L876 143" class="pl-line"/>')
s.both(910, gy + 6, "ติด top 50 แล้ว", "now in the top 50", "ml-ok")
s.both(910, 142, "reranker ย้ายขึ้นบนสุด", "the reranker moves it up", "ml-ok")
s.both(620, 452, "✓ Recall@50 = 1 → rerank: Recall@5 = 1", "✓ Recall@50 = 1 → after reranking, Recall@5 = 1", "ml-ok")
s.save("l12-rerank-limit.svg", 484)

# ---------------------------------------------------------------- 11. context optimisation on the final-exam question
# Filtering: the real top 4 for "When is the final exam?" (fact 7, 2, 5, 4); only fact 7 answers it.
# Compression and parent document use our real facts written as a course-page chunk.
W = 1180
s = Svg(W, "Three ways to give the LLM better context for 'When is the final exam?'. Filtering keeps fact 7 and drops the three chunks "
           "that do not answer. Compression keeps only the sentence about the final exam from a longer chunk. Parent-document retrieval "
           "matches the small chunk 'It is on Monday 30 November.' and sends its whole section, so the LLM knows what 'it' is.")
s.box(W / 2 - 200, 8, 400, 46, "nt-bubble", 23)
s.text(W / 2, 38, "When is the final exam?", "pl-text", "middle")
PX = [20 + k * 392 for k in range(3)]
heads = [("A · Filtering", "ตัด chunk ที่ไม่ช่วยตอบ", "drop chunks that don't help"),
         ("B · Compression", "เก็บเฉพาะประโยคที่ตอบ", "keep only the answering sentence"),
         ("C · Parent document", "ค้นชิ้นเล็ก ส่งทั้งส่วน", "search small, send the section")]
for x, (t, th, en) in zip(PX, heads):
    s.box(x, 70, 376, 380, "ml-cell", 14)
    s.text(x + 16, 102, t, "pl-label")
    s.both(x + 16, 128, th, en, "pl-note")
# A
x = PX[0]
for k, (txt, keep) in enumerate([("fact 7 · final exam: 30 Nov", True), ("fact 2 · midterm: 21 Sep", False),
                                 ("fact 5 · 26 Oct: agents", False), ("fact 4 · 19 Oct: RAG", False)]):
    y = 146 + k * 40
    s.box(x + 16, y, 344, 32, "pl-chip" if keep else "pl-chip-del", 8)
    s.text(x + 30, y + 22, txt, "pl-text" if keep else "pl-del")
s.arrow(x + 188, 310, x + 188, 334)
s.box(x + 16, 338, 344, 32, "pl-chip", 8)
s.text(x + 30, 360, "fact 7 · final exam: 30 Nov", "pl-text")
s.both(x + 16, 432, "✓ 1 chunk แทน 4", "✓ 1 chunk instead of 4", "ml-ok")
# B
x = PX[1]
lines = ["2190519 meets on Mondays in EN100,", "room 501. The midterm was on 21 Sep.", "The final exam is on Monday", "30 November 2026."]
s.box(x + 16, 146, 344, 116, "ml-cell", 8)
s.box(x + 22, 204, 332, 52, "rc-res", 6)
for k, ln in enumerate(lines):
    s.text(x + 30, 172 + k * 26, ln, "dg-code")
s.arrow(x + 188, 270, x + 188, 300)
s.box(x + 16, 306, 344, 64, "pl-chip", 8)
s.text(x + 30, 332, "The final exam is on Monday", "dg-code")
s.text(x + 30, 356, "30 November 2026.", "dg-code")
s.both(x + 16, 432, "✓ 117 → 45 ตัวอักษร", "✓ 117 → 45 characters", "ml-ok")
# C
x = PX[2]
s.box(x + 16, 146, 230, 40, "pl-chip", 8)
s.text(x + 30, 172, "It is on Monday 30 Nov.", "dg-code")
s.both(x + 256, 172, "“it” คือ?", "“it” = ?", "ml-neg")
s.arrow(x + 140, 192, x + 140, 222)
s.box(x + 16, 228, 344, 104, "rc-res", 8)
s.text(x + 30, 254, "## Final exam", "dg-code")
s.text(x + 30, 280, "The final exam of 2190519.", "dg-code")
s.box(x + 24, 290, 210, 26, "pl-chip", 5)
s.text(x + 30, 308, "It is on Monday 30 Nov.", "dg-code")
s.both(x + 16, 432, "✓ LLM รู้ว่า “it” คืออะไร", "✓ the LLM knows what “it” is", "ml-ok")
s.both(20, 482, "เป้าหมาย: หลักฐานที่เกี่ยวข้องและพอ ไม่ใช่ข้อความมากที่สุด", "Goal: enough relevant evidence, not the most text", "pl-label")
s.save("l12-context-opt.svg", 498)

# ---------------------------------------------------------------- 14. why RAG: eight icon tiles
W = 1180


def ico(kind, x, y):
    L = 'class="pl-line" fill="none"'
    d = {
        "calendar": f'<rect x="{x}" y="{y + 4}" width="32" height="28" rx="3" {L}/><path d="M{x} {y + 12} H{x + 32} M{x + 8} {y} V{y + 8} M{x + 24} {y} V{y + 8}" {L}/>',
        "lock": f'<rect x="{x + 2}" y="{y + 14}" width="28" height="20" rx="3" {L}/><path d="M{x + 8} {y + 14} V{y + 8} A8 8 0 0 1 {x + 24} {y + 8} V{y + 14}" {L}/>',
        "rare": f'<path d="M{x + 16} {y} L{x + 20} {y + 11} L{x + 32} {y + 12} L{x + 23} {y + 20} L{x + 26} {y + 32} L{x + 16} {y + 25} L{x + 6} {y + 32} L{x + 9} {y + 20} L{x} {y + 12} L{x + 12} {y + 11} Z" {L}/>',
        "source": f'<path d="M{x + 4} {y} H{x + 22} L{x + 30} {y + 8} V{y + 32} H{x + 4} Z" {L}/><path d="M{x + 10} {y + 20} L{x + 15} {y + 25} L{x + 24} {y + 14}" {L}/>',
        "guess": f'<path d="M{x} {y + 2} H{x + 32} V{y + 24} H{x + 14} L{x + 6} {y + 32} V{y + 24} H{x} Z" {L}/><path d="M{x + 12} {y + 10} A4 4 0 1 1 {x + 17} {y + 14} V{y + 17}" {L}/>',
        "edit": f'<path d="M{x + 4} {y + 28} L{x + 6} {y + 20} L{x + 22} {y + 4} L{x + 28} {y + 10} L{x + 12} {y + 26} Z M{x + 4} {y + 32} H{x + 30}" {L}/>',
        "coin": f'<circle cx="{x + 16}" cy="{y + 16}" r="14" {L}/><path d="M{x + 16} {y + 8} V{y + 24} M{x + 11} {y + 12} H{x + 20} M{x + 12} {y + 20} H{x + 21}" {L}/>',
        "people": f'<circle cx="{x + 10}" cy="{y + 9}" r="5" {L}/><circle cx="{x + 24}" cy="{y + 9}" r="5" {L}/><path d="M{x + 1} {y + 30} Q{x + 10} {y + 14} {x + 19} {y + 30} M{x + 15} {y + 30} Q{x + 24} {y + 14} {x + 33} {y + 30}" {L}/>',
    }
    s.out.append(d[kind])


TILES = [
    ("calendar", "ทันสมัย", "Up to date", "✗ ติดที่วัน cutoff", "✗ stuck at cutoff", "✓ อ่านไฟล์ใหม่ได้", "✓ reads new files"),
    ("lock", "ข้อมูลส่วนตัว", "Private data", "✗ มองไม่เห็น", "✗ can't see it", "✓ อ่านหน้าเว็บเรา", "✓ reads our page"),
    ("rare", "ข้อมูลหายาก", "Rare facts", "✗ เห็นน้อยเกินไป", "✗ seen too rarely", "✓ 1 บรรทัดก็พอ", "✓ 1 line is enough"),
    ("source", "ตรวจสอบได้", "Checkable", "✗ ไม่มีที่มา", "✗ no source", "✓ อ้าง [fact 7]", "✓ cites [fact 7]"),
    ("guess", "แต่งน้อยลง", "Fewer made-up", "✗ เดาวันที่", "✗ guesses a date", "✓ หรือบอกไม่แน่ใจ", "✓ or says not sure"),
    ("edit", "อัปเดตง่าย", "Easy to update", "✗ ต้องเทรนใหม่", "✗ must retrain", "✓ แก้ 1 บรรทัด", "✓ edit one line"),
    ("coin", "ถูกกว่า", "Cheaper", "✗ ต้องโมเดลใหญ่", "✗ needs a big model", "✓ โมเดลเล็กก็พอ", "✓ a small model"),
    ("people", "ปลอดภัยกว่า", "Safer", "✗ ทุกคนได้เท่ากัน", "✗ same for everyone", "✓ แยกสิทธิ์ต่อคน", "✓ per-user access"),
]
s = Svg(W, "Eight reasons to use RAG instead of an LLM alone, as tiles. Fixes the limits of an LLM alone: up to date, private data, rare facts, "
           "checkable answers, fewer made-up answers. Practical reasons: easy to update, cheaper, safer per-user access.")
s.box(W / 2 - 240, 8, 480, 46, "nt-bubble", 23)
s.text(W / 2, 38, "When is the final exam of 2190519?", "pl-text", "middle")
TW, TH = 220, 164
for gk, (gth, gen, rng, y0, band) in enumerate([("แก้ข้อจำกัดของ LLM อย่างเดียว", "Fixes the limits of an LLM alone", range(0, 5), 74, "nt-band-a"),
                                                  ("เหตุผลด้านการใช้งาน", "Practical reasons", range(5, 8), 292, "nt-band-b")]):
    s.both(20, y0 + 22, gth, gen, "pl-label")
    for j, k in enumerate(rng):
        kind, tth, ten, xth, xen, oth, oen = TILES[k]
        x, y = 20 + j * (TW + 10), y0 + 36
        s.box(x, y, TW, TH, band, 12)
        s.out.append(f'<circle cx="{x + TW - 24}" cy="{y + 28}" r="13" class="pl-dot"/>')
        s.text(x + TW - 24, y + 33, str(k + 1), "pl-num", "middle")
        ico(kind, x + 14, y + 12)
        s.both(x + 14, y + 74, tth, ten, "pl-label")
        s.both(x + 14, y + 112, xth, xen, "ml-neg")
        s.both(x + 14, y + 142, oth, oen, "ml-ok")
s.save("l12-why-rag.svg", 506)

# ---------------------------------------------------------------- 21. exact search vs ANN (HNSW): why a vector database is fast
# Measured in a scratch venv, one question at a time, 300 questions: numpy exact search vs hnswlib (M=16, ef=100).
# 43,900 real sentences from 8 public-domain books, embedded with all-MiniLM-L6-v2; 200,000 and 1,000,000 = those real
# vectors repeated with a little noise. Exact 3.6 / 8.8 / 42.9 ms; HNSW 0.69 / 0.75 / 0.78 ms; true nearest found
# 98.3% on the real 43,900 (97.3% at 200k).
ANN_N = "1,000,000"
ANN_EXACT_MS = "43"
ANN_HNSW_MS = "0.8"
ANN_SPEEDUP = "55"
ANN_RECALL = "98"
W = 1180
s = Svg(W, f"Exact search versus approximate nearest neighbour search with HNSW, over {ANN_N} vectors. Exact search compares the question "
           f"with every vector: {ANN_EXACT_MS} ms per question. HNSW walks a layered graph, a few hops per layer: {ANN_HNSW_MS} ms per "
           f"question, about {ANN_SPEEDUP} times faster, and it finds the true nearest vector {ANN_RECALL}% of the time.")
s.box(W / 2 - 260, 8, 520, 46, "nt-bubble", 23)
s.both(W / 2, 38, f"1 คำถาม · ค้นใน {ANN_N} vector", f"One question · search {ANN_N} vectors", "pl-text", "middle")
import random as _r
# ---- left: exact search compares with every vector
s.box(20, 70, 560, 420, "sw-warn-box", 14)
s.both(40, 102, "✗ ค้นแบบตรงทุกตัว (exact)", "✗ Exact search: compare with every vector", "pl-label")
rnd = _r.Random(7)
pts = [(rnd.uniform(230, 550), rnd.uniform(140, 400)) for _ in range(110)]
qx, qy = 80, 270
near = min(pts, key=lambda p: (p[0] - 300) ** 2 + (p[1] - 250) ** 2)
for x, y in pts:
    s.out.append(f'<path d="M{qx} {qy} L{x:.0f} {y:.0f}" class="pl-line" stroke-width="0.5" opacity="0.35"/>')
for x, y in pts:
    s.out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" class="{"ml-bar-top" if (x, y) == near else "ml-bar"}"/>')
s.out.append(f'<circle cx="{qx}" cy="{qy}" r="12" class="pl-dot"/>')
s.text(qx, qy + 5, "?", "pl-num", "middle")
s.both(40, 432, f"เทียบ {ANN_N} ครั้งต่อ 1 คำถาม", f"{ANN_N} comparisons per question", "ml-neg")
s.both(40, 470, f"✗ {ANN_EXACT_MS} ms ต่อคำถาม · ข้อมูล 10 เท่า = ช้า 10 เท่า", f"✗ {ANN_EXACT_MS} ms per question · 10× the data = 10× slower", "ml-neg")
# ---- right: HNSW hops through a layered graph
s.box(600, 70, 560, 420, "nt-band-a", 14)
s.both(620, 102, "✓ ANN ด้วย HNSW: กระโดดตามกราฟ", "✓ ANN with HNSW: hop through a graph", "pl-label")
layers = [
    (155, [(650, 150), (730, 162), (820, 148), (900, 160)], [(650, 150), (730, 162), (820, 148)],
     "ชั้นบน: ไม่กี่จุด", "top: a few points"),
    (265, [(640, 268), (680, 255), (715, 275), (750, 258), (785, 272), (820, 255), (850, 275), (880, 262), (910, 270), (935, 255)],
     [(820, 255), (850, 275), (880, 262)], "ชั้นกลาง: ซูมเข้า", "middle: zoom in"),
    (375, [(635 + k * 13.5, 375 + (8 if k % 3 == 0 else -6 if k % 3 == 1 else 2)) for k in range(24)],
     [(878, 381), (891, 367), (905, 377)], "ชั้นล่าง: ทุกจุด", "bottom: every point"),
]
for i, (yc, ps, path, th, en) in enumerate(layers):
    s.box(624, yc - 34, 330, 68, "ml-cell", 10)
    for x, y in ps:
        s.out.append(f'<circle cx="{x}" cy="{y}" r="5" class="ml-bar"/>')
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        s.arrow(x1, y1, x2, y2)
    s.out.append(f'<circle cx="{path[0][0]}" cy="{path[0][1]}" r="6" class="ml-bar-top"/>')
    s.both(968, yc + 6, th, en, "pl-note")
    if i < 2:
        nx, ny = path[-1]
        s.out.append(f'<path d="M{nx} {ny + 8} V{layers[i + 1][0] - 40}" class="pl-line" stroke-dasharray="5 4"/>')
        s.arrow(nx, layers[i + 1][0] - 44, nx, layers[i + 1][0] - 36)
fx, fy = layers[2][2][-1]
s.out.append(f'<circle cx="{fx}" cy="{fy}" r="8" class="ml-bar-top"/>')
s.out.append(f'<circle cx="{fx + 22}" cy="{fy - 4}" r="11" class="pl-dot"/>')
s.text(fx + 22, fy + 1, "?", "pl-num", "middle")
s.both(620, 432, "แค่ไม่กี่ hop ต่อชั้น (ราว log N)", "only a few hops per layer (about log N)", "ml-ok")
s.both(620, 470, f"✓ {ANN_HNSW_MS} ms ต่อคำถาม · เร็วกว่า {ANN_SPEEDUP} เท่า", f"✓ {ANN_HNSW_MS} ms per question · {ANN_SPEEDUP}× faster", "ml-ok")
s.both(20, 522, "เหมือนเดินทาง: รถด่วนข้ามเมือง → รถท้องถิ่น → เดินไปถึงบ้าน", "Like travelling: an express train between cities → a local train → walk to the door", "pl-label")
s.both(20, 550, f"วัดจริง: numpy (exact) กับ hnswlib · HNSW เจอตัวที่ใกล้ที่สุดจริง {ANN_RECALL}% ของครั้ง บนประโยคจริง 43,900 ประโยค",
       f"Measured: numpy (exact) vs hnswlib · HNSW finds the true nearest {ANN_RECALL}% of the time on 43,900 real sentences", "pl-note")
s.save("l12-ann.svg", 566)

# ---------------------------------------------------------------- 22. what LangChain is: one ready piece per RAG step, joined with |
# The data under each piece is our own run on the 7 course facts (all-MiniLM-L6-v2: 384 numbers; top 2 = fact 7, fact 2).
W = 1180
s = Svg(W, "LangChain gives one ready piece per RAG step: Document, TextSplitter, Embeddings, VectorStore, Retriever, PromptTemplate, "
           "ChatModel and OutputParser, each shown with what it does on our 7 course facts. The last pieces are joined with | into one chain. "
           "Without LangChain you write every piece and the glue between them yourself; with it, every piece has the same invoke() and "
           "swapping one (Gemini for another model, memory for a real vector database) is a one-line change.")
STEPS = [("1 Load", "1 Load", "Document", "7 facts", "7 facts"),
         ("2 ตัด", "2 Split", "TextSplitter", "1 ชิ้น/ข้อ", "1 chunk each"),
         ("3 Embed", "3 Embed", "Embeddings", "384 ตัวเลข", "384 numbers"),
         ("4 เก็บ", "4 Store", "VectorStore", "7 vector", "7 vectors"),
         ("5 ค้น", "5 Retrieve", "Retriever", "fact 7, fact 2", "fact 7, fact 2"),
         ("6 Prompt", "6 Prompt", "PromptTemplate", "คำถาม+context", "Q + context"),
         ("7 ตอบ", "7 Generate", "ChatModel", "Gemini", "Gemini"),
         ("8 แปลง", "8 Parse", "OutputParser", "ข้อความ", "plain text")]
BW, GAP = 132, 12
for k, (th, en, cls, dth, den) in enumerate(STEPS):
    x = 20 + k * (BW + GAP)
    s.box(x, 20, BW, 112, "nt-band-a" if k < 4 else "nt-band-b", 12)
    s.both(x + BW / 2, 48, th, en, "pl-label", "middle")
    s.box(x + 8, 60, BW - 16, 30, "ml-cell", 6)
    s.text(x + BW / 2, 80, cls, "dg-code", "middle")
    s.both(x + BW / 2, 118, dth, den, "pl-note", "middle")
    if k < 7:
        s.arrow(x + BW + 1, 75, x + BW + GAP - 1, 75)
x4, x7 = 20 + 4 * (BW + GAP), 20 + 7 * (BW + GAP) + BW
s.out.append(f'<path d="M{x4} 142 V152 H{x7} V142" class="pl-line" fill="none"/>')
s.both((x4 + x7) / 2, 176, "ต่อด้วย | เป็น chain เดียว: rag_chain.invoke(คำถาม)", "joined with | into one chain: rag_chain.invoke(question)", "pl-label", "middle")
s.both(20, 176, "เตรียมครั้งเดียว", "prepared once", "pl-note")
# ✗ / ✓
s.box(20, 206, 560, 250, "sw-warn-box", 14)
s.both(40, 238, "✗ เขียนเองทั้งหมด", "✗ Write it all yourself", "pl-label")
blocks = [(50, 262, 110, 46), (190, 280, 90, 60), (310, 258, 120, 40), (460, 284, 90, 52)]
for (x, y, w, h) in blocks:
    s.box(x, y, w, h, "ml-cell", 6)
    for yy in range(y + 10, y + h - 6, 9):
        s.box(x + 8, yy, w - 16 - (yy % 3) * 6, 3, "ml-bar", 1)
for (a, b) in zip(blocks, blocks[1:]):
    x1, y1 = a[0] + a[2], a[1] + a[3] / 2
    x2, y2 = b[0], b[1] + b[3] / 2
    s.out.append(f'<path d="M{x1} {y1} C{x1 + 30} {y1 + 40} {x2 - 30} {y2 - 40} {x2} {y2}" class="pl-line" stroke-dasharray="3 4" fill="none"/>')
s.both(40, 384, "เขียนทุกชิ้น และโค้ด \"กาว\" ที่ต่อแต่ละชิ้นเอง", "you write every piece and the \"glue\" between them", "pl-text")
s.both(40, 412, "✗ เปลี่ยน Gemini เป็นโมเดลอื่น = แก้การเรียก API และการอ่านผล", "✗ switch Gemini to another model: rewrite the API call", "ml-neg")
s.both(40, 438, "✗ เปลี่ยนเป็น vector database จริง = เขียนการค้นใหม่", "✗ switch to a real vector database: rewrite the search", "ml-neg")
s.box(600, 206, 560, 250, "nt-band-a", 14)
s.both(620, 238, "✓ ใช้ชิ้นสำเร็จรูปของ LangChain", "✓ LangChain's ready pieces", "pl-label")
for k in range(5):
    x = 630 + k * 102
    s.box(x, 262, 88, 50, "ml-cell" if k != 3 else "sw-chip-warn", 8)
    s.text(x + 44, 292, "invoke()", "dg-code", "middle")
    if k < 4:
        s.out.append(f'<path d="M{x + 88} 287 H{x + 102}" class="pl-line"/>')
s.text(630 + 3 * 102 + 44, 334, "llm = …", "dg-code", "middle")
s.both(620, 384, "ทุกชิ้นต่อกันแบบเดียวกัน: .invoke() และ |", "every piece plugs in the same way: .invoke() and |", "pl-text")
s.both(620, 412, "✓ เปลี่ยนโมเดลหรือ vector database = แก้ 1 บรรทัด", "✓ swap the model or the vector database: change 1 line", "ml-ok")
s.both(620, 438, "✓ ชิ้นอื่นและ chain เหมือนเดิมทั้งหมด", "✓ every other piece and the chain stay the same", "ml-ok")
s.save("l12-langchain.svg", 470)


# ---------------------------------------------------------------- 23. time per question as the collection grows (same measurements)
SCALE = [("43,900", 3.6, 0.69), ("200,000", 8.8, 0.75), ("1,000,000", 42.9, 0.78)]
W = 1180
s = Svg(W, "Time per question as the collection grows. Exact search: 3.6 ms for 43,900 vectors, 8.8 ms for 200,000, 42.9 ms for "
           "1,000,000: it grows with the data. HNSW: 0.69, 0.75 and 0.78 ms: almost flat.")
s.both(20, 30, "เวลาต่อ 1 คำถาม เมื่อข้อมูลโตขึ้น", "Time per question as the collection grows", "pl-label")
for k, (lab_th, lab_en, col) in enumerate([("exact (ทุกตัว)", "exact (every vector)", "ml-bar"), ("HNSW (ANN)", "HNSW (ANN)", "ml-bar-top")]):
    x = 640 + k * 260
    s.box(x, 16, 18, 18, col, 3)
    s.both(x + 26, 31, lab_th, lab_en, "pl-note")
X0, X1, Y0 = 200, 1100, 60
mx = 45.0
for i, (n, ex, hn) in enumerate(SCALE):
    y = Y0 + i * 92
    s.text(180, y + 36, n, "pl-label", "end")
    s.both(180, y + 60, "vector", "vectors", "pl-note", "end")
    we, wh = (X1 - X0) * ex / mx, max(4, (X1 - X0) * hn / mx)
    s.box(X0, y + 8, we, 30, "ml-bar", 4)
    s.text(X0 + we + 10, y + 30, f"{ex} ms", "pl-label")
    s.box(X0, y + 44, wh, 30, "ml-bar-top", 4)
    s.text(X0 + wh + 10, y + 66, f"{hn} ms", "ml-ok")
s.both(20, Y0 + 3 * 92 + 22, "exact โตตามขนาดข้อมูล (ข้อมูล 23 เท่า → ช้า 12 เท่า) ส่วน HNSW แทบไม่เปลี่ยน",
       "Exact grows with the data (23× the vectors → 12× slower); HNSW barely changes", "ml-ok")
s.both(20, Y0 + 3 * 92 + 50, "200,000 และ 1,000,000 คือ vector จริง 43,900 ตัว ซ้ำพร้อมเติม noise เล็กน้อย",
       "200,000 and 1,000,000 = the 43,900 real vectors repeated with a little noise", "pl-note")
s.save("l12-ann-scale.svg", Y0 + 3 * 92 + 64)


# ---------------------------------------------------------------- 24. why rerank: the right fact is found but ranked too low (real scores)
# "What is taught on 19 October?" on the 7 facts. Search (all-MiniLM-L6-v2 cosine): fact 5 0.428, fact 3 0.418, fact 2 0.355,
# fact 4 0.347. Asking about 26 October gives the same top 2 (fact 5 0.453, fact 3 0.445): the vector hardly sees the date.
# Reranker (cross-encoder/ms-marco-MiniLM-L6-v2) on the same 4: fact 4 3.974, fact 3 -3.440, fact 5 -5.287, fact 2 -10.742.
W = 1180
s = Svg(W, "Why rerank? Question: What is taught on 19 October? The answer is fact 4. Searching by vectors ranks fact 4 only 4th "
           "(0.347), below fact 5, fact 3 and fact 2, because every one of them is about a date and what the class does; only the top 2 "
           "go to the LLM, so the answer is never sent. A reranker reads the question and each fact together, sees that 19 October "
           "matches, and moves fact 4 to 1st (3.97); the others drop below 0.")
s.box(W / 2 - 230, 8, 460, 46, "nt-bubble", 23)
s.text(W / 2, 38, "What is taught on 19 October?", "pl-text", "middle")
s.both(W / 2 + 244, 38, "คำตอบอยู่ใน fact 4", "the answer is in fact 4", "pl-note")
ROWS_B = [("5", "26 Oct: workflows, agents", "0.428"), ("3", "12 Oct: no class", "0.418"),
          ("2", "21 Sep: midterm exam", "0.355"), ("4", "19 Oct: dense retrieval, RAG", "0.347")]
ROWS_A = [("4", "19 Oct: dense retrieval, RAG", "3.97"), ("3", "12 Oct: no class", "−3.44"),
          ("5", "26 Oct: workflows, agents", "−5.29"), ("2", "21 Sep: midterm exam", "−10.74")]


def rank_list(x0, rows, score_th, score_en):
    s.both(x0 + 500, 150, score_th, score_en, "pl-note", "end")
    for k, (f, t, sc) in enumerate(rows):
        y = 164 + k * 50 + (28 if k >= 2 else 0)
        s.box(x0, y, 510, 40, "sw-chip-warn" if f == "4" else "ml-cell", 8)
        s.text(x0 + 14, y + 27, f"{k + 1}.", "pl-label")
        s.text(x0 + 46, y + 27, f"fact {f} · {t}", "pl-text")
        s.text(x0 + 496, y + 27, sc, "pl-label", "end")
    yl = 164 + 2 * 50 + 10
    s.out.append(f'<path d="M{x0 - 6} {yl} H{x0 + 516}" class="pl-line" stroke-dasharray="7 5"/>')
    return yl


# ---- left: search alone
s.box(20, 70, 560, 470, "sw-warn-box", 14)
s.both(40, 102, "✗ ค้นด้วย vector อย่างเดียว", "✗ Search by vectors alone", "pl-label")
s.both(40, 128, "เรียงด้วย cosine แล้วส่ง 2 อันดับแรกให้ LLM", "ranked by cosine; the top 2 go to the LLM", "pl-note")
yl = rank_list(45, ROWS_B, "cosine", "cosine")
s.both(300, yl - 10, "↑ ส่งให้ LLM", "↑ sent to the LLM", "pl-note")
s.both(300, yl + 22, "↓ ไม่ได้ส่ง", "↓ not sent", "pl-note")
s.both(45, 418, "ทำไม: vector จับได้แค่ “วันที่ + วิชาเรียนอะไร”", "Why: the vector catches “a date + what the class does”,", "pl-text")
s.both(45, 444, "ทั้ง 4 ข้อเป็นแบบนั้น จึงไม่ดูว่าเป็นวันที่ 19 ไหม", "true of all four; it barely checks that the day is 19", "pl-text")
s.both(45, 470, "(ถาม 26 October ก็ได้ 2 อันดับแรกเหมือนเดิม: fact 5, fact 3)",
       "(ask about 26 October: the same top 2, fact 5 and fact 3)", "pl-note")
s.both(40, 520, "✗ คำตอบอยู่อันดับ 4 ไม่ถึง LLM · Recall@2 = 0", "✗ the answer is 4th and never sent · Recall@2 = 0", "ml-neg")
# ---- right: rerank
s.box(600, 70, 560, 470, "nt-band-a", 14)
s.both(620, 102, "✓ แล้ว rerank: อ่านคำถามคู่กับแต่ละ fact", "✓ Then rerank: read the question with each fact", "pl-label")
s.both(620, 128, "โมเดลที่สองให้คะแนน 4 ข้อนี้ใหม่ แล้วเรียงใหม่", "a second model rescores these 4 and reorders them", "pl-note")
yl = rank_list(625, ROWS_A, "คะแนน reranker", "reranker score")
s.both(880, yl - 10, "↑ ส่งให้ LLM", "↑ sent to the LLM", "pl-note")
s.both(880, yl + 22, "↓ ไม่ได้ส่ง", "↓ not sent", "pl-note")
s.both(625, 418, "อ่านสองข้อความพร้อมกัน จึงเห็นว่า", "It reads both texts at once, so it sees", "pl-text")
s.both(625, 444, "“19 October” อยู่ทั้งในคำถามและใน fact 4", "“19 October” in the question and in fact 4", "pl-text")
s.both(625, 470, "คะแนนสูง = เกี่ยวข้อง ต่ำกว่า 0 = น่าจะไม่เกี่ยว (ไม่ใช่ 0–1)",
       "high = relevant, below 0 = probably not (not a 0–1 scale)", "pl-note")
s.both(620, 520, "✓ คำตอบขึ้นอันดับ 1 ถึง LLM · Recall@2 = 1", "✓ the answer is 1st and reaches the LLM · Recall@2 = 1", "ml-ok")
s.both(20, 572, "ค้นหาผู้สมัครให้เจอ แล้ว rerank ยกตัวที่ตอบได้จริงขึ้นบนสุด",
       "Search finds the candidates; reranking puts the one that answers on top", "pl-label")
s.both(20, 600, "คะแนนจริง: all-MiniLM-L6-v2 (ค้น) · cross-encoder/ms-marco-MiniLM-L6-v2 (rerank)",
       "real scores: all-MiniLM-L6-v2 (search) · cross-encoder/ms-marco-MiniLM-L6-v2 (rerank)", "pl-note")
s.save("l12-rerank-why.svg", 614)


# ---------------------------------------------------------------- 25. hybrid search: two searches, each half right, merged by rank (RRF)
# "What does 2190519 cover on 19 October?" BM25 (rank_bm25, lowercase [a-z0-9]+ tokens) top 4: fact 4, 1, 5, 3;
# dense (all-MiniLM-L6-v2) top 4: fact 5, 4, 3, 2. RRF k = 60: fact 4 0.03252, fact 5 0.03227, fact 3 0.03150, fact 1 0.01613, fact 2 0.01562.
W = 1180
s = Svg(W, "Hybrid search for 'What does 2190519 cover on 19 October?'. BM25 matches exact words: fact 4 first (19, October), "
           "fact 1 second only because of the code 2190519. Dense search matches meaning: fact 5 (26 October) first, fact 4 second. "
           "Reciprocal rank fusion adds 1/(60 + rank) from each list: fact 4 wins with 0.03252, because it is near the top of both.")
s.box(W / 2 - 260, 8, 520, 46, "nt-bubble", 23)
s.text(W / 2, 38, "What does 2190519 cover on 19 October?", "pl-text", "middle")
PX3 = [20, 410, 800]
heads = [("ml-cell", "A · BM25: ตรงคำ", "A · BM25: same words", "นับคำในคำถามที่อยู่ใน fact", "counts the question's words in each fact"),
         ("ml-cell", "B · Dense: ใกล้ความหมาย", "B · Dense: close meaning", "cosine ของ vector", "cosine of the vectors"),
         ("nt-band-a", "C · RRF: รวมด้วยอันดับ", "C · RRF: merge by rank", "1/(60 + อันดับ) จากทั้งสองรายการ", "add 1/(60 + rank) from each list")]
for x, (cls, th, en, sth, sen) in zip(PX3, heads):
    s.box(x, 70, 360, 380, cls, 14)
    s.both(x + 16, 102, th, en, "pl-label")
    s.both(x + 16, 128, sth, sen, "pl-note")
BM = [("4", "19 · October", True), ("1", "2190519", False), ("5", "October", False), ("3", "October", False)]
DN = [("5", "26 Oct: agents", False), ("4", "19 Oct: RAG", True), ("3", "12 Oct: no class", False), ("2", "21 Sep: midterm", False)]
RR = [("4", "1/61 + 1/62 = 0.03252", True), ("5", "1/63 + 1/61 = 0.03227", False), ("3", "1/64 + 1/63 = 0.03150", False),
      ("1", "1/62 + 0 = 0.01613", False), ("2", "0 + 1/64 = 0.01562", False)]
for x, rows, hint in [(PX3[0], BM, "match"), (PX3[1], DN, None)]:
    for k, (f, txt, gold) in enumerate(rows):
        y = 146 + k * 52
        s.box(x + 16, y, 328, 40, "sw-chip-warn" if gold else "ml-cell", 8)
        s.text(x + 30, y + 27, f"{k + 1}. fact {f}", "pl-label")
        s.text(x + 150, y + 27, txt, "pl-text")
s.both(PX3[0] + 16, 382, "✓ เห็น 19 กับ 2190519 ตรงเป๊ะ", "✓ sees 19 and 2190519 exactly", "ml-ok")
s.both(PX3[0] + 16, 408, "✗ fact 1 ติดมาเพราะรหัสวิชาเท่านั้น", "✗ fact 1 is 2nd only for the code", "ml-neg")
s.both(PX3[1] + 16, 382, "✓ เข้าใจว่าถามเรื่องหัวข้อที่เรียน", "✓ knows it asks for a class topic", "ml-ok")
s.both(PX3[1] + 16, 408, "✗ 26 Oct ≈ 19 Oct สำหรับ vector", "✗ to a vector, 26 Oct ≈ 19 Oct", "ml-neg")
for k, (f, txt, gold) in enumerate(RR):
    y = 146 + k * 46
    s.box(PX3[2] + 16, y, 328, 36, "sw-chip-warn" if gold else "ml-cell", 8)
    s.text(PX3[2] + 30, y + 25, f"{k + 1}. fact {f}", "pl-label")
    s.text(PX3[2] + 336, y + 25, txt, "pl-text", "end")
s.both(PX3[2] + 16, 408, "✓ fact 4 อยู่บนของทั้งสองรายการ → ชนะ", "✓ fact 4 is high in both → it wins", "ml-ok")
s.arrow(384, 260, 406, 260)
s.arrow(774, 260, 796, 260)
s.both(20, 482, "คะแนน BM25 กับ cosine คนละสเกล บวกกันตรง ๆ ไม่ได้ RRF จึงใช้แค่อันดับ (k = 60)",
       "BM25 scores and cosines are on different scales, so RRF adds up ranks only (k = 60)", "pl-label")
s.save("l12-hybrid-rrf.svg", 498)


# ---------------------------------------------------------------- 26. query rewriting: the same failed question, asked better (real ranks)
# all-MiniLM-L6-v2 on the 7 facts. Original "What is taught on 19 October?": top 4 = 5, 3, 2, 4 (fact 4 4th).
# Rewrites (example LLM output): "Which topic does the 19 October 2026 class cover?" 5, 4, 6, 3; "19 October 2026 lecture topic" 5, 4, 2, 6;
# "19 October class content" 5, 4, 3, 7. RRF of all 4 lists: fact 5 0.0656, fact 4 0.0640, fact 3 0.0476.
W = 1180
s = Svg(W, "Query rewriting on 'What is taught on 19 October?'. Asked as it is, the search ranks fact 4, the answer, 4th, so with the top 2 "
           "it is never sent. An LLM writes three other versions of the question; each ranks fact 4 2nd. Searching with all four and "
           "merging the lists with RRF gives fact 5 and fact 4 as the top 2, so the answer reaches the LLM.")
s.box(20, 20, 400, 420, "sw-warn-box", 14)
s.both(40, 52, "✗ ถามแบบเดิม", "✗ The question as asked", "pl-label")
s.box(40, 74, 360, 44, "nt-bubble", 22)
s.text(220, 103, "What is taught on 19 October?", "pl-text", "middle")
for k, f in enumerate(["5", "3", "2", "4"]):
    y = 140 + k * 46
    s.box(60, y, 300, 36, "sw-chip-warn" if f == "4" else "ml-cell", 8)
    s.text(76, y + 25, f"{k + 1}. fact {f}", "pl-text")
s.out.append('<path d="M50 225 H370" class="pl-line" stroke-dasharray="7 5"/>')
s.both(240, 334, "← คำตอบ อันดับ 4", "← the answer, 4th", "ml-neg")
s.both(40, 416, "✗ top 2 ไม่มี fact 4 · Recall@2 = 0", "✗ fact 4 not in the top 2 · Recall@2 = 0", "ml-neg")
s.box(440, 20, 720, 420, "nt-band-a", 14)
s.both(460, 52, "✓ ให้ LLM เขียนคำถามใหม่ 3 แบบ แล้วค้นทุกแบบ", "✓ An LLM writes 3 more versions; search with each", "pl-label")
RW = [("Which topic does the 19 October 2026 class cover?", "2"), ("19 October 2026 lecture topic", "2"), ("19 October class content", "2")]
for k, (q, r) in enumerate(RW):
    y = 76 + k * 56
    s.box(460, y, 540, 44, "ml-cell", 10)
    s.text(476, y + 29, q, "dg-code")
    s.both(1016, y + 29, f"fact 4: อันดับ {r}", f"fact 4: rank {r}", "ml-ok")
s.arrow(730, 248, 730, 274)
s.both(746, 266, "รวม 4 รายการด้วย RRF (RAG Fusion)", "merge the 4 lists with RRF (RAG Fusion)", "pl-note")
for k, (f, sc) in enumerate([("5", "0.0656"), ("4", "0.0640"), ("3", "0.0476")]):
    y = 284 + k * 42
    s.box(560, y, 340, 34, "sw-chip-warn" if f == "4" else "ml-cell", 8)
    s.text(576, y + 24, f"{k + 1}. fact {f}", "pl-text")
    s.text(886, y + 24, sc, "pl-text", "end")
s.out.append('<path d="M550 360 H910" class="pl-line" stroke-dasharray="7 5"/>')
s.both(460, 416, "✓ fact 4 ติด top 2 แล้ว · Recall@2 = 1", "✓ fact 4 is in the top 2 · Recall@2 = 1", "ml-ok")
s.both(20, 470, "คำถามใหม่ 3 แบบเป็นตัวอย่างที่ LLM อาจเขียน · อันดับเป็นค่าจริงจาก all-MiniLM-L6-v2",
       "the 3 rewrites are examples of what an LLM may write · the ranks are real (all-MiniLM-L6-v2)", "pl-note")
s.save("l12-query-rewrite.svg", 486)


# ---------------------------------------------------------------- 27. what each evaluation score compares (question, retrieved facts, answer, gold answer)
W = 1180
s = Svg(W, "What each score compares. Retrieval scores (Recall@k, Precision@k, MRR) compare the question with the retrieved facts. "
           "Faithfulness compares the answer with the retrieved facts: is every claim in them? Relevance compares the answer with the "
           "question: does it answer what was asked? Correctness compares the answer with the gold answer we wrote: is it right? "
           "Faithfulness and relevance need no gold answer; correctness does.")
s.node(30, 30, 330, 84, "คำถาม", "Question", "nt-bubble", "When is the final exam?", "When is the final exam?")
s.node(820, 30, 330, 84, "fact ที่ค้นมา", "Retrieved facts", "ml-cell", "fact 7 · fact 2", "fact 7 · fact 2")
s.node(425, 300, 330, 84, "คำตอบของ RAG", "The RAG answer", "sw-chip-warn", "จาก Gemini", "written by Gemini")
s.node(820, 430, 330, 84, "คำตอบมาตรฐาน (gold)", "Gold answer", "nt-band-a", "30 Nov 2026, 13:00-16:00", "30 Nov 2026, 13:00-16:00")
# retrieval edge
s.out.append('<path d="M362 72 H818" class="pl-line" stroke-dasharray="7 5"/>')
s.both(590, 60, "การค้น: Recall@k, Precision@k, MRR", "Retrieval: Recall@k, Precision@k, MRR", "pl-note", "middle")
s.both(590, 96, "ค้นเจอ fact ที่ถูกไหม", "did search find the right facts?", "pl-note", "middle")
# faithfulness: facts <-> answer
s.arrow(900, 116, 700, 298)
s.box(820, 166, 330, 92, "nt-bubble", 12)
s.both(836, 196, "① Faithfulness (ยึดเอกสาร)", "① Faithfulness", "pl-label")
s.both(836, 222, "ทุกข้อความในคำตอบ", "is every claim in the answer", "pl-text")
s.both(836, 248, "อยู่ใน fact ที่ค้นมาไหม", "in the retrieved facts?", "pl-text")
# relevance: question <-> answer
s.arrow(240, 116, 480, 298)
s.box(30, 166, 330, 92, "nt-bubble", 12)
s.both(46, 196, "② Relevance (ตรงคำถาม)", "② Relevance", "pl-label")
s.both(46, 222, "ตอบสิ่งที่ถามไหม", "does it answer", "pl-text")
s.both(46, 246, "(ไม่ตอบเรื่องอื่น)", "what was asked?", "pl-text")
# correctness: answer <-> gold
s.arrow(700, 386, 818, 450)
s.box(30, 420, 560, 92, "nt-bubble", 12)
s.both(46, 450, "③ Correctness (ถูกต้อง)", "③ Correctness", "pl-label")
s.both(46, 476, "ตรงกับคำตอบมาตรฐานที่เราเขียนไว้ไหม", "does it match the gold answer we wrote?", "pl-text")
s.arrow(592, 466, 816, 470, dashed=True)
s.both(30, 556, "① และ ② ไม่ต้องมีคำตอบมาตรฐาน ใช้ตรวจคำถามจริงของผู้ใช้ได้ · ③ ต้องมี gold จึงใช้กับชุดทดสอบ",
       "① and ② need no gold answer, so they work on real users' questions · ③ needs a gold answer: a test set", "ml-ok")
s.save("l12-eval-map.svg", 572)


# ---------------------------------------------------------------- 28. three answers to the same question, scored (claims checked by hand)
# Context = fact 7 + fact 2 (the real top 2). Gold claims: date (Monday 30 November 2026), time (13:00-16:00).
# Relevance: RAGAS answer relevancy = cosine (all-MiniLM-L6-v2) between the question and a question written back from the answer:
# A "When is the final exam?" 1.00, B "When and where is the final exam?" 0.96, C "When was the midterm exam?" 0.66.
# Correctness: claim F1 = right / (right + ½(made-up + missing)).
W = 1180
s = Svg(W, "Three answers to 'When is the final exam?' from the same retrieved facts (fact 7: the final exam is on Monday 30 November 2026, "
           "13:00-16:00; fact 2: the midterm was on Monday 21 September 2026). Answer A gives the date and time: faithfulness 2/2 = 1, "
           "relevance 1.00, correctness 1. Answer B adds 'in room 501', which no retrieved fact says: faithfulness 1/2 = 0.5, relevance 0.96, "
           "correctness 0.5. Answer C gives the midterm date: faithful (1/1 = 1) but it answers another question: relevance 0.66, correctness 0.")
s.box(W / 2 - 200, 8, 400, 46, "nt-bubble", 23)
s.text(W / 2, 38, "When is the final exam?", "pl-text", "middle")
s.box(20, 66, W - 40, 62, "ml-cell", 10)
s.both(36, 90, "fact ที่ค้นมา:", "Retrieved:", "pl-note")
s.text(150, 90, "[fact 7] The final exam is on Monday 30 November 2026, 13:00-16:00.", "dg-code")
s.text(150, 114, "[fact 2] The midterm exam was on Monday 21 September 2026, 13:00-16:00.", "dg-code")
ANS = [
    ("A", "nt-band-a", ["The final exam is on Monday", "30 November 2026, 13:00-16:00."],
     [("Monday 30 November 2026", True, "fact 7"), ("13:00-16:00", True, "fact 7")],
     [("2/2 = 1", 1.0), ("1.00", 1.0), ("1", 1.0)], ("✓ ถูก ครบ ยึดเอกสาร", "✓ right, complete, grounded", "ml-ok")),
    ("B", "sw-warn-box", ["The final exam is on Monday", "30 November 2026, in room 501."],
     [("Monday 30 November 2026", True, "fact 7"), ("in room 501", False, "no fact says it")],
     [("1/2 = 0.5", 0.5), ("0.96", 0.96), ("0.5", 0.5)], ("✗ แต่งห้องสอบขึ้นมาเอง", "✗ made up the exam room", "ml-neg")),
    ("C", "sw-warn-box", ["The midterm exam was on", "Monday 21 September 2026."],
     [("midterm: 21 September 2026", True, "fact 2")],
     [("1/1 = 1", 1.0), ("0.66", 0.66), ("0", 0.0)], ("✗ ยึดเอกสาร แต่ตอบผิดคำถาม", "✗ grounded, but the wrong question", "ml-neg")),
]
MET = [("① Faithfulness", "① Faithfulness"), ("② Relevance", "② Relevance"), ("③ Correctness", "③ Correctness")]
for i, (name, cls, lines, claims, scores, res) in enumerate(ANS):
    x = 20 + i * 384
    s.box(x, 144, 372, 470, cls, 14)
    s.both(x + 16, 176, f"คำตอบ {name}", f"Answer {name}", "pl-label")
    s.box(x + 16, 188, 340, 62, "ml-cell", 8)
    for k, ln in enumerate(lines):
        s.text(x + 28, 212 + k * 24, ln, "dg-code")
    s.both(x + 16, 280, "ข้อความ (claim) → อยู่ใน fact ไหม", "claims → in the facts?", "pl-note")
    for k, (c, ok, src) in enumerate(claims):
        y = 292 + k * 58
        s.box(x + 16, y, 340, 52, "pl-chip" if ok else "pl-chip-del", 8)
        s.text(x + 30, y + 22, c, "pl-text")
        s.text(x + 30, y + 46, ("✓ " if ok else "✗ ") + src, "ml-ok" if ok else "ml-neg")
    for k, ((th, en), (lab, v)) in enumerate(zip(MET, scores)):
        y = 418 + k * 44
        s.both(x + 16, y + 18, th, en, "pl-note")
        s.box(x + 160, y + 4, 100, 18, "ml-cell", 4)
        if v > 0:
            s.box(x + 160, y + 4, 100 * v, 18, "ml-bar-top", 4)
        s.text(x + 356, y + 19, lab, "pl-label", "end")
    s.both(x + 16, 594, res[0], res[1], res[2])
s.both(20, 646, "คำตอบ A–C เป็นตัวอย่างที่เขียนขึ้น · gold มี 2 ข้อ: วันที่ และเวลา",
       "answers A–C are written as examples · the gold answer has 2 claims: date and time", "pl-note")
s.both(20, 672, "relevance = cosine (all-MiniLM-L6-v2) ของคำถาม กับคำถามที่เขียนย้อนจากคำตอบ",
       "relevance = cosine (all-MiniLM-L6-v2) of the question and a question written back from the answer", "pl-note")
s.save("l12-answer-scores.svg", 688)


# ---------------------------------------------------------------- 29. why an LLM judge: similarity scores can't see a wrong date (real numbers)
# Against the gold answer: word-overlap F1 (lowercase [a-z0-9]+ tokens) A 1.00, B 0.72, C 0.45;
# BERTScore F1 (roberta-large, rescaled with baseline) A 1.00, B 0.61, C 0.57. Claim-checking (judge) correctness: 1, 0.5, 0.
W = 1180
s = Svg(W, "Why use an LLM judge? Scored against the gold answer, the wrong answer C (the midterm date) still gets 0.45 for word overlap and "
           "0.57 for BERTScore, almost the same as answer B (0.61), because it shares most of the words and the sentence shape. "
           "A judge that checks each claim gives C 0, B 0.5 and A 1.")
s.box(20, 20, 560, 380, "sw-warn-box", 14)
s.both(40, 52, "✗ วัดความคล้ายของข้อความ", "✗ Text similarity scores", "pl-label")
s.both(40, 78, "เทียบคำตอบกับ gold ทั้งประโยค", "compare the whole answer with the gold one", "pl-note")
s.box(600, 20, 560, 380, "nt-band-a", 14)
s.both(620, 52, "✓ LLM judge ตรวจทีละข้อความ", "✓ An LLM judge checks each claim", "pl-label")
s.both(620, 78, "วันที่ถูกไหม เวลาถูกไหม มีอะไรแต่งเพิ่มไหม", "right date? right time? anything made up?", "pl-note")
SIM = [("A", 1.00, 1.00), ("B", 0.72, 0.61), ("C", 0.45, 0.57)]
for k, (n, ov, bs) in enumerate(SIM):
    y = 110 + k * 92
    s.both(40, y + 36, f"คำตอบ {n}", f"Answer {n}", "pl-label")
    for j, (lab, v, cls) in enumerate([("word overlap F1", ov, "ml-bar"), ("BERTScore", bs, "ml-bar-top")]):
        yy = y + 8 + j * 34
        s.box(170, yy, 260 * v, 24, cls, 4)
        s.text(170 + 260 * v + 8, yy + 19, f"{v:.2f}", "pl-label")
s.box(40, 368 - 4, 16, 16, "ml-bar", 3); s.text(62, 377, "word overlap F1", "pl-note")
s.box(250, 368 - 4, 16, 16, "ml-bar-top", 3); s.text(272, 377, "BERTScore", "pl-note")
JD = [("A", "วันที่ ✓ เวลา ✓", "date ✓ time ✓", "1", 1.0), ("B", "วันที่ ✓ เวลา: ขาด · ห้อง 501: แต่งเพิ่ม", "date ✓ time missing · room 501 made up", "0.5", 0.5),
      ("C", "วันสอบกลางภาค ≠ สอบปลายภาค", "midterm date ≠ final exam", "0", 0.0)]
for k, (n, th, en, lab, v) in enumerate(JD):
    y = 110 + k * 92
    s.both(620, y + 36, f"คำตอบ {n}", f"Answer {n}", "pl-label")
    s.both(750, y + 22, th, en, "pl-text")
    s.box(750, y + 40, 260, 24, "ml-cell", 4)
    if v > 0:
        s.box(750, y + 40, 260 * v, 24, "ml-bar-top", 4)
    s.text(1140, y + 59, lab, "pl-label", "end")
s.both(40, 428, "✗ C ผิดทั้งข้อ แต่ได้ 0.57 เกือบเท่า B (0.61)", "✗ C is plain wrong, yet scores 0.57, almost B's 0.61", "ml-neg")
s.both(620, 428, "✓ C = 0, B = 0.5, A = 1", "✓ C = 0, B = 0.5, A = 1", "ml-ok")
s.both(20, 466, "คำส่วนใหญ่เหมือนกัน (the … exam … on Monday … 2026) จึงคล้ายกันมาก แม้วันที่จะผิด",
       "Most words are shared (the … exam … on Monday … 2026), so the texts look alike even though the date is wrong", "pl-label")
s.both(20, 494, "ค่าจริง: word overlap F1 ของคำ · BERTScore F1 (roberta-large, rescaled) · คะแนน judge = ข้อความที่ถูก / (ถูก + ½(แต่งเพิ่ม + ขาด))",
       "real values: word-overlap F1 · BERTScore F1 (roberta-large, rescaled) · judge score = right / (right + ½(made up + missing))", "pl-note")
s.save("l12-judge-why.svg", 510)


# ---------------------------------------------------------------- 30. how an LLM judge computes faithfulness (the RAGAS steps) on answer B
W = 1180
s = Svg(W, "How an LLM judge scores faithfulness, on answer B. Input: the question, the retrieved facts and the answer. Step 1: the judge "
           "LLM splits the answer into claims: the final exam is on Monday 30 November 2026; the final exam is in room 501. Step 2: it "
           "checks each claim against the facts: the first is supported by fact 7, the second is in no retrieved fact. Step 3: plain code "
           "counts: 1 supported out of 2 = 0.5.")
s.box(20, 20, 300, 400, "ml-cell", 14)
s.both(36, 52, "Input", "Input", "pl-label")
s.both(36, 88, "คำถาม", "question", "pl-note")
s.text(36, 112, "When is the final exam?", "dg-code")
s.both(36, 150, "fact ที่ค้นมา", "retrieved facts", "pl-note")
for k, ln in enumerate(["[fact 7] final exam:", "Monday 30 November 2026,", "13:00-16:00", "[fact 2] midterm:", "Monday 21 September 2026"]):
    s.text(36, 174 + k * 22, ln, "dg-code")
s.both(36, 306, "คำตอบ B", "answer B", "pl-note")
for k, ln in enumerate(["The final exam is on", "Monday 30 November 2026,", "in room 501."]):
    s.text(36, 330 + k * 22, ln, "dg-code")
s.arrow(322, 220, 352, 220)
X1 = 356
s.box(X1, 20, 800, 400, "nt-band-a", 14)
s.both(X1 + 16, 52, "Judge LLM (เช่น Gemini) + prompt ที่บอกเกณฑ์", "A judge LLM (e.g. Gemini) + a prompt with the rules", "pl-label")
badge(X1 + 30, 96, 1)
s.both(X1 + 52, 102, "แตกคำตอบเป็นข้อความย่อย (claim)", "Split the answer into claims", "pl-label")
s.box(X1 + 52, 116, 340, 36, "ml-cell", 8); s.text(X1 + 64, 140, "1. final exam: Mon 30 Nov 2026", "pl-text")
s.box(X1 + 52, 158, 340, 36, "ml-cell", 8); s.text(X1 + 64, 182, "2. final exam: in room 501", "pl-text")
badge(X1 + 30, 230, 2)
s.both(X1 + 52, 236, "ตรวจทีละข้อ: อยู่ใน fact ไหม พร้อมเหตุผล", "Check each claim against the facts, with a reason", "pl-label")
s.box(X1 + 52, 250, 720, 36, "pl-chip", 8)
s.both(X1 + 64, 274, "1 → ✓ มี: fact 7 บอกว่า Monday 30 November 2026", "1 → ✓ yes: fact 7 says Monday 30 November 2026", "pl-text")
s.box(X1 + 52, 292, 720, 36, "pl-chip-del", 8)
s.both(X1 + 64, 316, "2 → ✗ ไม่มี: ไม่มี fact ไหนพูดถึงห้องสอบ", "2 → ✗ no: no retrieved fact mentions the exam room", "pl-text")
badge(X1 + 30, 364, 3)
s.both(X1 + 52, 370, "โค้ดนับ: ✓ 1 จาก 2 ข้อ → faithfulness = 1/2 = 0.5", "Code counts: 1 of 2 claims ✓ → faithfulness = 1/2 = 0.5", "pl-label")
s.both(X1 + 52, 398, "LLM ทำขั้น 1–2 ที่ต้องอ่านภาษา ส่วนการนับเป็นโค้ดธรรมดา", "the LLM does the reading (1–2); the counting is plain code", "pl-note")
s.both(20, 456, "correctness ใช้ขั้นเดียวกัน แต่เทียบกับคำตอบมาตรฐาน (gold) แทน fact ที่ค้นมา",
       "Correctness uses the same steps, checked against the gold answer instead of the retrieved facts", "ml-ok")
s.save("l12-llm-judge.svg", 472)


# ---------------------------------------------------------------- 31. why BERTScore misses a wrong date: word-by-word matches (real values)
# roberta-large, layer 17 (bert_score's default for English), cosine of word vectors. Answer C's words matched to the gold answer:
# The 0.99, midterm→final 0.92, exam 0.99, was→is 0.96, on 0.98, Monday 0.98, 21→30 0.92, September→November 0.92,
# 2026 0.99 (tokens 20 + 26: 0.989, 0.992). Gold-only "13:00-16:00": its 7 tokens' best matches in C average 0.77.
# Whole answer (raw BERTScore F1): C 0.93, B 0.93; rescaled 0.57 vs 0.61.
W = 1180
s = Svg(W, "How BERTScore compares answer C with the gold answer, word by word. Each word of answer C is matched to the most similar "
           "word in the gold answer. Same words score about 0.99. The wrong words still score 0.92: midterm matches final, 21 matches 30, "
           "September matches November, because they are the same kind of word (an exam, a number, a month). So the wrong answer C gets "
           "0.93 overall, the same as answer B.")
COLS = [("The", "The", "0.99", False), ("final", "midterm", "0.92", True), ("exam", "exam", "0.99", False), ("is", "was", "0.96", True),
        ("on", "on", "0.98", False), ("Monday", "Monday", "0.98", False), ("30", "21", "0.92", True), ("November", "September", "0.92", True),
        ("2026,", "2026.", "0.99", False), ("13:00-16:00.", None, "0.77", True)]
widths = [max(width(g), width(c or "")) + 26 for g, c, _, _ in COLS]
gap = 10
x = (W - (sum(widths) + gap * (len(COLS) - 1))) / 2
s.both(20, 36, "คำตอบมาตรฐาน (gold)", "Gold answer", "pl-label")
s.both(20, 274, "คำตอบ C (ผิด: ให้วันสอบกลางภาค)", "Answer C (wrong: the midterm date)", "pl-label")
for (g, c, sc, diff), w in zip(COLS, widths):
    cx = x + w / 2
    s.box(x, 56, w, 40, "ml-cell", 8)
    s.text(cx, 82, g, "pl-text", "middle")
    if c:
        s.box(x, 200, w, 40, "sw-chip-warn" if diff else "ml-cell", 8)
        s.text(cx, 226, c, "pl-text", "middle")
        s.out.append(f'<path d="M{cx:g} 98 V198" class="pl-line"/>')
    else:
        s.out.append(f'<rect x="{x:g}" y="200" width="{w:g}" height="40" rx="8" class="pl-chip-del" stroke-dasharray="6 5"/>')
        s.both(cx, 226, "ไม่มี", "missing", "ml-neg", "middle")
        s.out.append(f'<path d="M{cx:g} 98 V198" class="pl-line" stroke-dasharray="5 5"/>')
    s.box(cx - 30, 134, 60, 28, "nt-bubble" if not diff else "sw-warn-box", 14)
    s.text(cx, 154, sc, "ml-neg" if diff and sc != "0.96" else "pl-label", "middle")
    x += w + gap
s.both(20, 318, "คำเดียวกัน ≈ 0.99 · คำที่ผิดยังได้ 0.92 เพราะเป็นคำชนิดเดียวกัน:", "Same word ≈ 0.99 · the wrong words still get 0.92, because they are the same kind of word:", "pl-text")
s.both(20, 346, "midterm ≈ final (สอบทั้งคู่) · 21 ≈ 30 (ตัวเลขทั้งคู่) · September ≈ November (เดือนทั้งคู่)",
       "midterm ≈ final (both exams) · 21 ≈ 30 (both numbers) · September ≈ November (both months)", "pl-text")
s.both(20, 382, "✗ BERTScore ถามว่า “มีคำที่ความหมายคล้ายกันไหม” ไม่ได้ถามว่า “วันที่ถูกไหม” → C ได้ 0.93 เท่ากับ B",
       "✗ BERTScore asks “is there a word with a similar meaning?”, not “is the date right?” → C gets 0.93, like B", "ml-neg")
s.both(20, 410, "(ปรับสเกลเป็น 0–1 แบบที่ใช้กันทั่วไป: C 0.57, B 0.61 ยังใกล้กันมาก)",
       "(rescaled to the usual 0–1 range: C 0.57, B 0.61, still very close)", "pl-note")
s.both(20, 440, "ค่าจริง: roberta-large ชั้นที่ 17 (ค่าเริ่มต้นของ BERTScore), cosine ของ vector คำ · 13:00-16:00 ไม่มีคู่ใน C จึงได้แค่ 0.77",
       "real values: roberta-large, layer 17 (BERTScore's default), cosine of word vectors · 13:00-16:00 has no partner in C, so only 0.77", "pl-note")
s.save("l12-bertscore-words.svg", 456)
