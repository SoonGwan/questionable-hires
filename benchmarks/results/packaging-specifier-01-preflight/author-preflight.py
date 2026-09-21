"""Author controls for the committed selection rule; never launches models."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / 'benchmarks/local-runs/packaging-specifier-upstream-24.2'
REV = 'd8e3b31b734926ebbcaff654279f6855a73e052f'
assert subprocess.check_output(['git', '-C', str(UPSTREAM), 'rev-parse', 'HEAD'], text=True).strip() == REV
assert not subprocess.check_output(['git', '-C', str(UPSTREAM), 'status', '--porcelain'])
SPEC = importlib.util.spec_from_file_location('specifier_audit', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)
out = ROOT / 'benchmarks/local-runs/packaging-specifier-preflight-01'
out.mkdir(exist_ok=False)
project = out / 'project'
project.mkdir()
shutil.copytree(UPSTREAM / 'src/packaging', project / 'src/packaging')
(project / 'tests').mkdir()
for name in ('tests/__init__.py', 'tests/test_specifiers.py', 'tests/test_version.py',
             'LICENSE', 'LICENSE.BSD', 'LICENSE.APACHE', 'pyproject.toml'):
    shutil.copy2(UPSTREAM / name, project / name)

source = (project / 'src/packaging/specifiers.py').read_text()
lines = source.splitlines(keepends=True)
cls, = [n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == 'Specifier']
methods = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name.startswith('_compare_')][:3]
assert [n.name for n in methods] == ['_compare_compatible', '_compare_equal', '_compare_not_equal']
faults = []
for method in methods:
    last = max((n for n in ast.walk(method) if isinstance(n, ast.Return)), key=lambda n: (n.lineno, n.col_offset))
    old = ast.get_source_segment(source, last)
    assert source.count(old) == 1
    faulty = source.replace(old, 'return False', 1)
    ast.parse(faulty)
    faults.append(dict(target='src/packaging/specifiers.py', old=old, new='return False'))

inventory = helper.project_inventory(project)
manifest = {p.relative_to(project).as_posix(): dict(sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
             mode=p.stat().st_mode & 0o777) for p in project.rglob('*') if p.is_file()}
env = dict(os.environ, PYTHONPATH=str(project / 'src'), PYTHONDONTWRITEBYTECODE='1')
fresh = subprocess.run([sys.executable, '-B', '-c',
    'import pathlib, packaging, packaging.specifiers; from packaging.specifiers import Specifier; '
    'root=pathlib.Path.cwd(); assert pathlib.Path(packaging.__file__).resolve()==root/"src/packaging/__init__.py"; '
    'assert pathlib.Path(packaging.specifiers.__file__).resolve()==root/"src/packaging/specifiers.py"; '
    'assert Specifier("~=2.2").contains("2.3"); print(packaging.__version__, packaging.specifiers.__file__)'],
    cwd=project, env=env, capture_output=True, text=True, timeout=15)
assert fresh.returncode == 0, fresh.stderr
common = dict(files=['src/packaging', 'tests'], import_roots=['src'],
    imports=['packaging', 'packaging.specifiers', 'tests.test_specifiers'], runner='pytest',
    tests=['tests/test_specifiers.py', '-x', '-q', '--tb=short', '-p', 'no:cacheprovider'],
    guard_project=True,
    precheck='import packaging.specifiers as s, tests.test_specifiers as t\nassert t.Specifier is s.Specifier')
reports = {}
for label, selected in [('single', faults[:1]), ('multiple', faults)]:
    reports[label] = helper.audit_batch(project, dict(common, mutations=selected), timeout=30)
    # Retain reports even if native outcomes differ from the expected detection.
    (out / (label + '.json')).write_text(json.dumps(reports[label], indent=2) + '\n')
    assert helper.project_inventory(project) == inventory
summary = dict(upstream_revision=REV, skill_revision='c8fd471', selection_revision='8b591ff',
    python=sys.version, interpreter=sys.executable, manifest=manifest, mutations=faults,
    recipe_common=common, fresh_import=dict(exit_code=fresh.returncode, stdout=fresh.stdout, stderr=fresh.stderr),
    originals_unchanged=True, limitation='Author native preflight, not model execution, token savings or independent validation.')
(out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
for label, report in reports.items():
    print(label, report['status'])
    for audit in report['audits']:
        for name, check in audit['checks'].items():
            print(name, check['exit_code'], check.get('observation_ref'), check.get('output','')[-400:])
