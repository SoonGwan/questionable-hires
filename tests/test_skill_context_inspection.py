import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from inspect_skill_context import inspect


class SkillContextInspectionTests(unittest.TestCase):
    def fixture(self, directory, before=True, body=None, identity='example'):
        root = Path(directory)
        entry = root / 'SKILL.md'
        expected = '---\nname: friday\ndescription: Example\n---\n# Friday\nKnown instructions.\n'
        entry.write_text(expected)
        message = dict(type='response_item', payload=dict(type='message', role='user', content=[
            dict(type='input_text', text='<skill>\n<name>friday</name>\n<path>/private/path/SKILL.md</path>\n'
                 + (expected if body is None else body) + '\n</skill>')]))
        call = dict(type='response_item', payload=dict(type='custom_tool_call', call_id='one', name='exec', input='list files'))
        initial = dict(type='response_item', payload=dict(type='message', role='developer', content=[
            dict(type='input_text', text='<skills_instructions>\nPRIVATE-INSTRUCTION-MARKER\n'
                 '- friday: Review deployment. (file: r1/friday/SKILL.md)\n'
                 '- example:tool: Useful tool. (file: r2/example/SKILL.md)\n</skills_instructions>')]))
        records = [dict(type='session_meta', payload=dict(id=identity)), initial]
        records += [message, call] if before else [call, message]
        records.append(dict(type='response_item', payload=dict(type='custom_tool_call_output', call_id='one', output=[])))
        rollout, events = root / 'rollout.jsonl', root / 'events.jsonl'
        rollout.write_text(''.join(json.dumps(row) + '\n' for row in records))
        events.write_text(json.dumps(dict(type='thread.started', thread_id='example')) + '\n')
        return rollout, events, entry

    def test_exact_initial_injection_is_identified_without_private_text(self):
        with tempfile.TemporaryDirectory() as directory:
            result = inspect(*self.fixture(directory))
        self.assertTrue(result['matching_entry_before_first_tool'])
        self.assertEqual(result['first_tool_line'], 4)
        self.assertEqual(result['initial_skill_blocks'][0]['line'], 3)
        self.assertEqual(result['initial_catalog_names'], ['friday', 'example:tool'])
        self.assertNotIn('PRIVATE-INSTRUCTION-MARKER', json.dumps(result))
        self.assertNotIn('/private/path', json.dumps(result))
        self.assertNotIn('Known instructions.', json.dumps(result))

    def test_later_body_cannot_be_credited_as_initial_context(self):
        with tempfile.TemporaryDirectory() as directory:
            result = inspect(*self.fixture(directory, before=False))
        self.assertFalse(result['matching_entry_before_first_tool'])
        self.assertEqual(result['initial_skill_blocks'], [])

    def test_wrong_revision_is_not_an_exact_match(self):
        with tempfile.TemporaryDirectory() as directory:
            result = inspect(*self.fixture(directory, body='Different revision\n'))
        self.assertFalse(result['matching_entry_before_first_tool'])
        self.assertFalse(result['initial_skill_blocks'][0]['exact_entry_match'])

    def test_mismatched_session_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'requested CLI session'):
                inspect(*self.fixture(directory, identity='other'))
