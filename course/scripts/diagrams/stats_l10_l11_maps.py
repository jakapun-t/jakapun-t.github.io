"""Draws the lesson maps (the big picture card) of stats-dh lessons 10 and 11:
the problem on the lesson's running data, the parts of the lesson, what each part changes, its tools,
and its real result on that data.

    python3 scripts/diagrams/stats_l10_l11_maps.py courses/stats-dh/images

Every number is a real run in course/.venv (the same numbers as the lesson's code cells):
  L10 diabetes (load_diabetes, 80/20 split, random_state=42): LinearRegression on all 10 columns,
      test R² 0.453; on bmi, bp, s5 (SFS, filter and Lasso alpha=1 all keep these) 0.454;
      Ridge grid search best alpha 0.1 (CV R² 0.456), test R² 0.461.
  L11 obesity (108 rows; 70/30 split, random_state=42, StandardScaler, LogisticRegression):
      a straight line on Weight gives the heaviest person (120 kg) 0.51 and the lightest −0.21;
      the Weight-only model gives 100 kg p̂ 0.93; test accuracy 0.82 (33 people);
      Overweight precision 1.00, recall 0.44 (4 of 9); Overweight one-vs-rest AUC 0.94.

Uses the nt-*, pl-*, ml-*, sw-* and hk-* classes in templates/page.css (same look as nlp L11-S21).
"""

import os
import sys
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/stats-dh/images"


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


def lesson_map(name, title, data, problem, problem_note, ways_head, ways, last):
    """data: (th, en) pill; problem, problem_note: (th, en); ways: 4 tuples
    (title th, en, change th, en, tools, result th, en); last: (th, en) bottom line."""
    s = Svg(900, title)
    s.box(20, 16, 344, 54, "ml-cell", rx=27)
    s.both(40, 50, data[0], data[1], "pl-text")
    s.raw('<path d="M370 43 L392 43" class="nt-arrow"/><path d="M384 36 L393 43 L384 50" class="nt-arrow"/>')
    s.box(400, 10, 480, 66, "sw-warn-box", rx=12)
    s.both(416, 38, problem[0], problem[1], "nt-task")
    s.both(416, 64, problem_note[0], problem_note[1], "pl-note")
    s.both(450, 112, ways_head[0], ways_head[1], "nt-head", "middle")
    for k, (tth, ten, cth, cen, tools, exth, exen) in enumerate(ways):
        x = 20 + (k % 2) * 440
        y = 128 + (k // 2) * 162
        s.box(x, y, 420, 148, "ml-cell", rx=14)
        s.both(x + 20, y + 34, tth, ten, "nt-task")
        s.both(x + 20, y + 62, cth, cen, "hk-desc")
        s.text(x + 20, y + 92, tools, "pl-note")
        s.both(x + 20, y + 128, exth, exen, "ml-neg" if "✗" in exen else "ml-ok" if "✓" in exen else "pl-note")
    s.both(450, 466, last[0], last[1], "pl-note", "middle")
    s.save(name, 484)


# ---------------------------------------------------------------- L10 model tuning (diabetes)
lesson_map(
    "l10-map-lesson.svg",
    "Lesson map. The problem: a linear model on all 10 diabetes columns scores test R² 0.453. Three ways to score better with the same data and model: 2 pick features by hand, 3 let an algorithm pick (bmi, bp, s5: 0.454), 4 tune the settings (Ridge alpha 0.1: test R² 0.461), then 5 review.",
    ("diabetes · 442 คน · 10 คอลัมน์", "diabetes · 442 patients · 10 columns"),
    ("1 ปัญหา: linear model กับ 10 คอลัมน์ได้ R² 0.453", "1 The problem: linear model, 10 columns: R² 0.453"),
    ("(R² บนชุด test) ข้อมูลเดิม โมเดลเดิม ทำให้ดีขึ้นได้ไหม", "(test R²) Same data, same model: can we score better?"),
    ("3 วิธี แล้วทบทวน", "Three ways, then review"),
    [
        ("2 เลือก feature เอง", "2 Pick features by hand", "ตัดคอลัมน์ที่ช่วยทำนายไม่ได้", "Drop the columns that cannot help",
         "6-question checklist · domain knowledge", "diabetes: ทั้ง 10 เป็นค่าที่วัด ตัดเองไม่ออก", "diabetes: 10 measurements, none to drop"),
        ("3 ให้อัลกอริทึมเลือก", "3 Let an algorithm pick", "ให้คะแนนคอลัมน์ แล้วเก็บตัวที่ดีที่สุด", "Score the columns, keep the best",
         "filter · SFS · RFE · Lasso", "เหลือ bmi, bp, s5: test R² 0.454 ✓", "bmi, bp, s5 only: test R² 0.454 ✓"),
        ("4 ปรับค่าตั้ง", "4 Tune the settings", "เลือก alpha ด้วย cross-validation", "Choose alpha with cross-validation",
         "Ridge · grid search · random search", "alpha 0.1: test R² 0.461 ✓", "alpha 0.1: test R² 0.461 ✓"),
        ("5 ทบทวน", "5 Review", "เก็บชุด test ไว้วัดครั้งเดียวตอนท้าย", "Keep the test set for one final check",
         "summary · exit ticket", "ทุกการเลือกใช้แค่ชุด train", "every choice uses only the training set"),
    ],
    ("feature คือโมเดลเรียนจาก “อะไร” hyperparameter คือเรียน “อย่างไร”", "Features: what the model learns from. Hyperparameters: how it learns."),
)

# ---------------------------------------------------------------- L11 logistic regression (obesity)
lesson_map(
    "l11-map-lesson.svg",
    "Lesson map. The problem: predict which of 4 weight groups each of 108 people is in; a straight line gives no probability. Four steps: 2 a line inside a sigmoid (100 kg: 0.93, obese), 3 more than two classes (test accuracy 0.82), 4 count the mistakes (Overweight recall 0.44), 5 move the threshold (Overweight AUC 0.94), then 6 evaluate and review.",
    ("obesity · 108 คน · 4 กลุ่ม", "obesity · 108 people · 4 groups"),
    ("1 ปัญหา: แต่ละคนอยู่ภาวะน้ำหนักกลุ่มไหน", "1 The problem: which weight group is each in?"),
    ("เส้นตรงให้ความน่าจะเป็นไม่ได้: 120 กก. ได้แค่ 0.51", "A straight line is no probability: 120 kg gets only 0.51"),
    ("4 ขั้นจากความน่าจะเป็นสู่กลุ่ม", "Four steps from a probability to a class"),
    [
        ("2 เส้นตรงในฟังก์ชัน sigmoid", "2 A line inside a sigmoid", "บีบเส้นตรงให้อยู่ระหว่าง 0 ถึง 1", "Squeeze the line into 0 to 1",
         "sigmoid · threshold 0.5 · log loss", "หนัก 100 กก. → p̂ 0.93 → Obese ✓", "100 kg → p̂ 0.93 → Obese ✓"),
        ("3 มากกว่าสองกลุ่ม", "3 More than two classes", "คะแนนหนึ่งค่าต่อกลุ่ม แล้ว softmax", "One score per class, then softmax",
         "softmax · LogisticRegression", "ทายถูก 0.82 ของคน test 33 คน ✓", "accuracy 0.82 on 33 test people ✓"),
        ("4 นับว่าผิดแบบไหน", "4 Count the mistakes", "ดูว่าโมเดลผิดไปทางไหน", "See which way the model is wrong",
         "confusion matrix · precision · recall · F1", "Overweight: จับได้ 4 จาก 9 (recall 0.44) ✗", "Overweight: 4 of 9 caught (recall 0.44) ✗"),
        ("5 เลื่อน threshold", "5 Move the threshold", "แลกการเตือนผิดกับการพลาด", "Trade false alarms for misses",
         "threshold · ROC curve · AUC", "Overweight: AUC 0.94 เรียงคะแนนได้ดี", "Overweight AUC 0.94: scores rank well"),
    ],
    ("6 ประเมินโมเดลภาวะน้ำหนักด้วยทุกเครื่องมือ แล้วทบทวน", "6 Evaluate the obesity model with every tool, then review"),
)
