"""Copied startup adapter for audit.py's optional -m unittest invocation.

Not a standalone command. The parent injects spec and setup_source in the owned
copy. Observe the real TestProgram result without replacing the native CLI.
"""
import importlib
import json
import os
from pathlib import Path
import site
import sys
import traceback


def install():
    adapter = Path(__file__).resolve().parent
    root = adapter.parent
    paths = [str(root / name) for name in spec['import_roots']] + [str(root)]
    sys.path[:] = paths + [path for path in sys.path if path != str(adapter) and path not in paths]
    # Preserve real interpreter startup hooks and avoid propagating instrumentation
    # into subprocesses created by the tested application.
    os.environ['PYTHONPATH'] = os.pathsep.join(paths)
    identity = sys.modules.pop('sitecustomize')
    try:
        importlib.import_module('sitecustomize')
    except ImportError as error:
        if error.name != 'sitecustomize':
            raise
        sys.modules['sitecustomize'] = identity
    if site.ENABLE_USER_SITE:
        try:
            importlib.import_module('usercustomize')
        except ImportError as error:
            if error.name != 'usercustomize':
                raise
    if sys.argv[:1] != ['-m']:
        return
    import unittest
    original = unittest.TestProgram.runTests

    def observed_run(program):
        namespace = {'spec': spec}
        exec(setup_source, namespace)
        namespace['verify_setup']()
        try:
            return original(program)
        finally:
            result = getattr(program, 'result', None)
            if result is not None:
                observation = dict(tests=result.testsRun, skipped=len(result.skipped),
                                   successful=result.wasSuccessful())
                (adapter / 'result.json').write_text(json.dumps(observation))

    unittest.TestProgram.runTests = observed_run


try:
    install()
except BaseException:
    traceback.print_exc()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(7)
