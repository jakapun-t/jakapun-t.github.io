"""Pictures for the L11 cards that were text only. Each sits above the card's text: a student can skim the picture
and read the text for the detail.
  l11-class-kinds.svg     S02  binary, multiclass, multilabel: what one row can get (scam SMS, a song, a video)
  l11-one-row.svg         S03  one row is one person (row 1 of obesity.csv), and the 108 people by weight group
  l11-accuracy-trap.svg   S11  10,000 days with 10 earthquakes: a model that always says "no" scores 99.9%, catches 0
  l11-scam-filter.svg     S14  the exercise's story drawn: spam folder 6 (5 scams, 1 real), inbox 4 (2 scams, 2 real)
  l11-key-terms.svg       S20  six key terms, each with a small drawing

    course/.venv/bin/python scripts/diagrams/stats_l11_cards.py courses/stats-dh/images

Real numbers: obesity.csv row 1 is ID 1, age 25, Male, 175 cm, 80 kg, BMI 25.3, Normal Weight; Label counts
Underweight 47, Normal Weight 29, Overweight 20, Obese 12. The earthquake and scam-filter numbers are the cards' own story
numbers. Uses the mp-*, ml-*, nt-*, rc-*, dg-* classes in templates/page.css.
"""

import math

from stats_svg import CLS, NAMES, Svg, circ, embed_png, emoji_or_icon, icon_label, person, poly, width

W = 1100


def chips_col(s, x, y, labels, lit, w=170):
    """A column of answer chips; the lit ones are the answers this row gets."""
    for i, (th, en) in enumerate(labels):
        yy = y + i * 38
        s.box(x, yy, w, 30, "ml-cell-b" if i in lit else "ml-cell", 15)
        s.both(x + 16, yy + 21, th, en, "mp-chip")
        if i in lit:
            s.text(x + w - 14, yy + 21, "✓", "ml-ok", "end")


# ================================================================ S02 binary, multiclass, multilabel
s = Svg(W, "Three kinds of classification, by what one row can get. Binary: a text message is scam or safe, exactly "
           "two answers. Multiclass: a song gets one genre out of K-pop, lo-fi, rock and jazz. Multilabel: a short video "
           "can get several hashtags at once (#dance and #funny here, not #pets or #food), or none.")
s.bubble("แถวหนึ่งได้คำตอบกี่แบบ", "How many answers can one row get?")
KINDS = [
    ("Binary: 2 กลุ่ม", "Binary: 2 classes", "📩", "ข้อความ SMS", "a text message", [("หลอกลวง", "scam"), ("ปลอดภัย", "safe")], {0},
     "ตอบได้ 2 แบบเท่านั้น (1 / 0)", "exactly 2 answers (1 / 0)"),
    ("Multiclass: หลายกลุ่ม", "Multiclass: many classes", "🎵", "เพลงหนึ่งเพลง", "a song",
     [("K-pop", "K-pop"), ("lo-fi", "lo-fi"), ("rock", "rock"), ("jazz", "jazz")], {0}, "เลือกได้กลุ่มเดียว", "exactly one of many"),
    ("Multilabel: หลายป้าย", "Multilabel: many labels", "📱", "คลิปสั้นหนึ่งคลิป", "a short video",
     [("#dance", "#dance"), ("#funny", "#funny"), ("#pets", "#pets"), ("#food", "#food")], {0, 1},
     "ได้ 0, 1 หรือหลายป้ายพร้อมกัน", "0, 1 or several at once"),
]
for k, (tth, ten, icon, oth, oen, labels, lit, cth, cen) in enumerate(KINDS):
    x = 10 + k * 365
    s.panel(x, 70, 350, 250, "ml-cell", tth, ten, k + 1)
    s.raw(f'<circle cx="{x + 68}" cy="{180}" r="36" style="fill:var(--tag-concept-bg)"/>')
    emoji_or_icon(s, icon, x + 68, 180, 56)
    s.both(x + 68, 238, oth, oen, "mp-s", "middle")
    s.arrow(x + 112, 180, x + 146, 180)
    chips_col(s, x + 158, 118 if len(labels) > 2 else 146, labels, lit)
    s.both(x + 175, 300, cth, cen, "hk-desc", "middle")
s.save("l11-class-kinds.svg", 330)


# ================================================================ S03 one row = one person
s = Svg(W, "Our data. Left: one row is one person. Row 1 of obesity.csv: age 25, male, 175 cm, 80 kg, BMI 25.3 are the "
           "features (what we know); Label, Normal Weight, is the answer to predict. Right: all 108 people, one icon each, "
           "by weight group: Underweight 47, Normal Weight 29, Overweight 20, Obese 12. The groups are not the same size.")
s.bubble("หนึ่งแถว = คนหนึ่งคน ทั้งหมด 108 คน", "One row = one person, 108 people in all")
s.panel(10, 70, 530, 280, "ml-cell", "แถวที่ 1 ของ obesity.csv", "Row 1 of obesity.csv", 1)
embed_png(s, "cast-normal-man.png", 22, 112, 140, 222)
FEATS = [("อายุ 25", "Age 25"), ("เพศ Male", "Gender Male"), ("สูง 175 ซม.", "Height 175 cm"),
         ("หนัก 80 กก.", "Weight 80 kg"), ("BMI 25.3", "BMI 25.3")]
s.both(260, 132, "feature: สิ่งที่รู้", "features: what we know", "mp-s", "middle")
for i, (th, en) in enumerate(FEATS):
    y = 142 + i * 40
    s.box(186, y, 148, 30, "nt-band-a", 15)
    s.both(260, y + 21, th, en, "mp-chip", "middle")
    s.line(150, 218, 184, y + 15, "mp-guide")
s.arrow(340, 232, 368, 232)
s.both(452, 200, "label: คำตอบ", "label: the answer", "mp-s", "middle")
s.box(376, 214, 154, 36, "rc-ctx", 18)
s.text(453, 238, "Normal Weight", "mp-chip", "middle")

s.panel(560, 70, 530, 280, "ml-cell", "คนทั้ง 108 คน แยกตามภาวะน้ำหนัก", "All 108 people, by weight group", 2)
COUNTS = [47, 29, 20, 12]
i = 0
for k, n in enumerate(COUNTS):
    for _ in range(n):
        person(s, 594 + (i % 18) * 26, 134 + (i // 18) * 34, CLS[k])
        i += 1
lx = 582
for k, ((th, en), n) in enumerate(zip(NAMES, COUNTS)):
    s.fill(lx, 322, 16, 16, CLS[k], 3)
    lth, len_ = f"{th} {n}", f"{en} {n}"
    s.both(lx + 22, 336, lth, len_, "mp-c")
    lx += 40 + max(width(lth, 14), width(len_, 14))
s.save("l11-one-row.svg", 360)


# ================================================================ S11 the accuracy trap
s = Svg(W, "Why accuracy is not enough. Left: 10,000 days drawn as 1,000 squares of 10 days; the one red square is the 10 "
           "days with a serious earthquake. Right: a lazy model answers 'no earthquake' every day. It is right on 9,990 of "
           "10,000 days, accuracy 99.9%, yet it catches 0 of the 10 earthquakes.")
s.bubble("โมเดลที่ตอบ “ไม่มี” ทุกวัน ถูก 99.9% แต่ช่วยอะไรได้ไหม", "A model that always says “no” is 99.9% right. Is it any use?")
s.panel(10, 70, 600, 290, "ml-cell", "10,000 วัน (1 ช่อง = 10 วัน)", "10,000 days (1 square = 10 days)", 1)
for r in range(20):
    for c in range(50):
        quake = (r, c) == (13, 37)
        s.fill(34 + c * 11, 114 + r * 11, 9, 9, "var(--accent)" if quake else "var(--card-border)", 1.5)
s.both(34, 346, "ช่องสีแดง = 10 วันที่มีแผ่นดินไหวรุนแรง", "red square = the 10 days with a serious earthquake", "mp-acc")
s.panel(630, 70, 460, 290, "ml-cell", "โมเดลขี้เกียจ", "The lazy model", 2)
emoji_or_icon(s, "😴", 676, 152, 84)
for i in range(3):
    s.box(716, 116 + i * 30, 170, 26, "nt-bubble", 13)
    s.both(801, 134 + i * 30, "“ไม่มีแผ่นดินไหว”", "“no earthquake”", "mp-c", "middle")
s.box(650, 222, 200, 120, "rc-res", 12)
s.both(750, 250, "accuracy", "accuracy", "mp-s", "middle")
s.text(750, 290, "99.9% ✓", "mp-big", "middle")
s.both(750, 324, "ถูก 9,990 จาก 10,000 วัน", "right on 9,990 of 10,000", "mp-s", "middle")
s.box(866, 222, 204, 120, "rc-con", 12)
s.both(968, 250, "จับแผ่นดินไหวได้", "earthquakes caught", "mp-s", "middle")
s.text(968, 290, "0 / 10 ✗", "mp-big", "middle")
s.both(968, 324, "ไม่เคยเตือนเลย", "never warns once", "mp-s", "middle")
s.save("l11-accuracy-trap.svg", 370)


# ================================================================ S14 the scam-DM filter (story only, no answer)
SCAM, REAL = "var(--accent)", "var(--tag-exercise-dot)"
INBOX = [("คุณได้รับ iPhone ฟรี! 🎁", "You won a free iPhone! 🎁", True), ("เย็นนี้ 1 ทุ่ม หมูกระทะนะ 🍜", "mookata at 7 tonight? 🍜", False),
         ("รายงานแล็บเสร็จยัง", "did u finish the lab report?", False), ("พัสดุค้าง จ่าย ฿49 ที่ลิงก์", "parcel held: pay ฿49 here", True)]
SPAM = [("ธนาคาร: ยืนยัน PIN ด่วน", "Bank: confirm your PIN now", True), ("รับ 5,000 coins ฟรี →", "free 5,000 coins →", True),
        ("คริปโต x10 ใน 1 วัน 🚀", "crypto x10 in 1 day 🚀", True), ("แม่: ว่างแล้วโทรหาแม่นะ 📞", "Mom: call me when free 📞", False),
        ("งานง่าย รายได้ดี DM มา 💸", "easy money, DM me 💸", True), ("รับรางวัลของคุณวันนี้", "claim your prize today", True)]


def phone(x, em, title_th, title_en, msgs):
    s.box(x, 70, 360, 330, "ml-model", 34)
    s.box(x + 12, 104, 336, 284, "ml-cell", 18)
    s.fill(x + 150, 82, 60, 8, "var(--card)", 4)
    icon_label(s, x + 30, 134, em, title_th, title_en, "mp-t", 26)
    for i, (th, en, scam) in enumerate(msgs):
        y = 148 + i * 39
        s.raw(f'<rect x="{x + 26}" y="{y}" width="308" height="32" rx="16" '
              f'style="fill:var(--card);stroke:{SCAM if scam else REAL};stroke-width:2.2"/>')
        s.raw(f'<circle cx="{x + 44}" cy="{y + 16}" r="7" style="fill:{SCAM if scam else REAL}"/>')
        s.both(x + 60, y + 21, th, en, "mp-c")


s = Svg(W, "The scam-DM filter. An AI filter should move scam messages to the spam folder (scam = positive). Left, the inbox: "
           "it left 4 messages there, 2 scams (red) and 2 real messages from friends (green). Right, the spam folder: it moved "
           "6 messages, 5 scams and 1 real message from Mom.")
s.bubble("AI กรอง DM ควรย้าย DM หลอกลวงไปโฟลเดอร์สแปม (หลอกลวง = positive)",
         "The AI filter should move scam DMs to spam (scam = positive)")
phone(150, "📥", "กล่องข้อความ (4)", "Inbox (4)", INBOX)
phone(590, "🗑", "โฟลเดอร์สแปม (6)", "Spam folder (6)", SPAM)
emoji_or_icon(s, "🤖", 550, 214, 96)
s.both(550, 278, "AI คัดแยก", "the AI sorts", "mp-s", "middle")
s.raw(f'<circle cx="430" cy="430" r="8" style="fill:{SCAM}"/>')
s.both(446, 436, "หลอกลวง (scam)", "scam", "mp-c")
s.raw(f'<circle cx="600" cy="430" r="8" style="fill:{REAL}"/>')
s.both(616, 436, "ข้อความจริงจากคนรู้จัก", "a real message", "mp-c")
s.save("l11-scam-filter.svg", 452)


# ================================================================ S20 key terms, each with a small drawing
s = Svg(W, "Six key terms with a picture each: the sigmoid squeezes any number into 0 to 1; the threshold is the cut-off "
           "(default 0.5); log loss punishes confident wrong answers; softmax turns K scores into probabilities that add to "
           "1; the confusion matrix counts TP, FN, FP, TN; precision reads the 'said yes' column (FP), recall reads the "
           "'really yes' row (FN).")


def d_sigmoid(x, y):
    poly(s, [(x + t * 3, y + 90 - 80 / (1 + math.exp(-(t - 20) / 4))) for t in range(41)], "mp-curve-b")
    s.line(x, y + 10, x + 120, y + 10, "mp-guide")
    s.line(x, y + 90, x + 120, y + 90, "mp-guide")


def d_threshold(x, y):
    s.line(x, y + 70, x + 120, y + 70, "mp-axis")
    for i, p in enumerate([0.1, 0.25, 0.4, 0.62, 0.8, 0.92]):
        circ(s, x + p * 120, y + 58, 6, "var(--accent)" if p >= 0.5 else "var(--muted)")
    s.line(x + 60, y + 20, x + 60, y + 84, "mp-straight")
    s.text(x + 60, y + 100, "0.5", "mp-s", "middle")


def d_logloss(x, y):
    poly(s, [(x + 6 + p * 110, y + 90 + 18 * math.log(p)) for p in [i / 40 for i in range(2, 41)]], "mp-curve")
    s.line(x, y + 90, x + 120, y + 90, "mp-axis")
    s.both(x + 10, y + 8, "มั่นใจแต่ผิด", "sure but wrong", "mp-s")


def d_softmax(x, y):
    for k, p in enumerate([0.08, 0.17, 0.25, 0.5]):
        s.fill(x + 6 + k * 29, y + 90 - p * 150, 22, p * 150, CLS[k], 3)
    s.both(x + 6, y + 10, "รวม = 1", "sum = 1", "mp-s")


def d_matrix(x, y, hi=None):
    cells = [("TP", 0, 0), ("FN", 1, 0), ("FP", 0, 1), ("TN", 1, 1)]
    for lab, c, r in cells:
        cls = "ml-cell"
        if hi == "both" and lab == "TP":
            cls = "ml-cell-b"
        elif hi == "both" and lab in ("FP", "FN"):
            cls = "rc-con"
        s.box(x + 10 + c * 52, y + 8 + r * 44, 48, 40, cls, 5)
        s.text(x + 34 + c * 52, y + 34 + r * 44, lab, "mp-n", "middle")


TERMS = [
    ("Sigmoid", d_sigmoid, "บีบตัวเลขใด ๆ\nให้อยู่ระหว่าง 0 ถึง 1", "squeezes any number\ninto 0 to 1"),
    ("Threshold", d_threshold, "จุดตัดความน่าจะเป็น\nค่าตั้งต้น 0.5 เลื่อนได้", "the probability cut-off;\ndefault 0.5, can move"),
    ("Log loss", d_logloss, "ลงโทษหนัก\nเมื่อมั่นใจแต่ผิด", "punishes confident\nwrong answers hardest"),
    ("Softmax", d_softmax, "คะแนน K กลุ่ม\n→ ความน่าจะเป็นรวม 1", "K class scores →\nprobabilities adding to 1"),
    ("Confusion matrix", lambda x, y: d_matrix(x, y), "นับว่าถูกและผิด\nแบบไหน", "counts how the model\nis right and wrong"),
    ("Precision / recall", lambda x, y: d_matrix(x, y, "both"), "precision ดู FP\nrecall ดู FN", "precision watches FP,\nrecall watches FN"),
]
for k, (name, draw, th, en) in enumerate(TERMS):
    x, y = 10 + (k % 3) * 365, 10 + (k // 3) * 162
    s.box(x, y, 350, 150, "ml-cell", 14)
    s.box(x + 12, y + 14, 132, 122, "dg-xl-head", 10)
    draw(x + 18, y + 20)
    s.text(x + 160, y + 46, name, "mp-t")
    ths, ens = th.split("\n"), en.split("\n")
    for i in range(2):
        s.both(x + 160, y + 82 + i * 26, ths[i], ens[i], "hk-desc")
s.save("l11-key-terms.svg", 334)


# ================================================================ S11 what accuracy is, on the weight model's 33 test people
# The 4-group model's test predictions (70/30 split, random_state=42): 27 right; wrong: 1 Underweight called Normal,
# 5 Overweight called Normal. People drawn in their real group's colour, grouped by real group.
s = Svg(W, "What accuracy is. The weight model guesses the group of 33 test people. Each person is drawn in the colour of "
           "their real group; a green tick under a person means the guess was right, a red cross means wrong. 27 are right "
           "and 6 are wrong (1 Underweight and 5 Overweight people were called Normal). Accuracy = right ÷ all = 27 ÷ 33 = 0.82.")
s.bubble("accuracy คืออะไร: ทายถูกกี่คนจากทั้งหมด", "What is accuracy? How many guesses are right, out of all")
GROUPS = [(0, 13, 1), (1, 6, 0), (2, 9, 5), (3, 5, 0)]     # (group, people, wrong)
x = 40
for k, n, wrong in GROUPS:
    s.both(x, 96, NAMES[k][0], NAMES[k][1], "mp-c")
    for i in range(n):
        px = x + 12 + i * 26
        person(s, px, 130, CLS[k])
        bad = i >= n - wrong
        s.text(px, 172, "✗" if bad else "✓", "ml-neg" if bad else "ml-ok", "middle")
    x += n * 26 + 34
s.box(40, 200, 1020, 120, "nt-band-a", 14)
s.both(70, 240, "accuracy = ทายถูก ÷ ทั้งหมด", "accuracy = right guesses ÷ all guesses", "mp-t")
s.text(70, 296, "= 27 ÷ 33 = 0.82", "mp-big")
s.both(1040, 240, "ถูก 27 ✓ · ผิด 6 ✗", "27 right ✓ · 6 wrong ✗", "mp-t", "end")
s.both(1040, 296, "ผิด 6 คนถูกทายว่า “ปกติ” ทั้งหมด", "all 6 wrong ones were called “Normal”", "mp-s", "end")
s.save("l11-accuracy-def.svg", 334)
