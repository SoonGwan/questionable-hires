"""Frozen source/export controls; no upstream checkout or model account needed."""
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import packaging_specifier_cases as fixture
import run


class SpecifierCaseTests(unittest.TestCase):
    def setUp(self):
        self.cases = fixture.cases(Path(sys.executable).absolute())
        self.files = self.cases[0]['files']
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.temp = Path(folder.name)

    def materialize(self):
        root = self.temp / 'source'
        root.mkdir()
        for name, content in self.files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode('utf-8'))
            path.chmod(0o644)
        return root

    def test_both_requests_keep_exact_upstream_files_and_licenses(self):
        self.assertEqual(len(self.cases), 2)
        self.assertEqual(self.cases[0]['files'], self.cases[1]['files'])
        self.assertIsNot(self.cases[0]['files'], self.cases[1]['files'])
        manifest = json.loads(fixture.SUMMARY.read_text())['manifest']
        self.assertEqual(set(self.files), set(manifest))
        for name, content in self.files.items():
            self.assertEqual(hashlib.sha256(content.encode()).hexdigest(), manifest[name]['sha256'])
        self.assertTrue({'LICENSE', 'LICENSE.BSD', 'LICENSE.APACHE', 'tests/test_specifiers.py',
                         'tests/test_version.py', 'src/packaging/__init__.py'} <= set(self.files))

    def test_mutations_are_independent_and_follow_committed_source_order(self):
        source = self.files['src/packaging/specifiers.py']
        cls, = [n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == 'Specifier']
        methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name.startswith('_compare_')][:3]
        self.assertEqual([m.name for m in methods], ['_compare_compatible', '_compare_equal', '_compare_not_equal'])
        faults = json.loads(fixture.SUMMARY.read_text())['mutations']
        for method, fault in zip(methods, faults):
            final = max((n for n in ast.walk(method) if isinstance(n, ast.Return)), key=lambda n: n.lineno)
            self.assertEqual(ast.get_source_segment(source, final), fault['old'])
            altered = source.replace(fault['old'], fault['new'], 1)
            ast.parse(altered)
            self.assertEqual(altered.count(fault['old']), 0)
            for other in faults:
                if other != fault:
                    self.assertIn(other['old'], altered)

    def test_source_corruption_or_inventory_changes_are_rejected(self):
        for changed in (dict(self.files, extra='x'), {k:v for k,v in self.files.items() if k != 'LICENSE'},
                        dict(self.files, LICENSE=self.files['LICENSE'] + '\n')):
            with self.subTest(size=len(changed)), self.assertRaises(ValueError):
                fixture.validate_files(changed)

    def test_export_roundtrip_and_overwrite_refusal(self):
        source = self.materialize()
        output = self.temp / 'export.json'
        fixture.export_source(source, output)
        self.assertEqual(json.loads(output.read_text()), self.files)
        original = output.read_bytes()
        with self.assertRaises(FileExistsError):
            fixture.export_source(source, output)
        self.assertEqual(output.read_bytes(), original)

    def test_export_rejects_mode_change_and_symlink_without_output(self):
        source = self.materialize()
        output = self.temp / 'export.json'
        license_path = source / 'LICENSE'
        license_path.chmod(0o755)
        with self.assertRaises(ValueError):
            fixture.export_source(source, output)
        self.assertFalse(output.exists())
        license_path.chmod(0o644)
        (source / 'alias').symlink_to('LICENSE')
        with self.assertRaises(ValueError):
            fixture.export_source(source, output)
        self.assertFalse(output.exists())

    def test_actual_model_workspace_materialization_preserves_bytes_modes(self):
        project = self.temp / 'project'
        run.prepare(self.cases[0], project)
        for name, content in self.files.items():
            self.assertEqual((project / name).read_bytes(), content.encode())
            self.assertEqual((project / name).stat().st_mode & 0o777, 0o644)

    def test_relative_runtime_rejected_before_cases_are_built(self):
        with self.assertRaises(ValueError):
            fixture.cases('python3')
