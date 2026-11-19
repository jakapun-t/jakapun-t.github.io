#!/bin/bash
# Real screenshots of the lesson 14 layout examples (card S06): one app, ?ex=<key> picks the example.
#   bash scripts/l14_apps/layouts/shoot.sh   (from course/)
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../../../courses/nlp-basic/images"
PY="$HERE/../../../.venv/bin/python"
PORT=8611
(cd "$HERE" && "$PY" -m streamlit run app.py --server.port $PORT --server.headless true \
   --browser.gatherUsageStats false --theme.base light >/dev/null 2>&1 & echo $! > /tmp/l14_layouts.pid)
for i in $(seq 1 40); do curl -s "http://localhost:$PORT/_stcore/health" | grep -q ok && break; sleep 0.5; done
for ex in stack sidebar columns tabs expander expander_open ratio cards; do
  node "$HERE/../shoot.mjs" "http://localhost:$PORT/?ex=$ex" "$OUT/l14-lay-$ex.png" 1000 640
done
node "$HERE/../shoot.mjs" "http://localhost:$PORT/?ex=centered" "$OUT/l14-lay-centered.png" 1280 520
node "$HERE/../shoot.mjs" "http://localhost:$PORT/?ex=wide" "$OUT/l14-lay-wide.png" 1280 520
node "$HERE/../shoot.mjs" "http://localhost:$PORT/?ex=all" "$OUT/l14-lay-all.png" 1280 760
kill "$(cat /tmp/l14_layouts.pid)" 2>/dev/null || true
cd "$HERE/../../.." && "$PY" scripts/l14_apps/trim.py courses/nlp-basic/images/l14-lay-*.png
