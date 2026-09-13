from pathlib import Path
import difflib
import hashlib
import os
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
audit = root / 'cookie-clear-audit'
interpreter = '<ENV>/venv/bin/python'
originals = [p for p in root.rglob('*') if p.is_file() and audit not in p.parents and '.git' not in p.parts]
before = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in originals}
(audit / 'original_hashes.json').write_text(__import__('json').dumps(before, indent=2))
for label in ('correct', 'faulty'):
    target = audit / label
    target.mkdir()
    for folder in ('httpx', 'tests'):
        shutil.copytree(root / folder, target / folder, ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy2(root / 'pyproject.toml', target / 'pyproject.toml')
source = audit / 'faulty/httpx/_models.py'
old = source.read_text()
needle = '            args.append(path)\n        self.jar.clear(*args)'
assert old.count(needle) == 1
new = old.replace(needle, '            # Mutation: discard the path, clearing the entire requested domain.\n        self.jar.clear(*args)')
source.write_text(new)
(audit / 'mutation.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True), new.splitlines(True), fromfile='correct/httpx/_models.py', tofile='faulty/httpx/_models.py')))
control = '''from pathlib import Path
import httpx
assert Path(httpx.__file__).resolve() == Path.cwd() / "httpx/__init__.py"
cookies = httpx.Cookies()
for domain, path, value in [
    ("example.com", "/subpath/1", "target-one"),
    ("example.com", "/subpath/2", "target-two"),
    ("example.org", "/subpath/1", "other-domain"),
]:
    cookies.set("name", value, domain=domain, path=path)
cookies.clear(domain="example.com")
remaining = {(c.domain, c.path, c.name, c.value) for c in cookies.jar}
assert remaining == {("example.org", "/subpath/1", "name", "other-domain")}, remaining
print("Imported:", httpx.__file__)
print("Domain-only control PASS:", remaining)
'''
(audit / 'domain_control.py').write_text(control)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
env.pop('PYTHONPATH', None)
results = {}
for label in ('correct', 'faulty'):
    target = audit / label
    commands = {
        'suite': [interpreter, '-B', '-m', 'pytest', '-p', 'no:cacheprovider', '-v', 'tests/models/test_cookies.py'],
        'domain_existing': [interpreter, '-B', '-m', 'pytest', '-p', 'no:cacheprovider', '-v', 'tests/models/test_cookies.py::test_cookies_with_domain'],
        'domain_control': [interpreter, '-B', '-c', control],
    }
    for name, command in commands.items():
        proc = subprocess.run(command, cwd=target, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (audit / f'{label}_{name}.log').write_text(proc.stdout)
        results[f'{label}_{name}'] = proc.returncode
        print(f'{label} {name}: exit {proc.returncode}\n{proc.stdout}', flush=True)
assert results == {'correct_suite': 0, 'correct_domain_existing': 0, 'correct_domain_control': 0, 'faulty_suite': 1, 'faulty_domain_existing': 0, 'faulty_domain_control': 0}, results
assert all(hashlib.sha256((root / name).read_bytes()).hexdigest() == digest for name, digest in before.items())
(audit / 'integrity.txt').write_text(f'All {len(before)} original files retain their SHA-256 hashes.\n')
print('Original file integrity verified.')
