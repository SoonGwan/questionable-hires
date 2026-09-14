#!/usr/bin/env python3
"""Author controls for reviewing two lossy header-dictionary projections."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PROBE = r'''
import json, pathlib, unittest, httpx
assert pathlib.Path(httpx.__file__).resolve() == pathlib.Path.cwd() / 'httpx/__init__.py'
cases = [
    ('unique', [(b'x-tag', b'one'), (b'x-other', b'other')]),
    ('repeated', [(b'X-Tag', b'one'), (b'x-tag', b'two')]),
    ('comma-value', [(b'x-tag', b'one, two')]),
    ('repeated-with-comma', [(b'x-tag', b'one, two'), (b'x-tag', b'three')]),
]
rows = []
for name, pairs in cases:
    original = httpx.Headers(pairs)
    projections = [('original', original),
        ('last-value', httpx.Headers({k.decode('ascii').lower(): v.decode('ascii') for k,v in pairs})),
        ('joined-value', httpx.Headers(dict(original)))]
    for version, h in projections:
        rows.append(dict(case=name, version=version, lookup=h['x-tag'],
                         values=h.get_list('x-tag'), multi_items=h.multi_items(),
                         raw=[[k.decode('ascii'),v.decode('ascii')] for k,v in h.raw]))
lookup = {(r['case'],r['version']):r for r in rows}
assert lookup['unique','original']['values'] == lookup['unique','last-value']['values'] == ['one']
assert lookup['repeated','original']['values'] == ['one','two']
assert lookup['repeated','last-value']['values'] == ['two']
assert lookup['repeated','joined-value']['values'] == ['one, two']
assert lookup['repeated','joined-value']['lookup'] == lookup['comma-value','joined-value']['lookup']
assert lookup['repeated','original']['values'] != lookup['comma-value','original']['values']
assert lookup['repeated-with-comma','original']['values'] == ['one, two','three']
try:
    unittest.TestCase().assertEqual(lookup['repeated','original']['values'],lookup['repeated','joined-value']['values'])
except AssertionError as error: failure = str(error)
else: raise AssertionError('Expected actual field-boundary loss')
print(json.dumps(dict(observations=rows, deliberate_assertion_failure=failure),indent=2))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists(): parser.error('Output exists')
    root = args.source.resolve()
    def git(*args): return subprocess.check_output(['git', *args],cwd=root,text=True).strip()
    assert git('rev-parse','HEAD') == '26d48e0634e6ee9cdc0533996db289ce4b430177'
    assert not git('status','--porcelain')
    names = git('ls-files').splitlines()
    before = {n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
    native = subprocess.run([str(args.python),'-B','-m','pytest','-q','-p','no:cacheprovider',
                             'tests/models/test_headers.py'],cwd=root,capture_output=True,text=True,check=True,timeout=30)
    result = subprocess.run([str(args.python),'-B','-c',PROBE],cwd=root,capture_output=True,text=True,check=True,timeout=30)
    assert before == {n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
    assert not git('status','--porcelain') and not list(root.rglob('__pycache__'))
    report = dict(source_revision=git('rev-parse','HEAD'),native_output=native.stdout,
                  original_files_unchanged=True,tracked_files=len(names),**json.loads(result.stdout),
                  limitation='Author projection checks, not complete replacement implementations or a model result.')
    with args.output.open('x') as stream: stream.write(json.dumps(report,indent=2)+'\n')
    print(native.stdout)
    print('Twelve header observations and real lossy-projection assertion verified.')


if __name__ == '__main__': main()
