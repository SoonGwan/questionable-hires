#!/usr/bin/env python3
"""Author-only real HTTPX observation preflight, not supplied to model cells."""
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
    body = b'alpha\nbeta\n'

    class RecordedStream(httpx.SyncByteStream):
        def __init__(self):
            self.close_calls = 0

        def __iter__(self):
            yield body[:6]
            yield body[6:]

        def close(self):
            self.close_calls += 1

    outcomes = []
    for mode in ('iter-preview', 'read-preview', 'ordinary-get'):
        stream = RecordedStream()
        def handle(request):
            return httpx.Response(200, stream=stream)

        def inspect(response):
            initial = dict(consumed=response.is_stream_consumed, closed=response.is_closed)
            preview = response.read() if mode == 'read-preview' else b''.join(response.iter_bytes())
            try:
                later = response.read()
                later_kind, later_body = 'bytes', later.decode()
            except httpx.StreamConsumed:
                later_kind, later_body = 'StreamConsumed', None
            return dict(mode=mode, initial=initial, preview=preview.decode(), later_kind=later_kind,
                        later_body=later_body, consumed=response.is_stream_consumed,
                        closed=response.is_closed, close_calls=stream.close_calls)

        with httpx.Client(transport=httpx.MockTransport(handle)) as client:
            if mode == 'ordinary-get':
                outcome = inspect(client.get('https://example.invalid/'))
            else:
                with client.stream('GET', 'https://example.invalid/') as response:
                    outcome = inspect(response)
        outcome['final_close_calls'] = stream.close_calls
        outcomes.append(outcome)
    check = unittest.TestCase()
    for row in outcomes:
        check.assertEqual(row['preview'], body.decode())
        check.assertTrue(row['consumed'])
        check.assertTrue(row['closed'])
        check.assertEqual(row['close_calls'], 1)
        check.assertEqual(row['final_close_calls'], 1)
    check.assertEqual([r['later_kind'] for r in outcomes], ['StreamConsumed', 'bytes', 'bytes'])
    check.assertEqual([r['later_body'] for r in outcomes], [None, body.decode(), body.decode()])
    try:
        check.assertEqual(outcomes[0]['later_kind'], 'bytes')
    except AssertionError as error:
        deliberate_failure = str(error)
    else:
        raise AssertionError('Negative assertion control did not fail')
    return dict(upstream_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip(),
                python=sys.version, imported_module='httpx/__init__.py',
                outcomes=outcomes, deliberate_assertion_failure=deliberate_failure,
                limitation='Author observations and assertion control. In-memory real Client/MockTransport; no live connection pool, network or model run.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    observation = observe(args.source.resolve())
    with args.output.open('x') as stream:
        json.dump(observation, stream, indent=2)
        stream.write('\n')
    print(json.dumps(observation, indent=2))
