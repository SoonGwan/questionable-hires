#!/usr/bin/env python3
"""Post-timing reconciliation including incomplete cells; never fills model gaps."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from replay_bundle_contract_04 import fingerprint

RESOURCE = '07fa9e2'


def reconcile(run, fixture):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and len(manifest['schedule']) == 2
    assert hashlib.sha256(fixture.read_bytes()).hexdigest() == manifest['cases_sha256']
    case, = json.loads(fixture.read_text())
    rows = []
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        terminal = [event['usage'] for event in events if event['type'] == 'turn.completed']
        if meta['completed']:
            assert terminal == [meta['usage']] and not meta['timed_out']
        else:
            assert not terminal and meta['usage'] is None
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(
            str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        for path, entry in meta['installed_resources_before'].items():
            source = subprocess.check_output(['git', 'show', RESOURCE + ':skills/' + path])
            assert hashlib.sha256(source).hexdigest() == entry['sha256']
        project = cell / 'project'
        inventory = fingerprint(project)
        changed = sorted(path for path, source in case['files'].items()
                         if (project / path).read_bytes() != source.encode())
        expected = ['apps/reports/exporter.py', 'tests/test_export.py'] if case['skill'] == 'hostage-negotiator' else []
        assert changed == expected
        assert sorted(inventory) == sorted(case['files'])
        rows.append({'cell': name, 'completed': meta['completed'],
                     'timed_out': meta['timed_out'], 'usage': meta['usage'],
                     'elapsed_seconds': meta['elapsed_seconds'],
                     'raw_and_resources_reconciled': True,
                     'changed_originals': changed, 'inventory_sha256': inventory,
                     'error_events': [event for event in events if event['type'] == 'error']})
    return case, rows


def replay(atomic, store):
    root = Path(__file__).resolve().parent
    case, atomic_rows = reconcile(atomic, root / 'hostage-atomic-export-local-temp-cases.json')
    _, store_rows = reconcile(store, root / 'landlord-check-scope-cases.json')
    report = {'kind': 'separate post-timing author checks', 'resource': RESOURCE,
              'cells': atomic_rows + store_rows, 'checks': []}
    original_methods = {node.name: ast.dump(node) for node in ast.walk(
        ast.parse(case['files']['tests/test_export.py'])) if isinstance(node, ast.FunctionDef)}
    for row in atomic_rows:
        project = atomic / row['cell'] / 'project'
        before = fingerprint(project)
        methods = {node.name: ast.dump(node) for node in ast.walk(
            ast.parse((project / 'tests/test_export.py').read_text())) if isinstance(node, ast.FunctionDef)}
        assert all(methods[name] == body for name, body in original_methods.items())
        for variant in ('before', 'after'):
            with tempfile.TemporaryDirectory(prefix='author-replay-', dir=atomic) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch)
                if variant == 'before':
                    (scratch / 'apps/reports/exporter.py').write_text(case['files']['apps/reports/exporter.py'])
                command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v']
                result = subprocess.run(command, cwd=scratch, capture_output=True,
                                        text=True, timeout=15)
                output = (result.stdout + result.stderr).replace(str(scratch), '<REPLAY>').replace(
                    str(Path.home()), '<HOME>')
                expected = int(variant == 'before')
                matched = result.returncode == expected and 'Ran 3 tests' in output
                if expected:
                    matched = matched and 'AssertionError' in output and 'FAILED (failures=' in output
                assert (scratch / 'tests/test_export.py').read_bytes() == (project / 'tests/test_export.py').read_bytes()
                report['checks'].append({'cell': row['cell'], 'variant': variant,
                                          'command': command, 'exit_code': result.returncode,
                                          'matched': matched, 'output': output})
        assert fingerprint(project) == before
    report['retained_projects_unchanged'] = True
    report['original_test_methods_preserved'] = True
    report['all_replays_matched'] = all(check['matched'] for check in report['checks'])
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atomic', type=Path, required=True)
    parser.add_argument('--store', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author attempt')
    report = replay(args.atomic.resolve(), args.store.resolve())
    with args.output.open('x') as output:
        json.dump(report, output, indent=2)
        output.write('\n')
    print(json.dumps({'cells': len(report['cells']), 'checks': len(report['checks']),
                      'all_replays_matched': report['all_replays_matched']}))
