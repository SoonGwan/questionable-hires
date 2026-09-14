#!/usr/bin/env python3
"""Author-only preflight for a full-history HTTPX redirect review."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

REVISION = '26d48e0634e6ee9cdc0533996db289ce4b430177'

PROBE = r'''
import ast, inspect, json, textwrap, unittest
from unittest.mock import patch
import httpx
import httpx._client as module

def candidate(name):
    tree = ast.parse('from __future__ import annotations\n' + textwrap.dedent(inspect.getsource(getattr(module.BaseClient, name))))
    function = tree.body[1]
    if name == '_redirect_headers':
        targets = [node for node in function.body if isinstance(node, ast.If)
                   and any(isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                           and call.func.attr == 'pop' and call.args
                           and isinstance(call.args[0], ast.Constant)
                           and call.args[0].value == 'Content-Length' for call in ast.walk(node))]
    else:
        targets = [node for node in function.body if isinstance(node, ast.If)]
    assert len(targets) == 1
    function.body.remove(targets[0])
    namespace = dict(module.__dict__)
    exec(compile(ast.fix_missing_locations(tree), '<independent proposal>', 'exec'), namespace)
    return namespace[name]

def observe(status, chunked):
    requests = []
    def handler(request):
        requests.append(dict(method=request.method, body=request.read().decode(),
                             length=request.headers.get('content-length'),
                             transfer=request.headers.get('transfer-encoding')))
        return httpx.Response(status, headers={'Location': '/done'}) if len(requests) == 1 else httpx.Response(200)
    with httpx.Client(transport=httpx.MockTransport(handler), follow_redirects=True) as client:
        response = client.post('https://example.invalid/start', content=iter([b'pay', b'load']) if chunked else b'payload')
    assert response.status_code == 200 and len(requests) == 2
    return requests[1]

inputs = [(302, False), (302, True), (307, False)]
observed = {'current': [observe(*args) for args in inputs]}
for label, name in [('headers-only', '_redirect_headers'), ('stream-only', '_redirect_stream')]:
    with patch.object(module.BaseClient, name, candidate(name)):
        observed[label] = [observe(*args) for args in inputs]
empty = dict(method='GET', body='', length=None, transfer=None)
normal = dict(method='POST', body='payload', length='7', transfer=None)
assert observed['current'] == [empty, empty, normal], observed
assert observed['headers-only'] == [{**empty, 'length': '7'}, {**empty, 'transfer': 'chunked'}, normal], observed
assert observed['stream-only'] == [{**empty, 'body': 'payload'}, {**empty, 'body': 'payload'}, normal], observed
failures = {}
for label in ('headers-only', 'stream-only'):
    try:
        unittest.TestCase().assertEqual(observed[label][0], empty)
    except AssertionError as error:
        failures[label] = str(error)
    else:
        raise AssertionError('Expected actual behavioral disagreement: ' + label)
print(json.dumps(dict(observations=observed, deliberate_assertion_failures=failures), indent=2))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists')
    source = args.source.resolve()
    def git(*parts):
        return subprocess.check_output(['git', *parts], cwd=source, text=True).strip()
    assert git('rev-parse', 'HEAD') == REVISION
    assert git('rev-parse', '--is-shallow-repository') == 'false'
    assert git('status', '--porcelain') == ''
    names = git('ls-files').splitlines()
    before = {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in names}
    native = subprocess.run([str(args.python), '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                             'tests/client/test_redirects.py::test_body_redirect',
                             'tests/client/test_redirects.py::test_no_body_redirect'],
                            cwd=source, capture_output=True, text=True, check=True, timeout=30)
    result = subprocess.run([str(args.python), '-B', '-c', PROBE], cwd=source,
                            capture_output=True, text=True, check=True, timeout=30)
    earlier = git('show', '00e150f^:httpx/middleware/redirect.py')
    assert 'headers.pop("Content-Length", None)' in earlier
    assert 'headers.pop("Transfer-Encoding", None)' in earlier
    assert 'return b""' in earlier
    assert before == {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in names}
    assert git('status', '--porcelain') == ''
    assert not list(source.rglob('__pycache__'))
    report = dict(revision=REVISION, reachable_commits=int(git('rev-list', '--count', 'HEAD')),
                  shallow=False, tracked_files=len(names), source_unchanged=True,
                  native_output=native.stdout, native_stderr=native.stderr,
                  earlier_middleware_revision=git('rev-parse', '00e150f^'),
                  earlier_middleware_sha256=hashlib.sha256(earlier.encode()).hexdigest(),
                  **json.loads(result.stdout),
                  limitation='Author-only local MockTransport checks; no actual network, protocol framing validation or model result. Earlier presence disproves introduction at a later refactor; not proof of first-ever origin.')
    with args.output.open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
