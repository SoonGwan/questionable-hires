#!/usr/bin/env python3
"""Author adaptation of frozen tests; does not rewrite model evidence."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

RESOURCE = 'e8ab180'
RESULT = 'benchmarks/results/hostage-keyed-import-01/'
PROJECT = RESULT + 'keyed-import--skill--1/project/'
TARGETS = {'test_duplicate_during_fetch_and_persist_then_retry',
           'test_other_keys_and_instances_proceed_independently'}


def frozen(path):
    return subprocess.check_output(['git', 'show', RESOURCE + ':' + path])


def adapt(source):
    tree = ast.parse(source)
    selected = []
    for function in ast.walk(tree):
        if isinstance(function, ast.AsyncFunctionDef) and function.name in TARGETS:
            candidates = [node for node in ast.walk(function) if isinstance(node, ast.With)]
            assert len(candidates) == 1
            node = candidates[0]
            call = node.items[0].context_expr
            assert len(node.items) == 1 and isinstance(call, ast.Call)
            assert isinstance(call.func, ast.Attribute) and call.func.attr == 'subTest'
            selected.append(node)
    assert len(selected) == 2
    lines = source.splitlines(keepends=True)
    for node in sorted(selected, key=lambda n: n.lineno, reverse=True):
        lines[node.lineno - 1:node.end_lineno] = [line[4:] if line.strip() else line
                                               for line in lines[node.lineno:node.end_lineno]]
    corrected = ''.join(lines)
    # All assertions, application calls, waits and cleanup code stay present.
    def calls(text):
        return [ast.dump(node, include_attributes=False) for node in ast.walk(ast.parse(text))
                if isinstance(node, ast.Call) and not
                (isinstance(node.func, ast.Attribute) and node.func.attr == 'subTest')]
    assert sorted(calls(source)) == sorted(calls(corrected))
    return corrected


def probe(scratch_root):
    names = ('importer.py', 'test_existing.py', 'test_importer.py', 'controlled_call.py', 'requirements.md')
    files = {name: frozen(PROJECT + name) for name in names}
    source = files['test_importer.py'].decode()
    corrected = adapt(source)
    variants = json.loads(frozen(RESULT + 'author-replay.json'))['checks']
    report = dict(kind='author-adapted native diagnostic control, not model evidence',
                  resource=RESOURCE, original_sha256={n: hashlib.sha256(b).hexdigest() for n, b in files.items()},
                  corrected_test_source=corrected, checks=[])
    for mode, test_source in [('original', source), ('dependent_phases_unwind', corrected)]:
        for variant in variants:
            with tempfile.TemporaryDirectory(prefix='phase-control-', dir=scratch_root) as temporary:
                project = Path(temporary).resolve()
                for name, content in files.items():
                    (project / name).write_bytes(content)
                (project / 'test_importer.py').write_text(test_source)
                (project / 'importer.py').write_text(variant['replacement_source'])
                try:
                    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'],
                                            cwd=project, capture_output=True, text=True, timeout=20)
                    output, code, timeout = result.stdout + result.stderr, result.returncode, False
                except subprocess.TimeoutExpired as error:
                    def text(value):
                        return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                    output, code, timeout = text(error.stdout) + text(error.stderr), None, True
                assert (project / 'test_importer.py').read_text() == test_source
                for name in names:
                    if name not in ('test_importer.py', 'importer.py'):
                        assert (project / name).read_bytes() == files[name]
                output = output.replace(str(project), '<CONTROL>').replace(str(Path.home()), '<HOME>')
                report['checks'].append(dict(mode=mode, variant=variant['variant'], exit_code=code,
                    expected_exit=variant['expected_exit'], timed_out=timeout,
                    matched=code == variant['expected_exit'] and not timeout and 'Ran 6 tests' in output,
                    secondary_unbound_error='UnboundLocalError' in output,
                    output=output, output_characters=len(output)))
    # These are explicit preconditions of the proposed correction, not a rescore.
    assert all(c['matched'] for c in report['checks'])
    assert sum(c['secondary_unbound_error'] for c in report['checks'] if c['mode'] == 'original') == 3
    assert not any(c['secondary_unbound_error'] for c in report['checks'] if c['mode'] != 'original')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scratch-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = probe(args.scratch_root)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for check in result['checks']:
        print(check['mode'], check['variant'], check['exit_code'],
              'secondary=', check['secondary_unbound_error'], 'characters=', check['output_characters'])
