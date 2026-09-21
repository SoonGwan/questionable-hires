"""Exact eager-equivalence controls for focused patch selection."""
from bisect import bisect_left
import importlib.util
from pathlib import Path
import re
import tracemalloc
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('hunk_stream', ROOT / 'skills/necromancer/scripts/trace.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


def eager(output, historical_path, line_numbers):
    """Unmodified selection implementation at c96730d, independent of Git history."""
    marker = '+++ b/' + historical_path + '\n'
    if output.count(marker) != 1 or any(c in historical_path for c in '\n\r\t"'):
        return output, 0
    header, body = output.split(marker, 1)
    if 'diff --git ' in body or '@@@' in body:
        return output, 0
    parts = re.split(r'(?m)(^@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@[^\n]*\n)', body)
    if len(parts) < 3 or parts[0].strip():
        return output, 0
    kept, omitted = [], 0
    targets = sorted(set(line_numbers))
    for index in range(1, len(parts), 2):
        hunk = parts[index]
        match = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', hunk)
        start, count = int(match[1]), int(match[2] or 1)
        position = bisect_left(targets, start)
        if position < len(targets) and targets[position] < start + count:
            kept.append(hunk + parts[index + 1])
        else:
            omitted += 1
    if not kept:
        return output, 0
    return header + marker + ''.join(kept), omitted


def fixtures():
    prefix = 'commit fixture\n--- a/a.py\n+++ b/a.py\n'
    many = prefix + ''.join(f'@@ -{i},1 +{i},1 @@\n-' + 'x' * 1000 + '\n+' + 'y' * 1000 + '\n'
                            for i in range(1, 2001))
    return {'many-sparse': (many, [1, 2000]),
            'many-all': (many, list(range(1, 2001))),
            'many-miss': (many, [3000]),
            'single-large': (prefix + '@@ -1 +1 @@\n-' + 'x' * 1_000_000 + '\n+y\n', [1]),
            'tiny': (prefix + '@@ -1 +1 @@\n-x\n+y\n', [1])}


class HunkStreamTests(unittest.TestCase):
    def test_exact_output_for_selected_omitted_and_ambiguous_inputs(self):
        prefix = 'commit fixture\n--- a/a.py\n+++ b/a.py\n'
        hunks = '@@ -1,2 +1,2 @@ title\n a\n b\n@@ -8 +8,0 @@\n-gone\n@@ -20 +20 @@\n-old\n+new\n'
        for body in (hunks, '\n \t\n' + hunks, 'unparsed\n' + hunks,
                     hunks + '@@@ ambiguous\n', hunks + 'diff --git other\n',
                     hunks + '@@ malformed tail\n', '', '@@ -1 +1 @@',
                     '@@ -1 +1 @@\r\n-한글\r\n+line\u2028value\r\n'):
            for targets in ([], [1], [2], [8], [20], [1, 20], [20, 1, 20], [999]):
                source = prefix + body
                self.assertEqual(helper.focused_patch(source, 'a.py', targets), eager(source, 'a.py', targets))
        for source, targets in fixtures().values():
            self.assertEqual(helper.focused_patch(source, 'a.py', targets), eager(source, 'a.py', targets))
        for path in ('missing', 'a\nb.py', 'a\rb.py', 'a\tb.py', 'a"b.py'):
            self.assertEqual(helper.focused_patch(prefix + hunks, path, [1]), eager(prefix + hunks, path, [1]))
        self.assertEqual(helper.focused_patch(prefix + hunks + prefix, 'a.py', [1]),
                         eager(prefix + hunks + prefix, 'a.py', [1]))

    def test_sparse_selection_does_not_allocate_unselected_hunk_copies(self):
        source, targets = fixtures()['many-sparse']
        peaks = []
        for function in (eager, helper.focused_patch):
            tracemalloc.start()
            try:
                result = function(source, 'a.py', targets)
                peaks.append(tracemalloc.get_traced_memory()[1])
            finally:
                tracemalloc.stop()
            self.assertEqual(result[1], 1998)
        self.assertLess(peaks[1], peaks[0] // 2)
