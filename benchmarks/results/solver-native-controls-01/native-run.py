import pathlib,sys,importlib,json,os
root=pathlib.Path(sys.argv[1]).resolve();mode=sys.argv[2]
if root.name in {"pytest-dev__pytest-5221","pytest-dev__pytest-5103","pytest-dev__pytest-6116"}: sys.path.insert(0,"/runtime-compat")
source=root/'src' if (root/'src').is_dir() else root
sys.path.insert(0,str(source));os.chdir(root)
module=importlib.import_module('requests' if root.name.startswith('psf') else 'pytest')
assert pathlib.Path(module.__file__).resolve().is_relative_to(root)
import pytest
if root.name.startswith('psf'): assert pathlib.Path(pytest.__file__).resolve().is_relative_to(pathlib.Path('/runtime/env'))
else: assert pathlib.Path(pytest.__file__).resolve().is_relative_to(root)
class Capture:
    def __init__(self): self.calls=[]
    def pytest_runtest_logreport(self,report):
        if report.when=='call': self.calls.append(dict(nodeid=report.nodeid,outcome=report.outcome,text=str(report.longrepr)))
cap=Capture()
result=int(pytest.main(['--assert=plain','-p','no:cacheprovider','-c','/native-controls/empty.ini','--confcutdir=/native-controls','--tb=short','/native-controls/test_control.py::test_'+mode],plugins=[cap]))
valid=(result==(0 if mode=='pass' else 1) and len(cap.calls)==1 and cap.calls[0]['outcome']==('passed' if mode=='pass' else 'failed') and (mode=='pass' or 'observed != expected' in cap.calls[0]['text']))
print(json.dumps(dict(issue=root.name,mode=mode,native_exit=result,calls=cap.calls,valid_control=valid,pytest_version=pytest.__version__,pytest_path=pytest.__file__),sort_keys=True))
sys.exit(0 if valid else 1)
