"""Frames for the layout stepper in nlp-basic lesson 14, card S06: the code of one layout example on the left (the
layout lines highlighted) and a real screenshot of that code running on the right.

    bash scripts/l14_apps/layouts/shoot.sh                          # the screenshots (real Streamlit runs)
    course/.venv/bin/python scripts/diagrams/l14_layout_steps.py courses/nlp-basic/images

The code text comes from scripts/l14_apps/layouts/examples.py, the same code the app runs.
"""

import base64
import io
import os
import sys
from html import escape

from PIL import Image, ImageChops

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "l14_apps", "layouts"))
from examples import EXAMPLES  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "courses/nlp-basic/images"
W, H = 1000, 372
CODE_W, IMG_X, IMG_W, IMG_H = 444, 460, 540, 318
LAYOUT_WORDS = ("st.sidebar", "st.columns", "st.tabs", "with tab", "st.expander", "container(border", "with left",
                "with right", "set_page_config", "c1.", "c2.", "c3.", "c1, c2")


def crop(im, keep_width=False):
    """Drop Streamlit's top bar (Deploy, ⋮) and the empty margins around the app's content; keep a sidebar."""
    im = im.crop((0, 110, im.width, im.height))
    side = sum(im.getpixel((6, im.height // 2))) < 3 * 248          # a grey sidebar down the left edge
    x0 = 0
    if side:
        x0 = next(x for x in range(im.width) if sum(im.getpixel((x, im.height // 2))) >= 3 * 252)
    main = im.crop((x0, 0, im.width, im.height))
    box = ImageChops.difference(main, Image.new("RGB", main.size, (255, 255, 255))).point(lambda v: 255 if v > 12 else 0).getbbox()
    if not box:
        return im
    m = 36
    if keep_width:                                                  # narrow vs wide: the margins are the point
        return im.crop((0, max(0, box[1] - m), im.width, min(im.height, box[3] + m)))
    top = 0 if side else max(0, box[1] - m)                         # a sidebar's heading sits above the main content
    left = 0 if side else max(0, box[0] - m)
    return im.crop((left, top, min(im.width, x0 + box[2] + m), min(im.height, box[3] + m)))


def png_data(name, width=1240):
    im = crop(Image.open(os.path.join(OUT, name)).convert("RGB"), keep_width=name in ("l14-lay-centered.png", "l14-lay-wide.png"))
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=82, optimize=True)
    return im.size, base64.b64encode(buf.getvalue()).decode()


def image(out, name, x, y, w, h, frame=True):
    (iw, ih), data = png_data(name)
    s = min(w / iw, h / ih)
    dw, dh = iw * s, ih * s
    out.append(f'<image x="{x:g}" y="{y:g}" width="{dw:.1f}" height="{dh:.1f}" href="data:image/jpeg;base64,{data}"/>')
    if frame:
        out.append(f'<rect x="{x:g}" y="{y:g}" width="{dw:.1f}" height="{dh:.1f}" rx="6" style="fill:none;stroke:var(--card-border);stroke-width:1.4"/>')
    return dh


def both(out, x, y, th, en, cls, anchor="start"):
    out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="th">{escape(th)}</text>')
    out.append(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="en" lang="en">{escape(en)}</text>')


def frame(name, title, code_key, shots, caption=None):
    """shots: list of (png name, label_th, label_en); one shot fills the right side, two sit one above the other."""
    out = []
    out.append(f'<rect x="0" y="0" width="{CODE_W}" height="{H}" rx="12" class="st-page"/>')
    out.append(f'<text x="16" y="26" class="in-sub">app.py</text>')
    lines = EXAMPLES[code_key].split("\n") if code_key else []
    for k, line in enumerate(lines):
        hl = any(w in line for w in LAYOUT_WORDS)
        y = 54 + k * 25
        if hl:
            out.append(f'<rect x="8" y="{y - 17}" width="{CODE_W - 16}" height="23" rx="5" style="fill:var(--tag-example-bg)"/>')
        out.append(f'<text x="16" y="{y}" class="{"in-code-acc" if hl else "in-code"}" xml:space="preserve">{escape(line)}</text>')
    if not lines:
        both(out, CODE_W / 2, H / 2, "โค้ดเต็มอยู่ในช่องโค้ดใต้ภาพนี้", "the full code is in the code cell below", "pl-note", "middle")
    if len(shots) == 1:
        png, lth, len_ = shots[0]
        both(out, IMG_X, 22, lth, len_, "in-h")
        image(out, png, IMG_X, 34, IMG_W, IMG_H)
    else:
        y = 0
        for png, lth, len_ in shots:
            both(out, IMG_X, y + 20, lth, len_, "in-h")
            dh = image(out, png, IMG_X, y + 30, IMG_W, (H - 70) / 2)
            y += dh + 40
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="diagram diagram-wide" role="img">'
           f'<title>{escape(title)}</title>' + "\n".join(out) + "</svg>")
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(svg + "\n")
    print("wrote", name, f"{os.path.getsize(os.path.join(OUT, name)) // 1024} KB")


REAL = ("ผลลัพธ์จริง", "The real result")
frame("l14-lay-1.svg", "By default everything stacks top to bottom in code order: title, text, metric, button.", "stack",
      [("l14-lay-stack.png", *REAL)])
frame("l14-lay-2.svg", "with st.sidebar: puts the header and slider in the grey panel on the left.", "sidebar",
      [("l14-lay-sidebar.png", *REAL)])
frame("l14-lay-3.svg", "st.columns(3) makes three columns side by side; c1.metric puts a metric in the first.", "columns",
      [("l14-lay-columns.png", *REAL)])
frame("l14-lay-4.svg", "st.tabs makes two tabs; only the open tab's content shows.", "tabs",
      [("l14-lay-tabs.png", *REAL)])
frame("l14-lay-5.svg", "st.expander hides content in a box that opens on a click: closed, then opened.", "expander",
      [("l14-lay-expander.png", "ตอนแรก: ปิดอยู่", "At first: closed"),
       ("l14-lay-expander_open.png", "หลังกดเปิด", "After a click: open")])
frame("l14-lay-6.svg", "st.columns([2, 1]): the left column is twice as wide as the right one.", "ratio",
      [("l14-lay-ratio.png", *REAL)])
frame("l14-lay-7.svg", "container(border=True) inside each column makes two bordered cards side by side.", "cards",
      [("l14-lay-cards.png", *REAL)])
frame("l14-lay-8.svg", "Without set_page_config the page is a narrow column; layout='wide' uses the whole screen width.", "wide",
      [("l14-lay-centered.png", "ไม่ใส่บรรทัดแรก: แคบ ตรงกลาง", "Without the first line: narrow, centred"),
       ("l14-lay-wide.png", 'ใส่ layout="wide": เต็มจอ', 'With layout="wide": full width')])
frame("l14-lay-9.svg", "Everything together: wide page, sidebar, three metrics, a 2:1 split with tabs on the left and a bordered box with an expander on the right.",
      None, [("l14-lay-all.png", *REAL)])
