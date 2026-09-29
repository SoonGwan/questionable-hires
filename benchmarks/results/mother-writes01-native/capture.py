import hashlib,importlib.util,io,json,sys,unittest
from pathlib import Path
root=Path(sys.argv[1]).resolve(); out=Path(sys.argv[2]); out.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('native_writes_checks',root/'tests/test_mother_writes_candidate.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
stream=io.StringIO()
result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(m))
log=stream.getvalue(); (out/'unittest.stderr').write_text(log)
for index,row in enumerate(m.OBSERVATIONS):
    if 'raw_stderr' in row:
        (out/(str(index)+'.stderr')).write_text(row.pop('raw_stderr'))
summary=dict(python=sys.version,tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),skips=len(result.skipped),observations=m.OBSERVATIONS,unittest_stderr_sha256=hashlib.sha256(log.encode()).hexdigest())
(out/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(log,end='')
raise SystemExit(0 if result.wasSuccessful() else 1)
