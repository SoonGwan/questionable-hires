
import importlib.util
import json
from pathlib import Path
import sys
import unittest
root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location('native_install_tests', root / 'tests/test_install.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
expected = root / 'scripts/install.py'
assert Path(module.installer.__file__).resolve() == expected
assert Path(module.installer.install.__code__.co_filename).resolve() == expected
assert module.installer.ROOT == root
print('PROVENANCE ' + json.dumps({'tests': module.__file__, 'installer': module.installer.__file__,
      'install_code': module.installer.install.__code__.co_filename, 'ROOT': str(module.installer.ROOT)}), flush=True)
class Result(unittest.TextTestResult):
    def startTest(self, test):
        self.lines = set()
        self.calls = 0
        def trace(frame, event, arg):
            if frame.f_code is module.installer.install.__code__:
                if event == 'call': self.calls += 1
                if event == 'line': self.lines.add(frame.f_lineno)
            return trace
        sys.settrace(trace)
        super().startTest(test)
    def addFailure(self, test, err):
        print('FAILURE_STATE ' + json.dumps({'test': test._testMethodName,
            'entries': sorted(p.name for p in test.dest.iterdir()),
            'marker': (test.dest / 'user.txt').read_text() if (test.dest / 'user.txt').exists() else None,
            'skill_files': {name: sorted(str(p.relative_to(test.dest / name)) for p in (test.dest / name).rglob('*') if p.is_file()) for name in ['necromancer','receipt']}}), flush=True)
        super().addFailure(test, err)
    def stopTest(self, test):
        sys.settrace(None)
        print('EXECUTED ' + json.dumps({'test': test._testMethodName, 'install_calls': self.calls, 'install_lines': sorted(self.lines)}), flush=True)
        assert self.calls > 0
        super().stopTest(test)
suite = unittest.TestSuite(module.InstallTests(name) for name in sys.argv[2:])
result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite)
print('COUNTS ' + json.dumps({'run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped)}), flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
