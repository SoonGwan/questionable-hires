from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from receipt_route_candidate import snapshot, revise, ANCHOR, ROUTING, REFERENCE_SENTENCE
from run import resource_manifest


class ReceiptRouteCandidateTests(unittest.TestCase):
    def test_only_instruction_routing_changes_not_runtime_or_evidence(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
            root = Path(scratch)
            snapshot(root / 'original')
            snapshot(root / 'candidate', candidate=True)
            old = resource_manifest(root / 'original/skills')
            new = resource_manifest(root / 'candidate/skills')
            self.assertEqual(set(old), set(new))
            self.assertEqual(sorted(p for p in old if old[p] != new[p]),
                             ['receipt/SKILL.md', 'receipt/references/existing-fix.md'])
            entry = 'skills/receipt/SKILL.md'
            ref = 'skills/receipt/references/existing-fix.md'
            self.assertEqual((root / 'candidate' / entry).read_text().replace(ROUTING, ''),
                             (root / 'original' / entry).read_text())
            self.assertEqual((root / 'candidate' / ref).read_text(),
                             (root / 'original' / ref).read_text().replace(REFERENCE_SENTENCE, ''))
            with self.assertRaises(FileExistsError):
                snapshot(root / 'candidate', candidate=True)

    def test_unknown_duplicate_or_already_revised_input_rejected(self):
        for entry, ref in [('', REFERENCE_SENTENCE), (ANCHOR * 2, REFERENCE_SENTENCE),
                           (ANCHOR + ROUTING, REFERENCE_SENTENCE), (ANCHOR, '')]:
            with self.subTest(entry=entry, ref=ref), self.assertRaises(ValueError):
                revise(entry, ref)
