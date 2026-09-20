import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import sequence_entry_case as fixture


class SequenceEntryCaseTests(unittest.TestCase):
    def test_frozen_inputs_match_actual_repository_replay_hashes(self):
        case = fixture.cases()[0]
        replay = json.loads((ROOT / 'benchmarks/sequence-entry-repository-preflight-01.json').read_text())
        self.assertEqual(json.loads(case['files']['selected-tests.json']), replay['selected_tests'])
        for name, digest in replay['fixed_sha256'].items():
            self.assertEqual(hashlib.sha256(case['working_files'][name].encode()).hexdigest(), digest)
        for index, row in enumerate(replay['rows']):
            raw = case['history'][index]['files'][fixture.IMPLEMENTATION]
            self.assertEqual(hashlib.sha256(raw.encode()).hexdigest(), row['implementation_sha256'])

    def test_exact_extracted_project_native_controls(self):
        rows = fixture.preflight()
        self.assertEqual([row['exit_code'] for row in rows], [1, 0])
        self.assertEqual(rows[0]['output'].count('TimeoutError\n'), 4)
        self.assertIn('Ran 8 tests', rows[1]['output'])
        self.assertIn('\nOK\n', rows[1]['output'])
