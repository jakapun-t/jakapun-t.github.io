"""Draws the pictures of lesson 14 of the international NLP course (workflows and LLM agents): SVG, inlined into
the page; ไทย/EN labels follow the language switch.

    python3 scripts/diagrams/nlp_l14_figures.py courses/nlp/images

Real numbers (computed in course/.venv on 2026-10-19):
- search_course = all-MiniLM-L6-v2 over the 7 course facts: "How many days are left until the final exam?" → fact 7
  (0.693), fact 2 (0.509); "final exam date" → fact 7 (0.830). 26 Oct → 30 Nov 2026 = 35 days; → 2 Nov = 7 days.
- Gemini runs (2026-10-23, gemini-3.5-flash-lite unless noted; the lesson's kept outputs): the running question reads
  256, 538, 591 input tokens in 3 calls (1,385 in, 102 out; the question alone is 11). The Deep Agent study-plan run
  (gemini-3.8-flash): 16 tool calls, 12 model calls, 97,743 input tokens (largest call 14,565). The earlier run before
  search_course had k: 65 tool calls (54 searches), 22 model calls, 167,828 input tokens, an empty final reply.
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
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


def pic(s, name, x, y, w, h, align="xMidYMax"):
    """Inline a generated picture from assets/ (characters stand on the bottom edge of their box)."""
    import base64
    data = base64.b64encode(open(os.path.join(ASSETS, name + ".png"), "rb").read()).decode()
    s.raw(f'<image x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" preserveAspectRatio="{align} meet" '
          f'href="data:image/png;base64,{data}"/>')


def ic(s, name, cx, cy, size):
    """A generated icon (assets/icon-<name>.png) centred on (cx, cy)."""
    pic(s, "icon-" + name, cx - size / 2, cy - size / 2, size, size, "xMidYMid")

# ---------------------------------------------------------------- 1. hook: RAG workflow vs agent
s = Svg(W, "A student asks 'How many days are left until the final exam?' on Monday 26 October. Left, the RAG workflow: "
           "it searches the 7 facts and keeps the top 2 (fact 7, final exam on Monday 30 November, cosine 0.693; fact 2, the "
           "midterm, 0.509), builds a prompt and lets Gemini write; no fact gives today's date and no step counts days, so the "
           "model can only guess. Right, an agent (a robot with tools): the LLM calls search_course('final exam date') → fact 7, "
           "get_today() → 2026-10-26, days_between('2026-10-26', '2026-11-30') → 35, then answers 35 days; the student is happy.")
pic(s, "ag-student-ask", 196, 4, 90, 112)
s.box(296, 34, 680, 46, "nt-bubble", 23)
s.both(636, 64, "“เหลืออีกกี่วันถึงสอบปลายภาค” (ถามวันจันทร์ที่ 26 ต.ค.)", "“How many days are left until the final exam?” (asked Mon 26 Oct)", "pl-text", "middle")
Y = 108
s.box(20, Y + 12, 560, 388, "sw-warn-box", 14)
s.both(40, Y + 44, "✗ RAG แบบ workflow (ขั้นตอนตายตัว)", "✗ RAG workflow (fixed steps)", "pl-label")
s.box(40, Y + 60, 520, 124, "ml-cell", 10)
s.num(62, Y + 84, 1)
s.both(84, Y + 90, "ค้นข้อเท็จจริง 7 ข้อ เก็บ 2 อันดับแรก", "Search the 7 facts, keep the top 2", "pl-text")
s.box(58, Y + 104, 484, 32, "sw-chip-warn", 8)
s.both(70, Y + 126, "fact 7 · สอบปลายภาค จันทร์ 30 พ.ย. · cos 0.693", "fact 7 · final exam, Mon 30 Nov · cos 0.693", "pl-note")
s.box(58, Y + 142, 484, 32, "ml-cell", 8)
s.both(70, Y + 164, "fact 2 · สอบกลางภาค 21 ก.ย. · cos 0.509", "fact 2 · midterm, 21 Sep · cos 0.509", "pl-note")
s.box(40, Y + 196, 520, 44, "ml-cell", 10)
s.num(62, Y + 218, 2)
s.both(84, Y + 224, "prompt = คำถาม + fact 2 ข้อนั้น", "Prompt = question + those 2 facts", "pl-text")
s.box(40, Y + 252, 520, 44, "ml-cell", 10)
s.num(62, Y + 274, 3)
s.both(84, Y + 280, "Gemini เขียนคำตอบ", "Gemini writes the answer", "pl-text")
s.both(40, Y + 336, "✗ ไม่มี fact ไหนบอกวันที่ของวันนี้", "✗ No fact gives today's date,", "ml-neg")
s.both(40, Y + 366, "และไม่มีขั้นไหนนับวัน → โมเดลต้องเดา", "and no step counts days → it guesses", "ml-neg")
s.box(600, Y + 12, 560, 388, "nt-band-a", 14)
s.both(620, Y + 44, "✓ Agent: LLM เลือกแต่ละขั้นเอง", "✓ Agent: the LLM picks each step", "pl-label")
pic(s, "ag-robot-tools", 612, Y + 76, 112, 150)
s.both(668, Y + 252, "LLM + tool", "LLM + tools", "pl-note", "middle")
CALLS = [('search_course("final exam date")', "→ fact 7: จันทร์ 30 พฤศจิกายน 2026", "→ fact 7: Monday 30 November 2026", "magnifier"),
         ("get_today()", "→ 2026-10-26", "→ 2026-10-26", "clock"),
         ('days_between("2026-10-26", "2026-11-30")', "→ 35", "→ 35", "abacus")]
for k, (c, rth, ren, icon) in enumerate(CALLS):
    y = Y + 64 + k * 82
    s.box(736, y, 404, 64, "ml-cell", 10)
    s.num(752, y + 20, k + 1)
    s.code(772, y + 26, c)
    s.both(772, y + 52, rth, ren, "ml-ok" if k == 2 else "pl-note")
    if k < 2:
        ic(s, icon, 1110, y + 44, 30)
    s.arrow(726, y + 32, 734, y + 32)
s.box(620, Y + 306, 450, 46, "nt-out", 10)
s.both(845, Y + 336, "“35 วัน: จันทร์ 30 พ.ย. 13:00–16:00”", "“35 days: Mon 30 Nov, 13:00–16:00”", "pl-text", "middle")
pic(s, "ag-student-happy", 1078, Y + 290, 76, 94)
s.both(620, Y + 382, "✓ LLM เลือก tool 3 ตัว โค้ดของเราเป็นคนนับ", "✓ the LLM chose 3 tools; our code counted", "ml-ok")
s.save("l14-hook.svg", Y + 416)

# ---------------------------------------------------------------- 2. lesson map: inside an agent
s = Svg(W, "Inside an agent, the map of the lesson. The student's question goes into the harness, the code around the model. "
           "The harness builds the context (rules, tool descriptions, memory, skills and MCP, the messages so far) and sends it "
           "to the LLM. The LLM decides: answer, or ask for a tool. A tool call is checked (valid? allowed? does a person have to "
           "approve?) and run by the harness; the result is added to the messages and the LLM is asked again: 3 rounds give "
           "35 days. Numbered badges mark the parts of the lesson: 1 from LLM to agent, 2 tool calling, 3 the loop and how it "
           "thinks, 4 inside the harness, 5 Deep Agents for long jobs, 6 MCP, skills and memory, 7 trace and evaluate.")
pic(s, "ag-student-ask", 20, 0, 56, 68)
s.box(82, 10, 498, 46, "nt-bubble", 23)
s.text(331, 40, Q, "pl-text", "middle")
s.num(604, 33, 1)
s.box(780, 10, 316, 46, "nt-out", 23)
s.both(938, 40, "“35 วัน (จันทร์ 30 พ.ย.)”", "“35 days (Mon 30 Nov)”", "pl-text", "middle")
pic(s, "ag-student-happy", 1104, 0, 56, 68)
s.arrow(190, 58, 190, 120)
s.box(20, 72, 1140, 392, "nt-band-a", 16)
s.num(234, 96, 4)
s.both(256, 102, "Harness: โค้ดรอบตัวโมเดล", "Harness: the code around the model", "pl-label")
# build the context
s.box(40, 122, 300, 250, "ml-cell", 12)
s.both(56, 150, "เตรียมสิ่งที่โมเดลอ่าน", "Build what the model reads", "pl-label")
CTX = [("กฎ (system prompt)", "rules (system prompt)"), ("คำอธิบาย tool", "tool descriptions"),
       ("memory · skills · MCP", "memory · skills · MCP"), ("ข้อความจนถึงตอนนี้", "the messages so far")]
for k, (th, en) in enumerate(CTX):
    s.chip(56, 166 + k * 42, 268, 34, th, en, "ml-cell-b")
s.num(306, 267, 6)
s.both(56, 360, "ส่งไปทุกครั้งที่เรียก", "sent with every call", "pl-note")
s.arrow(342, 240, 408, 240)
# the LLM
s.box(410, 170, 150, 140, "ml-cell-b", 12)
pic(s, "ag-robot-think", 440, 176, 90, 100)
s.both(485, 298, "LLM ตัดสินใจ", "LLM decides", "pl-label", "middle")
s.num(400, 154, 3)
s.arrow(530, 172, 776, 54)
s.both(694, 140, "ไม่มี tool call → ตอบ", "no tool call → answer", "pl-note")
s.arrow(562, 240, 648, 240)
s.both(605, 228, "tool call", "tool call", "pl-note", "middle")
s.num(605, 266, 2)
# check and run
s.box(650, 166, 250, 180, "ml-cell", 12)
s.both(666, 194, "ตรวจ แล้วจึงรัน", "Check, then run", "pl-label")
RUN = [("argument ถูกไหม", "valid arguments?"), ("อนุญาตไหม · ถามคนไหม", "allowed? ask a person?"), ("รัน tool", "run the tool")]
for k, (th, en) in enumerate(RUN):
    s.chip(666, 208 + k * 42, 218, 34, th, en, "nt-out" if k == 2 else "ml-cell-b")
s.arrow(902, 256, 928, 256)
s.box(930, 166, 210, 180, "pl-chip", 12)
s.both(946, 194, "Tools", "Tools", "pl-label")
for k, (t, icon) in enumerate([("search_course", "magnifier"), ("get_today", "clock"), ("days_between", "abacus"), ("add_to_calendar", "calendar")]):
    ic(s, icon, 958, 220 + k * 30, 24)
    s.code(976, 226 + k * 30, t)
# result back to the messages
s.path("M1035 348 L1035 392 L190 392 L190 376")
s.head(190, 392, 190, 376)
s.both(620, 384, "ผล → ต่อท้ายข้อความ → ถามใหม่ · 3 รอบ → 35 วัน", "result → added to the messages → ask again · 3 rounds → 35 days", "pl-note", "middle")
# long jobs and traces
s.box(40, 408, 540, 40, "ml-cell-b", 10)
s.num(62, 428, 5)
s.both(84, 434, "งานยาว: แผน · ไฟล์ · sub-agent · ย่อ context", "Long jobs: plans · files · sub-agents · shrink context", "hk-desc")
s.box(600, 408, 540, 40, "ml-cell-b", 10)
s.num(622, 428, 7)
s.both(644, 434, "ประเมินผล: benchmark ค่าใช้จ่าย เวลา", "Evaluate: benchmarks, cost, time", "hk-desc")
s.save("l14-map-lesson.svg", 476)

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

# ---------------------------------------------------------------- 3b. workflow vs agent on a help chat (an example)
s = Svg(W, "An example: an online shop's help chat. Left, a workflow: 'Where is my order #4812?' arrives thousands of times a "
           "day, so the path is written once: 1 classify the message as order status, 2 look the order up in the orders table, "
           "3 fill the reply template: 'Order #4812 arrives tomorrow.' Fast, cheap, the same every time, easy to test. But "
           "'It arrived broken and I was charged twice' fits no route, so the bot says it didn't understand and passes it to a "
           "person. Right, an agent takes that message and decides the steps as it goes: get the order, get the payments (two "
           "charges), read the refund policy, ask a person to approve a 590-baht refund, refund and create a return, book a "
           "courier, reply. It handles what nobody planned for, but needs many model calls, is slower and costs more, and a "
           "wrong refund is real money, so it asks first.")
s.box(20, 20, 560, 460, "ml-cell", 14)
s.both(40, 52, "Workflow: เส้นทางเดียวที่เขียนไว้", "Workflow: one path, written once", "pl-label")
s.both(40, 78, "ตัวอย่าง: แชตช่วยเหลือของร้านออนไลน์ · วันละหลายพันครั้ง", "example: a shop's help chat · thousands a day", "pl-note")
pic(s, "ag-student-ask", 40, 86, 56, 58)
s.box(104, 94, 456, 40, "nt-bubble", 20)
s.both(122, 120, "“ของที่สั่ง #4812 อยู่ไหน”", "“Where is my order #4812?”", "pl-text")
WF = [("จัดประเภท: สถานะคำสั่งซื้อ (LLM 1 ครั้ง)", "classify: order status (1 LLM call)"),
      ("ค้น #4812 ในตารางคำสั่งซื้อ (โค้ด)", "look up #4812 in the orders table (code)"),
      ("เติมแม่แบบคำตอบ", "fill the reply template")]
for k, (th, en) in enumerate(WF):
    y = 146 + k * 48
    s.box(40, y, 520, 38, "ml-cell-b", 8)
    s.num(62, y + 19, k + 1)
    s.both(84, y + 25, th, en, "hk-desc")
s.box(40, 292, 520, 40, "nt-out", 10)
pic(s, "ai-robot", 50, 294, 30, 36)
s.both(90, 318, "“#4812 จะถึงพรุ่งนี้”", "“Order #4812 arrives tomorrow.”", "pl-text")
s.both(40, 360, "✓ เร็ว ถูก เหมือนเดิมทุกครั้ง ทดสอบง่าย", "✓ fast, cheap, the same every time, easy to test", "ml-ok")
s.box(40, 378, 520, 86, "sw-chip-warn", 10)
ic(s, "parcel", 70, 400, 30)
s.both(92, 406, "“ของมาถึงแตก แล้วยังโดนตัดเงินสองครั้ง…”", "“It arrived broken and I was charged twice…”", "pl-text")
s.both(56, 434, "✗ ไม่มีเส้นทางไหนตรง → “ขออภัย ไม่เข้าใจ”", "✗ no route fits → “Sorry, I didn't get that”", "ml-neg")
s.both(56, 456, "→ ส่งต่อให้พนักงาน", "→ passed to a person", "pl-note")
s.box(600, 20, 560, 460, "nt-band-a", 14)
s.both(620, 52, "Agent: ตัดสินใจขั้นต่อไปเองระหว่างทาง", "Agent: decides the steps as it goes", "pl-label")
s.both(620, 78, "ข้อความเดียวกันที่ workflow รับไม่ได้", "the same chat, the message no route fits", "pl-note")
pic(s, "ag-customer-upset", 616, 84, 60, 60)
s.box(684, 94, 456, 40, "sw-chip-warn", 20)
s.both(700, 120, "“ของมาถึงแตก แล้วโดนตัดเงินสองครั้ง…”", "“It arrived broken and I was charged twice…”", "pl-text")
AG = ['get_order("4812") → delivered', 'get_payments("4812") → 2 charges', 'read_policy("refund")',
      'ask_person("refund 590 baht?") → OK', "refund(...) · create_return(...)", "book_courier(...)", "reply to the customer"]
for k, c in enumerate(AG):
    y = 146 + k * 36
    s.box(620, y, 520, 30, "sw-chip-warn" if k == 3 else "ml-cell", 7)
    s.text(634, y + 21, str(k + 1), "pl-label")
    s.code(660, y + 21, c)
    STEP_PIC = {0: "parcel", 1: "moneybag", 4: "moneybag", 5: "truck", 6: "chat"}
    if k in STEP_PIC:
        ic(s, STEP_PIC[k], 1118, y + 15, 26)
    if k == 3:
        pic(s, "ag-staff-ok", 1096, y - 4, 40, 34)
s.both(620, 418, "✓ รับเรื่องที่ไม่มีใครวางแผนไว้ได้", "✓ handles what nobody planned for", "ml-ok")
s.both(620, 444, "✗ เรียกโมเดลหลายครั้ง: ช้ากว่าและแพงกว่า", "✗ many model calls: slower and costlier", "ml-neg")
s.both(642, 468, "คืนเงินผิดคือเงินจริง → ต้องถามคนก่อน", "a wrong refund is real money → ask a person first", "pl-note")
s.save("l14-workflow-jobs.svg", 496)

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

# ---------------------------------------------------------------- 7. why tools
s = Svg(W, "Four limits of an LLM alone and the tool that fixes each. No clock: it guesses today's date; get_today() → 2026-10-26. "
           "No exact arithmetic: it writes numbers token by token; a calculator gives sqrt(1764) × 7 = 294. No private or new "
           "data: it never saw our 7 facts; search_course → fact 7. No hands: it can only write text; add_to_calendar adds the "
           "event. The first three fetch data; the last takes an action, so ask first.")
TILE_ICON = ["clock", "abacus", "books", "calendar"]
TILES = [("1 · ไม่มีนาฬิกา", "1 · No clock", ("เดาวันที่ของวันนี้", "", "guesses today's date", ""), "get_today()", "2026-10-26", False),
         ("2 · คำนวณไม่แม่น", "2 · No exact maths", ("เขียนตัวเลขทีละ token", "จึงพลาดได้", "writes numbers token by", "token, so it can slip"), "calculator(...)", "√1764 × 7 = 294", False),
         ("3 · ไม่มีข้อมูลใหม่", "3 · No new data", ("ไม่เคยเห็นข้อเท็จจริง", "7 ข้อของเรา", "never saw our", "7 course facts"), "search_course(...)", "fact 7", False),
         ("4 · ลงมือไม่ได้", "4 · No hands", ("เขียนได้แค่ข้อความ", "", "can only write text", ""), "add_to_calendar(...)", "event added", True)]
for k, (tth, ten, (n1t, n2t, n1e, n2e), call, res, act) in enumerate(TILES):
    x = 20 + k * 290
    s.box(x, 20, 280, 330, "sw-warn-box" if False else "ml-cell", 14)
    s.both(x + 18, 54, tth, ten, "pl-label")
    ic(s, TILE_ICON[k], x + 244, 76, 44)
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
        s.box(48, y - 16, 500, 22, "sw-chip-warn" if HL[k] == 2 else "dg-hl-col", 4)
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
        s.box(648, y - 16, 504, 22, "sw-chip-warn" if JHL[k] == 2 else "dg-hl-col", 4)
    s.code(656, y, ln)
for k, n in ((0, 1), (2, 2), (4, 3)):
    s.num(630, 76 + k * 24, n)
s.arrow(566, 140, 614, 140)
s.both(20, 302, "1 ชื่อฟังก์ชัน → name · 2 docstring → description: โมเดลอ่านอันนี้เพื่อเลือก tool · 3 type hint + Args → parameters",
       "1 function name → name · 2 docstring → description: what the model reads to choose · 3 type hints + Args → parameters", "pl-text")
s.box(20, 322, 1140, 110, "sw-warn-box", 14)
s.code(40, 356, '@tool')
s.code(40, 378, 'def multiply(a: int, b: int) -> int:')
s.code(40, 400, '    """Do math."""')
s.arrow(360, 378, 420, 378)
s.code(432, 378, '"description": "Do math."')
s.both(700, 366, "✗ คณิตแบบไหน กับอะไร เมื่อไร", "✗ which maths, on what, when?", "ml-neg")
s.both(700, 396, "โมเดลเลือกระหว่างมันกับเครื่องคิดเลขไม่ได้", "the model can't tell it from a calculator", "pl-note")
s.save("l14-tool-schema.svg", 448)

# ---------------------------------------------------------------- 8b. the docstring decides (real Gemini test)
s = Svg(W, "A real test with gemini-3.5-flash-lite, run 3 times each. The three tools were renamed tool_a, tool_b and tool_c, "
           "so their names say nothing. Left, with clear docstrings (search the course facts; get today's date; count the days "
           "between two dates), Gemini called tool_a('final exam date') and tool_b() in all 3 runs. Right, the same functions "
           "with the docstring 'A helper.' on each: no tool call in all 3 runs; it asked the student for the exam date instead. "
           "The docstring is what the model reads to choose a tool.")
pic(s, "ag-student-ask", 236, 0, 52, 62)
s.box(296, 10, 588, 44, "nt-bubble", 22)
s.text(590, 39, Q, "pl-text", "middle")
DOCS = [("tool_a(x)", ["Search the facts about course 2190519:", "class dates, topics and exams."]),
        ("tool_b()", ["Get today's date as YYYY-MM-DD."]),
        ("tool_c(x, y)", ["Count the days from one date to another."])]
for side, (x0, cls, th, en) in enumerate([(20, "nt-band-a", "✓ ชื่อถูกซ่อน docstring ชัด", "✓ Names hidden, clear docstrings"),
                                          (600, "sw-warn-box", "✗ ฟังก์ชันเดิม docstring \"A helper.\"", "✗ Same functions, docstring \"A helper.\"")]):
    s.box(x0, 70, 560, 380, cls, 14)
    s.both(x0 + 20, 102, th, en, "pl-label")
    s.both(x0 + 20, 128, "สิ่งที่ Gemini อ่าน (ชื่อไม่บอกอะไร)", "what Gemini reads (the names say nothing)", "pl-note")
    y = 142
    for k, (name, lines) in enumerate(DOCS):
        if side == 1:
            lines = ["A helper."]
        h = 30 + 22 * len(lines)
        chosen = side == 0 and k < 2
        s.box(x0 + 20, y, 400, h, "nt-out" if chosen else "ml-cell", 10)
        s.code(x0 + 34, y + 22, name, bold=True)
        for j, ln in enumerate(lines):
            s.code(x0 + 34, y + 44 + j * 22, '"' + ln + '"' if len(lines) == 1 else ('"' + ln if j == 0 else ln + '"'))
        if chosen:
            s.text(x0 + 408, y + 24, "✓", "ml-ok", "end")
        y += h + 10
    pic(s, "ag-robot-think" if side else "ag-robot-tools", x0 + 432, 150, 116, 150)
s.box(40, 360, 520, 76, "ml-cell", 10)
s.both(56, 388, "Gemini เรียก (ครบ 3 จาก 3 ครั้ง):", "Gemini called (all 3 of 3 runs):", "ml-ok")
s.code(56, 418, 'tool_a(x="final exam date") + tool_b()')
s.box(620, 360, 520, 76, "ml-cell", 10)
s.both(636, 388, "✗ ไม่เรียก tool เลย (3 จาก 3 ครั้ง)", "✗ no tool call (3 of 3 runs)", "ml-neg")
s.text(636, 418, "“I need to know the date of the exam!”", "pl-note")
s.both(20, 478, "ชื่อถูกซ่อนทั้งสองฝั่ง: docstring คือสิ่งที่ Gemini ใช้เลือก tool", "The names were hidden on both sides: the docstring is what Gemini used to choose.", "pl-text")
s.save("l14-docstring-test.svg", 494)

# ---------------------------------------------------------------- 9. function call (real Gemini run)
s = Svg(W, "How Gemini asks for a tool, from a real run. 1 The request has the question in contents and our three functions in "
           "their own field, tools; the API turns them into schemas the model reads. Of the 256 input tokens, only 11 are the question; about 245 are the tool descriptions (96%). Later calls also resend the earlier calls and results (538, then 591 tokens), and an agent adds its rules and memory. 2 Gemini's reply is a list "
           "of parts: two function_call parts in the same turn, get_today with no arguments and search_course with query "
           "'final exam' and k 7, and no text at all (text: None). 3 Our code runs both: 2026-10-26 and the facts, fact 7 first. "
           "4 The results go back as function_response parts and Gemini is called again.")
s.box(20, 20, 340, 380, "ml-cell", 14)
s.num(44, 50, 1)
s.both(66, 56, "สิ่งที่ส่งไป: ทั้ง context", "What we send: the context", "pl-label")
s.box(36, 72, 308, 54, "ml-cell", 10)
s.both(50, 94, "คำถาม", "the question", "hk-desc")
s.code(50, 116, '"How many days are left…"')
s.text(334, 94, "11", "pl-label", "end")
s.box(36, 134, 308, 100, "nt-band-a", 10)
s.both(50, 156, "tool: ชื่อ + docstring + parameter", "tools: name + docstring + params", "hk-desc")
for k, t in enumerate(["search_course(query, k)", "get_today()", "days_between(start, end)"]):
    s.code(60, 180 + k * 20, t)
s.text(334, 200, "≈245", "pl-label", "end")
s.both(36, 258, "input 256 token:", "256 input tokens:", "pl-note")
s.box(36, 266, 287, 18, "ml-bar", 3)
s.box(323, 266, 21, 18, "ml-model", 3)
s.both(36, 304, "96% คือ tool · 4% คือคำถาม", "96% tools · 4% the question", "pl-text")
s.box(36, 318, 308, 34, "pl-chip-del", 8)
s.both(48, 341, "+ รอบถัดไป: ผลเดิม (538, 591)", "+ later calls: past results (538, 591)", "hk-desc")
s.box(36, 358, 308, 34, "pl-chip-del", 8)
s.both(48, 381, "+ ใน agent: กฎ และ memory", "+ agents: rules, memory", "hk-desc")
s.arrow(362, 190, 392, 190)
s.box(396, 20, 400, 380, "nt-out", 14)
s.num(420, 50, 2)
s.both(442, 56, "คำตอบของ Gemini: list ของ part", "Gemini's reply: a list of parts", "pl-label")
s.box(412, 76, 368, 62, "ml-cell", 10)
s.code(428, 100, "function_call")
s.code(428, 124, "  get_today  {}")
s.box(412, 148, 368, 86, "ml-cell", 10)
s.code(428, 172, "function_call")
s.code(428, 196, "  search_course")
s.code(428, 220, "  {query: 'final exam', k: 7}")
s.box(412, 244, 368, 40, "sw-chip-warn", 10)
s.code(428, 270, "text: None")
s.both(412, 312, "✓ 2 คำขอในรอบเดียว (parallel)", "✓ two requests in one turn (parallel)", "ml-ok")
s.both(412, 340, "ไม่ใช่ JSON ในข้อความ: เป็น part มีชนิด", "not JSON in text: typed parts", "pl-note")
s.arrow(798, 190, 828, 190)
s.box(832, 20, 328, 380, "nt-band-a", 14)
s.num(856, 50, 3)
s.both(878, 56, "โค้ดของเรารันทั้งสอง", "Our code runs both", "pl-label")
s.box(848, 76, 296, 40, "pl-chip", 8)
s.code(860, 101, "get_today() → 2026-10-26")
s.box(848, 126, 296, 64, "pl-chip", 8)
s.code(860, 151, "search_course(...) →")
s.code(860, 175, "[fact 7] final exam 30 Nov …")
s.num(856, 222, 4)
s.both(878, 228, "ส่งผลกลับเป็น", "Sent back as", "pl-text")
s.code(878, 254, "function_response")
s.both(856, 300, "แล้วเรียก Gemini อีกครั้ง:", "then Gemini is called again:", "pl-note")
s.both(856, 326, "days_between แล้วจึงตอบ", "days_between, then the answer", "pl-note")
s.both(20, 434, "โมเดลไม่ได้รันอะไรเอง: มันคืนคำขอ แล้ว harness (โค้ดของเรา) เป็นคนรัน",
       "The model runs nothing: it returns requests, and the harness (our code) runs them.", "pl-text")
s.save("l14-function-call.svg", 450)

# ---------------------------------------------------------------- 11a. what plugs into the harness: into the context window
s = Svg(W, "The harness fills the context window from three outside sources. Long-term memory: AGENTS.md ('prefers Thai "
           "answers') is read at the start into the rules. Skills: only each skill's name and description (about 41 tokens) "
           "goes in; the full SKILL.md (about 144 tokens) is loaded only when a task matches. MCP: a calendar MCP server's "
           "tools, such as create_event, join the tool descriptions like our own tools, and the harness forwards each call to "
           "the server. Short-term memory is the thread itself: the earlier calls and results, saved by a checkpointer.")
SRC = [("brain", "Memory (ระยะยาว)", "Memory (long-term)", "เก็บไว้นอก thread", "saved outside the thread", "AGENTS.md: prefers Thai", 150),
       ("books", "Skills", "Skills", "วิธีทำงานในโฟลเดอร์", "know-how in a folder", "skills/exam-study-plan/", 342),
       ("plug", "MCP server", "MCP server", "tool จากข้างนอก ปลั๊กเดียว", "outside tools, one plug", "calendar → create_event", 562)]
for k, (icon, th, en, dth, den, code, target) in enumerate(SRC):
    x = 20 + k * 380
    s.box(x, 20, 368, 140, "nt-band-a", 14)
    ic(s, icon, x + 40, 58, 52)
    s.both(x + 76, 52, th, en, "pl-label")
    s.both(x + 76, 78, dth, den, "hk-desc")
    s.box(x + 16, 100, 336, 40, "ml-cell", 8)
    s.code(x + 30, 126, code)
    s.arrow(x + 184, 162, target, 222)
s.both(40, 298, "context window ที่ harness ประกอบ (ไม่ตามสเกล)", "the context window the harness builds (not to scale)", "pl-note")
BAR = [(40, 256, "dg-hl-col", "กฎ + AGENTS.md", "rules + AGENTS.md"), (260, 160, "ml-cell-b", "รายชื่อ skill", "skill list"),
       (424, 276, "ml-bar", "คำอธิบาย tool", "tool descriptions"), (704, 26, "ml-model", "", ""),
       (734, 226, "sw-chip-warn", "thread", "the thread")]
for x, w, cls, th, en in BAR:
    s.box(x, 226, w if w != 256 else 216, 48, cls, 4)
    if en:
        s.both(x + 12, 256, th, en, "hk-desc")
s.both(717, 296, "คำถาม", "question", "hk-desc", "middle")
s.box(966, 226, 174, 48, "nt-out", 4)
s.both(980, 256, "→ token ถัดไป", "→ next token", "hk-desc")
s.arrow(847, 334, 847, 278)
s.both(760, 352, "ความจำระยะสั้น = thread", "short-term memory = the thread", "hk-desc")
s.both(760, 376, "checkpointer บันทึกตาม thread_id", "saved by a checkpointer per thread_id", "pl-note")
CAP = [(20, "ตอนเริ่ม: อ่าน AGENTS.md และแค่ชื่อกับคำอธิบาย", "At start: AGENTS.md, and only each skill's",
        "ของแต่ละ skill (≈41 token) ทั้งไฟล์ (≈144)", "name + description (≈41 tokens); the full",
        "โหลดเฉพาะเมื่องานตรงกัน", "SKILL.md (≈144) only when a task matches"),
       (400, "tool ของ MCP ดูเหมือน tool ของเรา", "MCP tools look like our own tools;",
        "เมื่อ Gemini เรียก create_event", "when Gemini calls create_event,",
        "harness ส่งต่อให้ server", "the harness forwards it to the server")]
for x, a_th, a_en, b_th, b_en, c_th, c_en in CAP:
    s.box(x, 312, 368 if x == 20 else 340, 112, "ml-cell", 12)
    for j, (th, en) in enumerate([(a_th, a_en), (b_th, b_en), (c_th, c_en)]):
        s.both(x + 16, 344 + j * 28, th, en, "hk-desc")
s.save("l14-plugins.svg", 440)

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
ic(s, "plug", 1112, 46, 44)
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
s = Svg(W, "Short-term memory: the model remembers nothing between calls, so the harness sends the whole thread with every "
           "call: 'When is the NER class?', the reply (November 2, 2026), and 'How many days until then?' → 'There are 7 days "
           "until the NER class.' A new thread starts empty, and it is limited by the context window. Long-term memory: facts worth keeping are written to a store "
           "(a file, a database or a vector index), such as 'prefers Thai answers' and 'exam reminders added', and "
           "loaded into the prompt of a session next week.")
s.box(20, 20, 560, 420, "nt-band-a", 14)
s.both(40, 52, "ความจำระยะสั้น = state ของ thread", "Short-term memory = the thread's state", "pl-label")
s.both(40, 80, "ส่ง list ข้อความทั้งหมดไปทุกครั้ง", "the whole message list goes with every call", "pl-note")
ic(s, "save", 536, 46, 34)
CH = [("human", "When is the NER class?"), ("ai", "…(NER) is on November 2, 2026."), ("human", "How many days until then?")]
for k, (r, t) in enumerate(CH):
    y = 100 + k * 46
    s.box(40, y, 78, 34, "nt-bubble" if r == "human" else "ml-cell", 8)
    s.text(79, y + 23, r, "hk-desc", "middle")
    s.box(126, y, 434, 34, "ml-cell", 8)
    s.code(138, y + 22, t)
s.path("M300 240 L300 270")
s.head(300, 250, 300, 270)
s.both(316, 262, "ส่งทั้ง thread", "the whole thread sent", "pl-note")
s.llm(220, 274, 160, 48, "LLM", "LLM")
s.arrow(300, 324, 300, 344)
s.box(40, 348, 520, 34, "nt-out", 8)
s.code(56, 370, "ai: There are 7 days until the NER class.")
s.both(40, 418, "thread ใหม่เริ่มว่าง · จำกัดด้วย context window", "a new thread starts empty · limited by the window", "ml-neg")
s.box(600, 20, 560, 420, "ml-cell", 14)
s.both(620, 52, "ความจำระยะยาว = เก็บไว้ข้างนอก", "Long-term memory = saved outside", "pl-label")
ic(s, "brain", 1118, 44, 40)
s.chip(620, 84, 196, 44, "รอบที่ 1 (26 ต.ค.)", "session 1 (26 Oct)", "nt-bubble", "hk-desc")
s.arrow(818, 106, 846, 106)
s.both(832, 80, "เขียน", "write", "pl-note", "middle")
s.box(850, 72, 290, 180, "nt-band-a", 12)
s.both(864, 100, "ที่เก็บ: ไฟล์ · ฐานข้อมูล · vector", "store: file · database · vectors", "pl-note")
for k, t in enumerate(["prefers Thai answers", "exam reminders added", "weak topic: NER"]):
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
           "days_between (35 days = 5 weeks); 3 write the plan as a table; 4 add 5 review sessions with add_to_calendar, "
           "after asking. Below, chain-of-thought is one straight line of steps; tree of thoughts tries several branches, "
           "drops a bad one and keeps the best.")
s.box(310, 16, 560, 50, "ml-model", 25)
s.both(590, 48, "เป้าหมาย: แผนอ่าน 5 สัปดาห์ + รอบทบทวนในปฏิทิน", "Goal: a 5-week study plan + review sessions in my calendar", "ml-model-text", "middle")
SUB = [("1 หาหัวข้อ", "1 Find the topics", "search_course ×3", "→ fact 4, 5, 6", "→ facts 4, 5, 6"),
       ("2 นับสัปดาห์", "2 Count the weeks", "days_between", "→ 35 วัน = 5 สัปดาห์", "→ 35 days = 5 weeks"),
       ("3 เขียนแผน", "3 Write the plan", "(LLM writes)", "ตาราง: สัปดาห์ หัวข้อ งาน", "table: week, topics, task"),
       ("4 เพิ่ม 5 รอบทบทวน", "4 Add 5 reviews", "add_to_calendar ×5", "ถามนิสิตก่อน", "ask the student first")]
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
s = Svg(W, "The student asks 'How many days are left until the final exam?'. Left, chain-of-thought alone (a made-up example): "
           "with no tools it reasons from memory, 'final exams are usually in mid-December', 'today is probably early "
           "November', and answers about 42 days, wrong. Right, ReAct: Thought 'I need the exam date', Action "
           "search_course('final exam date'), Observation fact 7, 30 November 2026; Thought 'now today's date', Action "
           "get_today(), Observation 2026-10-26; Thought 'count the days', Action days_between, Observation 35; answer 35 days.")
pic(s, "ag-student-ask", 236, 0, 52, 62)
s.box(296, 10, 588, 44, "nt-bubble", 22)
s.text(590, 39, Q, "pl-text", "middle")
Y = 66
s.box(20, Y + 20, 400, 420, "sw-warn-box", 14)
s.both(40, Y + 52, "✗ CoT อย่างเดียว (ตัวอย่างสมมติ)", "✗ CoT alone (made-up example)", "pl-label")
COT_TH = ["Thought: สอบปลายภาคมักอยู่", "กลางเดือนธันวาคม", "Thought: วันนี้น่าจะต้น พ.ย.", "Thought: ห่างกันราว 6 สัปดาห์"]
COT_EN = ["Thought: final exams are usually", "in mid-December.", "Thought: today is probably early", "November.", "Thought: so about 6 weeks."]
for k, t in enumerate(COT_TH):
    s.raw(f'<text x="40" y="{Y + 92 + k * 30}" class="pl-text" data-only="th">{escape(t)}</text>')
for k, t in enumerate(COT_EN):
    s.raw(f'<text x="40" y="{Y + 92 + k * 30}" class="pl-text" data-only="en" lang="en">{escape(t)}</text>')
s.box(40, Y + 254, 360, 44, "ml-cell", 8)
s.both(56, Y + 282, "คำตอบ: ราว 42 วัน", "Answer: about 42 days", "pl-text")
s.both(40, Y + 344, "✗ ใช้แค่สิ่งที่อยู่ในน้ำหนักของโมเดล", "✗ only what is in its weights", "ml-neg")
s.both(40, Y + 374, "ไม่เห็นวันนี้ ไม่เห็นข้อเท็จจริงของเรา", "can't see today or our facts", "pl-note")
s.box(440, Y + 20, 720, 420, "nt-band-a", 14)
s.both(460, Y + 52, "✓ ReAct: Thought → Action → Observation", "✓ ReAct: Thought → Action → Observation", "pl-label")
RE = [("Thought", "ต้องรู้วันสอบก่อน", "I need the exam date first.", False), ("Action", 'search_course("final exam date")', None, True),
      ("Observation", "[fact 7] … Monday 30 November 2026", None, True),
      ("Thought", "ต่อไปคือวันที่ของวันนี้", "Now today's date.", False), ("Action", "get_today()", None, True), ("Observation", "2026-10-26", None, True),
      ("Thought", "นับวัน", "Count the days.", False), ("Action", 'days_between("2026-10-26", "2026-11-30")', None, True), ("Observation", "35", None, True)]
for k, (lab, a, b, code) in enumerate(RE):
    y = Y + 76 + k * 34
    cls = {"Thought": "ml-cell", "Action": "pl-chip", "Observation": "nt-bubble"}[lab]
    s.box(460, y, 130, 28, cls, 6)
    s.text(525, y + 20, lab, "hk-desc", "middle")
    if code:
        s.code(604, y + 19, a, bold=(lab == "Observation"))
    else:
        s.both(604, y + 21, a, b, "hk-desc")
s.box(460, Y + 386, 680, 40, "nt-out", 8)
s.both(476, Y + 412, "คำตอบ: 35 วัน (จันทร์ 30 พ.ย.) ✓ อิงข้อมูลจริงทุกขั้น", "Answer: 35 days (Mon 30 Nov) ✓ every step grounded in real data", "ml-ok")
s.save("l14-react.svg", Y + 456)

# ---------------------------------------------------------------- 16b. ReAct 2022 vs a 2026 agent
s = Svg(W, "Left, ReAct as written in 2022: the model writes Thought, Action and Observation lines as text, one action per "
           "step, and code parses the text: Thought 'I need the exam date', Action search_course, Observation fact 7, then "
           "get_today, then days_between, then the answer 35 days. Right, a 2026 agent: the same core loop (think, act, "
           "observe), but the thinking is hidden, the actions are typed function calls, several at once, and a harness "
           "around the loop adds a plan (write_todos), files (/study_plan.md), checkpoints (thread_id), a check before done "
           "(read_file), sub-agents (task), permission (approve before add_to_calendar), context management (summarise at "
           "85%) and a trace (LangSmith).")
s.box(20, 20, 470, 420, "ml-cell", 14)
s.both(40, 52, "ReAct ปี 2022: ไอเดียต้นแบบ", "ReAct, 2022: the idea", "pl-label")
s.both(40, 78, "โมเดลเขียนทุกบรรทัดเป็นข้อความ", "the model writes every line as text", "pl-note")
TR = [("Thought:", "I need the exam date."), ("Action:", "search_course[final exam]"), ("Observation:", "[fact 7] … 30 Nov 2026"),
      ("Thought:", "Now today's date."), ("Action:", "get_today[]"), ("Observation:", "2026-10-26"),
      ("Thought:", "Count the days."), ("Action:", "days_between[…]"), ("Observation:", "35"), ("Answer:", "35 days")]
for k, (a, b) in enumerate(TR):
    y = 104 + k * 26
    s.code(40, y, a, bold=True)
    s.code(160, y, b)
s.both(40, 386, "✓ ลูปนี้ยังเป็นแกนของ agent ทุกตัว", "✓ this loop is still the core of every agent", "ml-ok")
s.both(40, 414, "✗ thought เป็นข้อความ · ครั้งละ 1 action", "✗ thoughts as text · one action per step", "ml-neg")
s.box(510, 20, 650, 420, "nt-band-a", 14)
s.both(530, 52, "agent ปี 2026: ลูปเดิม อยู่ใน harness", "A 2026 agent: the same loop inside a harness", "pl-label")
s.box(704, 74, 244, 300, "ml-cell", 12)
s.both(826, 100, "ลูปแกน (ReAct)", "core loop (ReAct)", "pl-label", "middle")
pic(s, "ag-robot-think", 781, 108, 90, 100)
LOOP = [("คิด (ซ่อนอยู่)", "think (hidden)"), ("ลงมือ: เรียกหลาย tool", "act: several calls"), ("สังเกตผล", "observe results")]
for k, (th, en) in enumerate(LOOP):
    s.chip(716, 220 + k * 48, 200, 36, th, en, "nt-out" if k == 1 else "ml-cell-b")
    if k < 2:
        s.arrow(816, 258 + k * 48, 816, 266 + k * 48)
s.path("M918 334 L934 334 L934 238 L920 238")
s.head(934, 238, 920, 238)
TILES14 = [("แผน", "Plan", "write_todos", "icon-clipboard"), ("ไฟล์", "Files", "study_plan.md", "icon-folder"),
           ("checkpoint", "Checkpoints", "thread_id", "icon-save"), ("ตรวจก่อนจบ", "Check first", "read_file", "icon-magnifier"),
           ("sub-agent", "Sub-agents", "task(...)", "ag-robot-mini"), ("ขออนุญาต", "Permission", "approve?", "ag-staff-ok"),
           ("ย่อ context", "Context", "summarise", "icon-scissors"), ("trace", "Trace", "LangSmith", "icon-notepad")]
for k, (th, en, c, picname) in enumerate(TILES14):
    x = 524 if k < 4 else 960
    y = 74 + (k % 4) * 76
    s.box(x, y, 172 if k < 4 else 186, 64, "ml-cell", 10)
    pic(s, picname, x + 8, y + 12, 40, 40, "xMidYMid")
    s.both(x + 56, y + 28, th, en, "hk-desc")
    s.code(x + 56, y + 50, c)
s.both(530, 404, "✓ ลูปเหมือนเดิม สิ่งที่ใหม่คือ harness รอบลูป", "✓ the loop is the same; the harness around it is new", "ml-ok")
s.save("l14-react-2026.svg", 456)

# ---------------------------------------------------------------- 17a. hidden thinking (real run)
s = Svg(W, "A real run of our loop with gemini-3.8-flash and include_thoughts on. Round 1: 116 hidden thinking tokens, a summary "
           "titled 'Calculating Days Until the Final Exam', then get_today() → 2026-10-26 and search_course('final exam date') → "
           "fact 7. Round 2: 85 thinking tokens, a summary that starts 'Okay, here's my take on those thoughts', then "
           "days_between('2026-10-26', '2026-11-30') → 35. Round 3: 71 thinking tokens, 'Verifying the Timeframe', then the "
           "answer, 35 days. The thinking itself stays hidden; the summary is a rewrite of it for readers.")
pic(s, "ag-student-ask", 236, 0, 52, 62)
s.box(296, 10, 588, 44, "nt-bubble", 22)
s.text(590, 39, Q, "pl-text", "middle")
Y = 70
pic(s, "ag-robot-think", 20, Y + 40, 180, 220)
s.both(110, Y + 290, "Gemini 3.8 Flash", "Gemini 3.8 Flash", "pl-label", "middle")
s.both(110, Y + 316, "เปิด include_thoughts", "include_thoughts on", "pl-note", "middle")
s.both(340, Y + 8, "สิ่งที่โมเดลทำ (ซ่อนอยู่) และสรุปที่มันให้ดู", "what it did (hidden), and the summary it shows", "pl-note")
s.both(790, Y + 8, "สิ่งที่มันขอ", "what it asked for", "pl-note")
ROUNDS = [(116, "“Calculating Days Until the Final Exam”", ["get_today() → 2026-10-26", "search_course(...) → fact 7"], False),
          (85, "“Okay, here's my take on those thoughts…”", ["days_between(...) → 35"], False),
          (71, "“Verifying the Timeframe”", ["“There are 35 days left…”"], True)]
for k, (tok, summ, acts, final) in enumerate(ROUNDS):
    y = Y + 20 + k * 112
    s.box(220, y, 940, 100, "ml-cell", 12)
    s.both(238, y + 32, f"รอบ {k + 1}", f"Round {k + 1}", "pl-label")
    s.both(340, y + 30, f"thinking ที่ซ่อนอยู่: {tok} token", f"hidden thinking: {tok} tokens", "hk-desc")
    s.box(340, y + 40, tok * 2.6, 14, "ml-model", 3)
    s.text(340, y + 82, summ, "pl-note")
    s.arrow(764, y + 50, 784, y + 50)
    s.box(790, y + 14, 354, 72, "nt-out" if final else "pl-chip", 10)
    for j, a in enumerate(acts):
        if final:
            s.text(806, y + 56, a, "pl-text")
        else:
            s.code(806, y + (56 if len(acts) == 1 else 44 + j * 24), a)
s.both(220, Y + 374, "✓ 3 รอบเหมือนลูป ReAct · ✗ สรุปคือการเขียนใหม่ ไม่ใช่ตัวเหตุผล · thinking token คิดเงินเหมือน output",
       "✓ the same 3 rounds as the ReAct loop · ✗ the summary is a rewrite, not the reasoning · thinking tokens are billed", "pl-text")
s.save("l14-thinking.svg", Y + 392)

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
pic(s, "ag-robot-think", 260, 168, 150, 140)
s.both(220, 330, "✗ window เต็ม", "✗ the window fills;", "ml-neg")
s.both(220, 358, "สิ่งสำคัญจมหาย", "what matters gets lost", "ml-neg")
s.box(480, 20, 680, 420, "nt-band-a", 14)
s.both(500, 52, "✓ ผู้จัดการ + worker แต่ละตัวมี window ของตัวเอง", "✓ A manager + workers, each with its own window", "pl-label")
s.llm(730, 72, 180, 56, "Manager", "Manager", ("แบ่งงาน รวมผล", "splits, merges"))
pic(s, "ag-robot-plan", 918, 64, 60, 76)
WK = [("Research", "ค้นและรวบรวม", "search, collect"), ("Analysis", "ดึงผล เปรียบเทียบ", "extract, compare"), ("Writer", "เขียนรายงาน", "write the report")]
for k, (t, th, en) in enumerate(WK):
    x = 500 + k * 220
    s.arrow(820, 130, x + 100, 178)
    s.llm(x, 180, 200, 50, t, t)
    s.box(x + 30, 240, 140, 90, "ml-cell", 8)
    for j in range(3):
        s.box(x + 40, 250 + j * 26, 120, 20, "ml-cell-b", 4)
    s.both(x + 100, 352, th, en, "pl-note", "middle")
    pic(s, "ag-robot-mini", x + 160, 268, 40, 62)
s.both(500, 392, "แต่ละตัวส่งสรุปกลับ ≈ 1,000–2,000 token", "each returns a summary of ≈ 1,000–2,000 tokens", "pl-text")
s.both(500, 422, "✓ +90.2% เทียบ agent ตัวเดียว", "✓ +90.2% vs one agent", "ml-ok")
s.both(830, 422, "✗ token ≈ 15 เท่าของแชต", "✗ ≈ 15× a chat's tokens", "ml-neg")
s.save("l14-multi-agent.svg", 456)

# ---------------------------------------------------------------- 20. context growth (real Gemini counts)
s = Svg(W, "Left, our question with Gemini's real input-token counts per call (gemini-3.5-flash-lite): call 1 reads 256 tokens "
           "(the tool schemas, about 245, and the question, 11), call 2 538, call 3 591, as each call and result is added; "
           "1,385 tokens read to write 102. Right, a long research job with example sizes: each web page the agent reads stays "
           "in the context, so after 10, 20, 30 and 40 steps it holds about 50,000 to 200,000 tokens. Our study-plan job as a "
           "Deep Agent: 12 calls read 97,743 tokens. Chroma found 18 models do worse as input grows.")
s.box(20, 20, 560, 420, "ml-cell", 14)
s.both(40, 52, "คำถามของเรา: input token จริงต่อครั้ง", "Our question: real input tokens per call", "pl-label")
SEG = [(245, "ml-bar"), (11, "ml-model")]
CALLSZ = [256, 538, 591]
sc = 380 / 600
for k, tot in enumerate(CALLSZ):
    y = 84 + k * 64
    s.both(40, y + 24, f"ครั้งที่ {k + 1}", f"call {k + 1}", "pl-text")
    x = 120
    for v, cls in SEG:
        s.box(x, y + 4, v * sc, 30, cls, 2)
        x += v * sc
    if tot > 256:
        s.box(x, y + 4, (tot - 256) * sc, 30, "sw-chip-warn", 2)
    s.text(120 + tot * sc + 8, y + 26, str(tot), "pl-label")
s.box(40, 290, 16, 16, "ml-bar", 2)
s.both(62, 304, "tool schema ≈ 245", "tool schemas ≈ 245", "pl-note")
s.box(240, 290, 16, 16, "ml-model", 2)
s.both(262, 304, "คำถาม 11", "question 11", "pl-note")
s.box(390, 290, 16, 16, "sw-chip-warn", 2)
s.both(412, 304, "call + ผล", "calls + results", "pl-note")
s.both(40, 370, "รวม: อ่าน 1,385 token เพื่อเขียน 102", "In total: 1,385 tokens read to write 102", "pl-text")
s.both(40, 404, "ทุกครั้งที่เรียก ส่งทุกอย่างไปใหม่", "every call resends everything", "pl-note")
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
s.both(620, 392, "แผนอ่านหนังสือของเรา: 12 ครั้ง อ่าน 97,743 token", "our study plan: 12 calls read 97,743 tokens", "pl-text")
s.both(620, 420, "✗ Chroma: 18 โมเดลแย่ลงเมื่อ input ยาวขึ้น", "✗ Chroma: 18 models do worse as input grows", "ml-neg")
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

# ---------------------------------------------------------------- 21c. the context window (real tokens)
s = Svg(W, "The context window: everything the model reads on one call, in order. Rules (a system prompt, if any), the tool "
           "descriptions (about 245 tokens), the student's question (11), then everything from earlier rounds: Gemini's own "
           "tool calls and the tool results (282 tokens after round 1, 53 more after round 2); then the model predicts the "
           "next token. On call 3 of our question that is 591 tokens. Every call resends the whole window: 256, 538, 591 "
           "tokens. The study-plan job read 97,743 tokens in 12 calls, the biggest 14,565. Every token is billed on every "
           "call, long inputs are slower, and models do worse as the input grows (Chroma tested 18).")
s.both(20, 34, "context window = ทุกอย่างที่โมเดลอ่านในการเรียก 1 ครั้ง", "The context window = everything the model reads on one call", "pl-label")
SRC = [("icon", "notepad", "กฎ (system prompt)", "rules (system prompt)", 120),
       ("icon", "tools", "คำอธิบาย tool", "tool descriptions", 300),
       ("pic", "ag-student-ask", "คำถาม", "the question", 455),
       ("pic", "ai-robot", "call เดิมของโมเดล", "its own past calls", 600),
       ("icon", "magnifier", "ผลของ tool", "tool results", 800)]
for kind, name, th, en, cx in SRC:
    if kind == "icon":
        ic(s, name, cx, 82, 52)
    else:
        pic(s, name, cx - 30, 52, 60, 62, "xMidYMid")
    s.both(cx, 136, th, en, "hk-desc", "middle")
    s.arrow(cx, 144, cx, 176)
# the bar on call 3 of our question: 245 + 11 + 282 + 53 = 591 tokens
X, SC, Y = 40, 1.48, 180
SEG = [(16, "pl-chip-del", "none here"), (245, "ml-bar", "≈245"), (11, "ml-model", "11"), (282, "sw-chip-warn", "282"), (53, "sw-chip-warn", "53")]
x = X
for tok, cls, lab in SEG:
    w = 24 if tok == 16 else tok * SC
    s.box(x, Y, w, 44, cls, 3)
    if lab == "none here":
        s.both(x, Y + 66, "ไม่มีในรอบนี้", "none here", "hk-desc")
    elif lab:
        s.text(x + w / 2, Y + 66, lab, "hk-desc", "middle")
    x += w + 2
s.box(x + 6, Y, 1150 - x - 6, 44, "nt-out", 3)
s.both(x + 20, Y + 28, "→ token ถัดไป", "→ next token", "pl-text")
s.both(X, Y + 92, "การเรียกครั้งที่ 3 ของคำถามเรา: 591 token · รอบก่อนหน้า (call + ผล): 282 + 53",
       "Call 3 of our question: 591 tokens · earlier rounds (calls + results): 282 + 53", "pl-note")
# why it runs out
s.box(20, 296, 560, 200, "ml-cell", 14)
s.both(40, 326, "ส่งทั้ง window ไปใหม่ทุกครั้ง", "Every call resends the whole window", "pl-label")
for k, tok in enumerate([256, 538, 591]):
    y = 344 + k * 40
    s.both(40, y + 22, f"ครั้งที่ {k + 1}", f"call {k + 1}", "hk-desc")
    s.box(110, y + 4, tok * 0.6, 26, "ml-bar", 3)
    s.text(116 + tok * 0.6, y + 23, str(tok), "pl-label")
s.both(40, 482, "งานยาว: แผนอ่านหนังสือ 12 ครั้ง อ่าน 97,743 token", "a long job: the study plan, 12 calls, 97,743 tokens read", "pl-text")
s.box(600, 296, 560, 200, "sw-warn-box", 14)
s.both(620, 326, "ทำไม window ใหญ่ ๆ จึงเป็นปัญหา", "Why a big window is a problem", "pl-label")
WHY = [("moneybag", "คิดเงินทุก token ทุกครั้งที่เรียก", "every token is billed, on every call"),
       ("stopwatch", "input ยาว = ตอบช้าลง", "a longer input is slower"),
       ("brain", "โมเดลแย่ลงเมื่อ input ยาว (Chroma, 18 โมเดล)", "models do worse as it grows (Chroma, 18)")]
for k, (icon, th, en) in enumerate(WHY):
    y = 344 + k * 48
    ic(s, icon, 640, y + 16, 34)
    s.both(668, y + 23, th, en, "pl-text")
s.save("l14-context-window.svg", 512)

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
# ---------------------------------------------------------------- 10. the agent loop by hand (real Gemini run)
s = Svg(W, "Left: run_agent in four steps: 1 ask the model with the messages and tools; 2 no function call means done, return "
           "the text; 3 run each requested function in our code; 4 append the results to the messages and loop, at most "
           "MAX_STEPS = 10 times. Right: the real run with gemini-3.5-flash-lite. Round 1: get_today() → 2026-10-26 and "
           "search_course('final exam') → fact 7, in the same turn. Round 2: days_between('2026-10-26', '2026-11-30') → 35. "
           "Round 3: the answer, 35 days. The message list grows from 1 to 6.")
s.box(20, 20, 430, 440, "ml-cell", 14)
s.both(40, 52, "ลูปของ run_agent", "The loop in run_agent", "pl-label")
STEPS = [("ถามโมเดล", "Ask the model", "messages + tools"),
         ("ไม่มี call → จบ", "No call → done", "return response.text"),
         ("รันทุก call", "Run each call", "TOOLS[call.name](**args)"),
         ("ส่งผลกลับ", "Send results back", "messages.append(results)")]
for k, (th, en, c) in enumerate(STEPS):
    y = 72 + k * 84
    s.box(40, y, 390, 68, "nt-out" if k == 1 else "ml-cell-b", 10)
    s.num(62, y + 22, k + 1)
    s.both(84, y + 28, th, en, "pl-text")
    s.code(84, y + 54, c)
    if k < 3:
        s.arrow(235, y + 70, 235, y + 82)
s.path("M430 344 L444 344 L444 106 L432 106")
s.head(444, 106, 432, 106)
s.both(40, 420, "วนไม่เกิน MAX_STEPS = 10 รอบ", "at most MAX_STEPS = 10 rounds", "pl-note")
s.box(470, 20, 690, 440, "nt-band-a", 14)
s.both(490, 52, "การรันจริง: messages โตขึ้นทีละรอบ", "The real run: messages grow each round", "pl-label")
ROWS = [("user", "How many days are left until the final exam?", None, 1),
        ("model", "get_today()  +  search_course('final exam')", "รอบ 1|round 1", 2),
        ("user", "2026-10-26  ·  [fact 7] final exam, Mon 30 Nov", None, 3),
        ("model", "days_between('2026-10-26', '2026-11-30')", "รอบ 2|round 2", 4),
        ("user", "35", None, 5),
        ("model", "There are 35 days left until the final exam.", "รอบ 3|round 3", 6)]
for k, (role, txt, rnd, n) in enumerate(ROWS):
    y = 72 + k * 58
    s.box(486, y, 74, 40, "nt-bubble" if role == "user" else "ml-model", 8)
    s.text(523, y + 26, role, "hk-desc" if role == "user" else "ml-model-sub", "middle")
    s.box(568, y, 470, 40, "nt-out" if k == 5 else ("pl-chip" if role == "user" and k else "ml-cell"), 8)
    s.code(580, y + 26, txt, bold=(role == "user" and k > 0))
    s.text(1144, y + 26, f"{n}", "pl-label", "end")
    if rnd:
        th, en = rnd.split("|")
        s.both(1056, y + 26, th, en, "pl-note")
s.both(1144, 64, "len", "len", "pl-note", "end")
s.both(490, 430, "โมเดลเลือกแต่ละขั้น ลูปของเราเป็นคนรัน", "the model chose each step; our loop ran it", "ml-ok")
s.save("l14-loop.svg", 476)


# ---------------------------------------------------------------- 15b. the library stack
s = Svg(W, "Left: what create_agent does for each line of run_agent: keeps the message list, sends it with the tool schemas, "
           "runs the requested tools and sends the results back, stops when a reply has no tool call; the model is a string such "
           "as google_genai:gemini-3.5-flash-lite. Right: the stack. LangGraph at the bottom runs the graph (state, checkpoints, "
           "pausing); LangChain's create_agent builds the agent and takes middleware; Deep Agents' create_deep_agent adds plans, "
           "files, sub-agents and context management; LangSmith, beside all three, records traces and scores runs.")
s.box(20, 20, 540, 420, "ml-cell", 14)
s.both(40, 52, "run_agent ของเรา → create_agent", "our run_agent → create_agent", "pl-label")
MAP = [("messages = [...]", "เก็บ list ข้อความให้", "keeps the message list"),
       ("generate_content(tools=...)", "ส่ง schema ไปทุกครั้ง", "sends the schemas every call"),
       ("TOOLS[call.name](**args)", "รัน tool ที่ขอ", "runs the requested tools"),
       ("if not function_calls: return", "หยุดเมื่อไม่มี tool call", "stops when there is no call"),
       ('model="gemini-..." (Gemini only)', "โมเดลเป็นข้อความ เปลี่ยนเจ้าได้", "the model is a string: any provider")]
for k, (c, th, en) in enumerate(MAP):
    y = 70 + k * 72
    s.box(40, y, 500, 60, "ml-cell-b", 10)
    s.code(56, y + 24, c)
    s.both(56, y + 48, "→ " + th, "→ " + en, "ml-ok")
s.box(580, 20, 580, 420, "nt-band-a", 14)
s.both(600, 52, "ชั้นของไลบรารี", "The stack", "pl-label")
LAYERS = [("Deep Agents", "create_deep_agent", "แผน · ไฟล์ · sub-agent · ย่อ context", "plans · files · sub-agents · context", "nt-out"),
          ("LangChain", "create_agent + middleware", "สร้าง agent · เสียบ guardrail และขีดจำกัด", "builds the agent · guardrails, limits", "ml-cell"),
          ("LangGraph", "StateGraph · checkpointer", "ตัวรัน: state · checkpoint · หยุดรอ", "runtime: state · checkpoints · pause", "ml-cell-b")]
for k, (name, api, th, en, cls) in enumerate(LAYERS):
    y = 72 + k * 112
    s.box(600, y, 420, 100, cls, 12)
    s.text(620, y + 32, name, "pl-label")
    s.code(620, y + 58, api)
    s.both(620, y + 86, th, en, "pl-note")
    ic(s, ["clipboard", "puzzle", "loop"][k], 982, y + 34, 44)
s.box(1036, 72, 108, 324, "pl-chip", 12)
ic(s, "magnifier", 1090, 150, 50)
s.text(1090, 210, "Lang", "pl-label", "middle")
s.text(1090, 236, "Smith", "pl-label", "middle")
s.both(1090, 270, "trace", "traces", "pl-note", "middle")
s.both(1090, 294, "ประเมิน", "& evals", "pl-note", "middle")
s.both(600, 424, "ชั้นบนใช้ชั้นล่าง: เลือกใช้ชั้นที่พอกับงาน", "each layer uses the one below: pick what the job needs", "pl-note")
s.save("l14-stack.svg", 456)


# ---------------------------------------------------------------- 16b. middleware hooks
s = Svg(W, "The agent loop with its middleware hook points: before_model and after_model run just before and after each LLM "
           "call, wrap_model_call wraps the call itself, wrap_tool_call wraps each tool run. Our log_and_check is a "
           "wrap_tool_call: in the real run it let search_course and days_between through, rejected add_to_calendar on "
           "2026-10-20 because it is before today (2026-10-26), and let 2026-11-23 through, so the calendar ended with one event. "
           "Below, LangChain's built-in middleware by job: context, retries, budgets, safety, planning.")
s.box(20, 20, 700, 300, "ml-cell", 14)
s.both(40, 52, "จุดเสียบรอบลูป", "Hook points around the loop", "pl-label")
s.box(60, 112, 190, 40, "pl-chip", 8)
s.code(74, 138, "before_model")
s.arrow(252, 132, 286, 132)
s.box(290, 82, 180, 110, "sw-chip-warn", 12)
s.code(302, 104, "wrap_model_call")
s.llm(310, 114, 140, 64, "LLM", "LLM")
s.arrow(472, 132, 506, 132)
s.box(510, 112, 190, 40, "pl-chip", 8)
s.code(524, 138, "after_model")
s.box(290, 222, 180, 82, "sw-chip-warn", 12)
s.code(302, 244, "wrap_tool_call")
s.chip(310, 256, 140, 36, "tools", "tools", "ml-cell-b")
s.arrow(380, 194, 380, 220)
s.path("M290 262 L200 262 L200 154")
s.head(200, 262, 200, 154)
s.both(392, 214, "tool call", "tool call", "pl-note")
s.both(40, 300, "ผล → กลับไปที่โมเดล", "result → back to the model", "pl-note")
s.box(740, 20, 420, 300, "nt-band-a", 14)
s.both(760, 52, "log_and_check (การรันจริง)", "log_and_check (real run)", "pl-label")
ic(s, "shield", 1124, 44, 32)
LOG = [("search_course", "final exam", True), ("days_between", "11-23 → 11-30", True),
       ("add_to_calendar", "2026-10-20", False), ("add_to_calendar", "2026-11-23", True)]
for k, (t, a, ok) in enumerate(LOG):
    y = 70 + k * 50
    s.box(756, y, 388, 40, "ml-cell-b" if ok else "sw-chip-warn", 8)
    s.code(770, y + 26, t)
    s.code(940, y + 26, a)
    s.text(1132, y + 27, "✓" if ok else "✗", "ml-ok" if ok else "ml-neg", "end")
s.both(760, 296, "✗ วันที่ผ่านไปแล้ว: tool ไม่ถูกรัน", "✗ in the past: the tool never ran", "ml-neg")
GROUPS = [("Context", "Summarization"), ("Retries", "ModelRetry · ToolRetry · ModelFallback"),
          ("Budgets", "ModelCallLimit · ToolCallLimit"), ("Safety", "PII · HumanInTheLoop"), ("Planning", "TodoList")]
s.both(20, 356, "middleware สำเร็จรูปของ LangChain", "LangChain's built-in middleware", "pl-label")
for k, (g, items) in enumerate(GROUPS):
    x, y = 20 + (k % 2) * 575, 372 + (k // 2) * 52
    s.box(x, y, 565, 44, "ml-cell", 10)
    s.text(x + 14, y + 28, g, "pl-label")
    s.code(x + 110, y + 28, items)
s.save("l14-middleware.svg", 532)


# ---------------------------------------------------------------- 18b. human in the loop (real run)
s = Svg(W, "Human in the loop, from the real run. 1 The student asks for a review session one week before the final exam. "
           "2 Gemini asks for add_to_calendar(day 2026-11-23, title 'Review session for the final exam'). 3 The middleware "
           "interrupts: the state is saved in the checkpoint and invoke returns the request; the calendar is still empty. "
           "4 A person chooses approve, edit, reject or respond. 5 Command(resume=approve) continues at the same step: the tool "
           "runs and the calendar has one event.")
STAGE_PIC = [("pic", "ag-student-ask"), ("pic", "ag-robot-tools"), ("icon", "pause"), ("pic", "ag-staff-ok"), ("pic", "ag-student-happy")]
STAGES = [("ขอ", "Ask", ["“review session one", "week before the", "final exam”"], "nt-bubble"),
          ("Gemini ขอ", "Gemini asks", ["add_to_calendar(", " '2026-11-23',", " 'Review session…')"], "ml-cell"),
          ("หยุด", "Pause", ["state → checkpoint", "__interrupt__", "calendar = []"], "sw-warn-box"),
          ("คนตัดสินใจ", "A person decides", ["approve · edit", "reject · respond", "(maybe hours later)"], "ml-cell"),
          ("ทำต่อ", "Resume", ["tool runs", "calendar = 1 event", "Gemini answers"], "nt-out")]
for k, (th, en, lines, cls) in enumerate(STAGES):
    x = 20 + k * 230
    s.box(x, 20, 216, 300, cls, 14)
    s.num(x + 26, 50, k + 1)
    s.both(x + 48, 56, th, en, "pl-label")
    kind, name = STAGE_PIC[k]
    if kind == "pic":
        pic(s, name, x + 48, 70, 120, 112)
    else:
        ic(s, name, x + 108, 124, 84)
    if k == 4:
        ic(s, "calendar", x + 176, 160, 40)
    for j, t in enumerate(lines):
        s.code(x + 16, 214 + j * 32, t) if k in (1, 2) else s.text(x + 16, 214 + j * 32, t, "pl-text")
    if k < 4:
        s.arrow(x + 218, 170, x + 228, 170)
s.box(20, 340, 1140, 120, "ml-cell", 14)
s.code(40, 372, "HumanInTheLoopMiddleware(interrupt_on={\"add_to_calendar\": True})   # which tools stop first")
s.code(40, 406, "careful.invoke(Command(resume={\"decisions\": [{\"type\": \"approve\"}]}), thread)")
s.both(40, 442, "ต้องมี checkpointer: การรันหยุด แล้วกลับมาทำต่อจาก state ที่บันทึกไว้", "needs a checkpointer: the run stops, then continues from the saved state", "pl-note")
s.save("l14-hitl.svg", 476)

# ---------------------------------------------------------------- 21a. three ways to build the agent (tick table)
s = Svg(W, "Three ways to build the same agent. Write it yourself (run_agent, 20 lines): you write every part, the loop too. create_agent (LangChain, 4 lines): the loop and any model are built in; guardrails and limits, saving "
           "state and asking a person, a to-do plan and context management are one line each; files and sub-agents you write. "
           "create_deep_agent (Deep Agents, 5 lines): files, sub-agents and context management are built in too; guardrails, "
           "asking a person and the to-do plan are one line. Best for: learning, most apps, long jobs.")
COLS = [("icon-coder", "เขียนเอง", "Write it yourself", "run_agent · 20 บรรทัด", "run_agent · 20 lines", "ml-cell"),
        ("icon-puzzle", "create_agent", "create_agent", "LangChain · 4 บรรทัด", "LangChain · 4 lines", "ml-cell"),
        ("ag-robot-plan", "create_deep_agent", "create_deep_agent", "Deep Agents · 5 บรรทัด", "Deep Agents · 5 lines", "nt-band-a")]
X0, CW = 400, 248
s.box(20, 20, 368, 108, "ml-cell", 14)
for k, (mark, cls, th, en) in enumerate([("✓", "ml-ok", "มีให้แล้ว", "built in"), ("＋", "pl-label", "เพิ่ม 1 บรรทัด", "one line to add"),
                                        ("✗", "ml-neg", "ต้องเขียนเอง", "you write it")]):
    s.raw(f'<text x="48" y="{56 + k * 30}" class="{cls}" text-anchor="middle" style="font-size:24px">{mark}</text>')
    s.both(72, 54 + k * 30, th, en, "hk-desc")
for k, (picname, nth, nen, lth, len_, cls) in enumerate(COLS):
    x = X0 + k * (CW + 8)
    s.box(x, 20, CW, 108, cls, 14)
    pic(s, picname, x + 8, 28, 56, 56, "xMidYMid")
    s.both(x + 70, 54, nth, nen, "pl-label")
    s.both(x + 70, 80, lth, len_, "hk-desc")
ROWS = [("ลูป: เรียก รัน tool วนซ้ำ", "The loop: call, run tools, repeat", "✗✓✓"),
        ("ใช้โมเดลเจ้าไหนก็ได้", "Any model: Gemini, GPT, Claude", "✗✓✓"),
        ("guardrail และขีดจำกัด", "Guardrails and limits", "✗＋＋"),
        ("บันทึก state และถามคน", "Save state, ask a person", "✗＋＋"),
        ("แผนแบบ to-do", "A to-do plan", "✗＋＋"),
        ("ไฟล์: ls อ่าน เขียน", "Files: ls, read, write", "✗✗✓"),
        ("sub-agent", "Sub-agents", "✗✗✓"),
        ("จัดการ context", "Context management", "✗＋✓")]
MARK_CLS = {"✓": "ml-ok", "＋": "pl-label", "✗": "ml-neg"}
for r, (th, en, marks) in enumerate(ROWS):
    y = 140 + r * 40
    s.box(20, y, 1140, 34, "ml-cell" if r % 2 == 0 else "ml-cell-b", 6)
    s.both(36, y + 23, th, en, "hk-desc")
    for k, m in enumerate(marks):
        s.raw(f'<text x="{X0 + k * (CW + 8) + CW / 2:g}" y="{y + 27}" class="{MARK_CLS[m]}" text-anchor="middle" style="font-size:26px">{m}</text>')
y = 140 + len(ROWS) * 40 + 6
s.both(36, y + 30, "เหมาะกับ", "Best for", "pl-label")
for k, (th, en) in enumerate([("เรียนรู้ว่าทำงานอย่างไร", "learning how it works"), ("แอปส่วนใหญ่ งานสั้น", "most apps, short tasks"),
                              ("งานยาวหลายขั้น", "long, many-step jobs")]):
    x = X0 + k * (CW + 8)
    s.box(x, y, CW, 46, "nt-out", 10)
    s.both(x + CW / 2, y + 29, th, en, "hk-desc", "middle")
s.save("l14-three-ways.svg", y + 60)

# ---------------------------------------------------------------- 21b. Deep Agents (real run)
DEEP = [("gather", "รวบรวม", ["1 get_today()", "2 search_course(k=7) → all 7 facts", "3 days_between → 35"]),
        ("plan", "วางแผน", ["4 write_todos([...steps])"]),
        ("look", "ดูรอบ ๆ", ["5 ls('/')", "6 ls('/workspace')"]),
        ("act", "ลงมือ", ["8–12 add_to_calendar ×5: Sun 1 … 29 Nov"]),
        ("write", "เขียน", ["14 write_file('/study_plan.md')"]),
        ("check", "ตรวจ", ["15 read_file('/study_plan.md')"]),
        ("tick", "ติ๊ก", ["7, 13, 16 write_todos: tick items off"])]
s = Svg(W, "Left: what create_deep_agent adds to create_agent: planning (write_todos), a file system (ls, read_file, write_file, "
           "edit_file, glob, grep), sub-agents (task) and context management (big results to files, summarise old messages). "
           "Right: the real run of the study-plan job with gemini-3.8-flash, 16 tool calls in 12 model calls: gather (get_today, "
           "one search_course with k 7, days_between 35), plan (write_todos), look around (ls twice), act (five add_to_calendar, "
           "Sundays 1 to 29 November), write the plan file, read it back, and tick off the to-do list. Input: 97,743 tokens.")
s.box(20, 20, 420, 450, "ml-cell", 14)
s.both(40, 52, "create_deep_agent เพิ่มอะไร", "What create_deep_agent adds", "pl-label")
ADD = [("วางแผน", "Planning", "write_todos"), ("ระบบไฟล์", "Files", "ls · read/write/edit_file · grep"),
       ("sub-agent", "Sub-agents", "task(description, subagent_type)"), ("จัดการ context", "Context", "big results → files · summarise")]
ADD_PIC = ["ag-robot-plan", "icon-folder", "ag-robot-mini", "icon-scissors"]
for k, (th, en, c) in enumerate(ADD):
    y = 70 + k * 92
    s.box(40, y, 380, 80, "nt-band-a", 10)
    s.both(56, y + 30, th, en, "pl-label")
    s.code(56, y + 60, c)
    pic(s, ADD_PIC[k], 362, y + 6, 52, 52, "xMidYMid")
s.both(40, 450, "+ tool ของเรา 4 ตัว", "+ our 4 tools", "pl-note")
s.box(460, 20, 700, 450, "nt-band-a", 14)
s.both(480, 52, "การรันจริง: 16 การเรียก tool", "The real run: 16 tool calls", "pl-label")
y = 66
n = 1
for name, th, calls in DEEP:
    h = 26 * len(calls) + 10
    s.box(476, y, 668, h, "nt-out" if name in ("write", "check") else ("sw-chip-warn" if name == "act" else "ml-cell"), 8)
    s.both(490, y + 23, th, name, "hk-desc")
    for j, c in enumerate(calls):
        s.code(596, y + 23 + j * 26, c)
    y += h + 6
s.both(480, 456, "12 ครั้งที่เรียกโมเดล · input 97,743 token", "12 model calls · 97,743 input tokens", "pl-note")
s.save("l14-deep.svg", 486)

# ---------------------------------------------------------------- 30b. reading a trace: two real runs
RUN1 = "pgssssssssssssssssssssssssssssssssssffssssdssssssssssssssssfpdddd"
RUN2 = "gsdpffpaaaaapwrp"
KIND = {"s": "nt-hub", "p": "ml-model", "g": "ml-bar", "d": "ml-bar", "f": "dg-hl-col",
        "a": "nt-out", "w": "nt-out", "r": "nt-out"}
s = Svg(W, "Two real runs of the study-plan job with gemini-3.8-flash, one square per tool call. Top, before search_course had "
           "k: 65 tool calls, 54 of them searches with queries such as 'November 9', 'fact 8', 'fact 9', 'fact 10' and "
           "'professor'; after 22 model calls and 167,828 input tokens it stopped with an empty reply, no plan and no events. "
           "Middle, the fix in the tool: a k parameter whose docstring says there are 7 facts in all. Bottom, after: 16 tool "
           "calls, one search with k 7, 12 model calls, 97,743 input tokens, the plan file and 5 calendar events.")
s.box(20, 20, 1140, 196, "sw-warn-box", 14)
s.both(40, 52, "✗ ก่อน: search_course คืนครั้งละ 1 fact", "✗ Before: search_course returns 1 fact per call", "pl-label")
for k, c in enumerate(RUN1):
    x, y = 40 + (k % 33) * 33, 70 + (k // 33) * 34
    s.box(x, y, 28, 28, KIND[c], 4)
for k, q in enumerate(["“November 9”", "“fact 8”", "“fact 9”", "“fact 10”", "“professor”"]):
    s.box(40 + k * 150, 146, 140, 30, "ml-cell", 8)
    s.text(110 + k * 150, 167, q, "hk-desc", "middle")
s.both(800, 168, "65 tool calls · ค้น 54 ครั้ง", "65 tool calls · 54 searches", "pl-text")
pic(s, "ag-robot-think", 1068, 136, 80, 76)
s.both(40, 204, "เรียกโมเดล 22 ครั้ง · 167,828 token → คำตอบว่าง ไม่มีแผน ไม่มีนัด", "22 model calls · 167,828 tokens → an empty reply, no plan, no events", "ml-neg")
s.box(20, 228, 1140, 86, "ml-cell", 14)
s.both(40, 258, "แก้ที่ tool ไม่ใช่ที่ prompt", "Fix the tool, not the prompt", "pl-label")
s.code(40, 292, 'def search_course(query: str, k: int = 1):  # k: how many facts to return, best first (there are 7 in all)')
s.box(20, 326, 1140, 140, "nt-band-a", 14)
s.both(40, 358, "✓ หลัง: ค้นครั้งเดียวด้วย k=7", "✓ After: one search with k=7", "pl-label")
for k, c in enumerate(RUN2):
    s.box(40 + k * 33, 376, 28, 28, KIND[c], 4)
s.both(600, 398, "16 tool calls · ค้น 1 ครั้ง", "16 tool calls · 1 search", "pl-text")
pic(s, "ag-robot-plan", 1062, 334, 86, 128)
s.both(40, 448, "เรียกโมเดล 12 ครั้ง · 97,743 token → ไฟล์แผน + นัด 5 รายการ", "12 model calls · 97,743 tokens → the plan file + 5 events", "ml-ok")
LEG = [("nt-hub", "search_course"), ("ml-model", "write_todos"), ("ml-bar", "today / days"), ("dg-hl-col", "ls / glob"), ("nt-out", "calendar / file")]
for k, (cls, t) in enumerate(LEG):
    s.box(40 + k * 226, 484, 18, 18, cls, 3)
    s.code(66 + k * 226, 499, t)
s.save("l14-trace.svg", 514)

# ---------------------------------------------------------------- 27b. Artificial Analysis Coding Agent Index (24 Oct 2026)
AA = [  # agent (harness · model), index, FrontierCode v1.1, Terminal-Bench 4.0, SWE-Atlas-QnA-AA; read from the page on 2026-10-24
    ("Claude Code · Opus 5.5", 62, 56, 63, 66), ("Claude Code · Sonnet 5.5", 59, 48, 66, 64),
    ("Muse Code · Muse Wonder Full", 59, 49, 59, 69), ("Codex · GPT-6 Astra", 55, 49, 56, 59),
    ("Codex · GPT-6.1 Sol", 54, 49, 53, 60), ("Antigravity CLI · Gemini 4 Argon", 53, 49, 56, 55),
    ("Grok Build · Grok 4.7", 47, 44, 33, 63), ("Kimi Code CLI · Kimi K3", 41, 43, 21, 60)]
s = Svg(W, "How coding agents are scored today: the Artificial Analysis Coding Agent Index v2.0 (data read on 24 October "
           "2026). What is tested is a harness plus a model as one agent, such as Claude Code with Opus 5.5, not the model "
           "alone. Three benchmarks: FrontierCode v1.1 by Cognition, 100 software engineering tasks with partial credit; "
           "Terminal-Bench 4.0 by Laude Institute, 66 terminal tasks, pass or fail; SWE-Atlas-QnA-AA by Scale AI, 124 "
           "technical questions about a code base, pass or fail. Each score is the mean of 3 attempts per task, and the index "
           "is the plain average of the three. Top rows: Claude Code with Opus 5.5 62 (56, 63, 66); Claude Code with Sonnet "
           "5.5 59; Muse Code with Muse Wonder Full 59; Codex with GPT-6 Astra 55; Codex with GPT-6.1 Sol 54; Antigravity CLI "
           "with Gemini 4 Argon 53; Grok Build with Grok 4.7 47; Kimi Code CLI with Kimi K3 41 (Terminal-Bench only 21).")
# what a benchmark tests: the model inside its harness, as one agent
s.box(20, 14, 1140, 64, "nt-out", 14)
s.both(40, 54, "สิ่งที่ถูกทดสอบ:", "What is tested:", "pl-label")
s.box(220, 24, 250, 44, "ml-cell-b", 10)
pic(s, "icon-tools", 228, 28, 36, 36, "xMidYMid")
s.both(272, 52, "harness: Claude Code", "harness: Claude Code", "hk-desc")
s.text(490, 54, "+", "pl-label", "middle")
s.box(510, 24, 220, 44, "ml-cell-b", 10)
pic(s, "ai-robot", 518, 28, 36, 36, "xMidYMid")
s.both(562, 52, "model: Opus 5.5", "model: Opus 5.5", "hk-desc")
s.text(750, 54, "=", "pl-label", "middle")
s.box(770, 24, 370, 44, "nt-band-a", 10)
s.both(786, 52, "agent เดียว ไม่ใช่โมเดลอย่างเดียว", "one agent, not the model alone", "pl-label")
BENCH = [("icon-coder", "FrontierCode v1.1", "Cognition · 100 งาน", "Cognition · 100 tasks", "งานซอฟต์แวร์ ได้คะแนนบางส่วน", "build features; partial credit"),
         ("icon-laptop", "Terminal-Bench 4.0", "Laude Institute · 66 งาน", "Laude Institute · 66 tasks", "ใช้ terminal ผ่าน/ไม่ผ่าน", "work in a terminal; pass/fail"),
         ("icon-magnifier", "SWE-Atlas-QnA-AA", "Scale AI · 124 งาน", "Scale AI · 124 tasks", "ถามตอบเรื่อง code ผ่าน/ไม่ผ่าน", "code questions; pass/fail")]
for k, (icon, name, bth, ben, dth, den) in enumerate(BENCH):
    x = 20 + k * 384
    s.box(x, 98, 372, 112, "nt-band-a", 14)
    pic(s, icon, x + 14, 112, 54, 54, "xMidYMid")
    s.text(x + 80, 130, name, "pl-label")
    s.both(x + 80, 154, bth, ben, "hk-desc")
    s.both(x + 80, 180, dth, den, "pl-note")
s.box(20, 220, 1140, 38, "nt-out", 10)
s.both(36, 246, "Index = ค่าเฉลี่ยของ 3 คะแนน (น้ำหนักเท่ากัน) · แต่ละคะแนน = ค่าเฉลี่ยจากการทำ 3 ครั้งต่องาน",
       "Index = the average of the 3 scores (equal weight) · each score = the mean of 3 attempts per task", "pl-text")
s.both(36, 288, "agent (harness · โมเดล)", "agent (harness · model)", "pl-note")
s.text(330, 288, "Index", "pl-note")
for k, h in enumerate(["FrontierCode", "Terminal-Bench", "SWE-Atlas"]):
    s.text(820 + k * 124, 288, h, "pl-note", "middle")
for r, (name, idx, fc, tb, sa) in enumerate(AA):
    y = 300 + r * 34
    s.box(20, y, 1140, 28, "ml-cell" if r % 2 == 0 else "ml-cell-b", 5)
    s.text(36, y + 20, name, "hk-desc")
    s.box(330, y + 5, idx * 5.4, 18, "ml-bar-top" if r == 0 else "ml-bar", 3)
    s.text(336 + idx * 5.4, y + 20, str(idx), "pl-label")
    for k, v in enumerate((fc, tb, sa)):
        s.text(820 + k * 124, y + 20, str(v), "ml-neg" if v < 30 else "hk-desc", "middle")
s.both(20, 300 + len(AA) * 34 + 22, "ที่มา: Artificial Analysis, Coding Agent Index v2.0 (อ่านเมื่อ 24 ต.ค. 2026) · 8 จาก 14 agent",
       "Source: Artificial Analysis, Coding Agent Index v2.0 (read 24 Oct 2026) · 8 of 14 agents shown", "pl-note")
s.save("l14-agent-index.svg", 300 + len(AA) * 34 + 36)

# ---------------------------------------------------------------- 27c. score vs cost and time (24 Oct 2026)
TRADE = [("Opus 5.5", 62, 11.42, "1.0h"), ("Sonnet 5.5", 59, 13.30, "1.3h"), ("GPT-6 Astra", 55, 7.04, "24.8m"),
         ("GPT-6.1 Sol", 54, 1.50, "23.7m"), ("Gemini 4 Argon", 53, 5.86, "34.7m"), ("Muse Wonder", 52, 8.05, "24.5m"),
         ("Grok 4.7", 47, 9.48, "35.8m")]
s = Svg(W, "Score is not everything. Left, the Coding Agent Index against the average API cost per task (Artificial Analysis, "
           "24 October 2026): Claude Code with Opus 5.5 scores 62 at $11.42 and about 1.0 hour per task; Codex with GPT-6.1 "
           "Sol scores 54 at $1.50 and 23.7 minutes; Claude Code with Sonnet 5.5 scores 59 at $13.30 and 1.3 hours. Right, "
           "what to measure on your own agent: the outcome, the trajectory, cost and time, safety, and reliability over many "
           "runs (pass^k), with this lesson's examples.")
s.box(20, 20, 600, 440, "ml-cell", 14)
s.both(40, 52, "คะแนน vs ค่าใช้จ่ายต่องาน (และเวลา)", "Index vs cost per task (and time)", "pl-label")
X0, Y0, XW, YH = 90, 400, 500, 300
s.line(X0, Y0, X0 + XW, Y0)
s.line(X0, Y0, X0, Y0 - YH)
for v in (0, 4, 8, 12):
    s.text(X0 + v / 14 * XW, Y0 + 22, f"${v}", "hk-desc", "middle")
for v in (45, 55, 65):
    s.text(X0 - 10, Y0 - (v - 45) / 20 * YH + 6, str(v), "hk-desc", "end")
s.both(X0 + XW / 2, Y0 + 46, "ค่า API เฉลี่ยต่องาน (USD)", "average API cost per task (USD)", "pl-note", "middle")
for name, idx, cost, t in TRADE:
    cx, cy = X0 + cost / 14 * XW, Y0 - (idx - 45) / 20 * YH
    hl = name in ("Opus 5.5", "GPT-6.1 Sol")
    s.raw(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{9 if hl else 6}" class="{"ml-model-done" if hl else "ml-model"}"/>')
    dx, dy, anchor = {"Opus 5.5": (-12, -8, "end"), "Sonnet 5.5": (-12, -8, "end"), "GPT-6 Astra": (12, -8, "start"),
                      "GPT-6.1 Sol": (12, -8, "start"), "Gemini 4 Argon": (-12, 24, "end"), "Muse Wonder": (12, -8, "start"),
                      "Grok 4.7": (12, -8, "start")}[name]
    s.text(cx + dx, cy + dy, f"{name} · {t}", "hk-desc", anchor)
s.box(640, 20, 520, 440, "nt-band-a", 14)
s.both(660, 52, "agent ของเราเอง: วัดอะไรบ้าง", "Your own agent: what to measure", "pl-label")
MEAS = [("target", "ผลลัพธ์: ถูกไหม", "Outcome: is it right?", "35 วัน · แผนแต่งหัวข้อ ✗", "35 days · the plan invented topics ✗"),
        ("magnifier", "เส้นทาง: tool และ argument ถูกไหม", "Trajectory: right tools, right args?", "Qwen 0.6B แต่งวันที่ ✗", "a small model made up dates ✗"),
        ("stopwatch", "ค่าใช้จ่ายและเวลา", "Cost and time", "97,743 token สำหรับแผนเดียว", "97,743 tokens for one plan"),
        ("shield", "ความปลอดภัย: ขออนุญาตก่อนไหม", "Safety: did it ask first?", "หยุดก่อน add_to_calendar ✓", "paused before add_to_calendar ✓"),
        ("dice", "หลายรอบ: pass^k", "Many runs: pass^k", "90% ต่อครั้ง → 5 ครั้งติด 0.59", "90% each → all 5 right: 0.59")]
for k, (icon, th, en, eth, een) in enumerate(MEAS):
    y = 74 + k * 76
    ic(s, icon, 682, y + 26, 40)
    s.both(712, y + 22, th, en, "pl-text")
    s.both(712, y + 48, eth, een, "pl-note")
s.save("l14-agent-tradeoff.svg", 476)

# ---------------------------------------------------------------- 27a. one Terminal-Bench task, as an exam
# terminal-bench/tasks/sound-change-cascade (harbor-framework/terminal-bench, read 2026-10-24): described, not copied.
# The word pairs drawn here are a made-up mini example; no task data or answers are reproduced (the task carries a
# "never in training corpora" canary).
s = Svg(W, "One Terminal-Bench 4.0 task, sound-change-cascade from Carnegie Mellon, tested like an exam. 1 The question: "
           "find the ordered sound-change rules that turned old words into modern ones. A made-up mini example: pata → "
           "pada, lupa → luba, tapu → tabu, so t becomes d and p becomes b between vowels; the first t of tapu stays. The "
           "real task gives 780 pairs. 2 The exam room: a sealed computer (a Docker container), up to 8 hours, no answers "
           "from the internet. 3 The student is the agent, harness plus model, working alone: try rules, check, fix. "
           "4 Marking: the rules must reproduce all 780 known pairs and a set of hidden pairs exactly, and the files must "
           "be valid; all 7 checks pass scores 1, anything else 0. Each task is tried 3 times and averaged.")
s.both(20, 30, "งาน 1 ข้อของ Terminal-Bench 4.0 ทดสอบเหมือนการสอบ: sound-change-cascade (Carnegie Mellon)",
       "One Terminal-Bench 4.0 task is tested like an exam: sound-change-cascade (Carnegie Mellon)", "pl-label")
HEAD = [("1 · ข้อสอบ", "1 · The question", "icon-document"), ("2 · ห้องสอบ", "2 · The exam room", "icon-laptop"),
        ("3 · ผู้สอบ", "3 · The student", "ag-robot-tools"), ("4 · ตรวจข้อสอบ", "4 · Marking", "icon-clipboard")]
for k, (th, en, picname) in enumerate(HEAD):
    x = 20 + k * 288
    s.box(x, 46, 276, 330, "nt-band-a" if k == 3 else "ml-cell", 14)
    s.both(x + 16, 76, th, en, "pl-label")
    pic(s, picname, x + 206, 50, 60, 56, "xMidYMid")
    if k < 3:
        s.arrow(x + 277, 210, x + 287, 210)
# 1: the question, with a made-up mini example
s.both(36, 124, "คำเก่า → คำใหม่: หากฎ", "old → new: find the rules", "hk-desc")
PAIRS = [("pata", "pa", "d", "a"), ("lupa", "lu", "b", "a"), ("tapu", "ta", "b", "u")]
for r, (old, a, ch, b) in enumerate(PAIRS):
    y = 158 + r * 32
    s.raw(f'<text x="44" y="{y}" class="dg-code" style="font-size:20px">*{old}</text>')
    s.arrow(118, y - 6, 146, y - 6)
    s.raw(f'<text x="156" y="{y}" class="dg-code" style="font-size:20px">{a}<tspan class="ml-neg" font-weight="700">{ch}</tspan>{b}</text>')
s.box(36, 236, 244, 46, "nt-out", 8)
s.both(48, 256, "t→d, p→b ระหว่างสระ", "t→d, p→b between vowels", "hk-desc")
s.code(48, 275, "/ V _ V")
s.both(36, 308, "t ตัวแรกของ tapu ไม่เปลี่ยน", "tapu's first t stays", "pl-note")
s.both(36, 336, "ตัวอย่างสมมติ", "a made-up example;", "pl-note")
s.both(36, 362, "งานจริงมี 780 คู่", "the real task: 780 pairs", "pl-note")
# 2: the exam room
for j, (th, en) in enumerate([("คอมพิวเตอร์ปิด (Docker)", "a sealed computer (Docker)"), ("สอบได้ถึง 8 ชั่วโมง", "up to 8 hours"),
                              ("ห้ามหาเฉลยออนไลน์", "no answers from the internet")]):
    s.both(324, 134 + j * 34, th, en, "pl-text")
# 3: the student
for j, (th, en) in enumerate([("agent = harness + โมเดล", "the agent: harness + model"), ("ทำคนเดียว", "working alone"),
                              ("ลองกฎ → ตรวจ → แก้", "try rules → check → fix")]):
    s.both(612, 134 + j * 34, th, en, "pl-text")
ic(s, "loop", 714, 280, 64)
# 4: marking
for j, (th, en) in enumerate([("✓ คู่ที่ให้มา ถูกครบ 780", "✓ all 780 known pairs"), ("✓ คู่ที่ซ่อนไว้ ถูกหมด", "✓ all hidden pairs"),
                              ("✓ ไฟล์และรูปแบบถูก", "✓ files and format valid")]):
    s.both(900, 134 + j * 34, th, en, "pl-text")
s.box(900, 270, 244, 62, "nt-out", 10)
s.both(916, 296, "ผ่านทั้ง 7 ข้อ → 1", "all 7 checks pass → 1", "ml-ok")
s.both(916, 320, "ข้อใดไม่ผ่าน → 0", "any fails → 0", "ml-neg")
s.box(20, 392, 1140, 74, "ml-cell-b", 12)
s.both(36, 422, "คู่ที่ซ่อนไว้ = ข้อสอบใหม่ที่ไม่เคยเห็น: ต้องหากฎจริงให้ได้ ไม่ใช่แค่จำคู่ที่ให้มา",
       "Hidden pairs = new exam questions: the agent must find the real rules, not memorise the pairs it was given.", "pl-text")
s.both(36, 452, "ทำงานละ 3 ครั้งแล้วเฉลี่ย · 66 งาน → คะแนน Terminal-Bench 4.0",
       "Each task is tried 3 times and averaged · 66 tasks → the Terminal-Bench 4.0 score", "pl-note")
s.save("l14-bench-task.svg", 480)
