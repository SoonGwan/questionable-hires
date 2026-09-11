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
    def test_decision_gate_requests_share_verified_behavior_and_origin(self):
        fixture = load('decision_gate', 'benchmarks/decision_gate_cases.py')
        runner = load('gate_runner', 'benchmarks/run.py')
        removal, origin = fixture.cases()
        self.assertEqual(removal['files'], origin['files'])
        self.assertEqual(removal['history'], origin['history'])
        self.assertNotEqual(removal['task'], origin['task'])
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / 'project'
            runner.prepare(removal, project)
            original = removal['files']['summary.py']
            changed = original.replace("record.get('code') or 'unknown'", "record['code']")
            for source, expected in [(original, 0), (changed, 1)]:
                probe = ('import consumer, unittest\nnamespace = {}\n'
                         f'exec({source!r}, namespace)\n'
                         "consumer.summarize = namespace['summarize']\n"
                         'result = unittest.TextTestRunner().run(unittest.defaultTestLoader.discover("."))\n'
                         'raise SystemExit(not result.wasSuccessful())\n')
                completed = subprocess.run(['python3', '-B', '-c', probe], cwd=project,
                                           capture_output=True, text=True, timeout=5)
                self.assertEqual(completed.returncode, expected, completed.stderr)
                self.assertIn('Ran 4 tests', completed.stderr)
                if expected:
                    self.assertIn("KeyError: 'code'", completed.stderr)
                    self.assertIn('failures=1, errors=2', completed.stderr)
            patch = runner.command(['git', 'show', 'HEAD~3', '--', 'summary.py'], project)
            self.assertIn("-    code = record['code']", patch)
            self.assertIn("+    code = record.get('code') or 'unknown'", patch)
            self.assertEqual(runner.command(['git', 'status', '--porcelain'], project), '')
            for path, contents in removal['files'].items():
                self.assertEqual((project / path).read_text(), contents)

    def test_three_decisions_have_distinct_current_contract_effects(self):
        fixture = load('history_regions', 'benchmarks/history_region_cases.py')
        runner = load('region_runner', 'benchmarks/run.py')
        case = fixture.cases()[0]
        variants = [('', '', 0),
                    ("record.get('code') or 'unknown'", "record['code']", 1),
                    ("record.get('display_name') or record['name']", "record['display_name']", 0),
                    ("    if amount < 0:\n        raise ValueError('negative amount')\n", '', 1)]
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / 'project'
            runner.prepare(case, project)
            for old, new, expected in variants:
                source = case['files']['summary.py']
                if old:
                    self.assertEqual(source.count(old), 1)
                    source = source.replace(old, new)
                probe = ('import consumer, unittest\nnamespace = {}\n'
                         f'exec({source!r}, namespace)\n'
                         "consumer.summarize = namespace['summarize']\n"
                         'result = unittest.TextTestRunner().run(unittest.defaultTestLoader.discover("."))\n'
                         'raise SystemExit(not result.wasSuccessful())\n')
                result = subprocess.run(['python3', '-B', '-c', probe], cwd=project,
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertIn('Ran 4 tests', result.stderr)
            for offset, text in [(3, "record.get('code')"), (2, "record.get('display_name')"), (1, 'if amount < 0')]:
                shown = runner.command(['git', 'show', f'HEAD~{offset}', '--', 'summary.py'], project)
                self.assertIn(text, shown)
            self.assertEqual(runner.command(['git', 'status', '--porcelain'], project), '')

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
