"""Reject ambiguous recipes before SQL instead of silently dropping declared work."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1]/'skills/friday/scripts/sqlite_matrix.py'
spec = importlib.util.spec_from_file_location('friday_recipe_keys', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class FridayRecipeKeysTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='friday recipe ')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root/'readers.py').write_text('QUERY = "SELECT 1 AS value"\n')
        (self.root/'readers.py').chmod(0o640)

    def invoke(self, raw, from_file=False):
        path = self.root/'recipe.json'
        if from_file:
            path.write_text(raw)
        before = {p.name:(p.read_bytes(),p.stat().st_mode&0o777) for p in self.root.iterdir()}
        result = subprocess.run([sys.executable,'-I','-B',str(SCRIPT),'--source',str(self.root),
                                 '--spec',str(path) if from_file else '-'],
                                input='' if from_file else raw,text=True,capture_output=True,timeout=10)
        self.assertEqual(before,{p.name:(p.read_bytes(),p.stat().st_mode&0o777) for p in self.root.iterdir()})
        return result

    def reject(self, raw, key, from_file=False):
        result = self.invoke(raw,from_file)
        self.assertEqual(result.returncode,2,(result.stdout,result.stderr))
        report = json.loads(result.stdout)
        self.assertFalse(report['complete'])
        self.assertIn('Duplicate recipe key: '+json.dumps(key),report['error'])
        self.assertNotIn('phases',report)
        self.assertEqual(result.stderr,'')
        return result

    def test_duplicate_root_fields_cannot_replace_phases_or_checks(self):
        for key, raw in [
            ('phases','{"phases":[{"name":"lost","sql":"DROP TABLE missing;"}],"phases":[{"name":"kept"}],"checks":{"reader":"SELECT 1"}}'),
            ('checks','{"phases":[{"name":"initial"}],"checks":{"lost":"SELECT missing"},"checks":{"kept":"SELECT 1"}}')]:
            for from_file in (False,True):
                with self.subTest(key=key,from_file=from_file):
                    self.reject(raw,key,from_file)

    def test_duplicate_check_label_cannot_hide_a_failing_native_reader(self):
        raw='{"phases":[{"name":"initial","sql":"CREATE TABLE data(value);INSERT INTO data VALUES(1);"}],"checks":{"consumer":"SELECT missing FROM data","consumer":"SELECT value FROM data"}}'
        self.reject(raw,'consumer')

    def test_duplicate_phase_fields_are_rejected_at_their_own_object(self):
        for key, fragment in [
            ('sql','"name":"initial","sql":"DROP TABLE missing;","sql":""'),
            ('files','"name":"initial","files":["missing.sql"],"files":[]'),
            ('checks','"name":"initial","checks":["missing"],"checks":["reader"]'),
            ('name','"name":"discarded","name":"kept"')]:
            with self.subTest(key=key):
                self.reject('{"phases":[{'+fragment+'}],"checks":{"reader":"SELECT 1"}}',key)

    def test_duplicate_literal_reader_reference_fields_are_rejected(self):
        for key, reference in [
            ('python_file','"python_file":"absent.py","python_file":"readers.py","constant":"QUERY"'),
            ('constant','"python_file":"readers.py","constant":"MISSING","constant":"QUERY"')]:
            with self.subTest(key=key):
                self.reject('{"phases":[{"name":"initial"}],"checks":{"reader":{'+reference+'}}}',key)

    def test_escaped_duplicate_names_compare_decoded_keys_without_printing_values(self):
        raw=r'{"phases":[{"name":"initial"}],"checks":{"reader":"SECRET_FIRST","\u0072eader":"SECRET_SECOND"}}'
        result=self.reject(raw,'reader')
        self.assertNotIn('SECRET_',result.stdout+result.stderr)

    def test_duplicate_rejection_precedes_matrix_input_reads_and_sql_connection(self):
        raw='{"phases":[{"name":"initial"}],"checks":{"reader":"SELECT 1","reader":"SELECT 2"}}'
        output=io.StringIO()
        with patch.object(sys,'argv',['sqlite_matrix.py','--spec','-','--source',str(self.root)]), \
                patch.object(sys,'stdin',io.StringIO(raw)), contextlib.redirect_stdout(output), \
                patch.object(helper,'matrix',wraps=helper.matrix) as matrix, \
                patch.object(helper.sqlite3,'connect',wraps=helper.sqlite3.connect) as connect:
            code=helper.main()
        self.assertEqual(code,2,output.getvalue())
        matrix.assert_not_called()
        connect.assert_not_called()

    def test_valid_repeated_phase_labels_and_query_values_preserve_native_observations(self):
        recipe=dict(phases=[dict(name='checkpoint',sql='CREATE TABLE data(value BLOB);INSERT INTO data VALUES(x\'00ff\');'),
                            dict(name='checkpoint')],
                    checks={'first':'SELECT value AS label, value AS label FROM data',
                            'second':'SELECT value AS label, value AS label FROM data'})
        for from_file in (False,True):
            with self.subTest(from_file=from_file):
                result=self.invoke(json.dumps(recipe),from_file)
                self.assertEqual(result.returncode,0,result.stderr)
                report=json.loads(result.stdout);self.assertTrue(report['complete'])
                self.assertEqual(len(report['phases']),2)
                for phase in report['phases']:
                    for observed in phase['checks'].values():
                        self.assertEqual(observed,dict(ok=True,columns=['label','label'],
                            rows=[[{'blob_hex':'00ff'},{'blob_hex':'00ff'}]],truncated=False))

    def test_long_duplicate_key_has_bounded_error_and_no_values(self):
        key='x'*2000
        raw='{"phases":[{"name":"initial"}],"checks":{'+json.dumps(key)+':"SECRET_A",'+json.dumps(key)+':"SECRET_B"}}'
        result=self.invoke(raw)
        self.assertEqual(result.returncode,2,result.stdout)
        report=json.loads(result.stdout)
        self.assertIn('Duplicate recipe key:',report['error'])
        self.assertLess(len(report['error']),300)
        self.assertNotIn('SECRET_',result.stdout+result.stderr)


if __name__=='__main__':
    unittest.main()
