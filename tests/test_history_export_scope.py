import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'benchmarks' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HistoryExportScopeTests(unittest.TestCase):
    def test_parent_history_is_not_borrowed_and_refusal_creates_no_output(self):
        with tempfile.TemporaryDirectory(prefix='history-scope-') as folder:
            parent = Path(folder).resolve()
            subprocess.run(['git','init','-q','--template=',str(parent)], check=True, capture_output=True)
            archive = parent / 'archive'
            archive.mkdir()
            discovered = subprocess.check_output(['git','rev-parse','--show-toplevel'], cwd=archive, text=True).strip()
            self.assertEqual(Path(discovered).resolve(), parent)
            for name in ('packaging_cases', 'run_friday_compact_01'):
                module = load(name)
                with self.subTest(module=name), patch.object(module,'ROOT',archive):
                    output = archive / 'out'
                    with self.assertRaisesRegex(ValueError, 'checkout'):
                        module.cases() if name == 'packaging_cases' else module.prepare(output)
                    self.assertFalse(output.exists())
                with patch.object(module,'ROOT',parent):
                    module.require_checkout()

    def test_git_root_mismatch_is_rejected_even_with_local_metadata_marker(self):
        for name in ('packaging_cases', 'run_friday_compact_01'):
            module = load(name)
            with tempfile.TemporaryDirectory() as folder, self.subTest(module=name):
                root = Path(folder)
                (root / '.git').mkdir()
                response = subprocess.CompletedProcess([],0,stdout=str(root.parent),stderr='')
                with patch.object(module,'ROOT',root), patch.object(module.subprocess,'run',return_value=response):
                    with self.assertRaisesRegex(ValueError, 'selected project root'):
                        module.require_checkout()
