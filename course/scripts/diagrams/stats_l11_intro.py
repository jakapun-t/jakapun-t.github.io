"""The two pictures of stats-dh L11-S01 (what is classification?), for students who meet classifiers every day:
  l11-classify-everywhere.svg  eight apps that sort things into groups (what each looks at → the groups it picks from)
  l11-classify-parts.svg       the parts on one example: a music app learns genres from songs whose genre is known
                               (features blue, label amber), then guesses the genre of a new song.
The examples are descriptions, not data: no numbers to check. ไทย/EN labels follow the language switch.

    course/.venv/bin/python scripts/diagrams/stats_l11_intro.py courses/stats-dh/images

Uses the mp-*, nt-*, rc-*, ml-* and dg-* classes in templates/page.css.
"""

from stats_svg import Svg, emoji_or_icon, width

W = 1100

# ================================================================ eight apps that classify
APPS = [
    ("🎵", "แอปเพลง", "Music app", "จังหวะ · บีต · เสียงร้อง", "tempo · beat · voice", ["K-pop", "lo-fi", "rock"], ["K-pop", "lo-fi", "rock"]),
    ("📱", "ฟีด For You", "For You feed", "เวลาที่ดู · ไลก์", "watch time · likes", ["ดูจบ", "ปัดทิ้ง"], ["watch", "swipe"]),
    ("🚨", "SMS หลอกลวง", "Scam SMS", "ลิงก์ · คำเร่งด่วน", "links · urgent words", ["หลอกลวง", "ปลอดภัย"], ["scam", "safe"]),
    ("icon:app-gamechat", "แชตในเกม", "Game chat", "คำ · อีโมจิ · ตัวใหญ่", "words · emoji · CAPS", ["toxic", "ปกติ"], ["toxic", "OK"]),
    ("🔓", "สแกนหน้าปลดล็อก", "Face unlock", "ตา · จมูก · กราม", "eyes · nose · jaw", ["คุณ", "ไม่ใช่คุณ"], ["you", "not you"]),
    ("📷", "อัลบั้มรูปอัตโนมัติ", "Photo albums", "พิกเซลในภาพ", "the photo's pixels", ["อาหาร", "สัตว์เลี้ยง", "เซลฟี"], ["food", "pets", "selfies"]),
    ("🌐", "แอปแปลภาษา", "Translate app", "ตัวอักษร · คำ", "letters · words", ["ไทย", "อังกฤษ", "เกาหลี"], ["Thai", "English", "Korean"]),
    ("💳", "แอปธนาคาร", "Bank app", "ยอดเงิน · สถานที่", "amount · place", ["โกง", "ปกติ"], ["fraud", "normal"]),
]

s = Svg(W, "Classification is everywhere. Eight apps that sort things into groups, each with what it looks at and the "
           "groups it picks from: a music app (tempo, beat, voice → K-pop, lo-fi, rock), the For You feed (watch time, "
           "likes → watch or swipe), scam SMS (links, urgent words → scam or safe), game chat (words, emoji, caps → toxic "
           "or OK), face unlock (eyes, nose, jaw → you or not you), photo albums (pixels → food, pets, selfies), a "
           "translate app (letters, words → Thai, English, Korean), a bank app (amount, place → fraud or normal).")
s.bubble("วันนี้คุณใช้แอปไหนไปแล้วบ้าง ทุกแอปนี้กำลังจัดของเข้ากลุ่ม", "Used any of these today? Every one is sorting things into groups")
TW, TG, TH_ = 252, 24, 182
for k, (icon, nth, nen, fth, fen, lth, len_) in enumerate(APPS):
    x, y = 10 + (k % 4) * (TW + TG), 72 + (k // 4) * (TH_ + 18)
    s.box(x, y, TW, TH_, "ml-cell", 14)
    s.raw(f'<circle cx="{x + 40}" cy="{y + 42}" r="27" style="fill:var(--tag-concept-bg)"/>')
    emoji_or_icon(s, icon, x + 40, y + 42, 50)
    s.both(x + 78, y + 40, nth, nen, "mp-t")
    two = len(len_) == 2
    s.both(x + 78, y + 64, "2 กลุ่ม" if two else f"{len(len_)} กลุ่ม", "2 groups" if two else f"{len(len_)} groups", "mp-s")
    s.both(x + 16, y + 98, "ดูจาก", "looks at", "mp-s")
    s.both(x + 16, y + 121, fth, fen, "hk-desc")
    for lang, labels in (("th", lth), ("en", len_)):
        cx = x + 16
        for i, lab in enumerate(labels):
            w = width(lab, 16) + 16
            cls = "ml-cell-b" if i == 0 else "ml-cell"
            attr = ' lang="en"' if lang == "en" else ""
            s.raw(f'<g data-only="{lang}"{attr}>'
                  f'<rect x="{cx:g}" y="{y + 138}" width="{w:g}" height="28" rx="14" class="{cls}"/>'
                  f'<text x="{cx + w / 2:g}" y="{y + 158}" text-anchor="middle" class="mp-chip">{lab}</text></g>')
            cx += w + 6
s.save("l11-classify-everywhere.svg", 72 + 2 * TH_ + 18 + 10)


# ================================================================ the parts, on one example
ROWS = [("เพลง 1", "song 1", "เร็ว", "fast", "สูง", "high", "ใช่", "yes", "K-pop"),
        ("เพลง 2", "song 2", "เร็ว", "fast", "สูง", "high", "ไม่", "no", "rock"),
        ("เพลง 3", "song 3", "ช้า", "slow", "ต่ำ", "low", "ไม่", "no", "lo-fi"),
        ("เพลง 4", "song 4", "เร็ว", "fast", "สูง", "high", "ใช่", "yes", "K-pop")]
GENRE = {"K-pop": "var(--accent)", "rock": "var(--ink-2)", "lo-fi": "var(--tag-concept-dot)"}

s = Svg(W, "The parts of classification on one example. Left, labeled data: four songs whose genre is known. The blue "
           "columns are the features (tempo, energy, Korean lyrics: what we know); the amber column is the label (the "
           "genre: the answer). Right: a new song, fast, high energy, Korean lyrics, genre unknown, goes into the model "
           "that learned the pattern from the table, and it answers K-pop.")
s.bubble("แอปเพลงรู้ได้ยังไงว่าเพลงใหม่เป็น K-pop", "How does a music app know a new song is K-pop?")
s.panel(10, 70, 560, 290, "ml-cell", "เรียนจากเพลงที่รู้แนวแล้ว (labeled data)", "Learn from songs whose genre is known (labeled data)", 1)
COLX = [34, 160, 262, 364, 478]
s.box(140, 112, 316, 236, "nt-band-a", 10)
s.box(462, 112, 96, 236, "rc-ctx", 10)
s.both(298, 138, "feature: สิ่งที่เรารู้", "features: what we know", "pl-label", "middle")
s.both(510, 138, "label", "label", "pl-label", "middle")
for x, th, en in zip(COLX, ["เพลง", "จังหวะ", "พลัง", "ร้องเกาหลี", "แนว"], ["song", "tempo", "energy", "Korean?", "genre"]):
    s.both(x, 170, th, en, "mp-s")
for r, (sth, sen, a_th, a_en, b_th, b_en, c_th, c_en, g) in enumerate(ROWS):
    y = 204 + r * 36
    s.line(24, y - 24, 556, y - 24, "mp-guide")
    s.both(COLX[0], y, sth, sen, "pl-text")
    s.both(COLX[1], y, a_th, a_en, "pl-text")
    s.both(COLX[2], y, b_th, b_en, "pl-text")
    s.both(COLX[3], y, c_th, c_en, "pl-text")
    s.fill(472, y - 19, 76, 26, GENRE[g], 13)
    s.raw(f'<text x="510" y="{y}" text-anchor="middle" class="ml-model-text" lang="en">{g}</text>')

s.panel(590, 70, 500, 290, "ml-cell", "ทายแนวของเพลงใหม่", "Guess the genre of a new song", 2)
s.box(610, 116, 460, 50, "nt-band-a", 10)
s.both(626, 148, "เพลงใหม่: เร็ว · สูง · ใช่", "new song: fast · high · yes", "pl-text")
s.box(1000, 126, 56, 30, "ml-cell", 15)
s.text(1028, 147, "?", "mp-n", "middle")
s.arrow(840, 170, 840, 204)
s.box(760, 208, 160, 46, "ml-model", 10)
s.both(840, 237, "โมเดล", "model", "ml-model-text", "middle")
s.arrow(840, 258, 840, 290)
s.fill(790, 296, 100, 34, GENRE["K-pop"], 17)
s.raw('<text x="840" y="319" text-anchor="middle" class="ml-model-text" lang="en">K-pop</text>')
s.text(900, 320, "✓", "ml-ok")
s.raw('<path d="M572 231 L752 231" class="nt-arrow" stroke-dasharray="6 5"/><path d="M744 224 L753 231 L744 238" class="nt-arrow"/>')
s.both(662, 220, "รูปแบบที่เรียนได้", "the pattern it learned", "mp-s", "middle")
s.save("l11-classify-parts.svg", 370)
