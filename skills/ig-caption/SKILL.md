---
name: ig-caption
description: "Write and lint Instagram captions with an approximate 125-character preview, search terms and one CTA. Use for /ig-caption, $ig-caption or Instagram caption requests."
---

# ig-caption

Read [shared Codex operation](../ig-reel/references/codex.md) before using this workflow. Invoke with `$ig-caption`; `/ig-caption` is a textual alias, subject to the client UI.


## Workflow

1. Infer Job A (video carries the hook; caption adds context/CTA) or Job B (caption carries the idea). Ask only when the distinction is unresolved and material.
2. Draft in the user's voice: strong first line, short readable body, one CTA when appropriate, search phrases used naturally, relevant hashtags or none. Read `caption.py --help` for configurable defaults.
3. Apply `$ig-human`, then run `python3 <skill-dir>/caption.py <caption-file> --keywords "termen unu,termen doi" --truncate 125 --json`. RO/EN CTAs, Unicode hashtags and diacritics are supported. Use the user's known keywords; do not force an extra question for them.
4. Resolve actual errors and discuss material warnings. Do not fabricate numerical specificity merely to satisfy the checker. The preview is a rough 125-character slice, not an exact simulation of the current feed. Verify current platform limits when making factual claims; helpers expose override flags.

## Deliver

Copy-ready caption; approximate visible preview; character, hashtag and detected CTA counts; keyword coverage; checker verdict. Include descriptive alt text for photos/carousels when source visuals are available. URLs may be included if the user wants them, but do not promise they are clickable. No publishing action.
