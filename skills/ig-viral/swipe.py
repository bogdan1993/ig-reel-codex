#!/usr/bin/env python3
"""Rank observed Reel counts against account medians. Missing baselines stay unranked."""
import argparse
import csv
import io
import json
from pathlib import Path
import re
import statistics
import sys

HERE = Path(__file__).resolve().parent
HOOKS = HERE.parent/'ig-reel/hooks.json'
sys.path.insert(0, str(HERE.parent/'ig-reel'))
from hookscore import run as score_hook, words


def number(value, field):
    if value is None or not str(value).strip():
        return None
    value = str(value).strip()
    if not re.fullmatch(r'\d+', value):
        raise ValueError(f'{field}: supply a full nonnegative integer, not {value!r}')
    return int(value)


def load_formulas(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    by_id = {h['id']: h for h in data['hooks']}
    result = []
    for fid in data.get('classify_order', by_id):
        hook = by_id[fid]
        patterns = [re.compile(hook[k], re.I) for k in ('match', 'match_ro') if hook.get(k)]
        result.append((fid, hook['name'], patterns))
    return result


def classify(hook, formulas):
    for fid, name, patterns in formulas:
        if any(pattern.search(hook) for pattern in patterns):
            return fid, name
    return None, 'unclassified'


def read_rows(path):
    raw = sys.stdin.read() if str(path) == '-' else Path(path).read_text(encoding='utf-8-sig')
    reader = csv.DictReader(io.StringIO(raw), delimiter='\t')
    if not {'account','views','hook'}.issubset(reader.fieldnames or []):
        raise ValueError('Required TSV headers: account, views, hook; median may be blank')
    rows = []
    for line, row in enumerate(reader, 2):
        if not any(row.values()):
            continue
        if None in row:
            raise ValueError(f'row {line}: extra cells; quote tabs inside fields')
        if not row['account'].strip() or not row['hook'].strip():
            raise ValueError(f'row {line}: account and hook are required')
        for key in ('views','median','followers'):
            row[key] = number(row.get(key), f'row {line} {key}')
        rows.append(row)
    return rows


def analyse(rows, formulas):
    ranked, unranked = [], []
    for original in rows:
        row = dict(original)
        median, views = row.get('median'), row.get('views')
        row['baseline'] = median
        row['outlier'] = round(views/median, 4) if median is not None and median > 0 and views is not None else None
        row['formula_id'], row['formula'] = classify(row['hook'], formulas)
        row['words'] = len(words(row['hook']))
        _, score, verdict, _ = score_hook(row['hook'])
        row['hook_score'], row['hook_verdict'] = round(score, 1), verdict
        (ranked if row['outlier'] is not None else unranked).append(row)
    ranked.sort(key=lambda r: -r['outlier'])
    third = len(ranked)//3
    top = ranked[:third] if third else []
    bottom = ranked[-third:] if third else []
    def median(items, key):
        return statistics.median([r[key] for r in items]) if items else None
    counts = {}
    for row in top:
        counts[row['formula']] = counts.get(row['formula'], 0)+1
    return {'baseline':'account median', 'n':len(rows), 'ranked_n':len(ranked), 'unranked_n':len(unranked),
            'accounts':len({r['account'] for r in rows}), 'reels':ranked+unranked,
            'top_formulas':sorted(counts.items(), key=lambda item:-item[1]),
            'top_hook_score':median(top,'hook_score'), 'bottom_hook_score':median(bottom,'hook_score'),
            'unclassified':sum(r['formula_id'] is None for r in ranked+unranked),
            'note':'Only measured positive medians are ranked. No follower fallback. Pattern matches and scores are editorial heuristics.'}


def to_markdown(result):
    lines = ['# Swipe file','',f"{result['n']} observations; {result['ranked_n']} ranked; {result['unranked_n']} without a usable median.",'',result['note'],'']
    for row in result['reels']:
        multiple = f"{row['outlier']:.2f}x" if row['outlier'] is not None else 'N/A'
        lines += [f"## {row['account']} | {multiple} | {row['formula']}",
                  f"- Views: {row['views']}; measured median: {row['baseline']}",
                  f"- Hook: {row['hook']}", f"- Heuristic hook score: {row['hook_score']}"]
        for key in ('url','observed_at','published_at','baseline_window','baseline_n'):
            if row.get(key):
                lines.append(f'- {key}: {row[key]}')
        lines.append('')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', default='-')
    parser.add_argument('--hooks', default=HOOKS)
    parser.add_argument('--out')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        rows = read_rows(args.input)
        if not rows:
            raise ValueError('No observations supplied')
        result = analyse(rows, load_formulas(args.hooks))
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2) if args.json else to_markdown(result))
    if args.out:
        path = Path(args.out).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(to_markdown(result), encoding='utf-8')


if __name__ == '__main__':
    main()
