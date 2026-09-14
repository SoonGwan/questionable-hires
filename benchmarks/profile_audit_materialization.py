"""Local file-copy cost probe; not model-token evidence."""
import argparse
import importlib.util
import json
from pathlib import Path
import statistics
import sys
import tempfile
import time
from unittest.mock import patch


def measure(script, repeats):
    spec = importlib.util.spec_from_file_location('measured_audit', script)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    samples = []
    parent = Path(__file__).resolve().parent / 'local-runs'
    with tempfile.TemporaryDirectory(prefix='audit-materialization-', dir=parent) as folder:
        root = Path(folder)
        (root / 'service.py').write_text('def value():\n    return 7\n')
        (root / 'test_service.py').write_text('import unittest\nfrom service import value\nclass Tests(unittest.TestCase):\n    def test_value(self):\n        self.assertEqual(value(), 7)\n')
        for group in range(8):
            directory = root / 'data' / str(group)
            directory.mkdir(parents=True)
            for index in range(64):
                (directory / str(index)).write_bytes(b'x' * 2048)
        recipe = dict(files=['service.py', 'test_service.py', 'data'], imports=['service'],
                      tests=['-v', 'test_service'], target='service.py', old='return 7', new='return 8',
                      probe='from service import value\nassert value() == 7, (value(), 7)')
        original_mkdir = Path.mkdir
        for _ in range(repeats):
            mkdir_calls = []
            def recorded(path, *args, **kwargs):
                mkdir_calls.append(str(path))
                return original_mkdir(path, *args, **kwargs)
            start = time.perf_counter()
            with patch.object(Path, 'mkdir', recorded):
                result = helper.audit(root, recipe, python=sys.executable)
            elapsed = time.perf_counter() - start
            assert result['status'] == 'observed'
            assert [result['checks'][name]['exit_code'] for name in ['correct_tests', 'correct_probe', 'mutant_tests', 'mutant_probe']] == [0, 0, 1, 1]
            assert 'AssertionError: 8 != 7' in result['checks']['mutant_tests']['output']
            assert 'AssertionError: (8, 7)' in result['checks']['mutant_probe']['output']
            assert result['integrity']['owned_scratch_removed']
            samples.append(dict(elapsed_seconds=elapsed, mkdir_calls=len(mkdir_calls)))
    return dict(samples=samples, median_seconds=statistics.median(s['elapsed_seconds'] for s in samples),
                selected_files=514, checks_per_sample=4, correctness='pass/pass/assertion-fail/assertion-fail',
                limitation='Authored 1 MiB/514-file fixture, same host, local helper wall time including instrumented mkdir, not model efficiency.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--script', type=Path, required=True)
    parser.add_argument('--repeats', type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.repeats <= 10:
        parser.error('Use 1–10 repeats')
    print(json.dumps(measure(args.script.resolve(), args.repeats), indent=2))
