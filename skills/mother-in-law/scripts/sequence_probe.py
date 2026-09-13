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
        unexpected_errors = []
        checkpoints = []
        failed_checkpoints = []
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
                if failure != index:
                    unexpected_errors.append({'query': query, 'error': str(error)})
            if sequential:
                if failure == index and error_state_name is not None:
                    passed = bool(getattr(target, error_state_name))
                else:
                    passed = getattr(target, state_name) == query + ' result'
                    if error_state_name is not None:
                        passed = passed and not getattr(target, error_state_name)
                checkpoints.append(bool(passed))
                if not passed:
                    detail = {'query': query, 'state': getattr(target, state_name)}
                    if failure != index:
                        detail['expected_state'] = query + ' result'
                    if error_state_name is not None:
                        detail['error_state'] = getattr(target, error_state_name)
                        detail['expected_error'] = 'displayed' if failure == index else 'clear'
                    # Freeze failure evidence before subsequent requests mutate state.
                    failed_checkpoints.append(json.loads(json.dumps(detail)))
        observed = {'queries': queries,
                    'completion_order': [queries[i] for i in order],
                    'state': getattr(target, state_name), 'errors': errors}
        if error_state_name is not None:
            observed['error_state'] = getattr(target, error_state_name)
        if sequential:
            observed['checkpoints_passed'] = checkpoints
        if unexpected_errors:
            observed['unexpected_errors'] = unexpected_errors
        if failed_checkpoints:
            observed['failed_checkpoints'] = failed_checkpoints
        return observed
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


async def probe(factory, method, state, old, new, boundary, error_state=None):
    cases = []

    def record(name, observed, passed):
        cases.append({'name': name,
                      'passed': bool(passed and not observed.get('unexpected_errors')),
                      'observed': observed})

    def successful(observed, query):
        return (observed['state'] == query + ' result'
                and (error_state is None or not observed['error_state']))

    normal = await sequence(factory, method, state, [old, new], [0, 1],
                            error_state_name=error_state, sequential=True)
    record('normal', normal, all(normal['checkpoints_passed']))
    stale = await sequence(factory, method, state, [old, new], [1, 0],
                           error_state_name=error_state)
    record('older-success-after-newer-success', stale, successful(stale, new))
    if error_state is not None:
        recovery = await sequence(factory, method, state, [old, new], [0, 1],
                                  failure=0, error_state_name=error_state,
                                  sequential=True)
        record('current-error-then-recovery', recovery, all(recovery['checkpoints_passed']))
        stale_error = await sequence(factory, method, state, [old, new], [1, 0],
                                     failure=0, error_state_name=error_state)
        record('older-error-after-newer-success', stale_error, successful(stale_error, new))
    if boundary is not None:
        boundary_normal = await sequence(factory, method, state, [old, boundary],
                                         [0, 1], error_state_name=error_state,
                                         sequential=True)
        record('normal-boundary', boundary_normal, all(boundary_normal['checkpoints_passed']))
        crossed = await sequence(factory, method, state, [old, boundary], [1, 0],
                                 error_state_name=error_state)
        record('older-success-after-boundary', crossed, successful(crossed, boundary))
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
