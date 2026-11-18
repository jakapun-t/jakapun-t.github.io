"""Send the reference sketch + stage-1 app.py to Gemini, as a student would, and save its real answer.
    ../../../.venv/bin/python ask_ai.py      (reads GOOGLE_API_KEY from course/.env; never prints it)
"""
import pathlib, re
from google import genai
from google.genai import types

HERE = pathlib.Path(__file__).parent
env = dict(l.split("=", 1) for l in (HERE / "../../../.env").read_text().splitlines() if "=" in l and not l.startswith("#"))
client = genai.Client(api_key=env["GOOGLE_API_KEY"].strip().strip('"'))

PROMPT = open(HERE / "prompt.txt").read()
app = open(HERE / "../../../courses/nlp-basic/projects/l14-thai-review-app/app.py").read()
resp = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[types.Part.from_bytes(data=(HERE / "sketch.png").read_bytes(), mime_type="image/png"),
              PROMPT + "\n\nMy current app.py:\n```python\n" + app + "```"])
text = resp.text
(HERE / "response.md").write_text(text)
code = re.search(r"```python\n(.*?)```", text, re.S)
(HERE / "app.py").write_text(code.group(1) if code else text)
print(text)
