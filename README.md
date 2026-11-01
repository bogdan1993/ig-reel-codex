# Instagram Reel skill for Codex

A self-contained Codex skill that turns one idea into a Reel script: **three scored hooks from 26 formulas, spoken copy, screen text and estimated beat timing**, with Romanian and English editorial support.

Adapted from [Jake Schincariol's instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill), MIT licensed. The original 26 hook formulas are preserved. `upstream-commit.json` records the source revision. This is an independent adaptation, not an official OpenAI or Instagram integration.

## Install

Copy this repository into a directory named `ig-reel` under your Codex skills directory (`$CODEX_HOME/skills`, commonly `~/.codex/skills`). Keep SKILL.md, Python helpers and JSON resources together. If an ig-reel skill already exists, preserve it before replacing it; this project does not silently overwrite existing skills.

Alternatively, ask Codex to install this repository as the `ig-reel` skill, using the repository root as the skill path. The skill should be discoverable on the next turn; refresh the conversation if your client needs it.

**Requirements:** Codex with local file and shell tools; Python 3.10+. Helpers use only the Python standard library. No API key, Instagram login, account connection or third-party Python package is needed.

## Use

```text
$ig-reel Write a 35-second Reel about leading without a management title.
$ig-reel Scrie un Reel despre leadership fără funcție de management, în română.
$ig-reel Refine this draft in my voice. Return only the final spoken script: ...
```

`$ig-reel` is the native skill invocation. `/ig-reel` is supported as a textual convention if the client sends it to the agent; installation does not add a native slash command or guarantee slash autocomplete.

The skill prepares a script and a production plan. It does not render or publish videos and cannot message people or manage an Instagram account. Existing personal voice instructions are respected, but no proprietary voice profile or brand asset is bundled.

## What's included

| File | Purpose |
| --- | --- |
| SKILL.md | Codex workflow and invocation rules |
| hooks.json | Original 26 formulas plus Romanian templates, examples and conservative match patterns |
| hookscore.py | Five editorial checks for a spoken hook |
| beats.py | Estimated line-by-line timing with configurable speaking rate |
| humanize.py | Conservative copy cleanup and editorial suggestions |
| detect.py | Five-check style panel; not AI authorship detection |
| slop.json | Combined English/Romanian editorial lexicon |
| slop-ro.json / slop-en.json | Language-specific editorial lexicons |
| test_helpers.py | Local behavior tests |

## Run the helpers directly

```bash
python3 hookscore.py --hook "Nu mai aștepta promovarea ca să fii lider." --json
python3 beats.py script.txt --target 40 --wpm 165 --json
python3 humanize.py script.txt -o clean.txt --report
python3 detect.py script.txt clean.txt --json
python3 -B -m unittest test_helpers -v
```

Run helpers by absolute path when your working directory differs from the skill directory. They accept UTF-8 files; most also support stdin with `-`. An editorial REVIEW may return exit code 1. Read the report rather than treating every nonzero code as a runtime error.

By default, cleanup preserves paragraph breaks, natural punctuation, URLs and compound emoji. `--apply-lexical` and `--normalize-typography` are optional modes that require review for meaning. Use `--lexicon slop-ro.json` or `--lexicon slop-en.json` to restrict lexical review.

## Honest limitations

- Scores are **uncalibrated editorial heuristics**, including the Romanian additions. They do not predict views or identify a viral winner. Useful concrete examples may score poorly because a simple checker cannot understand their meaning.
- `detect.py` is a style review, not an AI detector or watermark remover. Typography and invisible characters do not prove authorship. Short texts can return INSUFFICIENT_DATA.
- Beat timings estimate speech from word count. Set the person's actual speaking rate when known; verify with a recording for production.
- Formula examples are fictional illustrations unless explicitly sourced. They must not become invented claims about a user's clients or achievements.
- This repository contains no personal voice corpus, private drafts, account credentials or analytics.

## În română

Invocă `$ig-reel` și precizează ideea. Poți indica durata, publicul și vocea dorită; profilul personal existent rămâne local. Vei primi un singur scenariu, cu trei variante de început punctate dacă nu ceri doar textul final. Scorurile ghidează revizia, fără promisiuni de viralitate.

## Attribution and license

Original project and formula library: **Jake Schincariol**. Codex workflow, Romanian support and conservative style-tool adaptations: prepared for **Bogdan Pădurariu** with Codex. Original copyright and MIT permission notice are preserved in LICENSE. The adapted code is distributed under the same license.
