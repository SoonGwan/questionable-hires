#!/usr/bin/env python3
"""Post-timing interval/final-only contract replay; never original model evidence."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from replay_mother_routing_01 import fingerprint


def replay(run, start_directories=None):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest.get('finished_at') and len(manifest['schedule']) == 4
    start_directories = start_directories or {}
    for cell, directory in start_directories.items():
        path = Path(directory)
        if cell not in manifest['schedule'] or path.is_absolute() or '..' in path.parts:
            raise ValueError('Test start directory must be project-relative for a scheduled cell')
    guarded = (run / 'search-protected--baseline--1/project/search.py').read_text()
    transient = guarded.replace('        self.generation = 0',
                                '        self.generation = 0\n        self.completed_generation = 0')
    transient = transient.replace('            self.result = result',
                                  '            self.result = result\n            self.completed_generation = generation')
    transient += ('        if generation < self.generation and self.completed_generation < self.generation:\n'
                  '            self.result = result\n')
    report = {'kind': 'separate post-timing author replay', 'checks': []}
    for case in ('search-protected', 'search-order'):
        for arm in ('baseline', 'skill'):
            project = run / f'{case}--{arm}--1' / 'project'
            before = fingerprint(project)
            control = 'transient' if case == 'search-protected' else 'guarded'
            for variant in ('original', control):
                with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                    scratch = Path(temporary) / 'project'
                    shutil.copytree(project, scratch, ignore=shutil.ignore_patterns('.agents', '.git', '__pycache__'))
                    if variant != 'original':
                        (scratch / 'search.py').write_text(transient if variant == 'transient' else guarded)
                    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-v']
                    start_directory = start_directories.get(f'{case}--{arm}--1')
                    if start_directory is not None:
                        if not (scratch / start_directory).is_dir():
                            raise ValueError('Test start directory does not exist')
                        command.extend(['-s', start_directory])
                    result = subprocess.run(command, cwd=scratch, text=True,
                                            capture_output=True, timeout=15)
                    evidence = (result.stdout + result.stderr).replace(str(scratch), '<REPLAY>').replace(
                        str(Path.home()), '<HOME>')
                    expected = int(variant == 'transient' or case == 'search-order' and variant == 'original')
                    ran_tests = 'Ran ' in evidence and 'Ran 0 tests' not in evidence
                    intended_failure = 'AssertionError' in evidence and 'FAILED (failures=' in evidence
                    assert not (scratch / '.agents').exists()
                    assert all((scratch / name).read_bytes() == (project / name).read_bytes()
                               for name in before if name.endswith('.py') and name != 'search.py'
                               and not name.startswith(('.agents/', '.git/')))
                    report['checks'].append({
                        'case': case, 'arm': arm, 'variant': variant,
                        'command': command,
                        'exit_code': result.returncode, 'expected_exit': expected,
                        'matched': result.returncode == expected and ran_tests
                                   and (not expected or intended_failure),
                        'production_source': (scratch / 'search.py').read_text(),
                        'output': evidence})
            assert fingerprint(project) == before
    report['original_projects_unchanged'] = True
    report['all_matched'] = all(c['matched'] for c in report['checks'])
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--test-start-directory', action='append', default=[],
                        metavar='CELL=DIR', help='Explicit retained test discovery location')
    args = parser.parse_args()
    start_directories = dict(entry.split('=', 1) for entry in args.test_start_directory)
    result = replay(args.run.resolve(), start_directories)
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps(result, indent=2))
