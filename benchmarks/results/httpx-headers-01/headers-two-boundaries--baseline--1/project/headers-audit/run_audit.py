from pathlib import Path
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'headers-audit'
PYTHON = '<ENV>/venv/bin/python'
assert Path(sys.executable).resolve() == Path(PYTHON).resolve()
originals = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in ROOT.rglob('*') if p.is_file() and OUT not in p.parents and '.git' not in p.parts}
source = (ROOT / 'httpx/_models.py').read_text()
faults = {
    'correct': source,
    'getitem_case_sensitive': source.replace('normalized_key = key.lower().encode(self.encoding)', 'normalized_key = key.encode(self.encoding)', 1),
    'get_list_reverse_unsplit': source.replace('if not split_commas:\n            return values', 'if not split_commas:\n            return values[::-1]', 1),
}
assert source.count('normalized_key = key.lower().encode(self.encoding)') == 1
assert source.count('if not split_commas:\n            return values') == 1
results = {}
for name, mutated in faults.items():
    dest = OUT / name
    dest.mkdir()
    for directory in ('httpx', 'tests'):
        shutil.copytree(ROOT / directory, dest / directory, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    shutil.copy2(ROOT / 'pyproject.toml', dest / 'pyproject.toml')
    (dest / 'httpx/_models.py').write_text(mutated)
    (OUT / f'{name}.patch').write_text(''.join(difflib.unified_diff(source.splitlines(True), mutated.splitlines(True), fromfile='correct/httpx/_models.py', tofile=f'{name}/httpx/_models.py')))
    (dest / 'test_audit_control.py').write_text('''import pathlib
import httpx


def test_lowercase_single_value_control():
    assert pathlib.Path(httpx.__file__).resolve().parent == pathlib.Path(__file__).resolve().parent / "httpx"
    h = httpx.Headers({"x-control": "plain"})
    assert h["x-control"] == "plain"
    assert h.get_list("x-control") == ["plain"]
''')
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['PYTHONPATH'] = str(dest)
    results[name] = {}
    commands = {
        'provenance': [PYTHON, '-B', '-c', 'import httpx, sys; print(sys.executable); print(httpx.__file__)'],
        'existing': [PYTHON, '-B', '-m', 'pytest', '-p', 'no:cacheprovider', '-q', 'tests/models/test_headers.py'],
        'control': [PYTHON, '-B', '-m', 'pytest', '-p', 'no:cacheprovider', '-q', 'test_audit_control.py'],
    }
    for label, command in commands.items():
        proc = subprocess.run(command, cwd=dest, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (OUT / f'{name}-{label}.log').write_text(proc.stdout)
        results[name][label] = {'command': command, 'cwd': str(dest), 'exit_code': proc.returncode}
        print(f'{name} {label}: exit {proc.returncode}\n{proc.stdout}', flush=True)
changed = [p for p, digest in originals.items() if not (ROOT / p).is_file() or hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != digest]
assert not changed, changed
results['original_files_verified_unchanged'] = len(originals)
(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
(OUT / 'original-sha256.json').write_text(json.dumps(originals, indent=2) + '\n')
print(f'Verified {len(originals)} original files unchanged.')
