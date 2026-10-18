"""Draws the lesson map of lesson 12 of the international NLP course (Gemini API and RAG): the
one question followed through its parts (lesson 12: four; lesson 13: five): what each part adds and what our question gets.
SVG, inlined into the page; ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/l12_map.py courses/nlp/images

Real results (computed in course/.venv): all-MiniLM-L6-v2 puts fact 7 first for "When is the final
exam?" (0.89, then fact 2 at 0.68), so Recall@2 = 1 and MRR = 1; for "What is taught on 19 October?"
the bi-encoder has fact 4 4th (0.347) and cross-encoder/ms-marco-MiniLM-L6-v2 moves it to 1st (3.974).
Part titles are the lesson's front matter `parts:` titles, word for word.

Uses the nt-*, pl-*, ml-*, sw-* and hk-* classes in templates/page.css.
"""

import os
import sys
import unicodedata
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp/images"


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


# One question followed through the six parts: what each part adds, and what our question gets.
def tw(t, fs):  # rough text width: Latin 0.58 em, Thai combining marks take no width
    return sum(0 if unicodedata.category(c) == "Mn" else fs * 0.58 for c in t)


def lesson_map(name, question, title, rows):
    s = Svg(1180, title)
    W = s.w
    s.box(W / 2 - 225, 10, 450, 50, "ml-cell", rx=25)
    s.text(W / 2, 42, question, "pl-text", "middle")
    s.both(20, 92, "แต่ละส่วนเพิ่มอะไร", "What each part adds", "nt-head")
    s.both(810, 92, "คำถามของเราได้อะไร", "What our question gets", "nt-head")
    y = 106
    for tth, ten, dth, den, rth, ren in rows:
        bad = "✗" in ren
        s.box(20, y, W - 40, 46, "sw-warn-box" if bad else "ml-cell", rx=12)
        for lang, t, d in (("th", tth, dth), ("en", ten, den)):  # the note follows its title, so place it per language
            attr = ' lang="en"' if lang == "en" else ""
            s.raw(f'<g data-only="{lang}"{attr}>')
            s.raw(f'<text x="40" y="{y + 30}" class="nt-task">{escape(t)}</text>')
            s.raw(f'<text x="{40 + tw(t, 19) + 18:g}" y="{y + 30}" class="hk-desc">{escape(d)}</text>')
            s.raw("</g>")
        s.both(810, y + 30, rth, ren, "ml-neg" if bad else "ml-ok")
        y += 54
    s.save(name, y + 2)


# lesson 12: one question through four parts
lesson_map("l12-map-lesson.svg", "When is the final exam of 2190519?",
           "Lesson map: one question, When is the final exam of 2190519?, followed through four parts. "
           "1 The problem: asked directly, Gemini has no date or makes one up. 2 Call an LLM: sent from Python, still no date. "
           "3 Look it up first (RAG): fact 7 goes into the prompt and the answer is Monday 30 November 2026 [fact 7]. "
           "4 Measure it: search put fact 7 first, and the answer is scored for faithfulness, relevance and correctness.", [
    ("1 ปัญหา", "1 The problem", "ถาม Gemini ตรง ๆ", "Ask Gemini directly",
     "ไม่รู้ หรือแต่งวันที่ขึ้นมา ✗", "no date, or a made-up one ✗"),
    ("2 เรียก LLM จากโค้ด", "2 Call an LLM", "ส่งคำถามจาก Python", "Send the question from Python",
     "ยังไม่ได้วันที่ ✗", "still no date ✗"),
    ("3 ค้นก่อนตอบ (RAG)", "3 Look it up first (RAG)", "หา fact 7 แล้วใส่ใน prompt", "Find fact 7, put it in the prompt",
     "30 November 2026 [fact 7] ✓", "30 November 2026 [fact 7] ✓"),
    ("4 วัดผล", "4 Measure it", "ให้คะแนนการค้นและคำตอบ", "Score the search and the answer",
     "fact 7 อันดับ 1 คำตอบยึดเอกสาร ✓", "fact 7 1st, a grounded answer ✓"),
])

# lesson 13 (advanced RAG): one question through five parts. Real results: the search ranks fact 4 4th (0.347);
# the cross-encoder gives it 3.974 and the other three below 0; three rewritten questions each rank fact 4 2nd.
lesson_map("l13-map-lesson.svg", "What is taught on 19 October?",
           "Lesson map: one question, What is taught on 19 October?, followed through five parts. "
           "1 The problem: the search ranks fact 4, the answer, 4th, so with the top 2 it never reaches the LLM. "
           "2 Rerank: reading the question with each fact moves fact 4 from 4th to 1st. "
           "3 Search better: words and meaning together, and rewritten questions, put fact 4 in the top 2. "
           "4 Better context: keep only facts the reranker scores above 0: 1 fact instead of 4. "
           "5 Sum up and build your own: a better RAG of your own.", [
    ("1 ปัญหา", "1 The problem", "ค้น 7 fact ส่ง 2 อันดับแรก", "Search 7 facts, send the top 2",
     "fact 4 อันดับ 4: ไม่ถูกส่ง ✗", "fact 4 is 4th: never sent ✗"),
    ("2 เรียงใหม่ (rerank)", "2 Rerank", "อ่านคำถามคู่กับแต่ละ fact", "Read the question with each fact",
     "fact 4 จากอันดับ 4 ขึ้นอันดับ 1 ✓", "fact 4 goes from 4th to 1st ✓"),
    ("3 ค้นให้ดีขึ้น", "3 Search better", "คำ + ความหมาย ถามใหม่", "Words + meaning, better questions",
     "fact 4 ติด top 2 ตั้งแต่ขั้นค้น ✓", "fact 4 in the top 2 from search ✓"),
    ("4 บริบทที่ดีขึ้น", "4 Better context", "ส่งเฉพาะ fact ที่ตอบได้", "Send only what answers",
     "1 fact แทน 4 ✓", "1 fact instead of 4 ✓"),
    ("5 สรุป แล้วสร้างเอง", "5 Sum up and build your own", "ข้อมูลและคำถามของเราเอง", "Your own facts and questions",
     "RAG ที่ดีขึ้นของเราเอง ✓", "a better RAG of your own ✓"),
])


# ---------------------------------------------------------------- the 7 course facts (projector copy of the data card)
FACTS = [
    "2190519 Natural Language Processing meets on Mondays, 13:00-16:00, in building EN100, room 501.",
    "The midterm exam was on Monday 21 September 2026, 13:00-16:00.",
    "There is no class on Monday 12 October 2026 because of the long weekend.",
    "On 19 October 2026 the class covers dense retrieval and RAG.",
    "On 26 October 2026 the class covers workflows and LLM agents.",
    "On 2 November 2026 the class covers named entity recognition (NER).",
    "The final exam is on Monday 30 November 2026, 13:00-16:00.",
]
ASKED = {4: "← What is taught on 19 October?", 7: "← When is the final exam?"}
s = Svg(1180, "The 7 course facts. Fact 7 answers 'When is the final exam?'; fact 4 answers 'What is taught on 19 October?'.")
for k, text in enumerate(FACTS, start=1):
    y = 10 + (k - 1) * 52
    s.box(10, y, 1160, 44, "sw-chip-warn" if k in ASKED else "ml-cell", 8)
    s.text(26, y + 29, f"fact {k}", "nt-task")
    s.text(116, y + 29, text, "pl-text")
    if k in ASKED:
        s.text(780, y + 29, ASKED[k], "ml-ok")
s.save("l12-facts.svg", 372)
