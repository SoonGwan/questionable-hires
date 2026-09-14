#!/usr/bin/env python3
"""Author controls for a new URL-auth history/compatibility review."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PROBE = r'''
import __future__, ast, base64, inspect, json, textwrap, unittest
from unittest.mock import patch
import httpx
from httpx._client import BaseClient

original = BaseClient._build_request_auth
tree = ast.parse(textwrap.dedent(inspect.getsource(original)))
body = tree.body[0].body
removed = [node for node in body if
           (isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple)
            and [name.id for name in node.targets[0].elts] == ['username', 'password'])
           or (isinstance(node, ast.If) and ast.unparse(node.test) == 'username or password')]
assert len(removed) == 2
for node in removed: body.remove(node)
flags = 0
for name in __future__.all_feature_names: flags |= getattr(__future__, name).compiler_flag
namespace = dict(original.__globals__)
exec(compile(ast.fix_missing_locations(tree), '<proposal>', 'exec',
             flags=original.__code__.co_flags & flags, dont_inherit=True), namespace)
candidate = namespace[original.__name__]
assert candidate.__annotations__ == original.__annotations__
url = 'https://url-user:url-pass@example.invalid/path'
client_auth = ('client-user', 'client-pass')
request_auth = ('request-user', 'request-pass')
cases = [
    ('URL only', url, {}, {}),
    ('client overrides URL', url, {'auth': client_auth}, {}),
    ('request overrides client', url, {'auth': client_auth}, {'auth': request_auth}),
    ('explicit None with URL', url, {'auth': client_auth}, {'auth': None}),
    ('explicit None without URL', 'https://example.invalid/path', {'auth': client_auth}, {'auth': None}),
]
def observe():
    observed = []
    for label, target, options, request_options in cases:
        headers = []
        def handler(request):
            headers.append(request.headers.get('Authorization'))
            return httpx.Response(200)
        with httpx.Client(transport=httpx.MockTransport(handler), trust_env=False, **options) as client:
            assert client.get(target, **request_options).status_code == 200
        assert len(headers) == 1
        observed.append(dict(case=label, authorization=headers[0]))
    return observed
def basic(user, password):
    return 'Basic ' + base64.b64encode((user + ':' + password).encode()).decode()
current = observe()
with patch.object(BaseClient, '_build_request_auth', candidate): proposed = observe()
assert [row['authorization'] for row in current] == [basic('url-user','url-pass'), basic(*client_auth), basic(*request_auth), basic('url-user','url-pass'), None]
assert [row['authorization'] for row in proposed] == [None, basic(*client_auth), basic(*request_auth), None, None]
try:
    unittest.TestCase().assertEqual(proposed[0]['authorization'], current[0]['authorization'])
except AssertionError as error:
    failure = str(error)
else: raise AssertionError('Expected actual URL-auth behavior disagreement')
print(json.dumps(dict(current=current, proposed=proposed, deliberate_assertion_failure=failure,
                     annotations_preserved=True), indent=2))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists(): parser.error('Output exists')
    root = args.source.resolve()
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=root, text=True).strip()
    revision = git('rev-parse', 'HEAD')
    assert revision == '26d48e0634e6ee9cdc0533996db289ce4b430177'
    assert git('rev-parse', '--is-shallow-repository') == 'false'
    assert git('status', '--porcelain') == ''
    names = git('ls-files').splitlines()
    before = {n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in names}
    native = subprocess.run([str(args.python), '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                             'tests/client/test_auth.py::test_auth_hidden_url'], cwd=root,
                            capture_output=True, text=True, check=True, timeout=30)
    result = subprocess.run([str(args.python), '-B', '-c', PROBE], cwd=root,
                            capture_output=True, text=True, check=True, timeout=30)
    earlier = git('show', '00e150f^:httpx/client.py')
    assert 'if request.url.username or request.url.password:' in earlier
    assert 'return BasicAuthMiddleware(' in earlier
    assert before == {n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in names}
    assert git('status', '--porcelain') == '' and not list(root.rglob('__pycache__'))
    report = dict(revision=revision, shallow=False, reachable_commits=int(git('rev-list','--count','HEAD')),
                  tracked_files=len(names), source_unchanged=True, native_output=native.stdout,
                  earlier_revision=git('rev-parse','00e150f^'),
                  earlier_source_sha256=hashlib.sha256(earlier.encode()).hexdigest(),
                  **json.loads(result.stdout),
                  limitation='Author preflight, not model adoption or performance; all credentials are synthetic, no network or live authentication. Earlier presence is not first-ever origin.')
    with args.output.open('x') as stream: stream.write(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__': main()
