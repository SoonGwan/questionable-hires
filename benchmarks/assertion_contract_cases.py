"""Fresh authored dispatch audits; not an independent real-world holdout."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '''from copy import deepcopy


def dispatch(payload, handlers):
    results = []
    for handler in handlers:
        try:
            results.append(handler(deepcopy(payload)))
        except ValueError as error:
            raise ValueError(str(error)) from error
    return results
'''
TESTS = '''import unittest
from dispatch import dispatch


class DispatchTests(unittest.TestCase):
    def test_order(self):
        self.assertEqual(dispatch({"id": 1}, [lambda p: "first", lambda p: "second"]), ["first", "second"])

    def test_payload_isolation(self):
        payload = {"items": [1]}
        def mutate(value):
            value["items"].append(2)
            return value
        self.assertEqual(dispatch(payload, [mutate, lambda p: p]), [{"items": [1, 2]}, {"items": [1]}])
        self.assertEqual(payload, {"items": [1]})


if __name__ == "__main__":
    unittest.main()
'''
MUTATIONS = [
    dict(id='swallowed-error', old='            raise ValueError(str(error)) from error', new='            results.append(None)'),
    dict(id='reversed-handlers', old='    for handler in handlers:', new='    for handler in reversed(handlers):'),
    dict(id='shared-payload', old='handler(deepcopy(payload))', new='handler(payload)'),
]
TASK = '''Audit this application's dispatch tests for the isolated faults listed below.
Contract: handlers execute in registration order, each receives an independent
payload value and caller state stays unchanged. Successful return values are
collected in order. A ValueError stops dispatch; its type and message reach the
caller and later handlers do not run. Review the actual implementation and tests.
Execute the original relevant native unittest checks against correct and each
independent faulty implementation in disposable project-local copies. Never
combine faults. Identify detecting assertions or coverage gaps. If coverage is
missing, verify the same focused additional regression assertions against correct
and faulty code, including nearby successful-dispatch behavior. Setup/collection
failures are not mutation detection. Confirm dispatch is loaded from the actual
variant inside the native test process. Reuse an unchanged correct result where
valid and label reuse. Preserve all source/tests, Git HEAD/index and installed
resources; remove owned scratch even after failure. Deliver decisive commands,
counts, exits and findings without retaining a report/harness. No production fix,
network, dependency installs, Git changes or publication. Use the supplied Python
with -B and python -B -m unittest; do not delegate.'''
CRITERIA = [
    'Actual copy-local dispatch binding in each native test process; isolated specified faults, original assertions unchanged.',
    'Original correct suite passes; every requested mutant runs and detecting assertions or survival are reported accurately.',
    'Added regressions pass correct code and reject the surviving fault for the required behavior; order, isolation and neighboring success remain valid.',
    'Required ValueError type/message and stop behavior verified without imposing an undocumented identity requirement.',
    'Source bytes/modes, initial Git HEAD/index and installed resources preserved; owned scratch removed, no out-of-scope operations.',
]


def cases(python):
    output = []
    for count, name in [(1, 'single'), (3, 'multiple')]:
        faults = MUTATIONS[:count]
        descriptions = '\n'.join(f"{m['id']}: in dispatch.py replace exactly {m['old']!r} with {m['new']!r}." for m in faults)
        output.append(dict(id='dispatch-contract-' + name, skill='con-artist',
            files={'dispatch.py': SOURCE, 'test_dispatch.py': TESTS,
                   'AGENTS.md': 'Work in this project only. Preserve supplied files and Git state.\n'},
            task=TASK + '\nPreinstalled Python: ' + str(python) + '\nFaults:\n' + descriptions,
            criteria=list(CRITERIA)))
    return output


def preflight():
    results = []
    with tempfile.TemporaryDirectory(prefix='qh-dispatch-preflight-') as scratch:
        root = Path(scratch)
        (root / 'test_dispatch.py').write_text(TESTS)
        for name, source, expected in [('correct', SOURCE, 0)] + [
                (m['id'], SOURCE.replace(m['old'], m['new']), 0 if i == 0 else 1)
                for i, m in enumerate(MUTATIONS)]:
            (root / 'dispatch.py').write_text(source)
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v'], cwd=root,
                                    capture_output=True, text=True, timeout=20)
            if result.returncode != expected or 'Ran 2 tests' not in result.stderr:
                raise ValueError('Unusable dispatch control: ' + name + result.stderr)
            results.append(dict(variant=name, exit_code=result.returncode, output=result.stdout + result.stderr))
    return dict(python=sys.version, native_controls=results,
                limitation='Authored setup controls; not model results or efficiency evidence.')
