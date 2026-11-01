---
name: ig-reel
description: Create Instagram Reel scripts with three scored hooks from 26 formulas, spoken copy, screen text and estimated beat timing. Supports Romanian and English. Use for $ig-reel, /ig-reel or Instagram Reel script requests.
---

# Instagram Reel for Codex

## Operation

- Native invocation is `$ig-reel`. `/ig-reel` is a textual alias when the message reaches the agent, not a registered native slash command.
- This skill is self-contained. Resolve all helpers and JSON files relative to this SKILL.md directory. Python 3.10+ and its standard library suffice; no API key or Instagram credentials are needed.
- Follow the user's language and voice. Use voice instructions and samples already available; an optional external personal-voice skill can supply style, but is not required. Do not request an initial corpus when enough context exists. Ask only for missing facts that materially affect the script.
- Keep user state in `.instagram/` inside the active project or an explicitly selected directory. Relevant optional files are voice.md, swipe.md and log.md. Scratch files belong in work/; requested deliverables follow workspace rules. Never copy private voice samples, drafts or account data into this skill repository.
- These helpers prepare content. They do not publish, message, follow, access accounts or schedule outreach. A script request authorizes the local draft, not an external action.
- Never invent personal stories, clients, numbers, testimonials, deadlines or results. Formula examples are illustrative, not user evidence. Label hypothetical examples clearly.
- All scores are uncalibrated editorial heuristics, not predictions of reach, truth, provenance or AI authorship. Short text may have insufficient data. Do not add fake specificity or distort the writer's voice to increase a score.
- Verify current official Instagram rules when stating current limits. Timing, safe margins, lengths and card sizes in this workflow are working defaults. This skill creates a script, not a rendered video.

## Reel workflow

1. Read relevant supplied voice and niche context. Develop one specific central idea grounded in known facts. A 30–45 second script is a reasonable starting point; honor explicit length requests.
2. Read `hooks.json`. Keep the original 26 formula IDs/names. Each has an original English template and a Romanian template/example. Choose three distinct formulas that fit; draft a spoken hook and a separate short screen hook for each.
3. Save spoken hooks as one UTF-8 line each. Run `python3 <skill-dir>/hookscore.py <hooks.txt> --json`. Compare actual scores and weakest properties. No score can identify a guaranteed winner; choose the strongest truthful hook editorially. Show all three scored alternatives unless the user asks for final copy only or a supplied voice workflow calls for a single clean deliverable.
4. Write a continuous spoken script: relevant opening, context/stake, example or mechanism, payoff, and an ending that closes the argument. A CTA or repeated opening is optional; never force either. Avoid slogan lists and unsupported leaps in reasoning.
5. Save one spoken beat per line and run `python3 <skill-dir>/beats.py <script.txt> --target 40 --wpm 165 --json`, adjusting rate and target to context. These timings estimate speech, not measure the person's actual voice. Shorten long lines or make a production note if technical planning is requested. The tool's abstraction/loop warnings are suggestions, not hard requirements.
6. Run `python3 <skill-dir>/humanize.py <script.txt> -o <clean.txt> --report`. It preserves typography, paragraph breaks, URLs and emoji joiners by default and reports lexical/structural suggestions. Review suggestions for context; lexical replacements and typography normalization are opt-in. For Romanian-only review add `--lexicon <skill-dir>/slop-ro.json` (English: slop-en.json; default: bilingual).
7. Rewrite useful suggestions manually, then run `python3 <skill-dir>/detect.py <script.txt> <clean.txt> --json`. Despite its historical filename, this is a five-check **style panel**, not an AI detector. N/A or INSUFFICIENT_DATA is valid for short copy. At most two score-driven revisions; accurate meaning and voice prevail. Re-run timing after text edits.

## Delivery

- Deliver one usable Reel unless more were requested. Default: three short scored hook alternatives, chosen spoken script, estimated duration and separate screen text/timecodes. Include filming/editing notes only if requested; if a personal voice workflow asks for clean copy, keep the technical detail internal.
- If the user requests only the script, deliver only the text to say. Do not expose internal analysis or label sentences HOOK/VALUE/CTA.
- Report actual helper outputs if presenting a score. Exit 1 can mean editorial REVIEW, not a crash. Do not claim successful checks that were not run.
- If saving a log, record the date, formula ID, hook and `status: draft`. Approval of a draft is not proof it has been published.

## Local helper interfaces

```text
python3 hookscore.py hooks.txt --json
python3 hookscore.py --hook "Your spoken opening" --json
python3 beats.py script.txt --target 40 --wpm 165 --json
python3 humanize.py script.txt -o clean.txt --report
python3 detect.py script.txt clean.txt --json
```

See README.md for installation, examples, attribution and limitations.
