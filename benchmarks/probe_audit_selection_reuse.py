"""Native baseline-execution accounting; not model performance evidence."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/con-artist/scripts/audit.py'
SOURCE = "def save(store, value):\n    store.append(value)\n    return True\n"
TESTS = '''import unittest
from service import save
class Tests(unittest.TestCase):
    def test_ack(self):
        self.assertTrue(save([], 'value'))
    def test_stored(self):
        values = []; save(values, 'value'); self.assertEqual(values, ['value'])
'''
SEQUENCES = {'adjacent-control': ['ack', 'ack', 'stored'],
             'revisited-selection': ['ack', 'stored', 'ack'],
             'alternating-eight': ['ack', 'stored'] * 4}


def probe():
    module = importlib.util.spec_from_file_location('selection_reuse', SCRIPT)
    helper = importlib.util.module_from_spec(module)
    module.loader.exec_module(helper)
    native_execute = helper.execute
    report = dict(kind='author native execution-count probe, not model evidence',
        helper_sha256=hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
        python=sys.version.split()[0], source=SOURCE, tests=TESTS, cases={})
    for name, selections in SEQUENCES.items():
        executions = []
        with tempfile.TemporaryDirectory(prefix='audit-reuse-') as folder:
            root = Path(folder)
            (root / 'service.py').write_text(SOURCE)
            (root / 'test_service.py').write_text(TESTS)
            def execute(python, directory, spec, check, timeout):
                result = native_execute(python, directory, spec, check, timeout)
                executions.append(dict(phase=directory.name, selection=spec['tests'],
                    exit_code=result['exit_code'], timed_out=result['timed_out'],
                    output=result['output'].replace(str(root), '<PROJECT>').replace(str(Path(folder).resolve()), '<PROJECT>').replace(sys.executable, '<PYTHON>'),
                    output_truncated=result['output_truncated']))
                return result
            helper.execute = execute
            recipe = dict(files=['service.py', 'test_service.py'], imports=['service', 'test_service'],
                          tests=['-v', 'test_service'], mutations=[dict(target='service.py',
                            old='    store.append(value)\n', new='',
                            tests=['-v', 'test_service.Tests.test_' + selection])
                            for selection in selections])
            result = helper.audit_batch(root, recipe, timeout=5)
            assert result['status'] == 'observed'
            assert [item['checks']['mutant_tests']['exit_code'] for item in result['audits']] == [int(s == 'stored') for s in selections]
            assert (root / 'service.py').read_text() == SOURCE
            assert (root / 'test_service.py').read_text() == TESTS
            assert not list(root.glob('.con-artist-*'))
            for call in executions:
                assert not call['timed_out'] and not call['output_truncated']
                assert 'Ran 1 test' in call['output']
            report['cases'][name] = dict(selections=selections, executions=executions,
                correct_executions=sum(c['phase'] == 'correct-tests' for c in executions),
                mutant_executions=sum(c['phase'] == 'mutant-tests' for c in executions),
                reused=[bool(a.get('correct_tests_reused')) for a in result['audits']],
                originals_preserved=True, owned_scratch_removed=True)
    report['limitations'] = ('Authored deterministic tests, no external state; repeated selections deliberately expose cache topology. '
        'No proposed cache, elapsed-time, token or whole-task gain is measured. Each mutant remains necessary. '
        'Additional reuse would need current identity validation, direct observation references and bounded retained memory.')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # Reserve before execution: never replace an earlier measurement.
    with args.output.open('x') as destination:
        json.dump(probe(), destination, indent=2)
        destination.write('\n')
