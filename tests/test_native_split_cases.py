"""Native source/consumer controls; no model calls or outcome-based selection."""
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
import native_split_cases_02 as fixture
import run_native_split_02 as runner


class NativeSplitCasesTests(unittest.TestCase):
    def test_original_native_suite_survives_and_consumer_detects_all_faults(self):
        result=fixture.preflight()
        self.assertEqual(len(result['native_controls']),8)
        for row in result['native_controls']:
            self.assertIn('Ran 13 tests' if row['selection']=='original' else 'Ran 1 test',row['output'])
            if row['selection']=='original' or row['variant']=='correct':
                self.assertEqual(row['exit_code'],0)
            else:
                self.assertEqual(row['exit_code'],1)
                self.assertIn('AssertionError: Lists differ:',row['output'])
                self.assertNotIn('ImportError',row['output'])

    def test_source_change_rejected_before_case_creation(self):
        real=Path.read_text
        def changed(path,*args,**kwargs):
            value=real(path,*args,**kwargs)
            if path==fixture.SOURCE:
                data=json.loads(value);data['more_itertools/more.py']+='\n# changed\n'
                return json.dumps(data)
            return value
        with patch.object(Path,'read_text',changed):
            with self.assertRaisesRegex(ValueError,'Pinned source bytes differ'):
                fixture.cases(Path(sys.executable))

    def test_distinct_mutations_and_scheduled_inputs_preserve_unrelated_functions(self):
        import ast
        source=fixture.files()['more_itertools/more.py']
        originals={n.name:ast.dump(n) for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)}
        for mutation in fixture.mutations():
            modified=source.replace(mutation['old'],mutation['new'])
            actual={n.name:ast.dump(n) for n in ast.parse(modified).body if isinstance(n,ast.FunctionDef)}
            self.assertEqual([name for name in originals if actual[name]!=originals[name]],[mutation['id']])
        self.assertEqual(len(runner.driver.SCHEDULE),6)
        self.assertEqual(runner.driver.CONDITIONS,('baseline','predecessor','current'))
        self.assertEqual(runner.driver.RESOURCE,'6c099d68')
        cases=fixture.cases(Path(sys.executable))
        self.assertEqual([c['id'] for c in cases],['native-split-single','native-split-multiple'])
        self.assertEqual(cases[0]['files'],cases[1]['files'])
