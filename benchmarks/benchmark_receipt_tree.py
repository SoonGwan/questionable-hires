#!/usr/bin/env python3
"""Compare trusted Receipt revisions with real Git and actual isolated tests."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time
import types

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'skills/receipt/scripts/compare.py'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-revision', required=True, help='Trusted local commit to execute')
    args = parser.parse_args()
    revision = subprocess.check_output(['git', 'rev-parse', '--verify', args.baseline_revision + '^{commit}'], cwd=ROOT, text=True).strip()
    baseline = types.ModuleType('receipt_baseline')
    exec(subprocess.check_output(['git', 'show', revision + ':' + SCRIPT], cwd=ROOT), baseline.__dict__)
    spec = importlib.util.spec_from_file_location('receipt_candidate', ROOT / SCRIPT)
    candidate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate)
    for count in (1, 3, 10):
        with tempfile.TemporaryDirectory(prefix='qh-receipt-bench-') as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=root, text=True).strip()
            git('init', '-q', '--template=')
            git('config', 'user.name', 'Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            git('config', 'commit.gpgsign', 'false')
            git('config', 'core.hooksPath', str(root / 'no-hooks'))
            names = [f'config_{i}.txt' for i in range(count)]
            (root / 'implementation.py').write_text('from pathlib import Path\ndef values():\n    return [int(Path(name).read_text()) for name in ' + repr(names) + ']\n')
            (root / 'test_values.py').write_text('import unittest\nfrom implementation import values\nclass Values(unittest.TestCase):\n    def test_values(self):\n        self.assertEqual(values(), ' + repr([1] * count) + ')\n')
            revisions = []
            for value in ('0', '1'):
                for name in names:
                    (root / name).write_text(value)
                git('add', '.')
                git('commit', '-qm', 'configuration ' + value)
                revisions.append(git('rev-parse', 'HEAD'))
            recipe = dict(fixed=['implementation.py', 'test_values.py'], vary=names,
                          imports=['implementation'], runner='unittest', tests=['-v', 'test_values'],
                          before=revisions[0], after=revisions[1])
            originals = {name: (root / name).read_bytes() for name in names + recipe['fixed']}
            times = {'baseline': [], 'candidate': []}
            calls = {'baseline': [], 'candidate': []}
            for repeat in range(3):
                order = ('baseline', 'candidate') if repeat % 2 == 0 else ('candidate', 'baseline')
                for label in order:
                    module = baseline if label == 'baseline' else candidate
                    original_git = module.git
                    counter = []
                    def observed(repo, *args):
                        counter.append(args[0])
                        return original_git(repo, *args)
                    module.git = observed
                    try:
                        start = time.perf_counter()
                        result = module.compare(root, recipe, timeout=5)
                        elapsed = time.perf_counter() - start
                    finally:
                        module.git = original_git
                    assert result['revisions'] == dict(before=revisions[0], after=revisions[1])
                    assert result['status'] == 'observed'
                    assert result['fixed_sha256'] == {
                        name: hashlib.sha256(originals[name]).hexdigest() for name in recipe['fixed']}
                    for stage, code in (('before', 1), ('after', 0)):
                        check = result['checks'][stage]
                        assert check['exit_code'] == code and not check['timed_out']
                        assert 'Ran 1 test' in check['output']
                        assert 'Verified copied import: implementation' in check['output']
                        assert ('AssertionError' in check['output']) == (stage == 'before')
                    times[label].append(elapsed)
                    calls[label].append(dict(total=len(counter), tree=counter.count('ls-tree')))
            assert all((root / name).read_bytes() == value for name, value in originals.items())
            assert not git('status', '--porcelain')
            print(json.dumps(dict(files=count, baseline_revision=revision,
                                  candidate_sha256=hashlib.sha256((ROOT / SCRIPT).read_bytes()).hexdigest(),
                                  seconds=times, medians={k: statistics.median(v) for k, v in times.items()},
                                  git_calls=calls, checks='Actual before assertion fails; after passes; originals preserved',
                                  limitation='Local compare function including Git and child tests, not fresh collector startup or model performance. Output durations/temp paths are not byte-identical.')),
                  flush=True)


if __name__ == '__main__':
    main()
