"""nlp-basic L11-S10 closing picture: one set of numbers drawn two ways, side by side. Made-up monthly spending on a
gacha game by 300 players (baht): 294 ordinary players and 6 super spenders, a heavy right tail.
Left: the KDE (density, an estimate of the PDF) with the area up to 1,000 baht shaded.
Right: the ECDF (the data's CDF), whose height at 1,000 baht is that same share (0.93).

    course/.venv/bin/python scripts/diagrams/l11_pdf_cdf_gacha.py courses/nlp-basic

The numbers are generated here (seed 11) and printed, so the lesson text can quote them.
"""

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

course = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic"
rng = np.random.default_rng(11)
base = np.round(rng.lognormal(mean=np.log(250), sigma=0.9, size=294), -1)  # 294 ordinary players, to the nearest 10
WHALES = np.array([8000, 12000, 15000, 18000, 25000, 30000.0])              # 6 super spenders
spend = np.concatenate([base, WHALES])
gacha = pd.DataFrame({"Spend (baht)": spend})
gacha.to_csv(os.path.join(course, "data", "gacha_spending.csv"), index=False)

X, BW = 1000, 100   # BW: the KDE's smoothing width in baht
share = (spend <= X).mean()
median, mean = np.median(spend), spend.mean()
whale_money = WHALES.sum() / spend.sum()
print(f"n={len(spend)} share<={X}: {share:.2f}  median {median:.0f}  mean {mean:.0f}  whales {len(WHALES)} "
      f"= {len(WHALES) / len(spend):.0%} of players, {whale_money:.0%} of the money")

INK, RUST, BLUE = "#2a2722", "#a44f2b", sns.color_palette()[0]
XMAX = 32000
fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4))

# left: the KDE, area up to X shaded, the whales marked on the axis
# a Gaussian KDE with a fixed 100-baht width, mirrored at 0 (spending can't be negative, so no area leaks below 0)
xs = np.linspace(0, XMAX, 16001)
ys = sum(np.exp(-0.5 * ((xs - v) / BW) ** 2) + np.exp(-0.5 * ((xs + v) / BW) ** 2) for v in spend)
ys /= len(spend) * BW * np.sqrt(2 * np.pi)
a.plot(xs, ys, color=BLUE, linewidth=2)
keep = xs <= X
area = np.trapezoid(ys[keep], xs[keep])
print(f"KDE total area {np.trapezoid(ys, xs):.3f}, area up to {X}: {area:.3f}")
a.fill_between(xs[keep], ys[keep], color=RUST, alpha=0.45)
a.text(X + 900, ys.max() * 0.62, f"shaded area = {area:.2f}\n(spend at most {X:,} baht)", fontsize=11, fontweight="bold", color=RUST)
a.plot(WHALES, [ys.max() * 0.02] * len(WHALES), "v", color=RUST, markersize=9, clip_on=False)
a.annotate(f"{len(WHALES)} super spenders:\n{WHALES.min():,.0f}–{WHALES.max():,.0f} baht", (19000, ys.max() * 0.05),
           xytext=(19000, ys.max() * 0.32), ha="center", fontsize=10.5, color=INK,
           arrowprops=dict(arrowstyle="->", color=INK))
a.text(16000, ys.max() * 0.12, "long right tail", ha="center", fontsize=10, color=INK, style="italic")
a.set_xlim(0, XMAX)
a.set_ylim(0, None)
a.set_yticks([])
a.set_xlabel("Spend per month (baht)")
a.set_ylabel("Density (height)")
a.set_title("PDF (KDE): where do the players pile up?", fontsize=11.5, color=INK)

# right: the ECDF, its height at X, and the slow climb through the tail
sns.ecdfplot(spend, ax=b, color=BLUE, linewidth=2.2)
b.plot([X, X], [0, share], color=RUST, linestyle="--", linewidth=1.3)
b.plot([0, X], [share, share], color=RUST, linestyle="--", linewidth=1.3)
b.plot([X], [share], "o", color=RUST)
b.text(X + 900, share - 0.1, f"at {X:,} baht: {share:.2f}", fontsize=12, fontweight="bold", color=RUST)
b.plot(WHALES, [0.02] * len(WHALES), "v", color=RUST, markersize=9, clip_on=False)
b.annotate(f"the last {len(WHALES) / len(spend):.0%} stretch\nfrom {WHALES.min():,.0f} to {WHALES.max():,.0f} baht",
           (19000, 0.99), xytext=(19000, 0.6), ha="center", fontsize=10.5, color=INK,
           arrowprops=dict(arrowstyle="->", color=INK))
b.set_xlim(0, XMAX)
b.set_ylim(0, 1.02)
b.set_xlabel("Spend per month (baht)")
b.set_ylabel("Share of players (at most x)")
b.set_title("CDF (ECDF): what share spend at most x?", fontsize=11.5, color=INK)
for ax in (a, b):
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))

fig.tight_layout(w_pad=4)
out = os.path.join(course, "images", "l11-pdf-cdf-gacha.png")
fig.savefig(out, dpi=144, bbox_inches="tight", facecolor="white", metadata={"Software": None})
print("wrote", out)
