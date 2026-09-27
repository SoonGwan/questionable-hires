"""Synthetic scheduling/drift controls; no model calls or repository history."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'benchmarks'))
spec=importlib.util.spec_from_file_location('urllib3_transfer02',ROOT/'benchmarks/run_urllib3_inline_transfer_02.py');r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class Controls(unittest.TestCase):
    def result(self,complete=True,limit=False):return dict(completed=complete,timed_out=not complete,limit_detected=limit,usage={},elapsed_seconds=1)
    def fixture(self,root,results):
        frozen=dict(case={'id':'synthetic','skill':'necromancer'},source_identity={'metadata':'frozen'})
        manifest=dict(frozen,completed_cells=[],stopped=False)
        with patch.object(r,'frozen',return_value=frozen),patch.object(r.run,'disabled_skills',return_value=[]),patch.object(r.run,'run_cell',side_effect=results) as calls:r.execute(Path('/synthetic-source'),root,manifest)
        return manifest,calls
    def test_order_source_and_exclusive_restart(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);m,c=self.fixture(root,[self.result(),self.result()])
            self.assertEqual([x['condition'] for x in m['completed_cells']],['previous','candidate'])
            self.assertEqual(c.call_count,2)
            for call in c.call_args_list:
                self.assertEqual(call.kwargs['project_source'],Path('/synthetic-source'))
                self.assertEqual(call.args[4:7],('gpt-6-astra','medium',360))
            with patch.object(r,'frozen',return_value={}),patch.object(r.run,'run_cell') as again:
                with self.assertRaises(ValueError):r.execute(Path('/synthetic-source'),root,m)
                again.assert_not_called()
    def test_incomplete_and_limit_stop(self):
        for result in [self.result(False),self.result(limit=True)]:
            with tempfile.TemporaryDirectory() as folder:
                m,c=self.fixture(Path(folder),[result]);self.assertTrue(m['stopped']);self.assertEqual(c.call_count,1)
    def test_metadata_drift_prevents_first_call(self):
        with tempfile.TemporaryDirectory() as folder,patch.object(r,'frozen',return_value={'source_identity':{'metadata':'changed'}}),patch.object(r.run,'run_cell') as c:
            with self.assertRaises(ValueError):r.execute(Path('/synthetic-source'),Path(folder),dict(source_identity={'metadata':'frozen'},completed_cells=[],stopped=False))
            c.assert_not_called()
    def test_ignored_metadata_inventory_included(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder);meta=source/r.METADATA;meta.parent.mkdir(parents=True);meta.write_text('genuine metadata placeholder for inventory test only')
            with patch.object(r,'source_identity',return_value={'revision':'synthetic'}):
                first=r.fixture_identity(source);meta.write_text('changed');second=r.fixture_identity(source)
            self.assertNotEqual(first,second);self.assertIn(r.METADATA,first['files'])

    def test_between_cell_drift_stops_second_call(self):
        fixed={'case':{'id':'synthetic'},'source_identity':{'metadata':'frozen'}}
        changed={'case':{'id':'synthetic'},'source_identity':{'metadata':'changed'}}
        with tempfile.TemporaryDirectory() as folder,patch.object(r,'frozen',side_effect=[fixed,fixed,changed]),patch.object(r.run,'disabled_skills',return_value=[]),patch.object(r.run,'run_cell',return_value=self.result()) as calls:
            manifest=dict(fixed,completed_cells=[],stopped=False)
            with self.assertRaises(ValueError):r.execute(Path('/synthetic'),Path(folder),manifest)
            self.assertEqual(calls.call_count,1)
    def test_started_marker_rejects_even_blank_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'execution-started.json').write_text('{}')
            with patch.object(r,'frozen',return_value={'case':{}}),patch.object(r.run,'run_cell') as calls:
                with self.assertRaises(FileExistsError):r.execute(Path('/synthetic'),root,dict(case={},completed_cells=[],stopped=False))
                calls.assert_not_called()
