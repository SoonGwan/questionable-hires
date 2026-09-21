import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('standalone_archive', ROOT / 'scripts/package_skills.py')
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class StandaloneArchiveTests(unittest.TestCase):
    def test_reproducible_archive_installs_all_resources_offline(self):
        with tempfile.TemporaryDirectory(prefix='standalone-') as temporary:
            root = Path(temporary)
            first, second = root / 'one.tar.gz', root / 'two.tar.gz'
            report = builder.package(first)
            builder.package(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            unpacked = root / 'unpacked'
            unpacked.mkdir()
            with tarfile.open(first) as archive:
                for entry in archive.getmembers():
                    self.assertTrue(entry.isfile())
                    relative = Path(entry.name)
                    self.assertEqual(relative.parts[0], 'questionable-hires')
                    self.assertFalse(relative.is_absolute() or '..' in relative.parts)
                    target = unpacked / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.extractfile(entry).read())
                    target.chmod(entry.mode)
            package = unpacked / 'questionable-hires'
            manifest = json.loads((package / 'CONTENTS.json').read_text())
            self.assertEqual(report['files'], len(manifest) + 1)
            for name, info in manifest.items():
                source, copied = ROOT / name, package / name
                self.assertEqual(copied.read_bytes(), source.read_bytes())
                self.assertEqual(hashlib.sha256(copied.read_bytes()).hexdigest(), info['sha256'])
                self.assertEqual(copied.stat().st_mode & 0o777, info['mode'])
            self.assertEqual(set(p.name for p in package.iterdir()), {'skills', 'scripts', 'LICENSE', 'CONTENTS.json'})
            install = package / 'scripts/install.py'
            destination = root / 'consumer/.agents/skills'
            command = [sys.executable, '-I', '-B', str(install), '--dest', str(destination)]
            installed = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=15)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            checked = subprocess.run(command + ['--check'], cwd=root, capture_output=True, text=True, timeout=15)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertTrue(json.loads(checked.stdout)['matches'])
            self.assertEqual(len(list(destination.glob('*/SKILL.md'))), 8)
            for script in destination.glob('*/scripts/*.py'):
                result = subprocess.run([sys.executable, '-I', '-B', str(script), '--help'],
                                        cwd=root, capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
            # Exercise behavior from the extracted/installed resource, not only
            # its argument parser or a checkout-imported module.
            consumer = root / 'consumer'
            source = consumer / 'sample.py'
            original = ''.join('def f%d():\n' % i + '    x = 1\n' * 9 for i in range(21))
            source.write_text(original)
            source.chmod(0o600)
            context = destination / 'con-artist/scripts/context.py'
            reports = {}
            for format_args in ([], ['--pretty']):
                result = subprocess.run([sys.executable, '-I', '-B', str(context),
                    '--root', str(consumer), *format_args, 'sample.py'], cwd=consumer,
                    capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, '')
                reports[bool(format_args)] = json.loads(result.stdout)
            self.assertEqual(reports[False]['selected'][0]['representation'], 'definition_index')
            selected = reports[True]['selected'][0]
            self.assertEqual(selected['representation'], 'full_source')
            self.assertEqual(selected['sha256'], hashlib.sha256(original.encode()).hexdigest())
            self.assertEqual(selected['source'], '\n'.join(
                f'{i}: {line}' for i, line in enumerate(original.splitlines(), 1)))
            self.assertEqual(source.read_bytes(), original.encode())
            self.assertEqual(source.stat().st_mode & 0o777, 0o600)
            self.assertEqual({p.name for p in consumer.iterdir()}, {'.agents', 'sample.py'})
            # The installed guard must preserve native evidence and detect an
            # unselected original edit, not merely expose a working --help.
            project = root / 'audit-consumer'
            project.mkdir()
            originals = {
                'service.py': 'def value():\n    return 1\n',
                'test_service.py': 'import unittest\nimport service\nclass Tests(unittest.TestCase):\n    def test_positive(self):\n        self.assertGreater(service.value(), 0)\n',
                'notes.txt': 'owner notes',
            }
            for name, contents in originals.items():
                (project / name).write_text(contents)
                (project / name).chmod(0o600)
            recipe = dict(files=['service.py', 'test_service.py'], imports=['service'],
                target='service.py', old='return 1', new='return 2',
                tests=['-v', 'test_service'], guard_project=True,
                probe='import service\nassert service.value() == 1, service.value()\n')
            audit = [sys.executable, '-I', '-B',
                str(destination / 'con-artist/scripts/audit.py'),
                '--source', str(project), '--spec', '-']
            observed = subprocess.run(audit, input=json.dumps(recipe), cwd=root,
                capture_output=True, text=True, timeout=15)
            self.assertEqual(observed.returncode, 0, observed.stderr)
            evidence = json.loads(observed.stdout)
            self.assertEqual({k: v['exit_code'] for k, v in evidence['checks'].items()},
                dict(correct_tests=0, mutant_tests=0, correct_probe=0, mutant_probe=1))
            self.assertIn('Ran 1 test', evidence['checks']['correct_tests']['output'])
            self.assertIn('AssertionError: 2', evidence['checks']['mutant_probe']['output'])
            self.assertTrue(evidence['integrity']['project_guard']['unchanged'])
            self.assertEqual({p.name for p in project.iterdir()}, set(originals))
            for name, contents in originals.items():
                self.assertEqual((project / name).read_text(), contents)
                self.assertEqual((project / name).stat().st_mode & 0o777, 0o600)
            recipe['precheck'] = 'from pathlib import Path\nPath(%r).write_text("changed")\n' % str(project / 'notes.txt')
            rejected = subprocess.run(audit, input=json.dumps(recipe), cwd=root,
                capture_output=True, text=True, timeout=15)
            self.assertEqual(rejected.returncode, 2, rejected.stderr)
            self.assertEqual(rejected.stdout, '')
            self.assertIn('Project tree changed during audit; not restored', rejected.stderr)
            self.assertIn('notes.txt', rejected.stderr)
            self.assertEqual((project / 'notes.txt').read_text(), 'changed')
            self.assertEqual({p.name for p in project.iterdir()}, set(originals))
            self.check_recent_installed_helpers(destination, root)
            rechecked = subprocess.run(command + ['--check'], cwd=root,
                capture_output=True, text=True, timeout=15)
            self.assertEqual(rechecked.returncode, 0, rechecked.stderr)
            self.assertTrue(json.loads(rechecked.stdout)['matches'])

    def check_recent_installed_helpers(self, destination, root):
        """Execute recent capabilities from installed files, outside checkout."""
        region = destination / 'necromancer/scripts/python_regions.py'
        source = b'\xef\xbb\xbfdef selected():\r\n    return 1\r\n'
        for name, code in [('selected', 0), ('missing', 1)]:
            result = subprocess.run([sys.executable, '-I', '-B', str(region), '--name', name],
                input=source, cwd=root, capture_output=True, timeout=15)
            self.assertEqual(result.returncode, code, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data['source_sha256'], hashlib.sha256(source).hexdigest())
            self.assertEqual(data['source_bytes'], len(source))
            self.assertEqual(data['complete'], code == 0)
            if code == 0:
                self.assertEqual(data['regions'][0]['text'], source[3:].decode())
                self.assertEqual(data['regions'][0]['start_line'], 1)
            else:
                self.assertEqual(data['missing_names'], ['missing'])

        project = root / 'receipt-consumer'
        project.mkdir()
        def git(*args):
            result = subprocess.run(['git', *args], cwd=project,
                capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout.strip()
        git('init', '-q', '--template=')
        git('config', 'user.name', 'Fixture Author')
        git('config', 'user.email', 'fixture@example.invalid')
        git('config', 'commit.gpgsign', 'false')
        (project/'.git/no-hooks').mkdir()
        git('config', 'core.hooksPath', str(project/'.git/no-hooks'))
        revisions = []
        for expression in ('n > 18', 'n >= 17'):
            (project/'rule.py').write_text('def eligible(n): return ' + expression + '\n')
            git('add', 'rule.py')
            git('commit', '-qm', 'Historical implementation')
            revisions.append(git('rev-parse', 'HEAD'))
        (project/'rule.py').write_text('def eligible(n): return n >= 18\n')
        (project/'test_rule.py').write_text('import unittest\nimport rule\n'
            'class Boundary(unittest.TestCase):\n'
            '    def test_adult(self): self.assertTrue(rule.eligible(18))\n'
            '    def test_minor(self): self.assertFalse(rule.eligible(17))\n')
        def inventory():
            return {str(p.relative_to(project)): (p.read_bytes(), p.stat().st_mode & 0o777)
                    for p in project.rglob('*') if p.is_file()}
        before = inventory()
        recipe = dict(fixed=['test_rule.py'], vary=['rule.py'], before=revisions[0],
            additional_before=[revisions[1]], after={'working_tree': True},
            imports=['rule'], runner='unittest', invocation='module',
            tests=['-v', 'test_rule'], guard_tree=True)
        result = subprocess.run([sys.executable, '-I', '-B',
            str(destination/'receipt/scripts/compare.py'), '--source', str(project), '--spec', '-'],
            input=json.dumps(recipe), cwd=root, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['revisions'], dict(before=revisions[0], before_2=revisions[1], after=None))
        self.assertEqual(list(data['checks']), ['before', 'before_2', 'after'])
        for label, code in [('before', 1), ('before_2', 1), ('after', 0)]:
            observed = data['checks'][label]
            self.assertEqual(observed['native_exit_code'], code)
            self.assertTrue(observed['provenance_ready'])
            self.assertFalse(observed['timed_out'])
            self.assertFalse(observed['output_truncated'])
            self.assertIn('Ran 2 tests', observed['output'])
            self.assertIn('Verified copied import: rule', observed['output'])
        self.assertIn('False is not true', data['checks']['before']['output'])
        self.assertIn('True is not false', data['checks']['before_2']['output'])
        self.assertTrue(data['tree_guard']['unchanged'])
        self.assertTrue(data['comparison_copies_removed'])
        self.assertEqual(inventory(), before)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'existing.tar.gz'
            output.write_bytes(b'owner archive')
            with self.assertRaises(FileExistsError):
                builder.package(output)
            self.assertEqual(output.read_bytes(), b'owner archive')

    def test_linked_resource_is_rejected_before_output_creation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'skills/demo').mkdir(parents=True)
            (root / 'skills/demo/SKILL.md').write_text('demo')
            (root / 'skills/demo/link').symlink_to(ROOT / 'LICENSE')
            output = root / 'bundle.tar.gz'
            with patch.object(builder, 'ROOT', root), self.assertRaisesRegex(ValueError, 'Linked'):
                builder.package(output)
            self.assertFalse(output.exists())

    def test_output_cannot_pollute_installable_resources(self):
        output = ROOT / 'skills/con-artist/bundle.tar.gz'
        self.assertFalse(output.exists())
        with self.assertRaisesRegex(ValueError, 'outside source'):
            builder.package(output)
        self.assertFalse(output.exists())
