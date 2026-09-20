"""Transformation integrity, not behavioral proof of shorter instructions."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import exorcist_disclosure_candidate as candidate


class ExorcistDisclosureCandidateTests(unittest.TestCase):
    def test_frozen_transform_round_trips_without_touching_other_sections(self):
        source = (ROOT / 'skills/exorcist/SKILL.md').read_text()
        revised = candidate.revise(source)
        self.assertEqual(revised.replace(candidate.CANDIDATE, candidate.ORIGINAL), source)
        self.assertLess(len(revised.encode()), len(source.encode()))
        self.assertEqual(source.split('---', 2)[:2], revised.split('---', 2)[:2])

    def test_unfrozen_or_already_transformed_sources_reject(self):
        source = (ROOT / 'skills/exorcist/SKILL.md').read_text()
        for changed in ('', source + '\n', candidate.revise(source), source.replace('Exorcist', 'Changed')):
            with self.subTest(length=len(changed)), self.assertRaises(ValueError):
                candidate.revise(changed)
