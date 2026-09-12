import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / 'benchmarks/inspect_usage.py'
spec = importlib.util.spec_from_file_location('usage_inspection', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def event(**overrides):
    usage = dict(input_tokens=100, cached_input_tokens=80, output_tokens=5)
    usage.update(overrides)
    return dict(type='turn.completed', usage=usage)


class UsageInspectionTests(unittest.TestCase):
    def test_cache_is_partition_not_extra_or_removed_cost(self):
        result = module.inspect([dict(type='item.completed'), event()])
        self.assertEqual(result['total_tokens'], 105)
        self.assertEqual(result['uncached_input_tokens'], 20)
        self.assertEqual(result['cached_input_tokens'], 80)
        self.assertEqual(sum(result[k] for k in ('cached_input_tokens', 'uncached_input_tokens', 'output_tokens')), 105)

    def test_rejects_ambiguous_or_invalid_accounting(self):
        for events in ([], [event(), event()], [event(cached_input_tokens=101)],
                       [event(input_tokens=True)], [event(output_tokens=-1)],
                       [event(cached_input_tokens=None)], ['invalid'],
                       [dict(type='other', usage={})]):
            with self.subTest(events=events), self.assertRaises(ValueError):
                module.inspect(events)


if __name__ == '__main__':
    unittest.main()
