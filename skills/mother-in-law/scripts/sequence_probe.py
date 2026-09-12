#!/usr/bin/env python3
"""Probe latest-result behavior for a local async run(query, fetch) component."""
import argparse
import asyncio
import importlib.util
import json
from pathlib import Path
import sys


def load_class(source, class_name, root):
    root = root.resolve(strict=True)
    if source.is_symlink():
        raise ValueError('source must not be a symlink')
    source = source.resolve(strict=True)
    if root not in source.parents or not source.is_file():
        raise ValueError('source must be a regular Python file below --root')
    spec = importlib.util.spec_from_file_location('_interaction_probe_target', source)
    if not spec or not spec.loader:
        raise ValueError('cannot load source module')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    candidate = getattr(module, class_name, None)
    if not isinstance(candidate, type):
        raise ValueError('class not found')
    return candidate


async def sequence(factory, method_name, state_name, queries, order, failure=None):
    target = factory()
    pending, entered, tasks = {}, asyncio.Queue(), []

    async def fetch(query):
        future = asyncio.get_running_loop().create_future()
        pending[query] = future
        entered.put_nowait(query)
        return await future

    try:
        for query in queries:
            method = getattr(target, method_name)
            tasks.append(asyncio.create_task(method(query, fetch)))
            if await entered.get() != query:
                raise AssertionError('submission order changed')
        errors = []
        for index in order:
            query = queries[index]
            if failure == index:
                pending[query].set_exception(RuntimeError('controlled failure'))
            else:
                pending[query].set_result(query + ' result')
            try:
                await tasks[index]
            except RuntimeError as error:
                errors.append(str(error))
        return {'queries': queries, 'completion_order': [queries[i] for i in order],
                'state': getattr(target, state_name), 'errors': errors}
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def probe(factory, method, state, old, new, boundary):
    cases = []
    normal = await sequence(factory, method, state, [old, new], [0, 1])
    cases.append({'name': 'normal', 'passed': normal['state'] == new + ' result',
                  'observed': normal})
    stale = await sequence(factory, method, state, [old, new], [1, 0])
    cases.append({'name': 'older-success-after-newer-success',
                  'passed': stale['state'] == new + ' result', 'observed': stale})
    if boundary is not None:
        crossed = await sequence(factory, method, state, [old, boundary], [1, 0])
        cases.append({'name': 'older-success-after-boundary',
                      'passed': crossed['state'] == boundary + ' result',
                      'observed': crossed})
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--class-name', required=True)
    parser.add_argument('--method', default='run')
    parser.add_argument('--state', default='result')
    parser.add_argument('--old', default='old')
    parser.add_argument('--new', default='new')
    parser.add_argument('--boundary', help='optional documented invalidating query; empty is valid')
    parser.add_argument('--timeout', type=float, default=5)
    args = parser.parse_args()
    try:
        if not 0 < args.timeout <= 30 or args.old == args.new:
            raise ValueError('timeout must be in (0, 30] and queries must differ')
        factory = load_class((args.root / args.source), args.class_name, args.root)
        cases = asyncio.run(asyncio.wait_for(
            probe(factory, args.method, args.state, args.old, args.new, args.boundary),
            timeout=args.timeout))
        result = {'complete': True, 'layer': 'local async component', 'cases': cases}
        print(json.dumps(result, separators=(',', ':')))
        return int(any(not case['passed'] for case in cases))
    except (AttributeError, OSError, TypeError, ValueError, asyncio.TimeoutError) as error:
        print(json.dumps({'complete': False, 'error': str(error)}, separators=(',', ':')))
        return 2


if __name__ == '__main__':
    sys.exit(main())
