import tempfile
import unittest
from pathlib import Path
from apps.reports.exporter import write_rows


class ExportTests(unittest.TestCase):
    def test_iterator_failure_preserves_destination(self):
        for exists in (True, False):
            with self.subTest(destination_exists=exists):
                with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
                    path = Path(directory) / "report.txt"
                    previous = b"previous\r\n\xff"
                    if exists:
                        path.write_bytes(previous)
                    original_entries = set(Path(directory).iterdir())
                    failure = RuntimeError("row iterator failed")

                    def failing_rows():
                        yield "Ada"
                        yield "한글"
                        raise failure

                    with self.assertRaises(RuntimeError) as caught:
                        write_rows(path, failing_rows())

                    self.assertIs(caught.exception, failure)
                    self.assertEqual(set(Path(directory).iterdir()), original_entries)
                    if exists:
                        self.assertEqual(path.read_bytes(), previous)
                    else:
                        self.assertFalse(path.exists())

    def test_success_replaces_file(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            path = Path(directory) / "report.txt"
            path.write_text("previous")
            self.assertEqual(write_rows(path, iter(["Ada", "한글"])), 2)
            self.assertEqual(path.read_bytes(), "Ada\n한글\n".encode("utf-8"))

    def test_empty_export(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]) as directory:
            path = Path(directory) / "report.txt"
            self.assertEqual(write_rows(path, iter([])), 0)
            self.assertEqual(path.read_bytes(), b"")
