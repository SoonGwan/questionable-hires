import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('swe_runtime_stage',
    ROOT / 'benchmarks/swe-lite-runtime/stage.py')
stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)


class RuntimeStageTests(unittest.TestCase):
    def fixture(self, root):
        for name in ('Dockerfile', 'prepare.py'):
            path = root / 'benchmarks/swe-lite-runtime' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('synthetic recipe')
        for manifest, folder, filename in (
            ('requests-diagnosis/installed-wheel-hashes.json', 'requests-pytest', 'pytest.whl'),
            ('services/wheel-hashes.json', 'wheelhouse', 'wheel.whl'),
            ('tls/certifi-wheel.json', 'requests-pytest', 'certifi.whl'),
        ):
            wheel = root / 'benchmarks/local-runs' / ('swe-lite-pilot-01-' + folder) / filename
            wheel.parent.mkdir(parents=True, exist_ok=True)
            wheel.write_bytes(b'synthetic wheel')
            path = root / 'benchmarks/results' / ('swe-lite-pilot-01-' + manifest)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({filename: hashlib.sha256(wheel.read_bytes()).hexdigest()}))
        ca = root / 'benchmarks/local-runs/swe-lite-tls-01/ca.pem'
        ca.parent.mkdir(parents=True)
        ca.write_text('-----BEGIN CERTIFICATE-----\nsynthetic\n-----END CERTIFICATE-----')
        (ca.parent / 'ca.key').write_text('PRIVATE KEY must not travel')
        (root / 'benchmarks/local-runs/gold.json').write_text('hidden answer')
        return ca

    def test_copies_only_allowlisted_bytes_and_refuses_reuse(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            output = root / 'context'
            manifest = stage.stage(output, root)
            self.assertEqual(set(manifest), {'Dockerfile', 'prepare.py', 'ca.pem',
                'wheels/pytest.whl', 'wheels/wheel.whl', 'wheels/certifi.whl'})
            for name, digest in manifest.items():
                self.assertEqual(hashlib.sha256((output / name).read_bytes()).hexdigest(), digest)
            self.assertEqual(set(manifest), {p.relative_to(output).as_posix()
                for p in output.rglob('*') if p.is_file()})
            with self.assertRaises(FileExistsError):
                stage.stage(output, root)

    def test_rejects_changed_or_linked_wheels_before_creating_context(self):
        for kind in ('changed', 'linked'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                self.fixture(root)
                wheel = root / 'benchmarks/local-runs/swe-lite-pilot-01-requests-pytest/pytest.whl'
                if kind == 'changed':
                    wheel.write_bytes(b'changed')
                else:
                    other = wheel.with_suffix('.original')
                    wheel.rename(other)
                    wheel.symlink_to(other)
                with self.assertRaises(ValueError):
                    stage.stage(root / 'context', root)
                self.assertFalse((root / 'context').exists())

    def test_rejects_private_key_in_certificate(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root).write_text('-----BEGIN PRIVATE KEY-----')
            with self.assertRaises(ValueError):
                stage.stage(root / 'context', root)
            self.assertFalse((root / 'context').exists())

    def test_rejects_manifest_path_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            path = root / 'benchmarks/results/swe-lite-pilot-01-tls/certifi-wheel.json'
            path.write_text(json.dumps({'../secret.whl': 'unused'}))
            with self.assertRaises(ValueError):
                stage.stage(root / 'context', root)
            self.assertFalse((root / 'context').exists())
