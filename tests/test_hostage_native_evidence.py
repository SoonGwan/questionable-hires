"""Execute the shipped recipe with real native outcomes and dropped display."""
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'skills/hostage-negotiator/references/native-evidence.md'


class NativeEvidenceTests(unittest.TestCase):
    def recipe(self):
        return REFERENCE.read_text().split('```sh\n', 1)[1].split('\n```', 1)[0]

    def run_check(self, passing):
        with tempfile.TemporaryDirectory(prefix='capture-test-', dir=ROOT / 'benchmarks') as temporary:
            project = Path(temporary) / 'project with spaces'
            project.mkdir()
            source = ('from pathlib import Path\nimport unittest\n'
                      'class NativeCheck(unittest.TestCase):\n'
                      '    def test_actual_result(self):\n'
                      '        with Path("executions.txt").open("a") as stream:\n'
                      '            stream.write("executed\\n")\n'
                      '        self.assertEqual(41 + 1, ' + ('42' if passing else '43') + ')\n')
            test = project / 'test_actual.py'
            test.write_text(source)
            previous = project / '.test-evidence.previous'
            previous.mkdir()
            (previous / 'output.txt').write_text('owner evidence\n')
            # Deliberately discard display, not the native report: a simulation
            # of unavailable terminal evidence, not reproduction of the CLI bug.
            result = subprocess.run(['sh', '-ec', self.recipe()], cwd=project,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                                    text=True, timeout=15)
            self.assertEqual(result.returncode, 0 if passing else 1)
            self.assertEqual(result.stderr, '')
            fresh = [p for p in project.glob('.test-evidence.*') if p != previous]
            self.assertEqual(len(fresh), 1)
            evidence = fresh[0]
            self.assertEqual((evidence / 'argv.txt').read_text().splitlines(),
                             ['python3', '-B', '-m', 'unittest', 'discover', '-v'])
            self.assertEqual((evidence / 'exit.txt').read_text(), str(result.returncode) + '\n')
            output = (evidence / 'output.txt').read_text()
            self.assertIn('test_actual_result', output)
            self.assertIn('Ran 1 test', output)
            self.assertIn('\nOK\n' if passing else 'AssertionError: 42 != 43', output)
            self.assertEqual((project / 'executions.txt').read_text(), 'executed\n')
            self.assertEqual(test.read_text(), source)
            self.assertEqual((previous / 'output.txt').read_text(), 'owner evidence\n')

    def test_pass_survives_lost_display_without_rerun(self):
        self.run_check(True)

    def test_actual_failure_survives_errexit_and_lost_display(self):
        self.run_check(False)

    def test_zero_discovered_tests_remains_visible_despite_exit_zero(self):
        with tempfile.TemporaryDirectory(prefix='capture-empty-', dir=ROOT / 'benchmarks') as temporary:
            project = Path(temporary)
            result = subprocess.run(['sh', '-ec', self.recipe()], cwd=project,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=15)
            self.assertEqual(result.returncode, 0)
            evidence, = project.glob('.test-evidence.*')
            self.assertIn('Ran 0 tests', (evidence / 'output.txt').read_text())
            self.assertEqual((evidence / 'exit.txt').read_text(), '0\n')

    def test_missing_native_command_keeps_its_own_failure(self):
        with tempfile.TemporaryDirectory(prefix='capture-missing-', dir=ROOT / 'benchmarks') as temporary:
            project = Path(temporary)
            recipe = self.recipe().replace('set -- python3 -B -m unittest discover -v',
                                           'set -- ./missing-native-command')
            result = subprocess.run(['sh', '-ec', recipe], cwd=project,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=15)
            direct = subprocess.run(['sh', '-ec', 'if ./missing-native-command; then exit 0; else exit "$?"; fi'], cwd=project,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=15)
            self.assertNotEqual(direct.returncode, 0)
            self.assertEqual(result.returncode, direct.returncode)
            evidence, = project.glob('.test-evidence.*')
            self.assertEqual((evidence / 'exit.txt').read_text(), str(direct.returncode) + '\n')
            self.assertIn('missing-native-command', (evidence / 'output.txt').read_text())
            self.assertNotIn('Ran 1 test', (evidence / 'output.txt').read_text())

    def test_nonstandard_exit_is_not_replaced_by_successful_output_read(self):
        with tempfile.TemporaryDirectory(prefix='capture-exit-', dir=ROOT / 'benchmarks') as temporary:
            project = Path(temporary)
            recipe = self.recipe().replace('set -- python3 -B -m unittest discover -v',
                                           "set -- sh -c 'printf native-failure; exit 37'")
            result = subprocess.run(['sh', '-ec', recipe], cwd=project,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, timeout=15)
            self.assertEqual(result.returncode, 37)
            evidence, = project.glob('.test-evidence.*')
            self.assertEqual((evidence / 'exit.txt').read_text(), '37\n')
            self.assertEqual((evidence / 'output.txt').read_text(), 'native-failure')
