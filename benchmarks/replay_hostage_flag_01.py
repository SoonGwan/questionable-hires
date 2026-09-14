#!/usr/bin/env python3
"""Audit retained native evidence and separately exercise actual flag tests."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from hostage_flag_cases import SOURCE, BROKEN, ORACLE
from replay_hostage_call_01 import inventory

REVISION = '094cc69445e14df2dbb57e4b36c7285ddfe62a94'
CASES_SHA = 'aab8a877f828a4df84a425862d6fc676aba8d183b91760348b5bb2bbd23a7574'
COMMAND = ['python3', '-B', '-m', 'unittest', 'discover', '-v']


def existing_class(source):
    return ast.dump(next(node for node in ast.parse(source).body
                        if isinstance(node, ast.ClassDef) and node.name == 'ExistingFlagTests'))


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['revision'] == REVISION and manifest['finished_at']
    frozen = subprocess.check_output(['git', 'show', REVISION + ':benchmarks/hostage-flag-cases.json'])
    assert hashlib.sha256(frozen).hexdigest() == manifest['cases_sha256'] == CASES_SHA
    cases = {c['id']: c for c in json.loads(frozen)}
    report = dict(kind='original artifact audit plus separate author controls', revision=REVISION,
                  cells=[], checks=[])
    assert len(list(run.glob('*--*'))) == 4
    for cell in sorted(run.glob('*--*')):
        meta = json.loads((cell / 'metadata.json').read_text())
        events = [json.loads(line) for line in (cell / 'stdout.original.jsonl').read_text().splitlines()]
        assert [e['usage'] for e in events if e.get('type') == 'turn.completed'] == [meta['usage']]
        assert meta['completed'] and not meta['timed_out'] and not meta['limit_detected']
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        project = cell / 'project'
        before = inventory(project)
        case = cases[meta['case']]
        for name in ('worker.py', 'requirements.md', 'notes.txt', 'verification/owner.txt'):
            assert (project / name).read_text() == case['files'][name]
        if meta['case'].endswith('b'):
            assert (project / 'flags.py').read_text() == case['files']['flags.py']
        assert existing_class((project / 'test_flags.py').read_text()) == existing_class(case['files']['test_flags.py'])
        commands = [e['item'] for e in events if e.get('type') == 'item.completed'
                    and e.get('item', {}).get('type') == 'command_execution']
        count = 8 if meta['arm'] == 'skill' else (10 if meta['case'].endswith('a') else 13)
        evidence = []
        for path in sorted(project.rglob('*')):
            if not path.is_file() or path.name not in ('output.txt', 'native-output.txt'):
                continue
            directory = path.parent
            argv = directory / ('argv.txt' if meta['arm'] == 'skill' else 'command.txt')
            recorded_command = argv.read_text().splitlines() if argv.name == 'argv.txt' else argv.read_text().split()
            assert recorded_command == COMMAND
            exit_path = directory / ('exit-code.txt' if path.name == 'native-output.txt' else 'exit.txt')
            code = int(exit_path.read_text())
            output = path.read_text()
            relative = str(directory.relative_to(project))
            expected_code = 1 if relative.startswith('verification/baseline-') else 0
            assert code == expected_code and re.findall(r'Ran (\d+) tests? in ', output) == [str(count)]
            # A successful final report must have been actually read, not just
            # created. The failed baseline intentionally inspected head/tail.
            reads = [i for i in commands if str(path.relative_to(project)) in i['command']]
            assert reads
            if code == 0:
                assert any(output in i.get('aggregated_output', '') for i in reads)
                assert '\nOK\n' in output
            else:
                assert 'FAILED (failures=124)' in output and 'AssertionError:' in output
            evidence.append(dict(directory=relative, exit_code=code, native_count=count,
                                 output_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                 observed_read_items=[i['id'] for i in reads]))
        assert len(evidence) == (2 if cell.name == 'flag-handoff-a--baseline--1' else 1)
        report['cells'].append(dict(cell=cell.name, usage=meta['usage'], seconds=meta['elapsed_seconds'],
                                   native_evidence=evidence, source_inventory=before))
        final = (project / 'flags.py').read_text()
        alternative = SOURCE.replace('raise ValueError("Invalid flag")', 'raise ValueError("Unsupported setting")')
        for variant, source in [('final', final), ('truthiness_fault', BROKEN),
                                ('valid_error_wording', alternative), ('oracle_final', final)]:
            with tempfile.TemporaryDirectory(prefix='author-flag-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                if variant == 'oracle_final':
                    scratch.mkdir()
                    (scratch / 'worker.py').write_text(case['files']['worker.py'])
                    (scratch / 'test_contract.py').write_text(ORACLE)
                else:
                    shutil.copytree(project, scratch)
                (scratch / 'flags.py').write_text(source)
                try:
                    result = subprocess.run([sys.executable, *COMMAND[1:]], cwd=scratch,
                                            capture_output=True, text=True, timeout=15)
                    code, output, timed_out = result.returncode, result.stdout + result.stderr, False
                except subprocess.TimeoutExpired as error:
                    def decode(value):
                        return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                    code, output, timed_out = None, decode(error.stdout) + decode(error.stderr), True
                expected = int(variant == 'truthiness_fault')
                expected_count = 5 if variant == 'oracle_final' else count
                unchanged = variant == 'oracle_final' or all((scratch / p).read_bytes() == (project / p).read_bytes()
                                                             for p in before if p != 'flags.py')
                matched = (code == expected and not timed_out and unchanged and
                           re.findall(r'Ran (\d+) tests? in ', output) == [str(expected_count)])
                if variant == 'truthiness_fault':
                    matched = matched and 'ValueError not raised' in output and 'True is not False' in output and 'ERROR:' not in output
                report['checks'].append(dict(cell=cell.name, variant=variant, exit_code=code,
                    expected_count=expected_count, matched=matched, timed_out=timed_out,
                    retained_sources_unchanged=unchanged, output=output.replace(str(scratch), '<REPLAY>')))
        assert inventory(project) == before
    report['original_projects_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite earlier observations')
    report = replay(args.run.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps([dict(cell=c['cell'], variant=c['variant'], matched=c['matched']) for c in report['checks']], indent=2))
