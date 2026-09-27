import json,os,sys
from pathlib import Path
import pytest
records=[]
def pytest_runtest_logreport(report):
 records.append(dict(nodeid=report.nodeid,when=report.when,outcome=report.outcome))
def pytest_collection_finish(session):
 module=sys.modules.get('requests')
 assert module is not None and module.__file__.startswith('/testbed/'),'Native pytest imports outside variant source'
def pytest_sessionfinish(session,exitstatus):
 module=sys.modules.get('requests')
 Path('/var/tmp/'+os.environ['QH_VARIANT']+'-observer.json').write_text(json.dumps(dict(records=records,exitstatus=int(exitstatus),collected=len(session.items),executable=sys.executable,pytest_version=pytest.__version__,project_path=module.__file__ if module else None)))
