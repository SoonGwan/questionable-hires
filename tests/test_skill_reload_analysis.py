import copy
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from analyze_skill_reloads import analyze, summarize


class SkillReloadAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.meta = dict(skill='demo', arm='skill', case='case', skill_sha256='abc')
        self.audit = dict(first_tool_line=4, skills={'demo': dict(entry_sha256='abc', observations=[
            dict(line=2, phase='initial_message'), dict(line=5, phase='tool_output')])})

    def test_initial_and_tool_only_are_distinct(self):
        self.assertTrue(summarize(self.meta, self.audit)['tool_reexposure_after_initial'])
        self.audit['skills']['demo']['observations'].pop(0)
        result = summarize(self.meta, self.audit)
        self.assertFalse(result['tool_reexposure_after_initial'])
        self.assertEqual(result['tool_body_output_lines'], [5])
        self.audit['skills']['demo']['observations'] = []
        self.assertFalse(summarize(self.meta, self.audit)['initially_exposed'])

    def test_wrong_revision_or_phase_order_rejected(self):
        for change in ('hash', 'order', 'phase', 'line'):
            audit = copy.deepcopy(self.audit)
            entry = audit['skills']['demo']
            if change == 'hash': entry['entry_sha256'] = 'wrong'
            elif change == 'order': entry['observations'].reverse()
            elif change == 'phase': entry['observations'][1]['phase'] = 'initial_message'
            else: entry['observations'][0]['line'] = True
            with self.subTest(change=change), self.assertRaises(ValueError):
                summarize(self.meta, audit)

    def test_all_original_screen_cells(self):
        result = analyze(ROOT / 'benchmarks/results/all-eight-current-03')
        self.assertEqual(len(result['rows']), 16)
        skill = [r for r in result['rows'] if r['arm'] == 'skill']
        baseline = [r for r in result['rows'] if r['arm'] == 'baseline']
        self.assertEqual(sum(r['initially_exposed'] for r in skill), 8)
        self.assertEqual(sum(r['tool_reexposure_after_initial'] for r in skill), 7)
        self.assertFalse(any(r['initially_exposed'] for r in baseline))
