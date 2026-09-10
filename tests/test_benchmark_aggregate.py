import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('aggregate', Path(__file__).resolve().parents[1] / 'benchmarks/aggregate.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


def cell(case, arm, repeat, value, **extra):
    return dict(case=case, arm=arm, repeat=repeat, completed=True, timed_out=False,
                usage={}, total_tokens=value, elapsed_seconds=value, **extra)


class AggregateTests(unittest.TestCase):
    def test_mean_of_case_ratios_not_ratio_of_pooled_means(self):
        rows = [cell(c, arm, 1, value) for c, values in [('small', [10, 20, 30]), ('large', [100, 100, 100])]
                for arm, value in zip(a.ARMS, values)]
        data = a.summarize(rows)['normalized']['total_tokens']
        self.assertEqual(data['arms']['control']['mean'], 150)
        self.assertEqual(data['arms']['skill']['mean'], 200)
        self.assertEqual(data['arms']['skill']['min'], 100)
        self.assertEqual(data['arms']['skill']['max'], 300)

    def test_case_means_before_ratios_and_equal_task_weight(self):
        rows = [cell('one', arm, rep, value) for rep, values in [(1, [10, 30, 10]), (2, [30, 30, 30])]
                for arm, value in zip(a.ARMS, values)]
        self.assertEqual(a.summarize(rows)['normalized']['total_tokens']['arms']['control']['mean'], 150)

    def test_zero_baseline_is_undefined_even_zero_over_zero(self):
        self.assertIsNone(a.ratio(0, 0))
        self.assertIsNone(a.ratio(20, 0))
        rows = [cell('zero', arm, 1, 0) for arm in a.ARMS]
        result = a.summarize(rows)['normalized']['total_tokens']
        self.assertEqual(result['zero_baseline_cases'], ['zero'])
        self.assertIsNone(result['arms']['baseline']['mean'])

    def test_timeout_and_missing_metrics_exclude_whole_block_but_retain_time(self):
        rows = [cell('one', arm, 1, 10) for arm in a.ARMS]
        rows[2].update(timed_out=True, completed=False, elapsed_seconds=240)
        data = a.summarize(rows)
        self.assertEqual(data['normalized']['total_tokens']['excluded_blocks'], 1)
        self.assertEqual(data['execution']['skill']['all_attempt_wall_seconds']['mean'], 240)
        self.assertEqual(data['execution']['skill']['timeouts'], 1)
        rows[2].update(timed_out=False, completed=True, total_tokens=None)
        self.assertEqual(a.summarize(rows)['normalized']['total_tokens']['eligible_blocks'], 0)

    def test_duplicate_cells_rejected(self):
        row = cell('one', 'skill', 1, 10)
        with self.assertRaises(ValueError):
            a.summarize([row, row])

    def test_token_cache_not_added_twice_and_loc_only_implementation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for case in ['boundary-fix', 'history-active']:
                c = root / f'{case}--skill--1'
                c.mkdir()
                (c / 'metadata.json').write_text(json.dumps(dict(case=case, arm='skill', repeat=1, usage={
                    'input_tokens': 100, 'cached_input_tokens': 80, 'output_tokens': 20})))
                (c / 'changes.diff').write_text('diff --git a/eligibility.py b/eligibility.py\n--- a/eligibility.py\n+++ b/eligibility.py\n-old\n+new\ndiff --git a/test_x.py b/test_x.py\n+test\n')
            rows = a.read_cells(root)
            self.assertEqual(rows[0]['total_tokens'], 120)
            self.assertEqual(rows[0]['uncached_input_tokens'], 20)
            self.assertEqual(rows[0]['changed_loc'], 3)
            self.assertEqual(rows[0]['loc_by_type'], {'production': 2, 'tests': 1})
            self.assertIsNone(rows[1]['changed_loc'])

    def test_missing_usage_not_zero(self):
        with tempfile.TemporaryDirectory() as directory:
            c = Path(directory) / 'one--skill--1'
            c.mkdir()
            (c / 'metadata.json').write_text('{"case":"one", "usage":null}')
            row = a.read_cells(Path(directory))[0]
            self.assertIsNone(row['total_tokens'])
            self.assertIsNone(row['changed_loc'])

    def test_loc_excludes_skills_and_cache(self):
        diff = 'diff --git a/.agents/skills/a/SKILL.md b/.agents/skills/a/SKILL.md\n+ignore\ndiff --git a/app.py b/app.py\n-a\n+b\n'
        self.assertEqual(a.diff_loc(diff), {'production': 2, 'tests': 0})


if __name__ == '__main__':
    unittest.main()
