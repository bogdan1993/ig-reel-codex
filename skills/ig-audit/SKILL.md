---
name: ig-audit
description: "Audit Instagram post metrics by account median, sends per reach and follows per reach. Use for /ig-audit, $ig-audit or Instagram Insights analysis."
---

# ig-audit

Read [shared Codex operation](../ig-reel/references/codex.md) before using this workflow. Invoke with `$ig-audit`; `/ig-audit` is a textual alias, subject to the client UI.


## Workflow

1. Read available Insights/exported post data and relevant draft/published log state. Prefer a comparable window of about 30 posts; report actual sample size, period, post age and mixed-format limitations. Missing metrics are N/A, not zero.
2. Prepare CSV with `id`, `views`, `reach`, `sends`, `shares`, `follows`, `account`, `format` where available. Use complete nonnegative numbers; blanks mean unknown. `sends` means DM sends if separately available; `shares` is total shares and must not silently be labelled sends.
3. Run `python3 <skill-dir>/audit.py <posts.csv> --json`. It computes medians per account+format, outlier=view/median, sends/reach, shares/reach and follows/reach. Undefined ratios (zero/missing denominator) stay N/A; missing counts do not become zero. Compare recent cohorts cautiously if post ages differ.
4. Show rankings by outlier and sends per reach separately; if only shares are available, label that ranking shares per reach. Include baseline, denominator and cohort count. For retention, use actual starts/still-watching-at-3s values when provided and distinguish average watch time from completion.
5. Compare top/bottom groups for formula, opening, format, length, theme, non-follower reach and profile conversion. Describe associations as hypotheses; low views alone do not prove a hook problem, and low follows alone do not prove a profile problem. Avoid causal claims from a few posts.
6. Recommend what to continue, stop and test next with evidence and confidence; save findings to `<state-dir>/audit.md` for `$ig-plan` and `$ig-viral` when requested.

## Deliver

Period/sample/coverage, metrics table with workings, top/bottom rankings, supported patterns and a short next-test plan. A draft log does not prove publication or actual performance.
