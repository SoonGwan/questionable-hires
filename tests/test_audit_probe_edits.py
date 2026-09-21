"""Small test edits retain the full native comparison contract."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/con-artist/scripts/audit.py'
SPEC = importlib.util.spec_from_file_location('edit_audit', SCRIPT)
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class ProbeEditTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.source = 'def save(values):\n    values.append("item")\n    return True\n'
        self.old = '        self.assertTrue(save(values))\n'
        self.new = self.old + '        self.assertEqual(values, ["item"])\n'
        self.weak = ('import unittest\nfrom service import save\nclass Tests(unittest.TestCase):\n'
                     '    def test_save(self):\n        values = []\n' + self.old)
        (self.root/'service.py').write_text(self.source)
        (self.root/'test_service.py').write_text(self.weak)
        (self.root/'test_service.py').chmod(0o640)
        self.recipe = dict(files=['service.py','test_service.py'], imports=['service','test_service'],
            tests=['-v','test_service'], target='service.py', old='    values.append("item")\n', new='',
            probe_edits={'test_service.py':dict(old=self.old,new=self.new)},
            probe_tests=['-v','test_service'])

    def test_native_four_checks_preserve_bytes_modes_and_cleanup(self):
        real_execute = helper.execute
        seen = []
        def inspect(python, directory, spec, probe, timeout):
            expected = self.weak.replace(self.old,self.new) if directory.name.endswith('-probe') else self.weak
            self.assertEqual((directory/'test_service.py').read_text(),expected)
            self.assertEqual((directory/'test_service.py').stat().st_mode & 0o777,0o640)
            seen.append(directory)
            return real_execute(python,directory,spec,probe,timeout)
        with patch.object(helper,'execute',inspect):
            result = helper.audit(self.root,self.recipe)
        self.assertEqual({k:v['exit_code'] for k,v in result['checks'].items()},
            dict(correct_tests=0,correct_probe=0,mutant_tests=0,mutant_probe=1))
        self.assertIn("[] != ['item']",result['checks']['mutant_probe']['output'])
        self.assertTrue(all('Ran 1 test' in v['output'] for v in result['checks'].values()))
        self.assertEqual(len(set(seen)),4)
        self.assertTrue(all(not p.exists() for p in seen))
        self.assertEqual((self.root/'test_service.py').read_text(),self.weak)
        self.assertEqual((self.root/'service.py').read_text(),self.source)

    def test_cli_and_native_module_mode(self):
        result = subprocess.run([sys.executable,'-I','-B',str(SCRIPT),'--source',str(self.root),'--spec','-'],
            input=json.dumps(dict(self.recipe,invocation='module')),capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        checks = json.loads(result.stdout)['checks']
        self.assertEqual(checks['correct_probe']['native_exit_code'],0)
        self.assertEqual(checks['mutant_probe']['native_exit_code'],1)
        self.assertIn('AssertionError',checks['mutant_probe']['output'])

    def test_invalid_edits_rejected_before_execution(self):
        edits = [{}, [], {'missing.py':dict(old='x',new='y')},
            {'service.py':dict(old='True',new='False')}, {'../outside':dict(old='x',new='y')},
            {'test_service.py':dict(old='',new='x')}, {'test_service.py':dict(old='absent',new='x')},
            {'test_service.py':dict(old='self',new='other')},
            {'test_service.py':dict(old=self.old,new=self.old)},
            {'test_service.py':dict(old=self.old,new=3)}, {'test_service.py':dict(old=self.old,new='x',count=1)},
            {'test_service.py':dict(old=self.old,new=self.new),'./test_service.py':dict(old=self.old,new=self.new)}]
        for edit in edits:
            with self.subTest(edit=edit),patch.object(helper,'execute') as execute:
                with self.assertRaises(ValueError):
                    helper.audit(self.root,dict(self.recipe,probe_edits=edit))
                execute.assert_not_called()
        for extra in [dict(probe='assert True'),dict(probe_tests=[]),
                      dict(probe_replacements={'test_service.py':self.weak}),
                      dict(probe_files={'test_service.py':'pass'})]:
            with self.subTest(extra=extra),patch.object(helper,'execute') as execute:
                with self.assertRaises(ValueError):
                    helper.audit(self.root,dict(self.recipe,**extra))
                execute.assert_not_called()

    def test_batch_compares_materialized_bytes_not_edit_syntax(self):
        common = {k:self.recipe[k] for k in ('files','imports','tests')}
        fault = {k:v for k,v in self.recipe.items() if k not in common}
        full = dict(fault,probe_replacements={'test_service.py':self.weak.replace(self.old,self.new)})
        del full['probe_edits']
        changed = dict(fault,probe_edits={'test_service.py':dict(old=self.old,new=self.new+'        # different\n')})
        result = helper.audit_batch(self.root,dict(common,mutations=[fault,full,changed]))
        first,same,different = result['audits']
        self.assertEqual(first['status'],'observed')
        self.assertTrue(same['correct_probe_reused'])
        self.assertEqual(same['checks']['correct_probe']['observation_ref'],'#/audits/0/checks/correct_probe')
        self.assertNotIn('correct_probe_reused',different)
        self.assertTrue(all(a['checks']['mutant_probe']['exit_code']==1 for a in result['audits']))

    def test_budget_counts_complete_result_even_for_small_edit(self):
        large = self.weak + '#' + 'x'*10_000_000
        (self.root/'test_service.py').write_text(large)
        with patch.object(helper,'execute') as execute:
            with self.assertRaisesRegex(ValueError,'20 MB'):
                helper.audit(self.root,self.recipe)
            execute.assert_not_called()

    @unittest.skipUnless(importlib.util.find_spec('pytest'), 'pytest not installed')
    def test_pytest_fixture_and_assertion_rewriting_are_preserved(self):
        weak = ('import pytest\nfrom service import save\n@pytest.fixture\n'
                'def values(): return []\ndef test_save(values):\n    assert save(values)\n')
        (self.root/'test_service.py').write_text(weak)
        recipe = dict(self.recipe, runner='pytest',tests=['-q','test_service.py'],
            probe_tests=['-q','test_service.py'], probe_edits={'test_service.py':dict(
                old='    assert save(values)\n',new='    assert save(values)\n    assert values == ["item"]\n')})
        result = helper.audit(self.root,recipe)
        self.assertEqual({k:v['exit_code'] for k,v in result['checks'].items()},
            dict(correct_tests=0,correct_probe=0,mutant_tests=0,mutant_probe=1))
        self.assertIn("assert [] == ['item']",result['checks']['mutant_probe']['output'])
        self.assertEqual((self.root/'test_service.py').read_text(),weak)

    def test_edit_preserves_unmodified_crlf_and_unicode_bytes(self):
        raw = ('# café\r\n' + self.weak.replace('\n','\r\n')).encode()
        (self.root/'test_service.py').write_bytes(raw)
        old = self.old.replace('\n','\r\n')
        new = self.new.replace('\n','\r\n')
        real_execute = helper.execute
        def inspect(python,directory,spec,probe,timeout):
            expected = raw.replace(old.encode(),new.encode(),1) if directory.name.endswith('-probe') else raw
            self.assertEqual((directory/'test_service.py').read_bytes(),expected)
            return real_execute(python,directory,spec,probe,timeout)
        with patch.object(helper,'execute',inspect):
            result = helper.audit(self.root,dict(self.recipe,probe_edits={'test_service.py':dict(old=old,new=new)}))
        self.assertEqual(result['checks']['mutant_probe']['exit_code'],1)
        self.assertEqual((self.root/'test_service.py').read_bytes(),raw)
