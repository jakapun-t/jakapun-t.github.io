"""Draws the pictures of lesson 14 of the international NLP course (workflows and LLM agents): SVG, inlined into
the page; ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/nlp_l14_figures.py courses/nlp/images

Real numbers (computed in course/.venv on 2026-10-19):
- search_course = all-MiniLM-L6-v2 over the 7 course facts: "How many days are left until the final exam?" → fact 7
  (0.693), fact 2 (0.509); "final exam date" → fact 7 (0.830). 26 Oct → 30 Nov 2026 = 35 days; → 2 Nov = 7 days.
- Tokens (OpenAI o200k tokenizer, as an estimate for Gemini): system prompt 32, the 3 tool schemas 220 (83 + 42 + 94),
  question 10; the four calls of the running question send 262, 307, 325, 358 tokens (1,252 in, 94 out).
- exam-study-plan SKILL.md: name + description 41 tokens, whole file 144.
- Run B in l14-eval is a real run of Qwen3-0.6B (transformers chat template with the three tools): it called
  days_between("2023-10-01", "2023-11-01") → 31 and answered "There are 31 days left until the final exam."
Published numbers are cited in the lesson text (Anthropic, OpenAI, LangChain, Manus, Chroma, arXiv 2609.00006).

Uses the nt-*, pl-*, sw-*, ml-* and dg-* classes in templates/page.css.
"""

import math
import os
import sys
import unicodedata
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp/images"
FS = 19
W = 1180


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

    def code(self, x, y, s, anchor="start", bold=False):
        w = ' font-weight="600"' if bold else ""
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="dg-code" text-anchor="{anchor}" xml:space="preserve"{w}>{escape(s)}</text>')

    def box(self, x, y, w, h, cls, rx=12):
        self.out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}"/>')

    def line(self, x1, y1, x2, y2, dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="pl-line"{dash}/>')

    def path(self, d, dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="{d}" class="pl-line"{dash}/>')

    def head(self, x1, y1, x2, y2):
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 10 * math.cos(a - 0.55), y2 - 10 * math.sin(a - 0.55))
        p2 = (x2 - 10 * math.cos(a + 0.55), y2 - 10 * math.sin(a + 0.55))
        self.out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2:g} {y2:g} L{p2[0]:.1f} {p2[1]:.1f}" class="pl-line"/>')

    def arrow(self, x1, y1, x2, y2, dashed=False):
        self.line(x1, y1, x2, y2, dashed)
        self.head(x1, y1, x2, y2)

    def num(self, x, y, n):
        self.out.append(f'<circle cx="{x:g}" cy="{y:g}" r="13" class="pl-dot"/>')
        self.text(x, y + 5, str(n), "pl-num", "middle")

    def llm(self, x, y, w, h, th="LLM", en="LLM", sub=None):
        self.box(x, y, w, h, "ml-model", 12)
        cy = y + h / 2 + (0 if sub else 6)
        self.both(x + w / 2, cy, th, en, "ml-model-text", "middle")
        if sub:
            self.both(x + w / 2, cy + 22, sub[0], sub[1], "ml-model-sub", "middle")

    def chip(self, x, y, w, h, th, en, cls="ml-cell", tcls="hk-desc"):
        self.box(x, y, w, h, cls, 8)
        self.both(x + w / 2, y + h / 2 + 6, th, en, tcls, "middle")

    def raw(self, s):
        self.out.append(s)

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


def bubble(s, text, y=8, w=None, x=None):
    w = w or width(text) + 60
    x = W / 2 - w / 2 if x is None else x
    s.box(x, y, w, 46, "nt-bubble", 23)
    s.text(x + w / 2, y + 30, text, "pl-text", "middle")


def bubble2(s, th, en, y=8, w=700):
    s.box(W / 2 - w / 2, y, w, 46, "nt-bubble", 23)
    s.both(W / 2, y + 30, th, en, "pl-text", "middle")


Q = "How many days are left until the final exam?"

# ---------------------------------------------------------------- 1. hook: RAG workflow vs agent
s = Svg(W, "The question 'How many days are left until the final exam?', asked on Monday 26 October. Left, the RAG workflow: "
           "it searches the 7 facts and keeps the top 2 (fact 7, final exam on Monday 30 November, cosine 0.693; fact 2, the "
           "midterm, 0.509), builds a prompt and lets Gemini write; no fact gives today's date and no step counts days, so the "
           "model can only guess. Right, an agent: the LLM calls search_course('final exam date') → fact 7, get_today() → "
           "2026-10-26, days_between('2026-10-26', '2026-11-30') → 35, then answers 35 days.")
bubble2(s, "“เหลืออีกกี่วันถึงสอบปลายภาค” (ถามวันจันทร์ที่ 26 ต.ค.)", "“How many days are left until the final exam?” (asked Mon 26 Oct)", w=720)
s.box(20, 72, 560, 388, "sw-warn-box", 14)
s.both(40, 104, "✗ RAG แบบ workflow (ขั้นตอนตายตัว)", "✗ RAG workflow (fixed steps)", "pl-label")
s.box(40, 120, 520, 124, "ml-cell", 10)
s.num(62, 144, 1)
s.both(84, 150, "ค้นข้อเท็จจริง 7 ข้อ เก็บ 2 อันดับแรก", "Search the 7 facts, keep the top 2", "pl-text")
s.box(58, 164, 484, 32, "sw-chip-warn", 8)
s.both(70, 186, "fact 7 · สอบปลายภาค จันทร์ 30 พ.ย. · cos 0.693", "fact 7 · final exam, Mon 30 Nov · cos 0.693", "pl-note")
s.box(58, 202, 484, 32, "ml-cell", 8)
s.both(70, 224, "fact 2 · สอบกลางภาค 21 ก.ย. · cos 0.509", "fact 2 · midterm, 21 Sep · cos 0.509", "pl-note")
s.box(40, 256, 520, 44, "ml-cell", 10)
s.num(62, 278, 2)
s.both(84, 284, "prompt = คำถาม + fact 2 ข้อนั้น", "Prompt = question + those 2 facts", "pl-text")
s.box(40, 312, 520, 44, "ml-cell", 10)
s.num(62, 334, 3)
s.both(84, 340, "Gemini เขียนคำตอบ", "Gemini writes the answer", "pl-text")
s.both(40, 396, "✗ ไม่มี fact ไหนบอกวันที่ของวันนี้", "✗ No fact gives today's date,", "ml-neg")
s.both(40, 426, "และไม่มีขั้นไหนนับวัน → โมเดลต้องเดา", "and no step counts days → it guesses", "ml-neg")
s.box(600, 72, 560, 388, "nt-band-a", 14)
s.both(620, 104, "✓ Agent: LLM เลือกแต่ละขั้นเอง", "✓ Agent: the LLM picks each step", "pl-label")
s.llm(620, 124, 92, 224, "LLM", "LLM")
CALLS = [('search_course("final exam date")', "→ fact 7: จันทร์ 30 พฤศจิกายน 2026", "→ fact 7: Monday 30 November 2026"),
         ("get_today()", "→ 2026-10-26", "→ 2026-10-26"),
         ('days_between("2026-10-26", "2026-11-30")', "→ 35", "→ 35")]
for k, (c, rth, ren) in enumerate(CALLS):
    y = 124 + k * 82
    s.box(736, y, 404, 64, "ml-cell", 10)
    s.num(752, y + 20, k + 1)
    s.code(772, y + 26, c)
    s.both(772, y + 52, rth, ren, "ml-ok" if k == 2 else "pl-note")
    s.arrow(712, y + 32, 734, y + 32)
s.box(620, 362, 520, 46, "nt-out", 10)
s.both(880, 392, "“35 วัน: จันทร์ 30 พ.ย. 13:00–16:00”", "“35 days: Mon 30 Nov, 13:00–16:00”", "pl-text", "middle")
s.both(620, 440, "✓ LLM เลือก tool 3 ตัว โค้ดของเราเป็นคนนับ", "✓ the LLM chose 3 tools; our code counted", "ml-ok")
s.save("l14-hook.svg", 476)

# ---------------------------------------------------------------- 2. lesson map
def tw(t, fs):
    return sum(0 if unicodedata.category(c) == "Mn" else fs * 0.58 for c in t)


ROWS = [
    ("1 ปัญหา", "1 The problem", "จากการตอบ สู่การลงมือทำ", "From answering to doing", "“เหลืออีกกี่วัน”: RAG นับไม่ได้ ✗", "“How many days?”: RAG can't count ✗"),
    ("2 Workflow", "2 Workflows", "โค้ดกำหนดเส้นทาง", "Code fixes the path", "route คำถามเรื่องวัน → 35 วัน ✓", "date questions routed → 35 days ✓"),
    ("3 Tools, MCP, skills, memory", "3 Tools, MCP, skills, memory", "ให้มือกับโมเดล", "Give the model hands", "search_course, get_today, days_between ✓", "search_course, get_today, days_between ✓"),
    ("4 ReAct", "4 Reasoning: ReAct", "คิด → ลงมือ → สังเกต", "Think → act → observe", "tool call 3 ครั้ง → 35 วัน ✓", "3 tool calls → 35 days ✓"),
    ("5 หลาย agent", "5 Many agents", "แบ่งงานใหญ่", "Split a big job", "แผนอ่านหนังสือ: ผู้จัดการ + worker ✓", "study plan: a manager + workers ✓"),
    ("6 Context engineering", "6 Context engineering", "เลือกสิ่งที่โมเดลเห็น", "Choose what it sees", "262 → 358 token งานยาวใช้ไฟล์ ✓", "262 → 358 tokens; files for long jobs ✓"),
    ("7 Agent harness", "7 The agent harness", "โค้ดรอบตัวโมเดล", "The code around the model", "ถามก่อนแตะปฏิทิน ✓", "asks before touching the calendar ✓"),
    ("8 ประเมินผล", "8 Evaluate it", "ตรวจคำตอบและเส้นทาง", "Check answer and path", "จับ “31 วัน” จากวันที่แต่งขึ้นได้ ✓", "catches “31 days” from made-up dates ✓"),
]
s = Svg(W, "Lesson map: one course assistant followed through eight parts. The problem (RAG can't count the days left), workflows "
           "(code fixes the path; a router can count days if someone foresaw it), tools, MCP, skills and memory (three tools), "
           "ReAct (three tool calls give 35 days), many agents (a manager and workers for the study plan), context engineering "
           "(262 to 358 tokens; files for long jobs), the agent harness (asks before touching the calendar) and evaluation "
           "(catches an answer of 31 days built on made-up dates).")
bubble(s, "How many days are left until the final exam? → plan my 5 weeks", w=680)
s.both(20, 92, "แต่ละส่วนเพิ่มอะไร", "What each part adds", "nt-head")
s.both(700, 92, "ผู้ช่วยของเราได้อะไร", "What our assistant gets", "nt-head")
y = 106
for tth, ten, dth, den, rth, ren in ROWS:
    bad = "✗" in ren
    s.box(20, y, W - 40, 46, "sw-warn-box" if bad else "ml-cell", 12)
    for lang, t, d in (("th", tth, dth), ("en", ten, den)):
        attr = ' lang="en"' if lang == "en" else ""
        s.raw(f'<g data-only="{lang}"{attr}>')
        s.raw(f'<text x="40" y="{y + 30}" class="nt-task">{escape(t)}</text>')
        s.raw(f'<text x="{40 + tw(t, 19) + 18:g}" y="{y + 30}" class="hk-desc">{escape(d)}</text>')
        s.raw("</g>")
    s.both(700, y + 30, rth, ren, "ml-neg" if bad else "ml-ok")
    y += 54
s.save("l14-map-lesson.svg", y + 2)

# ---------------------------------------------------------------- 3. workflow vs agent
s = Svg(W, "Left, a workflow: the path is written in code in advance, question → search the facts → build the prompt → the LLM "
           "writes → answer, the same steps for every question: predictable, cheap and easy to test, but it only handles what "
           "its author foresaw. Right, an agent: the LLM calls a tool, reads the result and decides again, in a loop, and stops "
           "when it answers without a tool call: it handles tasks nobody foresaw, but makes more calls and mistakes can pile up.")
s.box(20, 20, 560, 440, "ml-cell", 14)
s.both(40, 52, "Workflow: โค้ดกำหนดเส้นทาง", "Workflow: code fixes the path", "pl-label")
STEPS = [("คำถาม", "question", "nt-bubble"), ("1 ค้นข้อเท็จจริง", "1 search the facts", "ml-cell-b"),
         ("2 สร้าง prompt", "2 build the prompt", "ml-cell-b"), ("3 LLM เขียน", "3 the LLM writes", "ml-model"), ("คำตอบ", "answer", "nt-out")]
for k, (th, en, cls) in enumerate(STEPS):
    y = 72 + k * 62
    s.box(40, y, 250, 44, cls, 10)
    s.both(165, y + 28, th, en, "ml-model-text" if cls == "ml-model" else "pl-text", "middle")
    if k:
        s.arrow(165, y - 18, 165, y - 2)
s.path("M308 116 Q326 116 326 134 L326 276 Q326 294 308 294")
s.both(340, 192, "เขียนไว้ในโค้ด", "written in code,", "pl-text")
s.both(340, 218, "ล่วงหน้า", "in advance", "pl-text")
s.both(340, 252, "ขั้นเดิมกับทุกคำถาม", "same steps for", "pl-note")
s.both(340, 276, "", "every question", "pl-note")
s.both(40, 412, "✓ คาดเดาได้ ถูก ทดสอบง่าย", "✓ predictable, cheap, easy to test", "ml-ok")
s.both(40, 442, "✗ รับได้แค่สิ่งที่คนเขียนคาดไว้", "✗ only what its author foresaw", "ml-neg")
s.box(600, 20, 560, 440, "nt-band-a", 14)
s.both(620, 52, "Agent: LLM ตัดสินใจขั้นถัดไป", "Agent: the LLM decides the next step", "pl-label")
s.box(780, 72, 200, 44, "nt-bubble", 22)
s.both(880, 100, "คำถาม / งาน", "question / job", "pl-text", "middle")
s.arrow(880, 118, 880, 152)
s.llm(800, 156, 160, 70, "LLM", "LLM", ("เลือกขั้นถัดไป", "picks the next step"))
s.box(1020, 156, 120, 70, "pl-chip", 10)
s.both(1080, 197, "tools", "tools", "pl-chip-text", "middle")
s.path("M962 172 Q990 150 1018 172")
s.head(990, 158, 1018, 172)
s.both(990, 144, "เรียก tool", "call a tool", "pl-note", "middle")
s.path("M1018 212 Q990 236 962 212")
s.head(990, 228, 962, 212)
s.both(990, 254, "ผลลัพธ์", "result", "pl-note", "middle")
s.arrow(880, 228, 880, 300)
s.both(868, 274, "ไม่มี tool call = เสร็จ", "no tool call = done", "pl-note", "end")
s.box(800, 304, 160, 44, "nt-out", 10)
s.both(880, 332, "คำตอบ", "answer", "pl-text", "middle")
s.both(620, 412, "✓ รับงานที่ไม่มีใครคาดไว้ได้", "✓ handles tasks nobody foresaw", "ml-ok")
s.both(620, 442, "✗ เรียกมากขึ้น แพงขึ้น ความผิดพลาดสะสม", "✗ more calls, more cost; errors pile up", "ml-neg")
s.save("l14-workflow-agent.svg", 476)

# ---------------------------------------------------------------- 4. five workflow patterns
s = Svg(W, "Five workflow patterns applied to the course assistant. 1 Prompt chaining: an LLM drafts the study plan, code checks "
           "it has 5 weeks, another LLM call translates it into Thai. 2 Routing: a router sends a date question to count days, a "
           "topic question to search, a grades question to the grades table. 3 Parallelization: several LLM calls at once, "
           "sectioning (summarise lessons 10 to 15) or voting (ask 3 times). 4 Orchestrator-workers: an LLM splits the job at run "
           "time, one worker per topic, then merges. 5 Evaluator-optimizer: one LLM writes a practice question, another grades it "
           "and gives feedback until it passes. Start with the simplest one that works.")
PH = 236
PX = [(20, 20), (404, 20), (788, 20), (212, 268), (596, 268)]
TITLES = [("1 · Prompt chaining", "แบ่งเป็นขั้น มีด่านตรวจ", "steps, with a check between"),
          ("2 · Routing", "แยกประเภท แล้วส่งต่อ", "classify, then send on"),
          ("3 · Parallelization", "หลายครั้งพร้อมกัน", "several calls at once"),
          ("4 · Orchestrator-workers", "LLM แบ่งงานตอนรัน", "the LLM splits it at run time"),
          ("5 · Evaluator-optimizer", "เขียน → ให้คะแนน → แก้", "write → grade → rewrite")]
EX = [("ร่างแผน → โค้ดตรวจ 5 สัปดาห์", "draft plan → code checks 5 weeks", "→ แปลเป็นภาษาไทย", "→ translate into Thai"),
      ("คำถามเรื่องวัน → get_today", "date question → get_today", "+ days_between", "+ days_between"),
      ("sectioning: สรุป L10–L15 พร้อมกัน", "sectioning: L10–L15 at once", "voting: ถาม 3 ครั้ง เอาเสียงข้างมาก", "voting: ask 3 times, majority"),
      ("worker หนึ่งตัวต่อหนึ่งหัวข้อ", "one worker per topic", "จำนวนตัดสินตอนรัน", "the number is decided at run time"),
      ("ข้อสอบฝึกเรื่อง NER", "a practice question on NER", "วนจนผ่านเกณฑ์", "loop until it passes")]
for k, ((x, y), (t, sth, sen), (e1t, e1e, e2t, e2e)) in enumerate(zip(PX, TITLES, EX)):
    s.box(x, y, 372, PH, "ml-cell", 14)
    s.text(x + 16, y + 30, t, "pl-label")
    s.both(x + 16, y + 58, sth, sen, "pl-note")
    s.both(x + 16, y + 200, e1t, e1e, "hk-desc")
    s.both(x + 16, y + 224, e2t, e2e, "hk-desc")
# 1 chaining: draft → check → Thai
x, y = PX[0]
s.llm(x + 14, y + 86, 104, 42, "LLM ร่าง", "LLM draft")
s.arrow(x + 120, y + 107, x + 134, y + 107)
s.box(x + 136, y + 86, 104, 42, "nt-out", 8)
s.both(x + 188, y + 113, "โค้ดตรวจ", "code check", "hk-desc", "middle")
s.arrow(x + 242, y + 107, x + 256, y + 107)
s.llm(x + 258, y + 86, 100, 42, "LLM แปล", "LLM Thai")
s.both(x + 188, y + 158, "ไม่ผ่าน → หยุด", "fails → stop", "pl-note", "middle")
# 2 routing: question → router → 3 branches
x, y = PX[1]
s.box(x + 12, y + 100, 88, 38, "nt-bubble", 19)
s.both(x + 56, y + 125, "คำถาม", "question", "hk-desc", "middle")
s.arrow(x + 102, y + 119, x + 114, y + 119)
s.llm(x + 116, y + 99, 78, 40, "router", "router")
for j, (th, en) in enumerate([("วันที่ → นับวัน", "date → count"), ("หัวข้อ → ค้น", "topic → search"), ("คะแนน → ตาราง", "grades → table")]):
    yy = y + 70 + j * 36
    s.arrow(x + 196, y + 119, x + 212, yy + 15)
    s.chip(x + 214, yy, 144, 30, th, en, "ml-cell-b" if j == 0 else "ml-cell")
# 3 parallel: task → 3 LLM → merge
x, y = PX[2]
s.box(x + 12, y + 100, 72, 38, "nt-bubble", 19)
s.both(x + 48, y + 125, "งาน", "task", "hk-desc", "middle")
for j in range(3):
    yy = y + 70 + j * 36
    s.arrow(x + 86, y + 119, x + 116, yy + 15)
    s.llm(x + 118, yy, 96, 30, "LLM", "LLM")
    s.arrow(x + 216, yy + 15, x + 246, y + 119)
s.box(x + 248, y + 99, 108, 40, "nt-out", 8)
s.both(x + 302, y + 125, "รวมผล", "merge", "hk-desc", "middle")
# 4 orchestrator → workers → merge
x, y = PX[3]
s.llm(x + 12, y + 94, 136, 50, "orchestrator", "orchestrator")
for j, t in enumerate(["RAG", "agents", "NER"]):
    yy = y + 70 + j * 36
    s.arrow(x + 150, y + 119, x + 172, yy + 15)
    s.box(x + 174, yy, 86, 30, "ml-cell-b", 8)
    s.text(x + 217, yy + 21, t, "hk-desc", "middle")
    s.arrow(x + 262, yy + 15, x + 284, y + 119)
s.llm(x + 286, y + 99, 72, 40, "รวม", "merge")
# 5 evaluator ⇄ optimizer
x, y = PX[4]
s.llm(x + 14, y + 98, 116, 46, "LLM เขียน", "LLM writes")
s.llm(x + 202, y + 98, 116, 46, "LLM ตัดสิน", "LLM grades")
s.path(f"M{x + 132} {y + 108} Q{x + 166} {y + 86} {x + 200} {y + 108}")
s.head(x + 180, y + 93, x + 200, y + 108)
s.both(x + 166, y + 82, "ร่าง", "draft", "pl-note", "middle")
s.path(f"M{x + 200} {y + 134} Q{x + 166} {y + 156} {x + 132} {y + 134}")
s.head(x + 152, y + 149, x + 132, y + 134)
s.both(x + 166, y + 176, "feedback", "feedback", "pl-note", "middle")
s.arrow(x + 320, y + 121, x + 352, y + 121)
s.text(x + 338, y + 108, "✓", "ml-ok", "middle")
s.both(20, 540, "ทั้ง 5 แบบเก็บเส้นทางไว้ในโค้ด: เริ่มจากแบบที่ง่ายที่สุดที่ใช้ได้ แล้วค่อยเพิ่มขั้นเมื่อวัดได้ว่าช่วย",
       "All five keep the path in code. Start with the simplest one that works; add steps only when they measurably help.", "pl-text")
s.save("l14-patterns.svg", 556)

# ---------------------------------------------------------------- 5. LangGraph routing workflow
s = Svg(W, "The routing workflow as a LangGraph graph: START → route(state) → count_days or search → END. The state is a typed "
           "dict with question and answer. Real results: 'How many days are left until the final exam?' → count_days → 35 days "
           "(30 November 2026); 'How many days until the NER class?' → count_days → 7 days (2 November 2026); 'When is the NER "
           "class?' → search → fact 6; 'How long until the final exam?' means the same as the first question but has no 'how "
           "many days', so it goes to search and returns fact 7 as text, not a count.")
s.box(20, 20, 700, 196, "ml-cell", 14)
s.box(36, 96, 76, 40, "ml-model", 20)
s.text(74, 122, "START", "ml-model-text", "middle")
s.arrow(114, 116, 146, 116)
s.box(148, 92, 150, 48, "nt-out", 10)
s.code(223, 121, "route(state)", "middle")
s.both(223, 164, "โค้ด 1 บรรทัด:", "one line of code:", "pl-note", "middle")
s.both(223, 188, "มี “how many days” ไหม", "“how many days” in it?", "pl-note", "middle")
s.arrow(300, 106, 386, 66)
s.both(330, 70, "ใช่", "yes", "pl-note")
s.arrow(300, 126, 386, 166)
s.both(348, 132, "ไม่", "no", "pl-note")
s.box(388, 44, 150, 44, "ml-cell-b", 10)
s.code(463, 71, "count_days", "middle")
s.box(388, 144, 150, 44, "ml-cell-b", 10)
s.code(463, 171, "search", "middle")
s.arrow(540, 66, 614, 106)
s.arrow(540, 166, 614, 126)
s.box(616, 96, 76, 40, "ml-model", 20)
s.text(654, 122, "END", "ml-model-text", "middle")
s.box(740, 20, 420, 196, "nt-band-a", 14)
s.both(760, 52, "state (TypedDict) ที่ส่งต่อกัน", "the state passed along (TypedDict)", "pl-label")
s.code(760, 88, "class State(TypedDict):")
s.code(780, 112, "question: str")
s.code(780, 136, "answer: str")
s.both(760, 172, "node คืนเฉพาะ key ที่เปลี่ยน", "a node returns only what it changes,", "pl-note")
s.code(760, 198, '{"answer": "35 days (30 November 2026)"}')
s.both(20, 252, "ผลจริงของ 4 คำถาม", "Real results for 4 questions", "nt-head")
RES = [("How many days are left until the final exam?", "count_days", "35 วัน (30 พ.ย. 2026) ✓", "35 days (30 Nov 2026) ✓", True),
       ("How many days until the NER class?", "count_days", "7 วัน (2 พ.ย. 2026) ✓", "7 days (2 Nov 2026) ✓", True),
       ("When is the NER class?", "search", "fact 6 ✓", "fact 6 ✓", True),
       ("How long until the final exam?", "search", "ได้ fact 7 เป็นข้อความ ไม่นับวัน ✗", "fact 7 as text, no count ✗", False)]
for k, (q, node, rth, ren, ok) in enumerate(RES):
    y = 266 + k * 50
    s.box(20, y, W - 40, 42, "ml-cell" if ok else "sw-warn-box", 10)
    s.text(36, y + 28, q, "pl-text")
    s.box(560, y + 6, 130, 30, "ml-cell-b", 8)
    s.code(625, y + 26, node, "middle")
    s.both(710, y + 28, rth, ren, "ml-ok" if ok else "ml-neg")
s.save("l14-langgraph.svg", 474)

# ---------------------------------------------------------------- 6. agent components
s = Svg(W, "What an agent is made of: an LLM core that reasons and plans, in a loop of perceive, plan, act, reflect; around it "
           "tools (search_course, get_today, days_between), MCP connections (Google Calendar, GitHub), memory (short-term: this "
           "chat; long-term: saved files, such as 'prefers Thai answers') and skills (exam-study-plan/SKILL.md).")
PARTS = [(20, 20, "Tools", "Tools", "ฟังก์ชันที่ agent เรียกได้", "functions the agent can call", "search_course · get_today · days_between"),
         (760, 20, "MCP connections", "MCP connections", "ปลั๊กมาตรฐานสู่บริการภายนอก", "a standard plug to outside services", "Google Calendar · GitHub"),
         (20, 286, "Memory", "Memory", "สั้น: แชตนี้ · ยาว: เก็บไว้ข้างนอก", "short: this chat · long: saved outside", "“prefers Thai answers”"),
         (760, 286, "Skills", "Skills", "วิธีทำงาน โหลดเมื่อจำเป็น", "know-how, loaded when needed", "exam-study-plan/SKILL.md")]
for x, y, th, en, dth, den, ex in PARTS:
    s.box(x, y, 400, 150, "nt-band-a", 14)
    s.both(x + 20, y + 34, th, en, "pl-label")
    s.both(x + 20, y + 68, dth, den, "pl-text")
    s.box(x + 20, y + 88, 360, 40, "ml-cell", 8)
    s.code(x + 34, y + 113, ex)
s.llm(470, 150, 240, 96, "LLM แกนกลาง", "LLM core", ("ให้เหตุผลและวางแผน", "reasons and plans"))
for x1, y1, x2, y2 in ((470, 170, 420, 130), (710, 170, 760, 130), (470, 226, 420, 296), (710, 226, 760, 296)):
    s.line(x1, y1, x2, y2)
s.box(462, 262, 256, 96, "ml-cell", 14)
s.both(590, 292, "ลูปของทุก agent", "the loop of every agent", "pl-note", "middle")
s.both(590, 318, "1 รับรู้ → 2 วางแผน →", "1 perceive → 2 plan →", "pl-text", "middle")
s.both(590, 344, "3 ลงมือ → 4 ทบทวน ↺", "3 act → 4 reflect ↺", "pl-text", "middle")
s.both(590, 64, "agent = LLM + ส่วนประกอบรอบตัว", "agent = an LLM + the parts around it", "pl-label", "middle")
s.save("l14-components.svg", 456)

# ---------------------------------------------------------------- 7. why tools
s = Svg(W, "Four limits of an LLM alone and the tool that fixes each. No clock: it guesses today's date; get_today() → 2026-10-26. "
           "No exact arithmetic: it writes numbers token by token; a calculator gives sqrt(1764) × 7 = 294. No private or new "
           "data: it never saw our 7 facts; search_course → fact 7. No hands: it can only write text; add_calendar_event adds the "
           "event. The first three fetch data; the last takes an action, so ask first.")
TILES = [("1 · ไม่มีนาฬิกา", "1 · No clock", ("เดาวันที่ของวันนี้", "", "guesses today's date", ""), "get_today()", "2026-10-26", False),
         ("2 · คำนวณไม่แม่น", "2 · No exact maths", ("เขียนตัวเลขทีละ token", "จึงพลาดได้", "writes numbers token by", "token, so it can slip"), "calculator(...)", "√1764 × 7 = 294", False),
         ("3 · ไม่มีข้อมูลใหม่", "3 · No new data", ("ไม่เคยเห็นข้อเท็จจริง", "7 ข้อของเรา", "never saw our", "7 course facts"), "search_course(...)", "fact 7", False),
         ("4 · ลงมือไม่ได้", "4 · No hands", ("เขียนได้แค่ข้อความ", "", "can only write text", ""), "add_calendar_event(...)", "event added", True)]
for k, (tth, ten, (n1t, n2t, n1e, n2e), call, res, act) in enumerate(TILES):
    x = 20 + k * 290
    s.box(x, 20, 280, 330, "sw-warn-box" if False else "ml-cell", 14)
    s.both(x + 18, 54, tth, ten, "pl-label")
    s.both(x + 18, 90, "LLM อย่างเดียว", "LLM alone", "pl-note")
    s.both(x + 18, 118, "✗ " + n1t, "✗ " + n1e, "ml-neg")
    if n1e and (n2t or n2e):
        s.both(x + 36, 144, n2t, n2e, "ml-neg")
    s.both(x + 18, 190, "มี tool", "with a tool", "pl-note")
    s.box(x + 18, 202, 244, 34, "pl-chip", 8)
    s.code(x + 30, 224, call)
    s.both(x + 18, 266, "✓ " + res, "✓ " + res, "ml-ok")
    s.box(x + 18, 290, 244, 40, "sw-chip-warn" if act else "ml-cell-b", 20)
    s.both(x + 140, 316, "ลงมือทำ: ถามก่อน" if act else "ดึงข้อมูล", "take an action: ask first" if act else "fetch data", "hk-desc", "middle")
s.save("l14-why-tools.svg", 366)

# ---------------------------------------------------------------- 8. tool schema
s = Svg(W, "How @tool turns a Python function into the schema the model reads: 1 the function name days_between becomes the "
           "tool's name; 2 the docstring 'Count the days from one date to another.' becomes the description; 3 the type hints "
           "and the Args lines become the parameters start and end, each a string with a description. Below, a tool whose "
           "docstring says only 'Do math.' gives the model nothing to decide with.")
s.box(20, 20, 540, 250, "ml-cell", 14)
s.both(40, 50, "สิ่งที่เราเขียน (Python)", "What we write (Python)", "pl-label")
CODE = ["@tool", "def days_between(start: str, end: str) -> int:", '    """Count the days from one date to another.', "",
        "    Args:", "        start: the first date, YYYY-MM-DD", "        end: the last date, YYYY-MM-DD", '    """']
HL = {1: 1, 2: 2, 5: 3, 6: 3}
for k, ln in enumerate(CODE):
    y = 82 + k * 22
    if k in HL:
        s.box(48, y - 16, 500, 22, "dg-hl-col", 4)
    s.code(56, y, ln)
for k, n in ((1, 1), (2, 2), (5, 3)):
    s.num(30, 76 + k * 22, n)
s.box(620, 20, 540, 250, "nt-band-a", 14)
s.both(640, 50, "สิ่งที่โมเดลอ่าน (JSON schema)", "What the model reads (JSON schema)", "pl-label")
JS = ['{"name": "days_between",', ' "description":', '   "Count the days from one date to another.",', ' "parameters": {',
      '   "start": {"type": "string",', '             "description": "the first date, YYYY-MM-DD"},', '   "end": {"type": "string", ...}}}']
JHL = {0: 1, 2: 2, 4: 3, 5: 3, 6: 3}
for k, ln in enumerate(JS):
    y = 82 + k * 24
    if k in JHL:
        s.box(648, y - 16, 504, 22, "dg-hl-col", 4)
    s.code(656, y, ln)
for k, n in ((0, 1), (2, 2), (4, 3)):
    s.num(630, 76 + k * 24, n)
s.arrow(566, 140, 614, 140)
s.both(20, 302, "1 ชื่อฟังก์ชัน → name · 2 docstring → description (โมเดลอ่านเพื่อเลือก tool) · 3 type hint + Args → parameters",
       "1 function name → name · 2 docstring → description (read to choose a tool) · 3 type hints + Args → parameters", "pl-text")
s.box(20, 322, 1140, 110, "sw-warn-box", 14)
s.code(40, 356, '@tool')
s.code(40, 378, 'def multiply(a: int, b: int) -> int:')
s.code(40, 400, '    """Do math."""')
s.arrow(360, 378, 420, 378)
s.code(432, 378, '"description": "Do math."')
s.both(700, 366, "✗ คณิตแบบไหน กับอะไร เมื่อไร", "✗ which maths, on what, when?", "ml-neg")
s.both(700, 396, "โมเดลเลือกระหว่างมันกับเครื่องคิดเลขไม่ได้", "the model can't tell it from a calculator", "pl-note")
s.save("l14-tool-schema.svg", 448)

# ---------------------------------------------------------------- 9. function call
s = Svg(W, "How a model calls a tool. 1 The model reads the system part with the three tool schemas (220 tokens) and the user's "
           "question. 2 At the start of its reply it can write text ('The final exam is in about...') or a function call as JSON: "
           "name search_course, args query 'final exam date'. 3 Our code runs search_course and gets fact 7. 4 The result goes "
           "back as a function response and the model continues: get_today, days_between, then the answer.")
s.box(20, 20, 340, 340, "ml-cell", 14)
s.num(44, 50, 1)
s.both(66, 56, "สิ่งที่โมเดลอ่าน", "What the model reads", "pl-label")
s.box(36, 76, 308, 150, "nt-band-a", 10)
s.code(50, 100, "system: tools =")
for k, t in enumerate(["search_course(query)", "get_today()", "days_between(start, end)"]):
    s.code(70, 126 + k * 24, t)
s.both(50, 210, "schema JSON 220 token", "220 tokens of JSON schema", "pl-note")
s.box(36, 238, 308, 104, "ml-cell", 10)
s.code(50, 262, "user:")
s.text(50, 290, "How many days are left", "pl-text")
s.text(50, 316, "until the final exam?", "pl-text")
s.arrow(362, 190, 392, 190)
s.box(396, 20, 400, 340, "ml-cell", 14)
s.num(420, 50, 2)
s.both(442, 56, "โมเดลเขียนต่อ: แบบไหน", "The model continues: which?", "pl-label")
s.box(412, 76, 368, 84, "ml-cell", 10)
s.both(428, 102, "ทาง A: ข้อความ", "Option A: text", "pl-note")
s.text(428, 134, "“The final exam is in about…”", "pl-text")
s.text(762, 134, "✗", "ml-neg", "end")
s.box(412, 176, 368, 166, "nt-out", 10)
s.both(428, 202, "ทาง B: function call (JSON)", "Option B: a function call (JSON)", "pl-note")
s.code(428, 232, '{"name": "search_course",')
s.code(428, 256, ' "args": {"query":')
s.code(428, 280, '          "final exam date"}}')
s.both(428, 320, "✓ ต้องใช้ข้อมูลที่มันไม่มี", "✓ it needs data it doesn't have", "ml-ok")
s.arrow(798, 260, 828, 260)
s.box(832, 20, 328, 340, "nt-band-a", 14)
s.num(856, 50, 3)
s.both(878, 56, "โค้ดของเรารัน", "Our code runs it", "pl-label")
s.box(848, 76, 296, 40, "pl-chip", 8)
s.code(860, 101, 'search_course("final exam date")')
s.arrow(996, 118, 996, 138)
s.box(848, 140, 296, 64, "ml-cell", 8)
s.code(860, 166, "[fact 7] The final exam is")
s.code(860, 190, "on Monday 30 November 2026 …")
s.num(856, 236, 4)
s.both(878, 242, "ส่งผลกลับเป็น", "Sent back as a", "pl-text")
s.both(878, 268, "function response", "function response", "pl-text")
s.both(856, 304, "แล้วโมเดลเรียก get_today,", "then it calls get_today,", "pl-note")
s.both(856, 330, "days_between แล้วจึงตอบ", "days_between, then answers", "pl-note")
s.both(20, 394, "โมเดลไม่ได้รันอะไรเอง: มันเขียน JSON แล้ว harness (โค้ดของเรา) เป็นคนรัน",
       "The model runs nothing: it writes the JSON, and the harness (our code) runs it.", "pl-text")
s.save("l14-function-call.svg", 410)

# ---------------------------------------------------------------- 10. tool loop in LangGraph + message trace
s = Svg(W, "Left: the agent graph, START → agent ⇄ tools → END; tools_condition sends a reply with tool calls to the tools node "
           "and a reply without one to END. Right: the messages one run adds to the state for our question: the question; a call "
           "to search_course('final exam date') and its result, fact 7; get_today() → 2026-10-26; days_between('2026-10-26', "
           "'2026-11-30') → 35; and the answer, 35 days. The tool results are real outputs of our tools.")
s.box(20, 20, 380, 420, "ml-cell", 14)
s.both(40, 52, "กราฟ (LangGraph)", "The graph (LangGraph)", "pl-label")
s.box(150, 72, 100, 36, "ml-model", 18)
s.text(200, 96, "START", "ml-model-text", "middle")
s.arrow(200, 110, 200, 140)
s.llm(130, 144, 140, 56, "agent", "agent", ("เรียก LLM", "calls the LLM"))
s.box(130, 276, 140, 50, "pl-chip", 10)
s.text(200, 307, "tools", "pl-chip-text", "middle")
s.path("M150 202 L150 274")
s.head(150, 240, 150, 274)
s.path("M250 274 L250 202")
s.head(250, 236, 250, 202)
s.both(40, 236, "มี tool call", "tool call?", "pl-note")
s.both(40, 260, "→ tools", "→ tools", "pl-note")
s.both(262, 246, "ผล → agent", "result → agent", "pl-note")
s.arrow(272, 172, 330, 172)
s.box(316, 154, 72, 36, "ml-model", 18)
s.text(352, 178, "END", "ml-model-text", "middle")
s.both(40, 360, "ไม่มี tool call → END", "no tool call → END", "pl-note")
s.code(40, 392, "tools_condition")
s.both(40, 420, "ตัดสินทางแยกให้", "decides the branch", "pl-note")
s.box(420, 20, 740, 420, "nt-band-a", 14)
s.both(440, 52, "state[\"messages\"] หลังรัน 1 ครั้ง (add_messages ต่อท้าย)", "state[\"messages\"] after one run (add_messages appends)", "pl-label")
MSGS = [("human", Q), ("ai", 'tool call: search_course(query="final exam date")'),
        ("tool", "[fact 7] The final exam is on Monday 30 November 2026, 13:00-16:00."),
        ("ai", "tool call: get_today()"), ("tool", "2026-10-26"),
        ("ai", 'tool call: days_between(start="2026-10-26", end="2026-11-30")'), ("tool", "35"),
        ("ai", "There are 35 days left until the final exam (Mon 30 Nov) [fact 7].")]
for k, (role, txt) in enumerate(MSGS):
    y = 70 + k * 42
    cls = {"human": "nt-bubble", "ai": "ml-cell", "tool": "pl-chip"}[role]
    s.box(436, y, 64, 32, cls, 8)
    s.text(468, y + 21, role, "hk-desc", "middle")
    s.box(508, y, 636, 32, "nt-out" if k == 7 else "ml-cell", 8)
    s.code(520, y + 21, txt, bold=(role == "tool"))
s.both(440, 428, "ผลของ tool เป็นผลจริงจาก tool ของเรา · LLM ถูกเรียก 4 ครั้ง", "tool results: real outputs of our tools · the LLM is called 4 times", "pl-note")
s.save("l14-tool-loop.svg", 456)

# ---------------------------------------------------------------- 11. MCP
s = Svg(W, "Before MCP: three apps (Claude Desktop, Cursor, Gemini CLI) each build their own connector to three services "
           "(Google Calendar, GitHub, a database): 9 connectors to build and maintain. With MCP: each app is an MCP host with one "
           "MCP client per server, each service ships one MCP server, and they all speak the same protocol: 3 + 3 pieces, and any "
           "app can use any server.")
APPS = ["Claude Desktop", "Cursor", "Gemini CLI"]
SVCS = ["Google Calendar", "GitHub", "Database"]
s.box(20, 20, 560, 380, "sw-warn-box", 14)
s.both(40, 52, "✗ ก่อนมี MCP: ต่อกันเองทุกคู่", "✗ Before MCP: every pair wired by hand", "pl-label")
for k, a in enumerate(APPS):
    s.chip(40, 90 + k * 90, 170, 44, a, a, "ml-cell", "pl-text")
for k, v in enumerate(SVCS):
    s.chip(390, 90 + k * 90, 170, 44, v, v, "ml-cell", "pl-text")
for i in range(3):
    for j in range(3):
        s.line(212, 112 + i * 90, 388, 112 + j * 90)
s.both(40, 372, "✗ 3 × 3 = ตัวเชื่อมต่อ 9 ตัวที่ต้องสร้างและดูแล", "✗ 3 × 3 = 9 connectors to build and maintain", "ml-neg")
s.box(600, 20, 560, 380, "nt-band-a", 14)
s.both(620, 52, "✓ มี MCP: ปลั๊กมาตรฐานเดียว", "✓ With MCP: one standard plug", "pl-label")
for k, a in enumerate(APPS):
    y = 90 + k * 90
    s.box(616, y, 152, 44, "ml-cell", 8)
    s.text(692, y + 28, a, "hk-desc", "middle")
    s.box(772, y + 8, 64, 28, "ml-cell-b", 6)
    s.text(804, y + 27, "client", "ml-i", "middle")
    s.line(838, y + 22, 868, y + 22)
s.box(868, 84, 44, 236, "ml-model", 10)
s.raw('<text x="890" y="202" class="ml-model-text" text-anchor="middle" transform="rotate(-90 890 202)">MCP</text>')
for k, v in enumerate(SVCS):
    y = 90 + k * 90
    s.line(912, y + 22, 940, y + 22)
    s.box(940, y + 8, 60, 28, "ml-cell-b", 6)
    s.text(970, y + 27, "server", "ml-i", "middle")
    s.box(1004, y, 148, 44, "ml-cell", 8)
    s.text(1078, y + 28, v, "hk-desc", "middle")
s.both(620, 344, "host = แอป · client = 1 ตัวต่อ server · server = tool ของบริการ", "host = the app · client = 1 per server · server = a service's tools", "pl-note")
s.both(620, 372, "✓ แอปไหนก็ใช้ server ไหนก็ได้", "✓ any app can use any server", "ml-ok")
s.save("l14-mcp.svg", 416)

# ---------------------------------------------------------------- 12. memory
s = Svg(W, "Short-term memory: the model remembers nothing between calls, so the app sends the whole message list with every "
           "call: 'Hello! My name is Alex.', the reply, and 'Do you remember my name?' → 'Yes, I do! Your name is Alex.' It ends "
           "with the session and is limited by the context window. Long-term memory: facts worth keeping are written to a store "
           "(a vector database, a key-value store or a file), such as 'prefers Thai answers' and 'exam reminders added', and "
           "loaded into the prompt of a session next week.")
s.box(20, 20, 560, 420, "nt-band-a", 14)
s.both(40, 52, "ความจำระยะสั้น = context", "Short-term memory = the context", "pl-label")
s.both(40, 80, "ส่ง list ข้อความทั้งหมดไปทุกครั้ง", "the whole message list goes with every call", "pl-note")
CH = [("human", "Hello! My name is Alex. What's yours?"), ("ai", "Hello, Alex! It's a pleasure to meet you…"), ("human", "Do you remember my name?")]
for k, (r, t) in enumerate(CH):
    y = 100 + k * 46
    s.box(40, y, 78, 34, "nt-bubble" if r == "human" else "ml-cell", 8)
    s.text(79, y + 23, r, "hk-desc", "middle")
    s.box(126, y, 434, 34, "ml-cell", 8)
    s.code(138, y + 22, t)
s.path("M300 240 L300 270")
s.head(300, 250, 300, 270)
s.both(316, 262, "ส่งทั้ง 3 ข้อความ", "all 3 messages sent", "pl-note")
s.llm(220, 274, 160, 48, "LLM", "LLM")
s.arrow(300, 324, 300, 344)
s.box(40, 348, 520, 34, "nt-out", 8)
s.code(56, 370, "ai: Yes, I do! Your name is Alex.")
s.both(40, 418, "หายเมื่อจบรอบ · จำกัดด้วย context window", "ends with the session · limited by the window", "ml-neg")
s.box(600, 20, 560, 420, "ml-cell", 14)
s.both(620, 52, "ความจำระยะยาว = เก็บไว้ข้างนอก", "Long-term memory = saved outside", "pl-label")
s.chip(620, 84, 196, 44, "รอบที่ 1 (26 ต.ค.)", "session 1 (26 Oct)", "nt-bubble", "hk-desc")
s.arrow(818, 106, 846, 106)
s.both(832, 80, "เขียน", "write", "pl-note", "middle")
s.box(850, 72, 290, 180, "nt-band-a", 12)
s.both(864, 100, "ที่เก็บ: vector DB, ไฟล์", "store: vector DB, a file", "pl-note")
for k, t in enumerate(["prefers Thai answers", "exam reminders added", "weak topic: HMMs"]):
    s.box(864, 116 + k * 42, 262, 34, "ml-cell", 8)
    s.code(876, 138 + k * 42, t)
s.chip(620, 380 - 76, 196, 44, "รอบที่ 2 (สัปดาห์หน้า)", "session 2 (next week)", "nt-bubble", "hk-desc")
s.arrow(995, 254, 995, 300)
s.both(1007, 284, "อ่านกลับ", "read back", "pl-note")
s.box(850, 304, 290, 44, "nt-out", 8)
s.both(864, 332, "เติมลงใน prompt รอบใหม่", "added to the new prompt", "pl-text")
s.arrow(848, 326, 818, 326)
s.both(620, 418, "✓ อยู่ข้ามรอบการใช้งาน", "✓ survives across sessions", "ml-ok")
s.save("l14-memory.svg", 456)

# ---------------------------------------------------------------- 13. skills: progressive disclosure
s = Svg(W, "Progressive disclosure of skills. 1 Discovery, at startup: only each skill's name and description sit in the "
           "context, about 41 tokens for exam-study-plan. 2 Activation, when a request matches: the full SKILL.md is read, 144 "
           "tokens: find the exam date, count the days, find the topics, spread them over the weeks, write a table, ask before "
           "the calendar. 3 Execution, only if a step needs them: scripts and reference files. Without skills the agent picks "
           "tool calls on the fly; with skills it chooses a skill and follows it, using tools.")
COLS3 = [(20, "1 · Discovery", "ตอนเริ่ม", "at startup"), (410, "2 · Activation", "เมื่องานตรงกับคำอธิบาย", "when a request matches"),
         (800, "3 · Execution", "เฉพาะเมื่อขั้นไหนต้องใช้", "only if a step needs it")]
for x, t, sth, sen in COLS3:
    s.box(x, 20, 360, 344, "ml-cell", 14)
    s.text(x + 18, 52, t, "pl-label")
    s.both(x + 18, 78, sth, sen, "pl-note")
SK = [("exam-study-plan:", "Make a week-by-week study", "plan for an exam…", True), ("pdf-processing:", "Extract PDF text, fill", "forms, merge files…", False),
      ("grade-report:", "Summarise a student's", "scores by topic…", False)]
for k, (n, d1, d2, hi) in enumerate(SK):
    y = 94 + k * 72
    s.box(36, y, 328, 64, "sw-chip-warn" if hi else "ml-cell", 8)
    s.code(48, y + 20, n, bold=True)
    s.code(48, y + 40, d1)
    s.code(48, y + 58, d2)
s.both(36, 334, "≈ 41 token ต่อ skill (ของเรา)", "≈ 41 tokens per skill (ours)", "ml-ok")
s.arrow(372, 190, 404, 190)
SKL = ["---", "name: exam-study-plan", "description: Make a week-by-…", "---", "1. Find the exam date.", "2. get_today, days_between.",
       "3. Find the topics.", "4. Spread them over the weeks.", "5. Write a table.", "6. Ask before the calendar."]
s.box(426, 92, 328, 228, "nt-band-a", 8)
for k, ln in enumerate(SKL):
    s.code(438, 112 + k * 21, ln)
s.both(426, 344, "SKILL.md ทั้งไฟล์ ≈ 144 token", "the whole SKILL.md ≈ 144 tokens", "ml-ok")
s.arrow(762, 190, 794, 190)
TREE = ["exam-study-plan/", "├── SKILL.md", "├── scripts/", "│   └── make_table.py", "├── references/", "│   └── past_exams.md", "└── assets/",
        "    └── plan_template.md"]
for k, ln in enumerate(TREE):
    s.code(822, 112 + k * 24, ln, bold=(k == 0))
s.both(816, 324, "เปิดเฉพาะเมื่อขั้นไหนต้องใช้", "opened only when a step needs it", "pl-note")
s.box(20, 380, 560, 44, "sw-warn-box", 10)
s.both(36, 408, "ไม่มี skill: ผู้ใช้ → agent → เลือก tool ไปเรื่อย ๆ", "Without: user → agent → tool calls on the fly", "pl-text")
s.box(600, 380, 560, 44, "nt-band-a", 10)
s.both(616, 408, "มี skill: ผู้ใช้ → agent → เลือก skill → ใช้ tool", "With: user → agent → a skill → its tool calls", "pl-text")
s.save("l14-skills.svg", 440)

# ---------------------------------------------------------------- 14. system prompt vs AGENTS.md
s = Svg(W, "Left: a system prompt lives in one app's code and is sent as the first message of every call: 'You are the course "
           "assistant for 2190519. Cite the fact you used. Never guess a date: use the tools.' Right: AGENTS.md lives in the "
           "project folder, and Codex, Claude Code, Gemini CLI and other compatible agents read it at the start of every "
           "session; keep it a short map that links to deeper docs, not one huge manual the agent can't search.")
s.box(20, 20, 520, 420, "ml-cell", 14)
s.both(40, 52, "1 · System prompt (ในโค้ด)", "1 · System prompt (in the code)", "pl-label")
s.box(40, 72, 480, 130, "nt-band-a", 10)
for k, ln in enumerate(['SYSTEM = (', '  "You are the course assistant for 2190519. "', '  "Cite the fact you used, like [fact 7]. "',
                        '  "Never guess a date: use the tools.")']):
    s.code(54, 98 + k * 26, ln)
s.arrow(280, 206, 280, 246)
s.both(292, 232, "ข้อความแรกของทุกครั้งที่เรียก", "first message of every call", "pl-note")
s.llm(200, 250, 160, 50, "LLM", "LLM")
s.both(40, 352, "✓ ง่าย อยู่กับแอป", "✓ simple, part of the app", "ml-ok")
s.both(40, 382, "✗ ใช้ได้แอปเดียว ต้องแก้โค้ด", "✗ one app only; change = code change", "ml-neg")
s.box(560, 20, 600, 420, "nt-band-a", 14)
s.both(580, 52, "2 · AGENTS.md (ในโฟลเดอร์โปรเจกต์)", "2 · AGENTS.md (in the project folder)", "pl-label")
TREE = ["course-assistant/", "├── AGENTS.md", "├── docs/", "│   ├── facts.md", "│   └── testing.md", "└── tools.py"]
for k, ln in enumerate(TREE):
    s.code(580, 90 + k * 24, ln, bold=(k == 1))
s.box(830, 70, 314, 176, "ml-cell", 10)
for k, ln in enumerate(["# Course assistant", "- Cite the fact: [fact 7]", "- Thai in → Thai out", "- Never guess dates: use tools",
                        "- Tests: see docs/testing.md"]):
    s.code(844, 96 + k * 30, ln, bold=(k == 0))
s.both(580, 274, "อ่านตอนเริ่มทุกรอบ:", "read at every session's start by", "pl-note")
for k, a in enumerate(["Codex", "Claude Code", "Gemini CLI", "…"]):
    s.chip(580 + k * 140, 290, 128, 36, a, a, "ml-cell", "hk-desc")
s.both(580, 368, "✓ แผนที่สั้น ๆ ชี้ไปยังเอกสารที่ละเอียด", "✓ a short map that points to deeper docs", "ml-ok")
s.both(580, 400, "✗ คู่มือยาวพันบรรทัด: agent หาสิ่งสำคัญไม่เจอ", "✗ a 1,000-line manual: it can't find what matters", "ml-neg")
s.save("l14-behaviour.svg", 456)

# ---------------------------------------------------------------- 15. planning
s = Svg(W, "Planning the study-plan job: the goal 'a 5-week study plan + review sessions in my calendar' breaks into four "
           "subtasks: 1 find the topics with search_course for each class date (facts 4, 5 and 6); 2 count the weeks with "
           "days_between (35 days = 5 weeks); 3 write the plan as a table; 4 add 5 review sessions with add_calendar_event, "
           "after asking. Below, chain-of-thought is one straight line of steps; tree of thoughts tries several branches, "
           "drops a bad one and keeps the best.")
s.box(310, 16, 560, 50, "ml-model", 25)
s.both(590, 48, "เป้าหมาย: แผนอ่าน 5 สัปดาห์ + รอบทบทวนในปฏิทิน", "Goal: a 5-week study plan + review sessions in my calendar", "ml-model-text", "middle")
SUB = [("1 หาหัวข้อ", "1 Find the topics", "search_course ×3", "→ fact 4, 5, 6", "→ facts 4, 5, 6"),
       ("2 นับสัปดาห์", "2 Count the weeks", "days_between", "→ 35 วัน = 5 สัปดาห์", "→ 35 days = 5 weeks"),
       ("3 เขียนแผน", "3 Write the plan", "(LLM writes)", "ตาราง: สัปดาห์ หัวข้อ งาน", "table: week, topics, task"),
       ("4 เพิ่ม 5 รอบทบทวน", "4 Add 5 reviews", "add_calendar_event ×5", "ถามนิสิตก่อน", "ask the student first")]
for k, (th, en, c, rth, ren) in enumerate(SUB):
    x = 20 + k * 290
    s.arrow(590, 68, x + 140, 100)
    s.box(x, 102, 280, 132, "sw-warn-box" if k == 3 else "nt-band-a", 12)
    s.both(x + 16, 132, th, en, "pl-label")
    s.box(x + 16, 146, 248, 32, "pl-chip", 8)
    s.code(x + 28, 167, c)
    s.both(x + 16, 212, rth, ren, "pl-text")
s.box(20, 254, 560, 170, "ml-cell", 14)
s.both(40, 284, "Chain-of-thought: ทางเดียว", "Chain-of-thought: one line", "pl-label")
for k in range(5):
    x = 70 + k * 110
    s.raw(f'<circle cx="{x}" cy="342" r="14" class="ml-model"/>')
    if k:
        s.arrow(x - 96, 342, x - 16, 342)
s.both(40, 400, "คิดทีละขั้น แล้วลงมือ", "think step by step, then act", "pl-note")
s.box(600, 254, 560, 170, "ml-cell", 14)
s.both(620, 284, "Tree of thoughts: หลายทาง เก็บทางที่ดีที่สุด", "Tree of thoughts: try several, keep the best", "pl-label")
s.raw('<circle cx="650" cy="344" r="14" class="ml-model"/>')
for k, (dy, ok) in enumerate(((-34, None), (0, True), (34, False))):
    s.arrow(666, 344, 760, 344 + dy)
    s.raw(f'<circle cx="776" cy="{344 + dy}" r="14" class="{"ml-model-done" if ok else "ml-model"}"/>')
    if ok is True:
        s.arrow(792, 344, 880, 344)
        s.raw('<circle cx="896" cy="344" r="14" class="ml-model-done"/>')
        s.both(920, 350, "✓ ทางที่ดีที่สุด", "✓ the best branch", "ml-ok")
    if ok is False:
        s.text(800, 384, "✗", "ml-neg")
s.both(620, 408, "ประเมินแต่ละกิ่ง ย้อนกลับได้ แต่เรียก LLM มากขึ้น", "judge each branch, back up if needed; more LLM calls", "pl-note")
s.save("l14-planning.svg", 440)

# ---------------------------------------------------------------- 16. CoT vs ReAct
s = Svg(W, "Left, chain-of-thought alone (a made-up example): with no tools it reasons from memory, 'final exams are usually in "
           "mid-December', 'today is probably early November', and answers about 42 days, wrong. Right, ReAct: Thought 'I need "
           "the exam date', Action search_course('final exam date'), Observation fact 7, 30 November 2026; Thought 'now today's "
           "date', Action get_today(), Observation 2026-10-26; Thought 'count the days', Action days_between, Observation 35; "
           "answer 35 days.")
s.box(20, 20, 400, 420, "sw-warn-box", 14)
s.both(40, 52, "✗ CoT อย่างเดียว (ตัวอย่างสมมติ)", "✗ CoT alone (made-up example)", "pl-label")
COT_TH = ["Thought: สอบปลายภาคมักอยู่", "กลางเดือนธันวาคม", "Thought: วันนี้น่าจะต้น พ.ย.", "Thought: ห่างกันราว 6 สัปดาห์"]
COT_EN = ["Thought: final exams are usually", "in mid-December.", "Thought: today is probably early", "November.", "Thought: so about 6 weeks."]
for k, t in enumerate(COT_TH):
    s.raw(f'<text x="40" y="{92 + k * 30}" class="pl-text" data-only="th">{escape(t)}</text>')
for k, t in enumerate(COT_EN):
    s.raw(f'<text x="40" y="{92 + k * 30}" class="pl-text" data-only="en" lang="en">{escape(t)}</text>')
s.box(40, 254, 360, 44, "ml-cell", 8)
s.both(56, 282, "คำตอบ: ราว 42 วัน", "Answer: about 42 days", "pl-text")
s.both(40, 344, "✗ ใช้แค่สิ่งที่อยู่ในน้ำหนักของโมเดล", "✗ only what is in its weights", "ml-neg")
s.both(40, 374, "ไม่เห็นวันนี้ ไม่เห็นข้อเท็จจริงของเรา", "can't see today or our facts", "pl-note")
s.box(440, 20, 720, 420, "nt-band-a", 14)
s.both(460, 52, "✓ ReAct: Thought → Action → Observation", "✓ ReAct: Thought → Action → Observation", "pl-label")
RE = [("Thought", "ต้องรู้วันสอบก่อน", "I need the exam date first.", False), ("Action", 'search_course("final exam date")', None, True),
      ("Observation", "[fact 7] … Monday 30 November 2026", None, True),
      ("Thought", "ต่อไปคือวันที่ของวันนี้", "Now today's date.", False), ("Action", "get_today()", None, True), ("Observation", "2026-10-26", None, True),
      ("Thought", "นับวัน", "Count the days.", False), ("Action", 'days_between("2026-10-26", "2026-11-30")', None, True), ("Observation", "35", None, True)]
for k, (lab, a, b, code) in enumerate(RE):
    y = 76 + k * 34
    cls = {"Thought": "ml-cell", "Action": "pl-chip", "Observation": "nt-bubble"}[lab]
    s.box(460, y, 130, 28, cls, 6)
    s.text(525, y + 20, lab, "hk-desc", "middle")
    if code:
        s.code(604, y + 19, a, bold=(lab == "Observation"))
    else:
        s.both(604, y + 21, a, b, "hk-desc")
s.box(460, 386, 680, 40, "nt-out", 8)
s.both(476, 412, "คำตอบ: 35 วัน (จันทร์ 30 พ.ย.) ✓ อิงข้อมูลจริงทุกขั้น", "Answer: 35 days (Mon 30 Nov) ✓ every step grounded in real data", "ml-ok")
s.save("l14-react.svg", 456)

# ---------------------------------------------------------------- 17. Reflexion + thinking models
s = Svg(W, "Left, Reflexion: the actor writes a study plan with 6 weeks; the evaluator says only 35 days are left; "
           "self-reflection writes a lesson, 'I counted from 19 October; call get_today first', which is kept in memory and added "
           "to the next try, which plans 5 weeks. The weights never change. Right: ReAct is a prompted, visible loop of Thought, "
           "Action and Observation lines; today's models think in hidden reasoning, emit native function calls and can think "
           "again between calls, so the loop lives in the harness.")
s.box(20, 20, 640, 420, "ml-cell", 14)
s.both(40, 52, "Reflexion: เรียนจากความผิดด้วยคำพูด", "Reflexion: learn from a failure in words", "pl-label")
s.llm(40, 80, 170, 56, "Actor", "Actor", ("ทำงาน", "does the task"))
s.box(250, 84, 380, 48, "sw-chip-warn", 8)
s.both(266, 114, "ลองครั้งที่ 1: แผน 6 สัปดาห์", "try 1: a 6-week plan", "pl-text")
s.arrow(212, 108, 248, 108)
s.arrow(440, 134, 440, 162)
s.llm(40, 166, 170, 56, "Evaluator", "Evaluator", ("ให้คะแนน", "scores it"))
s.box(250, 170, 380, 48, "ml-cell", 8)
s.both(266, 200, "✗ เหลือแค่ 35 วัน (5 สัปดาห์)", "✗ only 35 days (5 weeks) left", "ml-neg")
s.arrow(440, 220, 440, 248)
s.llm(40, 252, 170, 56, "Self-reflection", "Self-reflection", ("เขียนบทเรียน", "writes a lesson"))
s.box(250, 252, 380, 70, "nt-band-a", 8)
s.both(266, 280, "“ฉันนับจาก 19 ต.ค. ต้องเรียก", "“I counted from 19 Oct; call", "pl-text")
s.both(266, 306, "get_today ก่อน”", "get_today first.”", "pl-text")
s.arrow(440, 324, 440, 352)
s.box(250, 356, 380, 48, "nt-out", 8)
s.both(266, 386, "ลองครั้งที่ 2: แผน 5 สัปดาห์ ✓", "try 2: a 5-week plan ✓", "ml-ok")
s.box(40, 342, 170, 44, "nt-out", 8)
s.both(125, 370, "memory: บทเรียน", "memory: the lesson", "hk-desc", "middle")
s.arrow(248, 300, 190, 340)
s.arrow(212, 372, 248, 378)
s.both(40, 420, "น้ำหนักของโมเดลไม่เปลี่ยน", "the weights never change", "pl-note")
s.box(680, 20, 480, 420, "nt-band-a", 14)
s.both(700, 52, "ReAct กับโมเดล thinking ปัจจุบัน", "ReAct vs today's thinking models", "pl-label")
s.both(700, 86, "ReAct: สั่งด้วย prompt มองเห็นทุกบรรทัด", "ReAct: prompted, every line visible", "pl-note")
for k, t in enumerate(["Thought: …", "Action: search_course(…)", "Observation: …", "Thought: … → Answer"]):
    s.code(716, 112 + k * 24, t)
s.both(700, 236, "ปัจจุบัน: คิดภายใน แล้วเรียก tool โดยตรง", "Today: think inside, call tools natively", "pl-note")
FLOW = [("[thinking]", "ml-cell"), ("call", "pl-chip"), ("[thinking]", "ml-cell"), ("call", "pl-chip"), ("answer", "nt-out")]
x = 700
for k, (t, cls) in enumerate(FLOW):
    w = 96 if "think" in t else 62 if t == "call" else 80
    s.box(x, 256, w, 34, cls, 8)
    s.code(x + w / 2, 278, t, "middle")
    if k < len(FLOW) - 1:
        s.arrow(x + w + 2, 273, x + w + 12, 273)
    x += w + 14
s.both(700, 330, "ไม่มีลูปตายตัวในข้อความ", "no fixed loop in the text;", "pl-text")
s.both(700, 358, "ลูปอยู่ใน harness ที่รัน tool", "the loop lives in the harness", "pl-text")
s.both(700, 400, "(thinking มักซ่อนหรือสรุปให้ดู)", "(thinking is often hidden or summarised)", "pl-note")
s.save("l14-reflexion.svg", 456)

# ---------------------------------------------------------------- 18. one agent vs many
s = Svg(W, "Left: one agent researching AI agents reads every paper and note into one context window, which fills up. Right: "
           "a manager agent gives the research, analysis and writer agents each their own window; each returns a short summary "
           "(about 1,000 to 2,000 tokens). Anthropic's research system scored 90.2% higher than a single agent, at about 15 "
           "times the tokens of a chat.")
s.box(20, 20, 440, 420, "sw-warn-box", 14)
s.both(40, 52, "✗ agent ตัวเดียว window เดียว", "✗ One agent, one window", "pl-label")
s.box(60, 76, 140, 330, "ml-cell", 10)
for k in range(10):
    s.box(70, 86 + k * 30, 120, 24, "sw-chip-warn" if k < 8 else "ml-cell-b", 4)
    s.code(130, 103 + k * 30, f"paper {k + 1}" if k < 8 else "notes", "middle")
s.both(220, 120, "ทุกบทความ ทุกโน้ต", "every paper, every note", "pl-text")
s.both(220, 146, "อยู่ใน context เดียว", "in one context", "pl-text")
s.both(220, 330, "✗ window เต็ม", "✗ the window fills;", "ml-neg")
s.both(220, 358, "สิ่งสำคัญจมหาย", "what matters gets lost", "ml-neg")
s.box(480, 20, 680, 420, "nt-band-a", 14)
s.both(500, 52, "✓ ผู้จัดการ + worker แต่ละตัวมี window ของตัวเอง", "✓ A manager + workers, each with its own window", "pl-label")
s.llm(730, 72, 180, 56, "Manager", "Manager", ("แบ่งงาน รวมผล", "splits, merges"))
WK = [("Research", "ค้นและรวบรวม", "search, collect"), ("Analysis", "ดึงผล เปรียบเทียบ", "extract, compare"), ("Writer", "เขียนรายงาน", "write the report")]
for k, (t, th, en) in enumerate(WK):
    x = 500 + k * 220
    s.arrow(820, 130, x + 100, 178)
    s.llm(x, 180, 200, 50, t, t)
    s.box(x + 30, 240, 140, 90, "ml-cell", 8)
    for j in range(3):
        s.box(x + 40, 250 + j * 26, 120, 20, "ml-cell-b", 4)
    s.both(x + 100, 352, th, en, "pl-note", "middle")
s.both(500, 392, "แต่ละตัวส่งสรุปกลับ ≈ 1,000–2,000 token", "each returns a summary of ≈ 1,000–2,000 tokens", "pl-text")
s.both(500, 422, "✓ +90.2% เทียบ agent ตัวเดียว", "✓ +90.2% vs one agent", "ml-ok")
s.both(830, 422, "✗ token ≈ 15 เท่าของแชต", "✗ ≈ 15× a chat's tokens", "ml-neg")
s.save("l14-multi-agent.svg", 456)

# ---------------------------------------------------------------- 19. Generative Agents and ChatDev
s = Svg(W, "Left, Generative Agents (Stanford and Google, 2023): 25 agents in the town of Smallville. Each keeps a memory stream "
           "of observations; for each next step memories are scored on recency, importance and relevance and the top ones go "
           "into the prompt; reflections and day plans are stored as memories too. A Valentine's Day party spread from one "
           "agent and five came. Right, ChatDev (2023): agents play CEO, CTO, programmer, reviewer and tester along a chain of "
           "design, coding, testing and documentation.")
s.box(20, 20, 680, 420, "nt-band-a", 14)
s.both(40, 52, "Generative Agents: 25 ตัวใน Smallville", "Generative Agents: 25 agents in Smallville", "pl-label")
s.both(40, 80, "memory stream (ตัวอย่างความจำในแบบของงานวิจัย)", "memory stream (example memories in the paper's style)", "pl-note")
MEM = [("07:02", "Isabella plans a Valentine's Day party", True), ("08:15", "Klaus is reading about gentrification", False),
       ("09:30", "the cafe's coffee machine is broken", False), ("10:04", "Maria asked about the party at Hobbs Cafe", True),
       ("12:40", "Isabella invited Klaus to the party", True)]
for k, (t, m, hi) in enumerate(MEM):
    y = 94 + k * 38
    s.box(40, y, 420, 30, "sw-chip-warn" if hi else "ml-cell", 6)
    s.code(52, y + 20, t)
    s.code(110, y + 20, m)
s.box(476, 94, 208, 182, "ml-cell", 10)
s.both(490, 120, "ดึงความจำด้วยคะแนน", "retrieval score", "pl-label")
for k, (th, en) in enumerate([("ความใหม่", "recency"), ("+ ความสำคัญ", "+ importance"), ("+ ความเกี่ยวข้อง", "+ relevance")]):
    s.both(490, 150 + k * 28, th, en, "pl-text")
s.both(490, 250, "สูงสุด → เข้า prompt", "top ones → prompt", "ml-ok")
s.arrow(462, 180, 474, 180)
s.box(40, 296, 300, 70, "ml-cell", 10)
s.both(56, 324, "Reflection", "Reflection", "pl-label")
s.both(56, 352, "สรุประดับสูงจากความจำ", "higher-level conclusions", "pl-note")
s.box(360, 296, 324, 70, "ml-cell", 10)
s.both(376, 324, "Planning", "Planning", "pl-label")
s.both(376, 352, "แผนของวัน → รายชั่วโมง", "a day plan → hourly steps", "pl-note")
s.both(40, 414, "ข่าวปาร์ตี้แพร่จาก agent สู่ agent: มาตรงเวลา 5 ตัว", "the party news spread agent to agent: 5 came on time", "ml-ok")
s.box(720, 20, 440, 420, "ml-cell", 14)
s.both(740, 52, "ChatDev: บริษัทซอฟต์แวร์ของ agent", "ChatDev: a software company of agents", "pl-label")
ORG = [("CEO", 880, 76), ("CTO", 880, 144), ("Programmer", 750, 216), ("Reviewer", 1010, 216), ("Tester", 880, 288)]
for t, x, y in ORG:
    s.llm(x, y, 140, 44, t, t)
s.line(950, 120, 950, 144)
s.line(950, 188, 820, 216)
s.line(950, 188, 1080, 216)
s.path("M892 238 L1008 238", dashed=True)
s.line(820, 260, 950, 288)
s.line(1080, 260, 950, 288)
s.both(740, 362, "ออกแบบ → เขียนโค้ด → ทดสอบ → เอกสาร", "design → coding → testing → docs", "pl-text")
s.both(740, 394, "บทบาทตายตัว ลำดับตายตัว", "fixed roles, a fixed chain", "pl-note")
s.save("l14-generative.svg", 456)

# ---------------------------------------------------------------- 20. context growth
s = Svg(W, "Left, our question with real token counts per call (GPT tokenizer): call 1 sends 262 tokens (system prompt 32, the "
           "three tool schemas 220, question 10), call 2 307, call 3 325, call 4 358; 1,252 tokens read to write 94. Right, a "
           "long research job with example sizes: each web page the agent reads stays in the context, so after 10, 20, 30 and 40 "
           "steps the context holds about 50,000, 100,000, 150,000 and 200,000 tokens. Chroma found 18 models do worse as input "
           "grows: a focused input of about 300 tokens beat the full 113,000-token input that held the same answer.")
s.box(20, 20, 560, 420, "ml-cell", 14)
s.both(40, 52, "คำถามของเรา: token จริงต่อครั้งที่เรียก", "Our question: real tokens per call", "pl-label")
SEG = [(32, "nt-hub"), (220, "ml-bar"), (10, "ml-model")]
CALLSZ = [262, 307, 325, 358]
sc = 400 / 360
for k, tot in enumerate(CALLSZ):
    y = 84 + k * 56
    s.both(40, y + 24, f"ครั้งที่ {k + 1}", f"call {k + 1}", "pl-text")
    x = 120
    for v, cls in SEG:
        s.box(x, y + 4, v * sc, 30, cls, 2)
        x += v * sc
    if tot > 262:
        s.box(x, y + 4, (tot - 262) * sc, 30, "sw-chip-warn", 2)
    s.text(120 + tot * sc + 8, y + 26, str(tot), "pl-label")
s.box(40, 312, 16, 16, "nt-hub", 2)
s.both(62, 326, "system 32", "system 32", "pl-note")
s.box(160, 312, 16, 16, "ml-bar", 2)
s.both(182, 326, "tools 220", "tools 220", "pl-note")
s.box(300, 312, 16, 16, "ml-model", 2)
s.both(322, 326, "คำถาม 10", "question 10", "pl-note")
s.box(430, 312, 16, 16, "sw-chip-warn", 2)
s.both(452, 326, "call + ผล", "calls + results", "pl-note")
s.both(40, 380, "รวม: อ่าน 1,252 token เพื่อเขียน 94", "In total: 1,252 tokens read to write 94", "pl-text")
s.both(40, 410, "ทุกครั้งที่เรียก ส่งทุกอย่างไปใหม่", "every call resends everything", "pl-note")
s.box(600, 20, 560, 420, "sw-warn-box", 14)
s.both(620, 52, "งาน research ยาว ๆ (ขนาดสมมติ)", "A long research job (example sizes)", "pl-label")
s.line(660, 330, 1130, 330)
s.line(660, 330, 660, 80)
for k, v in enumerate([3, 50, 100, 150, 200]):
    x = 690 + k * 88
    h = v * 1.15
    s.box(x, 330 - h, 56, h, "ml-bar-top" if k == 4 else "ml-bar", 3)
    s.text(x + 28, 322 - h, f"{v}k", "hk-desc", "middle")
    s.both(x + 28, 354, f"ขั้น {k * 10 or 1}", f"step {k * 10 or 1}", "pl-note", "middle")
s.both(680, 104, "ทุกหน้าเว็บค้างอยู่ใน context", "every web page stays in the context", "pl-note")
s.both(620, 392, "✗ Chroma: 18 โมเดลแย่ลงเมื่อ input ยาวขึ้น", "✗ Chroma: 18 models do worse as input grows", "ml-neg")
s.both(620, 420, "คัดแล้ว ≈ 300 token ชนะ ทั้งหมด ≈ 113,000", "focused ≈ 300 tokens beat the full ≈ 113,000", "pl-note")
s.save("l14-context-grow.svg", 456)

# ---------------------------------------------------------------- 21. types of context
s = Svg(W, "Five kinds of context compete for one limited window: prompt context (what the student typed now: How many days are "
           "left until the final exam?), conversation context (earlier messages, tool calls and results), document context "
           "(the 7 facts, lecture slides), stored context (preferences, AGENTS.md, long-term memory) and external context "
           "(search_course results, the calendar API). Context engineering chooses what goes in, in what form, at each step.")
TYPES = [("Prompt context", "สิ่งที่พิมพ์ตอนนี้", "what was typed now", "How many days are left…?"),
         ("Conversation context", "ข้อความก่อนหน้า tool call ผลลัพธ์", "earlier messages, tool calls, results", "ai: tool call get_today()"),
         ("Document context", "PDF โน้ต ชุดข้อมูล", "PDFs, notes, datasets", "the 7 facts · lecture slides"),
         ("Stored context", "ความชอบ ข้อมูลผู้ใช้", "preferences, user info", "AGENTS.md · prefers Thai"),
         ("External context", "ผลการค้น ฐานข้อมูล API", "search results, databases, APIs", "search_course · calendar API")]
for k, (t, dth, den, ex) in enumerate(TYPES):
    y = 20 + k * 82
    s.box(20, y, 600, 72, "ml-cell", 12)
    s.text(36, y + 30, t, "pl-label")
    s.both(36, y + 56, dth, den, "pl-note")
    s.code(360, y + 30, ex)
    s.arrow(622, y + 36, 698, 120 + k * 52)
s.box(700, 60, 460, 300, "nt-band-a", 14)
s.both(720, 92, "context window (มีจำกัด)", "the context window (limited)", "pl-label")
for k, (t, *_r) in enumerate(TYPES):
    s.box(720, 104 + k * 52, 420, 40, "ml-cell", 8)
    s.text(736, 130 + k * 52, t, "hk-desc")
s.both(700, 392, "context engineering: เลือกว่าอะไรเข้า", "Context engineering: choose what goes in,", "pl-text")
s.both(700, 420, "ในรูปแบบไหน ที่ขั้นไหน", "in what form, at which step", "pl-text")
s.save("l14-context-types.svg", 436)

# ---------------------------------------------------------------- 22. offload, reduce, isolate
s = Svg(W, "Three ways to keep the window small. Offload: the agent writes plan.md, notes and full results to files and keeps "
           "only a path; Manus uses fewer than 20 general tools, and code calling MCP tools cut one job from 150,000 to 2,000 "
           "tokens. Reduce: compaction replaces old tool results with the file path where the full result is saved, keeping the "
           "newest in full; when that isn't enough, a structured summary (goal, decisions, open problems). Isolate: each "
           "sub-agent works in its own window and returns a summary of about 1,000 to 2,000 tokens to the lead agent.")
PAN = [(20, "1 · Offload", "ย้ายออกไปไว้ในไฟล์", "move it out to files"), (406, "2 · Reduce", "ย่อสิ่งที่ค้างอยู่", "shrink what stays"),
       (792, "3 · Isolate", "แยก window ให้งานย่อย", "a window per sub-task")]
for x, t, th, en in PAN:
    s.box(x, 20, 368, 420, "nt-band-a", 14)
    s.text(x + 18, 52, t, "pl-label")
    s.both(x + 18, 78, th, en, "pl-note")
x = 20
s.box(x + 18, 96, 168, 170, "ml-cell", 10)
s.both(x + 102, 118, "context", "context", "hk-desc", "middle")
s.box(x + 26, 130, 152, 26, "ml-cell-b", 4)
s.code(x + 34, 148, "plan.md (path)")
s.box(x + 26, 162, 152, 26, "ml-cell-b", 4)
s.code(x + 34, 180, "notes.md (path)")
s.box(x + 222, 96, 128, 170, "ml-cell", 10)
s.both(x + 286, 118, "ไฟล์", "files", "hk-desc", "middle")
for k, f in enumerate(["plan.md", "notes.md", "results/…", "todo.md"]):
    s.code(x + 234, 146 + k * 26, f)
s.arrow(x + 188, 160, x + 220, 160)
s.arrow(x + 220, 200, x + 188, 200)
s.both(x + 18, 304, "tool ทั่วไป < 20 ตัว (Manus)", "< 20 general tools (Manus)", "pl-text")
s.both(x + 18, 334, "MCP ผ่านโค้ด:", "MCP called from code:", "pl-text")
s.both(x + 18, 364, "150,000 → 2,000 token", "150,000 → 2,000 tokens", "ml-ok")
x = 406
s.both(x + 18, 112, "ก่อน", "before", "pl-note")
for k in range(3):
    s.box(x + 18, 122 + k * 30, 330, 22, "sw-chip-warn", 4)
s.arrow(x + 183, 216, x + 183, 236)
s.both(x + 18, 252, "compaction", "compaction", "pl-note")
for k in range(2):
    s.box(x + 18, 262 + k * 30, 200, 22, "ml-cell-b", 4)
    s.code(x + 26, 278 + k * 30, f"results/step-0{k + 1}.txt")
s.box(x + 18, 322, 330, 22, "sw-chip-warn", 4)
s.both(x + 230, 296, "ใหม่สุด: เต็ม", "newest: full", "pl-note")
s.both(x + 18, 378, "ไม่พอ? สรุป:", "Not enough? Summarise:", "pl-text")
s.code(x + 18, 404, "goal · decisions · open problems")
x = 792
s.llm(x + 110, 96, 150, 50, "lead agent", "lead agent")
for k in range(3):
    xx = x + 18 + k * 116
    s.arrow(x + 185, 148, xx + 52, 196)
    s.box(xx, 198, 104, 96, "ml-cell", 8)
    s.both(xx + 52, 222, "sub-agent", "sub-agent", "hk-desc", "middle")
    for j in range(2):
        s.box(xx + 12, 236 + j * 24, 80, 18, "ml-cell-b", 4)
s.both(x + 18, 334, "แต่ละตัวมี window ของตัวเอง", "each has its own window", "pl-text")
s.both(x + 18, 364, "ส่งกลับสรุป ≈ 1–2k token", "returns a ≈ 1–2k-token summary", "ml-ok")
s.save("l14-ori.svg", 456)

# ---------------------------------------------------------------- 23. the harness
s = Svg(W, "Agent = model + harness. In the middle, the LLM is the brain; around it, the harness is the operating system: "
           "loop, tools and sandbox, context, state and memory, guardrails, lifecycle, extensions; outside, the world: files, "
           "the terminal, a browser, the calendar, the user. Examples: Claude Code, Codex, Gemini CLI, OpenHands, Manus; to "
           "build one: Deep Agents, OpenAI Agents SDK, Claude Agent SDK. LangChain kept the model fixed and changed only the "
           "harness: Terminal-Bench 2.0 score 52.8 → 66.5, from outside the top 30 to the top 5.")
s.box(20, 20, 680, 420, "ml-cell", 14)
s.both(40, 52, "agent = โมเดล + harness", "agent = model + harness", "pl-label")
s.box(60, 80, 600, 290, "nt-band-a", 140)
s.llm(270, 180, 180, 90, "LLM", "LLM", ("สมอง", "the brain"))
RING = [("loop", 360, 116), ("tools + sandbox", 160, 150), ("context", 560, 150), ("state + memory", 150, 300),
        ("guardrails", 570, 300), ("lifecycle", 260, 340), ("extensions", 470, 340)]
for t, x, y in RING:
    s.box(x - width(t, 17) / 2 - 12, y - 22, width(t, 17) + 24, 32, "ml-cell", 16)
    s.text(x, y, t, "hk-desc", "middle")
s.both(40, 404, "harness = ระบบปฏิบัติการ · โลก: ไฟล์ terminal browser ปฏิทิน ผู้ใช้", "harness = the operating system · world: files, terminal, browser, calendar, user", "pl-note")
s.box(720, 20, 440, 230, "ml-cell", 14)
s.both(740, 52, "โมเดลเดิม เปลี่ยนแค่ harness", "Same model, harness changed only", "pl-label")
s.both(740, 78, "LangChain · Terminal-Bench 2.0 (89 งาน)", "LangChain · Terminal-Bench 2.0 (89 tasks)", "pl-note")
for k, (v, cls, th, en) in enumerate([(52.8, "ml-bar", "ก่อน · นอก top 30", "before · outside top 30"), (66.5, "ml-bar-top", "หลัง · top 5", "after · top 5")]):
    y = 100 + k * 70
    s.box(740, y, v * 5.4, 34, cls, 4)
    s.text(740 + v * 5.4 + 10, y + 25, f"{v}", "pl-label")
    s.both(740, y + 56, th, en, "pl-note")
s.box(720, 266, 440, 174, "nt-band-a", 14)
s.both(740, 298, "harness ที่เราใช้กัน", "Harnesses you have used", "pl-label")
for k, ln in enumerate(["Claude Code · Codex · Gemini CLI", "OpenHands · Manus", "สร้างเอง: Deep Agents ·" if False else "build one: Deep Agents ·",
                        "OpenAI Agents SDK · Claude Agent SDK"]):
    s.text(740, 330 + k * 28, ln, "hk-desc")
s.save("l14-harness.svg", 456)

# ---------------------------------------------------------------- 24. seven parts of a harness
HP = [("ลูปของ agent", "Agent loop", "เรียกโมเดล รัน tool ส่งผลกลับ กฎการหยุด", "call the model, run tools, feed back; stop rules", "หยุดเมื่อครบ 30 ขั้น", "stops after ≤ 30 steps"),
      ("Tool และ sandbox", "Tools and sandbox", "tool อะไรบ้าง โค้ดรันที่ไหน", "which tools; where code runs", "เขียน plan.md ได้แค่ในโฟลเดอร์ตัวเอง", "writes plan.md in its own folder only"),
      ("การจัดการ context", "Context management", "อะไรเข้าไปในแต่ละครั้ง", "what goes into each call", "ผลเก่า → path ของไฟล์", "old results → file paths"),
      ("State และ memory", "State and memory", "log ทุกขั้น checkpoint ความจำ", "a log of every step, checkpoints", "ล่มที่ขั้น 23 ก็ทำต่อได้", "resumes after a crash at step 23"),
      ("Guardrail และสิทธิ์", "Guardrails, permissions", "ตรวจ argument ขออนุญาต hook", "check arguments, ask, hooks", "ถามก่อนเพิ่ม 5 event", "asks before adding 5 events"),
      ("วงจรชีวิตของงาน", "Lifecycle", "เริ่ม หยุดชั่วคราว ทำต่อ หยุด", "start, pause, resume, stop", "นิสิตหยุดได้ทุกขั้น", "the student can stop it any time"),
      ("ส่วนขยาย", "Extensions", "skill, MCP, sub-agent, AGENTS.md", "skills, MCP, sub-agents, AGENTS.md", "โหลด exam-study-plan", "loads exam-study-plan")]
s = Svg(W, "The seven parts of a harness and what each does for the study-plan agent: agent loop (stops after at most 30 steps), "
           "tools and sandbox (writes plan.md in its own folder only), context management (old results become file paths), "
           "state and memory (resumes after a crash at step 23), guardrails and permissions (asks before adding 5 events), "
           "lifecycle (the student can stop it any time), extensions (loads the exam-study-plan skill).")
s.both(84, 26, "ส่วนของ harness", "Harness part", "nt-head")
s.both(360, 26, "ทำอะไร", "What it does", "nt-head")
s.both(790, 26, "ให้ agent ทำแผนอ่านหนังสือ", "For the study-plan agent", "nt-head")
for k, (pth, pen, dth, den, eth, een) in enumerate(HP):
    y = 40 + k * 56
    s.box(20, y, W - 40, 48, "sw-warn-box" if k == 4 else "ml-cell", 12)
    s.num(48, y + 24, k + 1)
    s.both(76, y + 30, pth, pen, "nt-task")
    s.both(360, y + 30, dth, den, "hk-desc")
    s.both(790, y + 30, eth, een, "ml-ok")
s.save("l14-harness-parts.svg", 40 + 7 * 56 + 4)

# ---------------------------------------------------------------- 25. long-running agents
s = Svg(W, "Top: a long job runs as many sessions, each starting with an empty window. Session 1, the initializer, writes "
           "feature_list.json (over 200 features, all 'passes: false'), claude-progress.txt, init.sh and a first git commit. "
           "Every later session reads the notes and git log, runs init.sh and a basic test, builds one feature, tests it end to "
           "end like a user, commits and updates the notes. Bottom: a separate evaluator. Building a retro game maker alone took "
           "20 minutes and $9 and the core mechanic did not work; planner, generator and evaluator took 6 hours and $200 and the "
           "game was playable.")
s.box(20, 20, 1140, 250, "nt-band-a", 14)
s.both(40, 52, "รอบการทำงานหลายรอบ แต่ละรอบเริ่มด้วย window ว่าง", "Many sessions, each starting with an empty window", "pl-label")
s.box(40, 72, 300, 180, "ml-cell", 10)
s.both(56, 98, "รอบที่ 1: initializer เขียน", "Session 1: the initializer writes", "pl-text")
for k, f in enumerate(['feature_list.json', '  200+ features, "passes": false', "claude-progress.txt", "init.sh · first git commit"]):
    s.code(56, 128 + k * 28, f, bold=(k != 1))
s.arrow(342, 162, 380, 162)
STEPS2 = [("1 อ่านโน้ต + git log", "1 read the notes + git log"), ("2 รัน init.sh + ทดสอบพื้นฐาน", "2 run init.sh + a basic test"),
          ("3 สร้าง feature เดียว", "3 build ONE feature"), ("4 ทดสอบเหมือนผู้ใช้ (browser)", "4 test it like a user (browser)"),
          ("5 commit + อัปเดตโน้ต", "5 commit + update the notes")]
s.box(384, 72, 420, 180, "ml-cell", 10)
s.both(400, 98, "รอบที่ 2, 3, … n: coding session", "Sessions 2, 3, … n: coding", "pl-text")
for k, (th, en) in enumerate(STEPS2):
    s.both(416, 126 + k * 26, th, en, "hk-desc")
s.path("M806 162 Q840 162 840 120 Q840 84 806 84")
s.head(822, 84, 806, 84)
s.both(850, 128, "วนซ้ำจน feature", "repeat until every", "pl-note")
s.both(850, 154, "ผ่านครบ", "feature passes", "pl-note")
s.box(850, 176, 290, 60, "sw-warn-box", 10)
s.both(864, 202, "แก้ได้แค่ช่อง passes", "may only change passes", "pl-text")
s.both(864, 226, "ห้ามลบหรือแก้การทดสอบ", "never edit the tests", "pl-note")
s.box(20, 286, 1140, 170, "ml-cell", 14)
s.both(40, 318, "ผู้ประเมินแยก: agent มักชมงานของตัวเอง", "A separate evaluator: agents praise their own work", "pl-label")
s.both(40, 350, "สร้างโปรแกรมทำเกมแนวเรโทร", "Building a retro game maker", "pl-note")
for k, (lab, mins, cost, sc_, ok, th, en) in enumerate([("solo", 20, 9, 60, False, "เกมใช้ไม่ได้ ✗", "core mechanic broken ✗"),
                                                       ("planner → generator → evaluator", 360, 200, 0, True, "เล่นได้ ✓", "playable ✓")]):
    y = 366 + k * 42
    s.text(40, y + 24, lab, "hk-desc")
    bw = mins / 360 * 420
    s.box(370, y + 4, max(bw, 8), 28, "ml-bar-top" if ok else "ml-bar", 4)
    s.text(370 + max(bw, 8) + 10, y + 25, f"{mins // 60} h, ${cost}" if mins >= 60 else f"{mins} min, ${cost}", "pl-label")
    s.both(940, y + 25, th, en, "ml-ok" if ok else "ml-neg")
s.save("l14-long-running.svg", 472)

# ---------------------------------------------------------------- 26. harness engineering in 2026
s = Svg(W, "Four lessons from 2026. OpenAI, February: about 1,000,000 lines of code and about 1,500 pull requests written by "
           "Codex in five months with three engineers, who built the harness instead. LangChain, February: a check before 'done' "
           "helped move the same model from 52.8 to 66.5. Anthropic Managed Agents, April: the session log, the harness and the "
           "sandbox are separate, so a crash loses nothing, passwords stay out of the sandbox, and the first reply came about 60% "
           "faster. A source-code study of eleven coding harnesses, July: plain file search such as grep instead of embeddings, "
           "skills in 9 of 11 and MCP in 8 of 11, and a minimal harness in about 90 lines.")
TL = [(20, 20, "OpenAI · ก.พ. 2026", "OpenAI · Feb 2026", "≈ 1,000,000 บรรทัด · ≈ 1,500 PR", "≈ 1,000,000 lines · ≈ 1,500 PRs",
       "Codex เขียนโค้ดทั้งหมด วิศวกร 3 คน", "all written by Codex; 3 engineers", "วิศวกรสร้าง harness: AGENTS.md เอกสาร test", "engineers built the harness: AGENTS.md, docs, tests"),
      (600, 20, "LangChain · ก.พ. 2026", "LangChain · Feb 2026", "52.8 → 66.5", "52.8 → 66.5",
       "agent หยุดโดยไม่รันอะไรเลย", "agents stopped without running anything", "middleware บังคับตรวจก่อน “เสร็จ”", "middleware forces a check before “done”"),
      (20, 232, "Anthropic · เม.ย. 2026", "Anthropic · Apr 2026", "session | harness | sandbox", "session | harness | sandbox",
       "container ล่ม งานไม่หาย", "a crashed container loses nothing", "รหัสผ่านอยู่นอก sandbox · เร็วขึ้น ≈ 60%", "passwords stay outside · ≈ 60% faster reply"),
      (600, 232, "งานวิจัย 11 harness · ก.ค. 2026", "Study of 11 harnesses · Jul 2026", "grep ไม่ใช่ embedding", "grep, not embeddings",
       "skill 9/11 > MCP 8/11", "skills 9/11 > MCP 8/11", "harness ขั้นต่ำ ≈ 90 บรรทัด", "a minimal harness ≈ 90 lines")]
for x, y, sth, sen, hth, hen, l1t, l1e, l2t, l2e in TL:
    s.box(x, y, 560, 196, "nt-band-a", 14)
    s.both(x + 20, y + 32, sth, sen, "pl-note")
    s.both(x + 20, y + 76, hth, hen, "pl-label")
    s.both(x + 20, y + 120, l1t, l1e, "pl-text")
    s.both(x + 20, y + 156, l2t, l2e, "ml-ok")
s.save("l14-harness-2026.svg", 444)

# ---------------------------------------------------------------- 27. evaluating an agent
s = Svg(W, "Three runs of our question scored on outcome, trajectory and efficiency. Run A: search_course, get_today, "
           "days_between → 35 days: right on all three. Run B, a real run of a small open model (Qwen3-0.6B): no search, "
           "days_between('2023-10-01', '2023-11-01') with made-up dates → 'There are 31 days left': wrong outcome, wrong "
           "trajectory. Run C, an example: right answer after 9 calls with 6 repeated searches: wasteful. Below: if one run "
           "succeeds 90% of the time, pass@5 (at least one of five) is about 1.00 but pass^5 (all five) is 0.59.")
s.both(200, 30, "tool call", "Tool calls", "nt-head")
s.both(700, 30, "คำตอบ", "Answer", "nt-head")
s.both(860, 30, "ผลลัพธ์", "Outcome", "nt-head")
s.both(960, 30, "เส้นทาง", "Path", "nt-head")
s.both(1050, 30, "คุ้มค่า", "Efficient", "nt-head")
RUNS = [("Run A", "", "", ['search_course("final exam date")', "get_today()", 'days_between("2026-10-26", "2026-11-30")'], "35 days", ("✓", "✓", "✓")),
        ("Run B", "จริง · Qwen3-0.6B", "real · Qwen3-0.6B", ['days_between("2023-10-01", "2023-11-01")', "(no search, made-up dates)"], "31 days", ("✗", "✗", "✓")),
        ("Run C", "ตัวอย่างสมมติ", "an example", ["search_course ×6 (same query)", "get_today() ×2", "days_between(…)"], "35 days", ("✓", "✓", "✗"))]
for k, (r, nth, nen, calls, ans, marks) in enumerate(RUNS):
    y = 44 + k * 112
    bad = "✗" in marks[:2]
    s.box(20, y, W - 40, 100, "sw-warn-box" if bad else "ml-cell", 12)
    s.text(36, y + 34, r, "pl-label")
    if nen:
        a, b = (nen.split(" · ") + [""])[:2]
        at, bt = (nth.split(" · ") + [""])[:2]
        s.both(36, y + 60, at, a, "pl-note")
        if b:
            s.both(36, y + 84, bt, b, "pl-note")
    for j, c in enumerate(calls):
        s.code(200, y + 30 + j * 26, c, bold=(j == 0 and k == 1))
    s.text(700, y + 56, ans, "pl-label")
    for j, m in enumerate(marks):
        s.text(890 + j * 96, y + 56, m, "ml-ok" if m == "✓" else "ml-neg", "middle")
s.box(20, 386, W - 40, 82, "nt-band-a", 12)
s.both(36, 416, "ถูก 90% ของเวลา (p = 0.9) รัน 5 ครั้ง:", "Right 90% of the time (p = 0.9), run 5 times:", "pl-text")
s.both(36, 448, "pass@5 = อย่างน้อย 1 ครั้งถูก ≈ 1.00 · pass^5 = ถูกทั้ง 5 ครั้ง = 0.9⁵ = 0.59", "pass@5 = at least one right ≈ 1.00 · pass^5 = all five right = 0.9⁵ = 0.59", "pl-label")
s.save("l14-eval.svg", 484)
