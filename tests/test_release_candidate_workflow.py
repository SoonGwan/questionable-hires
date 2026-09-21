"""Execute the actual packaging shell step; never dispatch or upload anything."""
import hashlib
import os
from pathlib import Path
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
