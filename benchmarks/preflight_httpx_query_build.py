#!/usr/bin/env python3
"""Author-only construction observations, never sent to model sessions."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import unittest


def observe(source):
    sys.path.insert(0, str(source))
    import httpx
    assert Path(httpx.__file__).resolve().is_relative_to(source)
    url = 'https://example.invalid/items?from=url&tag=url1&tag=url2'
    scenarios = [
        ('omitted', {}, {}, [('from', 'url'), ('tag', 'url1'), ('tag', 'url2')]),
        ('empty', {}, {'params': {}}, []),
        ('defaults', {'params': {'tenant': 'client'}}, {}, [('tenant', 'client')]),
        ('override', {'params': {'tenant': 'client', 'tag': ['client1', 'client2']}},
         {'params': {'tag': ['request1', 'request2'], 'page': '2'}},
         [('tenant', 'client'), ('tag', 'request1'), ('tag', 'request2'), ('page', '2')]),
    ]
    check = unittest.TestCase()
    results = []
    for name, client_kwargs, request_kwargs, expected in scenarios:
        with httpx.Client(trust_env=False, **client_kwargs) as client:
            request = client.build_request('GET', url, **request_kwargs)
            items = request.url.params.multi_items()
            check.assertEqual(items, expected)
            results.append(dict(case=name, client_kwargs=client_kwargs, request_kwargs=request_kwargs,
                                url=str(request.url), items=items))
    try:
        check.assertEqual(results[1]['items'], results[0]['items'])
    except AssertionError as error:
        failure = str(error)
    else:
        raise AssertionError('Contradictory assertion did not fail')
    return dict(upstream_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip(),
                python=sys.version, imported_module='httpx/__init__.py', results=results,
                deliberate_assertion_failure=failure,
                limitation='Author real-object construction preflight and actual assertion control, not model evidence; no requests sent or files created.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = observe(args.source.resolve())
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps(result, indent=2))
