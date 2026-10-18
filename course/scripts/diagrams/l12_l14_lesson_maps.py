"""Draws the lesson maps (big picture first) of nlp-basic lessons 12, 13 and 14: the problem on the
lesson's running example, the ways the lesson deals with it, each with what it changes, its tools and
its result on that example. Every result is real (course/.venv):

- L12, "How many reviews mention กาแฟ?" on reviews_th: a reader 7, split() 1, newmm 6 (R07 is cut
  กา | แฟก็ธรรม | ดา), attacut 7; the stray token กก 5 before normalizing, 0 after; top words after
  stop words: กาแฟ 6, อร่อย 5, บรรยากาศ 3.
- L13, "ร้านนี้ราคาแพงแต่อร่อย" on reviews_cls: 4 hand-written rules get 68 of 100 right, 30 match no
  rule; Naive Bayes (75/25 split, random_state=1) gets 24 of 25 test reviews and calls it negative.
  There is no Gemini run, so the map says students fill that answer in.
- L14, the word counter on SAMPLE: 5 lines, 25 words, 17 unique (scripts/l14_apps/nlp_logic.py).

    python3 scripts/diagrams/l12_l14_lesson_maps.py courses/nlp-basic/images

Uses the nt-*, pl-*, ml-*, sw-* and hk-* classes in templates/page.css, like nlp's l11-map-lesson.svg.
"""

import os
import sys
import unicodedata
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
SIZE = {"nt-task": 19, "hk-desc": 17, "pl-note": 18, "ml-ok": 18, "ml-neg": 19, "pl-text": 19, "hk-mono": 19, "nt-head": 17}


def width(s, fs):
    return sum(0 if unicodedata.category(c) == "Mn" else fs * 0.58 for c in s)


class Svg:
    def __init__(self, w, title):
        self.w, self.title, self.out = w, title, []

    def check(self, s, cls, room):
        if width(s, SIZE[cls]) > room:
            print(f"  too wide ({width(s, SIZE[cls]):.0f} > {room:.0f}): {s}")

    def both(self, x, y, th, en, cls, anchor="start", room=None):
        for s in (th, en):
            if room:
                self.check(s, cls, room)
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="th">{escape(th)}</text>')
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="en" lang="en">{escape(en)}</text>')

    def text(self, x, y, s, cls, anchor="start", room=None):
        if room:
            self.check(s, cls, room)
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" lang="en">{escape(s)}</text>')

    def box(self, x, y, w, h, cls, rx=12):
        self.out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}"/>')

    def raw(self, s):
        self.out.append(s)

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


def lesson_map(name, title, w, cols, example, problem, heading, ways, footer=None):
    """example: (th, en, cls) in the search-box bubble; problem: (th, en, detail_th, detail_en);
    ways: (title_th, title_en, change_th, change_en, tools, [(th, en, cls), ...])."""
    print(name)
    s = Svg(w, title)
    bw = 330 if w <= 900 else 380
    s.box(20, 16, bw, 54, "ml-cell", rx=27)
    th, en, cls = example
    s.both(42, 50, th, en, cls, room=bw - 44)
    s.raw(f'<path d="M{bw + 30} 43 L{bw + 66} 43" class="nt-arrow"/><path d="M{bw + 58} 36 L{bw + 67} 43 L{bw + 58} 50" class="nt-arrow"/>')
    px = bw + 76
    s.box(px, 10, w - 20 - px, 66, "sw-warn-box", rx=12)
    s.both(px + 18, 38, problem[0], problem[1], "nt-task", room=w - 56 - px)
    s.both(px + 18, 64, problem[2], problem[3], "pl-note", room=w - 56 - px)
    s.both(w / 2, 112, heading[0], heading[1], "nt-head", "middle")
    gap = 20
    cw = (w - 40 - gap * (cols - 1)) / cols
    lines = max(len(way[5]) for way in ways)
    ch = 108 + 28 * lines
    for k, (tth, ten, cth, cen, tools, results) in enumerate(ways):
        x = 20 + (k % cols) * (cw + gap)
        y = 128 + (k // cols) * (ch + 14)
        room = cw - 36
        s.box(x, y, cw, ch, "ml-cell", rx=14)
        s.both(x + 18, y + 34, tth, ten, "nt-task", room=room)
        s.both(x + 18, y + 62, cth, cen, "hk-desc", room=room)
        s.text(x + 18, y + 90, tools, "pl-note", room=room)
        for j, (rth, ren, rcls) in enumerate(results):
            s.both(x + 18, y + 122 + 28 * j, rth, ren, rcls, room=room)
    rows = (len(ways) + cols - 1) // cols
    h = 128 + rows * (ch + 14)
    if footer:
        s.both(w / 2, h + 18, footer[0], footer[1], "pl-note", "middle")
        h += 36
    s.save(name, h)


# ---------------------------------------------------------------- lesson 12
lesson_map(
    "l12-map-lesson.svg",
    "Lesson map. The problem: how many reviews mention กาแฟ? A reader counts 7, split() counts 1. Four steps from raw text to word counts: 2 clean, 3 tokenize, 4 filter and normalize, 5 count, each with its tools and its result on reviews_th; then 6 practice and review.",
    900, 2,
    ("กาแฟ อยู่ในกี่รีวิว?", "How many reviews say กาแฟ?", "pl-text"),
    ("1 ปัญหา: คนอ่านนับได้ 7 แต่ split() นับได้ 1 ✗", "1 The problem: a reader counts 7, split() counts 1 ✗",
     "ข้อความดิบยังไม่ใช่รายการคำที่โปรแกรมนับได้", "raw text is not yet a list of words a program can count"),
    ("4 ขั้นจากข้อความดิบสู่การนับคำ", "Four steps from raw text to word counts"),
    [("2 ทำความสะอาด", "2 Clean", "ลบส่วนที่ไม่ใช่ภาษา", "Remove what is not language", "regex · re.sub()",
      [("R01: RT @cafe_lover: กาแฟอร่อยมากกกก …", "R01: RT @cafe_lover: กาแฟอร่อยมากกกก …", "pl-note"),
       ("→ กาแฟอร่อยมาก ร้านสวย บรรยากาศดี ✓", "→ กาแฟอร่อยมาก ร้านสวย บรรยากาศดี ✓", "ml-ok")]),
     ("3 ตัดคำ", "3 Tokenize", "ตัดข้อความเป็นคำ", "Cut the text into words", "split() · newmm · attacut · BPE",
      [("newmm: 6 รีวิว · R07 → กา | แฟก็ธรรม | ดา ✗", "newmm: 6 · R07 → กา | แฟก็ธรรม | ดา ✗", "ml-neg"),
       ("attacut: 7 รีวิว ✓", "attacut: 7 reviews ✓", "ml-ok")]),
     ("4 กรองและปรับรูป", "4 Filter and normalize", "ตัดคำเติม รวมคำที่สะกดต่างกัน", "Drop filler words, merge spellings", "stop words · (.)\\1{2,}",
      [("token กก ที่นับผิด: 5 → 0 ✓", "the stray token กก: 5 → 0 ✓", "ml-ok"),
       ("แต่ stop list ตัด ไม่ ทิ้งด้วย ✗", "but the stop list also drops ไม่ (not) ✗", "ml-neg")]),
     ("5 นับคำ", "5 Count", "นับว่าแต่ละคำพบกี่ครั้ง", "Count how often each word appears", "value_counts() · bigrams",
      [("กาแฟ 6 · อร่อย 5 · บรรยากาศ 3 ✓", "กาแฟ 6 · อร่อย 5 · บรรยากาศ 3 ✓", "ml-ok"),
       ("กาแฟ ควรเป็น 7: R07 ถูกตัดผิด", "กาแฟ should be 7: R07 was cut wrong", "pl-note")])],
    ("6 ฝึกและทบทวน: ประมวลผลรีวิวหนึ่งรายการตั้งแต่ต้นจนจบ", "6 Practice and review: one review from start to finish"),
)

# ---------------------------------------------------------------- lesson 13
lesson_map(
    "l13-map-lesson.svg",
    "Lesson map. The problem: sort 100 reviews into positive or negative, such as ร้านนี้ราคาแพงแต่อร่อย. Five steps: 2 write rules (68 of 100 right), 3 train a classifier (24 of 25 on the test set, but this review comes out negative), 4 how an LLM works, 5 prompt an LLM, 6 call Gemini from Python.",
    1200, 3,
    ("ร้านนี้ราคาแพงแต่อร่อย", "ร้านนี้ราคาแพงแต่อร่อย", "pl-text"),
    ("1 ปัญหา: จัดรีวิว 100 รายการเป็น positive หรือ negative", "1 The problem: sort 100 reviews into positive or negative",
     "คนอ่านรีวิวนี้ว่าชม (แพงแต่อร่อย) โปรแกรมจะรู้ได้อย่างไร", "people read this one as praise (pricey but tasty): how can a program tell?"),
    ("5 ขั้น จากกฎที่เขียนเองสู่ LLM", "Five steps, from hand-written rules to an LLM"),
    [("2 เขียนกฎ", "2 Write rules", "คนเขียนกฎเอง", "A person writes the rules", "อร่อย → positive · ไม่ → negative …",
      [("4 กฎ: ถูก 68 จาก 100 ✗", "4 rules: 68 of 100 right ✗", "ml-neg"),
       ("30 รีวิวไม่มีกฎไหนตรงเลย", "30 reviews match no rule at all", "pl-note")]),
     ("3 เทรนตัวจัดกลุ่ม", "3 Train a classifier", "เรียนจากรีวิวที่มีป้ายกำกับ", "Learn from labelled reviews", "bag of words · Naive Bayes · test",
      [("ชุดทดสอบ: ถูก 24 จาก 25 (96%) ✓", "test set: 24 of 25 right (96%) ✓", "ml-ok"),
       ("แต่รีวิวนี้ → negative ✗", "but this review → negative ✗", "ml-neg")]),
     ("4 LLM ทำงานอย่างไร", "4 How an LLM works", "ทายคำถัดไปทีละ token", "Predict the next token, again and again", "tokens · pretraining · fine-tuning",
      [("เรียนจากข้อความมหาศาล", "learned from a huge amount of text,", "pl-note"),
       ("ไม่ใช่แค่ 75 รีวิว", "not just 75 reviews", "pl-note")]),
     ("5 เขียน prompt", "5 Prompt an LLM", "สั่งงานด้วยข้อความ ไม่ต้องเทรน", "Give the task in words, no training", "RCRC · zero-shot · few-shot · CoT",
      [("few-shot: ตัวอย่าง 3 ข้อ", "few-shot: 3 examples,", "pl-note"),
       ("แล้วตามด้วยรีวิวนี้", "then this review", "pl-note")]),
     ("6 เรียก Gemini จาก Python", "6 Call Gemini from Python", "ส่ง prompt จากโค้ด ทีละหลายรีวิว", "Send prompts from code, review after review", "google-genai · API key · classify()",
      [("คำตอบของ Gemini:", "Gemini's answer:", "pl-note"),
       ("รันเอง แล้วเติมลงตาราง", "run it and fill it in", "pl-note")])],
)

# ---------------------------------------------------------------- lesson 14
lesson_map(
    "l14-map-lesson.svg",
    "Lesson map. The problem: the Thai word counter (5 lines, 25 words, 17 unique on the sample reviews) only runs in VS Code. Five steps: 2 build a first app, 3 keep the NLP logic apart, 4 design with AI, 5 call Gemini, 6 put it online.",
    1200, 3,
    ("analyze_text(SAMPLE)", "analyze_text(SAMPLE)", "hk-mono"),
    ("1 ปัญหา: ตัวนับคำทำงานได้แค่ใน VS Code ของเรา", "1 The problem: the word counter only runs in your VS Code",
     "5 บรรทัด 25 คำ 17 คำไม่ซ้ำ แต่เพื่อนเปิดใช้ไม่ได้", "5 lines, 25 words, 17 unique, but a friend can't use it"),
    ("5 ขั้น จากสคริปต์สู่เว็บแอปออนไลน์", "Five steps, from a script to an app online"),
    [("2 สร้างแอปแรก", "2 Build a first app", "Python ไฟล์เดียวกลายเป็นหน้าเว็บ", "One Python file becomes a web page", "st.title · st.text_area · streamlit run",
      [("เปิดที่ localhost:8501 ✓", "opens at localhost:8501 ✓", "ml-ok"),
       ("เปลี่ยนค่า = รันใหม่ทั้งไฟล์", "every change reruns the whole file", "pl-note")]),
     ("3 แยกโค้ด NLP", "3 Keep the NLP logic apart", "โค้ด NLP อยู่ในไฟล์ของมันเอง", "NLP code lives in its own file", "nlp_logic.py · analyze_text()",
      [("5 บรรทัด · 25 คำ · 17 คำไม่ซ้ำ ✓", "5 lines · 25 words · 17 unique ✓", "ml-ok"),
       ("หน้าตาแบบไหนก็ได้ผลเดิม", "the same result in any interface", "pl-note")]),
     ("4 ให้ AI ช่วยออกแบบ", "4 Design with AI", "prompt เป็นสเปก ปรับทีละเรื่อง", "A prompt as a spec, one change at a time", "sidebar · columns · config.toml",
      [("ขั้น 1 → 2 → 3 ✓", "stage 1 → 2 → 3 ✓", "ml-ok"),
       ("หน้าตาใหม่ ตัวเลขเดิม", "new look, same numbers", "pl-note")]),
     ("5 เรียก Gemini", "5 Call Gemini", "เรียก LLM เมื่อผู้ใช้กดปุ่ม", "Call the LLM when the user clicks", "st.secrets · cache_resource · st.button",
      [("API key อยู่นอกโค้ด ✓", "the API key stays out of the code ✓", "ml-ok"),
       ("ไม่หลุดขึ้น GitHub", "so it never reaches GitHub", "pl-note")]),
     ("6 เอาขึ้นออนไลน์", "6 Put it online", "ให้ใครก็เปิดแอปได้", "Let anyone open the app", "Git · GitHub · Community Cloud",
      [("ได้ลิงก์ฟรี เปิดจากมือถือได้ ✓", "a free link that opens on a phone ✓", "ml-ok"),
       ("ทบทวนคำศัพท์ท้ายบท", "then review the key terms", "pl-note")])],
)
