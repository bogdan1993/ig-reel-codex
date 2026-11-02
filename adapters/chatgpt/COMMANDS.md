# Instagram Toolkit — command library

Citește numai secțiunile necesare cererii. Workflow-urile sunt activate de instrucțiunile proiectului, nu prin executarea aliasurilor.

## Runtime and resource mapping

Shared rules and JSON resources are in REFERENCE.md. The paths in the workflows below refer to paths preserved inside helpers.zip. `<skill-dir>` means the extracted `skills/<command>` directory, not a directory on the user's computer. Read other command modes from this library. With no Python execution, explicitly deliver qualitative results without claiming script scores. The optional `skills/ig-plan/assets/voice.md` is a voice-profile template; use the profile supplied by the user or draft a provisional one without inventing personal facts.

# /IG-AUDIT

# ig-audit


## Workflow

1. Read available Insights/exported post data and relevant draft/published log state. Prefer a comparable window of about 30 posts; report actual sample size, period, post age and mixed-format limitations. Missing metrics are N/A, not zero.
2. Prepare CSV with `id`, `views`, `reach`, `sends`, `shares`, `follows`, `account`, `format` where available. Use complete nonnegative numbers; blanks mean unknown. `sends` means DM sends if separately available; `shares` is total shares and must not silently be labelled sends.
3. Run `python3 <skill-dir>/audit.py <posts.csv> --json`. It computes medians per account+format, outlier=view/median, sends/reach, shares/reach and follows/reach. Undefined ratios (zero/missing denominator) stay N/A; missing counts do not become zero. Compare recent cohorts cautiously if post ages differ.
4. Show rankings by outlier and sends per reach separately; if only shares are available, label that ranking shares per reach. Include baseline, denominator and cohort count. For retention, use actual starts/still-watching-at-3s values when provided and distinguish average watch time from completion.
5. Compare top/bottom groups for formula, opening, format, length, theme, non-follower reach and profile conversion. Describe associations as hypotheses; low views alone do not prove a hook problem, and low follows alone do not prove a profile problem. Avoid causal claims from a few posts.
6. Recommend what to continue, stop and test next with evidence and confidence; save findings to `<state-dir>/audit.md` for `/IG-PLAN` and `/IG-VIRAL` when requested.

## Deliver

Period/sample/coverage, metrics table with workings, top/bottom rankings, supported patterns and a short next-test plan. A draft log does not prove publication or actual performance.

# /IG-CAPTION

# ig-caption


## Workflow

1. Infer Job A (video carries the hook; caption adds context/CTA) or Job B (caption carries the idea). Ask only when the distinction is unresolved and material.
2. Draft in the user's voice: strong first line, short readable body, one CTA when appropriate, search phrases used naturally, relevant hashtags or none. Read `caption.py --help` for configurable defaults.
3. Apply `/IG-HUMAN`, then run `python3 <skill-dir>/caption.py <caption-file> --keywords "termen unu,termen doi" --truncate 125 --json`. RO/EN CTAs, Unicode hashtags and diacritics are supported. Use the user's known keywords; do not force an extra question for them.
4. Resolve actual errors and discuss material warnings. Do not fabricate numerical specificity merely to satisfy the checker. The preview is a rough 125-character slice, not an exact simulation of the current feed. Verify current platform limits when making factual claims; helpers expose override flags.

## Deliver

Copy-ready caption; approximate visible preview; character, hashtag and detected CTA counts; keyword coverage; checker verdict. Include descriptive alt text for photos/carousels when source visuals are available. URLs may be included if the user wants them, but do not promise they are clickable. No publishing action.

# /IG-CAROUSEL

# ig-carousel


## Workflow

1. Use a sequence-shaped idea that benefits from rereading. Read available brand/design instructions and voice context. Use the requested slide count; a practical default is 6–10.
2. Build: cover hook (about six words), standalone stake/second cover, one idea per slide, a usable recap, one CTA. Keep body copy short (about 25 words per slide) and number slides. Use the real supplied handle; omit it or flag it as missing rather than inventing one.
3. Revise copy with `/IG-HUMAN`; prepare caption with `/IG-CAPTION` and alt text for each slide. If the user requests a finished carousel, proceed through rendering without a separate copy-approval gate unless explicitly requested.
4. Render each slide at **1080x1350**, PNG or JPEG. Use a supported local renderer, browser screenshot workflow or design connector. Editable HTML/CSS is suitable; use a font with Romanian glyphs, generous margins (~120 px), strong contrast and readable phone-scale type (working minimum 32 px). Do not deliver only a PDF when upload-ready slide images were requested.
5. Inspect rendered slides for crop, overflow, diacritics and legibility. Verify dimensions and expected slide count. Supply editable source, ordered image files and optionally a ZIP. If rendering is blocked, explicitly label the partial result and state the remaining work.

## Deliver

Slide-by-slide copy, actual upload-ready images, editable source, caption and alt text. State rendered file paths and what was verified. No upload to Instagram.

# /IG-COMMENT

# ig-comment


## Workflow

Read the actual post from supplied text, a screenshot or accessible URL before drafting. Choose **two different types** that fit, not a generic compliment:

1. Add a supported datum.
2. Add a missing case/condition.
3. Respectful disagreement grounded in the claim.
4. Extend one specific line.
5. Ask the actual unanswered question.
6. Give a real, supplied personal example.
7. Correct a verified factual error.
8. Reframe the same facts.
9. A relevant one-liner (usually under ten words).

Use 1–3 sentences, one point, specific to this post; no invented personal experience, automatic agreement, emoji-only reply or unsolicited pitch. Apply `/IG-HUMAN` with judgement for short text. Return two labelled copy-ready options and one recommendation. For a batch, return the requested count and label each source account/post. If recording state, mark comments as **drafted**, not posted. No sending, liking or account changes.

# /IG-DM

# ig-dm


## Workflow

1. Use known recipient, actual interaction/trigger, resource and intended outcome. Ask only for consequential missing facts. Do not fabricate familiarity, a watched post or a mutual connection.
2. Choose keyword delivery, warm first message or specific collaboration pitch. For a keyword, deliver the resource/link **first**, followed by brief use instructions and an optional question. Do not add a qualification gate before the promised resource.
3. Warm first message: 2–4 sentences referencing the real interaction, something useful, one small ask. Collaboration: observed work, specific proposal, their benefit, the actual request. Avoid fake praise and unnecessary funnels.
4. Include **at most two follow-ups**: suggested +4 days with genuinely new value, +10 days to close the loop. These are draft dates relative to a known first-send date; if unknown, keep relative offsets. Stop on refusal/opt-out; do not write persistence around a clear no.
5. Apply `/IG-HUMAN`, preserve the user's facts and count characters for each message. No automatic outreach or sending; discussing an approved keyword-response tool does not authorize configuring it.

## Deliver

Copy-ready first message and up to two relevant follow-ups, with character counts, timing and stop condition. If the recipient already declined, explain that no follow-up is appropriate.

# /IG-HUMAN

# ig-human


## Workflow

1. Preserve facts, author voice, deliberate typography, quotations and legitimate technical terms. Read known voice instructions. Use `slop-en.json` for English or `slop-ro.json` for Romanian; specify `--lexicon` explicitly for ambiguous unaccented Romanian. The default lexicon combines RO/EN editorial checks.
2. Run `python3 <skill-dir>/humanize.py <draft> -o <clean> --report`. Default mode cleans selected accidental control/spacing characters and reports lexical/structural suggestions; it preserves emoji joiners, typography and paragraph breaks. `--apply-lexical` and `--normalize-typography` are opt-in editing modes, not required quality steps. Review any automatic replacement for meaning.
3. Rewrite useful suggestions manually. Do not remove words solely because a list calls them AI-like. Avoid changing quotations or URLs. For Romanian, keep diacritics and natural syntax; do not reward English contractions.
4. Run `python3 <skill-dir>/detect.py <draft> <clean> --json`. This is a **style panel**, not an AI detector. Five heuristic checks cover sentence variation, specificity, stock phrases, accidental formatting and phrasing. Unsupported checks in short text are N/A; INSUFFICIENT_DATA is acceptable.
5. Compare what improved and why. Revise at most twice for the panel; editorial judgement and accurate meaning take precedence over a PASS label. Typography/invisible characters are not proof of AI authorship; no claim of watermark removal, detector evasion or guaranteed originality.

## Deliver

Clean copy plus a short change explanation and actual before/after style results when requested or material. Keep instrumentation out of publication copy. Do not apply this skill globally to unrelated writing merely because it exists.

# /IG-PLAN

# ig-plan


## Workflow

1. Read relevant voice.md, swipe.md, log.md and audit.md from the state directory. Use known offer, audience, themes, capacity and current events. Ask one concise question only for consequential missing inputs; otherwise use labelled assumptions.
2. Build a feasible seven-day plan using the requested cadence. A working starting point is 4–5 feed posts plus Stories; do not claim three Reels are compulsory or that only Reels reach non-followers. Mix proof, teaching, opinion, story and offer according to the actual goal.
3. For each slot specify concrete angle, format, objective, hook formula ID where useful, CTA and production asset. Avoid repeating recent drafts unless the user requests a series.
4. Choose exact dates in the client's current date context. Use audience timezone, labelled explicitly. Prefer actual Insights for timing; otherwise label times as hypotheses to test. A plan is not a scheduled automation.
5. Identify **10 accounts** with source links and an individual relevance reason when research is accessible (a useful mix is five audience-reach accounts, three peers and two possible buyers). If identities cannot be verified, show category slots and disclose the gap; do not invent handles. Suggest context-specific comment angles via `/IG-COMMENT`; do not send anything.
6. Save the requested plan to `<state-dir>/plan.md` and/or the deliverables directory. Draft every requested post in scope; do not impose a one-at-a-time gate. For a new voice profile, use the optional template in `assets/voice.md`; do not overwrite existing user state.

## Deliver

Seven-day calendar with dates/times/timezone, formats, angles, formula IDs, CTAs and production needs; ten-account engagement list with evidence or explicit gaps. State what is drafted versus merely planned. No publishing/scheduling.

# /IG-PROFILE

# ig-profile


## Workflow

1. Read accessible profile data or supplied screenshots/text: name, handle, bio, destination, highlights, pinned posts, first nine covers, activity and visible contact options. Mark unseen items unknown.
2. Read `rubric.json`: 12 criteria whose weights total 100. Score each observed item with evidence, show the table and coverage. For unseen items use N/A and report observed points / observed maximum; do not assign zero to missing evidence or extrapolate a complete score.
3. Prioritize the largest supported point losses. Rewrite the searchable name (three options), bio, clear offer/link label, pinned post roles and highlight names as relevant. Recommend grid/visual changes with actual examples.
4. Treat rubric character counts and platform features as working defaults; verify current official limits if exact compliance is requested. Never invent proof, claims or destinations.
5. Apply `/IG-HUMAN`. Distinguish points a text revision could improve from visual/activity improvements not yet implemented. A proposed score is an estimate, not the live profile's new score.

## Deliver

12-row scored table, evidence/unknowns, prioritized copy-ready rewrites, visual/action recommendations, and a clearly labelled possible improvement. Do not edit the live account.

# /IG-REEL

# ig-reel


## Workflow

1. Read relevant voice, swipe and recent draft log state. Use one specific idea and only substantiated facts.
2. Read `hooks.json`: preserve the 26 original IDs and formula names. Each formula also has a Romanian template/example and match pattern. Choose three distinct formulas that fit the idea and write a spoken hook plus a separate on-screen hook for each.
3. Write spoken hooks to a UTF-8 file, one per line. Run `python3 <skill-dir>/hookscore.py <hooks-file> --json`. Show all three scores and the weakest properties. Scores guide editing; they do not predict a winner.
4. Develop the best justified hook into the requested length (working default 15–45 seconds). Structure: hook, stake, one idea per beat, payoff, one CTA. A natural echo of the opening can support a loop; do not force it.
5. Write the script as one spoken beat per line. Run `python3 <skill-dir>/beats.py <script-file> --target 30 --wpm 165 --json`, adjusting target and speaking rate to the request. Estimate durations, do not claim measured speech. Fix long beats by shortening speech or specifying a visual cut.
6. Apply `/IG-HUMAN` to the copy without flattening the writer's voice. Re-run timing after text edits. Stop after two score-driven revisions.

## Deliver

- Three hook options with formula IDs, spoken and screen versions, scores and short rationale.
- A copy-ready spoken script, on-screen cards (usually no more than six words), estimated timecodes and shot/cut notes.
- Actual helper results and limitations; hand off to `/IG-CAPTION` when requested.
- If saving state, record date, formula, hook and `status: draft` in `.instagram/log.md`. No approval prompt is needed merely to finish the requested draft.

# /IG-REPLY

# ig-reply


## Workflow

Read supplied/accessibly retrieved comments with source context; do not invent missing thread context. Classify all comments, report counts, then draft in priority order:

| Category | Treatment |
| --- | --- |
| KEYWORD | Deliver the real promised resource; draft a public acknowledgment and optional DM. |
| LEAD | Answer the actual issue publicly, with an optional low-pressure offer of help. |
| SUBSTANCE | Address evidence, disagreement or an extension specifically. |
| QUESTION | Answer; flag useful recurring questions for a Reel with formula #16. |
| SUPPORT | Brief personal acknowledgment when useful. |
| NOISE | Recommend skipping spam/bait; no invented obligation to engage. |

Keep replies proportional, acknowledge a critic's valid point, and avoid a defensive back-and-forth. Apply `/IG-HUMAN`; a short reply need not pass statistical style checks. Never claim a resource has been sent when only its message is drafted. Moderation suggestions are recommendations, not permission to hide/delete comments. No publishing or sending.

## Deliver

Counts by category, copy-ready replies linked to original handles/comments, skipped-item reasons, and question-to-Reel candidates. Mark all outputs as drafts.

# /IG-REPURPOSE

# ig-repurpose


## Workflow

1. Read the complete available source/transcript. Use a connector/transcription tool if available for a supplied URL or file. State inaccessible or truncated portions; do not pretend to have watched a video from its title.
2. Extract independent claims, numbers, stories, mechanisms, mistakes and quotable lines. Preserve exact claims; record timestamp, paragraph or section references. Count what is actually present.
3. Map claims/stories to Reels, reusable mechanisms/steps to carousels, short moments/lines to Stories. Use original footage when supplied and suitable; distinguish a clip plan from an exported video.
4. Build a feasible week (often 4–6 posts) with varied hook formula IDs from `../ig-reel/hooks.json`. Do not pad a thin source or create multiple posts that require watching the source to understand.
5. Produce all drafts/exports the user actually requests using sibling skills; do not impose a mandatory one-draft-at-a-time approval sequence. For actual video edits invoke the available video workflow; for carousels render and inspect files with `/IG-CAROUSEL`.

## Deliver

Source coverage and extraction inventory, seven-day reuse plan, format/angle/CTA/formula and source location per post, plus the requested drafts or actual exports. Credit the original source and do not imply ownership of third-party footage.

# /IG-STORY

# ig-story


## Workflow

1. Use a real current event, process, offer or audience question. Default to 3–7 frames when no count is specified.
2. Sequence: personal/visual opening, context or demonstration, an interaction, payoff/next step. Put the interaction before the final frame when sensible. One idea per frame.
3. Choose a sticker by purpose: poll for a quick choice, question box for audience language, quiz for teaching if available, slider for light feedback, link for a real destination, countdown for a genuine deadline, Add Yours for a relevant participation prompt. Verify availability before promising a specific current feature.
4. Specify on-screen copy, spoken copy, visual and sticker label/options for each frame. Working canvas 1080x1920; keep important content away from top/bottom controls and inspect current UI when precision matters.
5. Explain how a voluntary poll/question/reply can open a conversation; draft the response or hand off to `/IG-DM`. Participation does not itself authorize this agent to message anyone. Do not claim that all voters have consented to marketing.
6. Apply `/IG-HUMAN` to copy. If imagery/video is requested, use the relevant creation workflow and label actual exports separately from a storyboard.

## Deliver

Ordered frame table with visual, spoken/on-screen text, sticker and purpose; one clear CTA; suggested responses to interactions. No publishing or automated DM setup.

# /IG-VIRAL

# ig-viral


## Workflow

1. Determine niche, audience and research window from context. Use supplied accounts or propose a relevant bounded sample (working target 6–12 accounts, up to 12 recent comparable Reels per account). Do not block read-only research on approval of an account list.
2. Read accessible source posts through connectors or browsing. Record account, URL, observation date, published date, views, hook, first screen card, length and CTA. Record followers as context only. Missing fields stay missing.
3. Compute each account's median from actual comparable recent Reel view counts. State window, sample size and whether the target Reel is included. Use complete integer counts, not `12k`/`1.2M`, in the TSV. Do not eyeball or invent a median. Do not mix paid and organic posts silently.
4. Create UTF-8 TSV with at least `account`, `median`, `views`, `hook`; retain `url` and `observed_at` columns. Run `python3 <skill-dir>/swipe.py <captured.tsv> --json --out <state-dir>/swipe.md`.
5. Rank only rows with a positive measured median by `views / median`. Missing/zero medians are unranked, never replaced by follower counts. The script recognizes original English and added Romanian formulas and leaves uncertain hooks unclassified. Review those manually; keep manual classifications separate from script output.
6. Report overrepresented formulas, structural differences, unclassified examples and data coverage with source links. Label small-sample findings tentative; 3x is a working outlier threshold, not a universal law. Do not infer causation from view counts.
7. Produce three original hook ideas grounded in the user's own facts and offer `/IG-REEL` production details within the requested scope.

If Instagram access is blocked, continue with available public sources or user data. A Shorts comparison must be explicitly labelled as YouTube evidence and never silently pooled with Instagram medians. Do not build a feed crawler. Save provenance alongside the swipe file.
