#!/usr/bin/env python3
"""Reconcile raw evidence for unchanged-fixture reviews; does not score correctness."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def reconcile(run, cases_file, resource):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'], 'Timing must finish before reconciliation'
    assert hashlib.sha256(cases_file.read_bytes()).hexdigest() == manifest['cases_sha256']
    cases = {case['id']: case for case in json.loads(cases_file.read_text())}
    report = {'kind': 'author raw/resource/snapshot reconciliation, not task scoring',
              'resource': resource, 'cells': []}
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        usage = [event['usage'] for event in events if event['type'] == 'turn.completed']
        if meta['completed']:
            assert usage == [meta['usage']] and not meta['timed_out']
        else:
            assert not usage and meta['usage'] is None
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(
            str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        for path, entry in meta['installed_resources_before'].items():
            source = subprocess.check_output(['git', 'show', resource + ':skills/' + path])
            assert hashlib.sha256(source).hexdigest() == entry['sha256']
        project = cell / 'project'
        expected = cases[meta['case']]['files']
        assert not any(path.is_symlink() for path in project.rglob('*')), 'Unsupported snapshot symlink'
        inventory = {path.relative_to(project).as_posix(): path.read_bytes()
                     for path in project.rglob('*') if path.is_file()}
        # This tool intentionally supports only reviews retaining exactly the
        # supplied files. Experiments/implementation tasks need different checks.
        assert inventory == {path: source.encode() for path, source in expected.items()}, name
        report['cells'].append({
            'cell': name, 'completed': meta['completed'], 'timed_out': meta['timed_out'],
            'usage': meta['usage'], 'elapsed_seconds': meta['elapsed_seconds'],
            'raw_usage_resources_reconciled': True, 'snapshot_matches_fixture': True,
            'inventory_sha256': {path: hashlib.sha256(source).hexdigest()
                                 for path, source in inventory.items()},
            'errors': [event for event in events if event['type'] == 'error']})
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--cases-file', type=Path, required=True)
    parser.add_argument('--resource', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author report')
    report = reconcile(args.run.resolve(), args.cases_file, args.resource)
    with args.output.open('x') as output:
        json.dump(report, output, indent=2)
        output.write('\n')
    print('Reconciled', len(report['cells']), 'scheduled cells; manual native review still required')
