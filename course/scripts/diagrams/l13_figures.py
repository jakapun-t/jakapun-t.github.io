"""Draws the lesson 13 infographics (SVG, inlined into the page; ไทย/EN labels follow the
language switch). Probabilities in the next-word figure are an illustration, not a model run.

    python3 scripts/diagrams/l13_figures.py courses/nlp-basic/images

Uses the nt-*, pl-*, sw-* and ml-* classes in templates/page.css.
"""

import math
import os
import sys
import unicodedata
from html import escape

from stats_svg import both_icon, icon_markup, put_icon  # noqa: E402,F401  (generated icons)

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
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

    def arrow(self, x1, y1, x2, y2):
        self.out.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="pl-line"/>')
        if x2 > x1:
            self.out.append(f'<path d="M{x2 - 8:g} {y2 - 6:g} L{x2:g} {y2:g} L{x2 - 8:g} {y2 + 6:g}" class="pl-line"/>')
        else:
            self.out.append(f'<path d="M{x2 - 6:g} {y2 - 8:g} L{x2:g} {y2:g} L{x2 + 6:g} {y2 - 8:g}" class="pl-line"/>')

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


# ---------------------------------------------------------------- 2. next-word prediction
s = Svg(900, "A language model gives every possible next word a probability; it picks a likely one, adds it, and repeats.")
s.both(20, 30, "บริบท (สิ่งที่พิมพ์มาแล้ว)", "Context (what has been written)", "nt-head")
s.both(420, 30, "ความน่าจะเป็นของคำถัดไป (ตัวอย่าง)", "Probability of the next word (illustration)", "nt-head")
# the example follows the language switch: a Thai sentence in Thai mode, an English one in EN mode
examples = [
    ("th", "ฉันหั่นผักด้วย ___", [("มีด", 0.72), ("กรรไกร", 0.15), ("เครื่องปั่น", 0.08), ("มือ", 0.04), ("ท้องฟ้า", 0.001)],
     ["ฉันหั่นผักด้วย", "มีด", "ที่", "คม", "มาก"]),
    ("en", "I cut vegetables with a ___", [("knife", 0.72), ("scissors", 0.15), ("blender", 0.08), ("spoon", 0.04), ("sky", 0.001)],
     ["I cut vegetables with a", "knife", "that", "is", "sharp"]),
]
for lang, context, cands, chain in examples:
    s.out.append(f'<g data-only="{lang}"' + (' lang="en"' if lang == "en" else "") + ">")
    s.box(20, 44, 350, 50, "nt-bubble", 25)
    s.text(38, 76, context, "pl-text")
    s.arrow(378, 69, 410, 69)
    y = 62
    for word, p in cands:
        s.text(420, y + 6, word, "pl-text")
        w = max(3, 300 * p)
        s.box(530, y - 11, w, 22, "ml-bar-top" if p == cands[0][1] else "ml-bar", 4)
        s.text(536 + w, y + 6, f"{p:.2f}" if p >= 0.01 else "≈0", "pl-note")
        y += 34
    x, yc = 20, y + 64
    for i, t in enumerate(chain):
        x = s.chip(x, yc, t, "pl-chip" if i == 0 else "sw-chip-warn") + 8
    s.out.append("</g>")
s.both(20, y + 26, "เลือกคำที่น่าจะเป็นสูง แล้วต่อท้าย → ทำซ้ำทีละ token จนจบคำตอบ", "Pick a likely word, add it → repeat one token at a time until the answer ends", "ml-ok")
y += 64
s.save("l13-next-word.svg", y + 34)

# ---------------------------------------------------------------- 3. pretrain → three ways to use it
s = Svg(900, "A pretrained language model learns language from huge text, then is used for a task by fine-tuning, few-shot prompting or zero-shot prompting.")
s.box(20, 20, 250, 200, "nt-band-a", 14)
s.both(145, 54, "1. Pretraining", "1. Pretraining", "pl-label", "middle")
s.both(145, 90, "อ่านข้อความจากอินเทอร์เน็ต", "Reads text from the internet", "pl-note", "middle")
s.both(145, 114, "หลายร้อย GB", "hundreds of GB", "pl-note", "middle")
s.both(145, 150, "ฝึกทายคำถัดไป", "practises predicting", "pl-note", "middle")
s.both(145, 174, "จนรู้ภาษาและความรู้ทั่วไป", "the next word", "pl-note", "middle")
routes = [
    ("Fine-tuning", "สอนเพิ่มด้วยข้อมูลที่มีป้ายกำกับ (ปรับค่าในโมเดล)", "train more on labelled data (changes the model)"),
    ("Few-shot prompting", "ใส่ตัวอย่างไม่กี่ข้อใน prompt (ไม่ปรับโมเดล)", "put a few examples in the prompt (model unchanged)"),
    ("Zero-shot prompting", "สั่งงานด้วยคำอธิบายอย่างเดียว ไม่มีตัวอย่าง", "describe the task only, no examples"),
]
y = 46
for name, th, en in routes:
    s.arrow(276, 120, 330, y)
    s.box(336, y - 26, 544, 52, "nt-band-b", 12)
    s.text(352, y - 2, name, "pl-label")
    s.both(352, y + 20, th, en, "pl-note")
    y += 74
s.both(20, 252, "สองทางหลังคือ in-context learning: โมเดลเรียนงานใหม่จากบริบทใน prompt โดยไม่ต้องฝึกใหม่", "The last two are in-context learning: the model picks up a new task from the prompt, with no retraining", "ml-ok")
s.save("l13-pretrain.svg", 272)

# ---------------------------------------------------------------- 4. RCRC prompt
s = Svg(900, "A prompt built from Role, Context, Result and Constraint, each part highlighted.")
parts = [
    ("Role", "rc-role", "บทบาท", "role", "คุณคือผู้ช่วยสอนวิชาภาษาศาสตร์"),
    ("Context", "rc-ctx", "บริบท", "context", "นักศึกษาปี 1 เพิ่งเริ่มเรียนเรื่องการตัดคำ"),
    ("Result", "rc-res", "ผลที่ต้องการ", "result", "อธิบายว่าทำไมภาษาไทยตัดคำยาก พร้อมตัวอย่าง 2 ข้อ"),
    ("Constraint", "rc-con", "ข้อจำกัด", "constraint", "ใช้ภาษาง่าย ไม่เกิน 5 บรรทัด เป็นข้อ ๆ"),
]
y = 40
for key, cls, th, en, txt in parts:
    s.box(20, y - 24, 860, 48, cls, 10)
    s.text(40, y + 7, key, "rc-key")
    s.both(180, y + 7, th, en, "pl-note")
    s.text(320, y + 7, txt, "pl-text")
    y += 60
s.save("l13-rcrc.svg", y - 12)

# ---------------------------------------------------------------- 5. API call
s = Svg(900, "An API call: your Python code sends a request with the prompt and an API key over the internet; the model's server sends back a response.")
s.box(20, 30, 230, 120, "nt-band-a", 14)
s.both(135, 62, "โค้ด Python ของเรา", "Our Python code", "pl-label", "middle")
s.text(135, 100, "VS Code", "pl-note", "middle")
s.box(650, 30, 230, 120, "nt-band-b", 14)
s.both(765, 62, "เซิร์ฟเวอร์ของโมเดล", "The model's server", "pl-label", "middle")
s.text(765, 100, "Gemini", "pl-note", "middle")
s.arrow(258, 70, 642, 70)
s.both(450, 52, "request: prompt + API key (JSON)", "request: prompt + API key (JSON)", "pl-note", "middle")
s.arrow(642, 118, 258, 118)
s.out.append('<path d="M266 112 L258 118 L266 124" class="pl-line"/>')
s.both(450, 142, "response: ข้อความคำตอบ", "response: the answer text", "pl-note", "middle")
s.both(20, 190, "ต้องมี 2 อย่าง: ที่อยู่ของ API (endpoint) และ API key ซึ่งต้องเก็บเป็นความลับเหมือนรหัสผ่าน", "You need 2 things: the API's address (endpoint) and an API key, which you keep secret like a password", "sw-warn-text")
s.save("l13-api.svg", 206)

# ---------------------------------------------------------------- 6. classic classifier vs LLM prompt
s = Svg(900, "Two ways to build a sentiment classifier: train a model on labelled data, or prompt a pretrained LLM.")
cols = [
    (20, "nt-band-a", "เทรนโมเดลเอง (Naive Bayes)", "Train your own model (Naive Bayes)",
     [("ต้องมีข้อมูลที่มีป้าย หลายร้อยถึงหลายพันข้อ", "needs hundreds to thousands of labelled texts"),
      ("ต้องเทรน แต่รันเร็วและฟรี", "needs training, but runs fast and free"),
      ("ทำได้แค่งานที่เทรนมา", "does only the task it was trained for")]),
    (460, "nt-band-b", "ใช้ LLM ด้วย prompt", "Prompt an LLM",
     [("ใช้ตัวอย่างไม่กี่ข้อ หรือไม่ใช้เลย", "a few examples, or none"),
      ("ไม่ต้องเทรน แต่เรียก API เสียเวลาและอาจเสียเงิน", "no training; API calls cost time and money"),
      ("เปลี่ยนงานได้แค่เปลี่ยน prompt", "change the task by changing the prompt")]),
]
for x, cls, th, en, items in cols:
    s.box(x, 16, 420, 190, cls, 14)
    s.both(x + 20, 50, th, en, "pl-label")
    y = 90
    for ith, ien in items:
        s.both(x + 20, y, "• " + ith, "• " + ien, "pl-note")
        y += 36
s.save("l13-compare.svg", 222)

# ---------------------------------------------------------------- 7. apps are shop fronts for an LLM (L13-S07)
s = Svg(900, "Chat apps are shop fronts: inside each one is a large language model, built by a company.")
s.both(20, 30, "🏪 แอป = หน้าร้าน   →   🧠 LLM = สมองข้างใน   →   🏢 บริษัทที่สร้าง",
       "🏪 App = shop front   →   🧠 LLM = the brain inside   →   🏢 the company that built it", "pl-label")
apps = [
    ("ChatGPT", "GPT", "OpenAI", ("สรุปข่าวนี้ให้หน่อย", "Summarise this news"), ("ข่าวนี้พูดถึง…", "This story is about…")),
    ("Gemini", "Gemini", "Google", ("แปลเป็นอังกฤษ", "Translate to Thai"), ("Sure: …", "ได้เลย: …")),
    ("Claude", "Claude", "Anthropic", ("ช่วยเขียนโค้ด", "Help me write code"), ("def clean(t): …", "def clean(t): …")),
    ("DeepSeek", "DeepSeek", "DeepSeek", ("แก้โจทย์ 2x = 8", "Solve 2x = 8"), ("x = 4", "x = 4")),
]
for i, (app, llm, co, ask, reply) in enumerate(apps):
    x0 = 20 + i * 220
    # the chat window
    s.box(x0, 52, 200, 170, "ai-window", 14)
    s.out.append(f'<path d="M{x0} 88 H{x0 + 200}" class="ai-rule"/>')
    for k, dx in enumerate((16, 30, 44)):
        s.out.append(f'<circle cx="{x0 + dx}" cy="70" r="4.5" class="ai-dot ai-dot-{k}"/>')
    s.text(x0 + 120, 77, app, "ai-app", "middle")
    s.box(x0 + 24, 102, 164, 32, "ai-you", 16)
    s.both(x0 + 106, 123, ask[0], ask[1], "ai-bubble-text", "middle")
    s.box(x0 + 12, 146, 140, 32, "ai-bot", 16)
    s.both(x0 + 82, 167, reply[0], reply[1], "ai-bubble-text", "middle")
    s.box(x0 + 12, 190, 176, 18, "ai-input", 9)
    # down to the brain inside
    s.out.append(f'<path d="M{x0 + 100} 228 V254" class="pl-line"/><path d="M{x0 + 94} 246 L{x0 + 100} 254 L{x0 + 106} 246" class="pl-line"/>')
    s.box(x0 + 20, 262, 160, 54, "ml-model", 14)
    put_icon(s, "🧠", x0 + 48, 297, "ai-brain", "middle", 24)
    s.text(x0 + 70, 296, llm, "ml-model-text")
    s.text(x0 + 100, 344, "🏢 " + co, "pl-note", "middle")
s.save("l13-llm-apps.svg", 360)

# ---------------------------------------------------------------- 8. how large is GPT-3? (L13-S09)
# 300e9 words / (250 words a minute, non-stop) ≈ 2,283 years; 700 GB / 16 GB ≈ 44 laptops;
# 2026 − 355 = 1671 (พ.ศ. 2214, King Narai's reign); $4M ≈ 140 million baht at ~35 baht/$.
s = Svg(900, "How large is GPT-3? 300 billion words, 700 GB of memory, 355 years on one GPU, about 4 million dollars.")
tiles = [
    ("📚", "300,000 ล้าน", "300 billion", "คำที่ใช้เทรน", "words to learn from", ("คนอ่านไม่หยุด 24 ชม.", "ต้องใช้ ~2,300 ปี"), ("a person reading non-stop", "needs ~2,300 years")),
    ("💾", "700 GB", "700 GB", "หน่วยความจำ", "of memory", ("เท่ากับ RAM ของ", "โน้ตบุ๊ก 16 GB 44 เครื่อง"), ("the RAM of 44", "laptops (16 GB each)")),
    ("⏳", "355 ปี", "355 years", "ถ้าเทรนด้วย GPU ตัวเดียว", "to train on one GPU", ("เริ่มเทรนสมัยพระนารายณ์", "เพิ่งเสร็จปีนี้"), ("start in 1671,", "finish this year")),
    ("💰", "$4 ล้าน", "$4 million", "ค่าเทรนหนึ่งครั้ง", "for one training run", ("≈ 140 ล้านบาท", "GPU 1,000+ ตัว 30 วัน"), ("1,000+ GPUs", "for 30 days")),
]
for i, (icon, big_th, big_en, lab_th, lab_en, cmp_th, cmp_en) in enumerate(tiles):
    x0 = 10 + i * 222
    cx = x0 + 105
    s.box(x0, 10, 210, 330, ["nt-band-a", "nt-band-b", "nt-band-a", "nt-band-b"][i], 16)
    put_icon(s, icon, cx, 62, "gs-icon", "middle", 40)
    s.both(cx, 106, big_th, big_en, "gs-big", "middle")
    s.both(cx, 134, lab_th, lab_en, "pl-note", "middle")
    # a small picture of the comparison
    if i == 0:
        for k in range(7):
            s.box(cx - 70 + k * 20, 196 - (k % 3) * 6 - 22, 16, 30 + (k % 3) * 6, "gs-book", 3)
    elif i == 1:
        for k in range(44):
            s.box(cx - 77 + (k % 11) * 14, 160 + (k // 11) * 12, 11, 8, "gs-ram", 2)
    elif i == 2:
        s.out.append(f'<path d="M{cx - 80} 186 H{cx + 80}" class="gs-time"/>')
        s.out.append(f'<circle cx="{cx - 80}" cy="186" r="6" class="gs-dot"/><circle cx="{cx + 80}" cy="186" r="6" class="gs-dot"/>')
        s.both(cx - 80, 214, "2214", "1671", "gs-year", "middle")
        s.both(cx + 80, 214, "2569", "2026", "gs-year", "middle")
    else:
        for k in range(30):
            s.box(cx - 75 + (k % 10) * 15, 160 + (k // 10) * 15, 11, 11, "gs-day", 2)
        s.both(cx, 220, "30 วัน", "30 days", "gs-year", "middle")
    s.both(cx, 270, cmp_th[0], cmp_en[0], "gs-cmp", "middle")
    s.both(cx, 294, cmp_th[1], cmp_en[1], "gs-cmp", "middle")
s.save("l13-gpt3-size.svg", 350)

# ---------------------------------------------------------------- 9. inside an LLM, one step at a time (L13-S24)
# Eleven frames for a ```stepper (Back / Next / Play): 0 the whole trip, 1-5 one stage at a time for "The cat sat",
# 6 the chosen token is appended, 7-9 one more token per round, 10 the finished sentence.
# Token IDs, vector shades and probabilities are an illustration. GPT-3 has 96 transformer layers.
IN_COLS = [
    ("ข้อความ", "Text", "ที่ป้อนเข้าไป", "what goes in"),
    ("Token → ID", "Token → ID", "เลขประจำตัวในคลังคำ", "its number in the vocab"),
    ("Embedding", "Embedding", "ID → เวกเตอร์ตัวเลข", "ID → a vector of numbers"),
    ("Transformer ×96", "Transformer ×96", "คำนวณหลายสิบชั้น", "dozens of layers of maths"),
    ("คำถัดไป", "Next token", "ความน่าจะเป็น", "probabilities"),
]
IN_TOK = [("The", 791), ("cat", 1234), ("sat", 345), ("on", 319), ("the", 262), ("mat", 2603), (".", 13)]
IN_PROBS = [[("on", .41), ("down", .22), ("by", .09), ("up", .06)], [("the", .62), ("a", .21), ("my", .05), ("top", .03)],
            [("mat", .34), ("floor", .18), ("sofa", .12), ("bed", .09)], [(".", .71), ("and", .12), (",", .06), ("with", .03)]]
IN_SHADES = [[.9, .3, .6, .2, .8, .4, .7], [.2, .8, .4, .9, .3, .6, .5], [.6, .5, .9, .3, .2, .8, .4],
             [.4, .9, .2, .7, .6, .3, .8], [.8, .2, .7, .4, .9, .5, .3], [.3, .6, .8, .5, .2, .9, .6]]
CW, CG = 162, 22
NEW_BOX = ' style="fill:var(--tag-warning-bg);stroke:var(--accent)"'   # a token the model wrote itself
NEW_TXT = ' style="fill:var(--accent)"'


def inside_frame(k, title, n, upto, current, strip, new, loop, tag, done=False):
    """n tokens are fed in; columns before `upto` are filled; `current` is outlined; the strip shows `strip` tokens and
    its chip number `new` fades in; loop is 'dim', 'norm' or 'on'."""
    s = Svg(918, title)                                        # the fifth column ends at x = 908
    g = s.out.append
    grow_tok = n - 1 if 3 < n < 7 and not done else None      # the token that joined the input this round

    def open_g(i, tok=None):
        g('<g class="grow-new">' if i == current or (tok is not None and tok == grow_tok) else "<g>")

    for i, (hth, hen, sth, sen) in enumerate(IN_COLS):
        x0 = 10 + i * (CW + CG)
        g("<g>" if i < upto else '<g opacity=".3">')
        s.box(x0, 10, CW, 220, "nt-band-a" if i % 2 == 0 else "nt-band-b", 14)
        g(f'<circle cx="{x0 + 18}" cy="34" r="11" class="pl-dot"/>')
        s.text(x0 + 18, 39, str(i + 1), "pl-num", "middle")
        s.both(x0 + 36, 40, hth, hen, "in-h")
        s.both(x0 + CW / 2, 64, sth, sen, "in-sub", "middle")
        g("</g>")
        if i < 4:
            g("<g>" if i + 1 < upto else '<g opacity=".3">')
            s.arrow(x0 + CW + 2, 140, x0 + CW + CG - 2, 140)
            g("</g>")
        if i == current:
            g(f'<rect x="{x0}" y="10" width="{CW}" height="220" rx="14" style="fill:none;stroke:var(--accent);stroke-width:3"/>')
    toks = IN_TOK[:n]
    # 1. the text that goes in: the prompt, then what the model has written so far
    more = " ".join(t for t, _ in toks[3:]).replace(" .", ".")
    open_g(0)
    if more:
        s.box(22, 96, 138, 82, "nt-bubble", 22)
        s.text(91, 130, "The cat sat", "in-text", "middle")
        g(f'<text x="91" y="160" class="in-text" text-anchor="middle"{NEW_TXT}>{escape(more)}</text>')
    else:
        s.box(22, 110, 138, 52, "nt-bubble", 26)
        s.text(91, 143, "The cat sat", "in-text", "middle")
    g("</g>")
    feed = toks[:6]                                             # the final "." is never fed back in
    two = len(feed) > 3
    # 2. tokens and their IDs
    if upto > 1:
        x0 = 10 + CW + CG
        for j, (t, num) in enumerate(feed):
            x, y = x0 + 8 + (j % 3) * 50, (78 + (j // 3) * 72) if two else 96
            open_g(1, j)
            g(f'<rect x="{x}" y="{y}" width="46" height="30" rx="8" class="pl-chip"{NEW_BOX if j >= 3 else ""}/>')
            g(f'<text x="{x + 23}" y="{y + 21}" class="in-chip" text-anchor="middle"{NEW_TXT if j >= 3 else ""}>{escape(t)}</text>')
            g(f'<path d="M{x + 23} {y + 34} V{y + (44 if two else 50)}" class="pl-line"/>')
            s.text(x + 23, y + (60 if two else 72), str(num), "in-id", "middle")
            g("</g>")
    # 3. one vector per token (the shades stand for numbers)
    if upto > 2:
        x0 = 10 + 2 * (CW + CG)
        step, h, y0 = (22, 16, 86) if two else (30, 20, 94)
        for j, (t, num) in enumerate(feed):
            y = y0 + j * step
            open_g(2, j)
            s.text(x0 + 38, y + h / 2 + 5, str(num), "in-id", "end")
            for c, v in enumerate(IN_SHADES[j]):
                g(f'<rect x="{x0 + 43 + c * 16}" y="{y}" width="14" height="{h}" rx="3" class="in-vec" opacity="{v:.2f}"/>')
            g("</g>")
        if len(feed) <= 5:
            open_g(2)
            s.text(x0 + CW / 2, 200 if len(feed) <= 4 else 214, "[0.83, −0.27, …]", "in-id", "middle")
            g("</g>")
    # 4. stacked layers; on the top one every token looks at the others (attention)
    if upto > 3:
        x0 = 10 + 3 * (CW + CG)
        open_g(3)
        for c in range(4, -1, -1):
            s.box(x0 + 20 + c * 6, 86 + c * 14, 110, 44, "in-layer", 8)
        m = len(feed)
        dots = [x0 + 40 + 70 * j / (m - 1) for j in range(m)]
        pairs = sorted({(j, m - 1) for j in range(m - 1)} | {(j, j + 1) for j in range(m - 1)})
        for a_, b_ in pairs:
            g(f'<path d="M{dots[a_]:.1f} 108 Q{(dots[a_] + dots[b_]) / 2:.1f} {92 - min(b_ - a_, 4) * 5} {dots[b_]:.1f} 108" class="in-att"/>')
        for j, d in enumerate(dots):
            g(f'<circle cx="{d:.1f}" cy="108" r="{6 if m <= 4 else 5}" class="in-dot"/>')
        s.text(x0 + CW / 2, 205, "attention", "in-h", "middle")
        s.both(x0 + CW / 2, 225, "แต่ละคำดูคำอื่น", "tokens look around", "in-sub", "middle")
        g("</g>")
    # 5. next-token probabilities for this round
    if upto > 4:
        x0 = 10 + 4 * (CW + CG)
        g('<g class="grow-new">' if current == 4 or grow_tok is not None else "<g>")
        for r, (t, pr) in enumerate(IN_PROBS[n - 3]):
            y = 92 + r * 28
            s.text(x0 + 48, y + 15, t, "in-chip", "end")
            s.box(x0 + 54, y + 2, 92 * pr, 18, "ml-bar-top" if r == 0 else "ml-bar", 4)
            s.text(x0 + 60 + 92 * pr, y + 16, f"{pr:.2f}", "in-id")
        g("</g>")
    # the loop back: the chosen token is appended and everything runs again
    g({"dim": '<g opacity=".3">', "norm": "<g>", "on": '<g style="stroke-width:3.4">'}[loop])
    g(f'<path d="M{10 + 4 * (CW + CG) + CW / 2} 232 V262 H{10 + CW / 2} V240" class="pl-line"{" style=\"stroke-width:3.4\"" if loop == "on" else ""}/>')
    g(f'<path d="M{10 + CW / 2 - 6} 248 L{10 + CW / 2} 240 L{10 + CW / 2 + 6} 248" class="pl-line"{" style=\"stroke-width:3.4\"" if loop == "on" else ""}/>')
    g("</g>")
    tw = max(width(tag[0], 16), width(tag[1], 16)) + 32
    s.box(459 - tw / 2, 248, tw, 28, "nt-bubble", 14)
    s.both(459, 267, tag[0], tag[1], "in-h", "middle")
    # the text so far: the prompt's tokens, then the tokens the model wrote (warm chips)
    s.box(10, 286, 898, 40, "nt-bubble", 12)
    s.both(26, 312, "ข้อความตอนนี้", "Text so far", "in-h")
    x = 150
    for j, (t, _) in enumerate(IN_TOK[:strip]):
        w = max(34, width(t, 15) + 22)
        g('<g class="grow-new">' if j == new else "<g>")
        g(f'<rect x="{x:g}" y="292" width="{w:g}" height="28" rx="8" class="pl-chip"{NEW_BOX if j >= 3 else ""}/>')
        g(f'<text x="{x + w / 2:g}" y="311" class="in-chip" text-anchor="middle"{NEW_TXT if j >= 3 else ""}>{escape(t)}</text>')
        g("</g>")
        x += w + 6
    if done:
        s.both(x + 12, 312, "✓ 4 รอบ ได้ 4 token ใหม่", "✓ 4 rounds, 4 new tokens", "ml-ok")
    elif strip > 3:
        s.both(x + 12, 311, "สีส้ม = token ที่โมเดลเขียนเอง", "orange = tokens the model wrote", "in-sub")
    s.save(f"l13-inside-{k}.svg", 334)


R1 = ("รอบที่ 1", "round 1")
for k, (title, n, upto, current, strip, new, loop, tag, done) in enumerate([
        ("Inside an LLM, the whole trip: text becomes token IDs, then vectors, then many layers of maths, then a probability for every next token; the chosen token is appended and the loop repeats.",
         3, 5, None, 4, None, "norm", ("วนซ้ำ ทีละ token (autoregressive)", "repeat, one token at a time (autoregressive)"), False),
        ("Step 1: the text 'The cat sat' goes in.", 3, 1, 0, 3, None, "dim", R1, False),
        ("Step 2: the text is cut into tokens, each with an ID: The 791, cat 1234, sat 345.", 3, 2, 1, 3, None, "dim", R1, False),
        ("Step 3: each ID becomes a vector of numbers.", 3, 3, 2, 3, None, "dim", R1, False),
        ("Step 4: the vectors pass through dozens of transformer layers, where each token looks at the others.", 3, 4, 3, 3, None, "dim", R1, False),
        ("Step 5: out comes a probability for each possible next token: on 0.41, down 0.22, by 0.09, up 0.06.", 3, 5, 4, 3, None, "dim", R1, False),
        ("The top token 'on' is appended: the text is now 'The cat sat on'.", 3, 5, None, 4, 3, "on", ("จบรอบที่ 1: ต่อท้าย “on”", "end of round 1: append “on”"), False),
        ("Round 2: 'The cat sat on' goes through every step again; the top next token is 'the' (0.62).", 4, 5, None, 5, 4, "on", ("รอบที่ 2: ได้ “the”", "round 2: “the”"), False),
        ("Round 3: 'The cat sat on the' goes in; the top next token is 'mat' (0.34).", 5, 5, None, 6, 5, "on", ("รอบที่ 3: ได้ “mat”", "round 3: “mat”"), False),
        ("Round 4: 'The cat sat on the mat' goes in; the top next token is a full stop (0.71).", 6, 5, None, 7, 6, "on", ("รอบที่ 4: ได้ “.”", "round 4: “.”"), False),
        ("Done: four rounds wrote four new tokens: 'The cat sat on the mat.'", 7, 1, None, 7, None, "dim", ("จบ", "done"), True)]):
    inside_frame(k, title, n, upto, current, strip, new, loop, tag, done)

# ---------------------------------------------------------------- 10. language models you already use (L13-S08)
s = Svg(900, "You already use language models: a search box completes your query, and a phone keyboard suggests the next word.")
both_icon(s, 20, 30, "🔍 ช่องค้นหาเติมคำให้", "🔍 Search suggests the rest", "pl-label")
both_icon(s, 560, 30, "📱 แป้นพิมพ์ทายคำถัดไป", "📱 Keyboard suggests a word", "pl-label")
examples = {
    "th": ("อากาศวันนี้", ["อากาศวันนี้ กรุงเทพ", "อากาศวันนี้ ฝนตกไหม", "อากาศวันนี้ เชียงใหม่", "อากาศวันนี้ ร้อนไหม"],
           ["ขอบคุณมากที่ช่วย", "เตรียมงานเมื่อวาน"], ["นะ", "ครับ", "ค่ะ"]),
    "en": ("what is the weather", ["what is the weather today", "what is the weather tomorrow", "what is the weather in bangkok", "what is the weather like"],
           ["Thanks so much for", "helping"], ["me", "out", "us"]),
}
for lang, (query, sugg, msg, nxt) in examples.items():
    s.out.append(f'<g data-only="{lang}"' + (' lang="en"' if lang == "en" else "") + ">")
    # search box and its dropdown
    s.box(20, 48, 470, 44, "ev-search", 22)
    put_icon(s, "🔍", 46, 77, "ev-icon", "start", 18)
    s.text(76, 77, query, "in-text")
    qx = 76 + width(query, 18)
    s.out.append(f'<path d="M{qx + 3:g} 60 V82" class="ev-caret"/>')
    s.box(20, 98, 470, 4 * 40 + 16, "ev-drop", 12)
    for k, t in enumerate(sugg):
        y = 128 + k * 40
        put_icon(s, "🔍", 46, y + 5, "ev-icon-sm", "start", 14)
        s.text(76, y + 6, query, "ev-typed")
        s.text(76 + width(query, 17) + 2, y + 6, t[len(query):], "ev-guess")
    # phone with a message, the suggestion bar and a keyboard
    px = 600
    s.box(px, 44, 230, 250, "ev-phone", 26)
    s.box(px + 12, 58, 206, 98, "ev-screen", 10)
    s.text(px + 24, 86, msg[0], "ev-msg")
    s.text(px + 24, 110, msg[1], "ev-msg")
    s.out.append(f'<path d="M{px + 24 + width(msg[1], 16) + 3:g} 96 V114" class="ev-caret"/>')
    s.box(px + 12, 164, 206, 34, "ev-bar", 8)
    for k, t in enumerate(nxt):
        cx = px + 12 + 206 * (k + 0.5) / 3
        s.text(cx, 187, t, "ev-next" if k == 0 else "ev-next-2", "middle")
        if k:
            s.out.append(f'<path d="M{px + 12 + 206 * k / 3:g} 170 V192" class="ev-sep"/>')
    for r in range(3):
        for c in range(10 - r):
            s.box(px + 16 + r * 10 + c * 20, 208 + r * 24, 16, 19, "ev-key", 4)
    s.out.append("</g>")
s.text(856, 182, "←", "ev-arrow", "middle")
s.both(856, 206, "ทาย", "guess", "ev-guess", "middle")
s.save("l13-lm-everyday.svg", 304)

# ---------------------------------------------------------------- 11. why chain-of-thought helps (L13-S14)
# The wrong answer 27 is the one reported without CoT in Wei et al. (2022) for the same question.
s = Svg(900, "Without chain-of-thought the model must jump from the question to the answer in one token and gets 27, wrong. With it, each small step becomes tokens it can build on, and it reaches 9.")
rows = [
    (16, "nt-band-a", "❌ ไม่มี CoT: ต้องตอบทันทีใน token เดียว", "❌ Without CoT: answer at once, in one token", [], ("27", False)),
    (152, "nt-band-b", "✅ มี CoT: เขียนทีละขั้น แต่ละ token เป็นฐานให้ token ถัดไป", "✅ With CoT: one step at a time, each token builds on the last",
     ["23 − 20", "= 3", "3 + 6", "= 9"], ("9", True)),
]
for y0, band, th, en, steps, (ans, ok) in rows:
    s.box(10, y0, 880, 122, band, 14)
    s.both(28, y0 + 32, th, en, "pl-label")
    yc = y0 + 84
    # the question, the steps, then the answer, always at the same x so the two rows compare
    s.box(28, yc - 20, 150, 40, "nt-bubble", 20)
    s.both(103, yc + 6, "โจทย์ผัดไทย", "the question", "in-text", "middle")
    centers = [103]
    x = 196
    for st in steps:
        w = width(st, 19) + 24
        s.chip(x, yc, st, "sw-chip-warn")
        centers.append(x + w / 2)
        x += w + 14
    ax = 690
    centers.append(ax + 32)
    for c1, c2 in zip(centers, centers[1:]):
        cls = "in-att" if steps else "cot-jump"
        lift = 30 if steps else 40
        s.out.append(f'<path d="M{c1:g} {yc - 22} Q{(c1 + c2) / 2:g} {yc - 22 - lift} {c2 - 4:g} {yc - 23}" class="{cls}"/>')
        s.out.append(f'<path d="M{c2 - 11:g} {yc - 31} L{c2 - 4:g} {yc - 23} L{c2 - 14:g} {yc - 22}" class="{cls}"/>')
    if not steps:
        s.both(400, yc + 6, "กระโดดทีเดียว ไม่มีที่ทด", "one big leap, no scratch paper", "wv-note", "middle")
    s.box(ax, yc - 22, 64, 44, "cot-ok" if ok else "cot-bad", 12)
    s.text(ax + 32, yc + 8, ans, "cot-ans", "middle")
    s.text(ax + 82, yc + 8, "✓" if ok else "✗", "cot-mark-ok" if ok else "cot-mark-bad")
s.save("l13-cot.svg", 284)

# ---------------------------------------------------------------- 12. getting a Gemini API key (L13-S17)
# Generic sketches of each step (no product logos). Labels follow ai.google.dev/gemini-api/docs/api-key.
s = Svg(900, "Six steps to a Gemini API key: open AI Studio's API Keys page, sign in, accept the terms, create a key, copy it, then save it as GEMINI_API_KEY and test it.")
steps = [
    ("เปิดหน้า API Keys", "Open the API Keys page", "url"),
    ("ลงชื่อเข้าใช้ด้วย Google", "Sign in with Google", "signin"),
    ("ยอมรับ Terms of Service", "Accept the Terms of Service", "terms"),
    ("กด Create API key", "Click Create API key", "create"),
    ("คัดลอก key", "Copy the key", "copy"),
    ("เก็บ key: เลือก 1 ใน 3 ทาง", "Store it: pick 1 of 3 ways", "term"),
]
PW, PH = 284, 168
for i, (th, en, kind) in enumerate(steps):
    x0, y0 = 10 + (i % 3) * (PW + 9), 10 + (i // 3) * (PH + 12)
    cx = x0 + PW / 2
    s.box(x0, y0, PW, PH, "nt-band-a" if i % 2 == 0 else "nt-band-b", 14)
    s.out.append(f'<circle cx="{x0 + 22}" cy="{y0 + 26}" r="13" class="pl-dot"/>')
    s.text(x0 + 22, y0 + 32, str(i + 1), "pl-num", "middle")
    s.both(x0 + 42, y0 + 32, th, en, "ks-h")
    yv = y0 + 58
    if kind == "url":
        s.box(x0 + 16, yv, PW - 32, 34, "ks-bar", 17)
        s.text(cx, yv + 22, "aistudio.google.com/apikey", "ks-mono", "middle")
        s.both(cx, yv + 70, "ลิงก์นี้พาไปหน้า API Keys ตรง ๆ", "this link opens the API Keys page", "in-sub", "middle")
    elif kind == "signin":
        s.box(cx - 80, yv + 2, 160, 38, "ks-btn", 19)
        s.text(cx, yv + 27, "👤 Sign in", "ks-btn-t", "middle")
        s.both(cx, yv + 64, "บัญชีมหาวิทยาลัยใช้ไม่ได้?", "University account blocked?", "in-sub", "middle")
        s.both(cx, yv + 84, "ลองใช้ Gmail ส่วนตัว", "try a personal Gmail", "in-sub", "middle")
    elif kind == "terms":
        s.box(x0 + 30, yv + 4, 20, 20, "ks-check", 4)
        s.text(x0 + 40, yv + 20, "✓", "ks-check-t", "middle")
        s.both(x0 + 60, yv + 20, "ยอมรับเงื่อนไข", "I accept", "ks-body")
        s.both(cx, yv + 58, "ผู้ใช้ใหม่: AI Studio สร้าง project", "New users: AI Studio makes a project", "in-sub", "middle")
        s.both(cx, yv + 78, "และ key แรกให้อัตโนมัติ", "and a first key for you", "in-sub", "middle")
    elif kind == "create":
        s.box(cx - 88, yv + 2, 176, 38, "ks-btn-main", 19)
        s.text(cx, yv + 27, "🔑 Create API key", "ks-btn-main-t", "middle")
        s.both(cx, yv + 64, "ถ้ามี key แล้วจากข้อ 3", "Already got one in step 3?", "in-sub", "middle")
        s.both(cx, yv + 84, "ข้ามข้อนี้ได้", "skip this step", "in-sub", "middle")
    elif kind == "copy":
        s.box(x0 + 22, yv + 2, PW - 44, 38, "ks-key", 10)
        s.text(x0 + 36, yv + 27, "AIza•••••••••••••", "ks-mono")
        put_icon(s, "📋", x0 + PW - 40, yv + 28, "ks-icon", "middle", 18)
        s.both(cx, yv + 64, "ทำเหมือนรหัสผ่าน", "treat it like a password", "wv-note", "middle")
        s.both(cx, yv + 84, "ห้ามแชร์ ห้ามขึ้น GitHub", "never share, never on GitHub", "in-sub", "middle")
    else:
        ways = [("A", "API_KEY = \"AIza…\"", "ในโค้ด", "in code"), ("B", ".env", "ไฟล์ .env", ".env file"), ("C", "export …", "Terminal", "Terminal")]
        for j, (letter, code, wth, wen) in enumerate(ways):
            yy = yv + 2 + j * 32
            s.box(x0 + 18, yy, 26, 26, "ks-btn-main", 7)
            s.text(x0 + 31, yy + 19, letter, "ks-btn-main-t", "middle")
            s.box(x0 + 52, yy, 150, 26, "ks-term", 6)
            s.text(x0 + 60, yy + 18, code, "ks-term-t")
            s.both(x0 + 210, yy + 18, wth, wen, "in-sub")
s.save("l13-api-key-steps.svg", 2 * PH + 30)

# ---------------------------------------------------------------- 13. Gemini API rate limits (L13-S25)
# The numbers are an illustration only; each project's real limits are at aistudio.google.com/rate-limit.
s = Svg(900, "Three rate limits: requests per minute, tokens per minute and requests per day. Going over any one gives error 429. The numbers are made up for illustration.")
meters = [
    ("RPM", "request ต่อนาที", "requests per minute", 0.8, "8 / 10", "เต็มแล้วรอนาทีถัดไป", "full: wait for the next minute"),
    ("TPM", "token ต่อนาที", "tokens per minute", 0.35, "87k / 250k", "prompt ยาว = token เยอะ", "long prompts use more tokens"),
    ("RPD", "request ต่อวัน", "requests per day", 0.55, "137 / 250", "รีเซ็ตเที่ยงคืนเวลาแปซิฟิก", "resets at midnight Pacific"),
]
for i, (code, th, en, frac, val, nth, nen) in enumerate(meters):
    x0 = 10 + i * 297
    cx = x0 + 142
    s.box(x0, 10, 285, 230, "nt-band-a" if i != 1 else "nt-band-b", 14)
    s.text(cx, 48, code, "rl-code", "middle")
    s.both(cx, 74, th, en, "in-sub", "middle")
    # a half-circle gauge
    r = 70
    ang = math.pi * (1 - frac)
    ex, ey = cx + r * math.cos(ang), 170 - r * math.sin(ang)
    s.out.append(f'<path d="M{cx - r} 170 A{r} {r} 0 0 1 {cx + r} 170" class="rl-track"/>')
    s.out.append(f'<path d="M{cx - r} 170 A{r} {r} 0 0 1 {ex:.1f} {ey:.1f}" class="rl-fill{" rl-hot" if frac > .7 else ""}"/>')
    s.text(cx, 164, val, "rl-val", "middle")
    s.both(cx, 214, nth, nen, "in-sub", "middle")
s.box(10, 252, 880, 46, "sw-warn-box", 12)
s.both(450, 281, "เกินข้อใดข้อหนึ่ง → error 429 RESOURCE_EXHAUSTED   ·   ตัวเลขในรูปเป็นตัวอย่าง",
       "Over any one → error 429 RESOURCE_EXHAUSTED   ·   numbers here are made up", "sw-warn-text", "middle")
s.save("l13-rate-limits.svg", 308)

# ---------------------------------------------------------------- 14. information extraction: entities and relations (L13-S15)
s = Svg(900, "Information extraction: find the named entities in a sentence and their types, then the relations between them: who does what, where, with whom.")
TYPES = {"P": ("ie-per", "PERSON"), "O": ("ie-org", "ORGANIZATION"), "L": ("ie-loc", "LOCATION")}
sentences = {
    "th": [("สมชาย", "P"), ("จาก", ""), ("จุฬาฯ", "O"), ("ไป", ""), ("เชียงใหม่", "L"), ("กับทีม", ""), ("Google", "O")],
    "en": [("Somchai", "P"), ("of", ""), ("Chula", "O"), ("goes to", ""), ("Chiang Mai", "L"), ("with", ""), ("Google", "O")],
}
relations = {
    "th": [("สังกัด", "จุฬาฯ", "O"), ("ไปที่", "เชียงใหม่", "L"), ("ไปกับ", "Google", "O")],
    "en": [("works at", "Chula", "O"), ("goes to", "Chiang Mai", "L"), ("goes with", "Google", "O")],
}
s.box(10, 10, 880, 130, "nt-band-a", 14)
s.both(28, 40, "1. หาชื่อเฉพาะและประเภท (NER)", "1. Find the names and their types (NER)", "pl-label")
s.box(10, 152, 880, 228, "nt-band-b", 14)
s.both(28, 182, "2. หาความสัมพันธ์: ใคร ทำอะไร ที่ไหน กับใคร", "2. Find the relations: who does what, where, with whom", "pl-label")
for lang in ("th", "en"):
    s.out.append(f'<g data-only="{lang}"' + (' lang="en"' if lang == "en" else "") + ">")
    # the sentence, entities highlighted with their type underneath, centred
    FSZ = 26 if lang == "th" else 22  # English words run longer
    wcls, pcls = ("ie-word-lg", "ie-plain") if lang == "th" else ("ie-word", "ie-plain-sm")
    bw = lambda w, fs: width(w, fs) * 1.15  # bold text runs wider than width() guesses
    parts = [(word, t, bw(word, FSZ) + (34 if t else 18)) for word, t in sentences[lang]]
    x, y = 450 - sum(p[2] for p in parts) / 2 + 8, 90
    for word, t, step in parts:
        w = bw(word, FSZ)
        if t:
            cls, name = TYPES[t]
            s.box(x - 8, y - 30, w + 16, 44, cls, 10)
            s.text(x + w / 2, y + 2, word, wcls, "middle")
            s.text(x + w / 2, y + 34, name, f"ie-type {cls}-t", "middle")
        else:
            s.text(x, y + 2, word, pcls)
        x += step
    # the relation graph: the person on the left, one arrow per relation, its verb on the arrow's straight end
    px, py = 150, 290
    s.box(px - 75, py - 26, 150, 52, "ie-per", 26)
    s.text(px, py + 8, sentences[lang][0][0], "ie-word-lg", "middle")
    for k, (verb, obj, t) in enumerate(relations[lang]):
        ty = 222 + k * 68
        ox = 600
        s.out.append(f'<path d="M{px + 75} {py} C{px + 190} {py} {ox - 330} {ty} {ox - 230} {ty} H{ox - 8}" class="ie-edge"/>')
        s.out.append(f'<path d="M{ox - 16} {ty - 6} L{ox - 8} {ty} L{ox - 16} {ty + 6}" class="ie-edge"/>')
        vw = bw(verb, 16) + 26
        mx = ox - 120
        s.box(mx - vw / 2, ty - 15, vw, 30, "ie-verb", 15)
        s.text(mx, ty + 6, verb, "ie-verb-t", "middle")
        cls, name = TYPES[t]
        ow = bw(obj, 22) + 32
        s.box(ox, ty - 23, ow, 46, cls, 10)
        s.text(ox + ow / 2, ty + 8, obj, "ie-word", "middle")
        s.text(ox + ow + 12, ty + 6, name, f"ie-type {cls}-t")
    s.out.append("</g>")
s.save("l13-info-extraction.svg", 390)

# ---------------------------------------------------------------- 15. a .env file in the project folder (L13-S17)
s = Svg(900, "A .env file holds the key next to your code; .gitignore keeps it off GitHub; load_dotenv() reads it into the environment for genai.Client().")
s.box(10, 10, 300, 250, "nt-band-a", 14)
s.text(30, 44, "📁 my-project/", "ks-mono")
files = [(".env", "dv-secret"), (".gitignore", "dv-file"), ("main.py", "dv-file")]
for k, (name, cls) in enumerate(files):
    y = 72 + k * 58
    s.out.append(f'<path d="M40 52 V{y + 20} H60" class="dv-tree"/>')
    s.box(62, y, 220, 40, cls, 8)
    s.text(78, y + 26, ("🔒 " if k == 0 else "📄 ") + name, "ks-mono")
# what each file holds
notes = [
    ("GEMINI_API_KEY=AIza••••", ("ความลับ:", "ห้ามแชร์ ห้ามขึ้น GitHub"), ("Secret:", "never share, never on GitHub")),
    (".env", ("บอก Git ว่า", "ไม่ต้องอัปโหลด .env"), ("Tells Git not", "to upload .env")),
    ("load_dotenv()\nclient = genai.Client()", ("อ่าน .env แล้วสร้าง client", "ไม่มี key อยู่ในโค้ด"), ("Reads .env, makes the client:", "no key in the code")),
]
for k, (code, th, en) in enumerate(notes):
    y = 72 + k * 58
    s.out.append(f'<path d="M286 {y + 20} H330" class="pl-line" stroke-dasharray="4 4"/>')
    lines = code.split("\n")
    h = 22 + 18 * len(lines)
    s.box(336, y + 20 - h / 2, 250, h, "ks-term", 8)
    for j, ln in enumerate(lines):
        s.text(350, y + 20 - h / 2 + 22 + 18 * j, ln, "ks-term-t")
    s.both(606, y + 14, th[0], en[0], "pl-note")
    s.both(606, y + 36, th[1], en[1], "pl-note")
s.save("l13-dotenv.svg", 270)


# ---------------------------------------------------------------- 12. inside the response: nested boxes (L13-S27)
# Real run, gemini-3.5-flash-lite, prompt "อธิบายว่า token คืออะไร ใน 2 ประโยค": finish STOP, tokens 13 in, 87 out, 100 total.
s = Svg(900, "What generate_content returns: boxes inside boxes. response holds candidates (a list); its first item [0] holds "
             "content, which holds parts (a list); its first item [0] holds the text. Beside it, finish_reason STOP, and "
             "usage_metadata with 13 prompt tokens, 87 answer tokens, 100 in total. response.text is a shortcut for "
             "response.candidates[0].content.parts[0].text.")


def nbox(x, y, w, h, label, cls="nt-band-a", note=None):
    s.box(x, y, w, h, cls, 10)
    s.text(x + 14, y + 24, label, "in-code")
    if note:
        s.both(x + w - 12, y + 24, note[0], note[1], "in-sub", "end")


nbox(10, 10, 880, 262, "response", "nt-bubble")
nbox(28, 46, 560, 214, "candidates", "nt-band-b", ("list: คำตอบได้หลายอัน", "list: possible answers"))
nbox(46, 82, 524, 166, "[0]", "nt-bubble", ("ตัวแรกของ list", "the first item"))
nbox(64, 116, 488, 92, "content", "nt-band-a")
nbox(82, 146, 452, 52, "parts[0]", "nt-bubble")
s.text(176, 177, "text = “**Token** คือ หน่วยข้อมูลที่เล็กที่สุด…”", "in-code-acc")
s.text(64, 234, "finish_reason = STOP", "in-code")
s.both(260, 234, "← ตอบจบเอง ไม่ถูกตัด", "← finished on its own, not cut off", "in-sub")
nbox(604, 46, 270, 214, "usage_metadata", "nt-band-b", None)
for k, (name, v) in enumerate([("prompt_token_count", 13), ("candidates_token_count", 87), ("total_token_count", 100)]):
    s.text(620, 102 + k * 50, name, "in-code")
    s.text(620, 124 + k * 50, f"= {v}", "in-code-acc")
s.both(862, 250, "token ที่ใช้: เข้า 13 ออก 87", "tokens used: 13 in, 87 out", "in-sub", "end")
s.text(20, 304, "response.candidates[0].content.parts[0].text", "in-code-acc")
s.both(430, 304, "= response.text  (ทางลัด)", "= response.text  (the shortcut)", "in-h")
s.save("l13-response-nested.svg", 320)

# ---------------------------------------------------------------- 13. temperature reshapes the next-token chances (L13-S28)
# The four chances are the illustration from the "inside an LLM" frames (on .41, down .22, by .09, up .06), re-scaled to
# add up to 1, then p ** (1 / T) and re-scaled again. T = 0 always takes the top token.
BASE = {"on": .41, "down": .22, "by": .09, "up": .06}


def at_temp(t):
    if t == 0:
        return {k: (1.0 if k == "on" else 0.0) for k in BASE}
    w = {k: v ** (1 / t) for k, v in BASE.items()}
    tot = sum(w.values())
    return {k: v / tot for k, v in w.items()}


s = Svg(900, "Temperature reshapes the chances of the next token after 'The cat sat'. At 0 the model always takes 'on'. "
             "At 1 the chances stay as learned: on 0.53, down 0.28, by 0.12, up 0.08. At 2 they flatten: on 0.39, down 0.28, "
             "by 0.18, up 0.15, so less likely words get picked more often.")
s.both(450, 26, "คำถัดไปของ “The cat sat …” เมื่อ temperature ต่างกัน", "The next token after “The cat sat …” at different temperatures", "in-h", "middle")
for i, (t, nth, nen) in enumerate([(0, "เลือก “on” ทุกครั้ง", "always “on”"), (1, "ตามที่โมเดลเรียนมา", "the chances as learned"),
                                   (2, "คำอื่นได้โอกาสมากขึ้น", "other words get more chances")]):
    x0 = 10 + i * 296
    s.box(x0, 44, 284, 220, "nt-band-a" if i != 1 else "nt-band-b", 14)
    s.text(x0 + 142, 76, f"temperature = {t}", "in-code-acc" if i != 1 else "in-code", "middle")
    for r, (tok_, p) in enumerate(at_temp(t).items()):
        y = 96 + r * 30
        s.text(x0 + 66, y + 15, tok_, "in-chip", "end")
        if p > 0:
            s.box(x0 + 74, y + 2, 150 * p, 18, "ml-bar-top" if r == 0 else "ml-bar", 4)
        s.text(x0 + 80 + 150 * p, y + 16, f"{p:.2f}", "in-id")
    s.both(x0 + 142, 246, nth, nen, "in-h", "middle")
s.both(160, 292, "ต่ำ = คำตอบแทบเหมือนเดิม เหมาะกับงานจัดกลุ่ม", "low = nearly the same answer: good for classifying", "in-sub", "middle")
s.both(740, 292, "สูง = หลากหลายขึ้น เหมาะกับงานคิดไอเดีย", "high = more varied: good for brainstorming", "in-sub", "middle")
s.save("l13-temperature.svg", 306)
