#!/bin/bash
# Daily job (launchd, 07:00): publish every course, and push only when a lesson page was added or removed
# (a lesson reached its release date). Publishing re-encrypts every page, so plain re-encryptions are thrown
# away instead of committed. Stops without touching anything if the repo is not in a clean, expected state.
# Log: ~/Library/Logs/course-daily-publish.log · job: ~/Library/LaunchAgents/com.jakapun.course-daily-publish.plist

set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
REPO="/Users/jakapuntachaiya/Documents/chula/Project/My Github Profile"
COURSES="nlp-basic nlp stats-dh"
LOG="$HOME/Library/Logs/course-daily-publish.log"
exec >>"$LOG" 2>&1
echo "=== $(date '+%Y-%m-%d %H:%M:%S')"

notify() { osascript -e "display notification \"$1\" with title \"Course pages\"" >/dev/null 2>&1 || true; }
fail() { echo "STOP: $1"; notify "Daily publish stopped: $1"; exit 1; }

cd "$REPO" || fail "repo folder not found"
[ "$(git branch --show-current)" = "dev" ] || fail "not on branch dev"
git diff --quiet -- public/courses && git diff --cached --quiet -- public/courses \
  || fail "public/courses has uncommitted changes"
[ -z "$(git status --porcelain -- public/courses)" ] || fail "public/courses has untracked files"
git fetch -q origin || fail "git fetch failed (offline?)"
[ "$(git rev-parse dev)" = "$(git rev-parse origin/dev)" ] || fail "local dev and origin/dev differ"

TMP="$(mktemp)"
for c in $COURSES; do
  npm --prefix course run -s publish -- "$c" >"$TMP" 2>&1
  status=$?
  grep -v -i "password" "$TMP"
  [ $status -eq 0 ] || { rm -f "$TMP"; git checkout -q -- public/courses; fail "publish $c failed"; }
done
rm -f "$TMP"

CHANGED="$(git status --porcelain -- public/courses | grep -E '^(\?\?|A |D | D)' || true)"
if [ -z "$CHANGED" ]; then
  git checkout -q -- public/courses          # only re-encryptions: keep the published files as they were
  echo "No lesson opened or closed today; nothing pushed."
  exit 0
fi

echo "Changed lesson pages:"; echo "$CHANGED"
NAMES="$(echo "$CHANGED" | awk '{print $2}' | xargs -n1 basename | sed 's/\.html$//' | paste -sd ', ' -)"
if [ "${DRY_RUN:-0}" = "1" ]; then
  git clean -fdq -- public/courses; git checkout -q -- public/courses
  echo "DRY RUN: would publish $NAMES; nothing committed."
  exit 0
fi
git add public/courses || fail "git add failed"
git commit -q -m "Publish lessons that reached their release date: $NAMES" -- public/courses || fail "commit failed (guard?)"
git push -q origin dev:main dev || fail "push failed"
echo "Pushed $(git rev-parse --short HEAD): $NAMES"
notify "Published: $NAMES"
