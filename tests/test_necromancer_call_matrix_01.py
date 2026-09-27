"""Adapter route checks, no Codex or Git history; scheduling tests reused."""
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'benchmarks'))
spec=importlib.util.spec_from_file_location('matrix_pair',ROOT/'benchmarks/run_necromancer_call_matrix_01.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class Routes(unittest.TestCase):
    def test_candidate_uses_new_helper_bundle_and_previous_uses_ordinary(self):
        with patch.object(r,'_original_snapshot') as capture:
            r.snapshot(Path('/synthetic'),'candidate','c889175e','old-candidate')
            self.assertEqual(capture.call_args.args[-1],'benchmarks/candidates/necromancer-call-matrix/skills/necromancer')
            r.snapshot(Path('/synthetic'),'previous','ddb7ad29','skills/necromancer')
            self.assertEqual(capture.call_args.args[-1],'skills/necromancer')

    def test_adapter_identity_is_frozen_with_resource_versions(self):
        with patch.object(r,'_original_frozen',return_value={'source_hashes':{}}):
            f=r.frozen(Path('/synthetic'))
        self.assertEqual(f['resource_revisions'],{'previous':'ddb7ad29','candidate':'c889175e'})
        self.assertIn('benchmarks/run_necromancer_call_matrix_01.py',f['source_hashes'])
        self.assertIn('tests/test_necromancer_call_matrix_01.py',f['source_hashes'])
