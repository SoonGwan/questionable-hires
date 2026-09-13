import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


class SourceArchiveWorkflowTests(unittest.TestCase):
    def test_archive_job_uses_committed_files_and_propagates_validation_failure(self):
        root = Path(__file__).resolve().parents[1]
        workflow = yaml.safe_load((root / '.github/workflows/validate.yml').read_text())
        steps = workflow['jobs']['source-archive']['steps']
        script, = [step['run'] for step in steps if step.get('shell') == 'bash']
        with tempfile.TemporaryDirectory() as scratch:
            workspace = Path(scratch) / 'repo'
            workspace.mkdir()
            temp = Path(scratch) / 'runner-temp'
            temp.mkdir()
            binaries = Path(scratch) / 'bin'
            binaries.mkdir()
            (binaries / 'python').symlink_to(sys.executable)
            env = dict(os.environ, RUNNER_TEMP=str(temp),
                       PATH=str(binaries) + os.pathsep + os.environ['PATH'])

            def git(*args):
                return subprocess.run(['git', '-c', 'commit.gpgsign=false',
                                       '-c', 'core.hooksPath=' + str(temp / 'no-hooks'), *args],
                                      cwd=workspace, check=True, capture_output=True, timeout=5)

            git('init', '-q', '--template=')
            git('config', 'user.name', 'Archive Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            files = {
                'payload.txt': 'committed',
                'scripts/validate.py': 'from pathlib import Path\n'
                    'assert Path("payload.txt").read_text() == "committed"\n'
                    'assert not Path("untracked.txt").exists()\n'
                    'print("archive validation passed")\n',
                'scripts/sync_featured_benchmark.py': 'print("archive sync passed")\n',
                'tests/test_payload.py': 'from pathlib import Path\nimport unittest\n'
                    'class PayloadTests(unittest.TestCase):\n'
                    '    def test_committed_payload(self):\n'
                    '        self.assertEqual(Path("payload.txt").read_text(), "committed")\n'
                    '        self.assertFalse(Path(".git").exists())\n',
            }
            for name, text in files.items():
                target = workspace / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
            git('add', '.')
            git('commit', '-qm', 'Committed distribution')
            (workspace / 'payload.txt').write_text('uncommitted')
            (workspace / 'untracked.txt').write_text('excluded')
            passed = subprocess.run(['bash', '-c', script], cwd=workspace, env=env,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(passed.returncode, 0, passed.stderr)
            self.assertIn('archive validation passed', passed.stdout)
            self.assertIn('archive sync passed', passed.stdout)
            self.assertIn('Ran 1 test', passed.stderr)
            self.assertEqual((workspace / 'payload.txt').read_text(), 'uncommitted')

            (workspace / 'scripts/validate.py').write_text('raise SystemExit(7)\n')
            git('add', 'scripts/validate.py')
            git('commit', '-qm', 'Fail validation')
            failed = subprocess.run(['bash', '-c', script], cwd=workspace, env=env,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(failed.returncode, 7, failed.stderr)
            self.assertNotIn('archive sync passed', failed.stdout)
            self.assertNotIn('Ran 1 test', failed.stderr)
