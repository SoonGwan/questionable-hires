#!/usr/bin/env python3
"""Native retained-form controls, separate from missing original model evidence."""
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

REVISION = '3a7d972d4cfa5cc28a5df44125c55eaeb60aa1b9'
CASES_SHA = '1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65'


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['revision'] == REVISION and manifest['finished_at']
    cases = subprocess.check_output(['git', 'show', REVISION + ':benchmarks/bundle-contract-v2-cases.json'])
    assert hashlib.sha256(cases).hexdigest() == manifest['cases_sha256'] == CASES_SHA
    case = next(c for c in json.loads(cases) if c['id'] == 'necessary-state')
    report = dict(kind='separate author controls; cannot fill original output gaps',
                  revision=REVISION, cases_sha256=CASES_SHA, cells=[], checks=[])
    for arm, count in [('baseline', 7), ('skill', 6)]:
        name = 'necessary-state--' + arm + '--1'
        cell, project = run / name, run / name / 'project'
        meta = json.loads((cell / 'metadata.json').read_text())
        events = [json.loads(line) for line in (cell / 'stdout.original.jsonl').read_text().splitlines()]
        assert [e['usage'] for e in events if e.get('type') == 'turn.completed'] == [meta['usage']]
        before = inventory(project)
        expected_files = ({'form.py', 'requirements.md', 'test_form.py'} if arm == 'baseline'
                          else {'form.py', 'requirements.md', 'tests/test_form.py', 'tests/controlled_call.py'})
        assert set(before) == expected_files
        assert (project / 'requirements.md').read_text() == case['files']['requirements.md']
        if arm == 'skill':
            asset = subprocess.check_output(['git', 'show', REVISION + ':skills/hostage-negotiator/assets/controlled_call.py'])
            assert (project / 'tests/controlled_call.py').read_bytes() == asset
        final = (project / 'form.py').read_text()
        guard = '        if self.pending:\n            return' + (' None' if arm == 'baseline' else '') + '\n'
        cleanup = '        finally:\n            self.pending = False'
        assert final.count(guard) == final.count(cleanup) == 1
        variants = {'final': final, 'original': case['files']['form.py'],
                    'missing_guard': final.replace(guard, ''),
                    'missing_cleanup': final.replace(cleanup, '        finally:\n            pass'),
                    'valid_duplicate_false': final.replace(guard, '        if self.pending:\n            return False\n')}
        report['cells'].append(dict(cell=name, inventory_sha256=before,
            retained_sources={p: (project / p).read_text() for p in sorted(before)},
            original_capture_diagnostics=meta['capture_diagnostics']))
        for variant, source in variants.items():
            with tempfile.TemporaryDirectory(prefix='author-form-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch)
                (scratch / 'form.py').write_text(source)
                command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
                           'tests' if arm == 'skill' else '.', '-v']
                try:
                    result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                    code, output, timed_out = result.returncode, result.stdout + result.stderr, False
                except subprocess.TimeoutExpired as error:
                    def text(value):
                        return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                    code, output, timed_out = None, text(error.stdout) + text(error.stderr), True
                expected_exit = 0 if variant in ('final', 'valid_duplicate_false') else 1
                discovered = re.findall(r'Ran (\d+) tests? in ', output)
                unchanged = all((scratch / p).read_bytes() == (project / p).read_bytes()
                                for p in before if p != 'form.py')
                report['checks'].append(dict(cell=name, variant=variant,
                    command=command, implementation=source, exit_code=code,
                    contract_expected_exit=expected_exit, expected_test_count=count,
                    observed_test_counts=discovered, timed_out=timed_out,
                    test_sources_unchanged=unchanged,
                    contract_matched=(code == expected_exit and not timed_out
                                      and discovered == [str(count)] and unchanged),
                    output=output.replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')))
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
    print(json.dumps([dict(cell=c['cell'], variant=c['variant'], exit=c['exit_code'],
                          matched=c['contract_matched'], counts=c['observed_test_counts'])
                      for c in report['checks']], indent=2))
