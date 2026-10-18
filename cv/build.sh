#!/bin/sh
# Print cv/cv.html to public/Jakapun CV.pdf with headless Chrome (fonts load from Google Fonts).
cd "$(dirname "$0")/.." || exit 1
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --virtual-time-budget=10000 \
  --print-to-pdf="public/Jakapun CV.pdf" "file://$PWD/cv/cv.html"
