"""Author preflight: real caller, independent changes, passing/failing controls."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from httpx_link_history_case import HEAD

PROBE = r'''
import __future__, ast, inspect, json, textwrap, unittest
from pathlib import Path
from unittest.mock import patch
import httpx
import httpx._models as module
assert Path(httpx.__file__).resolve() == Path.cwd() / 'httpx/__init__.py'
original = module._parse_header_links
source = textwrap.dedent(inspect.getsource(original))
headers = [None, '</next>', '</next>; rel=next',
           '</next>; rel=next; type=text/plain',
           '</next>; token=a=b; rel=next', '</next>; preload; rel=next']
def observe():
    return [httpx.Response(200, headers={} if h is None else {'Link': h}).links
            for h in headers]
def variant(old, new):
    assert source.count(old) == 1
    flags = 0
    for feature in __future__.all_feature_names:
        flags |= getattr(__future__, feature).compiler_flag
    namespace = dict(original.__globals__)
    exec(compile(source.replace(old, new), '<independent proposal>', 'exec',
                 flags=original.__code__.co_flags & flags, dont_inherit=True), namespace)
    return namespace[original.__name__]
current = observe()
proposals = [('A', 'val.split(";", 1)', 'val.split(";")'),
             ('B', 'param.split("=")', 'param.split("=", 1)')]
rows = {'current': current}
for name, old, new in proposals:
    with patch.object(module, original.__name__, variant(old, new)):
        rows[name] = observe()
    assert module._parse_header_links is original
plain = {'/next': {'url': '/next'}}
named = {'next': {'url': '/next', 'rel': 'next'}}
expected = [{}, plain, named,
            {'next': {'url': '/next', 'rel': 'next', 'type': 'text/plain'}},
            plain, plain]
assert current == expected, (current, expected)
expected_a = expected[:3] + [{h.strip('<> \'"'): {'url': h.strip('<> \'"')}} for h in headers[3:]]
assert rows['A'] == expected_a, (rows['A'], expected_a)
expected_b = expected[:]
expected_b[4] = {'next': {'url': '/next', 'token': 'a=b', 'rel': 'next'}}
assert rows['B'] == expected_b, (rows['B'], expected_b)
failures = {}
for name, index in [('A', 3), ('B', 4)]:
    try:
        unittest.TestCase().assertEqual(rows[name][index], current[index])
    except AssertionError as error:
        failures[name] = str(error)
    else:
        raise AssertionError('Expected actual compatibility assertion failure')
assert observe() == current
print(json.dumps(dict(observations=rows, deliberate_assertion_failures=failures,
                     restored=True), indent=2))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists')
    root = args.source.resolve()
    def git(*arguments):
        return subprocess.check_output(['git', *arguments], cwd=root, text=True).strip()
    assert git('rev-parse', 'HEAD') == HEAD
    assert git('rev-parse', '--is-shallow-repository') == 'false'
    assert not git('status', '--porcelain')
    names = git('ls-files').splitlines()
    before = {n: hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
    native = subprocess.run([str(args.python), '-B', '-m', 'pytest', '-q', '-p',
                             'no:cacheprovider', 'tests/models/test_responses.py::test_link_headers'],
                            cwd=root, capture_output=True, text=True, check=True, timeout=30)
    result = subprocess.run([str(args.python), '-B', '-c', PROBE], cwd=root,
                            capture_output=True, text=True, check=True, timeout=30)
    prior_parser = git('show', '41597adf^:httpx/_utils.py')
    prior_caller = git('show', '41597adf^:httpx/_models.py')
    assert 'def parse_header_links' in prior_parser
    assert 'url, params = val.split(";", 1)' in prior_parser
    assert 'key, value = param.split("=")' in prior_parser
    assert 'for link in parse_header_links(header)' in prior_caller
    assert before == {n: hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
    assert not git('status', '--porcelain') and not list(root.rglob('__pycache__'))
    report = dict(revision=HEAD, tracked_files=len(names), source_unchanged=True,
                  native_output=native.stdout, earlier_revision=git('rev-parse','41597adf^'),
                  **json.loads(result.stdout),
                  limitation='Author preflight on pinned source; not model evidence, standards compliance or first-ever origin.')
    with args.output.open('x') as stream:
        stream.write(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
