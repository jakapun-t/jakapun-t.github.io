"""Step-by-step screen pictures for nlp-basic lesson 14 (S15 GitHub, S16 deploy) and the
"design from a reference" check picture (S19). Each step picture is a simplified window with the real
button labels, and rust rings with numbers in the order students click.

    python3 scripts/diagrams/l14_steps.py            (from course/)

The reference picture embeds the real screenshot images/l14-ref-result.png (made by
scripts/l14_apps/shoot.mjs from the app Gemini wrote, scripts/l14_apps/reference/app.py).
"""
import base64
import io
import os
from html import escape



class Svg:
    def __init__(self, w, title):
        self.w, self.title, self.out = w, title, []

    def add(self, s):
        self.out.append(s)

    def both(self, x, y, th, en, cls, anchor="start"):
        self.add(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="th">{escape(th)}</text>')
        self.add(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}" data-only="en" lang="en">{escape(en)}</text>')

    def text(self, x, y, s, cls, anchor="start"):
        self.add(f'<text x="{x:g}" y="{y:g}" class="{cls}" text-anchor="{anchor}">{escape(s)}</text>')

    def box(self, x, y, w, h, cls, rx=12):
        self.add(f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}"/>')

    def arrow(self, x1, y1, x2, y2, cls="pl-line"):
        self.add(f'<path d="M{x1:g} {y1:g} L{x2:g} {y2:g}" class="{cls}"/>')
        d = 8 if x2 > x1 else -8
        self.add(f'<path d="M{x2 - d:g} {y2 - 6:g} L{x2:g} {y2:g} L{x2 - d:g} {y2 + 6:g}" class="{cls}"/>')

    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram diagram-wide" role="img">'
               f'<title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")

OUT = "courses/nlp-basic/images"
W = 520


class Pic(Svg):
    def save(self, name, h):
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {h}" class="diagram" role="img">'
               f'<title>{escape(self.title)}</title>', *self.out, "</svg>"]
        open(os.path.join(OUT, name), "w", encoding="utf-8").write("\n".join(svg) + "\n")
        print("wrote", name, f"{self.w}x{h}")


def browser(s, x, y, w, h, url):
    """A browser window: title strip with three dots and the address."""
    s.box(x, y, w, h, "ks-bar", 12)
    s.add(f'<path d="M{x} {y + 34} H{x + w}" stroke="var(--card-border)" stroke-width="1.5"/>')
    for k in range(3):
        s.add(f'<circle cx="{x + 16 + k * 14}" cy="{y + 17}" r="4.5" fill="var(--card-border)"/>')
    s.box(x + 62, y + 7, w - 76, 20, "sc-url", 10)
    s.text(x + 74, y + 22, url, "sc-url-t")


def vscode(s, x, y, w, h, side_w=150):
    """A VS Code window: dark activity bar on the left, a light side panel, and the editor area."""
    s.box(x, y, w, h, "ks-bar", 12)
    s.add(f'<path d="M{x + 12} {y} H{x + 42} V{y + h} H{x + 12} A12 12 0 0 1 {x} {y + h - 12} V{y + 12} A12 12 0 0 1 {x + 12} {y}Z" class="sc-vs-bar"/>')
    s.add(f'<path d="M{x + 42 + side_w} {y} V{y + h}" stroke="var(--card-border)" stroke-width="1.5"/>')


def act_icon(s, x, y, kind):
    """Activity-bar icons, drawn in light strokes: files, search, source control, accounts."""
    c = 'fill="none" stroke="#e8e3d8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "files":
        s.add(f'<path d="M{x - 7} {y - 9} H{x + 3} L{x + 8} {y - 4} V{y + 9} H{x - 7} Z" {c}/>')
    elif kind == "search":
        s.add(f'<circle cx="{x - 2}" cy="{y - 2}" r="6" {c}/><path d="M{x + 3} {y + 3} L{x + 8} {y + 8}" {c}/>')
    elif kind == "git":
        s.add(f'<circle cx="{x - 5}" cy="{y - 7}" r="3" {c}/><circle cx="{x - 5}" cy="{y + 8}" r="3" {c}/>'
              f'<circle cx="{x + 6}" cy="{y - 3}" r="3" {c}/><path d="M{x - 5} {y - 4} V{y + 5} M{x + 6} {y} C{x + 6} {y + 5} {x - 5} {y + 2} {x - 5} {y + 5}" {c}/>')
    elif kind == "account":
        s.add(f'<circle cx="{x}" cy="{y - 4}" r="5" {c}/><path d="M{x - 9} {y + 9} C{x - 7} {y + 1} {x + 7} {y + 1} {x + 9} {y + 9}" {c}/>')


def btn(s, x, y, w, label, kind="plain", h=30):
    cls, tcls = {"plain": ("ks-btn", "ks-btn-t"), "main": ("ks-btn-main", "ks-btn-main-t"),
                 "green": ("ks-check", "ks-check-t")}[kind]
    s.box(x, y, w, h, cls, 8)
    s.text(x + w / 2, y + h / 2 + 5.5, label, tcls, "middle")


def field(s, x, y, w, label, value, h=28):
    s.text(x, y - 6, label, "sc-label")
    s.box(x, y, w, h, "ks-bar", 6)
    s.text(x + 10, y + 19, value, "ks-mono")


def ring(s, x, y, w, h, n, side="left"):
    """A rust ring around what to click, with its number badge."""
    s.box(x - 4, y - 4, w + 8, h + 8, "sc-ring", 10)
    bx = x - 4 if side == "left" else x + w + 4
    s.add(f'<circle cx="{bx:g}" cy="{y - 4:g}" r="11" class="pl-dot"/>')
    s.text(bx, y + 1, str(n), "pl-num", "middle")


def note(s, x, y, th, en, anchor="start"):
    s.both(x, y, th, en, "in-sub", anchor)


# ================================================================ design from a reference: check the result (S19)
from PIL import Image  # noqa: E402

im = Image.open(os.path.join(OUT, "l14-ref-result.png")).convert("RGB")
iw = 900
im = im.resize((iw, round(im.height * iw / im.width)), Image.LANCZOS)
buf = io.BytesIO()
im.save(buf, "PNG", optimize=True)
ih = im.height
data = base64.b64encode(buf.getvalue()).decode()
k = iw / 2000  # the screenshot was 2000 px wide
s = Svg(iw, "The app Gemini wrote from the sketch, a real screenshot. The layout matches the sketch: the title, the box that "
            "opens on click, three metric cards, Chart and Table tabs and the footer. Two things are wrong: Reviews shows 1 "
            "instead of 5, because the code reads a key review_count that analyze_text does not return, and the Words card "
            "says abc where the sketch had an icon.")
s.add(f'<image x="0" y="0" width="{iw}" height="{ih}" href="data:image/png;base64,{data}"/>')
s.add(f'<rect x="0.75" y="0.75" width="{iw - 1.5}" height="{ih - 1.5}" rx="10" fill="none" stroke="var(--card-border)" stroke-width="1.5"/>')
# 1: Reviews = 1 (callout in the empty left margin, its number inside it)
rx, ry = 290 * k, 600 * k
s.box(rx, ry, 70 * k, 90 * k, "sc-ring", 8)
s.box(6, ry - 4, 116, 62, "sc-callout", 8)
s.add(f'<circle cx="22" cy="{ry + 16:g}" r="10" fill="#fff"/>')
s.text(22, ry + 21, "1", "sc-badge-t", "middle")
s.both(38, ry + 22, "ควรเป็น 5", "should be 5", "sc-callout-t")
s.both(14, ry + 46, "(มี 5 รีวิว)", "(5 reviews)", "sc-callout-s")
s.add(f'<path d="M122 {ry + 26:g} L{rx - 4:g} {ry + 26:g}" class="sc-callout-line"/>')
# 2: abc instead of the icon
ax, ay = 770 * k, 545 * k
s.box(ax, ay, 66 * k, 44 * k, "sc-ring", 6)
s.box(ax + 64, ay - 50, 214, 34, "sc-callout", 8)
s.add(f'<circle cx="{ax + 80:g}" cy="{ay - 33:g}" r="10" fill="#fff"/>')
s.text(ax + 80, ay - 28, "2", "sc-badge-t", "middle")
s.both(ax + 96, ay - 27, "ในภาพร่างเป็นไอคอน", "the sketch had an icon", "sc-callout-t")
s.add(f'<path d="M{ax + 76:g} {ay - 16:g} L{ax + 24:g} {ay - 2:g}" class="sc-callout-line"/>')
# ✓ layout
s.box(iw - 250, ih - 112, 232, 70, "sc-ok", 10)
s.both(iw - 236, ih - 82, "✓ layout ตรงกับภาพร่าง", "✓ the layout matches", "sc-ok-t")
s.both(iw - 236, ih - 56, "หัวเรื่อง กล่องพับ 3 การ์ด แท็บ", "title, folding box, 3 cards, tabs", "in-sub")
s.save("l14-ref-check.svg", ih)


# ================================================================ design from a reference: what we send (projector copy, S19)
sk = Image.open(os.path.join(OUT, "l14-ref-sketch.png")).convert("RGB")
sk = sk.resize((600, 450), Image.LANCZOS)
buf = io.BytesIO()
sk.save(buf, "PNG", optimize=True)
skd = base64.b64encode(buf.getvalue()).decode()
s = Svg(1000, "What we send to the AI: a short prompt, with the sketch attached. Rebuild app.py to follow the attached sketch: "
              "header, folding reviews box, 3 metric cards, Chart and Table tabs and the footer; keep nlp_logic.py unchanged; "
              "built-in components only.")
s.box(10, 60, 450, 300, "ks-term", 14)
s.both(34, 98, "prompt", "prompt", "sc-callout-t")
for i, ln in enumerate(["Rebuild app.py to follow the", "attached sketch: header, folding", "reviews box, 3 metric cards,",
                        "Chart / Table tabs, footer.", "Keep nlp_logic.py unchanged;", "built-in components only."]):
    s.text(34, 140 + i * 30, ln, "sc-prompt-t")
s.box(34, 316, 170, 30, "sc-clip", 15)
s.text(50, 337, "📎 sketch.png", "sc-clip-t")
s.arrow(522, 210, 470, 210)
s.box(530, 10, 460, 345, "ks-bar", 12)
s.add(f'<image x="536" y="16" width="448" height="336" href="data:image/png;base64,{skd}"/>')
s.both(760, 385, "ภาพที่แนบ (reference)", "the attached picture (reference)", "in-sub", "middle")
s.save("l14-ref-ask.svg", 395)

# ================================================================ GitHub, step by step (S15)
H = 250

# 1. install Git
s = Pic(W, "Step 1, install Git. Mac: the first time Git is needed, a window asks to install the command line developer tools; "
           "click Install. Windows: on git-scm.com click Download for Windows, run the installer and keep clicking Next.")
s.text(10, 22, "Mac", "pl-label")
s.box(10, 36, 245, 190, "ks-bar", 12)
s.text(28, 66, "The “git” command requires the", "sc-small")
s.text(28, 86, "command line developer tools.", "sc-small")
s.text(28, 106, "Would you like to install", "sc-small")
s.text(28, 126, "the tools now?", "sc-small")
btn(s, 22, 172, 76, "Get Xcode")
btn(s, 104, 172, 68, "Not Now")
btn(s, 178, 172, 62, "Install", "main")
ring(s, 178, 172, 62, 30, 1, "right")
s.text(275, 22, "Windows", "pl-label")
browser(s, 275, 36, 235, 190, "git-scm.com")
s.text(295, 96, "git", "sc-logo")
btn(s, 295, 128, 196, "Download for Windows", "main")
ring(s, 295, 128, 196, 30, 1, "right")
note(s, 295, 186, "รันไฟล์ที่ได้ กด Next จนจบ", "run it, click Next to the end")
note(s, 295, 206, "แล้วเปิด VS Code ใหม่", "then reopen VS Code")
s.save("l14-gh-1.svg", 236)

# 2. sign up
s = Pic(W, "Step 2, sign up at github.com/signup: fill in your email, a password and a username, click Continue, then type the "
           "code GitHub sends to your email.")
browser(s, 10, 10, 500, 230, "github.com/signup")
s.text(40, 74, "Sign up for GitHub", "sc-h")
field(s, 40, 102, 270, "Email*", "you@email.com")
field(s, 40, 152, 270, "Password*", "••••••••••••")
field(s, 40, 202, 270, "Username*", "your-name")
ring(s, 40, 102, 270, 128, 1, "right")
btn(s, 340, 202, 130, "Continue", "green", 28)
ring(s, 340, 202, 130, 28, 2, "right")
note(s, 340, 120, "แล้วกรอกรหัสที่", "then type the code")
note(s, 340, 140, "ส่งมาทางอีเมล", "sent to your email")
s.save("l14-gh-2.svg", 250)

# 3. sign in from VS Code
s = Pic(W, "Step 3, sign in from VS Code: click the Accounts icon at the bottom of the left bar, choose Sign in with GitHub, "
           "then click Authorize in the browser that opens.")
vscode(s, 10, 10, 270, 230, side_w=0)
for k, kind in enumerate(["files", "search", "git"]):
    act_icon(s, 26, 40 + k * 38, kind)
act_icon(s, 26, 214, "account")
ring(s, 14, 200, 24, 26, 1)
s.box(52, 150, 216, 40, "sc-menu", 8)
s.text(64, 175, "Sign in with GitHub", "sc-small")
ring(s, 52, 150, 216, 40, 2, "right")
s.add('<path d="M40 210 L52 182" class="pl-line"/>')
browser(s, 296, 10, 214, 230, "github.com/login")
s.text(403, 80, "Authorize", "sc-h2", "middle")
s.text(403, 102, "Visual Studio Code", "sc-h2", "middle")
btn(s, 320, 140, 166, "Authorize", "green")
ring(s, 320, 140, 166, 30, 3, "right")
note(s, 403, 206, "แล้วกลับมาที่ VS Code", "then back to VS Code", "middle")
s.save("l14-gh-3.svg", 250)

# 4. create a repository
s = Pic(W, "Step 4, create a repository on github.com/new: name it my-streamlit-app, choose Public, switch on Add README, then "
           "click Create repository.")
browser(s, 10, 10, 500, 240, "github.com/new")
s.text(34, 70, "Create a new repository", "sc-h")
field(s, 34, 104, 230, "Repository name*", "my-streamlit-app")
ring(s, 34, 104, 230, 28, 1, "right")
s.add('<circle cx="44" cy="160" r="7" fill="var(--card)" stroke="var(--ink)" stroke-width="1.5"/><circle cx="44" cy="160" r="3.5" fill="var(--ink)"/>')
s.text(58, 165, "Public", "sc-small")
s.add('<circle cx="124" cy="160" r="7" fill="var(--card)" stroke="var(--ink)" stroke-width="1.5"/>')
s.text(138, 165, "Private", "sc-small")
ring(s, 34, 150, 66, 20, 2, "right")
s.box(34, 186, 30, 16, "ks-btn-main", 8)
s.add('<circle cx="56" cy="194" r="6" fill="#fff"/>')
s.text(74, 199, "Add README", "sc-small")
ring(s, 34, 184, 140, 20, 3, "right")
btn(s, 330, 206, 160, "Create repository", "green", 28)
ring(s, 330, 206, 160, 28, 4, "right")
s.save("l14-gh-4.svg", 260)

# 5. clone
s = Pic(W, "Step 5, clone in VS Code: open Source Control on the left bar, click Clone Repository, choose Clone from GitHub, pick "
           "you/my-streamlit-app, then choose a folder on your computer and Open.")
vscode(s, 10, 10, 500, 230, side_w=150)
for k, kind in enumerate(["files", "search", "git"]):
    act_icon(s, 26, 40 + k * 38, kind)
ring(s, 14, 102, 24, 26, 1)
s.text(62, 40, "SOURCE CONTROL", "sc-tiny")
btn(s, 60, 60, 124, "Clone Repository", "main", 28)
ring(s, 60, 60, 124, 28, 2, "right")
s.box(220, 30, 276, 120, "sc-menu", 8)
s.box(232, 38, 252, 22, "ks-bar", 4)
s.text(242, 54, "repository URL or pick a source", "sc-tiny")
s.text(240, 98, "Clone from GitHub", "sc-small")
ring(s, 232, 82, 160, 24, 3, "right")
s.text(240, 134, "you/my-streamlit-app", "ks-mono")
ring(s, 232, 118, 190, 24, 4, "right")
note(s, 222, 186, "แล้วเลือกโฟลเดอร์ในเครื่อง → Open", "then pick a folder on your computer → Open")
s.save("l14-gh-5.svg", 250)

# 6. add your files
s = Pic(W, "Step 6, add your files: copy app.py, nlp_logic.py and requirements.txt (for example from the zip you downloaded) "
           "into the my-streamlit-app folder you cloned, next to its README.md.")
FILES = ["app.py", "nlp_logic.py", "requirements.txt"]
s.box(10, 30, 200, 180, "ks-bar", 12)
s.text(26, 60, "thai-review-app/", "ks-mono")
note(s, 26, 22, "ไฟล์ของเรา (จาก zip)", "your files (from the zip)")
for k, f in enumerate(FILES):
    s.box(26, 78 + k * 40, 168, 30, "sc-file-new", 6)
    s.text(38, 98 + k * 40, f, "ks-mono")
s.arrow(218, 120, 290, 120)
s.both(254, 108, "คัดลอก", "copy", "gt-verb", "middle")
s.box(298, 30, 212, 200, "ks-bar", 12)
s.text(314, 60, "my-streamlit-app/", "ks-mono")
note(s, 298, 22, "โฟลเดอร์ที่ clone มา", "the folder you cloned")
s.box(314, 76, 180, 28, "ks-bar", 6)
s.text(326, 95, "README.md", "ks-mono")
for k, f in enumerate(FILES):
    s.box(314, 114 + k * 36, 180, 28, "sc-file-new", 6)
    s.text(326, 133 + k * 36, f, "ks-mono")
ring(s, 314, 114, 180, 100, 1, "right")
s.save("l14-gh-6.svg", 240)

# 7. commit, then sync
s = Pic(W, "Step 7, in Source Control: type a message such as add first app, click Commit (answer Yes if VS Code asks to "
           "stage all changes), then click Sync Changes.")
vscode(s, 10, 10, 500, 240, side_w=250)
for k, kind in enumerate(["files", "search", "git"]):
    act_icon(s, 26, 40 + k * 38, kind)
s.text(62, 40, "SOURCE CONTROL", "sc-tiny")
s.box(60, 52, 220, 28, "ks-bar", 6)
s.text(70, 71, "add first app", "ks-mono")
ring(s, 60, 52, 220, 28, 1, "right")
btn(s, 60, 90, 220, "✓ Commit", "main", 28)
ring(s, 60, 90, 220, 28, 2, "right")
s.text(62, 142, "Changes  3", "sc-tiny")
for k, f in enumerate(FILES):
    s.text(70, 164 + k * 22, f, "sc-small")
    s.text(268, 164 + k * 22, "U", "sc-u", "end")
s.box(300, 40, 200, 96, "sc-menu", 8)
s.text(312, 64, "Stage all changes and", "sc-tiny")
s.text(312, 80, "commit them directly?", "sc-tiny")
btn(s, 312, 96, 60, "Yes", "main", 26)
ring(s, 312, 96, 60, 26, 3, "right")
btn(s, 300, 196, 200, "↻ Sync Changes 1↑", "main", 28)
ring(s, 300, 196, 200, 28, 4, "right")
s.save("l14-gh-7.svg", 260)

# 8. check on github.com
s = Pic(W, "Step 8, check: refresh your repository page on github.com. You should see your commit message add first app and "
           "the files README.md, app.py, nlp_logic.py and requirements.txt.")
browser(s, 10, 10, 500, 230, "github.com/you/my-streamlit-app")
s.text(34, 66, "you / my-streamlit-app", "sc-h2")
s.box(232, 52, 52, 20, "ks-bar", 10)
s.text(258, 66, "Public", "sc-tiny", "middle")
s.box(34, 84, 452, 26, "sc-menu", 6)
s.text(46, 102, "your-name   add first app", "sc-small")
s.text(476, 102, "✓", "sc-ok-t", "end")
for k, f in enumerate(["README.md"] + FILES):
    s.text(46, 134 + k * 24, "📄 " + f, "sc-small")
    if f in ("app.py", "requirements.txt"):
        s.text(300, 134 + k * 24, "add first app", "in-sub")
ring(s, 40, 142, 170, 66, 1, "right")
s.save("l14-gh-8.svg", 250)

# ================================================================ deploy on Streamlit Community Cloud (S16)

# 1. continue with GitHub
s = Pic(W, "Deploy step 1: open share.streamlit.io, click Continue with GitHub, then click Authorize on GitHub so Streamlit can "
           "read your repositories.")
browser(s, 10, 10, 250, 220, "share.streamlit.io")
s.text(135, 80, "Streamlit", "sc-h", "middle")
s.text(135, 102, "Community Cloud", "sc-small", "middle")
btn(s, 30, 140, 210, "Continue with GitHub", "main")
ring(s, 30, 140, 210, 30, 1, "right")
browser(s, 274, 10, 236, 220, "github.com/login")
s.text(392, 82, "Authorize Streamlit", "sc-h2", "middle")
btn(s, 300, 140, 184, "Authorize", "green")
ring(s, 300, 140, 184, 30, 2, "right")
s.save("l14-dp-1.svg", 240)

# 2. create app
s = Pic(W, "Deploy step 2: in your workspace click Create app at the top right, then choose Yup, I have an app.")
browser(s, 10, 10, 500, 220, "share.streamlit.io")
s.text(34, 66, "My apps", "sc-h2")
btn(s, 384, 48, 110, "Create app", "main", 28)
ring(s, 384, 48, 110, 28, 1, "right")
s.box(150, 96, 330, 118, "sc-menu", 10)
s.text(170, 124, "Do you already have an app?", "sc-small")
btn(s, 170, 140, 290, "Yup, I have an app", "main", 28)
ring(s, 170, 140, 290, 28, 2, "right")
btn(s, 170, 176, 290, "Nope, create one from a template", "plain", 28)
s.save("l14-dp-2.svg", 240)

# 3. repository, branch, main file
s = Pic(W, "Deploy step 3: fill in Repository you/my-streamlit-app, Branch main and Main file path app.py.")
browser(s, 10, 10, 500, 240, "share.streamlit.io/deploy")
s.text(34, 66, "Deploy an app", "sc-h2")
field(s, 34, 96, 300, "Repository", "you/my-streamlit-app")
ring(s, 34, 96, 300, 28, 1, "right")
field(s, 34, 148, 300, "Branch", "main")
ring(s, 34, 148, 300, 28, 2, "right")
field(s, 34, 200, 300, "Main file path", "app.py")
ring(s, 34, 200, 300, 28, 3, "right")
s.save("l14-dp-3.svg", 260)

# 4. secrets
s = Pic(W, "Deploy step 4, only if the app uses an API key: click Advanced settings, type GEMINI_API_KEY = your key in the "
           "Secrets box, then Save. The key never goes in your code or on GitHub.")
browser(s, 10, 10, 500, 250, "share.streamlit.io/deploy")
s.text(34, 66, "Advanced settings", "sc-link")
ring(s, 34, 50, 140, 22, 1, "right")
s.box(34, 86, 452, 150, "sc-menu", 10)
s.text(52, 112, "Secrets", "sc-small")
s.box(52, 122, 416, 52, "ks-term", 6)
s.text(64, 154, 'GEMINI_API_KEY = "AIza…"', "ks-term-t")
ring(s, 52, 122, 416, 52, 2, "right")
btn(s, 388, 194, 80, "Save", "main", 28)
ring(s, 388, 194, 80, 28, 3, "left")
s.save("l14-dp-4.svg", 270)

# 5. deploy and wait
s = Pic(W, "Deploy step 5: click Deploy and wait a few minutes while Streamlit installs the libraries in requirements.txt "
           "and starts your app.")
browser(s, 10, 10, 500, 230, "share.streamlit.io/deploy")
btn(s, 34, 52, 120, "Deploy", "main")
ring(s, 34, 52, 120, 30, 1, "right")
s.box(34, 100, 452, 120, "ks-term", 8)
for k, ln in enumerate(["Installing requirements…", "  streamlit, pandas, pythainlp", "Your app is in the oven", "✓ Your app is live!"]):
    s.text(50, 126 + k * 24, ln, "ks-term-ok" if ln.startswith("✓") else "ks-term-t")
note(s, 300, 72, "รอ 2–5 นาที", "wait 2–5 minutes")
s.save("l14-dp-5.svg", 250)

# 6. share the link
s = Pic(W, "Deploy step 6: your app is online at an address ending in .streamlit.app. Copy the link and send it to anyone.")
browser(s, 10, 10, 500, 230, "you-my-streamlit-app.streamlit.app")
ring(s, 72, 17, 260, 20, 1, "right")
s.text(34, 70, "Thai review analyzer", "sc-h2")
for k, (lab, v) in enumerate([("Reviews", "5"), ("Words", "25"), ("Unique", "17")]):
    s.box(34 + k * 150, 86, 138, 64, "ks-bar", 8)
    s.text(48 + k * 150, 108, lab, "sc-tiny")
    s.text(48 + k * 150, 138, v, "sc-h")
for k, w in enumerate([300, 220, 150, 150, 150]):
    s.box(110, 160 + k * 12, w * 0.9, 8, "sc-bar", 3)
note(s, 260, 232, "ส่งลิงก์นี้ให้ใครก็เปิดได้", "send this link to anyone", "middle")
s.save("l14-dp-6.svg", 250)
