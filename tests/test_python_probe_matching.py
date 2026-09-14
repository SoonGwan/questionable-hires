"""Author controls for the optional AST-substitution guidance, not model scores."""
import ast
import copy
import unittest


def shape(node):
    return ast.dump(node, include_attributes=False)


def remove_one_statement(source, expected):
    """Test-only probe: reject missing/ambiguous matches before any substitution."""
    tree = ast.parse(source)
    function = tree.body[0]
    wanted = shape(ast.parse(expected).body[0])
    matches = [i for i, node in enumerate(function.body) if shape(node) == wanted]
    if len(matches) != 1:
        raise ValueError('Expected one statement, found %d' % len(matches))
    proposed = copy.deepcopy(tree)
    del proposed.body[0].body[matches[0]]
    namespace = {}
    exec(compile(proposed, '<author probe>', 'exec', dont_inherit=True), namespace)
    return namespace[function.name]


class PythonProbeMatchingTests(unittest.TestCase):
    def test_original_failure_is_formatting_not_missing_statement(self):
        supplied = 'username, password = request.url.username, request.url.password'
        node = ast.parse(supplied).body[0]
        # Actual failure mechanism in both recorded model probes: tuple parentheses.
        with self.assertRaises(AssertionError):
            self.assertEqual(ast.unparse(node), supplied)
        self.assertEqual(shape(node), shape(ast.parse(ast.unparse(node)).body[0]))

    def test_location_and_parentheses_do_not_change_structural_match(self):
        first = ast.parse('left, right = pair').body[0]
        second = ast.parse('\n\n(left, right) = (pair)  # formatting only').body[0]
        self.assertNotEqual(first.lineno, second.lineno)
        self.assertEqual(shape(first), shape(second))

    def test_wrong_attribute_operator_order_or_context_still_rejected(self):
        expected = ast.parse('left, right = request.first, request.second').body[0]
        for source in ('left, right = request.first, request.other',
                       'right, left = request.first, request.second',
                       'left, right = request.first + request.second',
                       'left, right = request.second, request.first'):
            with self.subTest(source=source):
                self.assertNotEqual(shape(expected), shape(ast.parse(source).body[0]))
        self.assertNotEqual(shape(ast.Name(id='value', ctx=ast.Load())),
                            shape(ast.Name(id='value', ctx=ast.Store())))

    def test_zero_or_duplicate_matches_refuse_instead_of_guessing(self):
        for body, count in [('    pass\n', 0), ('    value = 1\n    value = 1\n', 2)]:
            with self.subTest(count=count), self.assertRaisesRegex(ValueError, str(count)):
                remove_one_statement('def f():\n' + body + '    return 3\n', 'value=1')

    def test_matched_removal_still_requires_real_consumer_observations(self):
        source = ('def normalize(value):\n'
                  '    if isinstance(value, int):\n        return value\n'
                  '    return int(value * 100)\n')
        namespace = {}
        exec(compile(source, '<current>', 'exec', dont_inherit=True), namespace)
        original = namespace['normalize']
        proposed = remove_one_statement(source, 'if isinstance(value,int): return value')
        # Invoke the same actual caller with each binding, not an oracle simulation.
        def consumer(normalizer, value):
            return normalizer(value)
        self.assertEqual(consumer(original, 5), 5)
        self.assertEqual(consumer(proposed, 5), 500)
        self.assertEqual(consumer(original, 1.25), consumer(proposed, 1.25))
        with self.assertRaisesRegex(AssertionError, '500 != 5'):
            self.assertEqual(consumer(proposed, 5), 5)
        self.assertEqual(consumer(original, 5), 5)


if __name__ == '__main__':
    unittest.main()
