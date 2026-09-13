#!/usr/bin/env python3
"""Unchanged-test author replay after checkpoint 05; never model evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from replay_bundle_contract_04 import GUARDED, fingerprint


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest.get('finished_at') and len(manifest['schedule']) == 18
    report = {'kind': 'post-timing author replay, not missing model evidence',
              'cells': [], 'replays': []}
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        usage = next(e['usage'] for e in reversed(events) if e['type'] == 'turn.completed')
        assert usage == meta['usage'] and meta['completed'] and not meta['timed_out']
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(
            str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        for path, entry in meta['installed_resources_before'].items():
            source = subprocess.check_output(['git', 'show', 'd4a52ef:skills/' + path])
            assert hashlib.sha256(source).hexdigest() == entry['sha256']
        report['cells'].append({'cell': name, 'usage_events_resources_reconciled': True,
                               'total_tokens': usage['input_tokens'] + usage['output_tokens'],
                               'elapsed_seconds': meta['elapsed_seconds']})

    for case in ('search-order', 'search-protected', 'necessary-state'):
        for arm in ('baseline', 'skill'):
            name = f'{case}--{arm}--1'
            project = run / name / 'project'
            before = fingerprint(project)
            variants = ('original', 'guarded') if case.startswith('search-') else ('original',)
            for variant in variants:
                with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                    scratch = Path(temporary) / 'project'
                    shutil.copytree(project, scratch)
                    if variant == 'guarded':
                        (scratch / 'search.py').write_text(GUARDED)
                    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-v']
                    result = subprocess.run(command, cwd=scratch, capture_output=True,
                                            text=True, timeout=15)
                    output = (result.stdout + result.stderr).replace(str(scratch), '<REPLAY>').replace(
                        str(Path.home()), '<HOME>')
                    expected = 1 if case == 'search-order' and variant == 'original' else 0
                    assert result.returncode == expected, output
                    if expected:
                        assert 'AssertionError' in output and 'failures=1' in output, output
                    assert 'Ran 0 tests' not in output and 'Ran ' in output, output
                    assert 'TypeError' not in output and 'RuntimeWarning' not in output, output
                    report['replays'].append({'cell': name, 'variant': variant,
                                              'exit_code': result.returncode, 'output': output})
            assert fingerprint(project) == before
    report['retained_projects_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = replay(args.run.resolve())
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps(result, indent=2))
