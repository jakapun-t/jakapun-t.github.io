"""Draws the teaching figures of stats-dh lesson 13 (other classification models) as PNGs in images/.

    course/.venv/bin/python scripts/diagrams/stats_l13_charts.py courses/stats-dh

Charts students draw themselves come from the lesson's own code cells (npm run outputs); this script draws only
the annotated explainers: decision regions on height × weight (5-fold cross-validation accuracy in each title)
and the KNN neighbourhoods of a new person (186 cm, 100 kg). Data: the course's obesity.csv (Worksheet 4).
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Ellipse
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

course = sys.argv[1] if len(sys.argv) > 1 else "courses/stats-dh"
IMG = os.path.join(course, "images")
df = pd.read_csv(os.path.join(course, "data", "obesity.csv"))

INK = "#2a2722"
MUTED = "#6b655c"
ORDER = ["Underweight", "Normal Weight", "Overweight", "Obese"]
COLOR = {"Underweight": "#4d7aa8", "Normal Weight": "#4f8a5f", "Overweight": "#c08a2e", "Obese": "#a44f2b"}
MARK = {"Underweight": "s", "Normal Weight": "o", "Overweight": "^", "Obese": "D"}
plt.rcParams.update({"axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED, "font.size": 11})

X = df[["Height", "Weight"]].values.astype(float)
y = df["Label"].values
CV = StratifiedKFold(5, shuffle=True, random_state=42)


def save(fig, name, dpi=144):
    fig.savefig(os.path.join(IMG, name), dpi=dpi, bbox_inches="tight", facecolor="white", metadata={"Software": None})
    plt.close(fig)
    print("wrote", name)


def people(ax, s=34):
    for lab in ORDER:
        m = y == lab
        ax.scatter(X[m, 0], X[m, 1], s=s, marker=MARK[lab], color=COLOR[lab], edgecolor="white", lw=0.6, label=lab, zorder=3)


def regions(ax, model, title):
    pipe = make_pipeline(StandardScaler(), model)
    acc = cross_val_score(pipe, X, y, cv=CV).mean()
    pipe.fit(X, y)
    hh, ww = np.meshgrid(np.linspace(110, 222, 300), np.linspace(10, 128, 300))
    pred = pipe.predict(np.c_[hh.ravel(), ww.ravel()]).reshape(hh.shape)
    code = np.vectorize(ORDER.index)(pred)
    from matplotlib.colors import ListedColormap
    ax.contourf(hh, ww, code, levels=[-0.5, 0.5, 1.5, 2.5, 3.5], cmap=ListedColormap([COLOR[c] for c in ORDER]), alpha=0.18)
    ax.contour(hh, ww, code, levels=[0.5, 1.5, 2.5], colors=INK, linewidths=0.9)
    people(ax, 26)
    ax.set_title(f"{title}\n5-fold accuracy {acc:.2f}", fontsize=12, color=INK)
    ax.set_xlim(110, 222)
    ax.set_ylim(10, 128)
    ax.set_xlabel("Height (cm)")
    ax.set_ylabel("Weight (kg)")
    return acc


# ---------------------------------------------------------------- L12-S01 hook: straight cuts vs the tree's boxes
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.9))
regions(axes[0], LogisticRegression(max_iter=2000), "Logistic regression: straight cuts")
regions(axes[1], DecisionTreeClassifier(max_depth=3, random_state=42), "Decision tree (depth 3): one question at a time")
for bmi, lab in [(18.5, "BMI 18.5"), (25, "BMI 25"), (30, "BMI 30")]:
    h = np.linspace(110, 222, 100)
    for ax in axes:
        ax.plot(h, bmi * (h / 100) ** 2, color=MUTED, lw=1, ls=":")
axes[0].text(212, 30 * 2.12 ** 2 * 0.96, "BMI 30", color=MUTED, fontsize=9, ha="right", va="top")
axes[0].text(218, 18.5 * 2.18 ** 2 * 0.86, "BMI 18.5", color=MUTED, fontsize=9, ha="right", va="top")
axes[1].legend(loc="upper left", fontsize=9, frameon=False)
fig.tight_layout()
save(fig, "l13-hook.png")

# ---------------------------------------------------------------- L12-S16 six models, same people
fig, axes = plt.subplots(2, 3, figsize=(14, 8.6))
MODELS = [
    (LogisticRegression(max_iter=2000), "Logistic regression"),
    (DecisionTreeClassifier(max_depth=3, random_state=42), "Decision tree (depth 3)"),
    (KNeighborsClassifier(5), "KNN (k = 5)"),
    (SVC(C=10), "SVM (RBF kernel, C = 10)"),
    (RandomForestClassifier(random_state=42), "Random forest (100 trees)"),
    (GradientBoostingClassifier(random_state=42), "Gradient boosting (100 trees)"),
]
for ax, (m, t) in zip(axes.ravel(), MODELS):
    print(t, round(regions(ax, m, t), 3))
axes[0, 0].legend(loc="upper left", fontsize=9, frameon=False)
fig.tight_layout()
save(fig, "l13-boundaries.png")

# ---------------------------------------------------------------- L12-S14 KNN: k = 3 vs k = 7 for a new person
sc = StandardScaler().fit(X)
new = np.array([186.0, 100.0])
d = np.sqrt(((sc.transform(X) - sc.transform([new])) ** 2).sum(1))
order = np.argsort(d, kind="stable")
fig, axes = plt.subplots(1, 2, figsize=(11.5, 5))
for ax, k in zip(axes, [3, 7]):
    people(ax, 60)
    near = order[:k]
    ax.scatter(X[near, 0], X[near, 1], s=230, facecolor="none", edgecolor=INK, lw=1.6, zorder=4)
    # several people share one height and weight: say how many neighbours sit on each circled spot
    for (hx, wy), cnt in pd.Series([tuple(p) for p in X[near]]).value_counts().items():
        if cnt > 1:
            ax.text(hx + 1.3, wy + 1.2, f"×{cnt}", fontsize=11, color=INK, fontweight="bold", zorder=6)
    r = d[order[k - 1]] * 1.04
    ax.add_patch(Ellipse(new, 2 * r * sc.scale_[0], 2 * r * sc.scale_[1], fill=False, ls="--", color=INK, lw=1.2))
    ax.scatter(*new, s=200, marker="*", color=INK, zorder=5)
    votes = pd.Series(y[near]).value_counts()
    win = votes.index[0]
    ax.set_title(f"k = {k}: " + ", ".join(f"{v} {c}" for c, v in votes.items()) + f"  →  {win}", fontsize=12, color=COLOR[win])
    ax.set_xlim(165, 212)
    ax.set_ylim(72, 122)
    ax.set_aspect(sc.scale_[1] / sc.scale_[0])
    ax.set_xlabel("Height (cm)")
    ax.set_ylabel("Weight (kg)")
    ax.annotate("new person\n186 cm, 100 kg", new, xytext=(168, 116), fontsize=10, color=INK,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1))
axes[1].legend(loc="lower right", fontsize=9, frameon=False)
fig.tight_layout()
save(fig, "l13-knn.png")
