#!/usr/bin/env python3
"""Read an explicit Python audit slice and its ancestor context; never import it."""

import argparse
import ast
import hashlib
import json
from pathlib import Path
import stat
import sys


MAX_FILE = 256_000
MAX_INPUT = 2_000_000
MAX_OUTPUT = 100_000
FULL_SOURCE_LINES = 200
CONFIGS = ('pytest.ini', '.pytest.ini', 'pyproject.toml', 'tox.ini', 'setup.cfg')
DEFINITIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)


def checked(root, relative):
    path = Path(relative)
    if path.is_absolute() or not path.parts or '..' in path.parts or '.git' in path.parts:
        raise ValueError('Expected a project-relative path without traversal or Git internals')
    if len(path.parts) > 32:
        raise ValueError('Path nesting exceeds 32 components')
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError('Symlinks are not supported: ' + str(path))
    return current


def read(root, path, budget):
    source = checked(root, path)
    info = source.stat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_FILE:
        raise ValueError('Expected a regular file of at most 256000 bytes: ' + str(path))
    if budget[0] + info.st_size > MAX_INPUT:
        raise ValueError('Selected context exceeds 2000000 input bytes')
    with source.open('rb') as stream:
        data = stream.read(MAX_FILE + 1)
    if len(data) > MAX_FILE:
        raise ValueError('File exceeded read limit: ' + str(path))
    budget[0] += len(data)
    if budget[0] > MAX_INPUT:
        raise ValueError('Selected context exceeds 2000000 input bytes')
    return data.decode('utf-8'), hashlib.sha256(data).hexdigest()


def span(node):
    decorators = getattr(node, 'decorator_list', [])
    return min([node.lineno] + [d.lineno for d in decorators]), node.end_lineno


def excerpt(lines, first, last):
    return '\n'.join(f'{i}: {lines[i - 1]}' for i in range(first, last + 1))


def definition_index(body, source, prefix=''):
    records = []
    for node in body:
        if not isinstance(node, DEFINITIONS):
            continue
        first, last = span(node)
        name = prefix + node.name
        records.append(dict(name=name, kind=type(node).__name__, first_line=first,
                            last_line=last, decorators=[ast.get_source_segment(source, d)
                                                        for d in node.decorator_list]))
        if isinstance(node, ast.ClassDef):
            records.extend(definition_index(node.body, source, name + '.'))
    return records


def describe(root, path, budget, symbol=None, index=False, auto_index=False):
    source, digest = read(root, path, budget)
    lines = source.splitlines()
    result = dict(path=str(path), sha256=digest)
    large_selected = auto_index and Path(path).suffix == '.py' and len(lines) > FULL_SOURCE_LINES and not symbol
    index = index or large_selected
    if symbol or index:
        tree = ast.parse(source, filename=str(path))
        if symbol:
            body = tree.body
            for name in symbol.split('.'):
                matches = [n for n in body if isinstance(n, DEFINITIONS) and n.name == name]
                if len(matches) != 1:
                    raise ValueError('Missing or ambiguous definition: ' + str(path) + ':' + symbol)
                node = matches[0]
                body = node.body
            first, last = span(node)
            result.update(representation='definition', symbol=symbol, source=excerpt(lines, first, last))
            result['limitation'] = 'Definition excerpt only; imports, globals, bases and runtime bindings are not resolved.'
        else:
            definitions, top_level = definition_index(tree.body, source), []
            for node in tree.body:
                first, last = span(node)
                if not isinstance(node, DEFINITIONS):
                    top_level.append(excerpt(lines, first, last))
            result.update(representation='definition_index', bodies_omitted=True,
                          definitions=definitions, top_level=top_level,
                          limitation='Static index only; definition/class bodies are omitted, not reviewed. Inspect relevant definitions, fixtures, hooks and plugins before execution. Conditional definitions remain in top_level; runtime bindings are unresolved.')
            if large_selected:
                result['reason'] = 'Selected Python file exceeds 200 lines; use file:qualified.definition or --full to read bodies. No behavioral conclusion is established by this index.'
                full_result = dict(path=str(path), sha256=digest, representation='full_source',
                                   source=excerpt(lines, 1, len(lines)))
                if len(json.dumps(result, ensure_ascii=False)) >= len(json.dumps(full_result, ensure_ascii=False)):
                    return full_result
    else:
        result['representation'] = 'full_source'
        result['source'] = excerpt(lines, 1, len(lines))
    return result


def collect(root, selectors, full=False):
    root = Path(root).resolve(strict=True)
    if not root.is_dir() or not 1 <= len(selectors) <= 8:
        raise ValueError('Provide a project directory and 1–8 file[:qualified.definition] selectors')
    selected, directories = [], {Path('.')}
    budget = [0]
    for selector in selectors:
        path_text, separator, symbol = selector.partition(':')
        path = Path(path_text)
        checked(root, path)
        if separator and (not symbol or not all(s.isidentifier() for s in symbol.split('.'))):
            raise ValueError('Expected a dotted Python definition name')
        selected.append((path, symbol if separator else None))
        directories.update(path.parents)
    ordered = sorted(directories, key=lambda p: (len(p.parts), p.as_posix()))
    instructions, configs, conftests, checked_instructions = [], [], [], []
    for directory in ordered:
        for name in ('AGENTS.md', 'AGENTS.override.md', *CONFIGS, 'conftest.py'):
            relative = directory / name
            candidate = checked(root, relative)
            if name.startswith('AGENTS'):
                checked_instructions.append(str(relative))
            if not candidate.exists():
                continue
            record = describe(root, relative, budget, index=name == 'conftest.py')
            if name.startswith('AGENTS'):
                instructions.append(record)
            elif name == 'conftest.py':
                conftests.append(record)
            else:
                configs.append(record)
    result = dict(status='collected', instructions=instructions,
                  instruction_paths_checked=checked_instructions, configs=configs,
                  conftest_indexes=conftests,
                  selected=[describe(root, path, budget, symbol, auto_index=not full) for path, symbol in selected],
                  limitation='Read-only navigation, not execution or complete dependency/config discovery. Only selected-path ancestors inside the supplied root are checked. Host instructions still apply; inspect additional dependencies when needed. Files must remain stable while reading.')
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if len(encoded) > MAX_OUTPUT:
        raise ValueError('Context exceeds 100000 characters; narrow selectors or use project tools. No partial context emitted.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--full', action='store_true',
                        help='Return full selected files instead of indexing Python files over 200 lines; size limits still apply')
    parser.add_argument('selectors', nargs='+', metavar='FILE[:DEFINITION]')
    args = parser.parse_args()
    try:
        result = collect(args.root, args.selectors, full=args.full)
    except (OSError, ValueError, SyntaxError, RecursionError) as error:
        print(json.dumps(dict(status='incomplete', error=str(error))), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
