"""Isolated native-runtime partition; no edits to the ordinary Receipt package."""
import ast
from pathlib import Path

CONSTANTS = ('NODE_OBSERVER', 'MODULE_BINDINGS', 'BOOTSTRAP', 'NATIVE_STARTUP', 'ASSERTION_WRAPPER')
FUNCTIONS = ('run_check', 'capture_check', 'run_node_check')


def transform(source):
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    regions = []
    extracted = []
    found = set()
    for node in tree.body:
        name = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in CONSTANTS:
                name = node.targets[0].id
        elif isinstance(node, ast.FunctionDef) and node.name in FUNCTIONS:
            name = node.name
        if name is None:
            continue
        found.add(name)
        text = ''.join(lines[node.lineno - 1:node.end_lineno])
        if name == 'run_check':
            text = text.replace('def run_check(python, root, recipe, timeout):',
                'def run_check(python, root, recipe, timeout, *, capture_check, read_limited, assertion_startup):', 1)
            replacement = '''def run_check(python, root, recipe, timeout):
    return _native['run_check'](python, root, recipe, timeout,
        capture_check=capture_check, read_limited=read_limited,
        assertion_startup=assertion_startup)
'''
        elif name == 'run_node_check':
            text = text.replace('def run_node_check(node, root, recipe, timeout):',
                'def run_node_check(node, root, recipe, timeout, *, capture_check):', 1)
            replacement = '''def run_node_check(node, root, recipe, timeout):
    return _native['run_node_check'](node, root, recipe, timeout, capture_check=capture_check)
'''
        else:
            replacement = ''
        extracted.append(text)
        regions.append((node.lineno - 1, node.end_lineno, replacement))
    if found != set(CONSTANTS + FUNCTIONS):
        raise ValueError('Unexpected Receipt runtime structure')
    for first, end, replacement in reversed(regions):
        lines[first:end] = [replacement]
    driver = ''.join(lines)
    anchor = 'MAX_GUARD_BYTES = 20_000_000\n'
    if driver.count(anchor) != 1:
        raise ValueError('Unexpected Receipt loader anchor')
    loader = '''
# Native process startup/capture lives beside the revision/copy/guard controller.
# run_path reads this installed source without adding sys.path or writing its pyc.
import runpy
_native = runpy.run_path(str(Path(__file__).with_name('native.py')))
'''+''.join(f'{name} = _native[{name!r}]\n' for name in CONSTANTS)+"capture_check = _native['capture_check']\n"
    driver = driver.replace(anchor, anchor + loader, 1)
    native = '''"""Receipt native Python/Node startup and bounded foreground execution.

Loaded by compare.py from this installed directory. Trusted package code, not a
sandbox. Copy the complete Receipt skill when installing or relocating it.
"""
import codecs
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import tempfile
import time

'''+ '\n\n'.join(extracted)
    compile(driver, 'compare.py', 'exec')
    compile(native, 'native.py', 'exec')
    return driver, native


def apply(skill):
    skill = Path(skill)
    path = skill / 'scripts/compare.py'
    driver, native = transform(path.read_text())
    (skill / 'scripts/native.py').write_text(native)
    path.write_text(driver)
    return {'compare_bytes': len(driver.encode()), 'native_bytes': len(native.encode())}
