#!/usr/bin/env python3
"""Author-only frozen keyed-publication reconciliation and native controls."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from replay_hostage_call_01 import inventory

RESOURCE = 'a1a258c'


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and len(manifest['schedule']) == 2
    fixture = Path(__file__).resolve().parent / 'hostage-keyed-publish-cases.json'
    assert hashlib.sha256(fixture.read_bytes()).hexdigest() == manifest['cases_sha256']
    case, = json.loads(fixture.read_text())
    report = {'kind': 'separate author reconciliation/replay, not original output',
              'resource': RESOURCE, 'cells': [], 'checks': []}
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        assert [e['usage'] for e in events if e['type'] == 'turn.completed'] == [meta['usage']]
        assert meta['completed'] and not meta['timed_out']
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        for path, entry in meta['installed_resources_before'].items():
            source = subprocess.check_output(['git', 'show', RESOURCE + ':skills/' + path])
            assert hashlib.sha256(source).hexdigest() == entry['sha256']
        project = cell / 'project'
        before = inventory(project)
        expected = set(case['files']) | {'tests/test_publisher_regressions.py'}
        if meta['arm'] == 'skill':
            expected.add('tests/controlled_call.py')
            asset = subprocess.check_output(['git', 'show', RESOURCE + ':skills/hostage-negotiator/assets/controlled_call.py'])
            assert (project / 'tests/controlled_call.py').read_bytes() == asset
        assert set(before) == expected
        for path, source in case['files'].items():
            if path != 'app/publisher.py':
                assert (project / path).read_text() == source
        source = (project / 'app/publisher.py').read_text()
        condition = 'if document_id in self._in_flight:'
        cleanup = '            self._in_flight.remove(document_id)'
        assert source.count(condition) == source.count(cleanup) == 1
        variants = {'original': case['files']['app/publisher.py'], 'final': source,
                    'global_busy': source.replace(condition, 'if self._in_flight:'),
                    'missing_cleanup': source.replace(cleanup, '            pass')}
        for variant, implementation in variants.items():
            with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch)
                (scratch / 'app/publisher.py').write_text(implementation)
                command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v']
                result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                output = (result.stdout + result.stderr).replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')
                matched = result.returncode == (0 if variant == 'final' else 1) and 'Ran 9 tests' in output
                assert matched, (name, variant, output)
                for path in before:
                    if path != 'app/publisher.py':
                        assert (scratch / path).read_bytes() == (project / path).read_bytes()
                report['checks'].append({'cell': name, 'variant': variant, 'exit_code': result.returncode,
                                         'command': command, 'output': output, 'expected_outcome_matched': matched})
        assert inventory(project) == before
        report['cells'].append({'cell': name, 'usage': meta['usage'], 'elapsed_seconds': meta['elapsed_seconds'],
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
    args.output.write_text(json.dumps(replay(args.run.resolve()), indent=2) + '\n')
    print('Both cells reconcile; eight separate native outcomes match')
