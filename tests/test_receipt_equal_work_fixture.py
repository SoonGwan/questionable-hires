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
    def test_assembly_writer_matches_documented_lf_bytes(self):
        fixture = load('assembly_lf', 'benchmarks/receipt_assembly_cases.py').cases()[0]
        old, current = {}, {}
        exec(fixture['history'][0]['files']['assembly/writer.py'], old)
        exec(fixture['files']['assembly/writer.py'], current)
        for variant in (old, current):
            self.assertEqual(variant['render'](['one', 'two'], '|').encode(), b'one|two\n')
        self.assertEqual(old['render']([], '|').encode(), b'\n')
        self.assertEqual(current['render']([], '|').encode(), b'')
        mutant = {}
        exec(fixture['files']['assembly/writer.py'].replace('\\n', '\\\\n'), mutant)
        self.assertEqual(mutant['render'](['one', 'two'], '|').encode(), b'one|two\\n')
        self.assertNotEqual(mutant['render'](['one', 'two'], '|').encode(), b'one|two\n')

    def test_assembly_requires_both_historical_implementations(self):
        fixture = load('assembly_history', 'benchmarks/receipt_assembly_cases.py')
        runner = load('assembly_runner', 'benchmarks/run.py')
        helper = load('assembly_receipt', 'skills/receipt/scripts/compare.py')
        case = fixture.cases()[0]
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'project'
            runner.prepare(case, project)
            both = ['assembly/reader.py', 'assembly/writer.py']
            for varying in (both, both[:1], both[1:]):
                result = helper.compare(project, dict(
                    fixed=[name for name in case['files'] if name not in varying],
                    vary=varying, before='HEAD^', after='HEAD',
                    imports=['assembly.service', 'assembly.reader', 'assembly.writer'],
                    runner='unittest', tests=['-v', 'test_assembly']))
                before = result['checks']['before']
                self.assertEqual(before['exit_code'], 1)
                expected = 2 if varying == both else 1
                self.assertIn(f'FAILED (failures={expected})', before['output'])
                self.assertEqual(result['checks']['after']['exit_code'], 0)
                self.assertIn('Ran 2 tests', result['checks']['after']['output'])
            for name, source in case['files'].items():
                self.assertEqual((project / name).read_text(), source)
            self.assertEqual(runner.command(['git', 'status', '--porcelain'], project), '')

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
