import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / 'benchmarks/candidates/landlord-context/skills/landlord'


class LandlordContextCandidateTests(unittest.TestCase):
    def test_isolated_copy_preserves_groups_instructions_and_bounds(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            installed = root / 'installed/landlord'
            shutil.copytree(CANDIDATE, installed)
            project = root / 'project'
            project.mkdir()
            original = ('raise RuntimeError("must never import")\n'
                        'class Store:\n'
                        '    def save(self, value: int): ...\n'
                        '    def save(self, value):\n'
                        '        return value\n')
            (project / 'service.py').write_text(original)
            (project / 'AGENTS.md').write_text('Do not modify this project.\n')
            command = [sys.executable, '-I', '-B', str(installed / 'scripts/context.py'),
                       '--root', str(project), '--all-matches', 'service.py:Store.save']
            result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            selected = report['selected'][0]
            self.assertEqual(selected['sha256'], hashlib.sha256(original.encode()).hexdigest())
            self.assertEqual([(d['first_line'], d['last_line']) for d in selected['definitions']],
                             [(3, 3), (4, 5)])
            self.assertIn('return value', selected['definitions'][1]['source'])
            self.assertIn('Do not modify', report['instructions'][0]['source'])
            size = len(result.stdout)
            exact = subprocess.run(command + ['--max-output', str(size)], cwd=root,
                                   capture_output=True, text=True, timeout=10)
            self.assertEqual(exact.returncode, 0, exact.stderr)
            self.assertEqual(exact.stdout, result.stdout)
            failed = subprocess.run(command + ['--max-output', str(size - 1)], cwd=root,
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(failed.returncode, 2)
            self.assertEqual(failed.stdout, '')
            self.assertEqual(json.loads(failed.stderr)['status'], 'incomplete')
            self.assertEqual((project / 'service.py').read_text(), original)
            self.assertEqual({p.name for p in project.iterdir()}, {'service.py', 'AGENTS.md'})
            self.assertEqual({p.name for p in (root / 'installed').iterdir()}, {'landlord'})


if __name__ == '__main__':
    unittest.main()
