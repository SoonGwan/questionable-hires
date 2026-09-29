"""Adapter identities plus inherited synthetic guards; no model/history dependency."""
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'benchmarks'))
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
r=load('file_regions01','benchmarks/run_necromancer_file_regions_01.py')
controls=load('file_regions_synthetic_controls','tests/test_urllib3_inline_transfer_02.py');controls.r=r.base
class InheritedControls(controls.Controls):pass
class Adapter(unittest.TestCase):
    def test_changed_resource_and_complete_adapter_identity(self):
        with patch.object(r,'_original_frozen',return_value={'source_hashes':{}}):f=r.frozen(Path('/synthetic-source'),Path('/synthetic-output'))
        self.assertIn(r.CONTROL,f['source_hashes'])
        self.assertIn('benchmarks/run_necromancer_file_regions_01.py',f['source_hashes'])
        self.assertIn('benchmarks/candidates/necromancer-file-regions/skills/necromancer/scripts/python_regions.py',f['source_hashes'])
        self.assertEqual(r.base.RESOURCES['candidate'],('97c15593','benchmarks/candidates/necromancer-file-regions/skills/necromancer'))
        self.assertEqual(r.base.RESOURCES['previous'],('8b1d8163','skills/necromancer'))
