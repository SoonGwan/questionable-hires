#!/usr/bin/env python3
"""Frozen Python adoption reconciliation; separate from original model output."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from replay_hostage_call_01 import inventory

RESOURCE = '08a8f6e'


def frozen(path):
    return subprocess.check_output(['git', 'show', RESOURCE + ':' + path])


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and manifest['revision'].startswith(RESOURCE)
    assert manifest['schedule'] == ['necessary-state--skill--1']
    cases = frozen('benchmarks/bundle-contract-v2-cases.json')
    assert hashlib.sha256(cases).hexdigest() == manifest['cases_sha256']
    case = next(c for c in json.loads(cases) if c['id'] == 'necessary-state')
    cell = run / manifest['schedule'][0]
    meta = json.loads((cell / 'metadata.json').read_text())
    raw = (cell / 'stdout.original.jsonl').read_text()
    events = [json.loads(line) for line in raw.splitlines()]
    assert [e['usage'] for e in events if e['type'] == 'turn.completed'] == [meta['usage']]
    assert meta['completed'] and not meta['timed_out']
    assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
    assert meta['installed_resources_before'] == meta['installed_resources_after']
    for name, info in meta['installed_resources_before'].items():
        assert hashlib.sha256(frozen('skills/' + name)).hexdigest() == info['sha256']
    project = cell / 'project'
    original = inventory(project)
    assert set(original) == {'form.py', 'requirements.md', 'tests/__init__.py',
                             'tests/test_form.py', 'tests/controlled_call.py'}
    assert (project / 'requirements.md').read_text() == case['files']['requirements.md']
    assert (project / 'tests/controlled_call.py').read_bytes() == frozen('skills/hostage-negotiator/assets/controlled_call.py')
    source = (project / 'form.py').read_text()
    guard = '        if self.pending:\n            return\n'
    cleanup = '        finally:\n            self.pending = False'
    assert source.count(guard) == source.count(cleanup) == 1
    variants = {'final': source, 'original': case['files']['form.py'],
                'missing_guard': source.replace(guard, ''),
                'missing_cleanup': source.replace(cleanup, '        finally:\n            pass'),
                # Post-run specificity control: duplicate return is unspecified.
                # Preserve normal results, suppression and pending ownership.
                'valid_duplicate_false': source.replace(guard, guard.rstrip() + ' False\n')}
    report = dict(kind='separate author replay, not model evidence', resource=RESOURCE,
                  usage_resources_reconciled=True, inventory=original, checks=[])
    for variant, implementation in variants.items():
        with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
            scratch = Path(temporary) / 'project'
            shutil.copytree(project, scratch)
            (scratch / 'form.py').write_text(implementation)
            command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-v']
            try:
                result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                code, output, timeout = result.returncode, result.stdout + result.stderr, False
            except subprocess.TimeoutExpired as error:
                def text(value):
                    return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                code, output, timeout = None, text(error.stdout) + text(error.stderr), True
            unchanged = all((scratch / p).read_bytes() == (project / p).read_bytes()
                            for p in original if p != 'form.py')
            expected = 0 if variant in ('final', 'valid_duplicate_false') else 1
            report['checks'].append(dict(variant=variant, expected_exit=expected,
                exit_code=code, timed_out=timeout, test_sources_unchanged=unchanged,
                native_counts=re.findall(r'Ran (\d+) tests? in ', output),
                contract_matched=code == expected and not timeout and unchanged
                    and re.findall(r'Ran (\d+) tests? in ', output) == ['6'],
                replacement_source=implementation,
                output=output.replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')))
    assert inventory(project) == original
    report['retained_project_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = replay(args.run)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    for check in report['checks']:
        print(check['variant'], check['exit_code'], 'contract_matched=', check['contract_matched'])
