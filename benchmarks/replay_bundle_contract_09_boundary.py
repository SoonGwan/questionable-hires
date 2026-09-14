#!/usr/bin/env python3
"""Replay unchanged boundary tests against actual and adjacent faulty implementations."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from replay_bundle_contract_09_form import REVISION, CASES_SHA, inventory


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['revision'] == REVISION and manifest['finished_at']
    frozen = subprocess.check_output(['git', 'show', REVISION + ':benchmarks/bundle-contract-v2-cases.json'])
    assert hashlib.sha256(frozen).hexdigest() == CASES_SHA == manifest['cases_sha256']
    case = next(c for c in json.loads(frozen) if c['id'] == 'boundary-fix')
    report = dict(kind='separate retained-test controls, not original model execution', revision=REVISION, checks=[])
    for arm in ('baseline', 'skill'):
        cell = run / ('boundary-fix--' + arm + '--1')
        project = cell / 'project'
        before = inventory(project)
        assert set(before) == {'eligibility.py', 'test_eligibility.py'}
        final = (project / 'eligibility.py').read_text()
        assert final == 'def eligible(age):\n    return age >= 18\n'
        variants = {'final': (final, 0), 'original': (case['files']['eligibility.py'], 1),
                    'admits_minor': (final.replace('>= 18', '>= 17'), 1),
                    'rejects_adult': (final.replace('>= 18', '== 18'), 1)}
        for variant, (implementation, expected) in variants.items():
            with tempfile.TemporaryDirectory(prefix='author-boundary-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch)
                (scratch / 'eligibility.py').write_text(implementation)
                command = [sys.executable, '-B', '-m', 'unittest', '-v']
                result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                output = result.stdout + result.stderr
                assert (scratch / 'test_eligibility.py').read_bytes() == (project / 'test_eligibility.py').read_bytes()
                counts = re.findall(r'Ran (\d+) tests? in ', output)
                report['checks'].append(dict(cell=cell.name, variant=variant,
                    expected_exit=expected, exit_code=result.returncode,
                    counts=counts, inventory_sha256=before, implementation=implementation,
                    test_source=(project / 'test_eligibility.py').read_text(), command=command,
                    matched=(result.returncode == expected and counts == ['3']
                             and (not expected or 'AssertionError:' in output)),
                    output=output.replace(str(scratch), '<REPLAY>')))
        assert inventory(project) == before
    report['retained_projects_unchanged'] = True
    report['all_matched'] = all(c['matched'] for c in report['checks'])
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
    print(json.dumps(dict(checks=len(report['checks']), all_matched=report['all_matched'])))
