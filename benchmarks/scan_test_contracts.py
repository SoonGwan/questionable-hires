#!/usr/bin/env python3
"""Flag async overrides of synchronous unittest methods without importing targets.

Findings require behavioral review, not automatic benchmark rescoring. Local
inheritance and ordinary unittest import aliases are recognized; dynamically
constructed/imported project base classes and monkeypatches are not resolved.
"""
import argparse
import ast
import inspect
import json
from pathlib import Path
import unittest


SYNC_METHODS = {name for name in dir(unittest.TestCase)
                if callable(getattr(unittest.TestCase, name))
                and not inspect.iscoroutinefunction(getattr(unittest.TestCase, name))}


def inspect_source(source):
    tree = ast.parse(source)
    modules, bases = set(), set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            modules.update(alias.asname or alias.name for alias in node.names if alias.name == 'unittest')
        elif isinstance(node, ast.ImportFrom) and node.module == 'unittest':
            bases.update(alias.asname or alias.name for alias in node.names
                         if alias.name in {'TestCase', 'IsolatedAsyncioTestCase'})
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    known = set(bases)

    def native(base):
        return ((isinstance(base, ast.Name) and base.id in known) or
                (isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name)
                 and base.value.id in modules
                 and base.attr in {'TestCase', 'IsolatedAsyncioTestCase'}))

    selected = []
    while True:
        found = [node for node in classes if node not in selected and any(native(base) for base in node.bases)]
        if not found:
            break
        selected.extend(found)
        known.update(node.name for node in found)
    findings = [dict(class_name=cls.name, method=method.name, line=method.lineno,
                     reason='async override of synchronous unittest.TestCase method')
                for cls in selected for method in cls.body
                if isinstance(method, ast.AsyncFunctionDef) and method.name in SYNC_METHODS]
    unresolved = [dict(class_name=cls.name, line=cls.lineno)
                  for cls in classes if cls.bases and cls not in selected]
    return findings, unresolved


def scan(root):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError('Scan root must be an existing directory')
    result = dict(python_files=0, parsed_files=0, findings=[], parse_errors=[], unresolved_classes=[],
                  limitation='Static candidates only. Top-level classes and ordinary unittest aliases/local '
                  'inheritance only; imported project bases, nested/dynamic classes, rebinding, decorators, '
                  'monkeypatches and synchronous signature collisions are not resolved. No findings is not '
                  'a clean bill of health. Targets are not imported or executed.')
    for path in sorted(root.rglob('*.py')):
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root):
            continue
        relative = str(path.relative_to(root))
        result['python_files'] += 1
        try:
            findings, unresolved = inspect_source(path.read_text())
        except (SyntaxError, UnicodeError, OSError) as error:
            result['parse_errors'].append(dict(path=relative, error=type(error).__name__))
            continue
        result['parsed_files'] += 1
        result['findings'].extend(dict(path=relative, **finding) for finding in findings)
        result['unresolved_classes'].extend(dict(path=relative, **item) for item in unresolved)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--output', type=Path, help='New JSON output file; existing files are refused')
    args = parser.parse_args()
    try:
        output = json.dumps(scan(args.root), indent=2) + '\n'
        if args.output:
            with args.output.open('x') as target:
                target.write(output)
        else:
            print(output, end='')
    except (ValueError, OSError) as error:
        parser.error(str(error))
