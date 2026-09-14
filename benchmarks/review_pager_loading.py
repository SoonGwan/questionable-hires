#!/usr/bin/env python3
"""Separate author replays/integrity checks; never replace original model evidence."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from export import redact_paths
from pager_loading_cases import PAGER, cases


def review(run):
    results = []
    files = cases()[0]['files']
    for cell in sorted(run.glob('pager-loading-regression--*--1')):
        meta = json.loads((cell / 'metadata.json').read_text())
        workspace = Path(meta['workspace'])
        inventory = sorted(p.relative_to(workspace).as_posix() for p in workspace.rglob('*')
                           if p.is_file() and not set(p.relative_to(workspace).parts) & {'.git', '.agents'})
        assert inventory == sorted(files), inventory
        for name, content in files.items():
            if name != 'test_pager.py':
                assert (workspace / name).read_bytes() == content.encode(), name
        source = (workspace / 'test_pager.py').read_text()
        tree = ast.parse(source)
        methods = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                   and n.name.startswith('test_')]
        assert len(methods) == 4
        original = next(n for n in ast.walk(ast.parse(files['test_pager.py']))
                        if isinstance(n, ast.AsyncFunctionDef) and n.name == 'test_single_success')
        retained = next(n for n in methods if n.name == original.name)
        assert ast.dump(original) == ast.dump(retained)
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        events = [json.loads(line) for line in (cell / 'stdout.original.jsonl').read_text().splitlines()]
        assert next(e['usage'] for e in events if e['type'] == 'turn.completed') == meta['usage']
        commands = [e['item'] for e in events if e['type'] == 'item.completed'
                    and e.get('item', {}).get('type') == 'command_execution']
        native = [c for c in commands if 'Ran 4 tests' in c.get('aggregated_output', '')]
        assert len(native) == 1 and native[0]['exit_code'] == 1
        assert native[0]['aggregated_output'].count('AssertionError: Tuples differ:') == 2
        rollout = json.loads((run / ('rollout-' + meta['arm']) / 'tool-records.json').read_text())
        assert not any(rollout[key] for key in ('missing_output_call_ids', 'unmatched_output_call_ids',
                                               'duplicate_call_ids', 'duplicate_output_call_ids'))
        tool_outputs = []
        for entry in rollout['records']:
            payload = entry['record']['payload']
            if not payload['type'].endswith('_output'):
                continue
            for block in payload['output']:
                try:
                    output = json.loads(block.get('text', ''))
                except json.JSONDecodeError:
                    continue
                if isinstance(output, dict) and 'output' in output:
                    tool_outputs.append(output)
        assert len(tool_outputs) == len(commands)
        for tool, command in zip(tool_outputs, commands):
            assert tool['output'] == command['aggregated_output']
            assert tool['exit_code'] == command['exit_code']
        replays = []
        with tempfile.TemporaryDirectory(prefix='pager-replay-', dir=Path(__file__).parent) as temporary:
            project = Path(temporary).resolve()
            for name in files:
                (project / name).write_bytes((workspace / name).read_bytes())
            for variant in ('original', 'guarded'):
                production = PAGER if variant == 'original' else PAGER.replace(
                    '        finally:\n            self.loading = False\n',
                    '        finally:\n            if generation == self._generation:\n                self.loading = False\n')
                (project / 'pager.py').write_text(production)
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_pager'],
                                        cwd=project, capture_output=True, text=True, timeout=10)
                assert result.returncode == (1 if variant == 'original' else 0), result.stderr
                assert 'Ran 4 tests' in result.stderr
                if variant == 'original':
                    assert result.stderr.count('AssertionError: Tuples differ:') == 2
                    assert 'FAILED (failures=2)' in result.stderr
                assert sorted(p.name for p in project.iterdir()) == sorted(files)
                replays.append(dict(variant=variant, exit_code=result.returncode, stdout=result.stdout,
                                    stderr=result.stderr.replace(str(project), '<AUTHOR-COPY>')))
        results.append(dict(arm=meta['arm'], total_tokens=meta['usage']['input_tokens'] + meta['usage']['output_tokens'],
                            elapsed_seconds=meta['elapsed_seconds'], shell_commands=len(commands),
                            tool_pairs=len(rollout['records']) // 2, original_native_runs=len(native),
                            test_names=[n.name for n in methods], original_inventory=inventory,
                            test_sha256=hashlib.sha256(source.encode()).hexdigest(), replays=replays,
                            transport_errors=[e for e in events if e['type'] == 'error']))
    return dict(results=results, python=sys.version,
                limitation='Author replay and integrity reconciliation, separate from model timing. Source inspection still required for assertion coverage; no broad performance claim.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = review(args.run)
    with args.output.open('x') as stream:
        stream.write(redact_paths(json.dumps(result, indent=2), str(Path.cwd())) + '\n')
    print(json.dumps([{k: v for k, v in r.items() if k not in ('replays', 'test_names', 'original_inventory')}
                      for r in result['results']], indent=2))
