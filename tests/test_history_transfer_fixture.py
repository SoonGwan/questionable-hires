import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HistoryTransferFixtureTests(unittest.TestCase):
    def test_contract_and_contiguous_history(self):
        fixture = load('history_transfer', 'benchmarks/history_transfer_cases.py')
        runner = load('history_runner', 'benchmarks/run.py')
        for case in fixture.cases():
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory() as temporary:
                project = Path(temporary) / 'project'
                runner.prepare(case, project)
                baseline = subprocess.run(['python3', '-B', '-m', 'unittest', '-v'],
                    cwd=project, capture_output=True, text=True, timeout=10)
                self.assertEqual(baseline.returncode, 0, baseline.stderr)
                probe = ('import consumer\n'
                         'consumer.label = lambda record: record["display"]\n'
                         'import unittest\n'
                         'result = unittest.TextTestRunner().run(unittest.defaultTestLoader.discover("."))\n'
                         'raise SystemExit(not result.wasSuccessful())\n')
                changed = subprocess.run(['python3', '-B', '-c', probe], cwd=project,
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(changed.returncode, 0 if case['id'].endswith('normalized') else 1)
                if case['id'].endswith('active'):
                    self.assertIn('failures=1, errors=1', changed.stderr)
                patch = runner.command(['git', 'show', '--format=fuller', 'HEAD~1', '--', 'labels.py'], project)
                self.assertEqual(patch.count('\n@@ '), 1)
                self.assertGreater(patch.index('+    return record.get'), 12000)
                self.assertEqual(runner.command(['git', 'status', '--porcelain'], project), '')
