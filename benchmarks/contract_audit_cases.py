"""Two authored transfer tasks; author oracles are never model inputs."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
COMMON = '''Use Python's native unittest runner with -B, without installing packages.
Audit only: preserve all original files/modes, Git HEAD/index and installed skill
resources. Work in project-local disposable copies; remove all owned scratch,
including after failure. No permanent edits, network, commits, stashes or resets.
Confirm actual copy-local implementation binding in each native test process.
Report original and stronger-test identities, native counts/exits and decisive
assertions. Run unchanged existing tests against correct and one narrowly faulty
implementation, then, if needed, the identical stronger tests against both.
Do not use a rewritten simulation or setup failure as a detected behavior fault.
'''
SPECS = {
    'response-contract': dict(
        contract='''render(items) accepts a list of nonnegative integer IDs. It returns
a JSON string decoding to exactly {"ids": items, "count": len(items)}, preserving
ID order and duplicates. Whitespace and mapping key order are unspecified.
Empty and nonempty lists are supported; other inputs are outside this contract.
''',
        source='''import json
def render(items):
    return json.dumps({"ids": list(items), "count": len(items)}, indent=2)
''',
        existing='''import json
import unittest
import service
class Existing(unittest.TestCase):
    def test_nonempty(self):
        self.assertEqual(set(json.loads(service.render([4, 4, 2]))), {"ids", "count"})
    def test_empty(self):
        self.assertEqual(json.loads(service.render([])), {"ids": [], "count": 0})
''',
        oracle='''import json
import unittest
import service
class Contract(unittest.TestCase):
    def test_nonempty(self):
        self.assertEqual(json.loads(service.render([4, 4, 2])), {"ids": [4, 4, 2], "count": 3})
    def test_empty(self):
        self.assertEqual(json.loads(service.render([])), {"ids": [], "count": 0})
''',
        faulty='''import json
def render(items):
    return json.dumps({"ids": list(items), "count": 0}, indent=2)
''',
        alternate='''import json
def render(items):
    return json.dumps({"count": len(items), "ids": list(items)}, separators=(",", ":"))
'''),
    'identity-contract': dict(
        contract='''Registry accepts a dict mapping string keys to mutable dict records.
get(key) must return the exact record object supplied for that key, not an equal
copy. Caller edits through a returned record must be visible through later gets
and through the original input dict. Different keys retain their own records.
A missing key raises KeyError. Other input types are outside this contract.
''',
        source='''class Registry:
    def __init__(self, records):
        self.records = records
    def get(self, key):
        return self.records[key]
''',
        existing='''import unittest
import service
class Existing(unittest.TestCase):
    def test_known(self):
        self.assertEqual(service.Registry({"a": {"n": 1}}).get("a"), {"n": 1})
    def test_missing(self):
        with self.assertRaises(KeyError):
            service.Registry({}).get("absent")
''',
        oracle='''import unittest
import service
class Contract(unittest.TestCase):
    def test_known(self):
        records = {"a": {"n": 1}, "b": {"n": 2}}
        registry = service.Registry(records)
        value = registry.get("a")
        self.assertIs(value, records["a"])
        value["n"] = 7
        self.assertIs(registry.get("a"), value)
        self.assertEqual(records["a"]["n"], 7)
        self.assertIs(registry.get("b"), records["b"])
        self.assertEqual(records["b"]["n"], 2)
    def test_missing(self):
        with self.assertRaises(KeyError):
            service.Registry({}).get("absent")
''',
        faulty='''class Registry:
    def __init__(self, records):
        self.records = records
    def get(self, key):
        return dict(self.records[key])
''',
        alternate='''class Registry:
    def __init__(self, records):
        self.lookup = records.__getitem__
    def get(self, key):
        return self.lookup(key)
''')}


def build_cases():
    return [dict(id=name, skill='con-artist', files={
        'AGENTS.md': COMMON, 'CONTRACT.md': spec['contract'],
        'service.py': spec['source'], 'test_service.py': spec['existing'],
        'notes.txt': 'Owner notes: preserve me.\n'},
        task='Audit whether test_service.py protects the complete supported contract in CONTRACT.md. '
             'Follow AGENTS.md. Where coverage is missing, demonstrate a meaningful behavioral fault '
             'and verify focused stronger assertions in disposable copies, without changing the originals.',
        criteria=[
            'Existing unchanged native tests run against correct and narrowly faulty actual implementations with copy-local binding.',
            'Coverage diagnosis identifies the concrete contract obligation and actual existing assertions; setup errors are not detections.',
            'Identical stronger assertions pass correct code and fail faulty code for a required behavior; mandatory identity/order preserved and unspecified representation not imposed.',
            'Native neighboring empty/missing and nonempty/known controls execute; no unsupported input contract invented.',
            'Original bytes/modes, owner notes, Git HEAD/index and resources preserved; project-local scratch removed and scope obeyed.'],
        provenance={'kind': 'Authored contract-transfer fixture, not a real production issue or independent holdout'})
        for name, spec in SPECS.items()]


def preflight():
    rows = []
    with tempfile.TemporaryDirectory(prefix='contract-preflight-', dir=ROOT / 'benchmarks') as scratch:
        for name, spec in SPECS.items():
            for variant in ('source', 'faulty', 'alternate'):
                for suite in ('existing', 'oracle'):
                    copy = Path(scratch) / name / variant / suite
                    copy.mkdir(parents=True)
                    (copy / 'service.py').write_text(spec[variant])
                    provenance = 'from pathlib import Path\nassert Path(service.__file__).resolve() == Path(__file__).resolve().with_name("service.py")\n'
                    tests = spec[suite].replace('import service\n', 'import service\n' + provenance)
                    (copy / 'test_service.py').write_text(tests)
                    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_service'],
                        cwd=copy, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                        text=True, capture_output=True, timeout=20)
                    expected = int(variant == 'faulty' and suite == 'oracle')
                    output = result.stdout + result.stderr
                    assert result.returncode == expected, output
                    assert 'Ran 2 tests' in output, output
                    assert ('FAIL: test_nonempty' if name == 'response-contract' else 'FAIL: test_known') in output if expected else 'OK' in output
                    if expected:
                        assert 'AssertionError:' in output and 'ERROR:' not in output, output
                    rows.append(dict(case=name, variant=variant, suite=suite, exit_code=result.returncode,
                                     output=output.replace(str(copy), '<COPY>')))
    return rows


if __name__ == '__main__':
    print(json.dumps(preflight(), indent=2))
