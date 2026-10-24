# Art used in the course diagrams

All of it was generated for this course with ElevenLabs (model gpt-image-2.5-sunburst) on 2026-10-21, as sheets of
characters or icons in one row on white, then cut out with `tools/cut_sheet.py` (transparent PNG, 128 colours, about
10 KB each). `stats_svg.embed_png()`, `icon()`, `emoji_or_icon()`, `icon_markup()` and `put_icon()` inline them (base64)
into the generated SVG pictures, so the published pages carry no separate copy.

## Characters
- `ai-over-calm`, `ai-over-worried`, `ai-normal-puzzled`, `ai-normal-happy`, `ai-robot`: the first sheet, L11-S12.
  Overweight people wear amber (#c08a2e), Normal-weight people green (#4f8a5f).
- `cast-normal-man` (L11-S03 row 1), `cast-obese` (L12-S05), `cast-yawn` (L14-S08 lazy annotator), `cast-ra-a/b/c`
  (the three research assistants, L14 map, S03, S05), `cast-robot-sleep` (the lazy model, L11-S11): a second sheet made
  with the first as a style reference.

## Icons: `icon-*.png`
- 52 icons from 9 sheets, one shared flat style (rust, amber, green, blue, cream). `stats_svg.EMOJI_ICON` maps the emoji
  a picture used to show to its icon; an emoji with no icon (⏳, ✓, ✗) stays as text.
- Kept as emoji on purpose: emoji inside mock app screens (buttons, address bars), file trees (📁 my-project/), message
  text, and emoji that are part of the data (the ☕😍 in the text-cleaning example).

`stats_svg.embed_svg()` still exists for SVG art (it prefixes ids so copies don't clash) but no file uses it now.

## Lesson 14 (nlp, agents), 2026-10-24
Two more sheets in the same flow (gpt-image-2.5-sunburst, 1K): characters made with the first character sheet as a style
reference (433 credits), icons without a reference (190 credits).
- Characters `ag-*`: `ag-student-ask`, `ag-student-happy` (the student asking the running question), `ag-customer-upset`
  (shop customer with a broken parcel), `ag-staff-ok` (help-desk staff approving), `ag-robot-think`, `ag-robot-tools`,
  `ag-robot-plan` (re-cut with a border flood fill so the clipboard keeps its white paper), `ag-robot-mini` (a sub-agent).
- Icons: `icon-clock`, `icon-plug` (MCP), `icon-tools`, `icon-parcel`, `icon-truck`, `icon-pause`, `icon-save`, `icon-stopwatch`.
