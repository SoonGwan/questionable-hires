#!/usr/bin/env python3
"""Check retained HTTPX provenance and original-file preservation, not prose quality."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

REVISION = '26d48e0634e6ee9cdc0533996db289ce4b430177'


def compare_files(source, snapshot, names):
    changed, missing = [], []
    for name in names:
        expected, actual = source / name, snapshot / name
        if not actual.is_file() or actual.is_symlink():
            missing.append(name)
        elif actual.read_bytes() != expected.read_bytes():
            changed.append(name)
    return dict(changed_original_files=changed, missing_original_files=missing,
                originals_preserved=not changed and not missing)


def audit(source, run):
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    if revision != REVISION:
        raise ValueError('Source must match pinned revision')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=source, text=True).strip():
        raise ValueError('Source must be clean')
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=source).decode().split('\0')[:-1]
    manifest = json.loads((run / 'run.json').read_text())
    results = []
    for case, arm, repeat in manifest['schedule']:
        cell = run / f'{case}--{arm}--{repeat}'
        if not (cell / 'metadata.json').exists():
            results.append(dict(cell=cell.name, status='no_completed_record'))
            continue
        meta = json.loads((cell / 'metadata.json').read_text())
        row = dict(cell=cell.name, completed=meta['completed'], base_revision_matches=meta['base_commit'] == REVISION)
        row.update(compare_files(source, cell / 'project', names))
        row['skill_digest_matches'] = meta.get('skill_sha256') == (manifest['skill_sha256'] if arm == 'skill' else None)
        row['patch_rejection_recorded'] = 'patch rejected' in (cell / 'stderr.txt').read_text().lower()
        row['source_manifest_sha256'] = hashlib.sha256('\n'.join(names).encode()).hexdigest()
        results.append(row)
    return dict(upstream_revision=revision, tracked_file_count=len(names), cells=results,
                limitation='Final snapshots cannot prove no transient edits or outside writes. Review full command traces and behavioral claims separately. No completed record does not imply a stopped process.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.source, args.run)
    rendered = json.dumps(result, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as handle:
            handle.write(rendered)
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
