"""Project comparison: identical current tests against two allocation revisions.

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
