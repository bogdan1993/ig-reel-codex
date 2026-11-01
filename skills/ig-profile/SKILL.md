---
name: ig-profile
description: "Score an Instagram profile with a 12-part 100-point rubric and prioritize rewrites. Use for /ig-profile, $ig-profile or Instagram bio and profile audits."
---

# ig-profile

Read [shared Codex operation](../ig-reel/references/codex.md) before using this workflow. Invoke with `$ig-profile`; `/ig-profile` is a textual alias, subject to the client UI.


## Workflow

1. Read accessible profile data or supplied screenshots/text: name, handle, bio, destination, highlights, pinned posts, first nine covers, activity and visible contact options. Mark unseen items unknown.
2. Read `rubric.json`: 12 criteria whose weights total 100. Score each observed item with evidence, show the table and coverage. For unseen items use N/A and report observed points / observed maximum; do not assign zero to missing evidence or extrapolate a complete score.
3. Prioritize the largest supported point losses. Rewrite the searchable name (three options), bio, clear offer/link label, pinned post roles and highlight names as relevant. Recommend grid/visual changes with actual examples.
4. Treat rubric character counts and platform features as working defaults; verify current official limits if exact compliance is requested. Never invent proof, claims or destinations.
5. Apply `$ig-human`. Distinguish points a text revision could improve from visual/activity improvements not yet implemented. A proposed score is an estimate, not the live profile's new score.

## Deliver

12-row scored table, evidence/unknowns, prioritized copy-ready rewrites, visual/action recommendations, and a clearly labelled possible improvement. Do not edit the live account.
