import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
import shutil
import tempfile


class CollectorBenchmarkTests(unittest.TestCase):
    def test_real_git_comparison_checks_full_evidence(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            for name in ('benchmarks/benchmark_history_collector.py', 'skills/necromancer/scripts/trace.py'):
                target = repository / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(root / name, target)
            for args in (('init', '-q', '--template='), ('config', 'user.name', 'Collector Test'),
                         ('config', 'user.email', 'fixture@example.invalid'),
                         ('config', 'commit.gpgsign', 'false'),
                         ('config', 'core.hooksPath', str(repository / 'no-hooks')),
                         ('add', '.'), ('commit', '-qm', 'collector snapshot')):
                subprocess.run(['git', *args], cwd=repository, check=True, capture_output=True)
            result = subprocess.run(
                [sys.executable, '-B', 'benchmarks/benchmark_history_collector.py',
                 '--baseline-revision', 'HEAD'], cwd=repository, capture_output=True,
                text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report['evidence_identical'])
        self.assertEqual(report['current_file_bytes'], 1100000)
        self.assertEqual(report['candidate_sha256'], hashlib.sha256(
            (root / 'skills/necromancer/scripts/trace.py').read_bytes()).hexdigest())
        for name in ('baseline', 'candidate'):
            self.assertEqual(len(report['seconds'][name]), 3)
            self.assertTrue(all(value > 0 for value in report['seconds'][name]))
        # Do not assert timing superiority: the benchmark must retain regressions.


if __name__ == '__main__':
    unittest.main()
