import json
from pathlib import Path
import subprocess

import certifi
import requests

assert Path(requests.__file__).resolve() == Path('/testbed/requests/__init__.py')
def send(host):
    with requests.Session() as session:
        return session.send(requests.Request('GET', 'https://' + host + '/get').prepare(), timeout=5)

bundle = Path(certifi.where())
assert not str(bundle).startswith('/testbed/')
assert requests.adapters.DEFAULT_CA_BUNDLE_PATH == str(bundle)
try:
    send('httpbin.org')
except requests.exceptions.SSLError:
    print('UNTRUSTED_CA_REJECTED', flush=True)
else:
    raise AssertionError('Untrusted certificate accepted')
with bundle.open('ab') as out:
    out.write(b'\n' + Path('/fixture/ca.pem').read_bytes())
response = send('httpbin.org')
assert response.status_code == 200 and response.json()['url'] == 'https://httpbin.org/get'
print('TRUSTED_HTTPS_ACCEPTED', flush=True)
try:
    send('wrong.httpbin.test')
except requests.exceptions.SSLError as error:
    message = str(error).lower()
    assert 'match' in message or 'hostname' in message, message
    print('WRONG_HOST_REJECTED', flush=True)
else:
    raise AssertionError('Wrong hostname accepted')
subprocess.run(['git', 'diff', '--exit-code', '--quiet'], check=True)
print(json.dumps({'requests_source': requests.__file__, 'runtime_ca_bundle': str(bundle),
                  'project_tracked_diff': 'empty'}), flush=True)

import pytest

class NativeBindings:
    def pytest_collection_modifyitems(self, items):
        assert len(items) == 142
        for item in items:
            assert Path(item.module.__file__).resolve() == Path('/testbed/test_requests.py')
            assert item.module.requests is requests
        print(json.dumps({'same_process_native_bindings': True, 'collected': len(items)}), flush=True)

code = pytest.main(['-p', 'no:cacheprovider', '-q', '--tb=short', 'test_requests.py'], plugins=[NativeBindings()])
subprocess.run(['git', 'diff', '--exit-code', '--quiet'], check=True)
raise SystemExit(code)
