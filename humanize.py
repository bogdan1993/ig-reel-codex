#!/usr/bin/env python3
"""Conservative RO/EN copy cleanup and editorial suggestions; no authorship claims."""
import argparse
import json
from pathlib import Path
import re
import sys
import unicodedata

LEX = Path(__file__).with_name('slop.json')
URL_RE = re.compile(r'https?://\S+|www\.\S+|\S+@\S+\.\S+')
WORD_RE = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*")


def load_lexicon(path=LEX):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def lexical_pattern(entry):
    return re.compile(r'\b' + re.escape(entry['find']).replace(r'\ ', r'\s+') + r'\b', re.I)


def scan_structures(text, lex):
    flags = []
    for entry in lex['structures']:
        hits = list(re.finditer(entry['regex'], text, re.M))
        if hits:
            flags.append({'name': entry['name'], 'count': len(hits), 'fix': entry['fix']})
    return flags


def humanize(text, lex, apply_lexical=False, normalize_typography=False):
    urls = []
    def protect(match):
        urls.append(match.group())
        return f'\x00URL{len(urls)-1}\x00'
    text = URL_RE.sub(protect, text)
    report = {'invisible': [], 'typographic': [], 'lexical': [], 'structures': []}
    normalized = unicodedata.normalize('NFC', text)
    if normalized != text:
        report['invisible'].append({'name': 'Unicode NFC', 'count': 1, 'action': 'normalize'})
    text = normalized
    # Keep ZWJ/ZWNJ and emoji tag sequences: they can carry real language/emoji meaning.
    for chars, replacement, label in [('\u200b\ufeff\u00ad', '', 'accidental zero-width/BOM/soft hyphen'), ('\u00a0\u202f', ' ', 'nonbreaking spaces')]:
        count = sum(text.count(c) for c in chars)
        if count:
            text = text.translate({ord(c): replacement for c in chars})
            report['invisible'].append({'name': label, 'count': count, 'action': 'normalize'})
    if normalize_typography:
        for entry in lex['typographic']:
            count = text.count(entry['from'])
            if count:
                text = text.replace(entry['from'], entry['to'])
                report['typographic'].append({'name': entry['name'], 'count': count, 'to': entry['to']})
    for entry in sorted(lex['phrases'] + lex['words'], key=lambda e: len(e['find']), reverse=True):
        pattern = lexical_pattern(entry)
        count = len(pattern.findall(text))
        if count:
            report['lexical'].append({'find': entry['find'], 'replace': entry['replace'], 'count': count, 'applied': apply_lexical})
            if apply_lexical:
                def replace(match):
                    value = entry['replace']
                    if not value:
                        return ''
                    if match.group().isupper():
                        return value.upper()
                    return value[0].upper() + value[1:] if match.group()[0].isupper() else value
                text = pattern.sub(replace, text)
    report['structures'] = scan_structures(text, lex)
    for i, url in enumerate(urls):
        text = text.replace(f'\x00URL{i}\x00', url)
    return text, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', nargs='?', default='-')
    parser.add_argument('-o', '--out')
    parser.add_argument('--report', action='store_true')
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--lexicon', default=LEX)
    parser.add_argument('--apply-lexical', action='store_true', help='Apply suggested substitutions; review meaning afterward')
    parser.add_argument('--normalize-typography', action='store_true')
    args = parser.parse_args()
    raw = sys.stdin.read() if args.input == '-' else Path(args.input).read_text(encoding='utf-8')
    clean, report = humanize(raw, load_lexicon(args.lexicon), args.apply_lexical, args.normalize_typography)
    if args.out:
        Path(args.out).write_text(clean, encoding='utf-8')
    if args.json:
        print(json.dumps({'text': clean, 'report': report}, ensure_ascii=False, indent=2))
    elif not args.out:
        sys.stdout.write(clean)
    if args.report:
        print(json.dumps(report, ensure_ascii=False, indent=2), file=sys.stderr)


if __name__ == '__main__':
    main()
