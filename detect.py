#!/usr/bin/env python3
"""RO/EN editorial style panel. Not an AI authorship or provenance detector."""
import argparse
import json
from pathlib import Path
import re
import statistics
import sys

from humanize import LEX, WORD_RE, lexical_pattern, load_lexicon, scan_structures


def clamp(value):
    return max(0.0, min(100.0, value))


def run(text, lex):
    words = WORD_RE.findall(text)
    sentences = [WORD_RE.findall(s) for s in re.split(r'[.!?\n]+', text)]
    lengths = [len(s) for s in sentences if len(s) >= 3]
    checks = {}
    def add(name, score, detail):
        checks[name] = {'score': round(score, 1) if score is not None else None, 'detail': detail}
    if len(lengths) >= 4:
        variation = statistics.pstdev(lengths) / statistics.mean(lengths)
        add('BURSTINESS', clamp((variation-.22)/.48*100), f'{variation:.2f} sentence-length variation; stylistic, not authorship evidence')
    else:
        add('BURSTINESS', None, 'Need at least four substantive sentences')
    if len(words) >= 25:
        concrete = len(re.findall(r'\b\d[\d,.]*\b', text))
        concrete += len(set(re.findall(r'(?<!^)\b[A-ZĂÂÎȘȚŞŢ][a-zăâîșțşţ]{2,}\b', text)))
        add('SPECIFICITY', clamp((concrete*100/len(words)-.5)/5.5*100), f'{concrete} numeric/name markers; review concrete details manually too')
    else:
        add('SPECIFICITY', None, 'Need at least 25 words; concise copy can be appropriate')
    hits = sum(len(lexical_pattern(e).findall(text)) for e in lex['words']+lex['phrases'])
    add('SLOP DENSITY', clamp(100-hits*25), f'{hits} RO/EN lexical suggestions; context decides')
    accidental = sum(text.count(c) for c in '\u200b\ufeff\u00ad')
    add('FORMATTING', clamp(100-accidental*20), f'{accidental} selected accidental control characters; punctuation and emoji are preserved')
    flags = scan_structures(text, lex)
    if len(words) >= 25:
        add('PHRASING', clamp(100-sum(f['count'] for f in flags)*20), f'{len(flags)} structural suggestions; no English-contraction requirement')
    else:
        add('PHRASING', None, 'Short text: use editorial judgement')
    values = [v['score'] for v in checks.values() if v['score'] is not None]
    enough = all(v['score'] is not None for v in checks.values())
    score = round(statistics.mean(values)*.6+min(values)*.4, 1) if enough else None
    verdict = 'INSUFFICIENT_DATA' if not enough else ('PASS' if score >= 70 else 'REVIEW')
    return {'checks': checks, 'style_score': score, 'verdict': verdict, 'structural_flags': flags,
            'note': 'Uncalibrated editorial heuristics; not evidence of AI authorship, origin, truth or future reach.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', default='-')
    parser.add_argument('compare', nargs='?')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--lexicon', default=LEX)
    args = parser.parse_args()
    if args.compare == '-' and args.input == '-':
        parser.error('stdin cannot be used twice')
    lex = load_lexicon(args.lexicon)
    payload = []
    for path in [args.input] + ([args.compare] if args.compare else []):
        text = sys.stdin.read() if path == '-' else Path(path).read_text(encoding='utf-8')
        payload.append({'source': path, **run(text, lex)})
    if args.json:
        print(json.dumps(payload if args.compare else payload[0], ensure_ascii=False, indent=2))
    else:
        for result in payload:
            print(f"STYLE PANEL: {result['source']} | {result['verdict']} | {result['style_score'] if result['style_score'] is not None else 'N/A'}")
            for key, check in result['checks'].items():
                print(f"  {key}: {check['score'] if check['score'] is not None else 'N/A'} - {check['detail']}")
            print(result['note'])
    return 1 if payload[-1]['verdict'] == 'REVIEW' else 0


if __name__ == '__main__':
    sys.exit(main())
