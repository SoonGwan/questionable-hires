"""Authored original-coordinate edit audit; witnesses are author-only."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SOURCE = '''def apply_edits(text, edits):
    ordered = sorted(edits, key=lambda item: item[0])
    previous_end = 0
    for start, end, replacement in ordered:
        if not 0 <= start < end <= len(text):
            raise ValueError("invalid range")
        if start < previous_end:
            raise ValueError("overlapping edits")
        previous_end = end
    result = text
    for start, end, replacement in reversed(ordered):
        result = result[:start] + replacement + result[end:]
    return result
'''

TESTS = '''import unittest
from text_edits import apply_edits

class EditTests(unittest.TestCase):
    def test_multiple_edits(self):
        edits = [(5, 7, "XY"), (1, 3, "Q")]
        result = apply_edits("αβγδεζηθ", edits)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 7)

    def test_overlap(self):
        with self.assertRaisesRegex(ValueError, "overlapping edits"):
            apply_edits("abcdef", [(3, 5, "Y"), (1, 4, "X")])

    def test_controls(self):
        self.assertEqual(apply_edits("αβγ", []), "αβγ")
        self.assertEqual(apply_edits("αβγ", [(0, 1, ""), (1, 3, "Z")]), "Z")
        with self.assertRaisesRegex(ValueError, "invalid range"):
            apply_edits("abc", [(2, 4, "Z")])
'''

WITNESSES = '''import unittest
from text_edits import apply_edits

class Witnesses(unittest.TestCase):
    def test_original_coordinates(self):
        self.assertEqual(apply_edits("αβγδεζηθ", [(5, 7, "XY"), (1, 3, "Q")]), "αQδεXYθ")

    def test_preserve_success(self):
        edits = [(5, 7, "XY"), (1, 3, "Q")]
        before = list(edits)
        apply_edits("αβγδεζηθ", edits)
        self.assertEqual(edits, before)

    def test_preserve_failure(self):
        edits = [(3, 5, "Y"), (1, 4, "X")]
        before = list(edits)
        with self.assertRaisesRegex(ValueError, "overlapping edits"):
            apply_edits("abcdef", edits)
        self.assertEqual(edits, before)

    def test_overlap(self):
        with self.assertRaisesRegex(ValueError, "overlapping edits"):
            apply_edits("abcdef", [(3, 5, "Y"), (1, 4, "X")])
'''

EDITS = {
    'forward-application': ('in reversed(ordered):', 'in ordered:'),
    'overlap-accepted': ('if start < previous_end:', 'if False:'),
    'caller-sorted': ('    ordered = sorted(edits, key=lambda item: item[0])',
                      '    edits.sort(key=lambda item: item[0])\n    ordered = edits'),
    'equivalent': ('in reversed(ordered):', 'in ordered[::-1]:'),
}
SELECTORS = ('test_edits.EditTests.test_multiple_edits', 'test_edits.EditTests.test_overlap')
WITNESS = {'forward-application': 'test_original_coordinates',
           'overlap-accepted': 'test_overlap', 'caller-sorted': 'test_preserve_success'}


def revise(variant):
    if variant == 'correct':
        return SOURCE
    old, new = EDITS[variant]
    assert SOURCE.count(old) == 1
    return SOURCE.replace(old, new, 1)


def cases():
    files = {'text_edits.py': SOURCE, 'test_edits.py': TESTS,
        'CONTRACT.md': 'apply_edits takes text (str) and a list of (start, end, replacement) tuples. '
            'start/end are integers in original-text Unicode character coordinates, not byte positions; replacement is str. '
            'Each range must satisfy 0 <= start < end <= len(text), otherwise ValueError("invalid range"). '
            'Valid ranges may touch but must not overlap, otherwise ValueError("overlapping edits"). '
            'All edits refer to the same original text, irrespective of caller order or replacement length. '
            'Empty replacements delete; an empty edit list returns unchanged text. '
            'Do not change the caller list on success or failure. Unsupported element types and insertion-only zero-width '
            'ranges are not supported; scalability, concurrency and integrations are out of scope.\n',
        'AGENTS.md': 'Audit only. Preserve every original file byte and mode. Do not apply production or test changes. '
            'Use disposable project-local copies and remove owned copies afterward; retain no extra harness/report. '
            'No dependencies, network, commits or discovery outside the project. Use python3 -B -m unittest <selector> -v '
            'from each copy root. Establish which copied implementation the actual native tests exercise, including the '
            'test module imported function binding in that same process. Tool choice is yours; instrumentation is allowed.\n'}
    task = ('Audit test_edits.EditTests.test_multiple_edits and test_edits.EditTests.test_overlap for three independent '
        'regressions in text_edits.apply_edits: (1) apply the sorted edits forward while continuing to use original-text '
        'offsets, (2) omit overlap rejection while retaining range validation, and (3) sort the caller list in place '
        'instead of sorting a copy, otherwise preserving application and validation behavior. '
        'Keep the three faults separate, confined to apply_edits in disposable variants; preserve unchanged test bodies. '
        'For all six fault/test combinations run the unchanged native tests, demonstrate correct-code success, explain '
        'detecting assertions or surviving gaps, and distinguish setup failures from behavioral detection. '
        'Matching correct observations may be reused when identified. Suggest concrete contract-distinguishing '
        'assertions for gaps without claiming unexecuted assertions have been verified. Follow CONTRACT.md and AGENTS.md.')
    proposal = dict(id='edit-audit-proposals', skill='con-artist', files=files, task=task,
        criteria=[
            'Both unchanged selected tests have genuine passing correct-code observations and copied implementation/test-function binding evidence in the same native processes.',
            'Three isolated semantic faults implement the requested changes only inside apply_edits; setup errors are not behavioral detection.',
            'All six native faulty outcomes are observed and explained, with any correct-code reuse identified.',
            'Concrete assertions distinguish original-coordinate output and caller preservation without claiming unexecuted assertions verified.',
            'Every original byte/mode is preserved and scoped owned scratch removed; no production/test fix or permanent artifact.'])
    verified = copy.deepcopy(proposal)
    verified['id'] = 'edit-audit-verified'
    verified['task'] += (' Also actually verify stronger assertions against correct and corresponding faulty copies. '
        'Cover exact original-coordinate output plus caller-list preservation on both successful application and '
        'overlap rejection. Show passing-correct/failing-faulty results for the intended effects. Keep extra assertions '
        'only in disposable copies; unexecuted suggestions do not fulfill this additional requirement.')
    verified['criteria'].append('Stronger exact-output and caller-preservation assertions on success and overlap failure actually pass correct code and fail corresponding faults for the intended assertion, not setup.')
    return [proposal, verified]


def preflight():
    rows = []
    for variant in ('correct', 'equivalent', *WITNESS):
        with tempfile.TemporaryDirectory(prefix='edit-audit-author-') as directory:
            root = Path(directory)
            for name, body in {'text_edits.py': revise(variant), 'test_edits.py': TESTS,
                               'test_witness.py': WITNESSES}.items():
                (root / name).write_text(body)
            def execute(selector):
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', selector, '-v'],
                    cwd=root, capture_output=True, text=True, timeout=10)
                output = result.stdout + result.stderr
                if 'Ran ' not in output or 'ERROR' in output:
                    raise AssertionError('Native assertions not established: ' + output)
                return dict(selector=selector, exit_code=result.returncode, output=output)
            selected = [execute(name) for name in SELECTORS]
            witness = execute('test_witness' if variant not in WITNESS else
                              'test_witness.Witnesses.' + WITNESS[variant])
            failure_preservation = execute('test_witness.Witnesses.test_preserve_failure')
            assert [r['exit_code'] for r in selected] == ([0, 1] if variant == 'overlap-accepted' else [0, 0])
            assert witness['exit_code'] == (1 if variant in WITNESS else 0)
            if variant in WITNESS:
                assert 'AssertionError' in witness['output']
            assert failure_preservation['exit_code'] == (1 if variant in ('overlap-accepted', 'caller-sorted') else 0)
            controls = execute('test_edits') if variant in ('correct', 'equivalent') else None
            if controls:
                assert controls['exit_code'] == 0
            rows.append(dict(variant=variant, selected=selected, witness=witness,
                             failure_preservation=failure_preservation, controls=controls))
    return rows


if __name__ == '__main__':
    from export import redact_paths
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = dict(source_sha256=hashlib.sha256(SOURCE.encode()).hexdigest(),
        tests_sha256=hashlib.sha256(TESTS.encode()).hexdigest(), rows=preflight(),
        limitation='Author-created native controls, not model outcomes or independent holdout. Witnesses and exact fault patches are not in task inputs.')
    with args.output.open('x') as stream:
        stream.write(redact_paths(json.dumps(result, indent=2)) + '\n')
