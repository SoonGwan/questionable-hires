import pathlib,json,sys,threading,pytest
import control_package as package
assert pathlib.Path(package.__file__).resolve().is_relative_to(pathlib.Path.cwd())
assert pathlib.Path(pytest.__file__).resolve()==pathlib.Path(sys.argv[2]).resolve()
print('PUBLIC_ENTRY',package.__version__,package.__file__,flush=True)
class Capture:
    def __init__(self): self.items=[]; self.reports=[]
    def pytest_collection_finish(self, session): self.items=[i.nodeid for i in session.items]
    def pytest_configure(self, config): self.config=config
    def pytest_runtest_logreport(self, report):
        category, letter, label=self.config.hook.pytest_report_teststatus(report=report)
        self.reports.append(dict(nodeid=report.nodeid,when=report.when,outcome=report.outcome,wasxfail=hasattr(report,'wasxfail'),native_category=category))
cap=Capture()
result=pytest.main(sys.argv[3:],plugins=[cap])
threads=[t for t in threading.enumerate() if t.__class__.__module__=='pytest_httpbin.serve']
for t in threads: threading.Thread.join(t,2)
assert not any(t.is_alive() for t in threads)
pathlib.Path(sys.argv[1]).write_text(json.dumps(dict(items=cap.items,reports=cap.reports,native_complete=True,native_exit=int(result)),ensure_ascii=False,indent=2))
print('NATIVE_COMPLETE',flush=True)
sys.exit(result)
