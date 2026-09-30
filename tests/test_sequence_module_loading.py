"""Exercise actual dataclass imports and annotation lookup through the probe CLI."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_mother_in_law_sequence_probe import probe


SOURCE = '''from __future__ import annotations
from dataclasses import dataclass, fields
from typing import ClassVar, Optional, get_type_hints

Payload = Optional[str]

@dataclass
class Search:
    kind: ClassVar[str] = "search"
    result: Payload = None
    generation: int = 0

    async def run(self, query, fetch):
        assert get_type_hints(type(self))["result"] == Payload
        assert "kind" not in {field.name for field in fields(self)}
        self.generation += 1
        generation = self.generation
        result = await fetch(query)
        if GUARD:
            self.result = result
'''


class ModuleLoadingTests(unittest.TestCase):
    def test_scoped_import_restores_existing_module_on_success_and_failure(self):
        alias = '_interaction_probe_target'
        sentinel = object()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'component.py'
            for contents in (SOURCE.replace('GUARD', 'True'),
                             'raise ValueError("import failed")',
                             'class Other: pass'):
                source.write_text(contents)
                with self.subTest(contents=contents), patch.dict(sys.modules, {alias: sentinel}):
                    if contents.startswith('from'):
                        with probe.load_class(source, 'Search', root) as factory:
                            self.assertIs(sys.modules[factory.__module__].Search, factory)
                            self.assertIsNone(factory().result)
                    else:
                        with self.assertRaisesRegex(ValueError, 'import failed|class not found'):
                            with probe.load_class(source, 'Search', root):
                                self.fail('invalid source loaded')
                    self.assertIs(sys.modules[alias], sentinel)

    def test_scoped_import_removes_its_registration_after_caller_error(self):
        alias = '_interaction_probe_target'
        with tempfile.TemporaryDirectory() as directory, patch.dict(sys.modules):
            sys.modules.pop(alias, None)
            root = Path(directory)
            source = root / 'component.py'
            source.write_text(SOURCE.replace('GUARD', 'True'))
            with self.assertRaisesRegex(RuntimeError, 'caller failed'):
                with probe.load_class(source, 'Search', root):
                    raise RuntimeError('caller failed')
            self.assertNotIn(alias, sys.modules)

    def test_cli_dataclass_normal_and_stale_fault_keep_native_outcomes(self):
        for guard, status, outcomes in [
                ('generation == self.generation', 0, [True, True]),
                ('True', 1, [True, False])]:
            with self.subTest(guard=guard), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / 'component.py'
                source.write_text(SOURCE.replace('GUARD', guard))
                original = source.read_bytes()
                result = subprocess.run([sys.executable, '-B', probe.__file__,
                    '--root', directory, '--source', 'component.py',
                    '--class-name', 'Search', '--output', 'evidence.json'],
                    capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, status, result.stdout + result.stderr)
                evidence = json.loads(result.stdout)
                self.assertTrue(evidence['complete'])
                self.assertEqual([case['passed'] for case in evidence['cases']], outcomes)
                self.assertEqual(evidence, json.loads((root / 'evidence.json').read_text()))
                self.assertEqual(result.stderr, '')
                self.assertEqual(source.read_bytes(), original)
                if status:
                    self.assertEqual(evidence['cases'][1]['observed']['state'], 'old result')
