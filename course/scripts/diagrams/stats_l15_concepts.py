"""Concept pictures for stats-dh lesson 15 (data reliability and annotation agreement), in the style
of nlp l13-why-chunk.svg. ไทย/EN labels follow the language switch.

    course/.venv/bin/python scripts/diagrams/stats_l15_concepts.py courses/stats-dh/images

Numbers come from the lesson's practice data (scripts/diagrams/l15_practice_data.py: three research assistants label the
same 100 invented letters, 1840–1890, for emotion and formality), computed in course/.venv:
  Pilot 1: letters 1–8, emotion by RA A / B: Anxiety/Anxiety, Neutral/Neutral, Anxiety/Sadness, Anxiety/Sadness,
      Neutral/Anxiety, Neutral/Neutral, Anxiety/Anxiety, Anxiety/Anxiety; letter 3 formality A 1, B 9, C 8.
      A and B agree on 58 of 100 emotions; Cohen's kappa 0.42; Krippendorff's alpha (3 RAs) 0.375; formality ICC 0.418.
      "Anxiety or not", A vs B: both yes 17, A yes B no 10, A no B yes 18, both no 55: p_o 0.72, p_e 0.569, kappa 0.35.
  Pilot 2 (revised guidelines, 100 new letters): emotion alpha 0.684, formality ICC 0.807.
  Case-study loop picture: a made-up TikTok comments project, pilot 1 kappa 0.45 (64/100), pilot 2 kappa 0.80 (88/100).
"""

from stats_svg import Svg, W, math, width  # noqa: F401

EMO_COL = {"Anxiety": "var(--accent)", "Sadness": "var(--tag-concept-dot)", "Neutral": "var(--muted)", "Joy": "var(--tag-exercise-dot)"}
EMO_TH = {"Anxiety": "กังวล", "Sadness": "เศร้า", "Neutral": "เป็นกลาง", "Joy": "ยินดี"}


# ================================================================ L14 hook: two assistants, the same eight letters
LETTERS = [(1, "Anxiety", "Anxiety"), (2, "Neutral", "Neutral"), (3, "Anxiety", "Sadness"), (4, "Anxiety", "Sadness"),
           (5, "Neutral", "Anxiety"), (6, "Neutral", "Neutral"), (7, "Anxiety", "Anxiety"), (8, "Anxiety", "Anxiety")]
s = Svg(W, "Garbage in, garbage out. Two research assistants, A and B, label the same 8 letters for emotion. They agree on "
           "5 and disagree on 3 (letter 3: Anxiety vs Sadness; letter 4: Anxiety vs Sadness; letter 5: Neutral vs "
           "Anxiety). For letter 3 their formality scores are 1 and 9. Over all 100 letters they agree on only 58 "
           "emotions. A model or a chart built on these labels inherits the disagreement.")
s.bubble("ผู้ช่วยวิจัยสองคนอ่านจดหมายฉบับเดียวกัน ติดป้ายอารมณ์เหมือนกันไหม", "Two research assistants read the same letters: do they give the same emotion?")
s.box(20, 70, 1140, 330, "nt-band-a", 14)
s.both(40, 104, "จดหมาย", "letter", "pl-note")
s.both(40, 207, "ผู้ช่วย A", "RA A", "pl-label")   # middle of A's tag row (180–220)
s.both(40, 287, "ผู้ช่วย B", "RA B", "pl-label")   # middle of B's tag row (260–300)
for k, (lid, a, b) in enumerate(LETTERS):
    x = 170 + k * 124
    s.raw(f'<path d="M{x} 116 h86 l14 14 v34 h-100 Z" class="ml-cell"/>')   # a small sheet of paper
    for yy in (130, 140, 150):
        s.raw(f'<path d="M{x + 12} {yy} h60" class="dg-rule"/>')
    s.text(x + 50, 104, f"#{lid}", "pl-note", "middle")
    for row, lab in ((0, a), (1, b)):
        y = 180 + row * 80
        s.box(x - 4, y, 108, 40, "ml-cell", 20)
        s.raw(f'<circle cx="{x + 14}" cy="{y + 20}" r="8" style="fill:{EMO_COL[lab]}"/>')
        s.both(x + 28, y + 26, EMO_TH[lab], lab, "pl-note")
    if a != b:
        s.raw(f'<rect x="{x - 10}" y="172" width="120" height="156" rx="12" fill="none" class="pl-line" stroke-dasharray="6 5"/>')
        s.both(x + 50, 350, "✗ ไม่ตรงกัน", "✗ disagree", "ml-neg", "middle")
    else:
        s.both(x + 50, 350, "✓", "✓", "ml-ok", "middle")
s.both(40, 386, "จดหมาย #3: ความเป็นทางการ A ให้ 1 แต่ B ให้ 9 (จาก 1–10)", "Letter #3: formality A says 1, B says 9 (out of 1–10)", "pl-text")
s.box(20, 424, 1140, 92, "sw-warn-box", 14)
s.both(40, 458, "✗ จดหมายทั้ง 100 ฉบับ: A กับ B ติดป้ายอารมณ์ตรงกันแค่ 58 ฉบับ", "✗ All 100 letters: A and B give the same emotion for only 58", "ml-neg")
s.both(40, 494, "Garbage In, Garbage Out: โมเดลหรือกราฟ “อารมณ์ตลอด 50 ปี” ที่สร้างจากป้ายนี้ ได้ความไม่ตรงกันนี้ติดไปด้วย", "Garbage In, Garbage Out: a model or an “emotion over 50 years” chart built on these labels inherits this", "pl-text")
s.save("l15-hook.svg", 534)

# ================================================================ L14 reliability vs validity: four targets
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


# 6 annotators read one headline each and answer fake or real; reliable = the 6 answers agree, valid = they match the
# truth. One made-up headline per case.
CASES = [  # title th/en, headline th/en, truth (F/R), the 6 answers, reliable?, valid?, why th/en
    ("reliable และ valid", "Reliable and valid", "ดื่มน้ำมะนาวทุกเช้า รักษามะเร็งได้ 100%",
     "Lemon water every morning cures cancer 100%", "F", "FFFFFF", True, True,
     "✓ เป้าหมาย: ตรงกัน และถูก", "✓ The goal: they agree, and they're right"),
    ("reliable แต่ไม่ valid", "Reliable, not valid", "นายกฯ โกรธจัด! ตอกกลับสื่อกลางสภา",
     "PM furious! Hits back at the press in parliament", "R", "FFFFFF", True, False,
     "✗ ทุกคนตัดสินจาก น้ำเสียงโกรธ ไม่ใช่ความจริง", "✗ All judge the angry tone, not the facts"),
    ("valid แต่ไม่ reliable", "Valid, not reliable", "ผลวิจัย: กาแฟวันละ 5 แก้ว อายุยืนขึ้น 10 ปี",
     "Study: 5 coffees a day add 10 years to your life", "F", "FFRFRF", False, True,
     "✗ เสียงข้างมากถูก แต่คนละคนคนละแบบ", "✗ The majority is right, but people split"),
    ("ไม่ reliable ไม่ valid", "Neither", "ร้านดังปิดตัวกะทันหัน ลูกค้าโกรธจัด!",
     "Famous shop closes suddenly, customers furious!", "R", "FRFFRF", False, False,
     "✗ คนละคนคนละแบบ และเสียงข้างมากก็ผิด", "✗ People split, and the majority is wrong"),
]
LAB = {"F": ("ปลอม", "fake"), "R": ("จริง", "real")}
s = Svg(W, "Six annotators read the same made-up headline and answer fake or real. Reliable means the 6 answers agree; valid "
           "means they match the truth. 1 Reliable and valid: 'Lemon water cures cancer 100%' is fake, all 6 say fake. 2 "
           "Reliable, not valid: 'PM furious! Hits back at the press' is real, all 6 say fake because of the angry tone. "
           "3 Valid, not reliable: 'Study: 5 coffees a day add 10 years' is fake, 4 say fake and 2 real. 4 Neither: "
           "'Famous shop closes suddenly, customers furious!' is real, 4 say fake and 2 real.")
s.bubble("ผู้ติดป้าย 6 คนอ่านพาดหัวเดียวกัน แล้วตอบว่า “ข่าวปลอม” หรือ “ข่าวจริง”",
         "Six annotators read the same headline and answer “fake” or “real”")
PW, CHW, CHH = 272, 76, 36
for i, (th, en, hth, hen, truth, answers, rel, val, wth, wen) in enumerate(CASES):
    x0 = 20 + i * (PW + 17)
    good = rel and val
    s.box(x0, 70, PW, 470, "nt-band-a" if good else "sw-warn-box", 14)
    s.badge(x0 + 30, 96, i + 1)
    s.both(x0 + 50, 102, th, en, "pl-label")
    # the headline
    s.box(x0 + 14, 120, PW - 28, 80, "ml-cell", 8)
    a_, b_ = wrap("“" + hth + "”", PW - 52, 15 * 1.15), wrap("“" + hen + "”", PW - 52, 15 * 1.15)
    for k in range(max(len(a_), len(b_))):
        s.both(x0 + 26, 144 + k * 22, a_[k] if k < len(a_) else "", b_[k] if k < len(b_) else "", "mp-p")
    s.both(x0 + 20, 228, f"ความจริง: ข่าว{LAB[truth][0]}", f"Truth: {LAB[truth][1]}", "pl-label")
    # the 6 answers, ✓ when it matches the truth
    s.both(x0 + 20, 258, "คำตอบของ 6 คน:", "The 6 answers:", "pl-note")
    for k, ans in enumerate(answers):
        cx = x0 + 18 + (k % 3) * (CHW + 8)
        cy = 270 + (k // 3) * (CHH + 8)
        right = ans == truth
        s.box(cx, cy, CHW, CHH, "ml-cell", 6)
        s.both(cx + CHW / 2, cy + 25, ("✓ " if right else "✗ ") + LAB[ans][0], ("✓ " if right else "✗ ") + LAB[ans][1],
               "ml-ok" if right else "ml-neg", "middle")
    # the two checks
    nf = answers.count("F")
    split_th = f"ปลอม {nf} · จริง {6 - nf}"
    split_en = f"fake {nf} · real {6 - nf}"
    s.line(x0 + 16, 364, x0 + PW - 16, 364, "mp-guide")
    s.both(x0 + 20, 392, ("✓" if rel else "✗") + " reliable: " + ("ตอบเหมือนกันทั้ง 6" if rel else split_th),
           ("✓" if rel else "✗") + " reliable: " + ("all 6 the same" if rel else split_en), "ml-ok" if rel else "ml-neg")
    s.both(x0 + 20, 422, ("✓" if val else "✗") + " valid: " + ("ตรงกับความจริง" if val else "ผิดจากความจริง"),
           ("✓" if val else "✗") + " valid: " + ("matches the truth" if val else "misses the truth"), "ml-ok" if val else "ml-neg")
    va, vb = wrap(wth, PW - 40, 16 * 1.2), wrap(wen, PW - 40, 16 * 1.2)
    for k in range(max(len(va), len(vb))):
        s.both(x0 + 20, 466 + k * 26, va[k] if k < len(va) else "", vb[k] if k < len(vb) else "", "pl-note")
s.both(20, 574, "reliable = ทุกคนให้ป้ายเหมือนกันไหม · valid = ป้ายตรงกับสิ่งที่ตั้งใจวัด (ความจริง) ไหม · พาดหัวเป็นตัวอย่างสมมติ",
       "reliable = do the annotators give the same label? · valid = does the label match what we mean to measure? · made-up headlines",
       "pl-label")
s.save("l15-validity.svg", 594)

# ================================================================ L14 bad vs good guideline on four sentences
SENT = [  # sentence, bad guideline: rater 1, rater 2; good guideline: rater 1, rater 2
    ("“I love this!”", "Positive", "Positive", "Positive", "Positive"),
    ("“Oh, just great... my car broke down.”", "Positive", "Negative", "Negative", "Negative"),
    ("“It wasn't bad.”", "Positive", "Negative", "Neutral", "Neutral"),
    ("“She said she was very happy.”", "Positive", "Neutral", "Neutral", "Neutral"),
]
s = Svg(W, "The same 4 sentences under two guidelines. Bad guideline ('Positive: the text has a good or happy feeling'): "
           "raters split on sarcasm ('Oh, just great... my car broke down'), on negation ('It wasn't bad') and on "
           "reported feelings ('She said she was very happy'), agreeing on 1 of 4. Good guideline (a clear definition plus rules for "
           "sarcasm, weak praise and reported sentiment): every rater gives Positive, Negative, Neutral, Neutral.")
s.bubble("คู่มือสองแบบ ประโยคเดียวกัน 4 ประโยค ผู้ติดป้ายสองคนตอบตรงกันไหม", "Two guidelines, the same 4 sentences: do two raters agree?")
GUIDE = [  # what each guideline actually says, line by line: (th, en, css class)
    [("Positive = ข้อความรู้สึกดีหรือมีความสุข", "Positive = the text has a good or happy feeling", "pl-text"),
     ("(แค่นี้ ไม่มีนิยามอื่น ไม่มีกฎกรณีขอบ)", "(that's all: no other definitions, no edge-case rules)", "pl-note")],
    [("นิยาม: Positive = ผู้เขียนพอใจหรือยินดีชัดเจน", "Definition: Positive = the author is clearly pleased", "pl-text"),
     ("และเป็นความรู้สึกของผู้เขียนเอง", "and the feeling is the author's own", "pl-text"),
     ("กฎ 1: ประชด → Negative (ใช้กับประโยค 2)", "Rule 1: sarcasm → Negative (sentence 2)", "pl-note"),
     ("กฎ 2: ชมแบบจืด “ไม่เลว” → Neutral (ประโยค 3)", "Rule 2: weak praise “not bad” → Neutral (sentence 3)", "pl-note"),
     ("กฎ 3: เล่าความรู้สึกคนอื่น → Neutral (ประโยค 4)", "Rule 3: someone else's feeling → Neutral (sentence 4)", "pl-note")],
]
for i, (cls, th, en) in enumerate([("sw-warn-box", "✗ คู่มือที่ไม่ดี", "✗ A bad guideline"),
                                   ("nt-band-a", "✓ คู่มือที่ดี", "✓ A good guideline")]):
    x0 = 20 + i * 580
    s.box(x0, 70, 560, 556, cls, 14)
    s.both(x0 + 20, 104, th, en, "pl-label")
    s.box(x0 + 16, 118, 528, 168, "ml-cell", 10)                  # the guideline page itself
    s.both(x0 + 32, 140, "คู่มือเขียนว่า:", "The guideline says:", "mp-s")
    for k, (gth, gen, gcls) in enumerate(GUIDE[i]):
        s.both(x0 + 32, 170 + k * 27, gth, gen, gcls)
    s.both(x0 + 300, 314, "ผู้ติดป้าย 1", "rater 1", "pl-note", "middle")
    s.both(x0 + 440, 314, "ผู้ติดป้าย 2", "rater 2", "pl-note", "middle")
    for k, (sent, b1, b2, g1, g2) in enumerate(SENT):
        y = 326 + k * 64
        r1, r2 = (b1, b2) if i == 0 else (g1, g2)
        sent = f"{k + 1}. {sent}"
        if width(sent, 18) < 225:
            s.text(x0 + 20, y + 26, sent, "pl-note")
        else:                                   # two lines, split at the space nearest the middle
            cut = min((j for j, ch in enumerate(sent) if ch == " "), key=lambda j: abs(j - len(sent) / 2))
            s.text(x0 + 20, y + 16, sent[:cut], "pl-note")
            s.text(x0 + 34, y + 38, sent[cut + 1:], "pl-note")
        for j, lab in enumerate((r1, r2)):
            bx = x0 + 250 + j * 140
            s.box(bx, y + 4, 100, 34, "ml-cell" if r1 == r2 else "rc-ctx", 17)
            s.text(bx + 50, y + 27, lab, "pl-note", "middle")
        s.text(x0 + 540, y + 27, "✓" if r1 == r2 else "✗", "ml-ok" if r1 == r2 else "ml-neg", "end")
    agree = sum((b1 == b2) if i == 0 else (g1 == g2) for (_, b1, b2, g1, g2) in SENT)
    s.both(x0 + 20, 606, f"ตรงกัน {agree} จาก 4 ประโยค", f"agree on {agree} of 4 sentences", "ml-neg" if i == 0 else "ml-ok")
s.both(20, 662, "ประโยค 2 ประชด · 3 ปฏิเสธซ้อน (ชมแบบจืด) · 4 เล่าความรู้สึกของคนอื่น ไม่ใช่ของผู้เขียน",
       "Sentence 2 is sarcasm · 3 is weak praise · 4 reports someone else's feeling, not the author's", "pl-note")
s.both(20, 688, "คู่มือที่ไม่ดีไม่บอกว่าสามแบบนี้ต้องทำอย่างไร ผู้ติดป้ายจึงเดาคนละแบบ คู่มือที่ดีมีกฎ 1–3 ตอบไว้แล้ว",
       "The bad guideline says nothing about these three, so raters guess differently; the good one answers them with rules 1–3", "pl-note")
s.save("l15-guideline.svg", 706)

# ================================================================ L14 Cohen's kappa worked on "Anxiety or not"
s = Svg(W, "Cohen's kappa for 'Anxiety or not', RA A vs RA B on the 100 pilot letters. The table: both yes 17, A yes and B "
           "no 10, A no and B yes 18, both no 55. Observed agreement p_o = (17 + 55) / 100 = 0.72. A says yes 27%, B "
           "says yes 35%, so chance agreement p_e = 0.27 × 0.35 + 0.73 × 0.65 = 0.569. Above chance they got 0.72 − 0.569 = "
           "0.151 out of a possible 1 − 0.569 = 0.431, so kappa = 0.151 / 0.431 = 0.35: only fair agreement, though they "
           "agree 72% of the time.")
s.bubble("A กับ B ตอบตรงกันว่า “กังวลหรือไม่” 72% ดีพอไหม คิด kappa ทีละขั้น",
         "A and B agree on “Anxiety or not” 72% of the time: is that good? Kappa step by step")
GREEN, CHANCE = "var(--tag-exercise-dot)", "var(--accent)"
# 1 the table, with totals
s.panel(20, 70, 570, 296, "nt-band-a", "นับใส่ตาราง พร้อมผลรวม", "Count into a table, with totals", 1)
TX, TY, CW_, CH_ = 210, 124, 108, 54
for j, (th, en) in enumerate([("B: yes", "B: yes"), ("B: no", "B: no"), ("รวม", "total")]):
    s.both(TX + j * (CW_ + 8) + CW_ / 2, TY + 18, th, en, "pl-note", "middle")
CELLS = [[(17, "agree"), (10, ""), (27, "tot")], [(18, ""), (55, "agree"), (73, "tot")], [(35, "tot"), (65, "tot"), (100, "tot")]]
NOTE = {(0, 2): "17 + 10", (1, 2): "18 + 55", (2, 0): "17 + 18", (2, 1): "10 + 55"}
for i, (th, en) in enumerate([("A: yes", "A: yes"), ("A: no", "A: no"), ("รวม", "total")]):
    y = TY + 28 + i * (CH_ + 6)
    s.both(TX - 16, y + 30, th, en, "pl-note", "end")
    for j, (v, kind) in enumerate(CELLS[i]):
        x = TX + j * (CW_ + 8)
        s.box(x, y, CW_, CH_, "rc-res" if kind == "agree" else ("rc-ctx" if kind == "tot" else "ml-cell"), 8)
        s.text(x + CW_ / 2, y + (25 if (i, j) in NOTE else 34), str(v), "pl-label", "middle")
        if (i, j) in NOTE:
            s.text(x + CW_ / 2, y + 46, NOTE[(i, j)], "mp-s", "middle")
s.both(40, 350, "สีเขียว = ตอบเหมือนกัน · สีเหลือง = ผลรวม",
       "green = same answer · yellow = totals", "pl-note")
# 2 observed agreement
s.panel(610, 70, 550, 296, "nt-band-a", "ตรงกันจริง (pₒ)", "Observed agreement (pₒ)", 2)
s.both(630, 140, "นับช่องเขียว: ตอบ yes ทั้งคู่ + ตอบ no ทั้งคู่", "Count the green cells: both yes + both no", "pl-note")
s.text(630, 186, "17 + 55 = 72", "pl-text")
s.text(630, 236, "pₒ = 72 / 100 = 0.72", "mp-big")
s.both(630, 330, "ฟังดูดี แต่ส่วนหนึ่งอาจตรงกันเพราะบังเอิญ", "Sounds good, but some of it may be luck", "pl-note")
# 3 chance agreement
s.panel(20, 380, 570, 300, "sw-warn-box", "ตรงกันเพราะบังเอิญ (pₑ)", "Agreement by chance (pₑ)", 3)
s.both(40, 446, "ถ้าทั้งคู่เดาสุ่มตามสัดส่วนของตัวเอง (ไม่อ่านจดหมายเลย)",
       "If both guessed at their own rates (without reading)", "pl-note")
CH = [("A ตอบ yes: 27 / 100 = 0.27 · B ตอบ yes: 35 / 100 = 0.35", "A says yes: 27 / 100 = 0.27 · B says yes: 35 / 100 = 0.35", "mp-p"),
      ("yes ทั้งคู่โดยบังเอิญ: 0.27 × 0.35 = 0.095", "both yes by chance: 0.27 × 0.35 = 0.095", "pl-text"),
      ("A ตอบ no: 0.73 · B ตอบ no: 0.65", "A says no: 0.73 · B says no: 0.65", "mp-p"),
      ("no ทั้งคู่โดยบังเอิญ: 0.73 × 0.65 = 0.475", "both no by chance: 0.73 × 0.65 = 0.475", "pl-text")]
for k, (th, en, cls) in enumerate(CH):
    s.both(40, 486 + k * 34, th, en, cls)
s.text(40, 642, "pₑ = 0.095 + 0.475 = 0.569", "mp-big")
s.both(570, 642, "57% ได้มาฟรี", "57% comes free", "ml-neg", "end")
# 4 kappa: how much of the room above chance they actually got
s.panel(610, 380, 550, 300, "nt-band-a", "kappa: ได้เกินบังเอิญกี่ส่วน", "Kappa: how much beyond chance", 4)
B0, B1, BY = 640, 1130, 462
xs = lambda v: B0 + v * (B1 - B0)
s.fill(xs(0), BY, xs(0.569) - xs(0), 30, CHANCE, 4)
s.raw(f'<rect x="{xs(0.569):g}" y="{BY}" width="{xs(1) - xs(0.569):g}" height="30" rx="4" class="ml-cell"/>')
s.fill(xs(0.569), BY, xs(0.72) - xs(0.569), 30, GREEN, 0)
for v in (0, 0.569, 0.72, 1):
    s.text(xs(v), BY + 50, f"{v:g}", "mp-s", "middle")
s.raw(f'<text x="{(xs(0) + xs(0.569)) / 2:g}" y="{BY + 21}" class="mp-chip" text-anchor="middle" style="fill:#fff" data-only="th">บังเอิญ</text>')
s.raw(f'<text x="{(xs(0) + xs(0.569)) / 2:g}" y="{BY + 21}" class="mp-chip" text-anchor="middle" style="fill:#fff" data-only="en" lang="en">chance</text>')
s.raw(f'<path d="M{xs(0.569):g} {BY - 8} v-8 H{xs(1):g} v8" class="mp-axis"/>')
s.both(xs(1), BY - 24, "เกินบังเอิญได้สูงสุด: 1 − 0.569 = 0.431", "most above chance: 1 − 0.569 = 0.431",
       "mp-s", "end")
s.both(630, BY + 92, "ได้เกินบังเอิญจริง (สีเขียว): 0.72 − 0.569 = 0.151", "actually above chance (green): 0.72 − 0.569 = 0.151",
       "pl-text")
s.text(630, BY + 140, "κ = 0.151 / 0.431 = 0.35", "mp-big")
s.both(630, BY + 180, "✗ ได้แค่ 35% ของที่เป็นไปได้: fair ต้องแก้คู่มือ", "✗ only 35% of what was possible: fair, fix the guidelines",
       "ml-neg")
s.save("l15-kappa.svg", 698)

# ================================================================ L14 three ways to scale up
s = Svg(W, "Three ways to label 20,000 letters when people can label only a few hundred. 1 Weak supervision: experts write "
           "labelling rules that vote, and a model weighs the rules into probabilistic labels. 2 LLM as a first pass: a "
           "language model labels every letter with your guideline in the prompt; people review and correct. 3 Active "
           "learning: a model trained on a small seed set asks people to label only the letters it is least sure about.")
s.bubble("คนติดป้ายได้ไม่กี่ร้อยฉบับ แต่มีจดหมาย 20,000 ฉบับ จะทำอย่างไร", "People can label a few hundred letters, but there are 20,000: what now?")
PW = 364
SC = [
    ("Weak supervision", "เขียนกฎแทนการคลิกทีละฉบับ", "Write rules instead of clicking each letter",
     ["LF1: “cry” → SAD", "LF2: “heartbroken” → SAD", "LF3: “happy” → NOT_SAD", "LF4: has “I” → NOT_SAD ✗"],
     "โมเดลชั่งน้ำหนักกฎ → P(SAD) = 0.85", "weighted rules → P(SAD) = 0.85"),
    ("LLM first pass", "ให้ LLM ติดป้ายตามคู่มือ แล้วคนตรวจ", "An LLM labels, people check",
     ["prompt = นิยาม + ตัวอย่าง 3–5 ข้อ", "ให้คิดทีละขั้น (CoT)", "ตอบเป็น JSON 1 บรรทัด", "คนตรวจแก้ เร็วกว่าเริ่มเอง 5–10 เท่า"],
     "เช็กกับชุด gold ที่คนติดไว้เสมอ", "always check against a human gold set"),
    ("Active learning", "ให้โมเดลถามเฉพาะฉบับที่ไม่แน่ใจ", "The model asks about unsure letters",
     ["ติดป้ายชุดเริ่ม 100 ฉบับ", "ฝึกโมเดล แล้วให้คะแนนทุกฉบับ", "ส่ง 100 ฉบับที่ไม่แน่ใจที่สุดให้คน", "เพิ่มป้าย ฝึกใหม่ ทำซ้ำ"],
     "P(SAD) 0.51 กับ 0.49 → ส่งให้คน", "P(SAD) 0.51 vs 0.49 → ask a person"),
]
SC_EN = [
    ["LF1: “cry” → SAD", "LF2: “heartbroken” → SAD", "LF3: “happy” → NOT_SAD", "LF4: has “I” → NOT_SAD ✗"],
    ["prompt = definition + 3–5 examples", "think step by step (CoT)", "answer as one line of JSON", "people correct: 5–10× faster"],
    ["label a seed set of 100", "train, then score every letter", "send the 100 least sure to people", "add labels, retrain, repeat"],
]
for i, (name, th, en, items_th, rth, ren) in enumerate(SC):
    x0 = 20 + i * (PW + 24)
    s.box(x0, 70, PW, 400, "nt-band-a", 14)
    s.badge(x0 + 32, 96, i + 1)
    s.text(x0 + 54, 102, name, "pl-label")
    s.both(x0 + 20, 140, th, en, "pl-note")
    for k, (it_th, it_en) in enumerate(zip(items_th, SC_EN[i])):
        y = 172 + k * 54
        s.box(x0 + 20, y, PW - 40, 40, "ml-cell", 10)
        s.both(x0 + 34, y + 26, it_th, it_en, "pl-note" if "✗" not in it_en else "ml-neg")
        if k < 3 and i == 2:
            s.arrow(x0 + PW / 2, y + 40, x0 + PW / 2, y + 54)
    if i == 2:
        s.raw(f'<path d="M{x0 + PW - 22} {172 + 3 * 54 + 20} C{x0 + PW + 2} {300} {x0 + PW + 2} {250} {x0 + PW - 22} {172 + 54 + 20}" class="pl-line" fill="none"/>')
    s.both(x0 + 20, 436, rth, ren, "ml-ok")
s.both(20, 508, "ทั้งสามวิธีต้องมีชุด gold ที่คนติดป้ายอย่างดี (คู่มือชัด + IRR สูง) เพื่อควบคุมและตรวจผล",
       "All three need a gold set labelled well by people (clear guidelines + high IRR) to steer and check the result", "pl-label")
s.save("l15-scaling.svg", 526)

# ================================================================ L14 the quality loop with the case-study numbers
s = Svg(W, "The data-quality loop on a made-up TikTok project: two friends label comments under a viral shop's videos as "
           "praise, complaint or neutral. Refine the guidelines, measure agreement, scale up, audit, and refine again. "
           "Pilot 1 with the first guidelines: they agree on 64 of 100 comments, kappa 0.45 (moderate), too low. After "
           "rules for sarcasm, '555' and off-topic comments, pilot 2 on 100 new comments: 88 of 100, kappa 0.80 "
           "(substantial), so labelling could go ahead.")
s.bubble("ค่าความตรงกันต่ำไม่ใช่ความล้มเหลว แต่เป็นสัญญาณให้แก้คู่มือ", "A low agreement score is not a failure: it tells you to fix the guidelines")
STEPS = [("1 แก้คู่มือ", "1 Refine", "นิยาม + ตัวอย่างหลัก", "definitions + anchors"),
         ("2 วัดผล", "2 Measure", "κ, α, ICC", "κ, α, ICC"),
         ("3 ขยาย", "3 Scale", "LLM · active learning", "LLM · active learning"),
         ("4 ตรวจ", "4 Audit", "เทียบกับชุด gold", "check the gold set")]
CX, CY, R = 300, 300, 170
for k, (th, en, sth, sen) in enumerate(STEPS):
    ang = -math.pi / 2 + k * math.pi / 2
    x, y = CX + R * math.cos(ang), CY + R * math.sin(ang)
    s.box(x - 100, y - 38, 200, 76, "ml-cell-b", 14)
    s.both(x, y - 6, th, en, "pl-label", "middle")
    s.both(x, y + 22, sth, sen, "pl-note", "middle")
    a2 = ang + math.pi / 2
    mid = (ang + a2) / 2
    s.raw(f'<path d="M{CX + 120 * math.cos(ang + 0.5):.1f} {CY + 120 * math.sin(ang + 0.5):.1f} A120 120 0 0 1 {CX + 120 * math.cos(a2 - 0.5):.1f} {CY + 120 * math.sin(a2 - 0.5):.1f}" class="pl-line" fill="none"/>')
    ex, ey = CX + 120 * math.cos(a2 - 0.5), CY + 120 * math.sin(a2 - 0.5)
    t = a2 - 0.5 + math.pi / 2
    s.raw(f'<path d="M{ex + 10 * math.cos(t + 2.6):.1f} {ey + 10 * math.sin(t + 2.6):.1f} L{ex:.1f} {ey:.1f} L{ex + 10 * math.cos(t - 2.6):.1f} {ey + 10 * math.sin(t - 2.6):.1f}" class="pl-line" fill="none"/>')
# results table on the right
s.box(600, 80, 560, 420, "nt-band-a", 14)
s.both(620, 116, "กรณีศึกษา: คอมเมนต์ 100 อัน เพื่อน 2 คนติดป้าย", "Case study: 100 comments, 2 friends label", "pl-label")
s.both(620, 142, "ป้าย: ชม · บ่น · เป็นกลาง (ตัวเลขสมมติ)", "labels: praise · complaint · neutral (made up)", "pl-note")
s.both(800, 184, "ตรงกัน", "agree", "pl-note", "middle")
s.both(1010, 184, "κ (หักส่วนบังเอิญ)", "κ (chance removed)", "pl-note", "middle")
for k, (th, en, agree, kap, ok, lab_th, lab_en) in enumerate([
        ("pilot 1: คู่มือแรก", "pilot 1: first guidelines", "64 / 100", "0.45", False, "ปานกลาง", "moderate"),
        ("pilot 2: เพิ่มกฎ 3 ข้อ", "pilot 2: 3 rules added", "88 / 100", "0.80", True, "ค่อนข้างมาก", "substantial")]):
    y = 222 + k * 120
    s.both(620, y, th, en, "pl-text")
    for j, v in enumerate((agree, kap)):
        cx = 800 + j * 210
        s.box(cx - 75, y + 16, 150, 50, "rc-res" if ok else "sw-warn-box", 10)
        s.text(cx, y + 49, v, "pl-label", "middle")
    s.both(1010, y + 88, lab_th, lab_en, "mp-s", "middle")
s.both(620, 476, "✓ pilot 2 ผ่าน (κ > 0.6) → เริ่มขยายได้", "✓ pilot 2 passes (κ > 0.6) → scale up", "ml-ok")
s.save("l15-loop.svg", 520)
