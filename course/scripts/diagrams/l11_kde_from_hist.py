"""nlp-basic L11-S10: a KDE is a smooth histogram. Four small panels on the real ratings of recommended reviews:
counts → counts ÷ 99 = density → the smooth curve over the bars → the curve alone (the KDE).

    course/.venv/bin/python scripts/diagrams/l11_kde_from_hist.py courses/nlp-basic

Data: courses/nlp-basic/data/airline_reviews.csv. Same seaborn defaults as the lesson's own kdeplot cell.
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

course = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic"
reviews = pd.read_csv(os.path.join(course, "data", "airline_reviews.csv"))
yes = reviews[reviews["Recommended"] == True].dropna(subset=["Rating"])  # noqa: E712
BLUE, ORANGE = sns.color_palette()[0], sns.color_palette()[1]
INK, RUST = "#2a2722", "#a44f2b"
print("recommended reviews with a rating:", len(yes))

import numpy as np  # noqa: E402

counts, edges = np.histogram(yes["Rating"], bins=np.arange(0.5, 11, 1))
top = int(counts.argmax())
top_x, top_n, n = (edges[top] + edges[top + 1]) / 2, int(counts[top]), len(yes)
print(f"tallest bar: {edges[top]}-{edges[top + 1]}, {top_n} reviews, {top_n} / {n} = {top_n / n:.2f}")

fig, axes = plt.subplots(1, 4, figsize=(15, 3.5), sharex=True)
kw = dict(binwidth=1, binrange=(0.5, 10.5), color=ORANGE, edgecolor="white")

ax = axes[0]
sns.histplot(yes["Rating"], ax=ax, stat="count", **kw)
ax.set_title(f"1. Histogram: count per bar\n({n} recommended reviews)", fontsize=11, color=INK)
ax.set_ylabel("Count")
ax.text(top_x, top_n + 0.8, f"{top_n}", ha="center", va="bottom", fontsize=11, fontweight="bold", color=RUST)
ax.set_ylim(0, top_n * 1.18)

ax = axes[1]
sns.histplot(yes["Rating"], ax=ax, stat="density", **kw)
ax.set_title(f"2. Divide each count by {n}:\ndensity (the bars add up to 1)", fontsize=11, color=INK)
ax.text(top_x, top_n / n + 0.008, f"{top_n} ÷ {n} = {top_n / n:.2f}", ha="center", va="bottom", fontsize=10.5,
        fontweight="bold", color=RUST)

ax = axes[2]
sns.histplot(yes["Rating"], ax=ax, stat="density", alpha=0.3, **kw)
sns.kdeplot(yes["Rating"], ax=ax, color=RUST, linewidth=2.5)
ax.set_title("3. Draw a smooth line\nover the tops of the bars", fontsize=11, color=INK)

ax = axes[3]
sns.kdeplot(yes["Rating"], ax=ax, color=ORANGE, fill=True, linewidth=2)
ax.set_title("4. Keep only the line:\nthis is the KDE", fontsize=11, color=INK)

ymax = (top_n / n) * 1.18
for a in axes:
    a.set_xlim(-0.5, 11.5)
    a.set_xlabel("Rating")
for a in axes[1:]:
    a.set_ylim(0, ymax)
    a.set_ylabel("Density" if a is axes[1] else "")
    a.tick_params(labelleft=a is axes[1])
fig.tight_layout(w_pad=5)
for a, b in zip(axes[:-1], axes[1:]):  # arrows between the panels, after the layout is fixed
    fig.add_artist(matplotlib.patches.FancyArrowPatch(
        (a.get_position().x1 + 0.006, 0.5), (b.get_position().x0 - 0.006 - (0.03 if b is axes[1] else 0), 0.5),
        transform=fig.transFigure, arrowstyle="-|>", mutation_scale=16, color=RUST, linewidth=1.8))
out = os.path.join(course, "images", "l11-kde-from-hist.png")
fig.savefig(out, dpi=144, bbox_inches="tight", facecolor="white", metadata={"Software": None})
print("wrote", out)
