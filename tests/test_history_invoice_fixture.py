import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from history_invoice_cases import cases
from run import prepare


class HistoryInvoiceFixtureTests(unittest.TestCase):
    def test_actual_boundary_controls_and_distinct_history(self):
        case = cases()[0]
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            project = Path(directory) / 'project'
            prepare(case, project)
            source = {p.name: p.read_bytes() for p in project.iterdir() if p.is_file()}
            baseline = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v'],
                                      cwd=project, capture_output=True, text=True, timeout=10)
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            for proposal, expected_code in [('A', 0), ('B', 1)]:
                check = '''import unittest, types
from pathlib import Path
from unittest.mock import patch
import invoice, test_invoice
source = Path('amounts.py').read_text()
if PROPOSAL == 'A':
    source = source.replace('    if isinstance(value, int):\\n        return value\\n', '')
else:
    source = source.replace('return int((Decimal(value) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))', 'return int(Decimal(value) * 100)')
candidate = types.ModuleType('candidate')
exec(compile(source, '<in-memory proposal>', 'exec'), candidate.__dict__)
with patch.object(invoice, 'amount_cents', candidate.amount_cents):
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_invoice))
raise SystemExit(not result.wasSuccessful())
'''.replace('PROPOSAL', repr(proposal))
                observed = subprocess.run([sys.executable, '-B', '-c', check], cwd=project,
                                          capture_output=True, text=True, timeout=10)
                self.assertEqual(observed.returncode, expected_code, observed.stderr)
                self.assertIn('Ran 3 tests', observed.stderr)
                if proposal == 'B':
                    self.assertIn('100 != 101', observed.stderr)
                    self.assertIn('-100 != -101', observed.stderr)
                    self.assertIn('FAILED (failures=2)', observed.stderr)
            self.assertEqual(source, {p.name: p.read_bytes() for p in project.iterdir() if p.is_file()})
            self.assertEqual(list(project.rglob('__pycache__')), [])
            self.assertEqual(subprocess.check_output(['git', 'status', '--porcelain'], cwd=project), b'')
            messages = subprocess.check_output(['git', 'log', '--format=%s', '--reverse'], cwd=project, text=True).splitlines()
            self.assertEqual(messages, [c['message'] for c in case['history']])

    def test_frozen_payload_matches_generator(self):
        self.assertEqual(json.loads((ROOT / 'benchmarks/history-invoice-01-cases.json').read_text()), cases())
