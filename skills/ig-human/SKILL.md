---
name: ig-human
description: "Revise Instagram copy for natural voice using local Romanian and English style checks. Use for /ig-human, $ig-human or Instagram copy humanization; not AI authorship detection."
---

# ig-human

Read [shared Codex operation](../ig-reel/references/codex.md) before using this workflow. Invoke with `$ig-human`; `/ig-human` is a textual alias, subject to the client UI.


## Workflow

1. Preserve facts, author voice, deliberate typography, quotations and legitimate technical terms. Read known voice instructions. Use `slop-en.json` for English or `slop-ro.json` for Romanian; specify `--lexicon` explicitly for ambiguous unaccented Romanian. The default lexicon combines RO/EN editorial checks.
2. Run `python3 <skill-dir>/humanize.py <draft> -o <clean> --report`. Default mode cleans selected accidental control/spacing characters and reports lexical/structural suggestions; it preserves emoji joiners, typography and paragraph breaks. `--apply-lexical` and `--normalize-typography` are opt-in editing modes, not required quality steps. Review any automatic replacement for meaning.
3. Rewrite useful suggestions manually. Do not remove words solely because a list calls them AI-like. Avoid changing quotations or URLs. For Romanian, keep diacritics and natural syntax; do not reward English contractions.
4. Run `python3 <skill-dir>/detect.py <draft> <clean> --json`. This is a **style panel**, not an AI detector. Five heuristic checks cover sentence variation, specificity, stock phrases, accidental formatting and phrasing. Unsupported checks in short text are N/A; INSUFFICIENT_DATA is acceptable.
5. Compare what improved and why. Revise at most twice for the panel; editorial judgement and accurate meaning take precedence over a PASS label. Typography/invisible characters are not proof of AI authorship; no claim of watermark removal, detector evasion or guaranteed originality.

## Deliver

Clean copy plus a short change explanation and actual before/after style results when requested or material. Keep instrumentation out of publication copy. Do not apply this skill globally to unrelated writing merely because it exists.
