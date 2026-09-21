"""Execute the actual packaging shell step; never dispatch or upload anything."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ReleaseCandidateWorkflowTests(unittest.TestCase):
    def runner_environment(self, root, output):
        # Model setup-python even on hosts which provide only a python3 name.
        binaries = root/'bin'
        binaries.mkdir()
        (binaries/'python').symlink_to(sys.executable)
        return dict(os.environ, RUNNER_TEMP=str(root), GITHUB_OUTPUT=str(output),
                    GITHUB_SHA='0' * 40,
                    PATH=str(binaries) + os.pathsep + os.environ.get('PATH', ''))

    def workflow(self):
        return yaml.load((ROOT/'.github/workflows/release-candidate.yml').read_text(), Loader=yaml.BaseLoader)

    def test_candidate_requires_full_validation_and_has_no_publish_trigger(self):
        workflow = self.workflow()
        self.assertEqual(set(workflow['on']), {'workflow_dispatch'})
        self.assertEqual(workflow['permissions'], {'contents': 'read'})
        jobs = workflow['jobs']
        self.assertEqual(jobs['validate']['uses'], './.github/workflows/validate.yml')
        self.assertEqual(jobs['package']['needs'], 'validate')
        self.assertNotIn('if', jobs['package'])
        self.assertNotIn('continue-on-error', jobs['package'])
        validation = yaml.load((ROOT/'.github/workflows/validate.yml').read_text(), Loader=yaml.BaseLoader)
        self.assertIn('workflow_call', validation['on'])
        self.assertIn('source-archive', validation['jobs'])
        self.assertEqual(validation['jobs']['validate']['strategy']['matrix']['python'], ['3.9', '3.11', '3.12'])
        steps = jobs['package']['steps']
        for step in steps:
            if 'uses' in step:
                revision = step['uses'].split('@')[1]
                self.assertEqual(len(revision), 40)
                int(revision, 16)
        upload = steps[-1]
        self.assertTrue(upload['uses'].startswith('actions/upload-artifact@'))
        self.assertEqual(upload['with']['if-no-files-found'], 'error')
        for step in steps:
            self.assertNotIn('if', step)
            self.assertNotIn('continue-on-error', step)

    def test_actual_shell_builds_reproducible_installable_minimal_artifact(self):
        step = next(s for s in self.workflow()['jobs']['package']['steps'] if s.get('id') == 'candidate')
        with tempfile.TemporaryDirectory(prefix='candidate-check-') as scratch:
            root = Path(scratch)
            output = root/'outputs'
            # Synthetic provenance for this local workflow test, not a release SHA.
            revision = '0' * 40
            env = self.runner_environment(root, output)
            result = subprocess.run(['bash', '-c', step['run']], cwd=ROOT, env=env,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            artifact = Path(output.read_text().strip().split('=', 1)[1])
            self.assertEqual(artifact.parent.parent, root)
            self.assertEqual({p.name for p in artifact.iterdir()},
                             {'questionable-hires.tar.gz', 'SOURCE_COMMIT', 'SHA256SUMS'})
            archive = artifact/'questionable-hires.tar.gz'
            self.assertEqual(archive.read_bytes(), (artifact.parent/'repeated.tar.gz').read_bytes())
            checksum, filename = (artifact/'SHA256SUMS').read_text().split()
            self.assertEqual(filename, archive.name)
            self.assertEqual(checksum, hashlib.sha256(archive.read_bytes()).hexdigest())
            self.assertEqual((artifact/'SOURCE_COMMIT').read_text().strip(), revision)
            self.assertEqual(len(list((artifact.parent/'consumer/.agents/skills').glob('*/SKILL.md'))), 8)
            self.assertIn('"matches": true', result.stdout)

    def test_failed_build_does_not_signal_an_upload_directory(self):
        step = next(s for s in self.workflow()['jobs']['package']['steps'] if s.get('id') == 'candidate')
        with tempfile.TemporaryDirectory(prefix='candidate-failure-') as scratch:
            root = Path(scratch)
            output = root/'outputs'
            # Empty working directory: the actual packager cannot be invoked.
            env = self.runner_environment(root, output)
            result = subprocess.run(['bash', '-c', step['run']], cwd=root, env=env,
                                    capture_output=True, text=True, timeout=30)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('package_skills.py', result.stderr)
            self.assertFalse(output.exists())
            self.assertEqual(list(root.rglob('SOURCE_COMMIT')), [])

    def test_privacy_finding_blocks_installation_and_candidate_signal(self):
        self.check_rejected_candidate('privacy')

    def test_install_verification_failure_blocks_candidate_signal(self):
        self.check_rejected_candidate('install-check')

    def check_rejected_candidate(self, failure):
        """Fault injection affects only a disposable copy, never shipped resources."""
        step = next(s for s in self.workflow()['jobs']['package']['steps'] if s.get('id') == 'candidate')
        with tempfile.TemporaryDirectory(prefix='candidate-rejection-') as scratch:
            root = Path(scratch)
            source = root/'source'
            source.mkdir()
            shutil.copytree(ROOT/'skills', source/'skills', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            (source/'scripts').mkdir()
            (source/'benchmarks').mkdir()
            for name in ('package_skills.py', 'install.py'):
                shutil.copy2(ROOT/'scripts'/name, source/'scripts'/name)
            shutil.copy2(ROOT/'LICENSE', source/'LICENSE')
            shutil.copy2(ROOT/'benchmarks/scan_evidence.py', source/'benchmarks/scan_evidence.py')
            if failure == 'privacy':
                # Header-only synthetic scanner control, not a private key.
                (source/'skills/receipt/rejection-control.txt').write_text('-----BEGIN PRIVATE KEY-----\n')
            else:
                installer = source/'scripts/install.py'
                # Insert before main runs, preserving any future-import position.
                original = installer.read_text()
                guard = "if __name__ == "
                position = original.index(guard)
                installer.write_text(original[:position] +
                                     "import sys\nif '--check' in sys.argv:\n    raise SystemExit(42)\n\n" +
                                     original[position:])
            output = root/'outputs'
            env = self.runner_environment(root, output)
            result = subprocess.run(['bash', '-c', step['run']], cwd=source, env=env,
                                    capture_output=True, text=True, timeout=30)
            self.assertFalse(output.exists(), result.stdout + result.stderr)
            self.assertEqual(list(root.rglob('SOURCE_COMMIT')), [])
            installed = list(root.glob('qh-candidate.*/consumer/.agents/skills/*/SKILL.md'))
            if failure == 'privacy':
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn('"kind": "credential"', result.stdout)
                self.assertEqual(installed, [])
            else:
                self.assertEqual(result.returncode, 42, result.stdout + result.stderr)
                self.assertEqual(len(installed), 8)
