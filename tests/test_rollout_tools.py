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
    def capture_fixture(self, directory, captured, outputs, exit_code=0):
        source, events = self.fixture(directory, with_output=False)
        rows = [json.loads(line) for line in source.read_text().splitlines()]
        # Replace the simple call with actual structured command-result envelopes.
        rows = rows[:2]
        for index, output in enumerate(outputs):
            call_id = 'call-' + str(index)
            rows.extend([
                dict(type='response_item', payload=dict(type='custom_tool_call',
                     call_id=call_id, name='functions.exec', input='command ' + str(index))),
                dict(type='response_item', payload=dict(type='custom_tool_call_output',
                     call_id=call_id, output=[dict(type='input_text', text=json.dumps(output))]))])
        source.write_text(''.join(json.dumps(row) + '\n' for row in rows))
        with events.open('a') as stream:
            stream.write(json.dumps(dict(type='item.completed', item=dict(
                id='item_1', type='command_execution', command='python3 -B -m unittest -v',
                aggregated_output=captured, exit_code=exit_code, status='completed'))) + '\n')
        return source, events

    def test_short_summary_identifies_original_output_without_private_messages(self):
        short = '\n----------------------------------------------------------------------\nRan 7 tests in 0.046s\n\nOK\n'
        self.assertEqual(len(short), 98)
        full = ''.join('test_%d (Tests) ... ok\n' % index for index in range(7)) + short
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, events = self.capture_fixture(directory, short, [dict(output=full, exit_code=0)])
            original_source, original_events = source.read_bytes(), events.read_bytes()
            raw, result = extractor.extract(source, events)
            match = result['command_output_candidates'][0]
            self.assertEqual(match['status'], 'single_candidate')
            candidate = match['candidates'][0]
            self.assertEqual(candidate['output_sha256'], hashlib.sha256(full.encode()).hexdigest())
            stored = next(r for r in result['records'] if r['line'] == candidate['output_line'])
            block = stored['record']['payload']['output'][candidate['output_block_index']]
            self.assertEqual(json.loads(block['text'])['output'], full)
            self.assertEqual(match['candidates'][0]['relation'], 'longer_suffix_match')
            self.assertEqual(match['candidates'][0]['call_id'], 'call-0')
            self.assertNotIn('PRIVATE', json.dumps(result))
            self.assertEqual(source.read_bytes(), original_source)
            self.assertEqual(events.read_bytes(), original_events)
            self.assertEqual(result['cli_events_sha256'], hashlib.sha256(original_events).hexdigest())

    def test_ambiguous_suffix_does_not_select_one_output(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, events = self.capture_fixture(directory, 'OK\n', [
                dict(output='first\nOK\n', exit_code=0), dict(output='second\nOK\n', exit_code=0)])
            match = extractor.extract(source, events)[1]['command_output_candidates'][0]
            self.assertEqual(match['status'], 'ambiguous')
            self.assertEqual(len(match['candidates']), 2)

    def test_empty_capture_cannot_match_every_output(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, events = self.capture_fixture(directory, '', [dict(output='OK\n', exit_code=0)])
            match = extractor.extract(source, events)[1]['command_output_candidates'][0]
            self.assertEqual(match['status'], 'empty_cli_output')
            self.assertEqual(match['candidates'], [])

    def test_exit_mismatch_running_result_and_non_command_object_are_not_candidates(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, events = self.capture_fixture(directory, 'OK\n', [
                dict(output='first\nOK\n', exit_code=1), dict(output='running\nOK\n', session_id=42),
                dict(output='false boolean exit\nOK\n', exit_code=False), dict(text='OK\n')])
            match = extractor.extract(source, events)[1]['command_output_candidates'][0]
            self.assertEqual(match['status'], 'unmatched')
            self.assertEqual(match['candidates'], [])

    def test_unpaired_or_duplicate_call_cannot_establish_output_binding(self):
        for variant in ('missing_call', 'duplicate_call', 'duplicate_output'):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory(dir=ROOT) as directory:
                source, events = self.capture_fixture(directory, 'OK\n', [dict(output='first\nOK\n', exit_code=0)])
                rows = [json.loads(line) for line in source.read_text().splitlines()]
                if variant == 'duplicate_call':
                    rows.insert(3, rows[2])
                elif variant == 'duplicate_output':
                    rows.append(rows[-1])
                else:
                    del rows[2]
                source.write_text(''.join(json.dumps(row) + '\n' for row in rows))
                match = extractor.extract(source, events)[1]['command_output_candidates'][0]
                self.assertEqual(match['status'], 'unmatched')
                self.assertEqual(match['candidates'], [])

    def test_string_envelope_equal_match_keeps_cli_and_source_line_identity(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            source, events = self.capture_fixture(directory, 'one\n', [dict(output='one\n', exit_code=0)])
            rows = [json.loads(line) for line in source.read_text().splitlines()]
            rows[-1]['payload']['output'] = rows[-1]['payload']['output'][0]['text']
            source.write_text(''.join(json.dumps(row) + '\n' for row in rows))
            result = extractor.extract(source, events)[1]
            match = result['command_output_candidates'][0]
            candidate = match['candidates'][0]
            self.assertEqual(match['cli_event_line'], 2)
            self.assertEqual(candidate['relation'], 'equal')
            self.assertIsNone(candidate['output_block_index'])
            raw_lines = source.read_bytes().splitlines()
            for kind in ('call', 'output'):
                self.assertEqual(candidate[kind + '_line_sha256'],
                                 hashlib.sha256(raw_lines[candidate[kind + '_line'] - 1]).hexdigest())

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
