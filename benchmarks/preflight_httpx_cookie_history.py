#!/usr/bin/env python3
"""Author-only redirect-cookie controls; no model results."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PROBE = r'''
import __future__, ast, inspect, json, textwrap, unittest
from unittest.mock import patch
import httpx
from httpx._client import BaseClient
original = BaseClient._redirect_headers
tree = ast.parse(textwrap.dedent(inspect.getsource(original)))
body = tree.body[0].body
removed = [n for n in body if isinstance(n, ast.Expr)
           and ast.unparse(n) == "headers.pop('Cookie', None)"]
assert len(removed) == 1
body.remove(removed[0])
flags = 0
for name in __future__.all_feature_names: flags |= getattr(__future__, name).compiler_flag
scope = dict(original.__globals__)
exec(compile(tree, '<proposal>', 'exec', flags=original.__code__.co_flags & flags,
             dont_inherit=True), scope)
candidate = scope[original.__name__]
assert candidate.__annotations__ == original.__annotations__
cases = [
    ('rotate', 'https://example.invalid/start', '/done', 'sid=new; Path=/', 'sid=old'),
    ('expire', 'https://example.invalid/start', '/done', 'sid=gone; Path=/; Max-Age=0', 'sid=old'),
    ('cross-host', 'https://example.invalid/start', 'https://other.invalid/done', None, 'sid=old'),
    ('unchanged', 'https://example.invalid/start', '/done', None, 'sid=old'),
    ('initially-empty', 'https://example.invalid/start', '/done', 'sid=new; Path=/', None),
]
def observe():
    rows = []
    for name, url, location, set_cookie, initial in cases:
        seen = []
        def handler(request):
            seen.append(dict(url=str(request.url), cookie=request.headers.get('Cookie')))
            if len(seen) == 1:
                headers = {'Location': location}
                if set_cookie: headers['Set-Cookie'] = set_cookie
                return httpx.Response(302, headers=headers)
            return httpx.Response(200)
        with httpx.Client(transport=httpx.MockTransport(handler), trust_env=False,
                          follow_redirects=True) as client:
            if initial: client.cookies.set('sid', 'old', domain='example.invalid', path='/')
            assert client.get(url).status_code == 200
        assert len(seen) == 2
        rows.append(dict(case=name, requests=seen))
    return rows
current = observe()
with patch.object(BaseClient, '_redirect_headers', candidate): proposed = observe()
assert [r['requests'][1]['cookie'] for r in current] == ['sid=new', None, None, 'sid=old', 'sid=new']
assert [r['requests'][1]['cookie'] for r in proposed] == ['sid=old', 'sid=old', 'sid=old', 'sid=old', 'sid=new']
assert [r['requests'][0]['cookie'] for r in current] == ['sid=old'] * 4 + [None]
assert [r['requests'][0] for r in current] == [r['requests'][0] for r in proposed]
try:
    unittest.TestCase().assertEqual(proposed[0]['requests'][1]['cookie'], current[0]['requests'][1]['cookie'])
except AssertionError as error: failure = str(error)
else: raise AssertionError('Expected actual stale-cookie mismatch')
print(json.dumps(dict(current=current, proposed=proposed,
                     deliberate_assertion_failure=failure, annotations_preserved=True), indent=2))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists(): parser.error('Output exists')
    root = args.source.resolve()
    def git(*parts):
        return subprocess.check_output(['git', *parts], cwd=root, text=True).strip()
    assert git('rev-parse', 'HEAD') == '26d48e0634e6ee9cdc0533996db289ce4b430177'
    assert git('rev-parse', '--is-shallow-repository') == 'false'
    assert not git('status', '--porcelain')
    names = git('ls-files').splitlines()
    before = {n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in names}
    native = subprocess.run([str(args.python), '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider',
                             'tests/client/test_redirects.py::test_redirect_cookie_behavior'],
                            cwd=root, capture_output=True, text=True, check=True, timeout=30)
    result = subprocess.run([str(args.python), '-B', '-c', PROBE], cwd=root,
                            capture_output=True, text=True, check=True, timeout=30)
    earlier = git('show', '00e150f^:httpx/middleware/redirect.py')
    assert 'headers.pop("Cookie", None)' in earlier
    assert 'cookies = Cookies(self.cookies)' in earlier
    assert before == {n: hashlib.sha256((root / n).read_bytes()).hexdigest() for n in names}
    assert not git('status', '--porcelain') and not list(root.rglob('__pycache__'))
    report = dict(revision=git('rev-parse', 'HEAD'), tracked_files=len(names), source_unchanged=True,
                  earlier_revision=git('rev-parse', '00e150f^'),
                  earlier_source_sha256=hashlib.sha256(earlier.encode()).hexdigest(),
                  native_output=native.stdout, **json.loads(result.stdout),
                  limitation='Author preflight only. Synthetic cookies, no network. Earlier presence is not first-ever origin.')
    with args.output.open('x') as stream: stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__': main()
