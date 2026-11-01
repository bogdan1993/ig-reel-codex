#!/usr/bin/env python3
"""Install this adapted pack without overwriting unrelated or modified skills."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dest',type=Path,default=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'skills')
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
    for relative, expected in manifest['files'].items():
        source=ROOT/relative
        if not source.is_file() or source.is_symlink() or digest(source)!=expected:
            parser.error(f'Package file missing, symlinked or modified: {relative}')
    names=manifest['skills']
    dest=args.dest.expanduser().resolve()
    conflicts=[]
    pending=[]
    for name in names:
        source=ROOT/'skills'/name
        target=dest/name
        if target.exists() or target.is_symlink():
            expected={p.relative_to(source):digest(p) for p in source.rglob('*') if p.is_file()}
            found={p.relative_to(target):digest(p) for p in target.rglob('*') if p.is_file() and '__pycache__' not in p.parts} if target.is_dir() and not target.is_symlink() else {}
            if expected!=found:
                conflicts.append(str(target))
        else:
            pending.append((source,target))
    if conflicts:
        parser.error('Existing different skills would be overwritten; no changes made: '+', '.join(conflicts))
    if args.check:
        print(f'Package verified: {len(names)} skills; {len(pending)} to install at {dest}; no conflicts.')
        return
    installed=[]
    try:
        dest.mkdir(parents=True,exist_ok=True)
        for source,target in pending:
            # Track before copying so rollback also removes a partially copied new directory.
            installed.append(target)
            shutil.copytree(source,target)
        for name in names:
            source=ROOT/'skills'/name
            for path in source.rglob('*'):
                if path.is_file() and digest(path)!=digest(dest/name/path.relative_to(source)):
                    raise RuntimeError(f'Installed content differs: {path}')
    except Exception:
        for target in installed:
            if target.exists():
                shutil.rmtree(target)
        raise
    print(f'Installed and verified {len(installed)} new skills; {len(names)-len(installed)} already identical. Destination: {dest}')
    print('Skills are available on the next turn. Native invocation: $ig-reel; /ig-reel is a textual alias.')


if __name__=='__main__':
    main()
