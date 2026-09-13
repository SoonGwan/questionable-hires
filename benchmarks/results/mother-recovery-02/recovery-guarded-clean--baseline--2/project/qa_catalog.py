"""Deterministic component QA; adds only a uniquely named JSON execution record."""
import asyncio
import hashlib
import json
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_FILES = ('lookup.py', 'requirements.md', 'README.md')
record = {
    'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    'python': sys.version,
    'timeout_seconds': 10,
    'method': 'Explicit fetch-entry events and manually settled futures; no sleeps or network.',
    'checks': [],
}


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in SOURCE_FILES}


def state(obj):
    return {'result': obj.result, 'error': obj.error}


def check(scenario, step, obj, expected):
    observed = state(obj)
    record['checks'].append({
        'scenario': scenario, 'step': step,
        'expected': expected, 'observed': observed,
        'passed': all(observed[key] == value for key, value in expected.items()),
    })


class ControlledFetch:
    def __init__(self):
        self.entered = asyncio.Event()
        self.future = asyncio.get_running_loop().create_future()

    async def __call__(self, query):
        self.query = query
        self.entered.set()
        return await self.future

    def release(self, outcome, label):
        if outcome == 'success':
            self.future.set_result(label + '-result')
        else:
            self.future.set_exception(RuntimeError(label + '-error'))


async def start(obj, label):
    fetch = ControlledFetch()
    task = asyncio.create_task(obj.run(label, fetch))
    await asyncio.wait_for(fetch.entered.wait(), timeout=1)
    return fetch, task


async def complete(pair, outcome, label):
    fetch, task = pair
    fetch.release(outcome, label)
    await asyncio.wait_for(task, timeout=1)


async def exercise(Lookup):
    obj = Lookup()
    pair = await start(obj, 'normal')
    await complete(pair, 'success', 'normal')
    check('normal success', 'completed', obj,
          {'result': 'normal-result', 'error': None})

    obj = Lookup()
    pair = await start(obj, 'attempt')
    await complete(pair, 'failure', 'attempt')
    # Requirements do not specify the result value after a current failure.
    check('failure then retry', 'current failure completed', obj,
          {'error': 'attempt-error'})
    pair = await start(obj, 'retry')
    await complete(pair, 'success', 'retry')
    check('failure then retry', 'successful retry completed', obj,
          {'result': 'retry-result', 'error': None})

    for older_outcome in ('success', 'failure'):
        for newer_outcome in ('success', 'failure'):
            for first in ('older', 'newer'):
                scenario = (f'older={older_outcome}, newer={newer_outcome}, '
                            f'completion={first}-first')
                obj = Lookup()
                older = await start(obj, 'older')
                newer = await start(obj, 'newer')
                newer_expected = ({'result': 'newer-result', 'error': None}
                                  if newer_outcome == 'success'
                                  else {'error': 'newer-error'})
                if first == 'older':
                    before = state(obj)
                    await complete(older, older_outcome, 'older')
                    check(scenario, 'older completed; newer pending', obj, before)
                    await complete(newer, newer_outcome, 'newer')
                    check(scenario, 'newer completed', obj, newer_expected)
                else:
                    await complete(newer, newer_outcome, 'newer')
                    check(scenario, 'newer completed; older pending', obj, newer_expected)
                    before = state(obj)
                    await complete(older, older_outcome, 'older')
                    check(scenario, 'older completed; preserve newer state', obj, before)


def main():
    output = ROOT / ('qa_catalog_execution_' + uuid.uuid4().hex + '.json')
    record['source_sha256_before'] = hashes()
    record['harness_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    started = time.monotonic()
    try:
        namespace = {'__name__': 'catalog_under_test'}
        # No import cache or bytecode files are written.
        exec(compile((ROOT / 'lookup.py').read_bytes(), str(ROOT / 'lookup.py'), 'exec'), namespace)
        asyncio.run(asyncio.wait_for(exercise(namespace['Lookup']), timeout=10))
    except Exception as error:
        record['execution_error'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        record['elapsed_seconds'] = time.monotonic() - started
        record['source_sha256_after'] = hashes()
        record['sources_unchanged'] = record['source_sha256_before'] == record['source_sha256_after']
        record['passed'] = (not record.get('execution_error')
                            and record['sources_unchanged']
                            and len(record['checks']) == 19
                            and all(item['passed'] for item in record['checks']))
        record['limits'] = [
            'Python component only; no browser or backend exists.',
            'Failures use RuntimeError, the exception handled by this component.',
            'Two overlapping requests, both completion orders, all success/failure pairs.',
            'Cancellation, other exception types, and three-or-more concurrent requests are not exercised.',
            'Current-failure result retention and loading state are unspecified; only required fields are asserted.',
            'Async timeout bounds cooperative waits; it cannot interrupt blocking synchronous code.',
        ]
        with output.open('x') as stream:
            json.dump(record, stream, indent=2)
            stream.write('\n')
    print(json.dumps({'passed': record['passed'], 'checks': len(record['checks']),
                      'record': str(output)}))
    return 0 if record['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
