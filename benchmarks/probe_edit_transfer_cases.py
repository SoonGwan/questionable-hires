"""Two sizes of one upstream native-test improvement, without altered semantics."""
import ast
import json
from pathlib import Path

from packaging_specifier_cases import SNAPSHOT, validate_files

SELECTOR = ['tests/test_specifiers.py::TestSpecifier::test_specifiers_valid',
            '-q', '--tb=short', '-p', 'no:cacheprovider']
TEST_FILE = 'tests/test_specifiers.py'
TARGET = 'src/packaging/specifiers.py'


def inputs():
    files = validate_files(json.loads(SNAPSHOT.read_text()))
    source = files[TARGET]
    cls, = [n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == 'Specifier']
    method, = [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '__str__']
    returned, = [n for n in method.body if isinstance(n, ast.Return)]
    old = ast.get_source_segment(source, method)
    expression = ast.get_source_segment(source, returned)
    assert expression == 'return "{}{}".format(*self._spec)' and old.count(expression) == 1
    fault = dict(target=TARGET, old=old, new=old.replace(expression, 'return ""', 1))
    assert source.count(old) == 1
    original = files[TEST_FILE]
    tests, = [n for n in ast.parse(original).body if isinstance(n, ast.ClassDef) and n.name == 'TestSpecifier']
    first = next(n for n in tests.body if isinstance(n, ast.FunctionDef))
    assert first.name == 'test_specifiers_valid'
    lines = original.splitlines(keepends=True)
    old_test = ''.join(lines[first.lineno-1:first.end_lineno])
    assert old_test == '    def test_specifiers_valid(self, specifier):\n        Specifier(specifier)\n'
    new_test = old_test.replace('        Specifier(specifier)', '        assert str(Specifier(specifier)) == specifier')
    assert original.count(old_test) == 1
    variants = dict(full=files, prefix=dict(files, **{TEST_FILE: ''.join(lines[:first.end_lineno])}))
    return variants, fault, dict(old=old_test, new=new_test)


def recipe(files, fault, edit, form):
    result = dict(files=list(files), imports=['packaging', 'packaging.specifiers', 'tests.test_specifiers'],
        import_roots=['src'], runner='pytest', tests=list(SELECTOR), probe_tests=list(SELECTOR),
        guard_project=True, precheck='import packaging.specifiers, tests.test_specifiers\n'
            'assert tests.test_specifiers.Specifier is packaging.specifiers.Specifier\n'
            'print("Verified native test Specifier binding", flush=True)\n', **fault)
    if form == 'edit':
        result['probe_edits'] = {TEST_FILE: edit}
    elif form == 'replacement':
        result['probe_replacements'] = {TEST_FILE: files[TEST_FILE].replace(edit['old'], edit['new'], 1)}
    else:
        raise ValueError('Choose edit or replacement')
    return result
