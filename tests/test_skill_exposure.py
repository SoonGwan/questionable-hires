import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'benchmarks'))
from inspect_skill_exposure import summarize


class SkillExposureTests(unittest.TestCase):
    def raw(self, *payloads):
        return '\n'.join(json.dumps(dict(type='response_item', payload=p)) for p in payloads).encode()

    def injected(self, name, body):
        return dict(type='message', role='user', content=[dict(text=
            f'<skill>\n<name>{name}</name>\n<path>/private/skill/{name}</path>\n{body}\n</skill>')])

    def test_initial_later_and_actual_tool_output_are_distinct(self):
        entries = {'one': '# One\nbody\n', 'two': '# Two\nother\n'}
        raw = self.raw(self.injected('one', entries['one']),
            dict(type='function_call', arguments='cat skill'),
            self.injected('two', entries['two']),
            dict(type='function_call_output', output=json.dumps(dict(output=entries['one'], exit_code=0))))
        result = summarize(raw, entries)
        self.assertEqual(result['skills']['one']['observations'],
                         [dict(line=1, phase='initial_message'), dict(line=4, phase='tool_output')])
        self.assertEqual(result['skills']['two']['observations'], [dict(line=3, phase='later_message')])
        self.assertNotIn('/private/', json.dumps(result))
        self.assertNotIn(entries['one'], json.dumps(result))

    def test_catalog_announcements_inputs_and_partial_output_are_not_body_reads(self):
        body = '# Example\nImportant specific body.\n'
        raw = self.raw(dict(type='message', role='developer', content=[dict(text='catalog: example/SKILL.md')]),
            dict(type='message', role='assistant', content=[dict(text='Using example.\n' + body)]),
            dict(type='function_call', arguments=body),
            dict(type='function_call_output', output='# Example\nImportant ... truncated'))
        self.assertEqual(summarize(raw, {'example': body})['skills']['example']['observations'], [])

    def test_concatenated_envelopes_and_multiple_bodies(self):
        entries = {'a': '# Alpha\naaa\n', 'b': '# Beta\nbbb\n'}
        output = json.dumps({'output': entries['a']}) + json.dumps({'output': entries['b']})
        raw = self.raw(dict(type='custom_tool_call', input='read'),
                       dict(type='custom_tool_call_output', output=[dict(type='text', text=output)]))
        result = summarize(raw, entries)
        self.assertTrue(all(v['observations'] == [dict(line=2, phase='tool_output')]
                            for v in result['skills'].values()))
