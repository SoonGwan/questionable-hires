import itertools
import tracemalloc
import unittest
from unittest.mock import patch

from test_history_helper import helper


class HistoryPatchStreamTests(unittest.TestCase):
    def test_physical_rows_match_existing_contract(self):
        for size in range(5):
            for parts in itertools.product(('x', '\n', '\r', '\u2028', '한'), repeat=size):
                text = ''.join(parts)
                self.assertEqual(list(helper.iter_git_lines(text)), helper.git_lines(text))

    def test_offset_rows_keep_lf_cr_and_unicode_content(self):
        for length in (0, 65535, 65536, 65537, 140000):
            tail = 'x' * length + '\r\n한\u2028\r\n\n'
            text = 'prefix\n한 prefix\n' + tail
            start = len(text) - len(tail)
            self.assertEqual(list(helper.iter_git_lines(text, start)), helper.git_lines(tail))
            self.assertEqual(list(helper.iter_git_lines(text, len(text))), [])

    def test_excerpt_and_invalid_tail_match_eager_path(self):
        text = '+++ b/a.py\n@@ -0,0 +1,20000 @@\n' + ''.join('+row %d\n' % i for i in range(20000))
        for source in (text, text.rstrip('\n'), text + '+unexpected\n'):
            for targets in ([1], [9999, 10000], [1, 20000]):
                expected = helper.selected_patch_excerpt(source, 'a.py', targets)
                with patch.object(helper, 'iter_git_lines', lambda text, start=0: helper.git_lines(text[start:])):
                    self.assertEqual(helper.selected_patch_excerpt(source, 'a.py', targets), expected)
        self.assertIsNone(helper.selected_patch_excerpt(text + '+unexpected\n', 'a.py', [1]))

    def test_chunk_boundaries_long_rows_and_empty_rows(self):
        for length in (65535, 65536, 65537, 140000):
            for ending in ('', '\n', '\n\n'):
                source = 'x' * length + '\r\n\n' + '한\u2028\r\n' * 20000 + ending
                self.assertEqual(list(helper.iter_git_lines(source)), helper.git_lines(source))

    def test_selected_excerpt_does_not_copy_the_whole_patch_body(self):
        text = '+++ b/a.py\n@@ -1,40000 +1,40000 @@\n' + ''.join(
            '-old row %d padding padding\n+new row %d padding padding\n' % (i, i)
            for i in range(40000))
        tracemalloc.start()
        try:
            excerpt = helper.selected_patch_excerpt(text, 'a.py', [20000])
            peak = tracemalloc.get_traced_memory()[1]
        finally:
            tracemalloc.stop()
        self.assertIsNotNone(excerpt)
        self.assertIn('new:20000 +new row 19999 padding padding', excerpt)
        self.assertLess(peak, 600000)

    def test_large_patch_reduces_intermediate_peak_without_changing_evidence(self):
        text = '+++ b/a.py\n@@ -0,0 +1,40000 @@\n' + ''.join('+row %d\n' % i for i in range(40000))
        def measure(eager):
            with patch.object(helper, 'iter_git_lines', (lambda text, start=0: helper.git_lines(text[start:])) if eager else helper.iter_git_lines):
                tracemalloc.start()
                try:
                    result = helper.selected_patch_excerpt(text, 'a.py', [1, 20000, 40000])
                    return result, tracemalloc.get_traced_memory()[1]
                finally:
                    tracemalloc.stop()
        eager, eager_peak = measure(True)
        streamed, streamed_peak = measure(False)
        self.assertIsNotNone(streamed)
        self.assertEqual(streamed, eager)
        self.assertLess(streamed_peak, eager_peak // 2)


if __name__ == '__main__':
    unittest.main()
