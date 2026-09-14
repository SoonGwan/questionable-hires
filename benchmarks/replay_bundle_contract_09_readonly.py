#!/usr/bin/env python3
"""Replay original Python witnesses for history/schema, not complete model sessions."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

from replay_bundle_contract_09_form import REVISION, CASES_SHA, inventory


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['revision'] == REVISION and manifest['finished_at']
    source = subprocess.check_output(['git', 'show', REVISION + ':benchmarks/bundle-contract-v2-cases.json'])
    assert hashlib.sha256(source).hexdigest() == CASES_SHA == manifest['cases_sha256']
    cases = {c['id']: c for c in json.loads(source)}
    report = dict(kind='separate original Python-witness replay; Git commands not rerun',
                  revision=REVISION, checks=[])
    for case in ('history-active', 'rolling-schema'):
        for arm in ('baseline', 'skill'):
            name = case + '--' + arm + '--1'
            cell, project = run / name, run / name / 'project'
            before = inventory(project)
            assert set(before) == set(cases[case]['files'])
            assert all((project / p).read_bytes() == content.encode()
                       for p, content in cases[case]['files'].items())
            events = [json.loads(line) for line in (cell / 'events.jsonl').read_text().splitlines()]
            items = [e['item'] for e in events if e.get('type') == 'item.completed'
                     and e.get('item', {}).get('type') == 'command_execution']
            witnesses = [item for item in items if 'import ' in item['command']]
            assert len(witnesses) == 1
            item = witnesses[0]
            shell = shlex.split(item['command'])[-1]
            if case == 'history-active' and arm == 'baseline':
                words = shlex.split(shell)
                assert words.count('-c') == 1
                program = words[words.index('-c') + 1]
            else:
                matches = re.findall(r"<<'PY'\n(.*?)\nPY(?:\n|$)", shell, re.S)
                assert len(matches) == 1
                program = matches[0]
            with tempfile.TemporaryDirectory(prefix='author-readonly-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch)
                command = [sys.executable, '-B', '-c', program]
                try:
                    result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                    code, out, err, timed_out = result.returncode, result.stdout, result.stderr, False
                except subprocess.TimeoutExpired as error:
                    def text(value):
                        return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                    code, out, err, timed_out = None, text(error.stdout), text(error.stderr), True
                unchanged = inventory(scratch) == before
                # No value/version normalization: a mismatch remains a mismatch.
                captured = bool(out.strip()) and out.strip() in item['aggregated_output']
                report['checks'].append(dict(cell=name, original_native_command=item,
                    witness_source=program, inventory_sha256=before,
                    retained_sources={p: (project / p).read_text() for p in sorted(before)},
                    exit_code=code, timed_out=timed_out, copy_unchanged=unchanged,
                    original_stdout_contains_replayed_output=captured,
                    stdout=out.replace(str(scratch), '<REPLAY>'),
                    stderr=err.replace(str(scratch), '<REPLAY>')))
            assert inventory(project) == before
    report['retained_projects_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author attempt')
    report = replay(args.run.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps([dict(cell=c['cell'], exit=c['exit_code'], unchanged=c['copy_unchanged'],
        stdout_match=c['original_stdout_contains_replayed_output']) for c in report['checks']], indent=2))
