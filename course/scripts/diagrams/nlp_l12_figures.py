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

# ---------------------------------------------------------------- 6. retrieval: scores and top-k
# cosine similarity from sentence-transformers/all-MiniLM-L6-v2 (course/.venv), question "When is the final exam?"
facts = [
    (7, "The final exam is on Monday 30 November 2026, 13:00-16:00.", 0.89),
    (2, "The midterm exam was on Monday 21 September 2026, 13:00-16:00.", 0.68),
    (5, "On 26 October 2026 the class covers workflows and LLM agents.", 0.42),
    (4, "On 19 October 2026 the class covers dense retrieval and RAG.", 0.41),
    (3, "There is no class on Monday 12 October 2026 because of the long weekend.", 0.34),
    (1, "2190519 Natural Language Processing meets on Mondays, ... room 501.", 0.27),
    (6, "On 2 November 2026 the class covers named entity recognition (NER).", 0.23),
]
s = Svg(900, "Retrieval for the question 'When is the final exam?': each fact's cosine similarity to the question, sorted. The top 2, the final exam and the midterm, are retrieved.")
s.box(20, 14, 520, 44, "nt-bubble", 22)
s.text(40, 43, "Question: When is the final exam?", "pl-text")
s.both(560, 43, "cosine similarity (สูง = ความหมายใกล้)", "cosine similarity (high = close in meaning)", "pl-note")
y = 96
for k, (n, txt, sc) in enumerate(facts):
    top = k < 2
    s.text(20, y + 6, f"fact {n}", "pl-label" if top else "pl-note")
    s.text(100, y + 6, txt if len(txt) < 62 else txt[:60] + "…", "dg-code")
    w = 150 * sc
    s.box(700, y - 11, w, 22, "ml-bar-top" if top else "ml-bar", 4)
    s.text(708 + w, y + 6, f"{sc:.2f}", "pl-label" if top else "pl-note")
    if k == 1:
        s.out.append(f'<path d="M14 {y + 22} L886 {y + 22}" class="pl-line" stroke-dasharray="6 5"/>')
        s.both(886, y + 44, "↑ top-k = 2 ส่งต่อให้ LLM", "↑ top-k = 2 go on to the LLM", "ml-ok", "end")
        y += 34
    y += 36
s.both(20, y + 14, "คะแนนจากโมเดล embedding แบบเปิด all-MiniLM-L6-v2 ตัวเลขของ Gemini ต่างไป แต่ลำดับใกล้เคียงกัน",
       "Scores from the open embedding model all-MiniLM-L6-v2; Gemini's numbers differ, the order is similar", "pl-note")
s.save("l12-retrieve.svg", y + 32)

# ---------------------------------------------------------------- 7. two-stage retrieval
s = Svg(900, "Two-stage retrieval: a fast retriever narrows 100,000 chunks to the top 50, a slower reranker reorders them and keeps the top 5, which go to the LLM with the question.")
s.box(10, 10, 430, 200, "nt-band-a", 14)
s.both(26, 40, "ขั้น 1: ค้นกว้าง เร็ว", "Stage 1: retrieve, fast and broad", "pl-label")
s.box(460, 10, 430, 200, "nt-band-b", 14)
s.both(476, 40, "ขั้น 2: เรียงใหม่ ละเอียด", "Stage 2: rerank, slower and precise", "pl-label")
s.node(26, 64, 120, 70, "100,000", "100,000", "nt-bubble", "chunk ทั้งหมด", "all chunks")
s.node(176, 64, 140, 70, "BM25 / vector", "BM25 / vector", "ml-cell-b", "retriever", "retriever")
s.node(336, 64, 92, 70, "50", "50", "nt-out", "top 50", "top 50")
s.node(476, 64, 160, 70, "Cross-encoder", "Cross-encoder", "ml-cell-b", "reranker", "reranker")
s.node(666, 64, 92, 70, "5", "5", "nt-out", "top 5", "top 5")
s.node(776, 64, 100, 70, "LLM", "LLM", "nt-bubble", "+ คำถาม", "+ question")
s.arrow(148, 99, 174, 99)
s.arrow(318, 99, 334, 99)
s.arrow(430, 99, 474, 99)
s.arrow(638, 99, 664, 99)
s.arrow(760, 99, 774, 99)
s.both(26, 170, "เน้น recall: อย่าให้หลุด", "goal: recall, don't miss it", "pl-note")
s.both(26, 194, "vector ของเอกสารคำนวณไว้ล่วงหน้า", "document vectors are computed in advance", "pl-note")
s.both(476, 170, "เน้น precision: ของดีขึ้นบน", "goal: precision, best on top", "pl-note")
s.both(476, 194, "รันโมเดลใหม่ทุกคู่ (คำถาม, chunk)", "runs the model on every (question, chunk) pair", "pl-note")
s.both(10, 244, "ตัวเลข 50 และ 5 เป็นตัวอย่าง ไม่ใช่ค่าที่ต้องใช้", "50 and 5 are examples, not required settings", "pl-note")
s.save("l12-two-stage.svg", 258)

# ---------------------------------------------------------------- 8. bi-encoder vs cross-encoder
# real scores: query "What is taught on 19 October?", document fact 4 "On 19 October 2026 the class covers dense retrieval and RAG."
# (all-MiniLM-L6-v2 cosine 0.347; cross-encoder/ms-marco-MiniLM-L6-v2 3.974)
s = Svg(900, "Bi-encoder: the query and the document are encoded separately into vectors and compared with cosine similarity (0.35). Cross-encoder: the query and the document go into one Transformer together, which outputs a relevance score (3.97).")
s.box(10, 10, 430, 380, "nt-band-a", 14)
s.text(26, 40, "Bi-encoder", "pl-label")
s.both(150, 40, "ใช้ค้น (retrieve)", "used to retrieve", "pl-note")
s.box(460, 10, 430, 380, "nt-band-b", 14)
s.text(476, 40, "Cross-encoder", "pl-label")
s.both(626, 40, "ใช้เรียงใหม่ (rerank)", "used to rerank", "pl-note")
for x, lab in ((26, "Query"), (232, "Document")):
    s.node(x, 60, 190, 44, lab, lab, "nt-bubble", tcls="pl-text")
    s.arrow(x + 95, 106, x + 95, 128)
    s.node(x, 130, 190, 44, "Encoder", "Encoder", "ml-cell-b", tcls="pl-text")
    s.arrow(x + 95, 176, x + 95, 198)
    s.box(x, 200, 190, 40, "ml-cell", 8)
    s.text(x + 95, 226, "[0.12, -0.40, …]", "dg-code", "middle")
s.arrow(121, 242, 205, 274)
s.arrow(327, 242, 243, 274)
s.node(140, 276, 170, 44, "cosine", "cosine", "nt-out", tcls="pl-text")
s.both(225, 350, "คะแนน 0.35 (−1 ถึง 1)", "score 0.35 (−1 to 1)", "pl-label", "middle")
s.node(500, 60, 350, 44, "Query + Document", "Query + Document", "nt-bubble", tcls="pl-text")
s.arrow(675, 106, 675, 140)
s.box(540, 142, 270, 90, "ml-model", 12)
s.text(675, 182, "Cross-encoder", "ml-model-text", "middle")
s.text(675, 208, "Transformer", "ml-model-sub", "middle")
s.arrow(675, 234, 675, 274)
s.node(590, 276, 170, 44, "relevance", "relevance", "nt-out", tcls="pl-text")
s.both(675, 350, "คะแนน 3.97 (ไม่ใช่ความน่าจะเป็น)", "score 3.97 (not a probability)", "pl-label", "middle")
s.both(10, 420, "Query: What is taught on 19 October?  ·  Document: On 19 October 2026 the class covers dense retrieval and RAG.",
       "Query: What is taught on 19 October?  ·  Document: On 19 October 2026 the class covers dense retrieval and RAG.", "pl-note")
s.both(10, 446, "เร็ว: vector ของเอกสารคำนวณเก็บไว้ก่อนได้", "Fast: document vectors can be stored in advance", "ml-ok")
s.both(460, 446, "ช้ากว่า: ต้องรันใหม่ทุกคู่ แต่เห็นคำทั้งสองข้างพร้อมกัน", "Slower: runs per pair, but sees both texts together", "sw-warn-text")
s.save("l12-bi-cross.svg", 462)

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

# ---------------------------------------------------------------- 10. reranking cannot recover a missed document
s = Svg(900, "A reranker only sees what the retriever returns: the correct document is ranked 120th, outside the top 50, so the reranker never receives it.")
levels = [(10, 840, "100,000 chunk", "100,000 chunks"), (110, 640, "Retriever → top 50", "Retriever → top 50"),
          (210, 440, "Reranker → top 5", "Reranker → top 5"), (310, 240, "LLM", "LLM")]
for i, (y, w, th, en) in enumerate(levels):
    x = 30 + (840 - w) / 2
    s.box(x, y, w, 70, ["nt-band-a", "nt-band-b", "nt-band-a", "nt-out"][i], 12)
    s.both(450, y + 42, th, en, "pl-label", "middle")
    if i < 3:
        s.arrow(450, y + 72, 450, y + 98)
s.chip(632, 150, "correct doc: rank 120", "sw-chip-warn", "pl-chip-text")
s.out.append('<path d="M760 168 L760 200" class="pl-line"/>')
s.both(760, 226, "✗ ไม่ติด top 50", "✗ not in the top 50", "ml-neg", "middle")
s.both(760, 252, "reranker ไม่เคยเห็น", "the reranker never sees it", "ml-neg", "middle")
s.both(30, 414, "reranker เรียงใหม่ได้เฉพาะสิ่งที่ retriever ส่งมา ของที่หลุดตั้งแต่ขั้นค้น ต้องแก้ที่ retriever",
       "A reranker only reorders what the retriever returns; a missed document is a retrieval problem", "sw-warn-text")
s.save("l12-rerank-limit.svg", 432)

# ---------------------------------------------------------------- 11. context optimisation: filter, compress, parent document
s = Svg(900, "Three ways to give the LLM better context: filtering drops irrelevant chunks, compression keeps only the sentences that answer the question, and parent-document retrieval searches small chunks but returns the larger section around the match.")
cols = [("A. Filtering", "ตัด chunk ที่ไม่เกี่ยว", "drop irrelevant chunks"),
        ("B. Compression", "เก็บเฉพาะประโยคที่ตอบ", "keep only the answering part"),
        ("C. Parent document", "ค้นชิ้นเล็ก ส่งส่วนใหญ่", "search small, send the section")]
for i, (title, th, en) in enumerate(cols):
    x = 10 + i * 297
    s.box(x, 10, 285, 290, "nt-band-a" if i != 1 else "nt-band-b", 14)
    s.text(x + 16, 40, title, "pl-label")
    s.both(x + 16, 66, th, en, "pl-note")
# A: five chunks → two
x = 26
for k, c in enumerate("ABCDE"):
    keep = c in "AC"
    s.box(x + k * 50, 92, 40, 40, "pl-chip" if keep else "pl-chip-del", 8)
    s.text(x + k * 50 + 20, 118, c, "pl-chip-text" if keep else "pl-del", "middle")
s.arrow(152, 140, 152, 186)
for k, c in enumerate("AC"):
    s.box(102 + k * 60, 196, 40, 40, "pl-chip", 8)
    s.text(122 + k * 60, 222, c, "pl-chip-text", "middle")
s.both(26, 280, "ตอบแค่ A, C เท่านั้น", "only A and C answer it", "pl-note")
# B: a long chunk with one useful line → a short one
x = 323
s.box(x, 86, 253, 96, "ml-cell", 8)
for k in range(5):
    cls = "ml-bar-top" if k == 2 else "ml-bar"
    s.box(x + 14, 100 + k * 16, 225 - (k % 2) * 40, 8, cls, 3)
s.arrow(449, 186, 449, 214)
s.box(x + 40, 220, 173, 30, "ml-cell", 8)
s.box(x + 54, 231, 145, 8, "ml-bar-top", 3)
s.both(x, 280, "token น้อยลง เสียงรบกวนน้อยลง", "fewer tokens, less noise", "pl-note")
# C: small chunks A B C; search hits B; send the whole section
x = 620
for k, c in enumerate("ABC"):
    s.box(x + k * 82, 92, 74, 40, "pl-chip" if c == "B" else "ml-cell", 8)
    s.text(x + k * 82 + 37, 118, c, "pl-chip-text" if c == "B" else "pl-text", "middle")
s.both(x + 119, 158, "ค้นเจอ chunk B", "search matches chunk B", "pl-note", "middle")
s.arrow(x + 119, 166, x + 119, 192)
s.box(x, 198, 238, 40, "nt-out", 8)
s.both(x + 119, 224, "ส่ง A + B + C ให้ LLM", "send A + B + C to the LLM", "pl-text", "middle")
s.both(x, 280, "ได้บริบทรอบ ๆ ครบ", "keeps the context around it", "pl-note")
s.both(10, 330, "เป้าหมายไม่ใช่ข้อมูลมากที่สุด แต่เป็นหลักฐานที่เกี่ยวข้องและพอสำหรับการตอบ",
       "The goal is not the most information, but enough relevant evidence", "ml-ok")
s.save("l12-context-opt.svg", 348)

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
