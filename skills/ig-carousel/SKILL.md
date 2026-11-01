---
name: ig-carousel
description: "Create Instagram carousel copy and rendered 1080x1350 slide files. Use for /ig-carousel, $ig-carousel or Instagram swipe post requests."
---

# ig-carousel

Read [shared Codex operation](../ig-reel/references/codex.md) before using this workflow. Invoke with `$ig-carousel`; `/ig-carousel` is a textual alias, subject to the client UI.


## Workflow

1. Use a sequence-shaped idea that benefits from rereading. Read available brand/design instructions and voice context. Use the requested slide count; a practical default is 6–10.
2. Build: cover hook (about six words), standalone stake/second cover, one idea per slide, a usable recap, one CTA. Keep body copy short (about 25 words per slide) and number slides. Use the real supplied handle; omit it or flag it as missing rather than inventing one.
3. Revise copy with `$ig-human`; prepare caption with `$ig-caption` and alt text for each slide. If the user requests a finished carousel, proceed through rendering without a separate copy-approval gate unless explicitly requested.
4. Render each slide at **1080x1350**, PNG or JPEG. Use a supported local renderer, browser screenshot workflow or design connector. Editable HTML/CSS is suitable; use a font with Romanian glyphs, generous margins (~120 px), strong contrast and readable phone-scale type (working minimum 32 px). Do not deliver only a PDF when upload-ready slide images were requested.
5. Inspect rendered slides for crop, overflow, diacritics and legibility. Verify dimensions and expected slide count. Supply editable source, ordered image files and optionally a ZIP. If rendering is blocked, explicitly label the partial result and state the remaining work.

## Deliver

Slide-by-slide copy, actual upload-ready images, editable source, caption and alt text. State rendered file paths and what was verified. No upload to Instagram.
