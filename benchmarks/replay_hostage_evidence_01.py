#!/usr/bin/env python3
"""Reconcile handoff evidence and separately exercise retained native tests."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile

RESOURCE = 'fe62f84305a9c521f60124029a455dbd4721757d'


def frozen(path):
    return subprocess.check_output(['git', 'show', RESOURCE + ':' + path])


def inventory(root):
    assert not any(p.is_symlink() for p in root.rglob('*'))
    return {p.relative_to(root).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest(), stat.S_IMODE(p.stat().st_mode))
            for p in root.rglob('*') if p.is_file()}


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and manifest['revision'] == RESOURCE
    expected_schedule = [f'evidence-{s}--skill--1' for s in ('matching', 'stale', 'absent')]
    assert manifest['schedule'] == expected_schedule
    source = frozen('benchmarks/hostage-evidence-cases.json')
    assert hashlib.sha256(source).hexdigest() == manifest['cases_sha256']
    cases = {c['id']: c for c in json.loads(source)}
    report = dict(kind='separate author reconciliation/replay, not original model output', resource=RESOURCE,
                  cells=[], checks=[])
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        case = cases[meta['case']]
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        assert meta['completed'] and not meta['timed_out'] and meta['exit_code'] == 0
        assert [e['usage'] for e in events if e['type'] == 'turn.completed'] == [meta['usage']]
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        for p, entry in meta['installed_resources_before'].items():
            assert hashlib.sha256(frozen('skills/' + p)).hexdigest() == entry['sha256']
            mode = subprocess.check_output(['git', 'ls-tree', RESOURCE, '--', 'skills/' + p]).split()[0]
            assert stat.S_IMODE(int(mode, 8)) == entry['mode']
        project = cell / 'project'
        before = inventory(project)
        # Stale model repair restores exactly the earlier valid implementation.
        assert before == {p: (hashlib.sha256(s.encode()).hexdigest(), 0o644) for p, s in case['files'].items()}
        commands = [e['item'] for e in events if e['type'] == 'item.completed'
                    and e.get('item', {}).get('type') == 'command_execution']
        reads = '\n'.join(c['aggregated_output'] for c in commands[:-1])
        for p, content in dict(case['files'], **case.get('working_files', {})).items():
            if content:
                assert content in reads, (name, p)
        initial_changed = sorted(case.get('working_files', {}))
        if initial_changed:
            assert meta['initial_working_files'] == {p: hashlib.sha256(s.encode()).hexdigest()
                                                      for p, s in case['working_files'].items()}
        report['cells'].append(dict(cell=name, raw_usage_resources_inventory_reconciled=True,
            restored_working_files=initial_changed, original_file_modes_preserved=True,
            total_tokens=meta['usage']['input_tokens'] + meta['usage']['output_tokens'],
            elapsed_seconds=meta['elapsed_seconds'], inventory_sha256_modes=before))
        variants = {'final': (project / 'form.py').read_text()}
        if initial_changed:
            variants['initial_missing_cleanup'] = case['working_files']['form.py']
        for variant, code in variants.items():
            with tempfile.TemporaryDirectory(prefix='handoff-replay-', dir=run) as directory:
                scratch = Path(directory) / 'project'
                shutil.copytree(project, scratch)
                (scratch / 'form.py').write_text(code)
                inputs = inventory(scratch)
                process = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'],
                    cwd=scratch, capture_output=True, text=True, timeout=15)
                output = process.stdout + process.stderr
                expected = int(variant != 'final')
                assert process.returncode == expected and 'Ran 6 tests' in output, output
                if expected:
                    assert 'FAILED (failures=6)' in output and 'AssertionError: True is not False' in output
                else:
                    assert '\nOK\n' in output and output.count(' ... ok\n') == 6
                assert inventory(scratch) == inputs
                report['checks'].append(dict(cell=name, variant=variant, native_test_count=6,
                    exit_code=process.returncode, expected_exit=expected, test_sources_unchanged=True,
                    output=output.replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')))
        assert inventory(project) == before
    absent = run / 'evidence-absent--skill--1'
    events = [json.loads(l) for l in (absent / 'stdout.original.jsonl').read_text().splitlines()]
    item = next(e['item'] for e in events if e['type'] == 'item.completed' and e.get('item', {}).get('id') == 'item_4')
    assert 'Ran 6 tests' not in item['aggregated_output']
    assert 'NATIVE_SUITE_EXIT=' not in item['aggregated_output']
    report['original_absent_case_gap'] = dict(item='item_4', output=item['aggregated_output'],
        limitation='Missing already in raw CLI stdout, not removed by export/redaction. Model-visible tool output is not independently available.')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author attempt')
    result = replay(args.run.resolve())
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('3 cells reconciled; 4 native replay outcomes matched; original capture gap preserved.')
