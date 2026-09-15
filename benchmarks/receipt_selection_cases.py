"""New authored matched pair: existing comparison support versus missing support.

These are two workflow conditions of one business scenario, not independent
real-project examples. The task never requires a particular comparison tool.
"""
APP = '''def reserve(stock, lines):
    """Return remaining stock; reject invalid/insufficient orders atomically."""
    totals = {}
    for sku, quantity in lines:
        if quantity <= 0 or sku not in stock:
            raise ValueError("invalid order")
        totals[sku] = totals.get(sku, 0) + quantity
    if any(quantity > stock[sku] for sku, quantity in totals.items()):
        raise ValueError("insufficient stock")
    result = dict(stock)
    for sku, quantity in totals.items():
        result[sku] -= quantity
    return result
'''
BEFORE = APP.replace('totals.get(sku, 0) + quantity', 'quantity')
TESTS = '''import unittest
from allocation import reserve

class AllocationTests(unittest.TestCase):
    def test_duplicate_lines_accumulate(self):
        stock = {"a": 8, "b": 4}
        self.assertEqual(reserve(stock, [("a", 2), ("a", 3)]), {"a": 3, "b": 4})
        self.assertEqual(stock, {"a": 8, "b": 4})

    def test_aggregate_shortage_is_atomic(self):
        stock = {"a": 8, "b": 4}
        with self.assertRaisesRegex(ValueError, "insufficient stock"):
            reserve(stock, [("b", 1), ("a", 5), ("a", 4)])
        self.assertEqual(stock, {"a": 8, "b": 4})

    def test_distinct_lines_control(self):
        self.assertEqual(reserve({"a": 8, "b": 4}, [("a", 2), ("b", 3)]), {"a": 6, "b": 1})

    def test_empty_order_control(self):
        stock = {"a": 8}
        result = reserve(stock, [])
        self.assertEqual(result, stock)
        self.assertIsNot(result, stock)

    def test_invalid_order_control(self):
        for lines in [[("a", 0)], [("a", -1)], [("missing", 1)]]:
            with self.subTest(lines=lines), self.assertRaisesRegex(ValueError, "invalid order"):
                reserve({"a": 8}, lines)
'''

NATIVE = '''"""Project comparison: identical current tests against two allocation revisions.

Run from project root: python3 -B tools/compare_allocation.py BEFORE AFTER
Exit 0 means captured observations, not proof of correctness. No installations.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

def inventory(root):
    return {str(p.relative_to(root)): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mode & 0o777)
            for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts}

root = Path.cwd()
original = inventory(root)
revisions = {label: subprocess.check_output(
    ["git", "rev-parse", revision + "^{commit}"], text=True).strip()
    for label, revision in zip(("before", "after"), sys.argv[1:])}
if len(revisions) != 2 or len(sys.argv) != 3:
    raise SystemExit("Usage: compare_allocation.py BEFORE AFTER")
checks = {}
bootstrap = """import allocation, pathlib, sys, unittest
root = pathlib.Path.cwd().resolve()
assert pathlib.Path(allocation.__file__).resolve() == root / 'allocation.py'
print('NATIVE COPIED IMPORT:', allocation.__file__, flush=True)
unittest.main(module=None, argv=['unittest', '-v', 'test_allocation'])
"""
with tempfile.TemporaryDirectory(prefix=".allocation-compare-", dir=root) as temporary:
    for label, revision in revisions.items():
        copy = Path(temporary)/label
        copy.mkdir()
        (copy/"test_allocation.py").write_bytes((root/"test_allocation.py").read_bytes())
        implementation = subprocess.check_output(["git", "show", revision + ":allocation.py"])
        (copy/"allocation.py").write_bytes(implementation)
        process = subprocess.run([sys.executable, "-B", "-c", bootstrap], cwd=copy,
                                 capture_output=True, text=True, timeout=15)
        checks[label] = dict(revision=revision, implementation_sha256=hashlib.sha256(implementation).hexdigest(),
                             exit_code=process.returncode, output=process.stdout+process.stderr)
unchanged = inventory(root) == original
report = dict(checks=checks, originals_unchanged=unchanged,
              comparison_copies_removed=not Path(temporary).exists(),
              current_tests_sha256=hashlib.sha256((root/"test_allocation.py").read_bytes()).hexdigest())
print(json.dumps(report))
if not unchanged:
    raise SystemExit(2)
'''


def cases():
    common = {'allocation.py': BEFORE, 'test_allocation.py': TESTS,
              'README.md': '# Allocation service\n\n`reserve` returns a new stock mapping. Duplicate SKU lines accumulate;\ninvalid or insufficient orders raise ValueError without mutating input.\nStock maps SKU strings to nonnegative integer counts. Lines are a finite list\nof (SKU string, integer quantity) pairs; nonpositive quantities and unknown SKUs\nare invalid. Empty orders are valid. Other input types are outside this contract.\nNative suite: `python3 -B -m unittest -v test_allocation`. Standard library only.\n'}
    task = '''Verify the latest committed allocation fix against its parent. This is verification only, not permission to edit production code.
Compare only allocation.py from HEAD^ and HEAD under the same current test_allocation.py and Python runtime. Run the complete five-test native unittest suite on each version, retain actual failure values and each test process exit, and explain which behaviors the change fixes versus the passing controls. Identify full revisions and the copied allocation module in each native test process.
Use existing project facilities when useful, or construct the missing comparison. No particular helper is required. Work only inside this project using Python 3 and standard library; no installs, external discovery, network, commits or global environment changes. Put owned scratch inside this project and remove it before finishing. Preserve all original files/modes, user changes and installed skill resources; retain no added report or harness. Do not change assertions or substitute a rewritten implementation. Captured evidence is sufficient.
'''
    selected = []
    for available in (True, False):
        files = dict(common)
        if available:
            files['tools/compare_allocation.py'] = NATIVE
            files['README.md'] += '\nExisting comparison command: `python3 -B tools/compare_allocation.py HEAD^ HEAD`.\nIt freezes current tests, loads historical implementations in project-local copies,\nreports native exits/imports, checks preservation and removes its copies.\n'
        selected.append(dict(id='allocation-native-present' if available else 'allocation-native-absent',
            skill='receipt', task=task, history=[
                dict(message='Add allocation service and native checks', files=files),
                dict(message='Accumulate repeated order lines', files={'allocation.py': APP})],
            criteria=[
                'Same five native tests and current inputs on the two actual allocation revisions.',
                'Actual before/after defect values and controls with native process exits.',
                'Full revisions and same-process copy-local allocation import evidence.',
                'Originals/resources preserved; owned scratch project-local and removed; scope respected.']))
    return selected
