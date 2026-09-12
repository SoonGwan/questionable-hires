import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('catalog_validator', ROOT / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class IssueFormTests(unittest.TestCase):
    def test_shipped_forms_pass(self):
        self.assertEqual(validator.validate_issue_forms(ROOT), [])

    def test_broken_forms_return_diagnostics_not_tracebacks(self):
        original = yaml.safe_load((ROOT / '.github/ISSUE_TEMPLATE/bug_report.yml').read_text())
        mutations = [None, {'name': 'empty'}, dict(original, body=[]),
                     dict(original, body=['not a field'])]
        duplicate = copy.deepcopy(original)
        duplicate['body'][1]['id'] = duplicate['body'][0]['id']
        mutations.append(duplicate)
        required = copy.deepcopy(original)
        required['body'][0]['validations']['required'] = 'true'
        mutations.append(required)
        blank = copy.deepcopy(original)
        blank['body'][0]['attributes']['label'] = ' '
        mutations.append(blank)
        missing_type = copy.deepcopy(original)
        del missing_type['body'][0]['type']
        mutations.append(missing_type)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / '.github/ISSUE_TEMPLATE'
            folder.mkdir(parents=True)
            (folder / 'new_hire.yml').write_bytes((ROOT / '.github/ISSUE_TEMPLATE/new_hire.yml').read_bytes())
            for value in mutations:
                with self.subTest(value=value):
                    (folder / 'bug_report.yml').write_text(yaml.safe_dump(value))
                    errors = validator.validate_issue_forms(root)
                    self.assertEqual(len(errors), 1)
                    self.assertIn('bug_report.yml', errors[0])
            (folder / 'bug_report.yml').write_text('body: [')
            self.assertEqual(len(validator.validate_issue_forms(root)), 1)
            (folder / 'bug_report.yml').unlink()
            self.assertEqual(len(validator.validate_issue_forms(root)), 1)
