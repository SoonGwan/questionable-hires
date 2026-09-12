import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / 'benchmarks/inspect_output_reuse.py'
spec = importlib.util.spec_from_file_location('output_reuse', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def event(identity, output, kind='item.completed'):
    return dict(type=kind, item=dict(id=identity, type='command_execution',
                                   aggregated_output=output, exit_code=0))


class OutputReuseTests(unittest.TestCase):
    def test_counts_only_prior_command_exact_lines(self):
        line = 'long evidence line\n'
        events = [event('a', line, 'item.started'), event('a', line * 2),
                  event('b', line + 'short\n'), event('c', ' long evidence line\n')]
        result = module.inspect(events, 10)
        self.assertEqual(result['command_count'], 3)
        self.assertEqual([c['recurring_characters'] for c in result['commands']],
                         [0, len(line), 0])
        self.assertEqual(result['output_characters'], sum(len(e['item']['aggregated_output'])
                                                        for e in events[1:]))

    def test_empty_outputs_and_unicode_are_not_inferred_tokens(self):
        line = '관측 결과입니다\n'
        result = module.inspect([event('a', ''), event('b', line), event('c', line)], 3)
        self.assertEqual(result['recurring_characters'], len(line))
        self.assertEqual(result['commands'][0]['output_characters'], 0)
        self.assertNotIn('tokens', result)

    def test_rejects_ambiguous_or_invalid_capture(self):
        for events in ([event('a', ''), event('a', '')], [event(None, '')],
                       [event('a', None)], ['not an object']):
            with self.subTest(events=events), self.assertRaises(ValueError):
                module.inspect(events)
        with self.assertRaises(ValueError):
            module.inspect([], 0)


if __name__ == '__main__':
    unittest.main()
