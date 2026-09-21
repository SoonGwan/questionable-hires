import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NativeInspectionAccountingTests(unittest.TestCase):
    def test_all_original_attempts_and_full_inspection_costs_retained(self):
        bundle = json.loads((ROOT / 'benchmarks/results/native-inspection-03.json').read_text())
        observed = bundle['observation']['cases']
        self.assertEqual(set(observed), {'tiny-pass', 'many-pass', 'repeated-failure', 'late-failure'})
        self.assertEqual(set(bundle['artifacts']), set(observed))
        for name, case in observed.items():
            artifacts = bundle['artifacts'][name]
            with self.subTest(name=name):
                self.assertEqual(artifacts['calls.txt']['text'], 'x' * case['executions'])
                self.assertEqual(int(artifacts['exit.txt']['text']), case['native_exit'])
                self.assertEqual(artifacts['case.test.mjs']['original_sha256'], case['source_sha256'])
                for filename, count in case['bytes'].items():
                    self.assertEqual(artifacts[filename]['original_bytes'], count)
                    self.assertEqual(artifacts[filename]['original_sha256'], case['sha256'][filename])
                self.assertTrue(case['stderr_present'])
                self.assertIn('MaxListenersExceededWarning', artifacts['stderr.txt']['text'])
                for native, field in [('raw.tap', 'full_tap_inspection_bytes'), ('raw.spec', 'full_spec_inspection_bytes')]:
                    self.assertEqual(case[field], case['bytes'][native] + case['bytes']['first-look.jsonl'])
                    self.assertGreater(case[field], case['bytes'][native])
        first = bundle['initial_attempt']['artifacts']
        self.assertEqual(first['calls.txt']['text'], 'x')
        self.assertEqual(first['exit.txt']['text'], '0\n')
        self.assertIn('MaxListenersExceededWarning', first['stderr.txt']['text'])
        for artifacts in [*bundle['artifacts'].values(), first]:
            for name, item in artifacts.items():
                with self.subTest(artifact=name):
                    data = item['text'].encode()
                    self.assertEqual(len(data), item['published_bytes'])
                    self.assertEqual(hashlib.sha256(data).hexdigest(), item['published_sha256'])
                    self.assertNotIn(b'/Users/admin', data)
