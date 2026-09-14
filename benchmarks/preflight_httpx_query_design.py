#!/usr/bin/env python3
"""Author preflight for QueryParams versus a specified plain-dict encoding."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

PROBE = r'''
import httpx, json, pathlib, unittest
from urllib.parse import urlencode
assert pathlib.Path(httpx.__file__).resolve() == pathlib.Path.cwd() / 'httpx/__init__.py'
cases = [
    [('a','1'),('a','2'),('keep','x')],
    {'enabled':True,'empty':None},
    {'a':['1','2']},
    {'a':'one two','keep':'x'},
]
rows = []
for index, value in enumerate(cases,1):
    q = httpx.QueryParams(value)
    rows.append(dict(case=index,current=str(q),multi_items=q.multi_items(),
                     proposed=urlencode(dict(value))))
assert [r['current'] for r in rows] == ['a=1&a=2&keep=x','enabled=true&empty=','a=1&a=2','a=one+two&keep=x']
assert [r['proposed'] for r in rows] == ['a=2&keep=x','enabled=True&empty=None','a=%5B%271%27%2C+%272%27%5D','a=one+two&keep=x']
base = httpx.QueryParams('a=1&a=2&keep=x')
derived = base.add('a','3')
with httpx.Client(params=base, trust_env=False, transport=httpx.MockTransport(lambda r:httpx.Response(200))) as client:
    request = client.build_request('GET','https://example.invalid/path',params=[('a','7'),('a','8')])
    client_after = str(client.params)
assert str(base) == client_after == 'a=1&a=2&keep=x'
assert str(derived) == 'a=1&a=2&a=3&keep=x'
assert str(request.url) == 'https://example.invalid/path?a=7&a=8&keep=x'
try:
    unittest.TestCase().assertEqual(rows[0]['current'],rows[0]['proposed'])
except AssertionError as error: failure = str(error)
else: raise AssertionError('Expected actual repeated-value loss')
print(json.dumps(dict(observations=rows,base=str(base),derived=str(derived),
                     request_url=str(request.url),client_after=client_after,
                     deliberate_assertion_failure=failure),indent=2))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--python',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if args.output.exists(): parser.error('Output exists')
    root = args.source.resolve()
    def git(*parts): return subprocess.check_output(['git',*parts],cwd=root,text=True).strip()
    assert git('rev-parse','HEAD') == '26d48e0634e6ee9cdc0533996db289ce4b430177'
    assert not git('status','--porcelain')
    names=git('ls-files').splitlines()
    before={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
    native=subprocess.run([str(args.python),'-B','-m','pytest','-q','-p','no:cacheprovider',
                           'tests/models/test_queryparams.py'],cwd=root,capture_output=True,text=True,check=True,timeout=30)
    result=subprocess.run([str(args.python),'-B','-c',PROBE],cwd=root,capture_output=True,text=True,check=True,timeout=30)
    assert before == {n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
    assert not git('status','--porcelain') and not list(root.rglob('__pycache__'))
    report=dict(source_revision=git('rev-parse','HEAD'),native_output=native.stdout,
                original_files_unchanged=True,tracked_files=len(names),**json.loads(result.stdout),
                limitation='Author checks only; no full replacement implementation, network request or model result.')
    with args.output.open('x') as stream:stream.write(json.dumps(report,indent=2)+'\n')
    print(native.stdout)
    print('Four encoding pairs, functional update and client merge verified.')


if __name__ == '__main__': main()
