import json,sys
from pathlib import Path
import pytest,requests
counts=dict(passed=0,failed=0,skipped=0,test_calls=0)
def pytest_collectreport(report):counts[report.outcome]+=1
def pytest_runtest_logreport(report):
 if report.when=='call':counts['test_calls']+=1
def pytest_sessionfinish(session,exitstatus):
 Path('/tmp/qh-collection-report.json').write_text(json.dumps(dict(counts=counts,collected=len(session.items),exitstatus=int(exitstatus),executable=sys.executable,pytest_version=pytest.__version__,pytest_path=pytest.__file__,project_path=requests.__file__)))
