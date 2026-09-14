from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'benchmarks/results/hostage-keyed-import-01/keyed-import--skill--1/project'


@unittest.skipUnless(shutil.which('git') and shutil.which('cmp'), 'POSIX Git/cmp required')
class FinalBatchControls(unittest.TestCase):
    def test_native_batch_retains_checks_and_does_not_hide_failures(self):
        # Real retained model tests, not fake executables reporting chosen exits.
        for fault in ('none', 'test', 'copy', 'original_test', 'whitespace'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory(prefix='final-batch-', dir=ROOT) as temporary:
                project = Path(temporary)
                for path in PROJECT.iterdir():
                    shutil.copyfile(path, project / path.name)
                asset = project / 'source asset.py'
                shutil.copyfile(project / 'controlled_call.py', asset)
                git = ['git', '-C', str(project)]
                def command(args):
                    return subprocess.run(args, cwd=project, capture_output=True, text=True, timeout=20)
                self.assertEqual(command(git + ['init', '-q']).returncode, 0)
                self.assertEqual(command(git + ['add', '.']).returncode, 0)
                self.assertEqual(command(git + ['-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                    '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null', 'commit', '-qm', 'fixture']).returncode, 0)
                implementation = project / 'importer.py'
                if fault == 'test':
                    implementation.write_text(implementation.read_text().replace('self.busy_keys.remove(key)', 'pass'))
                elif fault == 'copy':
                    with (project / 'controlled_call.py').open('a') as stream:
                        stream.write('\n# Unexpected local copy edit\n')
                elif fault == 'original_test':
                    with (project / 'test_existing.py').open('a') as stream:
                        stream.write('\n# Unexpected original-test edit\n')
                elif fault == 'whitespace':
                    implementation.write_text(implementation.read_text() + '\n# trailing space \n')
                before = {p.name: p.read_bytes() for p in project.iterdir() if p.is_file()}
                checks = [shlex.join([sys.executable, '-B', '-m', 'unittest', 'discover', '-v']),
                          shlex.join(['cmp', str(asset), 'controlled_call.py']),
                          'git diff --exit-code -- test_existing.py', 'git diff --check',
                          'git diff -- importer.py test_existing.py', 'git status --short']
                result = command(['/bin/sh', '-c', ' && '.join(checks)])
                output = result.stdout + result.stderr
                self.assertIn('Ran 6 tests', output)
                if fault == 'none':
                    self.assertEqual(result.returncode, 0, output)
                    self.assertIn('\nOK\n', output)
                else:
                    self.assertNotEqual(result.returncode, 0, output)
                    if fault == 'test':
                        self.assertIn('AssertionError', output)
                    if fault == 'copy':
                        self.assertEqual(result.returncode, 1, output)
                        self.assertIn('\nOK\n', output)
                        self.assertIn('cmp:', output)
                    if fault == 'original_test':
                        self.assertIn('Unexpected original-test edit', output)
                    if fault == 'whitespace':
                        self.assertIn('trailing whitespace', output)
                    # The historical semicolon shape can mask the same failure.
                    masked = command(['/bin/sh', '-c', '; '.join(checks)])
                    self.assertEqual(masked.returncode, 0, masked.stdout + masked.stderr)
                self.assertEqual({p.name: p.read_bytes() for p in project.iterdir() if p.is_file()}, before)
