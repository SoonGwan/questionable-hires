import json,os,pathlib,sys
import pytest
_session=None
_records=[]
def pytest_sessionstart(session):
 global _session
 if _session is None and 'QH_OBSERVER_PARENT_PID' not in os.environ:
  _session=session;os.environ['QH_OBSERVER_PARENT_PID']=str(os.getpid())
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item,call):
 result=yield
 if item.session is _session and os.environ.get('QH_OBSERVER_PARENT_PID')==str(os.getpid()):
  report=result.get_result();_records.append(dict(nodeid=report.nodeid,when=report.when,outcome=report.outcome,wasxfail=getattr(report,'wasxfail',None)))
def pytest_sessionfinish(session,exitstatus):
 if session is _session:
  pathlib.Path(os.environ.get('QH_OBSERVER_OUTPUT','/tmp/qh-pair-output/observer.json')).write_text(json.dumps(dict(exitstatus=int(exitstatus),collected=session.testscollected,executable=sys.executable,pytest_version=pytest.__version__,pytest_path=pytest.__file__,records=_records),indent=2)+'\n')
