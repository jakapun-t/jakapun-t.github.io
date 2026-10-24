"""Cut an AI-generated character sheet into transparent PNG characters for the course diagrams.

    course/.venv/bin/python scripts/diagrams/tools/cut_sheet.py sheet.png scripts/diagrams/assets name1,name2,...

The sheet: characters in one row on a pure-white background with white gaps between them (ask the image model for
exactly that). Each character is cropped, the white background reachable from the edges is cleared, large enclosed
white areas (e.g. between a raised arm and the head) are cleared too while small ones (eye whites) stay, stray bits of
neighbours are dropped, and the result is scaled to 300 px high and saved as a 128-colour PNG (~10 KB).
Embed the files with stats_svg.embed_png(); record each new file in assets/LICENSES.md.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage


def clean(path):
        im = Image.open(path).convert("RGBA")
        a = np.array(im)
        rgb, alpha = a[..., :3].astype(int), a[..., 3]
        near_white = (rgb.min(axis=2) > 232) & (alpha > 0)
        lab, n = ndimage.label(near_white)
        sizes = ndimage.sum(near_white, lab, range(1, n + 1))
        for i, sz in enumerate(sizes, 1):
            if sz > 350:
                a[lab == i, 3] = 0
        opaque = a[..., 3] > 0
        lab, n = ndimage.label(opaque)
        if n > 1:
            sizes = ndimage.sum(opaque, lab, range(1, n + 1))
            big = sizes.max()
            for i, sz in enumerate(sizes, 1):
                if sz < 0.05 * big:
                    a[lab == i, 3] = 0
        out = Image.fromarray(a, "RGBA")
        bbox = out.getbbox()
        out = out.crop(bbox)
        out.quantize(colors=128, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE).save(path, optimize=True)
        print(path.rsplit("/", 1)[1], out.size, "removed white areas >350px")



src, out_dir = sys.argv[1], sys.argv[2]
names = sys.argv[3].split(",")
im = Image.open(src).convert("RGB")
W, H = im.size
px = im.load()
white = lambda c: min(c) > 238
cols = [any(not white(px[x, y]) for y in range(0, H, 2)) for x in range(W)]
segs, start = [], None
for x, v in enumerate(cols + [False]):
    if v and start is None:
        start = x
    if not v and start is not None:
        if x - start > 2:     # keep thin pieces (an icon made of separate columns); merging below joins them
            segs.append((start, x))
        start = None
# an icon with two parts (a lamp and its smoke, two hands) makes two segments: merge the closest pair until the count fits
while len(segs) > len(names):
    i = min(range(len(segs) - 1), key=lambda k: segs[k + 1][0] - segs[k][1])
    segs[i:i + 2] = [(segs[i][0], segs[i + 1][1])]
# two characters touching make one segment: split the widest at its emptiest column (middle 60%) until the count fits
ink = [sum(not white(px[x, y]) for y in range(0, H, 2)) for x in range(W)]
while len(segs) < len(names):
    i = max(range(len(segs)), key=lambda k: segs[k][1] - segs[k][0])
    a, b = segs[i]
    lo, hi = a + (b - a) // 5, b - (b - a) // 5
    cut = min(range(lo, hi), key=lambda x: ink[x])
    segs[i:i + 1] = [(a, cut), (cut + 1, b)]
print("segments:", segs)
assert len(segs) == len(names), (len(segs), len(names))
for (x0, x1), name in zip(segs, names):
    rows = [y for y in range(H) if any(not white(px[x, y]) for x in range(x0, x1, 2))]
    y0, y1 = rows[0], rows[-1] + 1
    pad = 6
    crop = im.crop((max(0, x0 - pad), max(0, y0 - pad), min(W, x1 + pad), min(H, y1 + pad))).convert("RGBA")
    # clear the white background reachable from the edges (white inside the character, like eyes, stays)
    cw, ch = crop.size
    for seed in [(0, 0), (cw - 1, 0), (0, ch - 1), (cw - 1, ch - 1)] + [(x, 0) for x in range(0, cw, 10)] + [(0, y) for y in range(0, ch, 10)] + [(cw - 1, y) for y in range(0, ch, 10)]:
        if crop.getpixel(seed)[3] and min(crop.getpixel(seed)[:3]) > 230:
            ImageDraw.floodfill(crop, seed, (255, 255, 255, 0), thresh=40)
    k = 300 / ch
    crop = crop.resize((round(cw * k), 300), Image.LANCZOS)
    q = crop.quantize(colors=96, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    path = f"{out_dir}/{name}.png"
    q.save(path, optimize=True)
    clean(path)
    print(name, path)
