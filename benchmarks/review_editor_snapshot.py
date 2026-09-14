#!/usr/bin/env python3
"""Post-timing source checks and unchanged-suite counterfactual replays."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from editor_snapshot_cases import cases, EDITOR
from export import redact_paths


def review(run):
    fixtures = {case['id']: case for case in cases()}
    result = []
    for cell in sorted(run.glob('editor-snapshot-*--*--1')):
        meta = json.loads((cell / 'metadata.json').read_text())
        workspace = Path(meta['workspace'])
        files = fixtures[meta['case']]['files']
        source = (workspace / 'test_editor.py').read_text()
        methods = [n for n in ast.walk(ast.parse(source))
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name.startswith('test_')]
        original = next(n for n in ast.walk(ast.parse(files['test_editor.py']))
                        if isinstance(n, ast.AsyncFunctionDef) and n.name == 'test_initial_state')
        checks = dict(three_methods=len(methods) == 3,
                      initial_test_unchanged=any(ast.dump(n) == ast.dump(original) for n in methods),
                      other_originals_unchanged=all((workspace / name).read_bytes() == content.encode()
                          for name, content in files.items() if name != 'test_editor.py'),
                      installed_resources_unchanged=meta['installed_resources_before'] == meta['installed_resources_after'])
        paths = [p for p in workspace.rglob('*') if p.is_file()
                 and not set(p.relative_to(workspace).parts) & {'.git', '.agents', '__pycache__'}]
        inventory = sorted(p.relative_to(workspace).as_posix() for p in paths)
        events = [json.loads(line) for line in (cell / 'stdout.original.jsonl').read_text().splitlines()]
        usage_events = [e['usage'] for e in events if e['type'] == 'turn.completed']
        checks['usage_matches'] = usage_events == [meta.get('usage')]
        commands = [e['item'] for e in events if e['type'] == 'item.completed'
                    and e.get('item', {}).get('type') == 'command_execution']
        checks['allowed_file_inventory'] = all(name in files or name.endswith('.py') for name in inventory)
        replays = []
        with tempfile.TemporaryDirectory(prefix='editor-replay-', dir=Path(__file__).parent) as temporary:
            project = Path(temporary).resolve()
            for path in paths:
                target = project / path.relative_to(workspace)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(path.read_bytes())
            for variant in ('original', 'deep-snapshot'):
                (project / 'editor.py').write_text(EDITOR if variant == 'original' else EDITOR.replace(
                    'payload = dict(self.settings)', 'payload = deepcopy(self.settings)'))
                invocation = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_editor'],
                                            cwd=project, capture_output=True, text=True, timeout=10)
                replays.append(dict(variant=variant, exit_code=invocation.returncode,
                    stdout=invocation.stdout, stderr=invocation.stderr.replace(str(project), '<AUTHOR-COPY>')))
            checks['author_original_assertion_failure'] = (replays[0]['exit_code'] == 1
                and 'AssertionError:' in replays[0]['stderr'] and 'errors=' not in replays[0]['stderr']
                and 'Ran 3 tests' in replays[0]['stderr'])
            checks['author_deep_snapshot_three_passes'] = (replays[1]['exit_code'] == 0
                and 'Ran 3 tests' in replays[1]['stderr'] and 'OK' in replays[1]['stderr'])
        usage = meta.get('usage', {})
        result.append(dict(case=meta['case'], arm=meta['arm'], checks=checks,
            total_tokens=usage.get('input_tokens', 0) + usage.get('output_tokens', 0),
            elapsed_seconds=meta.get('elapsed_seconds'), shell_commands=len(commands),
            completed=meta.get('completed'), timed_out=meta.get('timed_out'),
            inventory=inventory, test_methods=[n.name for n in methods],
            test_sha256=hashlib.sha256(source.encode()).hexdigest(), replays=replays,
            transport_errors=[e for e in events if e['type'] == 'error']))
    return dict(results=result, python=sys.version,
                limitation='Separate author evidence, not original model execution. Inspect assertion paths, support and original tool responses before interpreting quality or cost. Bytecode directories are excluded from source inventory, not certified absent.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = review(args.run)
    with args.output.open('x') as stream:
        stream.write(redact_paths(json.dumps(result, indent=2), str(Path.cwd())) + '\n')
    print(json.dumps([{k: v for k, v in r.items() if k not in ('replays', 'inventory', 'test_methods')}
                      for r in result['results']], indent=2))
