import ast
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
import probe_edit_transfer_cases as fixture


class ProbeEditTransferTests(unittest.TestCase):
    def test_full_source_and_prefix_preserve_declared_upstream_content(self):
        variants,_,_ = fixture.inputs()
        self.assertEqual(variants['full'],fixture.validate_files(json.loads(fixture.SNAPSHOT.read_text())))
        full,prefix = variants['full'],variants['prefix']
        self.assertEqual(set(full),set(prefix))
        self.assertEqual([k for k in full if full[k]!=prefix[k]],[fixture.TEST_FILE])
        self.assertTrue(full[fixture.TEST_FILE].startswith(prefix[fixture.TEST_FILE]))
        self.assertEqual(len(full[fixture.TEST_FILE].encode()),30731)
        self.assertEqual(len(prefix[fixture.TEST_FILE].encode()),816)
        def method(source):
            cls=next(n for n in ast.parse(source).body if isinstance(n,ast.ClassDef) and n.name=='TestSpecifier')
            return next(n for n in cls.body if isinstance(n,ast.FunctionDef))
        self.assertEqual(ast.dump(method(full[fixture.TEST_FILE])),ast.dump(method(prefix[fixture.TEST_FILE])))

    def test_only_selected_method_return_is_changed_by_fault(self):
        variants,fault,_=fixture.inputs()
        source=variants['full'][fixture.TARGET]
        self.assertEqual(source.count(fault['old']),1)
        expected=ast.parse(source)
        cls=next(n for n in expected.body if isinstance(n,ast.ClassDef) and n.name=='Specifier')
        method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=='__str__')
        returned,=[n for n in method.body if isinstance(n,ast.Return)]
        returned.value=ast.Constant(value='')
        actual=ast.parse(source.replace(fault['old'],fault['new'],1))
        self.assertEqual(ast.dump(actual),ast.dump(expected))

    def test_forms_produce_identical_test_bytes_and_native_selectors(self):
        variants,fault,edit=fixture.inputs()
        for files in variants.values():
            full=fixture.recipe(files,fault,edit,'replacement')
            partial=fixture.recipe(files,fault,edit,'edit')
            self.assertEqual(files[fixture.TEST_FILE].count(edit['old']),1)
            output=files[fixture.TEST_FILE].encode().replace(edit['old'].encode(),edit['new'].encode(),1)
            self.assertEqual(output,full['probe_replacements'][fixture.TEST_FILE].encode())
            self.assertEqual(full['tests'],partial['tests'])
            self.assertEqual(full['probe_tests'],partial['probe_tests'])
            self.assertEqual(ast.parse(output).body[0].__class__,ast.Import)

    def test_retained_native_output_identifies_expected_test_file_in_every_phase(self):
        variants,_,edit=fixture.inputs()
        report=json.loads((ROOT/'benchmarks/results/probe-edit-transfer-01-preflight.json').read_text())
        self.assertEqual({(r['variant'],r['form']) for r in report['records']},
                         {(v,f) for v in ('full','prefix') for f in ('replacement','edit')})
        for row in report['records']:
            source=variants[row['variant']][fixture.TEST_FILE]
            self.assertEqual(row['fresh_import']['exit_code'],0)
            for phase,check in row['result']['checks'].items():
                expected=source.replace(edit['old'],edit['new'],1) if phase.endswith('probe') else source
                record,=re.findall(r'Verified copied import: tests.test_specifiers (\{[^\n]+\})',check['output'])
                self.assertEqual(json.loads(record)['sha256'],hashlib.sha256(expected.encode()).hexdigest())
                code=1 if phase=='mutant_probe' else 0
                self.assertEqual(check['exit_code'],code)
                self.assertIn('9 failed' if code else '9 passed',check['output'])
                self.assertFalse(check['timed_out'] or check['output_truncated'])
