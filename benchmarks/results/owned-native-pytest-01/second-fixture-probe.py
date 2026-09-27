import hashlib,json,os,subprocess,sys
from pathlib import Path
import pytest
root=Path('/tmp/qh-native-pytest');root.mkdir()
tests="""import subprocess,sys
from answer import answer

def test_answer():
    assert answer() == 42

def test_child():
    p = subprocess.run([sys.executable, '-I', '-B', '-c', 'print(6*7)'], capture_output=True, text=True, timeout=10)
    assert p.returncode == 0
    assert p.stdout == '42\\n'
"""
plugin="""import json,sys
from pathlib import Path
records=[]
def pytest_runtest_logreport(report):
    records.append(dict(nodeid=report.nodeid,when=report.when,outcome=report.outcome))
def pytest_sessionfinish(session,exitstatus):
    Path('observed.json').write_text(json.dumps(dict(records=records,exitstatus=int(exitstatus),executable=sys.executable)))
"""
cells=[]
for name,value in (('before',41),('after',42)):
 directory=root/name;directory.mkdir()
 (directory/'answer.py').write_text('def answer():\n    return '+str(value)+'\n')
 (directory/'test_answer.py').write_text(tests);(directory/'proof.py').write_text(plugin)
 completed=subprocess.run([sys.executable,'-B','-m','pytest','-rA','-p','proof','test_answer.py'],cwd=directory,capture_output=True,text=True,timeout=30)
 observed=json.loads((directory/'observed.json').read_text()) if (directory/'observed.json').is_file() else None
 cells.append(dict(name=name,native_exit=completed.returncode,observed=observed,tests_sha256=hashlib.sha256(tests.encode()).hexdigest(),output=completed.stdout,stderr=completed.stderr))
print('QH_PYTEST_OBSERVATION')
print(json.dumps(dict(checkpoint='owned-native-pytest-01',cells=cells,models=0,external_cases=0,pytest_version=pytest.__version__,pytest_path=pytest.__file__),sort_keys=True))
