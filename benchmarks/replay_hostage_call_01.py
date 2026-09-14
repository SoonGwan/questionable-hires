#!/usr/bin/env python3
"""Separate author reconciliation/replay; cannot fill absent original output."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

RESOURCE = '4deb638'


def inventory(root):
    assert not any(p.is_symlink() for p in root.rglob('*'))
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def replay(run):
    bench = Path(__file__).resolve().parent
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and len(manifest['schedule']) == 2
    cases = bench / 'bundle-contract-v2-cases.json'
    assert hashlib.sha256(cases.read_bytes()).hexdigest() == manifest['cases_sha256']
    case = next(c for c in json.loads(cases.read_text()) if c['id'] == 'necessary-state')
    report = {'kind': 'author reconciliation and replay, not original model output',
              'resource': RESOURCE, 'cells': [], 'checks': []}
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        terminal = [e['usage'] for e in events if e['type'] == 'turn.completed']
        if meta['completed']:
            assert terminal == [meta['usage']] and not meta['timed_out']
        else:
            assert not terminal and meta['usage'] is None
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        for path, entry in meta['installed_resources_before'].items():
            source = subprocess.check_output(['git', 'show', RESOURCE + ':skills/' + path])
            assert hashlib.sha256(source).hexdigest() == entry['sha256']
        project = cell / 'project'
        before = inventory(project)
        assert (project / 'requirements.md').read_text() == case['files']['requirements.md']
        if meta['arm'] == 'baseline':
            assert set(before) == set(case['files'])
            assert (project / 'form.py').read_text() == case['files']['form.py']
        else:
            assert set(before) == {'form.py', 'requirements.md', 'tests/__init__.py',
                                   'tests/test_form.py', 'tests/controlled_call.py'}
            asset = subprocess.check_output(['git', 'show', RESOURCE + ':skills/hostage-negotiator/assets/controlled_call.py'])
            assert (project / 'tests/controlled_call.py').read_bytes() == asset
            source = (project / 'form.py').read_text()
            guard = '        if self.pending:\n            return\n'
            cleanup = '        finally:\n            self.pending = False'
            assert source.count(guard) == source.count(cleanup) == 1
            variants = {'original': case['files']['form.py'], 'final': source,
                        'missing_guard': source.replace(guard, ''),
                        'missing_cleanup': source.replace(cleanup, '        finally:\n            pass')}
            for variant, implementation in variants.items():
                with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                    scratch = Path(temporary) / 'project'
                    shutil.copytree(project, scratch)
                    (scratch / 'form.py').write_text(implementation)
                    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-v']
                    result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=15)
                    output = (result.stdout + result.stderr).replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')
                    matched = (result.returncode == (0 if variant == 'final' else 1)
                               and 'Ran 6 tests' in output)
                    assert matched, (variant, result.returncode, output)
                    for path in ('tests/test_form.py', 'tests/controlled_call.py', 'tests/__init__.py'):
                        assert (scratch / path).read_bytes() == (project / path).read_bytes()
                    report['checks'].append({'cell': name, 'variant': variant, 'command': command,
                                             'exit_code': result.returncode, 'output': output,
                                             'expected_outcome_matched': matched})
        assert inventory(project) == before
        report['cells'].append({'cell': name, 'completed': meta['completed'],
                                'timed_out': meta['timed_out'], 'usage': meta['usage'],
                                'elapsed_seconds': meta['elapsed_seconds'],
                                'raw_resources_reconciled': True, 'inventory_sha256': before,
                                'errors': [e for e in events if e['type'] == 'error']})
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output exists')
    report = replay(args.run.resolve())
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('Reconciled both cells; four separate native controls matched')
