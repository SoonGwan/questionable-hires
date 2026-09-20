from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
from receipt_read_candidate import snapshot, revise, BEFORE, AFTER, RESOURCE
from run import resource_manifest
from receipt_snapshot_support import controlled_snapshots
from runner_snapshot_support import require_history


class ReceiptReadCandidateTests(unittest.TestCase):
    def test_only_known_input_guidance_changes_and_runtime_stays_identical(self):
        with controlled_snapshots():
            self.check_snapshots()

    def test_real_pinned_read_candidate(self):
        require_history(self, ROOT, [RESOURCE])
        self.check_snapshots()

    def check_snapshots(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch:
            root=Path(scratch)
            snapshot(root/'original')
            snapshot(root/'candidate',candidate=True)
            old=resource_manifest(root/'original/skills')
            new=resource_manifest(root/'candidate/skills')
            self.assertEqual(set(old),set(new))
            self.assertEqual([p for p in old if old[p]!=new[p]],['receipt/SKILL.md'])
            entry='skills/receipt/SKILL.md'
            self.assertEqual((root/'candidate'/entry).read_text().replace(AFTER,BEFORE),
                             (root/'original'/entry).read_text())
            with self.assertRaises(FileExistsError): snapshot(root/'candidate',candidate=True)

    def test_unknown_or_already_revised_input_is_not_silently_changed(self):
        for body in ('unrecognized',BEFORE+'\n'+BEFORE,AFTER):
            with self.subTest(body=body),self.assertRaises(ValueError): revise(body)
