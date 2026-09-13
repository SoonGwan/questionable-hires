import hashlib
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
    def test_directory_recipes_preserve_existing_comparison_evidence(self):
        runner = load('directory_runner', 'benchmarks/run.py')
        helper = load('directory_receipt', 'skills/receipt/scripts/compare.py')
        fixtures = [
            ('benchmarks/receipt_equal_work_cases.py',
             ['records/decode.py'],
             ['README.md', 'records/__init__.py', 'records/settings.py',
              'checks', 'samples'],
             ['records.decode', 'records.settings'], 'checks.test_records',
             'too many values to unpack', 'Ran 1 test'),
            ('benchmarks/receipt_assembly_cases.py',
             ['assembly/__init__.py', 'assembly/reader.py',
              'assembly/writer.py', 'assembly/service.py'],
             ['README.md', 'settings.json', 'samples', 'test_assembly.py'],
             ['assembly.service', 'assembly.reader', 'assembly.writer'],
             'test_assembly', 'FAILED (failures=2)', 'Ran 2 tests'),
        ]
        for path, varying, directories, imports, test, failure, count in fixtures:
            with self.subTest(fixture=path), tempfile.TemporaryDirectory() as directory:
                case = load('directory_fixture', path).cases()[0]
                project = Path(directory) / 'project'
                runner.prepare(case, project)
                originals = {name: ((project / name).read_bytes(),
                                    (project / name).stat().st_mode)
                             for name in case['files']}
                leaves = [name for name in case['files'] if name not in varying]
                identity = None
                for selection in (leaves, directories):
                    recipe = dict(fixed=list(selection), vary=varying,
                                  before='HEAD^', after='HEAD', imports=imports,
                                  runner='unittest', tests=['-v', test])
                    result = helper.compare(project, recipe)
                    self.assertEqual(recipe['fixed'], selection)
                    self.assertEqual(result['status'], 'observed')
                    self.assertEqual(result['checks']['before']['exit_code'], 1)
                    self.assertIn(failure, result['checks']['before']['output'])
                    self.assertEqual(result['checks']['after']['exit_code'], 0)
                    for check in result['checks'].values():
                        self.assertFalse(check['timed_out'])
                        self.assertFalse(check['output_truncated'])
                        self.assertIn(count, check['output'])
                        for name in imports:
                            self.assertIn('Verified copied import: ' + name,
                                          check['output'])
                    self.assertEqual(result['fixed_sha256'], {
                        name: hashlib.sha256(originals[name][0]).hexdigest()
                        for name in leaves})
                    current = (result['revisions'], result['fixed_sha256'])
                    if identity is None:
                        identity = current
                    self.assertEqual(current, identity)
                    self.assertEqual(originals, {
                        name: ((project / name).read_bytes(),
                               (project / name).stat().st_mode)
                        for name in case['files']})
                    self.assertEqual(runner.command(
                        ['git', 'status', '--porcelain'], project), '')
                    self.assertFalse(list(project.glob('.receipt-*')))

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
