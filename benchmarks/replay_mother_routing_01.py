#!/usr/bin/env python3
"""Separate author replay of unchanged standalone model tests; not model evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def fingerprint(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest.get('finished_at') and len(manifest['schedule']) == 4
    output = {'kind': 'post-timing author replay, not original model evidence', 'checks': []}
    for arm in ('baseline', 'skill'):
        project = run / f'search-protected--{arm}--1' / 'project'
        before = fingerprint(project)
        for variant in ('original', 'unguarded', 'transient'):
            with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch, ignore=shutil.ignore_patterns('.agents', '.git', '__pycache__'))
                source = scratch / 'search.py'
                text = source.read_text()
                assert text.count('if generation == self.generation:') == 1
                if variant == 'unguarded':
                    text = text.replace('if generation == self.generation:', 'if True:')
                if variant == 'transient':
                    text = text.replace('        self.generation = 0',
                                        '        self.generation = 0\n        self.completed_generation = 0')
                    text = text.replace('            self.result = result',
                                        '            self.result = result\n            self.completed_generation = generation')
                    text += ('        if generation < self.generation and self.completed_generation < self.generation:\n'
                             '            self.result = result\n')
                source.write_text(text)
                command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-v']
                result = subprocess.run(command, cwd=scratch, text=True, capture_output=True, timeout=15)
                evidence = (result.stdout + result.stderr).replace(str(scratch), '<REPLAY>').replace(
                    str(Path.home()), '<HOME>')
                expected = 0 if variant == 'original' or (variant == 'transient' and arm == 'skill') else 1
                assert result.returncode == expected, evidence
                assert 'Ran 0 tests' not in evidence and 'Ran ' in evidence, evidence
                if expected:
                    assert 'AssertionError' in evidence and 'FAILED (failures=' in evidence, evidence
                assert not (scratch / '.agents').exists()
                assert all((scratch / name).read_bytes() == (project / name).read_bytes()
                           for name in before if name.endswith('.py') and not name.startswith(('.agents/', '.git/'))
                           and name != 'search.py')
                output['checks'].append({'arm': arm, 'variant': variant, 'exit_code': result.returncode,
                                          'production_source': text, 'output': evidence})
        assert fingerprint(project) == before
    output['original_projects_unchanged'] = True
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = replay(args.run.resolve())
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps(result, indent=2))
