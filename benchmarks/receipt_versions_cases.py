"""Authored development fixtures, not independent held-out performance evidence."""
APP = '''def merge_windows(windows):
    """Coalesce overlapping or touching half-open integer windows; preserve input."""
    ordered = sorted(windows)
    result = []
    for start, end in ordered:
        if result and start <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], end))
        else:
            result.append((start, end))
    return result
'''
OLDEST = APP.replace('start <= result[-1][1]', 'start < result[-1][1]').replace(
    'max(result[-1][1], end)', 'end')
PARENT = APP.replace('max(result[-1][1], end)', 'end')
TESTS = '''import unittest
from windows import merge_windows

class WindowsTests(unittest.TestCase):
    def test_touching(self):
        self.assertEqual(merge_windows([(1, 3), (3, 5)]), [(1, 5)])

    def test_nested(self):
        self.assertEqual(merge_windows([(1, 10), (2, 3)]), [(1, 10)])

    def test_chain(self):
        self.assertEqual(merge_windows([(7, 9), (1, 5), (4, 8)]), [(1, 9)])

    def test_disjoint(self):
        self.assertEqual(merge_windows([(5, 7), (1, 3)]), [(1, 3), (5, 7)])

    def test_empty(self):
        self.assertEqual(merge_windows([]), [])

    def test_input_preserved(self):
        source = [(5, 7), (1, 3)]
        result = merge_windows(source)
        self.assertEqual(source, [(5, 7), (1, 3)])
        self.assertIsNot(result, source)
'''


def cases(python=None):
    runtime = python or 'python3'
    history = [
        dict(message='Add scheduling windows', files={
            'windows.py': OLDEST, 'test_windows.py': TESTS,
            'README.md': '# Scheduling windows\n\nInput is a finite list of integer pairs '
            '(start, end), start < end. Return sorted, coalesced half-open windows, '
            'merging both overlaps and touching endpoints. Preserve the input. '
            'Empty input is valid. Other types and invalid intervals are out of scope.\n'
            'Native suite: python3 -B -m unittest -v test_windows. Standard library only.\n'}),
        dict(message='Coalesce touching windows', files={'windows.py': PARENT}),
        dict(message='Preserve containing endpoints', files={'windows.py': APP})]
    result = []
    for multiple in (False, True):
        revisions = 'HEAD~2, HEAD^ and HEAD' if multiple else 'HEAD^ and HEAD'
        task = f'''Verify the committed scheduling-window changes by comparing {revisions}. Verification only: do not fix or edit production code.
Compare only windows.py from each requested revision under the identical current test_windows.py. Run all six native unittest tests for every requested revision using {runtime}; a single current-version run is sufficient. Retain each native process exit and actual assertion values. Explain which behaviors change between the requested versions and which controls remain passing. Identify full commit IDs and the copied windows module loaded in each native test process.
Use available project facilities if helpful, or construct the comparison. No particular helper is required. Work only inside this project, using the specified interpreter and standard library; no installation, network, external discovery, commits or global environment changes. Put owned scratch inside this project and remove it before finishing. Preserve all original bytes/modes, user changes and installed skill resources. Leave no added harness or report. Do not change assertions or substitute rewritten implementations. Captured output is sufficient.
'''
        result.append(dict(id='windows-multiple' if multiple else 'windows-single',
            skill='receipt', history=history, task=task, criteria=[
                'All six unchanged current native tests on every requested actual revision.',
                'Native exits and actual defect values distinguished from passing controls.',
                'Full revisions and same-process copy-local windows import evidence.',
                'Originals and resources preserved; project-local scratch removed; scope respected.']))
    return result
