"""Pictures added above the text of stats-dh L15 cards (data reliability and annotation agreement), in the stats-dh card
style: a student can skim the picture and read the card's text for the detail.
  l15-labels-everywhere.svg  S01  the lesson's problems in order: the letters, then 4 steps with everyday examples
  l15-quality-four.svg       S03  the four sides of data quality, each drawn
  l15-shortcut.svg           S05  the concept you mean vs an easy shortcut
  l15-shortcut-examples.svg  S05  four shortcuts (drama, sad song, sarcasm, fake news) on two made-up posts each, and the
                                 toxic-language model the fake-news labels would train
  l15-guide-checklist.svg    S07  the five parts to look for in a guideline (empty checklist, no answer)
  l15-lazy-annotator.svg     S08  100 letters: B says Anxiety on 35; a lazy "no" to everything still agrees on 65
  l15-kappa-scale.svg        S10  the Landis & Koch scale with the letters' 0.35 and 0.415
  l15-two-shapes.svg         S11  one raw table (3 raters × 4 letters) read two ways: Fleiss counts, Krippendorff as is
  l15-which-measure.svg      S13  how many raters × what kind of label → which measure (pilot 1 values)
  l15-lf-votes.svg           S15  4 labeling functions voting on 8 sentences, with how often each is right
  l15-llm-prompt.svg         S16  zero-shot vs a guided prompt on "It wasn't bad."
  l15-llm-vote.svg           S16  three LLMs vote on three comments: 2/3, 3/3, no majority
  l15-active-loop.svg        S17  the active-learning loop and the three letters' probabilities
  l15-takeaways.svg          S19  six takeaways as icons
  l15-case1-why.svg          S19  case study 1: the unlabelled comments, and three ways to label them (✗ ✗ ✓)
  l15-case1-key.svg          S19  stage 1: guideline, A and B label separately, answer key split into dev and test
  l15-case1-llm.svg          S19  stage 2: the LLM practises on dev (one fixed mistake), then labels all 20,000
  l15-case1-check.svg        S19  stage 3: test opened once (87 of 100 dots), then complaints before and after
  l15-case2.svg              S21  case study 2: three friends' 1–5 scores on a strip, before and after the guideline

    course/.venv/bin/python scripts/diagrams/stats_l15_cards.py courses/stats-dh/images

Real numbers (the lesson's code cells on scripts/diagrams/l15_practice_data.py output): B says Anxiety on 35 of 100, a
lazy all-"no" agrees 0.65; kappa Anxiety-or-not 0.35, 4 emotions (A vs B) 0.415; Fleiss 0.373, Krippendorff alpha 0.375,
ICC formality 0.418; labeling functions: lf_cry 4 of 4 right, lf_heartbroken 2 of 2, lf_happy 2 of 3, lf_has_I 2 of 6;
letters X [0.99, 0.005, 0.005] margin 0.98 entropy 0.09, Y [0.51, 0.49, 0] 0.02 / 1.00, Z [0.33, 0.33, 0.34] 0.01 / 1.58.
The B-Anxiety letters in the S08 grid are placed for the picture (35 of 100, as in the data), not at their real row
numbers. Exercise pictures show the task, not the answer. The app tiles are analogies.
Uses the mp-*, ml-*, nt-*, rc-*, dg-*, pl-* classes in templates/page.css.
"""

import math

from stats_svg import Svg, app_grid, circ, embed_png, emoji_or_icon, person, ring, term_grid, width  # noqa: F401

W = 1100
OK, NO, BLUE, GOLD = "var(--tag-exercise-dot)", "var(--accent)", "var(--tag-concept-dot)", "var(--tag-example-dot)"

# ================================================================ S01 the lesson's problems, in the order we solve them
def wrap(text, maxw, fs):
    out, line = [], ""
    for w in text.split(" "):
        t = (line + " " + w).strip()
        if width(t, fs) > maxw and line:
            out.append(line)
            line = w
        else:
            line = t
    return out + ([line] if line else [])


def para(s, x, y, th, en, cls, maxw, fs, lh, anchor="start"):
    """Wrapped Thai and English lines at the same place; returns the y under the longer one."""
    a, b = wrap(th, maxw, fs), wrap(en, maxw, fs)
    for i in range(max(len(a), len(b))):
        s.both(x, y + i * lh, a[i] if i < len(a) else "", b[i] if i < len(b) else "", cls, anchor)
    return y + max(len(a), len(b)) * lh


STEPS = [  # part, icon, everyday example, the problem (a question), what we learn
    ("ส่วนที่ 2", "Part 2", "🍅", "นักวิจารณ์ชมหนังตรงกัน แต่คนดูส่วนใหญ่ไม่ชอบ",
     "Critics praise a film; viewers don't",
     "ป้ายตรงกัน แปลว่าถูกต้องไหม?", "If labellers agree, are they right?",
     "ตรงกัน (reliable) ไม่เท่ากับ ถูกต้อง (valid)", "Reliable labels vs valid labels"),
    ("ส่วนที่ 3", "Part 3", "🚩", "ทีมตรวจโพสต์ต้องมีคู่มือ ว่าอะไรผิดกฎ",
     "Content moderators need a rulebook",
     "ทำอย่างไรให้ทุกคน ตัดสินแบบเดียวกัน?", "How do we make everyone judge alike?",
     "เขียนคู่มือ: นิยาม ตัวอย่าง และกฎ", "Guidelines: definitions, examples, rules"),
    ("ส่วนที่ 4", "Part 4", "🕺", "กรรมการเต้น 3 คน ให้ 3 คะแนนไม่เท่ากัน",
     "3 dance judges give 3 different scores",
     "เห็นตรงกันแค่ไหน เกินกว่าบังเอิญ?", "How much do they agree, beyond luck?",
     "ค่าความตรงกัน: kappa, alpha, ICC", "Agreement scores: kappa, alpha, ICC"),
    ("ส่วนที่ 5", "Part 5", "🚦", "CAPTCHA ให้คนทั้งโลกช่วยติดป้ายภาพ",
     "CAPTCHA gets the whole world labelling images",
     "ข้อมูลเป็นหมื่นชิ้น คนติดป้ายไม่ไหว", "Too many items to label by hand",
     "กฎ, LLM และ active learning", "Rules, LLMs, active learning"),
]
s = Svg(W, "The problems this lesson solves, in order. It starts from one problem: two research assistants label the same "
           "100 letters and give the same emotion to only 58, so any finding built on the labels is shaky. Part 2: if "
           "labellers agree, are they right? (critics agree, viewers disagree) → what good labels are, reliable vs valid. "
           "Part 3: how do we get everyone to judge the same way? (moderators need a rulebook) → write guidelines. Part 4: "
           "how much do they agree beyond luck? (3 dance judges, 3 scores) → kappa, alpha, ICC. Part 5: tens of thousands "
           "of items, too many by hand (CAPTCHA) → rules, LLMs, active learning. Part 6: a case study on TikTok comments "
           "uses all four steps.")
s.bubble("บทนี้แก้ปัญหาของ “ป้าย” ที่คนติดให้ข้อมูล ทีละขั้นตามลำดับนี้", "This lesson fixes the problems with human labels, one step at a time")
# the starting problem
s.box(10, 64, W - 20, 64, "sw-warn-box", 12)
emoji_or_icon(s, "📩", 50, 98, 40)
s.both(84, 92, "ส่วนที่ 1 ปัญหา: ผู้ช่วยวิจัย 2 คนอ่านจดหมาย 100 ฉบับเดียวกัน ติดป้ายอารมณ์ตรงกันแค่ 58 ฉบับ",
       "Part 1, the problem: 2 research assistants read the same 100 letters and agree on the emotion of only 58",
       "mp-p")
s.both(84, 118, "ผลวิจัยที่สร้างจากป้ายแบบนี้ก็เชื่อไม่ได้ (garbage in, garbage out)",
       "A finding built on such labels can't be trusted (garbage in, garbage out)", "mp-s")
# the four steps: fixed rows so the same kind of text lines up across the cards
CW, GAP, TOP, H = 246, 32, 146, 286
Y_EX, Y_Q, Y_RULE, Y_LEARN = TOP + 70, TOP + 128, TOP + 186, TOP + 208
for k, (pth, pen, em, exth, exen, qth, qen, lth, len_) in enumerate(STEPS):
    x = 10 + k * (CW + GAP)
    s.box(x, TOP, CW, H, "ml-cell", 14)
    s.badge(x + 24, TOP + 28, k + 1)
    s.both(x + 46, TOP + 35, pth, pen, "pl-label")
    circ(s, x + CW - 36, TOP + 30, 22, "var(--tag-concept-bg)")
    emoji_or_icon(s, em, x + CW - 36, TOP + 30, 34)
    para(s, x + 16, Y_EX, exth, exen, "mp-s", CW - 32, 14 * 1.15, 19)
    para(s, x + 16, Y_Q, qth, qen, "mp-t", CW - 32, 19 * 1.15, 25)
    s.line(x + 16, Y_RULE, x + CW - 16, Y_RULE, "mp-guide")
    s.both(x + 16, Y_LEARN, "เราเรียน:", "We learn:", "pl-note")
    para(s, x + 16, Y_LEARN + 26, lth, len_, "mp-acc", CW - 32, 17 * 1.15, 22)
    if k < 3:
        s.arrow(x + CW + 4, TOP + H / 2, x + CW + GAP - 4, TOP + H / 2)
# the case study
yb = TOP + H + 14
s.box(10, yb, W - 20, 56, "nt-band-a", 12)
emoji_or_icon(s, "💬", 50, yb + 28, 36)
s.both(84, yb + 35, "ส่วนที่ 6 กรณีศึกษา 2 เรื่อง: คอมเมนต์ร้านดัง (ป้ายกลุ่ม) และคอมเมนต์ไอดอล (คะแนน 1–5) ใช้ครบทั้ง 4 ขั้น",
       "Part 6, two case studies: a viral shop's comments (categories) and idol comments (scores 1–5), all 4 steps", "mp-p")
s.save("l15-labels-everywhere.svg", yb + 56 + 10)


# ================================================================ S03 four sides of quality
def chipr(x, y, w, label, cls="ml-cell"):
    s.box(x, y, w, 26, cls, 13)
    s.text(x + w / 2, y + 18, label, "mp-c", "middle")


def d_acc(x, y, w, h):
    chipr(x + 20, y + 14, 90, "Anxiety")
    chipr(x + 130, y + 14, 90, "Anxiety", "rc-res")
    s.text(x + 65, y + 66, "label", "mp-s", "middle")
    s.text(x + 175, y + 66, "gold ✓", "ml-ok", "middle")


def d_cons(x, y, w, h):
    for i, n in enumerate("AB"):
        embed_png(s, ("cast-ra-a.png", "cast-ra-b.png")[i], x + 16 + i * 110, y + 4, 36, 54)
        chipr(x + 54 + i * 110, y + 28, 64, "Joy", "ml-cell-b")
        s.text(x + 34 + i * 110, y + 80, n, "mp-c", "middle")


def d_comp(x, y, w, h):
    for r in range(3):
        for c in range(4):
            blank = (r, c) == (1, 2)
            s.box(x + 30 + c * 46, y + 10 + r * 22, 42, 18, "pl-chip-del" if blank else "ml-cell", 3)
    s.text(x + 30 + 2 * 46 + 21, y + 10 + 22 + 14, "?", "mp-acc", "middle")


def d_valid(x, y, w, h):
    for r in (30, 20, 10):
        ring(s, x + 70, y + 42, r, "mp-axis")
    circ(s, x + 70, y + 42, 4, NO)
    s.text(x + 116, y + 34, "fake news?", "mp-c")
    s.text(x + 116, y + 58, "≠ angry words", "mp-acc")


s = Svg(W, "Four sides of data quality: accuracy (the label matches a gold standard), consistency or reliability (the same "
           "letter gets the same label from anyone, this lesson's focus), completeness (no blank labels), validity (the "
           "label measures the concept you mean, e.g. fake news rather than angry language).")
term_grid(s, [
    (("ความถูกต้อง", "Accuracy"), d_acc, "ตรงกับ gold standard", "matches a gold standard", "เช่น ผู้เชี่ยวชาญ", "e.g. an expert's label"),
    (("ความสม่ำเสมอ", "Consistency"), d_cons, "ใครติดก็ได้ป้ายเดียวกัน", "same label from anyone", "← บทนี้เน้นข้อนี้", "← this lesson's focus"),
    (("ความครบ", "Completeness"), d_comp, "ไม่มีป้ายที่หายไป", "no missing labels", "ทุกช่องมีค่า", "every cell filled"),
    (("ความตรงตามที่วัด", "Validity"), d_valid, "วัดแนวคิดที่ตั้งใจจริง", "measures what you mean", "ไม่ใช่ทางลัดที่เห็นง่าย", "not an easy shortcut"),
])
s.save("l15-quality-four.svg", 212)

# ================================================================ S05 the concept vs the shortcut (story only)
s = Svg(W, "A label should measure the concept you mean, which is hard to see (deep, under the surface). Annotators may "
           "fall back on a cue that is easy to see on the surface. The exercise asks which surface cue each task's label "
           "might be measuring instead.")
s.bubble("ป้ายของเรากำลังวัดสิ่งที่ตั้งใจ หรือ “ทางลัด” ที่เห็นง่าย", "Does the label measure what you mean, or an easy “shortcut”?")
s.raw('<path d="M0 170 Q275 156 550 170 T1100 170 L1100 400 L0 400 Z" style="fill:var(--tag-concept-bg)"/>')
s.raw('<path d="M460 170 L520 92 L590 104 L640 170 Z" style="fill:var(--card);stroke:var(--card-border);stroke-width:2"/>')
s.raw('<path d="M400 172 L700 172 L780 300 L640 380 L470 372 L330 290 Z" style="fill:var(--card);stroke:var(--tag-concept-dot);stroke-width:2;opacity:.9"/>')
s.both(550, 150, "สิ่งที่เห็นง่าย = ?", "easy to see = ?", "mp-acc", "middle")
s.both(555, 270, "แนวคิดที่ตั้งใจวัด", "the concept you mean", "mp-t", "middle")
s.both(555, 300, "(เห็นยาก อยู่ใต้ผิว)", "(hard to see, under the surface)", "mp-s", "middle")
embed_png(s, "cast-ra-a.png", 190, 74, 60, 80)
s.raw('<path d="M240 120 L470 130" class="nt-arrow" stroke-dasharray="6 5"/>')
s.both(258, 96, "ผู้ติดป้ายมองแค่ผิว?", "the annotator looks at the surface?", "mp-s")
s.both(860, 230, "เช่น ดราม่า เพลงเศร้า ประชด", "e.g. drama, sad songs, sarcasm", "mp-c", "middle")
s.both(860, 256, "ทางลัดได้ป้ายถูกไหม? ดูภาพถัดไป", "does a shortcut get it right?", "mp-s", "middle")
s.save("l15-shortcut.svg", 400)

# ================================================================ S05 three shortcuts tried on two posts each (made-up posts)
SHORT = [  # label th/en, concept th/en, shortcut th/en, [(post th, post en, says th, says en, truth th, truth en, right)]
    ("ดราม่า", "Drama clip", "มีคนทะเลาะกันจริงในคลิป", "people really argue in the clip",
     "คอมเมนต์มี “!!!” → ดราม่า", "comments with “!!!” → drama",
     [("คลิปเต้น: “น่ารักมากกก!!! 😍”", "Dance clip: “she’s SO cute!!! 😍”", "ดราม่า", "drama", "แฟนคลับกรี๊ด", "a fan squealing", False),
      ("เถียงเรื่องหนี้: “พูดแบบนี้ได้ไง!!!”", "Debt argument: “how can you say that!!!”", "ดราม่า", "drama", "ทะเลาะกันจริง", "a real fight", True)]),
    ("เพลงเศร้า", "Sad song", "เนื้อเพลงเรื่องเศร้า เลิกรา สูญเสีย", "the lyrics are about sadness or loss",
     "จังหวะช้า → เศร้า", "slow tempo → sad",
     [("เพลงช้างานแต่ง: “จะรักเธอทุกวัน”", "Slow wedding song: “I’ll love you every day”", "เศร้า", "sad", "เพลงรักหวาน ๆ", "a sweet love song", False),
      ("แดนซ์จังหวะเร็ว: “ฉันโดนทิ้งอีกแล้ว”", "Fast dance song: “I got dumped again”", "ไม่เศร้า", "not sad", "เนื้อเพลงเศร้า", "sad lyrics", False)]),
    ("ประชด", "Sarcastic review", "หมายความตรงข้ามกับคำที่พิมพ์", "means the opposite of the words",
     "มี 🙃 หรือ 555 → ประชด", "🙃 or “lol” → sarcastic",
     [("“ดีมากเลย ได้ของช้าไป 3 วัน 🙃”", "“Great, my order only took 3 days 🙃”", "ประชด", "sarcastic", "ประชดจริง", "really sarcastic", True),
      ("“อร่อยมาก 555 จะสั่งอีก”", "“So tasty lol, ordering again”", "ประชด", "sarcastic", "ชมจริง", "real praise", False)]),
    ("ข่าวปลอม", "Fake news", "ข้อมูลเป็นเท็จ ตรวจสอบได้ว่าไม่จริง", "a false claim you can check",
     "ภาษาโกรธหรือหยาบ → ข่าวปลอม", "angry or rude words → fake",
     [("“นายกฯ โกรธจัด! ตอกกลับสื่อกลางสภา”", "“PM furious! Hits back at the press”", "ปลอม", "fake", "ข่าวจริง", "real news", False),
      ("“ผลวิจัยยืนยัน น้ำมะนาวรักษามะเร็งได้”", "“Study confirms lemon water cures cancer”", "จริง", "real", "ข่าวปลอม (เขียนสุภาพ)", "fake, written politely", False)]),
]
short_title = ("Three shortcuts tried on two made-up posts each. Drama (people really argue): the shortcut 'comments with !!! → "
           "drama' calls a squealing fan's dance clip drama (wrong) and a real debt argument drama (right). Sad song (sad "
           "lyrics): 'slow tempo → sad' calls a slow wedding love song sad (wrong) and a fast dance song about being dumped "
           "not sad (wrong). Sarcasm (means the opposite): '🙃 or lol → sarcastic' is right on 'Great, my order only took 3 "
           "days 🙃' and wrong on 'So tasty lol, ordering again'. Fake news (a false claim): 'angry or rude words → fake' calls "
           "an angry but real headline fake and a politely written false claim real; a model trained on these labels "
           "becomes a detector of angry, toxic language, not of fake news. The shortcuts are right on 2 of 8 posts.")

def shortcut_picture(name, rows, model_band=True, total=True):
    g = Svg(W, short_title)
    g.bubble("ทางลัดที่เห็นง่าย ได้ป้ายถูกบ้าง แต่ผิดบ่อย", "An easy shortcut gets some labels right, but many wrong")
    LW, PCW, RH, TOP = 300, 380, 140, 66
    for r, (lth, len_, cth, cen, sth, sen, posts) in enumerate(rows):
        y = TOP + r * (RH + 12)
        g.box(10, y, LW, RH, "nt-band-a", 12)
        g.both(28, y + 34, lth, len_, "mp-t")
        g.both(28, y + 60, "ตั้งใจวัด: " + cth, "Means: " + cen, "mp-s")
        g.box(24, y + 78, LW - 28, 46, "rc-ctx", 8)
        g.both(36, y + 96, "ทางลัด:", "Shortcut:", "mp-s")
        g.both(36, y + 116, sth, sen, "mp-p")
        for k, (pth, pen, say_th, say_en, tth, ten, ok) in enumerate(posts):
            x = 10 + LW + 14 + k * (PCW + 14)
            g.box(x, y, PCW, RH, "ml-cell" if ok else "sw-warn-box", 12)
            g.both(x + 18, y + 32, pth, pen, "mp-p")
            g.both(x + 18, y + 66, "ทางลัดบอกว่า: " + say_th, "Shortcut says: " + say_en, "mp-s")
            g.both(x + 18, y + 90, "ความจริง: " + tth, "Truth: " + ten, "mp-s")
            g.both(x + 18, y + 122, "✓ ทางลัดถูก" if ok else "✗ ทางลัดผิด", "✓ shortcut right" if ok else "✗ shortcut wrong",
                   "ml-ok" if ok else "ml-neg")
    yb = TOP + len(rows) * (RH + 12)
    if model_band:  # what a model learns from the fake-news labels
        g.box(10, yb, W - 20, 72, "sw-warn-box", 12)
        emoji_or_icon(g, "🤖", 48, yb + 36, 40)
        g.both(84, yb + 26, "ถ้าเอาป้าย “ข่าวปลอม” ชุดนี้ไปฝึกโมเดล โมเดลจะเรียนทางลัดตามไปด้วย",
               "Train a model on these “fake news” labels and it learns the shortcut too", "mp-p")
        g.both(84, yb + 56, "ได้ตัวจับภาษาโกรธหรือหยาบ (toxic) ไม่ใช่ตัวจับข่าวปลอม",
               "You get a toxic-language detector, not a fake-news detector", "ml-neg")
        yb += 72
    if total:
        yb += 30
        g.both(W / 2, yb, "ทางลัดถูกแค่ 2 จาก 8 โพสต์: ป้ายที่ได้วัด “!!!” จังหวะเพลง อีโมจิ และน้ำเสียง ไม่ใช่สิ่งที่ตั้งใจวัด",
               "The shortcuts are right on only 2 of 8 posts: the labels measure “!!!”, tempo, emoji and tone, not what we meant",
               "pl-label", "middle")
        yb += 18
    g.save(name, yb + 4)


shortcut_picture("l15-shortcut-examples.svg", SHORT)                                # the page
shortcut_picture("l15-shortcut-examples-1.svg", SHORT[:2], model_band=False, total=False)  # projector, frame 1
shortcut_picture("l15-shortcut-examples-2.svg", SHORT[2:])                          # projector, frame 2

# ================================================================ S07 what a good guideline has (empty checklist)
PARTS = [("นิยามที่ชัดและวัดได้", "clear, measurable definitions"), ("ตัวอย่างบวกและลบ", "positive and negative examples"),
         ("กฎกรณีขอบ", "edge-case rules"), ("กฎเมื่อป้ายชนกัน", "a rule when labels clash"), ("ป้าย “ไม่แน่ใจ”", "an Unsure code")]
s = Svg(W, "What to look for in a guideline: clear, measurable definitions; positive and negative examples; edge-case rules; "
           "a rule for when labels clash; an Unsure code. The exercise checks guidelines A, B and C against these five.")
s.bubble("คู่มือที่ดีมีครบ 5 ส่วนไหม", "Does the guideline have all 5 parts?")
s.box(320, 70, 460, 300, "ml-cell", 16)
s.fill(470, 60, 160, 26, "var(--ink-2)", 8)
for i, (th, en) in enumerate(PARTS):
    y = 116 + i * 50
    s.box(350, y, 28, 28, "ml-cell", 6)
    s.both(394, y + 21, th, en, "mp-t")
for k, n in enumerate("ABC"):
    s.box(840, 120 + k * 76, 200, 56, "nt-band-a", 12)
    s.both(940, 154 + k * 76, f"คู่มือ {n}: ?", f"guideline {n}: ?", "mp-t", "middle")
emoji_or_icon(s, "📋", 150, 222, 110)
s.save("l15-guide-checklist.svg", 382)

# ================================================================ S08 the lazy annotator
s = Svg(W, "Why percent agreement is not enough. 100 letters: research assistant B labels 35 of them Anxiety (red). A lazy "
           "annotator answers 'not anxious' for every letter without reading. They still agree on the 65 letters B called "
           "not anxious: 65% agreement for free.")
s.bubble("คนขี้เกียจตอบ “ไม่กังวล” ทุกฉบับ ตรงกับ B กี่ %", "A lazy annotator says “not anxious” to all: how often do they agree with B?")
s.panel(10, 70, 560, 300, "ml-cell", "จดหมาย 100 ฉบับ: ป้ายของ B", "100 letters: B's labels", 1)
anx = {(r * 10 + c) for r in range(10) for c in range(10) if (r * 7 + c * 3) % 20 < 7}
while len(anx) > 35:
    anx.pop()
for i in range(100):
    r, c = divmod(i, 10)
    s.fill(40 + c * 30, 110 + r * 24, 24, 18, NO if i in anx else "var(--card-border)", 3)
s.fill(360, 140, 18, 18, NO, 3)
s.both(386, 154, f"Anxiety {len(anx)}", f"Anxiety {len(anx)}", "mp-c")
s.fill(360, 172, 18, 18, "var(--card-border)", 3)
s.both(386, 186, f"ไม่กังวล {100 - len(anx)}", f"not anxious {100 - len(anx)}", "mp-c")
s.panel(590, 70, 500, 300, "ml-cell", "คนขี้เกียจไม่อ่านเลย", "The lazy annotator reads nothing", 2)
embed_png(s, "cast-yawn.png", 612, 104, 76, 104)
s.box(690, 140, 180, 34, "nt-bubble", 17)
s.both(780, 162, "“ไม่กังวล” ×100", "“not anxious” ×100", "mp-c", "middle")
s.box(620, 220, 440, 120, "rc-con", 12)
s.both(840, 252, "ตรงกับ B", "agrees with B", "mp-s", "middle")
s.text(840, 294, "65% ✗", "mp-big", "middle")
s.both(840, 324, "ทั้งที่ไม่ได้อ่านสักฉบับ", "without reading a single letter", "mp-s", "middle")
s.save("l15-lazy-annotator.svg", 380)

# ================================================================ S10 the kappa scale
BANDS = [("< 0", "แย่กว่าบังเอิญ", "Poor", -0.2, 0.0), ("0–0.20", "เล็กน้อย", "Slight", 0.0, 0.2), ("0.21–0.40", "พอใช้", "Fair", 0.2, 0.4),
         ("0.41–0.60", "ปานกลาง", "Moderate", 0.4, 0.6), ("0.61–0.80", "ค่อนข้างมาก", "Substantial", 0.6, 0.8),
         ("0.81–1", "เกือบสมบูรณ์", "Almost perfect", 0.8, 1.0)]
s = Svg(W, "The Landis & Koch kappa scale: below 0 poor, 0 to 0.20 slight, 0.21 to 0.40 fair, 0.41 to 0.60 moderate, 0.61 "
           "to 0.80 substantial, 0.81 to 1 almost perfect. The letters' pilot 1: Anxiety or not, kappa 0.35 (fair); four "
           "emotions, kappa 0.415 (moderate). A guide, not a law.")
s.bubble("kappa 0.35 หรือ 0.415 ถือว่าดีไหม", "Is a kappa of 0.35 or 0.415 good?")
XL, XR = 60, 1040
X = lambda v: XL + (v + 0.2) / 1.2 * (XR - XL)
shades = ["var(--accent)", "var(--accent-tint)", "var(--tag-example-bg)", "var(--tag-concept-bg)", "var(--tag-exercise-bg)", OK]
for (rng_, th, en, a, b), col in zip(BANDS, shades):
    s.fill(X(a), 150, X(b) - X(a) - 3, 60, col, 6)
    s.both((X(a) + X(b)) / 2, 236, th, en, "mp-c", "middle")
    s.text((X(a) + X(b)) / 2, 260, rng_, "mp-s", "middle")
for v, th, en, up in ((0.35, "Anxiety หรือไม่: 0.35", "Anxiety or not: 0.35", True), (0.415, "4 อารมณ์: 0.415", "4 emotions: 0.415", False)):
    s.raw(f'<path d="M{X(v):g} {140 if up else 220} L{X(v):g} {120 if up else 300}" class="mp-curve"/>')
    circ(s, X(v), 140 if up else 220, 6, "var(--ink)")
    s.both(X(v), 110 if up else 320, th, en, "mp-acc", "middle")
s.both(XR, 320, "ใช้เป็นแนวทาง ไม่ใช่กฎตายตัว", "a guide, not a law", "mp-s", "end")
s.save("l15-kappa-scale.svg", 340)

# ================================================================ S11 one set of labels, two ways to read it
RAW = [["Neu", "Neu", "Anx", "Joy"], ["Neu", "Neu", "Anx", "Neu"], ["Anx", "Neu", "Sad", "Anx"]]  # raters A, B, C × letters 1–4
LABS = ["Neu", "Joy", "Anx", "Sad"]
COUNTS = [[sum(RAW[r][c] == lab for r in range(3)) for lab in LABS] for c in range(4)]  # letters × labels
s = Svg(W, "The same labels from 3 raters on 4 letters, read two ways. The raw table (raters × letters): A gives Neutral, "
           "Neutral, Anxiety, Joy; B Neutral, Neutral, Anxiety, Neutral; C Anxiety, Neutral, Sadness, Anxiety. Fleiss' "
           "kappa counts, for each letter, how many raters chose each label (letter 1: Neutral 2, Anxiety 1), so every "
           "letter needs the same number of raters and the labels must be categories. Krippendorff's alpha uses the raw "
           "table as it is, so a blank (C skipped letter 4) is fine, and labels can also be ordered or numbers. On pilot 1's "
           "emotions: kappa 0.373, alpha 0.375.")
s.bubble("ป้ายชุดเดียวกัน อ่านได้สองแบบ", "One set of labels, read two ways")
# 1 the raw labels
RX, RY, CW2 = 360, 96, 92
s.box(RX - 110, 66, 600, 196, "rc-ctx", 14)
s.badge(RX - 82, 92, 1)
s.both(RX - 60, 98, "ป้ายที่ผู้ติดป้าย 3 คนให้จดหมาย 4 ฉบับ", "What 3 raters gave 4 letters", "pl-label")
for c in range(4):
    s.both(RX + 60 + c * CW2 + 37, RY + 34, f"ฉบับ {c + 1}", f"letter {c + 1}", "mp-s", "middle")
for r in range(3):
    s.text(RX + 30, RY + 66 + r * 40, "ABC"[r], "mp-n", "middle")
    for c in range(4):
        s.box(RX + 60 + c * CW2, RY + 44 + r * 40, 74, 32, "ml-cell", 6)
        s.text(RX + 60 + c * CW2 + 37, RY + 66 + r * 40, RAW[r][c], "mp-c", "middle")
# arrows to the two readings
s.arrow(RX + 40, 264, 280, 314)
s.arrow(RX + 400, 264, 820, 314)
s.both(250, 296, "นับต่อฉบับ", "count per letter", "mp-acc", "middle")
s.both(870, 296, "ใช้ตารางนี้ตรง ๆ", "use the table as it is", "mp-acc", "middle")
# 2 Fleiss
s.panel(10, 318, 530, 330, "ml-cell", "Fleiss' kappa: จดหมาย × ป้าย", "Fleiss' kappa: letters × labels", 2)
for j, lab in enumerate(LABS):
    s.text(170 + j * 86, 384, lab, "mp-s", "middle")
for i in range(4):
    s.both(36, 414 + i * 38, f"ฉบับ {i + 1}", f"letter {i + 1}", "mp-c")
    for j in range(4):
        v = COUNTS[i][j]
        s.box(136 + j * 86, 394 + i * 38, 68, 30, "ml-cell-b" if v else "ml-cell", 6)
        s.text(170 + j * 86, 415 + i * 38, str(v), "mp-n", "middle")
s.both(36, 568, "ช่อง = กี่คนเลือกป้ายนั้น (ฉบับ 1: Neu 2, Anx 1)", "cell = how many chose it (letter 1: Neu 2, Anx 1)", "mp-s")
s.both(36, 598, "✗ ทุกฉบับต้องมีผู้ติดป้ายเท่ากัน", "✗ same number of raters on every letter", "ml-neg")
s.both(36, 626, "✗ ป้ายแบบกลุ่มเท่านั้น", "✗ categories only", "ml-neg")
s.text(520, 626, "pilot 1: κ = 0.373", "mp-acc", "end")
# 3 Krippendorff
s.panel(560, 318, 530, 330, "ml-cell", "Krippendorff's α: ผู้ติดป้าย × จดหมาย", "Krippendorff's α: raters × letters", 3)
for c in range(4):
    s.both(680 + c * 92 + 37, 384, f"ฉบับ {c + 1}", f"letter {c + 1}", "mp-s", "middle")
for r in range(3):
    s.text(620, 416 + r * 40, "ABC"[r], "mp-n", "middle")
    for c in range(4):
        blank = (r == 2 and c == 3)
        s.box(680 + c * 92, 394 + r * 40, 74, 32, "pl-chip-del" if blank else "ml-cell", 6)
        s.text(680 + c * 92 + 37, 416 + r * 40, "–" if blank else RAW[r][c], "mp-acc" if blank else "mp-c", "middle")
s.both(586, 532, "ถ้า C ไม่ได้อ่านฉบับ 4 เว้นว่างไว้ได้", "If C skipped letter 4, leave it blank", "mp-s")
s.both(586, 568, "✓ เว้นว่างได้ · ✓ ป้ายแบบกลุ่ม ลำดับ หรือตัวเลข", "✓ blanks allowed · ✓ categories, ranks or numbers", "ml-ok")
s.both(586, 600, "(เช่น ความเป็นทางการ 1–10 ก็ใช้ได้)", "(formality 1–10 works too)", "mp-s")
s.text(1070, 626, "pilot 1: α = 0.375", "mp-acc", "end")
s.save("l15-two-shapes.svg", 660)

# ================================================================ S13 which measure
s = Svg(W, "Choosing an agreement measure from two questions, how many raters and what kind of label: 2 raters with "
           "categories → Cohen's kappa (letters A vs B: 0.415); 3 or more raters, same number per item, categories → Fleiss' "
           "kappa (0.373); any number, gaps allowed, any kind of label → Krippendorff's alpha (0.375); numbers or scales → "
           "ICC (formality: 0.418).")
s.bubble("ข้อมูลของเราควรใช้ตัววัดไหน", "Which measure fits your data?")
s.box(40, 180, 200, 60, "ml-model", 14)
s.both(140, 206, "ผู้ติดป้ายกี่คน", "how many raters?", "ml-model-text", "middle")
s.both(140, 228, "ป้ายแบบไหน", "what kind of label?", "ml-model-sub", "middle")
LEAVES = [("2 คน · ป้ายกลุ่ม", "2 raters · categories", "Cohen's κ", "0.415"),
          ("3+ คน ครบทุกชิ้น · กลุ่ม", "3+, every item complete", "Fleiss' κ", "0.373"),
          ("กี่คนก็ได้ ขาดได้ · ป้ายแบบใดก็ได้", "any number, gaps OK · any label", "Krippendorff's α", "0.375"),
          ("ป้ายเป็นตัวเลข / สเกล", "numbers or scales", "ICC", "0.418")]
for i, (cth, cen, m, v) in enumerate(LEAVES):
    y = 74 + i * 76
    s.arrow(244, 210, 330, y + 26)
    s.box(334, y, 360, 52, "nt-band-a", 12)
    s.both(352, y + 32, cth, cen, "mp-t")
    s.arrow(698, y + 26, 736, y + 26)
    s.box(740, y, 200, 52, "rc-res", 12)
    s.text(840, y + 33, m, "mp-t", "middle")
    s.text(1060, y + 33, v, "mp-acc", "end")
s.both(1060, 384, "ค่าจาก pilot 1", "pilot 1 values", "mp-s", "end")
s.save("l15-which-measure.svg", 396)

# ================================================================ S15 labeling functions vote
VOTES = [("SAD", None, None, "NOT", "SAD"), (None, "SAD", None, "NOT", "SAD"), (None, None, "NOT", None, "NOT"),
         (None, None, "NOT", "NOT", "NOT"), ("SAD", None, None, None, "SAD"), (None, None, None, "NOT", "NOT"),
         ("SAD", "SAD", None, "NOT", "SAD"), ("SAD", None, "NOT", "NOT", "SAD")]
RULES = [("lf_cry", "4 / 4"), ("lf_heartbroken", "2 / 2"), ("lf_happy", "2 / 3"), ("lf_has_I", "2 / 6")]
s = Svg(W, "Four labeling functions vote on 8 sentences: SAD, NOT or abstain (blank), next to the true (gold) label. A vote "
           "matching gold is solid, a wrong vote is outlined in red. Right out of votes cast: lf_cry 4 of 4, lf_heartbroken "
           "2 of 2, lf_happy 2 of 3, lf_has_I 2 of 6 (a bad rule that clashes with the others).")
s.bubble("ให้กฎ 4 ข้อโหวตป้ายของประโยค ป้ายที่ได้ดีแค่ไหน", "Let 4 rules vote on each sentence: how good are the labels?")
CX = [250, 420, 590, 760, 950]
for c, (name, _) in enumerate(RULES):
    s.text(CX[c], 92, name, "mp-mono", "middle")
s.text(CX[4], 92, "gold", "mp-mono", "middle")
for r, row in enumerate(VOTES):
    y = 104 + r * 32
    s.both(40, y + 20, f"ประโยค {r + 1}", f"sentence {r + 1}", "mp-c")
    gold = row[4]
    for c, v in enumerate(row):
        if v is None:
            s.text(CX[c], y + 20, "·", "mp-s", "middle")
            continue
        if c == 4:
            cls = "rc-ctx"
        else:
            cls = "ml-cell-b" if v == gold else "rc-con"
        s.box(CX[c] - 40, y + 3, 80, 24, cls, 12)
        s.text(CX[c], y + 20, v, "mp-c", "middle")
s.line(30, 366, 1070, 366, "mp-axis")
s.both(40, 392, "ถูก / โหวต", "right / votes", "mp-c")
for c, (name, r) in enumerate(RULES):
    bad = name == "lf_has_I"
    s.text(CX[c], 392, r + (" ✗" if bad else ""), "ml-neg" if bad else "mp-n", "middle")
s.save("l15-lf-votes.svg", 404)

# ================================================================ S16 LLM prompts
s = Svg(W, "Making an LLM follow your guideline. Zero-shot ('Label the sentiment') turns 'It wasn't bad.' into positive, "
           "against the guideline. A prompt with the guideline, few-shot examples, step-by-step reasoning and a JSON format "
           "returns neutral with its reason: a negated negative is weak praise.")
s.bubble("ให้ LLM ติดป้ายตามคู่มือของเรา ไม่ใช่ตามความเข้าใจของมันเอง", "Make the LLM label by your guideline, not its own idea")
for k, (tth, ten, chips, ans_th, ans_en, ok) in enumerate((
        ("Zero-shot", "Zero-shot", [("บอกงานอย่างเดียว", "just the task")], "positive ✗", "positive ✗", False),
        ("Prompt ที่มีคู่มือ", "A guided prompt", [("คู่มือ", "guideline"), ("ตัวอย่าง", "few-shot"), ("คิดทีละขั้น", "step by step"),
                                                  ("JSON", "JSON")], "neutral ✓", "neutral ✓", True))):
    y = 80 + k * 150
    s.box(10, y, 1080, 130, "rc-res" if ok else "rc-con", 14)
    s.both(30, y + 34, tth, ten, "mp-t")
    cx = 30
    for cth, cen in chips:
        w = max(width(cth, 16), width(cen, 16)) + 28
        s.box(cx, y + 52, w, 30, "ml-cell", 15)
        s.both(cx + w / 2, y + 73, cth, cen, "mp-chip", "middle")
        cx += w + 10
    s.box(560, y + 40, 210, 44, "ml-cell", 10)
    s.text(665, y + 68, "“It wasn't bad.”", "mp-c", "middle")
    s.arrow(774, y + 62, 810, y + 62)
    emoji_or_icon(s, "🤖", 840, y + 54, 50)
    s.both(870, y + 70, ans_th, ans_en, "ml-ok" if ok else "ml-neg")
    if ok:
        s.both(560, y + 112, "เหตุผล: ปฏิเสธคำลบ = ชมแบบจืด", "reason: a negated negative is weak praise", "mp-s")
s.save("l15-llm-prompt.svg", 380)

# ================================================================ S16 majority vote of three LLMs
MV = [("“It wasn't bad.”", ["neutral", "neutral", "positive"]),
      ("“Oh, just a perfect ending…”", ["negative", "negative", "negative"]),
      ("“Plot was mid but the OST slaps”", ["positive", "negative", "neutral"])]
s = Svg(W, "Majority vote of three LLMs (GPT, Claude, Gemini) on three movie comments. 'It wasn't bad.': neutral, neutral, "
           "positive, so neutral wins 2 of 3. 'Oh, just a perfect ending…': negative from all three, 3 of 3, sure. 'Plot was "
           "mid but the OST slaps': positive, negative, neutral, no majority, so a person decides.")
s.bubble("ถาม LLM หลายตัว แล้วใช้คำตอบที่ได้เสียงมากที่สุด", "Ask several LLMs and keep the answer with the most votes")
MX = [520, 660, 800]
for c, name in enumerate(("GPT", "Claude", "Gemini")):
    emoji_or_icon(s, "🤖", MX[c], 92, 40)
    s.text(MX[c], 134, name, "mp-p", "middle")
s.both(980, 134, "เสียงข้างมาก", "majority", "mp-p", "middle")
for r, (text, labels) in enumerate(MV):
    y = 152 + r * 74
    s.box(10, y, 1080, 62, "dg-row", 12)
    s.text(30, y + 37, text, "mp-c")
    top = max(labels, key=labels.count)
    n = labels.count(top)
    for c, lab in enumerate(labels):
        s.box(MX[c] - 58, y + 16, 116, 30, "ml-cell-b" if n >= 2 and lab == top else "ml-cell", 15)
        s.text(MX[c], y + 37, lab, "mp-chip", "middle")
    if n >= 2:
        s.box(892, y + 12, 176, 38, "rc-res", 19)
        s.text(980, y + 37, f"{top} ({n}/3)", "ml-ok", "middle")
    else:
        s.box(892, y + 12, 176, 38, "rc-con", 19)
        s.both(980, y + 37, "ไม่มี → ให้คนตัดสิน", "none → a person", "ml-neg", "middle")
s.box(10, 386, 1080, 46, "rc-ctx", 12)
s.both(550, 416, "3/3 = มั่นใจ  ·  2/3 = ใช้ได้  ·  1-1-1 = ส่งให้คนติดป้าย",
       "3/3 = sure  ·  2/3 = use it  ·  1-1-1 = send it to a person", "pl-label", "middle")
s.save("l15-llm-vote.svg", 444)

# ================================================================ S17 active learning
s = Svg(W, "Active learning. Left: the loop: 1 people label 100 letters, 2 train a model, 3 the model scores the other 900 "
           "letters, 4 the 100 it is least sure about go back to people; repeat with 200, 300 labels. Right: three letters' "
           "probabilities for SAD, NEUTRAL, JOY: X 0.99 / 0.005 / 0.005 (margin 0.99 − 0.005 = 0.98, sure), Y 0.51 / 0.49 / 0 "
           "(margin 0.02), Z 0.33 / 0.33 / 0.34 (margin 0.01, the least sure): send Z first, skip X.")
s.bubble("ควรส่งจดหมายฉบับไหนให้คนอ่าน", "Which letter should a person read?")
s.panel(10, 70, 470, 360, "ml-cell", "วงจร active learning", "The active-learning loop", 1)
LOOP = [(30, 126, "① คนติดป้าย 100 ฉบับ", "① people label 100"),
        (262, 126, "② ฝึกโมเดล", "② train a model"),
        (262, 296, "③ โมเดลทาย 900 ฉบับที่เหลือ", "③ model scores the other 900"),
        (30, 296, "④ ส่ง 100 ฉบับที่ไม่แน่ใจที่สุด", "④ send the 100 least sure")]
BW, BH = 198, 56
for (x, y, th, en) in LOOP:
    s.box(x, y, BW, BH, "nt-band-a", 12)
    s.both(x + BW / 2, y + 34, th, en, "mp-chip", "middle")
s.arrow(30 + BW + 4, 154, 262 - 4, 154)                    # 1 → 2
s.arrow(262 + BW / 2, 126 + BH + 4, 262 + BW / 2, 296 - 4)  # 2 → 3
s.arrow(262 - 4, 324, 30 + BW + 4, 324)                    # 3 → 4
s.arrow(30 + BW / 2, 296 - 4, 30 + BW / 2, 126 + BH + 4)    # 4 → 1
s.both(245, 232, "วนซ้ำ", "repeat", "pl-label", "middle")
s.both(245, 258, "ป้าย 100 → 200 → 300 …", "labels 100 → 200 → 300 …", "mp-s", "middle")
s.both(30, 408, "คนอ่านเฉพาะฉบับที่โมเดลยังไม่รู้ ไม่เสียเวลากับฉบับที่ง่าย", "People only read what the model can't decide yet", "mp-s")
s.panel(500, 70, 590, 360, "ml-cell", "โมเดลมั่นใจแค่ไหน", "How sure is the model?", 2)
LET = [("X", [0.99, 0.005, 0.005], "0.99 − 0.005 = 0.98", ("มั่นใจ ไม่ต้องส่ง", "sure: skip")),
       ("Y", [0.51, 0.49, 0.0], "0.51 − 0.49 = 0.02", ("ลังเล SAD/NEUTRAL", "torn SAD/NEUTRAL")),
       ("Z", [0.33, 0.33, 0.34], "0.34 − 0.33 = 0.01", ("ไม่รู้เลย ส่งก่อน ✓", "no idea: send first ✓"))]
COLS = (BLUE, "var(--muted)", OK)
for c, (lab, col) in enumerate(zip(("SAD", "NEUTRAL", "JOY"), COLS)):
    s.fill(530 + c * 120, 126, 14, 14, col, 3)
    s.text(550 + c * 120, 138, lab, "mp-s")
s.both(900, 138, "margin = อันดับ 1 − อันดับ 2", "margin = top − second", "mp-s")
for r, (n, ps, calc, (vth, ven)) in enumerate(LET):
    y = 158 + r * 80
    s.both(526, y + 26, f"ฉบับ {n}", f"letter {n}", "mp-t")
    x = 610
    for p, col in zip(ps, COLS):
        if p >= 0.05:
            s.fill(x, y + 6, p * 270, 30, col, 3)
            s.raw(f'<text x="{x + p * 135:.1f}" y="{y + 27}" text-anchor="middle" style="fill:#fff;font:600 14px var(--font-head)">{p:g}</text>')
        x += p * 270
    pick = n == "Z"
    s.text(900, y + 20, calc, "mp-acc" if pick else "mp-c")
    s.both(900, y + 44, vth, ven, "ml-ok" if pick else "mp-s")
s.both(526, 408, "margin ยิ่งน้อย โมเดลยิ่งไม่แน่ใจ → คนควรอ่านฉบับนั้น", "The smaller the margin, the less sure the model → a person should read it", "mp-s")
s.save("l15-active-loop.svg", 440)

# ================================================================ S18 compare the three ways to scale up
SCALE = [
    ("weak supervision", "weak supervision", "📜",
     ("คนทำ: เขียนกฎสั้น ๆ 10–50 ข้อ", "People: write 10–50 rules"),
     [("ป้ายครบ 20,000 ฉบับในไม่กี่นาที", "labels all 20,000 in minutes"),
      ("กฎอ่านออก อธิบายและแก้ได้", "rules are readable and fixable")],
     [("ต้องมีผู้เชี่ยวชาญเขียนกฎ", "needs an expert to write rules"),
      ("พลาดสิ่งที่ไม่มีคำบ่งชี้ เช่น ประชด", "misses what has no keyword")],
     ("เหมาะ: ข้อมูลมาก มีคำบ่งชี้ชัด", "Best: big data, clear cue words")),
    ("LLM ติดป้ายรอบแรก", "LLM first pass", "🤖",
     ("คนทำ: ใส่คู่มือใน prompt แล้วตรวจแก้", "People: prompt it, then review"),
     [("เข้าใจบริบท ประชด การตีความ", "gets context, irony, nuance"),
      ("เร็วกว่าเริ่มจากศูนย์ 5–10 เท่า", "5–10× faster than from scratch")],
     [("ผิดได้อย่างมั่นใจ ต้องสุ่มตรวจ", "can be confidently wrong"),
      ("เสียเงิน และส่งข้อมูลออกนอก", "costs money, data leaves you")],
     ("เหมาะ: งานตีความที่เขียนกฎไม่ได้", "Best: interpretive tasks")),
    ("active learning", "active learning", "🙋",
     ("คนทำ: ติดป้ายเฉพาะฉบับที่โมเดลถาม", "People: label only what it asks"),
     [("ใช้เวลาคนคุ้มที่สุด", "spends people's time best"),
      ("ทุกป้ายมาจากคน คุณภาพสูง", "every label is human")],
     [("ต้องวนฝึก-ทาย-ส่ง หลายรอบ", "needs many rounds"),
      ("ชุดที่ได้เอียงไปทางฉบับยาก", "labels lean to hard cases")],
     ("เหมาะ: มีคนติดป้าย แต่เวลาน้อย", "Best: few annotator hours")),
]
s = Svg(W, "Comparing the three ways to scale up labelling. Weak supervision: people write 10–50 rules; it labels all 20,000 "
           "letters in minutes and the rules can be read and fixed, but it needs an expert and misses anything without a "
           "cue word, such as irony. LLM first pass: people put the guideline in a prompt and review; it understands "
           "context and is 5–10 times faster than starting from scratch, but it can be confidently wrong, costs money and "
           "sends the data away. Active learning: people label only the letters the model asks about; it spends their "
           "time best and every label is human, but it needs many rounds and the labelled set leans to hard cases. All "
           "three need a human gold set to check quality, and they can be combined.")
s.bubble("ขยายการติดป้ายสามวิธี ได้อะไร เสียอะไร", "Three ways to scale up: what do you gain, what do you lose?")
PW = 352
for i, (tth, ten, icon_, (dth, den), pros, cons, (bth, ben)) in enumerate(SCALE):
    x0 = 10 + i * (PW + 12)
    s.panel(x0, 70, PW, 440, "ml-cell", tth, ten, i + 1)
    emoji_or_icon(s, icon_, x0 + PW / 2, 150, 52)
    s.both(x0 + 20, 206, dth, den, "pl-note")
    s.box(x0 + 14, 222, PW - 28, 104, "nt-band-a", 10)
    s.both(x0 + 28, 248, "ข้อดี", "Benefits", "mp-s")
    for k, (th, en) in enumerate(pros):
        s.both(x0 + 28, 278 + k * 30, "✓ " + th, "✓ " + en, "pl-note")
    s.box(x0 + 14, 336, PW - 28, 104, "sw-warn-box", 10)
    s.both(x0 + 28, 362, "ข้อเสีย", "Drawbacks", "mp-s")
    for k, (th, en) in enumerate(cons):
        s.both(x0 + 28, 392 + k * 30, "✗ " + th, "✗ " + en, "pl-note")
    s.both(x0 + 20, 478, bth, ben, "pl-label")
    for txt in [dth, den, bth, ben] + [t for pair in pros + cons for t in pair]:
        if width(txt, 17) >= PW - 40:
            print('LONG', round(width(txt, 17)), txt)
s.both(10, 540, "ทั้งสามวิธีต้องมีชุด gold ที่คนติดป้ายไว้เพื่อตรวจคุณภาพ และใช้ร่วมกันได้: LLM ติดรอบแรก แล้ว active learning ส่งฉบับที่ไม่แน่ใจให้คน",
       "All three need a human gold set to check quality, and they combine: an LLM labels first, then active learning sends the unsure ones to people", "mp-s")
s.save("l15-scale-compare.svg", 556)


# ================================================================ S19 takeaways
def emoji(icon):
    return lambda x, y, w, h: emoji_or_icon(s, icon, x + w / 2, y + h / 2, 66)


s = Svg(W, "Six takeaways: garbage in, garbage out; the guideline is your contract; measure inter-rater reliability instead "
           "of guessing; scale up with a gold set; repeat the quality loop; reliable is not the same as valid.")
bottom = term_grid(s, [
    ("GIGO", emoji("🗑️"), "ป้ายแย่ = ข้อสรุปแย่", "bad labels, bad findings", "โมเดลเก่งแค่ไหนก็แก้ไม่ได้", "no model can fix them"),
    (("คู่มือ = สัญญา", "Guidelines = contract"), emoji("📜"), "นิยาม ตัวอย่าง กรณีขอบ", "definitions, examples,", "และป้ายสำรอง", "edge cases, fallbacks"),
    (("วัด IRR อย่าเดา", "Measure IRR"), emoji("📏"), "κ, α หรือ ICC", "κ, α or ICC", "ค่าต่ำ = แก้คู่มือ", "low = fix the guide"),
    (("ขยายอย่างฉลาด", "Scale smart"), emoji("📈"), "ใช้ชุด gold คุมงาน", "a gold set steers", "weak sup., LLM, active", "weak sup., LLMs, active"),
    (("ทำวงจรซ้ำ", "Repeat the loop"), emoji("🔁"), "แก้ → วัด → ขยาย", "refine → measure →", "→ ตรวจ → แก้", "scale → audit → refine"),
    ("Reliable ≠ valid", emoji("🎯"), "ตรงกันอาจวัดผิดเรื่อง", "agreeing ≠ measuring", "ตรวจแนวคิดเสมอ", "the right concept"),
], cols=3, tw=352)
s.save("l15-takeaways.svg", bottom + 10)


# ================================================================ S21 case study 2: three friends score comments 1–5 (made up)
BEFORE = [("น่ารักมากกก 😍", "“so cute 😍”", (1, 1, 1)), ("ไม่ยอมมม!!!!", "“NOOO!!!!”", (5, 1, 2)),
          ("หน้าแบบนี้ยังกล้าออกงาน", "“that face, at an event?”", (2, 4, None)), ("ไปตายซะ", "“go die”", (5, 5, 4))]
AFTER = [("รักพี่ที่สุด 💕", "“love you most 💕”", (1, 1, 1)), ("พี่ไม่ผิดดดด!!!!", "“NOT HER FAULT!!!!”", (1, 1, 2)),
         ("แต่งตัวแบบนี้ไม่อายเหรอ", "“dressed like that, no shame?”", (4, 4, 3)), ("หายไปจากวงการเลย", "“just quit forever”", (4, 5, 5))]
RCOL = ["var(--tag-concept-dot)", "var(--tag-example-dot)", "var(--accent)"]
s = Svg(W, "Case study 2, made up: three friends score how toxic comments under an idol's posts "
           "are, from 1 (friendly) to 5 (an insult or threat). Round 1, with no guideline: their scores are far "
           "apart ('NOOO!!!!' gets 5, 1 and 2; C skipped one comment), ICC 0.52. Round 2, with an anchor comment for 1, 3 "
           "and 5 and the rule that CAPS or '!!!' alone never raises the score, on new comments: close together, ICC 0.86.")
s.bubble("กรณีศึกษา 2: เพื่อน 3 คนให้คะแนนความดุของคอมเมนต์ 1–5", "Case study 2: three friends score how toxic comments are, 1–5")


def score_panel(x0, th, en, rows, foot_th, foot_en, ok):
    PW_, Y0 = 500, 66
    s.box(x0, Y0, PW_, 340, "nt-band-a" if ok else "sw-warn-box", 14)
    s.both(x0 + 20, Y0 + 32, th, en, "pl-label")
    SX = x0 + 260                                     # the 1–5 strip
    sx = lambda v: SX + (v - 1) * 52
    for v in range(1, 6):
        s.text(sx(v), Y0 + 66, str(v), "mp-s", "middle")
    for k, (cth, cen, scores) in enumerate(rows):
        y = Y0 + 100 + k * 54
        s.both(x0 + 20, y + 6, cth, cen, "mp-p")
        s.line(sx(1), y, sx(5), y, "mp-guide")
        same = {}
        for r, v in enumerate(scores):
            if v is not None:
                same.setdefault(v, []).append(r)
        for r, v in enumerate(scores):
            if v is None:
                s.both(x0 + 20, y + 26, "(C ข้ามอันนี้)", "(C skipped this one)", "mp-s")
                continue
            group = same[v]
            cx = sx(v) + (group.index(r) - (len(group) - 1) / 2) * 19   # same score: side by side
            circ(s, cx, y, 9, RCOL[r])
            s.raw(f'<text x="{cx:g}" y="{y + 4:g}" text-anchor="middle" class="mp-s" style="fill:#fff;font-size:11px">{"ABC"[r]}</text>')
    s.both(x0 + 20, Y0 + 320, foot_th, foot_en, "ml-ok" if ok else "ml-neg")


score_panel(10, "รอบ 1: ยังไม่มีคู่มือ", "Round 1: no guideline yet", BEFORE,
            "✗ จุดห่างกันมาก · ICC 0.52", "✗ dots far apart · ICC 0.52", False)
s.arrow(516, 236, 584, 236)
score_panel(590, "รอบ 2: มีคู่มือแล้ว คอมเมนต์ใหม่", "Round 2: with a guideline, new comments", AFTER,
            "✓ จุดใกล้กัน · ICC 0.86 · α 0.84", "✓ dots close together · ICC 0.86 · α 0.84", True)
s.box(10, 418, W - 20, 56, "rc-ctx", 12)
s.both(28, 452, "คู่มือใหม่: ตัวอย่างหลักของคะแนน 1, 3, 5 + กฎ “ตัวใหญ่หรือ !!! อย่างเดียว ไม่เพิ่มคะแนน”",
       "New guideline: an anchor comment for 1, 3 and 5 + the rule “CAPS or !!! alone never raises the score”", "mp-p")
s.save("l15-case2.svg", 486)


# ================================================================ S19 case study 1 (made up): four pictures, top-down
# why → stage 1 people make the answer key → stage 2 the LLM labels everything → stage 3 check on test, then count
PW1, PH1, PY1 = 350, 256, 66
SARC = ("“อร่อยมากกก รอแค่ 2 ชม. 🙃”", "“Yummm, only a 2-hour wait 🙃”")
PRAISE = ("“ไก่นุ่มมาก อร่อย”", "“So tender. Delicious”")
COMPL = ("“รอคิว 2 ชม. ไม่ไหว”", "“2-hour queue. No way”")
NEUT = ("“ร้านอยู่ตรงไหนคะ”", "“Where is the shop?”")


def lab(x, y, th, en, cls, w=80, h=30):
    """A small label chip with ไทย/EN text centred in it."""
    s.box(x, y, w, h, cls, 8)
    s.both(x + w / 2, y + h / 2 + 5, th, en, "mp-c", "middle")


def step_panel(x, k, th, en, w=PW1, cls="nt-band-a"):
    s.box(x, PY1, w, PH1, cls, 14)
    s.badge(x + 28, PY1 + 28, k)
    s.both(x + 50, PY1 + 35, th, en, "pl-label")


# ---- picture 1: the data, and why neither people alone nor an LLM alone will do
s = Svg(W, "Case study 1 (made up). Left, the data: 20,000 comments under a chicken-rice shop's review clips, from before and "
           "after it went viral, with no label yet. Right, three ways to label them: read them all yourself (20,000 × 10 "
           "seconds ≈ 56 hours, too slow); let an LLM label them and just trust it (fast, but no way to know how many are "
           "wrong); people make a small answer key and the LLM does the rest (fast, and we know how far to trust it).")
s.bubble("คอมเมนต์ 20,000 อัน ยังไม่มีป้ายสักอัน จะติดป้ายอย่างไรดี", "20,000 comments and not one label: how do we label them?")
s.box(10, 64, 440, 292, "ml-cell", 14)
s.both(30, 94, "ข้อมูลของเรา", "Our data", "pl-label")
s.both(30, 116, "คอมเมนต์ใต้คลิปรีวิวร้านข้าวมันไก่", "comments under the shop's review clips", "mp-s")
s.both(65, 140, "เมื่อไร", "when", "mp-s", "middle")
s.both(114, 140, "คอมเมนต์", "comment", "mp-s")
s.both(419, 140, "ป้าย", "label", "mp-s", "middle")
for k, (pth, pen, cth, cen) in enumerate([
        ("ก่อนไวรัล", "before", *PRAISE), ("ก่อนไวรัล", "before", *NEUT),
        ("หลังไวรัล", "after", *COMPL), ("หลังไวรัล", "after", *SARC)]):
    y0 = 148 + k * 40
    lab(26, y0, pth, pen, "nt-band-a" if k < 2 else "sw-warn-box", 78)
    s.both(114, y0 + 21, cth, cen, "mp-chip")
    s.box(404, y0, 30, 30, "rc-ctx", 8)
    s.text(419, y0 + 21, "?", "mp-n", "middle")
s.both(30, 334, "… และอีก 19,996 อัน", "… and 19,996 more", "mp-s")
for k, (ok, tth, ten, dth, den, rth, ren) in enumerate([
        (False, "อ่านและติดป้ายเองทั้งหมด", "Read and label them all yourself",
         "20,000 อัน × 10 วินาที ≈ 56 ชั่วโมง", "20,000 × 10 seconds ≈ 56 hours", "✗ ช้าเกินไป", "✗ far too slow"),
        (False, "ให้ LLM ติดป้าย แล้วเชื่อเลย", "Let an LLM label them and just trust it",
         "เสร็จเร็ว แต่ไม่มีคำตอบที่ถูกไว้เทียบ", "fast, but there is no right answer to compare with",
         "✗ ไม่รู้ว่าผิดกี่อัน", "✗ no idea how many are wrong"),
        (True, "คนทำเฉลยชุดเล็ก แล้ว LLM ทำที่เหลือ", "People make an answer key; an LLM does the rest",
         "เฉลย 200 อันจากคน ใช้วัดว่า LLM ถูกกี่อัน", "200 human answers check how often the LLM is right",
         "✓ เร็ว และรู้ว่าเชื่อได้แค่ไหน", "✓ fast, and we know how far to trust it")]):
    x0, y0 = 462, 64 + k * 100
    s.box(x0, y0, 628, 92, "rc-res" if ok else "sw-warn-box", 14)
    if k == 0:
        person(s, x0 + 46, y0 + 43, BLUE)
    elif k == 1:
        emoji_or_icon(s, "🤖", x0 + 46, y0 + 46, 50)
    else:
        person(s, x0 + 30, y0 + 43, BLUE)
        emoji_or_icon(s, "🤖", x0 + 62, y0 + 47, 40)
    s.both(x0 + 96, y0 + 27, tth, ten, "pl-label")
    s.both(x0 + 96, y0 + 54, dth, den, "mp-r")
    s.both(x0 + 96, y0 + 83, rth, ren, "ml-ok" if ok else "ml-neg")
s.save("l15-case1-why.svg", 366)

# ---- picture 2, stage 1: people make the answer key (steps 1-3)
s = Svg(W, "Stage 1: people make the answer key. 1 Write the guideline: praise, complaint, neutral, each with an example "
           "comment. 2 A and B label the same comments on their own: a sarcastic comment splits them, kappa 0.45; after "
           "the rule 'sarcasm = complaint', on 200 new comments, kappa 0.80 (88% the same). 3 Their agreed answers are the "
           "answer key of 200, the gold set, split into dev 100 (homework: you may look) and test 100 (the exam: locked).")
s.bubble("ช่วงที่ 1: คนทำเฉลย (ชุด gold)", "Stage 1: people make the answer key (the gold set)")
X1 = [10, 375, 740]
step_panel(X1[0], 1, "เขียนคู่มือ", "Write the guideline")
step_panel(X1[1], 2, "A กับ B ติดป้ายแยกกัน", "A and B label separately")
step_panel(X1[2], 3, "รวมเป็นเฉลย แล้วแบ่งครึ่ง", "One answer key, split in two", cls="rc-ctx")
for a_ in (0, 1):
    s.arrow(X1[a_] + PW1 + 2, PY1 + PH1 / 2, X1[a_ + 1] - 2, PY1 + PH1 / 2)
x, y = X1[0], PY1
for k, (lth, len_, cls, cth, cen) in enumerate([
        ("ชม", "praise", "rc-res", *PRAISE), ("บ่น", "complaint", "sw-warn-box", *COMPL),
        ("เป็นกลาง", "neutral", "ml-cell", *NEUT)]):
    yy = y + 62 + k * 46
    lab(x + 18, yy, lth, len_, cls, 86)
    s.both(x + 116, yy + 21, cth, cen, "mp-chip")
s.both(x + 18, y + 226, "ป้ายละ 1 ความหมาย + 1 ตัวอย่าง", "one meaning + one example per label", "mp-c")
x = X1[1]
s.box(x + 18, y + 52, PW1 - 36, 34, "ml-cell", 8)
s.both(x + PW1 / 2, y + 75, *SARC, "mp-chip", "middle")
person(s, x + 34, y + 110, BLUE)
lab(x + 52, y + 98, "A: ชม", "A: praise", "rc-res", 96, 28)
person(s, x + 178, y + 110, GOLD)
lab(x + 196, y + 98, "B: บ่น", "B: complaint", "sw-warn-box", 108, 28)
s.text(x + 312, y + 119, "✗", "ml-neg")
s.both(x + 18, y + 160, "รอบ 1: κ 0.45 ✗", "Round 1: κ 0.45 ✗", "ml-neg")
s.both(x + 18, y + 186, "→ เพิ่มกฎในคู่มือ: ประชด = บ่น", "→ add a rule: sarcasm = complaint", "mp-chip")
s.both(x + 18, y + 216, "รอบ 2: κ 0.80 ✓", "Round 2: κ 0.80 ✓", "ml-ok")
s.both(x + 18, y + 240, "(200 อันใหม่ · ตอบตรงกัน 88%)", "(200 new comments · 88% the same)", "mp-c")
x = X1[2]
s.box(x + 18, y + 52, PW1 - 36, 34, "ml-cell-b", 8)
s.both(x + PW1 / 2, y + 74, "เฉลย 200 อัน = ชุด gold", "answer key of 200 = the gold set", "mp-chip", "middle")
s.arrow(x + 94, y + 88, x + 94, y + 104)
s.arrow(x + 256, y + 88, x + 256, y + 104)
s.box(x + 18, y + 108, 152, 134, "ml-cell", 10)
s.text(x + 30, y + 136, "dev 100", "pl-label")
s.both(x + 30, y + 163, "= แบบฝึกหัด", "= homework", "mp-chip")
s.both(x + 30, y + 190, "เปิดดูเฉลยได้", "you may look", "mp-c")
s.both(x + 30, y + 214, "ใช้ซ้อม LLM", "for LLM practice", "mp-c")
s.box(x + 180, y + 108, 152, 134, "sw-warn-box", 10)
emoji_or_icon(s, "🔒", x + 204, y + 130, 22)
s.text(x + 222, y + 136, "test 100", "pl-label")
s.both(x + 192, y + 163, "= ข้อสอบ", "= the exam", "mp-chip")
s.both(x + 192, y + 190, "ปิดไว้ ห้ามดู", "locked: no peeking", "mp-c")
s.both(x + 192, y + 214, "จนถึงตอนตรวจ", "until the check", "mp-c")
s.save("l15-case1-key.svg", PY1 + PH1 + 12)

# ---- picture 3, stage 2: the LLM practises on dev, then labels everything (steps 4-5)
s = Svg(W, "Stage 2: the LLM labels everything. 4 The LLM practises on dev and we fix the prompt: it calls 'The reviewer "
           "is so cute' praise, but the answer key says neutral (not about the shop); after that example is added to the "
           "prompt it answers neutral. 5 With the fixed prompt the LLM labels all 20,000 comments; test stays locked.")
s.bubble("ช่วงที่ 2: LLM ซ้อมกับ dev ก่อน แล้วติดป้ายทั้ง 20,000 อัน", "Stage 2: the LLM practises on dev, then labels all 20,000")
step_panel(10, 4, "LLM ซ้อมกับ dev แล้วเราแก้ prompt", "The LLM practises on dev; we fix the prompt", w=715)
step_panel(740, 5, "ติดป้ายทั้งหมด", "Label everything")
s.arrow(727, PY1 + PH1 / 2, 738, PY1 + PH1 / 2)
x, y = 10, PY1
CUTE = ("“พี่คนรีวิวน่ารักมาก 😍”", "“The reviewer is so cute 😍”")
for k in (0, 1):
    cx = x + 18 + k * 358
    s.box(cx, y + 52, 320, 190, "ml-cell" if k == 0 else "ml-cell-b", 10)
    if k == 0:
        s.both(cx + 14, y + 78, "prompt = คู่มือ + ตัวอย่าง", "prompt = guideline + examples", "mp-c")
        s.box(cx + 14, y + 90, 292, 32, "rc-ctx", 8)
        s.both(cx + 160, y + 112, *CUTE, "mp-chip", "middle")
        emoji_or_icon(s, "🤖", cx + 34, y + 154, 36)
        s.both(cx + 60, y + 161, "LLM: ชม ✗", "LLM: praise ✗", "ml-neg")
        s.both(cx + 14, y + 204, "เฉลย: เป็นกลาง (ไม่ได้พูดถึงร้าน)", "key: neutral (not about the shop)", "mp-c")
        s.both(cx + 14, y + 228, "LLM ใช้ความเข้าใจทั่วไปของมัน", "the LLM used its own general idea", "mp-s")
    else:
        s.both(cx + 14, y + 78, "เติมตัวอย่างนี้ลงใน prompt:", "add this example to the prompt:", "mp-c")
        s.box(cx + 14, y + 90, 292, 32, "rc-res", 8)
        s.both(cx + 160, y + 111, "ชมคนรีวิว ไม่ใช่ร้าน → เป็นกลาง", "praise for the reviewer → neutral", "mp-c", "middle")
        emoji_or_icon(s, "🤖", cx + 34, y + 154, 36)
        s.both(cx + 60, y + 161, "LLM: เป็นกลาง ✓", "LLM: neutral ✓", "ml-ok")
        s.both(cx + 14, y + 204, "ตรงกับเฉลยแล้ว", "now it matches the key", "mp-c")
        s.both(cx + 14, y + 228, "ทำซ้ำจนตอบ dev ได้ดี", "repeat until dev goes well", "mp-s")
s.arrow(x + 342, y + 147, x + 372, y + 147)
x = 740
emoji_or_icon(s, "🤖", x + PW1 / 2, y + 96, 76)
s.both(x + PW1 / 2, y + 168, "20,000 อัน", "20,000 comments", "mp-big", "middle")
s.both(x + PW1 / 2, y + 194, "ด้วย prompt ที่แก้แล้ว", "with the fixed prompt", "mp-chip", "middle")
emoji_or_icon(s, "🔒", x + 84, y + 226, 22)
s.both(x + 102, y + 232, "test ยังปิดอยู่", "test is still locked", "mp-c")
s.save("l15-case1-llm.svg", PY1 + PH1 + 12)

# ---- picture 4, stage 3: open test once, then count and report (steps 6-7)
s = Svg(W, "Stage 3: check, then count. 6 Open test once: of the 100 test comments the LLM's label matches the answer key "
           "on 87 and is wrong on 13; A and B agree with each other 88% of the time, so the LLM is about as good as one "
           "more person. 7 Count all 20,000 comments: 18% are complaints before the shop went viral and 41% after.")
s.bubble("ช่วงที่ 3: ใช้ test ตรวจ LLM แล้วค่อยนับ", "Stage 3: check the LLM on test, then count")
step_panel(10, 6, "เปิด test ครั้งเดียว", "Open test, once", w=530)
step_panel(555, 7, "นับทั้ง 20,000 อัน แล้วรายงาน", "Count all 20,000, then report", w=535)
s.arrow(542, PY1 + PH1 / 2, 553, PY1 + PH1 / 2)
x, y = 10, PY1
for n in range(100):
    circ(s, x + 34 + (n % 10) * 18, y + 66 + (n // 10) * 18, 6.5, OK if n < 87 else NO)
s.both(x + 226, y + 78, "ป้ายของ LLM เทียบกับเฉลย 100 อัน", "the LLM's labels vs the 100 answers", "mp-c")
s.both(x + 226, y + 122, "ตรงกัน 87", "87 match", "mp-big-ok")
s.both(x + 226, y + 152, "ผิด 13", "13 wrong", "ml-neg")
s.both(x + 226, y + 198, "A กับ B เองตอบตรงกัน 88%", "A and B agree on only 88%", "mp-chip")
s.both(x + 226, y + 228, "→ LLM ใกล้เคียงคน ใช้ได้", "→ close to a person: usable", "ml-ok")
x = 555
s.both(x + 24, y + 70, "คอมเมนต์ที่ได้ป้าย “บ่น”", "comments labelled “complaint”", "mp-c")
for k, (lth, len_, v) in enumerate([("ก่อนไวรัล", "before viral", 0.18), ("หลังไวรัล", "after viral", 0.41)]):
    by = y + 86 + k * 56
    s.both(x + 24, by + 27, lth, len_, "mp-chip")
    s.fill(x + 150, by + 4, 280 * v / 0.41, 34, NO, 6)
    s.text(x + 160 + 280 * v / 0.41, by + 28, f"{v:.0%}", "mp-n")
s.both(x + 24, y + 218, "บ่นเพิ่มขึ้นหลังไวรัล", "more complaints after going viral", "ml-neg")
s.both(x + 24, y + 242, "รายงานคู่กับ: ป้ายถูก 87 จาก 100", "report it with: labels right 87 in 100", "mp-c")
s.save("l15-case1-check.svg", PY1 + PH1 + 12)
