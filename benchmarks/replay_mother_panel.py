#!/usr/bin/env python3
"""Author replay and provenance checks; never counted as measured model work."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from mother_panel_cases import FILES


def initial_test(source):
    tree = ast.parse(source)
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'PanelTests')
    method = next(node for node in cls.body if isinstance(node, ast.AsyncFunctionDef)
                  and node.name == 'test_initial_state')
    return ast.dump(method)


def replay(run, rename_helper=False):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest.get('finished_at') and len(manifest['schedule']) == 2
    report = {'kind': 'author replay, outside measured model sessions',
              'author_only_fail_helper_renamed': rename_helper, 'cells': []}
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        events = [json.loads(line) for line in (cell / 'stdout.original.jsonl').read_text().splitlines()]
        usage = next(event['usage'] for event in reversed(events) if event['type'] == 'turn.completed')
        assert usage == meta['usage'] and meta['completed'] and not meta['timed_out']
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        original_events = (cell / 'stdout.original.jsonl').read_text()
        assert original_events.replace(str(Path(meta['workspace']).resolve()), '<WORKSPACE>').replace(
            str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        project = cell / 'project'
        assert {str(p.relative_to(project)) for p in project.rglob('*') if p.is_file()} == set(FILES)
        for path, contents in FILES.items():
            if path != 'test_panel.py':
                assert (project / path).read_bytes() == contents.encode(), path
        tests = (project / 'test_panel.py').read_text()
        assert initial_test(tests) == initial_test(FILES['test_panel.py'])
        if rename_helper:
            assert tests.count('async def fail(') == 1
            tests = tests.replace('async def fail(', 'async def fail_request(').replace(
                'await self.fail(', 'await self.fail_request(')
        row = {'cell': name, 'total_tokens': usage['input_tokens'] + usage['output_tokens'],
               'elapsed_seconds': meta['elapsed_seconds'], 'originals_preserved': True,
               'initial_test_ast_preserved': True, 'usage_and_events_reconciled': True,
               'test_sha256': hashlib.sha256(tests.encode()).hexdigest(), 'replays': []}
        variants = {'correct': FILES['panel.py'],
                    'stale-guard-bypassed': FILES['panel.py'].replace('if request == self._request:', 'if True:'),
                    'view-cleared-at-start': FILES['panel.py'].replace('        self.loading = True\n',
                                                             '        self.loading = True\n        self.view = None\n')}
        for variant, source in variants.items():
            with tempfile.TemporaryDirectory(prefix='author-panel-', dir=run) as directory:
                scratch = Path(directory)
                for path, content in FILES.items():
                    (scratch / path).write_text(tests if path == 'test_panel.py' else
                                                source if path == 'panel.py' else content)
                process = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_panel'],
                                         cwd=scratch, text=True, capture_output=True, timeout=10)
                output = process.stdout + process.stderr
                assert 'Ran 5 tests' in output, output
                assert process.returncode == (0 if variant == 'correct' else 1), output
                # Preserve support errors too: a nominal green suite can shadow
                # unittest.fail and lose the intended diagnostic on faulty code.
                output = output.replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')
                row['replays'].append({'variant': variant, 'exit_code': process.returncode,
                                      'assertion_error_present': 'AssertionError' in output,
                                      'type_error_present': 'TypeError' in output,
                                      'output': output})
        report['cells'].append(row)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--rename-helper', action='store_true',
                        help='Author-only counterfactual; never change measured artifacts')
    args = parser.parse_args()
    result = replay(args.run.resolve(), args.rename_helper)
    with args.output.open('x') as target:
        json.dump(result, target, indent=2)
        target.write('\n')
    print(json.dumps([{k: v for k, v in cell.items() if k != 'replays'} for cell in result['cells']], indent=2))
