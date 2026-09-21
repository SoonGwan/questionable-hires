#!/usr/bin/env python3
"""Select named Python function regions from UTF-8 stdin without executing it."""
import argparse
import ast
import bisect
import hashlib
import io
import json
import re
import sys
import tokenize


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
    # Keep offsets, not copies of every line. Bound each excerpt before slicing:
    # overlapping large definitions must not allocate their full bodies first.
    offsets = [match.start() for match in re.finditer(r'[^\r\n]*(?:\r\n|\r|\n|$)', source)]
    matches = []
    remaining = 12000
    decorator_lines = None

    def definition_start(node):
        nonlocal decorator_lines
        if not node.decorator_list:
            return node.lineno
        # AST decorator locations describe the expression, not its opening @.
        # Tokenize lazily; logical-statement starts exclude matrix @ operators
        # and apparent decorators inside strings or continued expressions.
        if decorator_lines is None:
            decorator_lines = []
            statement_start = True
            with io.StringIO(source, newline=None) as stream:
                for token in tokenize.generate_tokens(stream.readline):
                    if token.type == tokenize.NEWLINE:
                        statement_start = True
                    elif token.type not in (tokenize.NL, tokenize.COMMENT,
                                            tokenize.INDENT, tokenize.DEDENT):
                        if statement_start and token.string == '@':
                            decorator_lines.append(token.start[0])
                        statement_start = False
        first_expression = min(d.lineno for d in node.decorator_list)
        index = bisect.bisect_right(decorator_lines, first_expression) - 1
        if index < 0:
            raise ValueError('Cannot locate the opening decorator token')
        return decorator_lines[index]

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.scope = []

        def generic_visit(self, node):
            # A Python expression cannot contain a class/function statement.
            # Keep statement containers (handlers, match cases, etc.) traversable,
            # but do not walk unrelated expression trees or decorator/default code.
            for child in ast.iter_child_nodes(node):
                if not isinstance(child, ast.expr):
                    self.visit(child)

        def visit_ClassDef(self, node):
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_FunctionDef(self, node):
            nonlocal remaining
            qualified = '.'.join([*self.scope, node.name])
            selected = [name for name in names if name in (node.name, qualified)]
            if selected:
                if len(matches) >= 20:
                    raise ValueError('More than 20 matches; select narrower qualified names')
                start = definition_start(node)
                first, end = offsets[start - 1], offsets[node.end_lineno]
                kept = min(end - first, remaining)
                matches.append(dict(name=qualified, selected_by=selected, start_line=start,
                                    end_line=node.end_lineno,
                                    text=source[first:first + kept],
                                    truncated=end - first > remaining))
                remaining -= kept
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

    Visitor().visit(tree)
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
