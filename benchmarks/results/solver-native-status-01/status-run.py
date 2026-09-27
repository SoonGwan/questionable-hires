import sys, pathlib, os, json, io, contextlib
root=pathlib.Path(sys.argv[1]).resolve()
if root.name in {"pytest-dev__pytest-5221","pytest-dev__pytest-5103","pytest-dev__pytest-6116"}: sys.path.insert(0,"/runtime-compat")
source=root/'src' if (root/'src').is_dir() else root
sys.path.insert(0,str(source));os.chdir(root)
import pytest
assert pathlib.Path(pytest.__file__).resolve().is_relative_to(root)
class Capture:
    def __init__(self):
        self.reports = []

    def pytest_configure(self, config):
        self.config = config

    def pytest_report_teststatus(self, report, config):
        assert config is self.config
        return None

    def pytest_runtest_logreport(self, report):
        category, letter, label = self.config.hook.pytest_report_teststatus(report=report, config=self.config)
        self.reports.append(dict(nodeid=report.nodeid, when=report.when,
                                 outcome=report.outcome, category=category,
                                 wasxfail=hasattr(report, 'wasxfail')))

cap=Capture(); stream=io.StringIO(); control=pathlib.Path('/solver/status-controls')
with contextlib.redirect_stdout(stream),contextlib.redirect_stderr(stream):
    result=int(pytest.main(['--assert=plain','-q','--tb=line','-p','no:cacheprovider','-c',str(control/'empty.ini'),'--confcutdir='+str(control),'--basetemp',str(control/(root.name+'-tmp')),str(control/'test_states.py')],plugins=[cap]))
(control/(root.name+'.log')).write_text(stream.getvalue())
calls={r['nodeid'].split('::')[-1]:r for r in cap.reports if r['when']=='call'}
expected={'test_pass':'passed','test_fail':'failed','test_skip':'skipped','test_xfail':'xfailed','test_xpass':'xpassed'}
assert {name:calls[name]['category'] for name in expected}==expected
assert any(r['nodeid'].endswith('test_setup_error') and r['when']=='setup' and r['category']=='error' for r in cap.reports)
assert any(r['nodeid'].endswith('test_teardown_error') and r['when']=='teardown' and r['category']=='error' for r in cap.reports)
assert result==1,result
print(json.dumps(dict(result='PASS',issue=root.name,pytest_version=pytest.__version__,pytest_path=pytest.__file__,native_exit=result,expected_categories=expected,xpass_native_outcome=calls['test_xpass']['outcome'],setup_error=True,teardown_error=True,log_bytes=len(stream.getvalue().encode()),models=0,selected_issue_tests=0)))
