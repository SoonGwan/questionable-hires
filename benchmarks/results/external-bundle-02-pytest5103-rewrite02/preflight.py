import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

source = Path('/testbed')
out = Path('/tmp/qh-rewrite5103')
out.mkdir()
expected = json.loads(Path('/qh/source-manifest.json').read_text())
assert all(hashlib.sha256((source / n).read_bytes()).hexdigest() == v['sha256']
           for n, v in expected.items())
for wheel in json.loads(Path('/qh/wheels02.json').read_text())['wheels']:
    assert hashlib.sha256((Path('/qh/wheelhouse02') / wheel['filename']).read_bytes()).hexdigest() == wheel['sha256']
env = dict(os.environ, PIP_NO_INDEX='1', PIP_FIND_LINKS='/qh/wheelhouse02')
for label, command in [('gold-check', ['git', 'apply', '--check', '/qh/gold.patch']),
                       ('gold-apply', ['git', 'apply', '/qh/gold.patch']),
                       ('install', [sys.executable, '-m', 'pip', 'install', '-e', '.'])]:
    p = subprocess.run(command, cwd=source, env=env, capture_output=True, timeout=90)
    (out / (label + '.stdout')).write_bytes(p.stdout)
    (out / (label + '.stderr')).write_bytes(p.stderr)
    assert p.returncode == 0, label
    if label == 'install':
        assert b'Successfully installed pytest-' in p.stdout and b'ERROR:' not in p.stdout + p.stderr
    if label == 'gold-apply':
        patched = {n: hashlib.sha256((source / n).read_bytes()).hexdigest() for n in expected}
assert all(hashlib.sha256((source / n).read_bytes()).hexdigest() == h for n, h in patched.items())

header = 'def is_even(value):\n    return value % 2 == 0\n\ndef test_authored():\n'
cases = {'scalar': header + '    assert is_even(11)\n',
         'generator': header + '    assert all(is_even(value) for value in [11, 13])\n',
         'list': header + '    assert all([is_even(value) for value in [11, 13]])\n'}
direct = '''import ast,json,sys,warnings
warnings.simplefilter("error", SyntaxWarning)
from pathlib import Path
import pytest
from _pytest.assertion import rewrite
record=dict(pytest_path=pytest.__file__,pytest_version=pytest.__version__,rewrite_path=rewrite.__file__,special_all=hasattr(rewrite.AssertionRewriter,'_visit_all'))
try:
 tree=ast.parse(Path(sys.argv[1]).read_text());rewrite.rewrite_asserts(tree)
 code=compile(tree,str(sys.argv[1]),'exec');ns={};exec(code,ns);ns['test_authored']()
 record.update(stage='executed',outcome='unexpected-pass')
except BaseException as error:
 record.update(outcome=type(error).__name__,message=str(error))
print(json.dumps(record))
'''
plugin = '''import json,sys
from pathlib import Path
def pytest_collection_modifyitems(config,items):
 from _pytest.assertion import rewrite
 record=dict(assertmode=config.getoption('assertmode'),special_all=hasattr(rewrite.AssertionRewriter,'_visit_all'),rewrite_path=rewrite.__file__,hooks=[type(h).__name__ for h in sys.meta_path],collected=len(items),rewritten=[any(n.startswith('@pytest') for n in i.obj.__code__.co_names) for i in items])
 Path('native-observation.json').write_text(json.dumps(record))
'''
results = []
for label, body in cases.items():
    folder = out / label
    folder.mkdir()
    fixture = folder / 'test_authored.py'
    fixture.write_text(body)
    (folder / 'diagnostic_plugin.py').write_text(plugin)
    for mode in ('direct', 'native'):
        command = ([sys.executable, '-B', '-c', direct, str(fixture)] if mode == 'direct' else
                   [sys.executable, '-B', '-m', 'pytest', '-s', '-q', '--tb=short', '-p', 'no:cacheprovider', '-W', 'error::SyntaxWarning', str(fixture)])
        child_env = dict(env, PYTHONPATH=str(folder), PYTEST_PLUGINS='diagnostic_plugin')
        p = subprocess.run(command, cwd=folder, env=child_env, capture_output=True, timeout=15)
        (folder / (mode + '.stdout')).write_bytes(p.stdout)
        (folder / (mode + '.stderr')).write_bytes(p.stderr)
        row = dict(case=label, mode=mode, exit_code=p.returncode,
                   stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),
                   stderr_sha256=hashlib.sha256(p.stderr).hexdigest())
        if mode == 'direct' and p.returncode == 0:
            row['observation'] = json.loads(p.stdout)
        if mode == 'native' and (folder / 'native-observation.json').is_file():
            row['observation'] = json.loads((folder / 'native-observation.json').read_text())
        results.append(row)
        (out / 'observations.json').write_text(json.dumps(results, indent=2) + '\n')
        print(json.dumps(row), flush=True)
print(json.dumps(dict(result='DIAGNOSTIC-COMPLETE',cells=len(results))))
