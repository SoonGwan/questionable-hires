"""Reconcile native capture evidence without launching Codex or a model."""
import base64
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / 'benchmarks/results/app-server-native-capture-01'


class NativeCaptureTests(unittest.TestCase):
    def check_record(self, name, identity):
        events = [json.loads(line) for line in (ROOT / 'server-events.jsonl').read_text().splitlines()]
        record = json.loads((ROOT / (name + '.json')).read_text())
        chunks = [e['params'] for e in events if e.get('method') == 'command/exec/outputDelta'
                  and e['params']['processId'] == name]
        self.assertEqual(record['chunks'], chunks)
        response_index = next(i for i, e in enumerate(events) if e.get('id') == identity)
        self.assertEqual(record['response'], events[response_index])
        for i, event in enumerate(events):
            if event.get('method') == 'command/exec/outputDelta' and event['params']['processId'] == name:
                self.assertLess(i, response_index)
        for stream in ('stdout', 'stderr'):
            payload = b''.join(base64.b64decode(c['deltaBase64'], validate=True)
                               for c in chunks if c['stream'] == stream)
            self.assertEqual(payload.decode(), record['streams'][stream])
            self.assertEqual(record['response']['result'][stream], '')
        return record

    def test_delayed_payload_hash_and_markers_preserved(self):
        record = self.check_record('delayed', 1)
        witness = json.loads((ROOT / 'project/witness-delayed.json').read_text())
        payload = record['streams']['stdout'].encode()
        self.assertEqual(len(payload), witness['bytes'])
        self.assertEqual(hashlib.sha256(payload).hexdigest(), witness['sha256'])
        self.assertEqual(record['response']['result']['exitCode'], 0)
        self.assertFalse(any(c['capReached'] for c in record['chunks']))

    def test_actual_assertion_not_setup_error(self):
        record = self.check_record('assertion', 2)
        self.assertEqual(record['response']['result']['exitCode'], 1)
        self.assertEqual(record['streams']['stdout'], 'BEFORE_ASSERT\n')
        self.assertIn('AssertionError: actual=1 expected=2', record['streams']['stderr'])

    def test_zero_exit_does_not_hide_truncation(self):
        record = self.check_record('capped', 3)
        self.assertEqual(record['response']['result']['exitCode'], 0)
        self.assertEqual(record['streams']['stdout'], 'x' * 16)
        self.assertTrue(any(c['capReached'] for c in record['chunks']))

    def test_timeout_preserves_prior_output(self):
        record = self.check_record('timeout', 4)
        self.assertEqual(record['response']['result']['exitCode'], 124)
        self.assertEqual(record['streams']['stdout'], 'BEFORE_WAIT\n')


if __name__ == '__main__':
    unittest.main()
