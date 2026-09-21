import itertools
from pathlib import Path
import tempfile
import tracemalloc
import unittest
from unittest.mock import patch

from test_history_helper import helper


class CurrentLineSelectionTests(unittest.TestCase):
    def check_source(self, source):
        expected = helper.git_lines(source)
        selections = ([1], [len(expected)], sorted({1, max(1, len(expected) // 2), len(expected)})) if expected else ([1],)
        for numbers in selections:
            if not expected:
                with self.assertRaisesRegex(ValueError, 'exceeds current file'):
                    helper.selected_current_lines(source, numbers)
            else:
                self.assertEqual(helper.selected_current_lines(source, numbers),
                                 [dict(line=n, text=expected[n - 1]) for n in numbers])
        with self.assertRaisesRegex(ValueError, 'exceeds current file'):
            helper.selected_current_lines(source, [len(expected) + 1])

    def test_lf_semantics_and_endings(self):
        for length in range(5):
            for parts in itertools.product(('x', '\n', '\r', '\u2028', '한'), repeat=length):
                self.check_source(''.join(parts))

    def test_chunk_boundaries_long_rows_and_distant_selections(self):
        for length in (65535, 65536, 65537, 140000):
            for ending in ('', '\n', '\n\n'):
                self.check_source('x' * length + '\r\n\n' + '한\u2028\r\n' * 20000 + ending)
        self.check_source('\n' * 1_900_000)

    def test_selected_rows_do_not_allocate_full_file_line_list(self):
        source = 'short row\n' * 190000
        numbers = [1, 95000, 190000]
        def measure(function):
            tracemalloc.start()
            try:
                result = function()
                return result, tracemalloc.get_traced_memory()[1]
            finally:
                tracemalloc.stop()
        def eager():
            lines = helper.git_lines(source)
            return [dict(line=n, text=lines[n - 1]) for n in numbers]
        old, old_peak = measure(eager)
        new, new_peak = measure(lambda: helper.selected_current_lines(source, numbers))
        self.assertEqual(old, new)
        self.assertLess(new_peak, old_peak // 2)

    def test_all_selected_rows_and_unselected_invalid_encoding(self):
        source = 'row\r\n' * 100000
        numbers = list(range(1, 100001, 1000))
        self.assertEqual(helper.selected_current_lines(source, numbers),
                         [dict(line=n, text='row\r') for n in numbers])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'source.py').write_bytes(b'valid\n' + b'\n' * 70000 + b'\xff')
            with patch.object(helper, 'git') as git:
                with self.assertRaises(UnicodeDecodeError):
                    helper.trace(root, 'source.py', 1, 1)
                git.assert_not_called()


if __name__ == '__main__':
    unittest.main()
