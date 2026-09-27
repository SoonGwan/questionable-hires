"""Local prototype: bounded serialized report, primitive values, unchanged assertions."""
import json
import sys
import unittest

class UnavailableValue(Exception):
    pass

def encode(value, nodes, depth=0):
    nodes[0] -= 1
    if nodes[0] < 0:
        raise UnavailableValue('node limit')
    kind = type(value)
    if value is None or kind is bool:
        return value
    if kind is int and value.bit_length() <= 256:
        return value
    if kind is str and len(value) <= 256:
        return value
    if kind is bytes and len(value) <= 128:
        return {'bytes_hex': value.hex()}
    if depth < 3 and (kind is list or kind is tuple) and len(value) <= 16:
        return {'kind': 'list' if kind is list else 'tuple',
                'items': [encode(v, nodes, depth+1) for v in value]}
    raise UnavailableValue('unsupported or bounded value')

def compact(value):
    return json.dumps(value, separators=(',', ':'), ensure_ascii=True)

def observe(max_bytes=4096, max_records=64):
    if type(max_bytes) is not int or not 128 <= max_bytes <= 65536:
        raise ValueError('Byte budget must be128..65536')
    if type(max_records) is not int or not 1 <= max_records <= 64:
        raise ValueError('Record budget must be1..64')
    if sys.getprofile() is not None:
        raise RuntimeError('Existing profile hook: do not replace it')
    scope = 'assertEqual/assertIsNot current-thread calls'
    rows, state = [], {'reason': None, 'used': 0, 'stopped': False, 'closed': False}
    reserve = len(compact({'scope': scope, 'observations': [], 'complete': False, 'reason': 'unavailable_value'}))
    methods = {unittest.TestCase.assertEqual.__code__: ('assertEqual', 'first', 'second'),
               unittest.TestCase.assertIsNot.__code__: ('assertIsNot', 'expr1', 'expr2')}
    def profile(frame, event, arg):
        if state['stopped'] or event != 'call' or frame.f_code not in methods:
            return
        try:
            if len(rows) >= max_records:
                state.update(reason=state['reason'] or 'record_limit', stopped=True)
                return
            method, first, second = methods[frame.f_code]
            a, b = frame.f_locals[first], frame.f_locals[second]
            try:
                nodes = [32]
                row = dict(method=method, actual=encode(a, nodes), expected=encode(b, nodes), same_object=a is b)
            except UnavailableValue:
                state['reason'] = state['reason'] or 'unavailable_value'
                row = dict(method=method, values_observed=False, same_object=a is b)
            serialized = compact(row)
            added = len(serialized) + bool(rows)
            if reserve + state['used'] + added > max_bytes:
                state.update(reason=state['reason'] or 'byte_limit', stopped=True)
                return
            rows.append(serialized)
            state['used'] += added
        except Exception:
            state.update(reason=state['reason'] or 'observer_error', stopped=True)
    def report():
        reason = state['reason'] or ('no_observations' if not rows else None)
        result = compact({'scope': scope, 'observations': [json.loads(row) for row in rows],
                          'complete': reason is None, 'reason': reason})
        assert len(result.encode('ascii')) <= max_bytes
        return result
    def close():
        if not state['closed']:
            if sys.getprofile() is profile:
                sys.setprofile(None)
            else:
                state['reason'] = state['reason'] or 'profile_replaced'
            state['closed'] = True
        return report()
    report.close = close
    sys.setprofile(profile)
    return report
