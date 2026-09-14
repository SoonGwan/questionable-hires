import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('extractor', ROOT / 'benchmarks/extract_rollout_tools.py')
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)


class RolloutToolsTests(unittest.TestCase):
    def test_retained_model_responses_recover_both_chunks_without_replay(self):
        root = ROOT / 'benchmarks/results/cli-rollout-probe-01'
        records = json.loads((root / 'tool-records.json').read_text())
        chunks = []
        for entry in records['records']:
            payload = entry['record']['payload']
            if payload['type'] == 'custom_tool_call_output':
                chunks.extend(json.loads(block['text']) for block in payload['output']
                              if block['type'] == 'input_text' and block['text'].startswith('{'))
        self.assertEqual(len(chunks), 2)
        combined = ''.join(chunk['output'] for chunk in chunks).encode()
        cell = root / 'cli-yield-probe--baseline--1'
        witness = json.loads((cell / 'project/witness-delayed.json').read_text())
        self.assertEqual(len(combined), witness['bytes'])
        self.assertEqual(hashlib.sha256(combined).hexdigest(), witness['sha256'])
        self.assertIn('session_id', chunks[0])
        self.assertEqual(chunks[1]['exit_code'], 0)
        commands = json.loads((cell / 'commands.json').read_text())
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0]['aggregated_output'], chunks[1]['output'])
        self.assertEqual(records['missing_output_call_ids'], [])
        self.assertEqual(records['unmatched_output_call_ids'], [])

    def fixture(self, directory, identity='own', with_output=True):
        root = Path(directory)
        events = root / 'events.jsonl'
        events.write_text(json.dumps(dict(type='thread.started', thread_id='own')) + '\n')
        rows = [dict(type='session_meta', payload=dict(id=identity)),
                dict(type='response_item', payload=dict(type='message', role='developer', content='PRIVATE')),
                dict(type='response_item', payload=dict(type='custom_tool_call', call_id='a', input='probe'))]
        if with_output:
            rows.append(dict(type='response_item', payload=dict(type='custom_tool_call_output', call_id='a', output='BEGIN\nEND\n')))
        source = root / 'rollout.jsonl'
        source.write_text(''.join(json.dumps(row) + '\n' for row in rows))
        return source, events

    def test_selects_exact_tool_records_not_private_messages(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, events = self.fixture(directory)
            raw, result = extractor.extract(source, events)
            self.assertEqual(raw, source.read_bytes())
            self.assertEqual([r['line'] for r in result['records']], [3, 4])
            self.assertNotIn('PRIVATE', json.dumps(result))
            self.assertEqual(result['missing_output_call_ids'], [])

    def test_refuses_other_session(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, events = self.fixture(directory, identity='other')
            with self.assertRaisesRegex(ValueError, 'requested CLI session'):
                extractor.extract(source, events)

    def test_missing_output_is_explicit_not_a_complete_pair(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, events = self.fixture(directory, with_output=False)
            self.assertEqual(extractor.extract(source, events)[1]['missing_output_call_ids'], ['a'])


if __name__ == '__main__':
    unittest.main()
