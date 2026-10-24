"""Makes the practice annotation data for stats-dh lesson 15 (data reliability): three research assistants (A, B, C)
label the same 100 letters (women's letters, 1840–1890) for emotion (Joy, Anxiety, Sadness, Neutral) and for
formality (1–10). Pilot 1 uses the first, vague guidelines; pilot 2 labels 100 new letters with the revised guidelines
(anchor examples), so the raters agree much more. The letters are invented; the labels are simulated.

    course/.venv/bin/python scripts/diagrams/l15_practice_data.py courses/stats-dh/data

How the labels are made (numpy default_rng, seeds below):
  each letter has a true emotion (Neutral 45%, Joy 20%, Anxiety 20%, Sadness 15%) and a true formality 1–10;
  a rater copies the true emotion with probability `keep`, otherwise picks a confusable one (polite worry is easy
  to read as Neutral and back: Anxiety ↔ Neutral); formality = true + the rater's own bias + noise, clipped to 1–10.
  Pilot 1 (seed 14): keep 0.70, biases (0, +1.5, −1.5), noise sd 2.6.
  Pilot 2 (seed 34): keep 0.88, biases (0, +0.3, −0.3), noise sd 1.5.
"""

import os
import sys

import numpy as np
import pandas as pd

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/stats-dh/data"
EMO = ["Neutral", "Joy", "Anxiety", "Sadness"]
CONFUSE = {"Neutral": ["Anxiety", "Joy", "Sadness"], "Joy": ["Neutral", "Neutral", "Anxiety"],
           "Anxiety": ["Neutral", "Neutral", "Sadness"], "Sadness": ["Neutral", "Anxiety", "Anxiety"]}


def pilot(seed, keep, biases, sd, start_id):
    rng = np.random.default_rng(seed)
    n = 100
    truth = rng.choice(EMO, size=n, p=[0.45, 0.20, 0.20, 0.15])
    form = rng.integers(1, 11, size=n)
    df = pd.DataFrame({"letter_id": np.arange(start_id, start_id + n), "year": rng.integers(1840, 1891, size=n)})
    for r, bias in zip("ABC", biases):
        labels = [t if rng.random() < keep else rng.choice(CONFUSE[t]) for t in truth]
        df[f"emotion_{r}"] = labels
    for r, bias in zip("ABC", biases):
        df[f"formality_{r}"] = np.clip(np.round(form + bias + rng.normal(0, sd, size=n)), 1, 10).astype(int)
    return df


if __name__ == "__main__":
    p1 = pilot(14, 0.70, (0, 1.5, -1.5), 2.6, 1)
    p2 = pilot(34, 0.88, (0, 0.3, -0.3), 1.5, 101)
    p1.to_csv(os.path.join(OUT, "l15_pilot1.csv"), index=False)
    p2.to_csv(os.path.join(OUT, "l15_pilot2.csv"), index=False)
    print("wrote l15_pilot1.csv, l15_pilot2.csv")
