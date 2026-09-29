"""Copied import hashing preserves evidence without whole-source allocation."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit_import_hash', ROOT / 'skills/con-artist/scripts/audit.py')
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)

CHILD = '''import contextlib, io, json, sys, tracemalloc
request = json.loads(sys.stdin.read())
output = io.StringIO()
namespace = {'spec': {'imports': ['sample'], 'import_roots': []}}
with contextlib.redirect_stdout(output):
    exec(request['setup'], namespace)
import sample
output.seek(0)
output.truncate()
tracemalloc.start()
try:
    with contextlib.redirect_stdout(output):
        namespace['verify_setup']()
    peak = tracemalloc.get_traced_memory()[1]
finally:
    tracemalloc.stop()
print(json.dumps({'peak': peak, 'output': output.getvalue(), 'value': sample.value}))
'''


class AuditImportHashTests(unittest.TestCase):
    def test_native_setup_hashes_complete_source_with_bounded_intermediate_allocation(self):
        with tempfile.TemporaryDirectory(prefix='audit-import-hash-', dir=ROOT / 'benchmarks') as folder:
            root = Path(folder)
            for length in (0, 65536, 4_000_000):
                with self.subTest(source_padding=length):
                    content = b'value = 41\n#' + b'x' * length + '한글\n'.encode()
                    (root / 'sample.py').write_bytes(content)
                    process = subprocess.run([sys.executable, '-B', '-c', CHILD], cwd=root,
                        input=json.dumps({'setup': audit.SETUP}), capture_output=True,
                        text=True, timeout=10)
                    self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                    observed = json.loads(process.stdout)
                    self.assertEqual(observed['value'], 41)
                    prefix = 'Verified copied import: sample '
                    self.assertTrue(observed['output'].startswith(prefix), observed['output'])
                    self.assertEqual(json.loads(observed['output'][len(prefix):]), {
                        'path': 'sample.py', 'sha256': hashlib.sha256(content).hexdigest()})
                    self.assertLess(observed['peak'], 300_000)
