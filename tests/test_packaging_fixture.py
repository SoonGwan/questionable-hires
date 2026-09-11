import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('packaging_cases', ROOT / 'benchmarks/packaging_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class PackagingFixtureTests(unittest.TestCase):
    def test_pinned_real_build_has_retry_fault_and_preserves_existing_output(self):
        case = fixture.cases()[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for name, content in case['files'].items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            spec = importlib.util.spec_from_file_location('pinned_builder', root / 'scripts/build.py')
            builder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(builder)
            destination = root / 'output'
            failure = OSError('controlled final catalog copy failure')
            copy = builder.shutil.copy2
            def fail_catalog(source, target, *args, **kwargs):
                if Path(source) == root / 'packaging/marketplace.json':
                    raise failure
                return copy(source, target, *args, **kwargs)
            with patch.object(builder.shutil, 'copy2', side_effect=fail_catalog):
                with self.assertRaises(OSError) as observed:
                    builder.build(destination)
            self.assertIs(observed.exception, failure)
            self.assertTrue((destination / 'plugins/questionable-hires/LICENSE').is_file())
            with self.assertRaises(FileExistsError):
                builder.build(destination)
            sentinel = destination / 'owned-by-user.txt'
            sentinel.write_text('preserve')
            with self.assertRaises(FileExistsError):
                builder.build(destination)
            self.assertEqual(sentinel.read_text(), 'preserve')
