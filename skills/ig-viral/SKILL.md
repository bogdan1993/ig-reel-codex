---
name: ig-viral
description: "Research Instagram Reel examples in a niche, rank against each account median and save a sourced swipe file. Use for /ig-viral, $ig-viral or Instagram niche research."
---

# ig-viral

Read [shared Codex operation](../ig-reel/references/codex.md) before using this workflow. Invoke with `$ig-viral`; `/ig-viral` is a textual alias, subject to the client UI.


## Workflow

1. Determine niche, audience and research window from context. Use supplied accounts or propose a relevant bounded sample (working target 6–12 accounts, up to 12 recent comparable Reels per account). Do not block read-only research on approval of an account list.
2. Read accessible source posts through connectors or browsing. Record account, URL, observation date, published date, views, hook, first screen card, length and CTA. Record followers as context only. Missing fields stay missing.
3. Compute each account's median from actual comparable recent Reel view counts. State window, sample size and whether the target Reel is included. Use complete integer counts, not `12k`/`1.2M`, in the TSV. Do not eyeball or invent a median. Do not mix paid and organic posts silently.
4. Create UTF-8 TSV with at least `account`, `median`, `views`, `hook`; retain `url` and `observed_at` columns. Run `python3 <skill-dir>/swipe.py <captured.tsv> --json --out <state-dir>/swipe.md`.
5. Rank only rows with a positive measured median by `views / median`. Missing/zero medians are unranked, never replaced by follower counts. The script recognizes original English and added Romanian formulas and leaves uncertain hooks unclassified. Review those manually; keep manual classifications separate from script output.
6. Report overrepresented formulas, structural differences, unclassified examples and data coverage with source links. Label small-sample findings tentative; 3x is a working outlier threshold, not a universal law. Do not infer causation from view counts.
7. Produce three original hook ideas grounded in the user's own facts and offer `$ig-reel` production details within the requested scope.

If Instagram access is blocked, continue with available public sources or user data. A Shorts comparison must be explicitly labelled as YouTube evidence and never silently pooled with Instagram medians. Do not build a feed crawler. Save provenance alongside the swipe file.
