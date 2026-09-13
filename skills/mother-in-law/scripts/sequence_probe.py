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


async def sequence(factory, method_name, state_name, queries, order, failure=None,
                   error_state_name=None, sequential=False):
    target = factory()
    pending, entered, tasks = {}, asyncio.Queue(), []

    async def fetch(query):
        future = asyncio.get_running_loop().create_future()
        pending[query] = future
        entered.put_nowait(query)
        return await future

    async def start(query):
        method = getattr(target, method_name)
        tasks.append(asyncio.create_task(method(query, fetch)))
        if await entered.get() != query:
            raise AssertionError('submission order changed')

    try:
        if not sequential:
            for query in queries:
                await start(query)
        errors = []
        checkpoints = []
        for index in order:
            query = queries[index]
            if sequential:
                await start(query)
            if failure == index:
                pending[query].set_exception(RuntimeError('controlled failure'))
            else:
                pending[query].set_result(query + ' result')
            try:
                await tasks[index]
            except RuntimeError as error:
                errors.append(str(error))
            if sequential:
                if failure == index and error_state_name is not None:
                    checkpoints.append(bool(getattr(target, error_state_name)))
                else:
                    passed = getattr(target, state_name) == query + ' result'
                    if error_state_name is not None:
                        passed = passed and not getattr(target, error_state_name)
                    checkpoints.append(bool(passed))
        observed = {'queries': queries,
                    'completion_order': [queries[i] for i in order],
                    'state': getattr(target, state_name), 'errors': errors}
        if error_state_name is not None:
            observed['error_state'] = getattr(target, error_state_name)
        if sequential:
            observed['checkpoints_passed'] = checkpoints
        return observed
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def probe(factory, method, state, old, new, boundary, error_state=None):
    cases = []
    normal = await sequence(factory, method, state, [old, new], [0, 1], sequential=True)
    cases.append({'name': 'normal', 'passed': all(normal['checkpoints_passed']),
                  'observed': normal})
    stale = await sequence(factory, method, state, [old, new], [1, 0])
    cases.append({'name': 'older-success-after-newer-success',
                  'passed': stale['state'] == new + ' result', 'observed': stale})
    if error_state is not None:
        recovery = await sequence(factory, method, state, [old, new], [0, 1],
                                  failure=0, error_state_name=error_state,
                                  sequential=True)
        cases.append({'name': 'current-error-then-recovery',
                      'passed': all(recovery['checkpoints_passed']),
                      'observed': recovery})
        stale_error = await sequence(factory, method, state, [old, new], [1, 0],
                                     failure=0, error_state_name=error_state)
        cases.append({'name': 'older-error-after-newer-success',
                      'passed': stale_error['state'] == new + ' result'
                      and not stale_error['error_state'],
                      'observed': stale_error})
    if boundary is not None:
        boundary_normal = await sequence(factory, method, state, [old, boundary],
                                         [0, 1], sequential=True)
        cases.append({'name': 'normal-boundary',
                      'passed': all(boundary_normal['checkpoints_passed']),
                      'observed': boundary_normal})
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
    parser.add_argument('--error-state', help='error attribute; checks current error, recovery and stale error')
    parser.add_argument('--output', type=Path, help='new JSON evidence file below --root; never overwritten')
    parser.add_argument('--old', default='old')
    parser.add_argument('--new', default='new')
    parser.add_argument('--boundary', help='optional documented invalidating query; empty is valid')
    parser.add_argument('--timeout', type=float, default=5)
    args = parser.parse_args()
    evidence = None
    try:
        if (not 0 < args.timeout <= 30 or args.old == args.new
                or args.boundary in (args.old, args.new)):
            raise ValueError('timeout must be in (0, 30] and queries must differ')
        if args.output is not None:
            path = args.root / args.output
            if path.is_symlink() or args.root.resolve() not in path.resolve().parents:
                raise ValueError('output must be a new file below --root')
            evidence = path.open('x', encoding='utf-8')
        factory = load_class((args.root / args.source), args.class_name, args.root)
        cases = asyncio.run(asyncio.wait_for(
            probe(factory, args.method, args.state, args.old, args.new, args.boundary,
                  args.error_state),
            timeout=args.timeout))
        result = {'complete': True, 'layer': 'local async component', 'cases': cases}
        status = int(any(not case['passed'] for case in cases))
    except (AttributeError, OSError, TypeError, ValueError, asyncio.TimeoutError) as error:
        result = {'complete': False, 'error': str(error)}
        status = 2
    try:
        serialized = json.dumps(result, separators=(',', ':'))
        if evidence is not None:
            evidence.write(serialized + '\n')
        print(serialized)
        return status
    finally:
        if evidence is not None:
            evidence.close()


if __name__ == '__main__':
    sys.exit(main())
