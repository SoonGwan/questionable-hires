import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'benchmarks'))
from analyze_response_costs import analyze, compare, summarize


def profile(inputs):
    rows = [dict(input_tokens=i, cached_input_tokens=i//2, output_tokens=2) for i in inputs]
    totals = {k: sum(r[k] for r in rows) for k in rows[0]}
    return dict(recorded_responses=rows, totals=totals,
                total_tokens=totals['input_tokens']+totals['output_tokens'])


class ResponseCostsTests(unittest.TestCase):
    def test_exact_symmetric_identity_including_shrinking_context(self):
        b, c = profile([100, 120]), profile([110, 80, 140])
        result = compare(b, c)
        self.assertEqual(result['arithmetic_terms'], dict(response_count_term=105,
            first_input_term=25, later_input_term=-20, output_term=2))
        self.assertEqual(result['delta_total_tokens'], 112)
        reverse = compare(c, b)
        self.assertEqual(reverse['arithmetic_terms'],
                         {k:-v for k,v in result['arithmetic_terms'].items()})

    def test_incomplete_and_inconsistent_records_rejected(self):
        original = profile([100, 120])
        bad = []
        for field, value in (('recorded_responses', None), ('total_tokens', 1)):
            modified = copy.deepcopy(original)
            modified[field] = value
            bad.append(modified)
        modified = copy.deepcopy(original)
        modified['recorded_responses'][0]['cached_input_tokens'] = 101
        bad.append(modified)
        modified = copy.deepcopy(original)
        modified['totals']['input_tokens'] += 1
        bad.append(modified)
        for modified in bad:
            with self.subTest(modified=modified), self.assertRaises(ValueError):
                summarize(modified)

    def test_all_sixteen_frozen_profiles_reconcile(self):
        root = Path(__file__).resolve().parents[1]
        result = analyze(root/'benchmarks/results/all-eight-current-03')
        self.assertEqual(len(result['rows']), 8)
        self.assertEqual(sum(r['delta_total_tokens'] for r in result['rows']), 114945)
        self.assertEqual(sum(r['arithmetic_terms']['output_term'] for r in result['rows']), -507)

    def test_all_eventemitter_conditions_are_retained(self):
        root = Path(__file__).resolve().parents[1]
        result = analyze(root/'benchmarks/results/eventemitter-boundary-01', all_conditions=True)
        self.assertEqual(len(result['rows']), 4)
        deltas = {condition: sum(r['delta_total_tokens'] for r in result['rows']
                               if r['condition'] == condition) for condition in ('prior', 'candidate')}
        self.assertEqual(deltas, {'prior': 41971, 'candidate': 66491})
        for row in result['rows']:
            self.assertEqual(set(row['profile_sha256']), {'baseline', row['condition']})

    def test_missing_arm_duplicate_and_unsafe_names_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            rows = []
            for case in ('one', 'two'):
                for condition in ('baseline', 'prior', 'candidate'):
                    arm = 'baseline' if condition == 'baseline' else 'skill'
                    dest = root/condition/(case+'--'+arm+'--1')
                    dest.mkdir(parents=True)
                    data = profile([100, 120])
                    (dest/'usage-profile.json').write_text(json.dumps(data))
                    rows.append(dict(case=case, condition=condition, total_tokens=data['total_tokens']))
            manifest = root/'comparison.json'
            (root/'run.json').write_text(json.dumps(dict(completed_cells=rows)))
            for changed in (rows[:-1], rows + [rows[0]],
                            [row for row in rows if row['condition'] != 'candidate'],
                            [dict(rows[0], condition='../escape')],
                            [dict(rows[0], case='../escape')], []):
                manifest.write_text(json.dumps(dict(rows=changed)))
                with self.subTest(rows=changed), self.assertRaises(ValueError):
                    analyze(root, all_conditions=True)
            for changed in ([dict(rows[0], case='../escape')],
                            [dict(rows[0], condition='../escape')]):
                manifest.write_text(json.dumps(dict(rows=changed)))
                (root/'run.json').write_text(json.dumps(dict(completed_cells=changed)))
                with self.assertRaisesRegex(ValueError, 'Unexpected or duplicate'):
                    analyze(root, all_conditions=True)
