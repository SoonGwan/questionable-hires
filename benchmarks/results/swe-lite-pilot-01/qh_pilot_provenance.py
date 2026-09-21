import json
import os
from pathlib import Path


def pytest_collection_modifyitems(items):
    project = os.environ['QH_PROJECT']
    expected = Path('/testbed/test_requests.py' if project == 'requests'
                    else '/testbed/testing/test_skipping.py')
    # Pytest's own tests create nested child suites. They are not the outer
    # required file; absence of the outer marker is rejected by the collector.
    modules = [getattr(item, 'module', None) for item in items]
    if not any(Path(getattr(module,'__file__','/missing')).resolve() == expected for module in modules):
        return
    package = __import__(project)
    assert package.__file__.startswith('/testbed/')
    for module in modules:
        assert Path(module.__file__).resolve() == expected
        assert getattr(module,project) is package
    print('QH_NATIVE_BINDINGS ' + json.dumps(dict(source=package.__file__,count=len(items))),flush=True)
