#!/usr/bin/env python3
"""Select named Python function regions from UTF-8 stdin without executing it."""
import argparse
import ast
import hashlib
import json
import re
import sys


def select_regions(raw, names):
    if not isinstance(raw, bytes) or len(raw) > 2_000_000:
        raise ValueError('Provide at most 2 MB of UTF-8 source bytes')
    if (not isinstance(names, (list, tuple)) or not 1 <= len(names) <= 10
            or any(not isinstance(name, str) or len(name) > 256
                   or not all(part.isidentifier() for part in name.split('.')) for name in names)):
        raise ValueError('Select 1–10 function names or qualified names')
    names = list(dict.fromkeys(names))
    source = raw.decode('utf-8')
    try:
        tree = ast.parse(source)
    except (SyntaxError, RecursionError) as error:
        raise ValueError('Source cannot be parsed by this Python runtime: ' + str(error)) from error
    # Python physical lines, not str.splitlines()'s extra Unicode separators.
    lines = re.findall(r'[^\r\n]*(?:\r\n|\r|\n|$)', source)
    matches = []

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.scope = []

        def visit_ClassDef(self, node):
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_FunctionDef(self, node):
            qualified = '.'.join([*self.scope, node.name])
            selected = [name for name in names if name in (node.name, qualified)]
            if selected:
                if len(matches) >= 20:
                    raise ValueError('More than 20 matches; select narrower qualified names')
                start = min([node.lineno] + [d.lineno for d in node.decorator_list])
                matches.append(dict(name=qualified, selected_by=selected, start_line=start,
                                    end_line=node.end_lineno,
                                    text=''.join(lines[start - 1:node.end_lineno])))
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

    Visitor().visit(tree)
    remaining = 12000
    for match in matches:
        text = match['text']
        match['truncated'] = len(text) > remaining
        match['text'] = text[:remaining]
        remaining -= len(match['text'])
    found = {name for match in matches for name in match['selected_by']}
    missing = [name for name in names if name not in found]
    features = sorted({alias.name for node in tree.body if isinstance(node, ast.ImportFrom)
                       and node.module == '__future__' for alias in node.names})
    return dict(complete=not missing and not any(m['truncated'] for m in matches),
                source_sha256=hashlib.sha256(raw).hexdigest(), source_bytes=len(raw),
                module_future_features=features, regions=matches, missing_names=missing,
                limitation='Static excerpts, not executable replacements or proof of runtime binding, '
                           'origin, or absence of relevant surrounding code. Hash identifies stdin, not a Git revision.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', action='append', required=True, help='Repeat; bare name matches all scopes, dotted name selects a scope')
    args = parser.parse_args()
    try:
        result = select_regions(sys.stdin.buffer.read(2_000_001), args.name)
    except (ValueError, RecursionError) as error:
        parser.exit(2, 'Source regions unavailable: ' + str(error) + '\n')
    print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    sys.exit(main())
