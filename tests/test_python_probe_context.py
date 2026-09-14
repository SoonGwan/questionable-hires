"""Executable controls for preserving context in extracted-source probes.

These are author checks of the instruction's mechanism, not model adoption tests
or a supported general-purpose function transplant API.
"""
import __future__
import unittest


def recompile(original, source):
    future_mask = 0
    for name in __future__.all_feature_names:
        future_mask |= getattr(__future__, name).compiler_flag
    flags = original.__code__.co_flags & future_mask
    namespace = dict(original.__globals__)
    exec(compile(source, '<extracted probe>', 'exec', flags=flags, dont_inherit=True), namespace)
    return namespace[original.__name__]


class PythonProbeContextTests(unittest.TestCase):
    def original(self, source, future=False, namespace=None):
        namespace = {} if namespace is None else namespace
        flags = __future__.annotations.compiler_flag if future else 0
        exec(compile(source, '<original module>', 'exec', flags=flags, dont_inherit=True), namespace)
        return namespace['calculate']

    def test_deferred_annotation_does_not_become_setup_failure(self):
        source = 'def calculate(value: Later) -> Later:\n    return value + 1\n'
        original = self.original(source, future=True)
        self.assertEqual(original(4), 5)
        with self.assertRaisesRegex(NameError, 'Later'):
            exec(compile(source, '<lost module context>', 'exec', dont_inherit=True), {})
        preserved = recompile(original, source)
        self.assertEqual(preserved.__annotations__, original.__annotations__)
        self.assertEqual(preserved(4), 5)

    def test_eager_annotation_and_global_binding_remain_eager(self):
        class Later:
            pass
        source = 'def calculate(value: Later) -> Later:\n    return transform(value)\n'
        original = self.original(source, namespace={'Later': Later, 'transform': lambda value: value + 1})
        preserved = recompile(original, source)
        self.assertIs(preserved.__annotations__['value'], Later)
        self.assertEqual(preserved.__annotations__, original.__annotations__)
        self.assertEqual(preserved(4), 5)
        blindly_deferred = self.original(source, future=True, namespace=dict(original.__globals__))
        self.assertNotEqual(blindly_deferred.__annotations__, original.__annotations__)

    def test_probe_compiler_setting_cannot_override_original(self):
        source = 'def calculate(value: int) -> int:\n    return value + 1\n'
        original = self.original(source)
        caller = '''def transplant(source):
    namespace = {}
    exec(compile(source, '<probe inherits caller>', 'exec'), namespace)
    return namespace['calculate']
'''
        namespace = {}
        exec(compile(caller, '<probe module>', 'exec', flags=__future__.annotations.compiler_flag,
                     dont_inherit=True), namespace)
        inherited = namespace['transplant'](source)
        self.assertEqual(inherited.__annotations__['value'], 'int')
        self.assertIs(recompile(original, source).__annotations__['value'], int)

    def test_preserving_context_does_not_hide_behavioral_difference(self):
        source = 'def calculate(value: Later) -> Later:\n    return value + 1\n'
        original = self.original(source, future=True)
        changed = recompile(original, source.replace('value + 1', 'value + 2'))
        self.assertEqual(changed.__annotations__, original.__annotations__)
        self.assertEqual(original(4), 5)
        self.assertEqual(changed(4), 6)
        with self.assertRaisesRegex(AssertionError, '6 != 5'):
            self.assertEqual(changed(4), original(4))
