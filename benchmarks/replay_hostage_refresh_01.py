#!/usr/bin/env python3
"""Separate author controls; never reconstruct missing original test evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from hostage_refresh_cases import SOURCE, BROKEN, ORACLE
from replay_hostage_call_01 import inventory


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    revisions = {
        '3c2944362d41c7638a2d39938fb8a8fd92d55db7': {'a': 5, 'b': 8},
        'b237aae19e3466b9a90d9cb38bd40e68d5ab926b': {'a': 7, 'b': 6},
    }
    assert manifest['revision'] in revisions and manifest['finished_at']
    baseline_counts = revisions[manifest['revision']]
    frozen = subprocess.check_output(['git', 'show', manifest['revision'] + ':benchmarks/hostage-refresh-cases.json'])
    assert hashlib.sha256(frozen).hexdigest() == manifest['cases_sha256'] == '7b0bc8120865802a29dd97b6fedb9863bdbe19742ce68bb93307588b55a04c21'
    cases = {case['id']: case for case in json.loads(frozen)}
    # Same specified behavior with non-unit generation increments: tests must
    # inspect observable ownership, not prescribe an internal counter value.
    alternative = SOURCE.replace('self.generation += 1', 'self.generation += 2')
    report = dict(kind='author controls, not original model evidence', revision=manifest['revision'], cells=[], checks=[])
    for cell in sorted(run.glob('*--*')):
        meta = json.loads((cell / 'metadata.json').read_text())
        events = [json.loads(line) for line in (cell / 'stdout.original.jsonl').read_text().splitlines()]
        assert [e['usage'] for e in events if e.get('type') == 'turn.completed'] == [meta['usage']]
        assert meta['completed'] and not meta['timed_out'] and not meta['limit_detected']
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        project = cell / 'project'
        before = inventory(project)
        case = cases[meta['case']]
        for name in ('notes.txt', 'requirements.md'):
            assert (project / name).read_text() == case['files'][name]
        assert (project / 'preview.py').read_text() == SOURCE
        report['cells'].append(dict(cell=cell.name, usage=meta['usage'], elapsed_seconds=meta['elapsed_seconds'], inventory=before))
        for variant, source in [('final', SOURCE), ('broken_owner', BROKEN), ('valid_counter_step', alternative), ('author_oracle_final', SOURCE)]:
            with tempfile.TemporaryDirectory(prefix='author-refresh-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                if variant == 'author_oracle_final':
                    scratch.mkdir()
                    (scratch / 'test_preview.py').write_text(ORACLE)
                else:
                    shutil.copytree(project, scratch)
                (scratch / 'preview.py').write_text(source)
                try:
                    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'], cwd=scratch, capture_output=True, text=True, timeout=20)
                    code, output, timeout = result.returncode, result.stdout + result.stderr, False
                except subprocess.TimeoutExpired as error:
                    def decode(value):
                        return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                    code, output, timeout = None, decode(error.stdout) + decode(error.stderr), True
                count = (6 if variant == 'author_oracle_final' else
                         baseline_counts[meta['case'][-1]] if meta['arm'] == 'baseline' else 8)
                expected = 1 if variant == 'broken_owner' else 0
                counts = re.findall(r'Ran (\d+) tests? in ', output)
                tests_unchanged = variant == 'author_oracle_final' or all((scratch / p).read_bytes() == (project / p).read_bytes() for p in before if p != 'preview.py')
                matched = code == expected and not timeout and counts == [str(count)] and tests_unchanged
                if variant == 'broken_owner':
                    matched = matched and bool(re.search(r'AssertionError: False is not [Tt]rue', output)) and 'ERROR:' not in output
                report['checks'].append(dict(cell=cell.name, variant=variant, exit_code=code, timed_out=timeout, native_counts=counts, expected_exit=expected, expected_count=count, tests_unchanged=tests_unchanged, matched=matched, output=output.replace(str(scratch), '<REPLAY>')))
        assert inventory(project) == before
    report['original_projects_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite prior observations')
    report = replay(args.run.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps([dict(cell=c['cell'], variant=c['variant'], matched=c['matched'], counts=c['native_counts']) for c in report['checks']], indent=2))
