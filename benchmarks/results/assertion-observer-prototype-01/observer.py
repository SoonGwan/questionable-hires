"""Local prototype: bounded primitive arguments; never call arbitrary repr."""
import json
import sys
import unittest

def encode(value, depth=0):
    kind = type(value)
    if value is None or kind is bool:
        return value
    if kind is int:
        return value if value.bit_length() <= 256 else {'omitted': 'large integer'}
    if kind is str:
        return value if len(value) <= 256 else {'omitted': 'long string'}
    if kind is bytes:
        return {'bytes_hex': value.hex()} if len(value) <= 128 else {'omitted': 'long bytes'}
    if depth < 3 and (kind is list or kind is tuple) and len(value) <= 16:
        return {'kind': 'list' if kind is list else 'tuple', 'items': [encode(v, depth+1) for v in value]}
    return {'omitted': 'unsupported or bounded value'}

def observe():
    if sys.getprofile() is not None:
        raise RuntimeError('Existing profile hook: do not replace it')
    rows = []
    errors = []
    methods = {unittest.TestCase.assertEqual.__code__: ('assertEqual', 'first', 'second'),
               unittest.TestCase.assertIsNot.__code__: ('assertIsNot', 'expr1', 'expr2')}
    def profile(frame, event, arg):
        if event != 'call' or frame.f_code not in methods:
            return
        try:
            if len(rows) >= 64:
                if not errors: errors.append('observation limit')
                return
            method, first, second = methods[frame.f_code]
            a, b = frame.f_locals[first], frame.f_locals[second]
            rows.append(dict(method=method, actual=encode(a), expected=encode(b),
                             same_object=a is b))
        except Exception:
            if not errors: errors.append('unavailable observation')
    sys.setprofile(profile)
    return rows, errors
