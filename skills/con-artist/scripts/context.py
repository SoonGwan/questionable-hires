#!/usr/bin/env python3
"""Read an explicit Python audit slice and its ancestor context; never import it."""

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
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
    # Validate the opened object, not only the path inspected above. Nonblocking
    # open prevents a raced FIFO from waiting for a writer on supported systems.
    flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_BINARY', 0)
    descriptor = os.open(source, flags)
    with os.fdopen(descriptor, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino)):
            raise ValueError('Selected file changed while opening: ' + str(path))
        if opened.st_size > MAX_FILE or budget[0] + opened.st_size > MAX_INPUT:
            raise ValueError('Opened file exceeds context read budget: ' + str(path))
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


def physical_lines(source):
    # Python line numbers recognize LF, CRLF and CR, not all Unicode separators
    # accepted by str.splitlines(). Keep those characters inside source literals.
    lines = source.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    if lines[-1] == '':
        lines.pop()
    return lines


def definition_spans(tree):
    records = []
    def visit(node, prefix=''):
        if isinstance(node, DEFINITIONS):
            name = prefix + node.name
            first, last = span(node)
            records.append((first, last, name, node))
            prefix = name + '.'
        for child in ast.iter_child_nodes(node):
            # Expressions cannot contain definition statements. Traversing a
            # deeply nested value must not break an unrelated source selector.
            if not isinstance(child, ast.expr):
                visit(child, prefix)
    visit(tree)
    return records


def definition_at_line(tree, line, spans=None):
    if spans is None:
        spans = definition_spans(tree)
    matches = [(last - first, name, node) for first, last, name, node in spans
               if first <= line <= last]
    if not matches:
        raise ValueError('Line is outside a Python definition; select the full file for module context')
    matches.sort(key=lambda item: item[0])
    if len(matches) > 1 and matches[0][0] == matches[1][0]:
        raise ValueError('Line has ambiguous enclosing definitions')
    return matches[0][1:]


def definition_index(body, source, prefix='', segments=None):
    # AST columns are UTF-8 byte offsets. Split Python physical lines once,
    # retaining original terminators; str.splitlines also splits literal data.
    if segments is None:
        segments = re.findall(rb'[^\r\n]*(?:\r\n|\r|\n|$)', source.encode('utf-8'))
    def decorator_source(node):
        first, last = node.lineno - 1, node.end_lineno - 1
        if first == last:
            return segments[first][node.col_offset:node.end_col_offset].decode('utf-8')
        return (segments[first][node.col_offset:] + b''.join(segments[first+1:last]) +
                segments[last][:node.end_col_offset]).decode('utf-8')
    records = []
    for node in body:
        if not isinstance(node, DEFINITIONS):
            continue
        first, last = span(node)
        name = prefix + node.name
        records.append(dict(name=name, kind=type(node).__name__, first_line=first,
                            last_line=last, decorators=[decorator_source(d)
                                                        for d in node.decorator_list]))
        if isinstance(node, ast.ClassDef):
            records.extend(definition_index(node.body, source, name + '.', segments))
    return records


def scope_definitions(body):
    """Yield static definitions through control flow, but not nested scopes."""
    for node in body:
        if isinstance(node, DEFINITIONS):
            yield node
        elif not isinstance(node, ast.expr):
            yield from scope_definitions(ast.iter_child_nodes(node))


def describe(root, path, budget, symbol=None, index=False, auto_index=False, cache=None):
    # Invocation-local only: multiple excerpts must share the same source bytes.
    if cache is None:
        cache = {}
    if path not in cache:
        source, digest = read(root, path, budget)
        cache[path] = dict(source=source, digest=digest, lines=physical_lines(source))
    snapshot = cache[path]
    source, digest, lines = snapshot['source'], snapshot['digest'], snapshot['lines']
    result = dict(path=str(path), sha256=digest)
    large_selected = auto_index and Path(path).suffix == '.py' and len(lines) > FULL_SOURCE_LINES and not symbol
    index = index or large_selected
    if symbol or index:
        if 'tree' not in snapshot:
            snapshot['tree'] = ast.parse(source, filename=str(path))
        tree = snapshot['tree']
        if symbol:
            if isinstance(symbol, int):
                if symbol > len(lines):
                    raise ValueError('Selected line exceeds file length: ' + str(path))
                result['requested_line'] = symbol
                if 'definition_spans' not in snapshot:
                    snapshot['definition_spans'] = definition_spans(tree)
                symbol, node = definition_at_line(tree, symbol, snapshot['definition_spans'])
            else:
                body = tree.body
                scopes = snapshot.setdefault('scope_names', {})
                for name in symbol.split('.'):
                    key = id(body)  # The parsed tree owns these lists for this snapshot.
                    if key not in scopes:
                        names = {}
                        for definition in scope_definitions(body):
                            names.setdefault(definition.name, []).append(definition)
                        scopes[key] = names
                    matches = scopes[key].get(name, [])
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
                          limitation='Static index only; definition/class bodies are omitted, not reviewed. Inspect relevant definitions, fixtures, hooks and plugins before execution. Module-level conditional definitions remain in top_level; conditions inside class bodies are omitted. Runtime bindings are unresolved.')
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


def encode(result, pretty=False):
    return json.dumps(result, ensure_ascii=False, indent=2 if pretty else None,
                      separators=None if pretty else (',', ':'))


def collect(root, selectors, full=False, *, pretty=False):
    root = Path(root).resolve(strict=True)
    if not root.is_dir() or not 1 <= len(selectors) <= 8:
        raise ValueError('Provide a project directory and 1–8 file[:definition-or-line] selectors')
    selected, directories = [], {Path('.')}
    budget = [0]
    cache = {}
    for selector in selectors:
        path_text, separator, symbol = selector.partition(':')
        path = Path(path_text)
        checked(root, path)
        if separator:
            if symbol.isascii() and symbol.isdecimal() and len(symbol) <= 6 and str(int(symbol)) == symbol and int(symbol) > 0:
                symbol = int(symbol)
            elif not symbol or not all(s.isidentifier() for s in symbol.split('.')):
                raise ValueError('Expected a dotted Python definition name or positive canonical line number')
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
            record = describe(root, relative, budget, index=name == 'conftest.py', cache=cache)
            if name.startswith('AGENTS'):
                instructions.append(record)
            elif name == 'conftest.py':
                conftests.append(record)
            else:
                configs.append(record)
    result = dict(status='collected', instructions=instructions,
                  instruction_paths_checked=checked_instructions, configs=configs,
                  conftest_indexes=conftests,
                  selected=[describe(root, path, budget, symbol, auto_index=not full, cache=cache) for path, symbol in selected],
                  limitation='Read-only navigation, not execution or complete dependency/config discovery. Only selected-path ancestors inside the supplied root are checked. Host instructions still apply; inspect additional dependencies when needed. Files must remain stable while reading.')
    if len(encode(result, pretty)) + 1 > MAX_OUTPUT:  # CLI's terminating newline
        raise ValueError(f'Context exceeds {MAX_OUTPUT} characters; narrow selectors or use project tools. No partial context emitted.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--full', action='store_true',
                        help='Return full selected files instead of indexing Python files over 200 lines; size limits still apply')
    parser.add_argument('--pretty', action='store_true',
                        help='Indent JSON for manual inspection; default JSON is compact with identical values')
    parser.add_argument('selectors', nargs='+', metavar='FILE[:DEFINITION_OR_LINE]')
    args = parser.parse_args()
    try:
        result = collect(args.root, args.selectors, full=args.full, pretty=args.pretty)
    except (OSError, ValueError, SyntaxError, RecursionError) as error:
        print(json.dumps(dict(status='incomplete', error=str(error))), file=sys.stderr)
        return 2
    print(encode(result, args.pretty))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
