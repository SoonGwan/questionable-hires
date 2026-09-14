import json
import tempfile
import unittest
from pathlib import Path
from store.service import submit


class SubmissionTests(unittest.TestCase):
    def test_acknowledges_submission(self):
        with tempfile.TemporaryDirectory(prefix="audit-store-", dir=Path.cwd()) as folder:
            result = submit(folder, "ticket", {"title": "첫 요청", "count": 2})
            self.assertEqual(result, {"accepted": True, "key": "ticket"})
            self.assertEqual(
                json.loads((Path(folder) / "ticket.json").read_text(encoding="utf-8")),
                {"title": "첫 요청", "count": 2},
            )

    def test_acknowledges_replacement(self):
        with tempfile.TemporaryDirectory(prefix="audit-store-", dir=Path.cwd()) as folder:
            submit(folder, "ticket", {"title": "first", "count": 1})
            result = submit(folder, "ticket", {"title": "수정 요청", "count": 3})
            self.assertEqual(result, {"accepted": True, "key": "ticket"})
            self.assertEqual(
                json.loads((Path(folder) / "ticket.json").read_text(encoding="utf-8")),
                {"title": "수정 요청", "count": 3},
            )
