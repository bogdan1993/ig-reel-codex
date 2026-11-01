---
name: ig-reel
description: "Create Instagram Reel scripts with three scored hooks from 26 formulas, screen text and a timed beat sheet. Use for /ig-reel, $ig-reel or an Instagram Reel script request."
---

# ig-reel

Read [shared Codex operation](references/codex.md) before using this workflow. Invoke with `$ig-reel`; `/ig-reel` is a textual alias, subject to the client UI.


## Workflow

1. Read relevant voice, swipe and recent draft log state. Use one specific idea and only substantiated facts.
2. Read `hooks.json`: preserve the 26 original IDs and formula names. Each formula also has a Romanian template/example and match pattern. Choose three distinct formulas that fit the idea and write a spoken hook plus a separate on-screen hook for each.
3. Write spoken hooks to a UTF-8 file, one per line. Run `python3 <skill-dir>/hookscore.py <hooks-file> --json`. Show all three scores and the weakest properties. Scores guide editing; they do not predict a winner.
4. Develop the best justified hook into the requested length (working default 15–45 seconds). Structure: hook, stake, one idea per beat, payoff, one CTA. A natural echo of the opening can support a loop; do not force it.
5. Write the script as one spoken beat per line. Run `python3 <skill-dir>/beats.py <script-file> --target 30 --wpm 165 --json`, adjusting target and speaking rate to the request. Estimate durations, do not claim measured speech. Fix long beats by shortening speech or specifying a visual cut.
6. Apply `$ig-human` to the copy without flattening the writer's voice. Re-run timing after text edits. Stop after two score-driven revisions.

## Deliver

- Three hook options with formula IDs, spoken and screen versions, scores and short rationale.
- A copy-ready spoken script, on-screen cards (usually no more than six words), estimated timecodes and shot/cut notes.
- Actual helper results and limitations; hand off to `$ig-caption` when requested.
- If saving state, record date, formula, hook and `status: draft` in `.instagram/log.md`. No approval prompt is needed merely to finish the requested draft.
