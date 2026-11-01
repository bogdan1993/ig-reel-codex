#!/usr/bin/env python3
"""Compute Instagram audit ratios from CSV. Missing values stay unknown."""
import argparse
import csv
import io
import json
import math
from pathlib import Path
import statistics
import sys

FIELDS = ('views','reach','sends','shares','follows')


def numeric(value, field):
    if value is None or str(value).strip() == '':
        return None
    try:
        number = float(value)
    except ValueError:
        raise ValueError(f'{field}: use a full numeric count, not {value!r}') from None
    if not math.isfinite(number) or number < 0 or not number.is_integer():
        raise ValueError(f'{field}: counts must be finite nonnegative integers')
    return int(number)


def ratio(numerator, denominator):
    return numerator/denominator if numerator is not None and denominator is not None and denominator > 0 else None


def analyse(source):
    rows = []
    for i, original in enumerate(source, 1):
        row = dict(original)
        row.setdefault('id', str(i))
        row['account'] = row.get('account') or 'unspecified-account'
        row['format'] = row.get('format') or 'unspecified-format'
        for key in FIELDS:
            row[key] = numeric(row.get(key), f'row {i} {key}')
        rows.append(row)
    cohorts = {}
    for row in rows:
        key = (row['account'],row['format'])
        cohorts.setdefault(key,[])
        if row['views'] is not None:
            cohorts[key].append(row['views'])
    for row in rows:
        views = cohorts[(row['account'],row['format'])]
        row['median_views'] = statistics.median(views) if views else None
        row['baseline_n'] = len(views)
        row['outlier'] = ratio(row['views'],row['median_views'])
        row['sends_per_reach'] = ratio(row['sends'],row['reach'])
        row['shares_per_reach'] = ratio(row['shares'],row['reach'])
        row['follows_per_reach'] = ratio(row['follows'],row['reach'])
    rankings = {}
    for key in ('outlier','sends_per_reach','shares_per_reach','follows_per_reach'):
        rankings[key] = [r['id'] for r in sorted((r for r in rows if r[key] is not None),key=lambda r:-r[key])]
    return {'posts':rows,'n':len(rows),'rankings':rankings,
            'note':'Medians are computed within account+format over supplied observations, including the target post. Ratios are fractions, not percentages. Unknown/zero denominators yield null. Shares are not necessarily DM sends. No causal inference.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',nargs='?',default='-')
    parser.add_argument('--json',action='store_true')
    args = parser.parse_args()
    raw = sys.stdin.read() if args.input == '-' else Path(args.input).read_text(encoding='utf-8-sig')
    reader = csv.DictReader(io.StringIO(raw))
    if 'views' not in (reader.fieldnames or []):
        parser.error('CSV requires at least a views header; blank values are allowed')
    source = list(reader)
    if not source or any(None in row for row in source):
        parser.error('Supply at least one well-formed CSV data row')
    ids = [row.get('id') or str(i) for i,row in enumerate(source,1)]
    if len(ids) != len(set(ids)):
        parser.error('Post IDs must be unique')
    for row, pid in zip(source,ids):
        row['id'] = pid
    try:
        result = analyse(source)
    except ValueError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        print('INSTAGRAM AUDIT')
        for row in result['posts']:
            print(f"{row['id']}: median={row['median_views']} (n={row['baseline_n']}), outlier={row['outlier']}, sends/reach={row['sends_per_reach']}, shares/reach={row['shares_per_reach']}, follows/reach={row['follows_per_reach']}")
        print(result['note'])


if __name__ == '__main__':
    main()
