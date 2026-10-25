"""Shared drawing helpers for the stats-dh concept pictures (lessons 12–14): the Svg class (ไทย/EN text pairs,
panels, badges, people, stacked bars by weight group), entropy. Each lesson's script
imports these and draws its own figures; the output folder is the first command-line argument.
"""

import math
import os
import re
import sys
import unicodedata
from html import escape

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/stats-dh/images"
W = 1180
# weight groups, in the order Underweight, Normal Weight, Overweight, Obese
CLS = ["var(--tag-concept-dot)", "var(--tag-exercise-dot)", "var(--tag-example-dot)", "var(--accent)"]
NAMES = [("ผอม", "Underweight"), ("ปกติ", "Normal"), ("น้ำหนักเกิน", "Overweight"), ("อ้วน", "Obese")]


def width(s, fs=19):
    return sum(0 if unicodedata.category(c) == "Mn" else fs * (1.1 if ord(c) > 0x1F000 else 0.58) for c in s)


def H(counts):
    n = sum(counts)
    return -sum(c / n * math.log2(c / n) for c in counts if c)


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

    def fill(self, x, y, w, h, color, rx=3):
        self.out.append(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" style="fill:{color}"/>')

    def raw(self, s):
        self.out.append(s)

    def line(self, x1, y1, x2, y2, cls="pl-line", dashed=False):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.out.append(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="{cls}"{dash}/>')

    def arrow(self, x1, y1, x2, y2, dashed=False):
        self.line(x1, y1, x2, y2, dashed=dashed)
        a = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - 10 * math.cos(a - 0.55), y2 - 10 * math.sin(a - 0.55))
        p2 = (x2 - 10 * math.cos(a + 0.55), y2 - 10 * math.sin(a + 0.55))
        self.out.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{x2:g} {y2:g} L{p2[0]:.1f} {p2[1]:.1f}" class="pl-line"/>')

    def badge(self, x, y, k):
        self.out.append(f'<g class="dg-badge"><circle cx="{x:g}" cy="{y:g}" r="13"/>'
                        f'<text x="{x:g}" y="{y + 5:g}" text-anchor="middle">{k}</text></g>')

    def bubble(self, th, en, y=8):
        w = max(width(th), width(en)) + 56
        self.box(self.w / 2 - w / 2, y, w, 46, "nt-bubble", 23)
        self.both(self.w / 2, y + 30, th, en, "pl-text", "middle")

    def panel(self, x, y, w, h, cls, th, en, k=None):
        self.box(x, y, w, h, cls, 14)
        if k is None:
            self.both(x + 20, y + 32, th, en, "pl-label")
        else:
            self.badge(x + 32, y + 26, k)
            self.both(x + 54, y + 32, th, en, "pl-label")

    def person(self, x, y, color, r=5):
        """A small person (head and shoulders, about 14 × 22) filled with a weight group's colour."""
        self.out.append(f'<g style="fill:{color}"><circle cx="{x:g}" cy="{y - 6:g}" r="{r}"/>'
                        f'<path d="M{x - 7:g} {y + 12:g} Q{x - 7:g} {y + 1:g} {x:g} {y + 1:g} Q{x + 7:g} {y + 1:g} {x + 7:g} {y + 12:g} Z"/></g>')

    def stack(self, x, y, w, h, counts, labels=True):
        """One bar split by weight group; each piece shows its count when it is wide enough."""
        n = sum(counts)
        cx = x
        for k, c in enumerate(counts):
            if not c:
                continue
            pw = w * c / n
            self.fill(cx, y, pw, h, CLS[k], 2)
            if labels and pw > 26:
                self.raw(f'<text x="{cx + pw / 2:g}" y="{y + h / 2 + 6:g}" text-anchor="middle" class="pl-num">{c}</text>')
            cx += pw

    def legend(self, x, y):
        for k, (th, en) in enumerate(NAMES):
            self.fill(x, y - 13, 16, 16, CLS[k], 3)
            self.both(x + 22, y, th, en, "pl-note")
            x += 46 + max(width(th, 18), width(en, 18))

    def save(self, name, h, sized=False):
        size = f' width="{self.w}" height="{h}"' if sized else ""
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}"{size} class="diagram diagram-wide" role="img"><title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


# small drawing helpers shared by the lesson maps and the L11 card pictures
def circ(s, cx, cy, r, color, extra=""):
    s.raw(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" style="fill:{color}{extra}"/>')


def ring(s, cx, cy, r, cls):
    s.raw(f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" class="{cls}"/>')


def poly(s, pts, cls):
    s.raw(f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}" class="{cls}"/>')


def person(s, x, y, color, outline=False):
    style = "fill:none;stroke:var(--muted);stroke-width:1.5" if outline else f"fill:{color}"
    s.raw(f'<g style="{style}"><circle cx="{x:g}" cy="{y - 9:g}" r="7"/>'
          f'<path d="M{x - 10:g} {y + 16:g} Q{x - 10:g} {y + 1:g} {x:g} {y + 1:g} Q{x + 10:g} {y + 1:g} {x + 10:g} {y + 16:g} Z"/></g>')


def chip(s, x, y, w, h, label, cls="ml-cell", tcls="mp-c"):
    s.box(x, y, w, h, cls, 5)
    s.text(x + w / 2, y + h / 2 + 5, label, tcls, "middle")


def app_grid(s, apps, top=72, cols=3, tw=352, gap=12, th_=176):
    """Everyday apps that already use the lesson's idea. Each app: (icon, name th, en, does th, en, idea th, en).
    Returns the bottom y."""
    for k, app in enumerate(apps):
        em, nth, nen, dth, den, ith, ien = app[:7]
        why = app[7:9] if len(app) >= 9 else None   # optional: why there is no direct formula
        x, y = 10 + (k % cols) * (tw + gap), top + (k // cols) * (th_ + 14)
        s.box(x, y, tw, th_, "ml-cell", 14)
        s.raw(f'<circle cx="{x + 46}" cy="{y + 50}" r="34" style="fill:var(--tag-concept-bg)"/>')
        emoji_or_icon(s, em, x + 46, y + 50, 56)
        s.both(x + 90, y + 46, nth, nen, "mp-t")
        s.both(x + 90, y + 72, dth, den, "hk-desc")
        if why:
            s.both(x + 20, y + 108, why[0], why[1], "mp-acc")
        s.both(x + 20, y + 132 if why else y + 124, "จึงใช้" if why else "ทำงานแบบ", "so it uses" if why else "works like", "mp-s")
        w = max(width(ith, 16), width(ien, 16)) + 28
        cy = y + 140 if why else y + 134
        s.box(x + 20, cy, w, 30, "ml-cell-b", 15)
        s.both(x + 20 + w / 2, cy + 21, ith, ien, "mp-chip", "middle")
    return top + ((len(apps) - 1) // cols + 1) * (th_ + 14) - 14


def term_grid(s, terms, cols=4, tw=263, gap=12, th_=192, top=10):
    """Key terms, each with a small drawing on top: (name or (name th, en), draw(x, y, w, h) in a (tw − 20) × 84 box, line1 th, en,
    line2 th, en). Returns the bottom y."""
    for k, (name, draw, a_th, a_en, b_th, b_en) in enumerate(terms):
        x, y = 10 + (k % cols) * (tw + gap), top + (k // cols) * (th_ + 12)
        s.box(x, y, tw, th_, "ml-cell", 14)
        s.box(x + 10, y + 10, tw - 20, 84, "dg-xl-head", 10)
        draw(x + 10, y + 10, tw - 20, 84)
        if isinstance(name, tuple):
            s.both(x + 16, y + 122, name[0], name[1], "mp-t")
        else:
            s.text(x + 16, y + 122, name, "mp-t")
        s.both(x + 16, y + 150, a_th, a_en, "hk-desc")
        s.both(x + 16, y + 174, b_th, b_en, "hk-desc")
    return top + ((len(terms) - 1) // cols + 1) * (th_ + 12) - 12


ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
_embeds = [0]


def embed_svg(s, name, x, y, w, h):
    """Inline an art file from scripts/diagrams/assets (Open Peeps people, the Fluent robot; see assets/LICENSES.md) as
    a nested <svg> at (x, y), w × h. Every id gets a unique prefix so several copies can sit in one picture."""
    src = open(os.path.join(ASSETS, name), encoding="utf-8").read()
    src = re.sub(r"<metadata>.*?</metadata>", "", src, flags=re.S)
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = src[src.index(">", src.index("<svg")) + 1: src.rindex("</svg>")]
    _embeds[0] += 1
    p = f"e{_embeds[0]}-"
    body = re.sub(r'id="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', body)
    body = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{p}{m.group(1)})", body)
    body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{p}{m.group(1)}"', body)
    s.raw(f'<svg x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" viewBox="{vb}" aria-hidden="true">{body}</svg>')


def embed_png(s, name, x, y, w, h):
    """Inline a PNG from scripts/diagrams/assets as a base64 <image>, fitted into the w × h box and standing on its
    bottom edge (the AI-generated characters; see assets/LICENSES.md)."""
    import base64
    data = base64.b64encode(open(os.path.join(ASSETS, name), "rb").read()).decode()
    s.raw(f'<image x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" preserveAspectRatio="xMidYMax meet" '
          f'href="data:image/png;base64,{data}"/>')


def icon(s, name, cx, cy, size):
    """Draw generated icon assets/icon-<name>.png centred on (cx, cy), fitted into a size × size box. Use it in place of
    an emoji: emoji render differently on every computer and small; these share one style (see assets/LICENSES.md)."""
    import base64
    data = base64.b64encode(open(os.path.join(ASSETS, f"icon-{name}.png"), "rb").read()).decode()
    s.raw(f'<image x="{cx - size / 2:g}" y="{cy - size / 2:g}" width="{size:g}" height="{size:g}" '
          f'preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>')


# Emoji → generated icon (assets/icon-<name>.png). Pictures pass the emoji they used to show; one shared style replaces
# the system emoji, which look different (and small) on every computer.
EMOJI_ICON = {
    "🎵": "app-music", "📱": "app-feed", "🚨": "app-scam", "🔓": "app-faceunlock", "📷": "app-photos", "🌐": "app-translate",
    "💳": "app-bank", "🧞": "genie", "🟩": "tiles", "🎧": "headphones", "🍅": "tomato", "🦉": "owl", "🛡": "shield",
    "📩": "envelope", "📥": "envelope", "🐣": "chick", "🔍": "magnifier", "🔎": "magnifier", "🎯": "target", "⚖": "scale",
    "🌦": "weather", "🎰": "slot", "🗳": "ballot", "⭐": "stars", "📊": "poll", "🔀": "shuffle", "🎲": "dice",
    "🚦": "trafficlight", "👍": "thumbs", "🕺": "paddle", "🚩": "flag", "📋": "clipboard", "🔁": "loop", "🗑": "trash",
    "📜": "scroll", "📏": "ruler", "📈": "chartup", "🔑": "key", "🧠": "brain", "🔒": "padlock", "🧩": "puzzle",
    "👩‍🍳": "chef", "🍽": "plate", "🧊": "fridge", "☁": "cloud", "📁": "folder", "📄": "document", "✏": "pencil",
    "💻": "laptop", "🖥": "server", "👩‍💻": "user-laptop", "🧑‍💻": "coder", "👤": "profile", "📚": "books", "📝": "notepad",
    "💰": "moneybag", "💾": "chip", "🏢": "office", "🏪": "shop", "🛍": "shoppingbag", "🔢": "abacus", "✂": "scissors",
    "🎤": "microphone", "😊": "smile", "🚫": "noentry", "💬": "chat", "📅": "calendar",
}
PNG_FOR = {"🤖": "ai-robot.png", "😴": "cast-robot-sleep.png"}


def emoji_or_icon(s, em, cx, cy, size):
    """Draw the generated icon for an emoji centred on (cx, cy); fall back to the emoji itself if there is none."""
    key = em.replace("\ufe0f", "")
    if key.startswith("icon:"):
        icon(s, key[5:], cx, cy, size)
    elif key in EMOJI_ICON:
        icon(s, EMOJI_ICON[key], cx, cy, size)
    elif key in PNG_FOR:
        import base64
        data = base64.b64encode(open(os.path.join(ASSETS, PNG_FOR[key]), "rb").read()).decode()
        s.raw(f'<image x="{cx - size / 2:g}" y="{cy - size / 2:g}" width="{size:g}" height="{size:g}" '
              f'preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>')
    else:
        s.text(cx, cy + size * 0.35, em, "mp-emoji", "middle")


def icon_label(s, x, y, em, th, en, cls, size=24, gap=8):
    """A label that starts with an icon: the icon (for an emoji) at the start of the line, then the text. y is the text
    baseline. Returns nothing; the text starts at x + size + gap."""
    emoji_or_icon(s, em, x + size / 2, y - size * 0.32, size)
    s.both(x + size + gap, y, th, en, cls)


def icon_markup(em, cx, cy, size):
    """The <image> markup for an emoji's generated icon centred on (cx, cy), or None when there is no icon. For scripts
    whose Svg class keeps its own `out` list (the nlp-basic and nlp figure scripts)."""
    import base64
    key = em.replace("️", "")
    name = (f"icon-{key[5:]}.png" if key.startswith("icon:") else
            f"icon-{EMOJI_ICON[key]}.png" if key in EMOJI_ICON else PNG_FOR.get(key))
    if not name:
        return None
    data = base64.b64encode(open(os.path.join(ASSETS, name), "rb").read()).decode()
    return (f'<image x="{cx - size / 2:g}" y="{cy - size / 2:g}" width="{size:g}" height="{size:g}" '
            f'preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>')


def put_icon(s, em, x, y, cls, anchor="middle", font=30):
    """Drop-in for s.text(x, y, emoji, cls, anchor): the generated icon where one exists (sized from the emoji's font
    size), else the emoji itself."""
    cx = x if anchor == "middle" else x + font * 0.55
    mk = icon_markup(em, cx, y - font * 0.36, font * 1.45)
    if mk:
        s.out.append(mk)
    else:
        s.text(x, y, em, cls, anchor)


def both_icon(s, x, y, th, en, cls, anchor="start", size=24):
    """s.both() for a label that starts with an emoji ("📚 1. Training"): the emoji becomes its generated icon at the
    start of the line and the text moves right. Labels without a known leading emoji are drawn unchanged."""
    import re as _re
    m = _re.match(r"^(\S+)\s+", th)
    em = m.group(1) if m else ""
    mk = icon_markup(em, 0, 0, size) if em else None
    if not mk or anchor != "start":
        s.both(x, y, th, en, cls, anchor)
        return
    s.out.append(icon_markup(em, x + size / 2, y - size * 0.34, size))
    s.both(x + size + 8, y, th[m.end():], en[len(em):].lstrip() if en.startswith(em) else en, cls, anchor)
