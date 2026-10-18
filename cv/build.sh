#!/bin/sh
# Print cv/cv.html to public/Jakapun CV.pdf with headless Chrome (fonts load from Google Fonts).
# Chrome's own log lines (certificate, display, allocator) are harmless on macOS, so they are hidden.
cd "$(dirname "$0")/.." || exit 1
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --virtual-time-budget=10000 --log-level=3 \
  --print-to-pdf="public/Jakapun CV.pdf" "file://$PWD/cv/cv.html" 2>/dev/null
if [ -s "public/Jakapun CV.pdf" ]; then echo "✓ wrote public/Jakapun CV.pdf"; else echo "✗ the PDF was not written"; exit 1; fi
