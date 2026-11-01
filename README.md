# Instagram Agent Skills for Codex

**All 13 commands from the original Instagram agent pack**, adapted for Codex, with Romanian and English editorial support. Plan, research, write and review Instagram content using local skills and standard-library Python tools.

Adapted from [Jake Schincariol’s instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill), under the **MIT license**. The original 26 hook formula IDs and the 12-part, 100-point profile rubric are preserved. This is an independent adaptation, not an official OpenAI or Instagram integration.

The repository keeps its original URL, `bogdan1993/ig-reel-codex`, but now contains the complete pack. The earlier Reel-only layout has been replaced by `skills/ig-reel/` and its 12 sibling skills.

## All 13 commands

| Text alias | Native Codex invocation | What you get |
| --- | --- | --- |
| `/ig-reel` | `$ig-reel` | Three hooks from 26 formulas, actual heuristic scores, spoken script, screen text and estimated beat timing. |
| `/ig-viral` | `$ig-viral` | Sourced niche research, ranking against each account’s measured recent median and a swipe file. |
| `/ig-caption` | `$ig-caption` | A linted caption, search-term coverage, one suitable CTA and an approximate 125-character preview. |
| `/ig-carousel` | `$ig-carousel` | Cover, slide copy, recap, caption, alt text and actual 1080×1350 exports through an available renderer. |
| `/ig-story` | `$ig-story` | A frame-by-frame Stories sequence, sticker suggestions and voluntary conversation handoffs. |
| `/ig-profile` | `$ig-profile` | A 12-part profile assessment out of 100, evidence coverage and prioritized rewrites. |
| `/ig-plan` | `$ig-plan` | A seven-day content plan, formats, audience-local times and ten relevant accounts when verifiable. |
| `/ig-human` | `$ig-human` | Natural-voice revision with conservative cleanup and a five-check local style panel. |
| `/ig-comment` | `$ig-comment` | Specific comment drafts selected from nine comment types. |
| `/ig-reply` | `$ig-reply` | Comment triage into keyword, lead, substance, question, support and noise, then reply drafts. |
| `/ig-dm` | `$ig-dm` | Keyword delivery, warm first messages, collaboration pitches and at most two follow-ups. |
| `/ig-repurpose` | `$ig-repurpose` | A long source turned into independent Reels, carousels and Stories, with source locations. |
| `/ig-audit` | `$ig-audit` | Post analysis by account median, sends per reach, shares per reach and follows per reach. |

`$ig-name` is the native skill invocation. `/ig-name` is a textual alias when the client sends it to the agent. Installing the pack does **not** register native slash commands or guarantee slash autocomplete.

## Install the full pack

**Requirements:** Codex with local file and shell tools; Python 3.10+. The bundled helpers use the standard library. Drafting and local checks require no Instagram login or API key. Research and rendering use the connectors, browser and rendering tools available in the calling session.

Clone or download this repository, then run from its root:

```bash
python3 install.py --check
python3 install.py
```

The installer checks package hashes and copies all 13 skill directories into `$CODEX_HOME/skills`, falling back to `~/.codex/skills`. It refuses to overwrite an existing different skill, checks the complete destination before copying and rolls back newly copied directories on failure. Identical existing skills are left alone.

For another location:

```bash
python3 install.py --dest /absolute/path/to/skills --check
python3 install.py --dest /absolute/path/to/skills
```

Keep the pack together: the sibling workflows share `skills/ig-reel/references/codex.md`, and `ig-viral` uses the Reel formula library and scorer. If you installed the previous Reel-only version, preserve that existing directory before installing the complete pack. Do not install the repository root as a single skill anymore.

Alternatively, ask Codex:

```text
Install all 13 skills from https://github.com/bogdan1993/ig-reel-codex.
Use every skills/ig-* directory, not the repository root.
```

Skills are available on the next turn; refresh the conversation if your client needs it.

## Examples

```text
$ig-reel Write a 35-second Reel about leading without a management title.
$ig-caption Write the caption for that script, using my existing voice profile.
$ig-viral Research leadership Reels and separate verified data from missing metrics.
$ig-carousel Turn this argument into a finished seven-slide carousel with PNG exports.
$ig-plan Plan next week for an audience in Europe/Bucharest.
$ig-audit Analyze this CSV; distinguish DM sends from total shares.
```

In Romanian:

```text
$ig-reel Scrie un Reel despre leadership fără funcție de management.
$ig-story Pregătește cinci Stories care continuă ideea, în vocea mea.
$ig-dm Redactează livrarea resursei promise și două reveniri potrivite.
$ig-repurpose Transformă acest transcript într-o săptămână de conținut.
```

An existing personal-voice skill can guide tone, but none is required or bundled. Private voice samples, drafts, credentials and analytics are not part of the repository.

## Local state and deliverables

Optional working state lives in `.instagram/` **inside the active project**, or an explicitly chosen directory:

- `voice.md`: known voice and audience preferences.
- `swipe.md`: sourced research evidence.
- `log.md`: drafts/approved/published entries, labelled according to actual evidence.
- `plan.md` and `audit.md`: planning and analysis outputs.

Start a voice profile from `templates/voice.md` or `skills/ig-plan/assets/voice.md` if needed. These are empty templates; the pack does not include a personal writing corpus. Scratch files go in `work/`; actual deliverables follow the workspace’s output rules.

## Tools that run locally

| Command | Helpers/resources |
| --- | --- |
| `ig-reel` | `hookscore.py`, `beats.py`, `hooks.json` |
| `ig-viral` | `swipe.py`, shared Reel formulas/scorer |
| `ig-caption` | `caption.py` with configurable limits and preview width |
| `ig-human` | `humanize.py`, `detect.py`, RO/EN editorial lexicons |
| `ig-profile` | `rubric.json`: 12 criteria, weights totaling 100 |
| `ig-audit` | `audit.py`: account+format cohorts and missing-value-safe ratios |

Examples from the repository root:

```bash
python3 skills/ig-reel/hookscore.py --hook "Nu mai aștepta promovarea ca să fii lider." --json
python3 skills/ig-reel/beats.py script.txt --target 40 --wpm 165 --json
python3 skills/ig-caption/caption.py caption.txt --keywords "leadership,management" --json
python3 skills/ig-human/humanize.py script.txt -o clean.txt --report
python3 skills/ig-human/detect.py script.txt clean.txt --json
python3 skills/ig-viral/swipe.py captured.tsv --json --out .instagram/swipe.md
python3 skills/ig-audit/audit.py posts.csv --json
```

An editorial REVIEW may return exit code 1; inspect the report. `detect.py` retains its historical filename but is a **style panel**, not an AI detector. `humanize.py` preserves natural typography, paragraphs, URLs and emoji joiners by default. Automatic lexical substitutions and typography normalization are optional and need editorial review.

## Data and capability boundaries

- These skills prepare content. They do not publish, message, follow, like, hide comments or schedule outreach.
- `ig-viral` depends on accessible source posts and comparable view counts. It never substitutes follower count for a missing median, invents unavailable counts or silently pools YouTube evidence with Instagram. Missing baselines stay unranked.
- `ig-audit` keeps unknown values distinct from zero and total shares distinct from DM sends. Zero/missing denominators yield N/A.
- Scores are uncalibrated editorial heuristics, including Romanian additions. They do not predict reach, determine authorship or guarantee originality. Short texts can return INSUFFICIENT_DATA.
- Beat timing estimates speech from word count; a recording is needed for actual timing.
- A 125-character preview and platform limits are configurable working defaults, not a promise about every device or the current Instagram UI. Verify current official rules when exact compliance matters.
- Carousel/video export requires a suitable renderer or media workflow in the calling session. The pack does not install or bundle a new video renderer. A copy-only result must not be labelled a finished exported carousel.
- Source examples and hypothetical scenarios are not evidence about a user’s experience. No fake clients, testimonials, results or statistics.

## Verification

```bash
python3 -B -m unittest discover -s tests -v
python3 install.py --check --dest /absolute/path/to/a/test-skills-directory
```

The suite covers Unicode/diacritics, RO/EN copy checks, caption preview, conservative cleanup, missing/zero analytics, preserved provenance, command-line operation from another working directory and non-overwriting installation. `VERIFICARE.md` records the scope and limitations of the checks. PyYAML is only needed if you separately run Codex’s official skill validator; it is not a runtime dependency of this pack.

## Attribution and license

Original project and formula library: **Jake Schincariol**, [instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill). Codex workflow, Romanian support and conservative tooling adaptations: prepared for **Bogdan Pădurariu** with Codex. Original copyright and MIT permission notices remain in the root LICENSE and each skill directory. `upstream-commit.json` identifies the original source revision.
