"""Small SVG helpers for the nlp-basic concept pictures (basic_l10_concepts.py … basic_l13_concepts.py),
in the style of nlp l12-why-chunk.svg (scripts/diagrams/nlp_l12_figures.py, figure 17).

The SVGs are inlined into the page (```figure), so text uses the page fonts and the nt-*, pl-*, ml-*,
sw-*, dg-*, rc-* classes in templates/page.css; ไทย/EN labels follow the language switch (data-only).
"""

import math
import os
import unicodedata
from html import escape

HALO = "paint-order: stroke; stroke: var(--card); stroke-width: 5px; stroke-linejoin: round"
# hk-mono (19px, bold, blue) names --font-mono, which the page does not define: set the code font here
MONO = "font-family: var(--font-code)"


def style(cls, halo):
    s = "; ".join(x for x in (MONO if "hk-mono" in cls.split() else "", HALO if halo else "") if x)
    return f' style="{s}"' if s else ""


def width(s, fs=19):
    """Rough text width, for laying out chips (checked afterwards with getBBox in the preview)."""
    return sum(0 if unicodedata.category(c) == "Mn" else fs * (1.1 if ord(c) > 0x1F000 else 0.56) for c in s)


class Svg:
    def __init__(self, out_dir, w, title):
        self.dir, self.w, self.title, self.out = out_dir, w, title, []

    def raw(self, s):
        self.out.append(s)

    def text(self, x, y, s, cls, anchor="start", halo=False, lang_en=True):
        lang = ' lang="en"' if lang_en else ""
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}"{lang}{style(cls, halo)}>{escape(s)}</text>')

    def thai(self, x, y, s, cls, anchor="start", halo=False):
        """Language data (Thai words), shown in both modes."""
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}"{style(cls, halo)}>{escape(s)}</text>')

    def both(self, x, y, th, en, cls, anchor="start", halo=False):
        h = style(cls, halo)
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="th"{h}>{escape(th)}</text>')
        self.out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="en" lang="en"{h}>{escape(en)}</text>')

    def box(self, x, y, w, h, cls, rx=12, extra=""):
        self.out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}"{extra}/>')

    def line(self, x1, y1, x2, y2, cls="pl-line", dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="{cls}"{dash}/>')

    def path(self, d, cls="pl-line", extra=""):
        if cls.startswith("dg-rule"):  # rule classes set only a stroke: an open corner path must not fill
            extra += ' fill="none"'
        self.out.append(f'<path d="{d}" class="{cls}"{extra}/>')

    def arrow(self, x1, y1, x2, y2, dashed=False, cls="pl-line"):
        self.line(x1, y1, x2, y2, cls, dashed)
        self.head(x1, y1, x2, y2, cls)

    def head(self, x1, y1, x2, y2, cls="pl-line"):
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 10 * math.cos(a - 0.55), y2 - 10 * math.sin(a - 0.55))
        p2 = (x2 - 10 * math.cos(a + 0.55), y2 - 10 * math.sin(a + 0.55))
        self.out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2:g} {y2:g} L{p2[0]:.1f} {p2[1]:.1f}" class="{cls}"/>')

    def curve(self, x1, y1, cx, cy, x2, y2, dashed=False):
        """A quadratic arrow from (x1, y1) to (x2, y2) bending through the control point (cx, cy)."""
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="M{x1:g} {y1:g} Q{cx:g} {cy:g} {x2:g} {y2:g}" class="pl-line"{dash}/>')
        self.head(cx, cy, x2, y2)

    def badge(self, x, y, k):
        """A numbered circle; the card's text explains the item with the same number."""
        self.out.append(f'<g class="dg-badge"><circle cx="{x:g}" cy="{y:g}" r="13"/>'
                        f'<text x="{x:g}" y="{y + 5:g}" text-anchor="middle" lang="en">{k}</text></g>')

    def bubble(self, cx, y, th, en, w):
        """The running example's question, in a bubble at the top."""
        self.box(cx - w / 2, y, w, 46, "nt-bubble", 23)
        self.both(cx, y + 30, th, en, "pl-text", "middle")

    def chip(self, x, y, t, cls="pl-chip", tcls="pl-chip-text", fs=19, pad=12, h=34, thai=True):
        """A word chip with its left edge at x, centred on y; returns its right edge."""
        w = width(t, fs) + 2 * pad
        self.box(x, y - h / 2, w, h, cls, 8)
        (self.thai if thai else self.text)(x + w / 2, y + fs * 0.32, t, tcls, "middle")
        return x + w

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img">'
               f'<title>{escape(self.title)}</title>', *self.out, "</svg>"]
        with open(os.path.join(self.dir, name), "w", encoding="utf-8") as f:
            f.write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")
