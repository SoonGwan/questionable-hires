import json
from pathlib import Path


def pytest_collection_modifyitems(items):
    import requests
    assert Path(requests.__file__).resolve() == Path('/testbed/requests/__init__.py')
    assert items
    for item in items:
        assert Path(item.module.__file__).resolve() == Path('/testbed/test_requests.py')
        assert item.module.requests is requests
    print('QH_NATIVE_BINDINGS ' + json.dumps({'source': requests.__file__, 'count': len(items)}), flush=True)
