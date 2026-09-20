from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import hostage_input_candidate as candidate


class InputCandidateConstructionTests(unittest.TestCase):
    def test_one_paragraph_change_preserves_all_other_instructions(self):
        entry = (ROOT / 'skills/hostage-negotiator/SKILL.md').read_text()
        modified = candidate.revise(entry)
        self.assertEqual(modified.replace(candidate.CANDIDATE, candidate.ORIGINAL), entry)
        self.assertEqual(modified.count(candidate.CANDIDATE), 1)

    def test_wrong_duplicate_or_already_changed_input_rejects(self):
        for entry in ('unrelated', candidate.ORIGINAL * 2, candidate.CANDIDATE,
                      candidate.ORIGINAL + candidate.CANDIDATE):
            with self.subTest(entry=entry), self.assertRaises(ValueError):
                candidate.revise(entry)
