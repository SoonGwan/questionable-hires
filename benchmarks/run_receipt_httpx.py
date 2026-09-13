#!/usr/bin/env python3
"""Run the frozen seeded HTTPX Receipt pair using the existing cell runner."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shlex

from prepare_httpx_receipt import CHECKS, TARGET
from run import ROOT, command, disabled_skills, run_cell
from run_httpx import freeze_skill

SKILL_REVISION = '562c25acbc58b601cb36aaabab2eb724e130f6a5'
SEEDED_REVISION = '8ed44f4f3d3c06bc408b378e435f9e106a7d4254'


def task(python):
    test_command = shlex.join([str(python), '-B', '-m', 'pytest', '-q', '-p',
                               'no:cacheprovider', *CHECKS])
    return ('This is an authored seeded defect in an HTTPX checkout, not an upstream incident. '
            'Fix URL.copy_set_param in httpx/_urls.py so setting an existing query key replaces '
            'its value instead of appending a duplicate. Preserve the public API and neighboring '
            'add/remove behavior. Run the following unchanged native tests before production '
            'edits, capture the defect-specific assertion failure, then fix only httpx/_urls.py '
            'and rerun the same command. Preserve all other existing files, including tests. '
            'Review the focused diff and report actual before/after outcomes. Do not install '
            'dependencies, use network access, change interpreter/environment settings or '
            'perform a general audit. Any necessary diagnostic artifacts must stay inside '
            'this project. Use this preinstalled interpreter for all Python commands.\n\n' + test_command)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixture', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    fixture = args.fixture.resolve()
    data = json.loads((fixture / 'fixture.json').read_text())
    source = fixture / 'project'
    if data['seeded_revision'] != SEEDED_REVISION or command(['git', 'rev-parse', 'HEAD'], source) != SEEDED_REVISION:
        raise ValueError('Unexpected seeded revision')
    if command(['git', 'status', '--porcelain'], source):
        raise ValueError('Prepared source changed')
    for name, digest in data['original_sha256'].items():
        expected = data['seeded_target_sha256'] if name == TARGET else digest
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Prepared input changed: ' + name)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    hashes = freeze_skill(ROOT, SKILL_REVISION, output / 'skills/receipt', 'receipt')
    case = dict(id='httpx-set-param-fix', skill='receipt', task=task(data['interpreter']))
    manifest = dict(revision=command(['git', 'rev-parse', 'HEAD'], ROOT),
                    fixture=data, skill_revision=SKILL_REVISION, skill_files_sha256=hashes,
                    task=case['task'], model='gpt-6-astra', effort='medium', repeats=1,
                    jobs=1, timeout_seconds=240, schedule=['baseline', 'skill'],
                    started_at=datetime.now(timezone.utc).isoformat(), completed_cells=[])
    def save():
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    save()
    disabled = disabled_skills()
    for arm in manifest['schedule']:
        result = run_cell(case, arm, 1, output, 'gpt-6-astra', 'medium', 240,
                          disabled, output / 'skills', source)
        manifest['completed_cells'].append(dict(arm=arm, completed=result['completed']))
        save()
        print(arm, result['completed'], result['elapsed_seconds'], flush=True)
        if result['limit_detected']:
            manifest['stopped_after_limit'] = True
            save()
            raise SystemExit('Account limit; remaining cells unattempted, no retry')
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    save()
    if not all(row['completed'] for row in manifest['completed_cells']):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
