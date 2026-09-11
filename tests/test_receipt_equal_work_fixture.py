import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReceiptEqualWorkFixtureTests(unittest.TestCase):
    def test_current_inputs_distinguish_revisions_while_old_inputs_do_not(self):
        fixture = load('equal_work', 'benchmarks/receipt_equal_work_cases.py')
        runner = load('equal_runner', 'benchmarks/run.py')
        helper = load('equal_receipt', 'skills/receipt/scripts/compare.py')
        case = fixture.cases()[0]
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'project'
            runner.prepare(case, project)
            recipe = dict(fixed=[p for p in case['files'] if p != 'records/decode.py'],
                          vary=['records/decode.py'], before='HEAD^', after='HEAD',
                          imports=['records.decode', 'records.settings'],
                          runner='unittest', tests=['-v', 'checks.test_records'])
            observed = helper.compare(project, recipe)
            self.assertEqual(observed['checks']['before']['exit_code'], 1)
            self.assertIn('too many values to unpack', observed['checks']['before']['output'])
            self.assertEqual(observed['checks']['after']['exit_code'], 0)
            for label in ('before', 'after'):
                self.assertIn('Verified copied import: records.decode', observed['checks'][label]['output'])
                self.assertIn('Ran 1 test', observed['checks'][label]['output'])
            # Historical tests/data by themselves conceal the defect. This copy
            # is author-only counterevidence, never supplied as a model hint.
            historical = Path(directory) / 'historical'
            historical.mkdir()
            for name in case['files']:
                data = subprocess.check_output(['git', 'show', 'HEAD^:' + name], cwd=project)
                target = historical / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            old = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v',
                                  'checks.test_records'], cwd=historical,
                                 capture_output=True, text=True, timeout=10)
            self.assertEqual(old.returncode, 0, old.stderr)
            for name, source in case['files'].items():
                self.assertEqual((project / name).read_text(), source)
            self.assertEqual(runner.command(['git', 'status', '--porcelain'], project), '')
