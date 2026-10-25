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
s = Svg(W, "Reliability and validity as four targets. The bullseye is the concept we mean to label, fake news. 1 Reliable "
           "and valid: the marks agree and hit the centre. 2 Reliable but not valid: the marks agree but all land off "
           "centre, labelling angry language instead of fake news. 3 Valid on average but not reliable: the marks scatter "
           "around the centre. 4 Neither.")
s.bubble("ผู้ติดป้าย 6 คนติดป้าย “ข่าวปลอม” ให้ข่าวเดียวกัน ป้ายดีหรือไม่", "Six annotators label the same article for “fake news”: are the labels good?")
TARGETS = [
    ("ตรงกัน และ ถูกเป้า", "Reliable and valid", [(0, 0), (6, -4), (-5, 3), (3, 6), (-4, -5), (5, 2)], 0, 0, "ml-ok", ("✓ เป้าหมาย", "✓ the goal")),
    ("ตรงกัน แต่ ผิดเป้า", "Reliable, not valid", [(0, 0), (5, -3), (-4, 4), (3, 5), (-5, -4), (4, 3)], 48, -40, "ml-neg",
     ("✗ วัด “ภาษาโกรธ” แทน", "✗ labels angry tone")),
    ("ถูกเป้า แต่ไม่ตรงกัน", "Valid, not reliable", [(-50, 20), (40, 45), (30, -55), (-45, -35), (55, -5), (-25, 50)], 0, 0, "ml-neg",
     ("✗ คนละคนคนละแบบ", "✗ each labels differently")),
    ("ไม่ตรงกัน และ ผิดเป้า", "Neither", [(-30, 10), (30, 40), (50, -20), (-10, -55), (65, 30), (5, 25)], 35, -30, "ml-neg", ("✗ ใช้ไม่ได้", "✗ useless")),
]
PW = 272
for i, (th, en, marks, dx, dy, cls, (rth, ren)) in enumerate(TARGETS):
    x0 = 20 + i * (PW + 17)
    s.box(x0, 70, PW, 400, "nt-band-a" if i == 0 else "sw-warn-box", 14)
    s.badge(x0 + 30, 96, i + 1)
    s.both(x0 + 50, 102, th, en, "pl-label")
    cx, cy = x0 + PW / 2, 260
    for r, cls_r in ((110, "ml-cell"), (78, "ml-cell"), (46, "ml-cell"), (16, "ml-cell-b")):
        s.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls_r}"/>')
    for (mx, my) in marks:
        x, y = cx + mx + dx, cy + my + dy
        s.raw(f'<path d="M{x - 7} {y - 7} L{x + 7} {y + 7} M{x + 7} {y - 7} L{x - 7} {y + 7}" class="pl-line" stroke-width="3"/>')
    s.both(x0 + 20, 420, rth, ren, cls)
    if i == 1:
        s.both(x0 + 20, 448, "ป้ายตรงกัน (IRR สูง) แต่ใช้ไม่ได้", "high agreement, still useless", "pl-note")
s.both(20, 504, "จุดกลางเป้า = สิ่งที่ตั้งใจวัด (ข่าวปลอม) · ✕ = ป้ายของผู้ติดป้ายแต่ละคน", "Centre = the concept we mean (fake news) · ✕ = each annotator's label", "pl-note")
s.both(20, 536, "reliability (ความน่าเชื่อถือ) = ป้ายตรงกันไหม · validity (ความถูกต้อง) = วัดสิ่งที่ตั้งใจวัดจริงไหม", "reliability = do the labels agree? · validity = do they measure what we mean?", "pl-label")
s.save("l15-validity.svg", 554)

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
           "says yes 35%, so chance agreement p_e = 0.27 × 0.35 + 0.73 × 0.65 = 0.569. Kappa = (0.72 − 0.569) / (1 − "
           "0.569) = 0.35: only fair agreement, though they agree 72% of the time.")
s.bubble("A กับ B ตอบตรงกันว่า “กังวลหรือไม่” 72% ดีพอไหม", "A and B agree on “Anxiety or not” 72% of the time: is that good enough?")
# 1 the table
s.panel(20, 70, 380, 430, "nt-band-a", "ตารางของสองคน", "Two raters' table", 1)
X, Y = 150, 170
s.both(X + 115, Y - 20, "ผู้ช่วย B", "RA B", "pl-note", "middle")
s.text(X + 55, Y + 10, "yes", "pl-note", "middle")
s.text(X + 175, Y + 10, "no", "pl-note", "middle")
s.both(40, Y + 90, "ผู้ช่วย A", "RA A", "pl-note")
s.text(X - 20, Y + 62, "yes", "pl-note", "end")
s.text(X - 20, Y + 172, "no", "pl-note", "end")
for (r, c, v, agree) in [(0, 0, 17, True), (0, 1, 10, False), (1, 0, 18, False), (1, 1, 55, True)]:
    x, y = X + c * 120, Y + 24 + r * 110
    s.box(x, y, 110, 100, "rc-res" if agree else "ml-cell", 10)
    s.text(x + 55, y + 60, str(v), "pl-label", "middle")
s.both(40, 440, "สีเขียว = ตอบตรงกัน: 17 + 55 = 72", "green = agree: 17 + 55 = 72", "pl-text")
s.both(40, 474, "A ตอบ yes 27 · B ตอบ yes 35", "A says yes 27 · B says yes 35", "pl-note")
# 2 chance agreement
s.panel(420, 70, 360, 430, "sw-warn-box", "ตรงกันเพราะบังเอิญ", "Agreement by chance", 2)
s.both(440, 140, "ถ้าทั้งคู่เดาสุ่มตามสัดส่วนของตัวเอง", "If both guessed at their own rates", "pl-note")
s.text(440, 190, "both yes: 0.27 × 0.35 = 0.095", "pl-text")
s.text(440, 230, "both no:  0.73 × 0.65 = 0.475", "pl-text")
s.text(440, 290, "pₑ = 0.095 + 0.475 = 0.569", "pl-label")
s.both(440, 350, "ป้าย “ไม่กังวล” มีมาก", "“not anxious” is common,", "pl-note")
s.both(440, 378, "จึงตรงกันง่ายแม้ไม่ได้อ่านเลย", "so they'd agree often without reading", "pl-note")
s.both(440, 474, "✗ 57% ของความตรงกันได้มาฟรี", "✗ 57% agreement comes for free", "ml-neg")
# 3 kappa
s.panel(800, 70, 360, 430, "nt-band-a", "kappa: เกินกว่าบังเอิญเท่าไร", "Kappa: how far beyond chance", 3)
s.text(820, 150, "κ = (pₒ − pₑ) / (1 − pₑ)", "pl-label")
s.text(820, 196, "= (0.72 − 0.569) / (1 − 0.569)", "pl-text")
s.text(820, 236, "= 0.151 / 0.431 = 0.35", "pl-label")
# a gauge from 0 to 1 with the bands
G0, G1, GY = 830, 1130, 320
for (a, b, cls) in [(0, 0.2, "ml-cell"), (0.2, 0.4, "rc-ctx"), (0.4, 0.6, "ml-cell"), (0.6, 0.8, "rc-ctx"), (0.8, 1.0, "rc-res")]:
    s.box(G0 + a * (G1 - G0), GY, (b - a) * (G1 - G0), 26, cls, 2)
for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
    s.text(G0 + v * (G1 - G0), GY + 48, f"{v:g}", "pl-note", "middle")
kx = G0 + 0.35 * (G1 - G0)
s.raw(f'<path d="M{kx} {GY - 4} l-8 -14 h16 Z" class="pl-dot"/>')
s.text(kx, GY - 24, "0.35", "pl-label", "middle")
s.both(820, 410, "0 = ตรงกันแค่เท่าบังเอิญ · 1 = ตรงกันทุกฉบับ", "0 = chance level · 1 = perfect", "pl-note")
s.both(820, 474, "✗ fair เท่านั้น ต้องแก้คู่มือ", "✗ only fair: fix the guidelines", "ml-neg")
s.save("l15-kappa.svg", 520)

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
