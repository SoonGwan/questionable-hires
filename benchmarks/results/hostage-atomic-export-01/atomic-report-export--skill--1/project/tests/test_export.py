import tempfile
import unittest
from pathlib import Path
from apps.reports.exporter import write_rows


class ExportTests(unittest.TestCase):
    def test_success_replaces_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.txt"
            path.write_text("previous")
            self.assertEqual(write_rows(path, iter(["Ada", "한글"])), 2)
            self.assertEqual(path.read_bytes(), "Ada\n한글\n".encode("utf-8"))

    def test_empty_export(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.txt"
            self.assertEqual(write_rows(path, iter([])), 0)
            self.assertEqual(path.read_bytes(), b"")

    def test_iterator_failure_preserves_destination_and_cleans_up(self):
        for exists in (False, True):
            for error_type in (RuntimeError, KeyboardInterrupt):
                with self.subTest(exists=exists, error_type=error_type):
                    with tempfile.TemporaryDirectory() as directory:
                        path = Path(directory) / "report.txt"
                        previous = b"previous\x00\xff\r\n"
                        if exists:
                            path.write_bytes(previous)
                        original_entries = set(Path(directory).iterdir())
                        error = error_type("iterator failed")

                        def rows():
                            yield "Ada"
                            yield "한글"
                            raise error

                        with self.assertRaises(error_type) as raised:
                            write_rows(path, rows())

                        self.assertIs(raised.exception, error)
                        if exists:
                            self.assertEqual(path.read_bytes(), previous)
                        else:
                            self.assertFalse(path.exists())
                        self.assertEqual(set(Path(directory).iterdir()), original_entries)
