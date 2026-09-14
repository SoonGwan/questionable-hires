#!/usr/bin/env python3
"""Check a supplied skills CLI in a disposable project; never install globally."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise AssertionError('Expected --copy files, not symlinks: ' + str(path))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = {
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'mode': path.stat().st_mode & 0o777,
            }
    return result


def exercise_recent_helpers(installed, project, run):
    """Use installed CLIs, not imports from the source checkout."""
    selector = installed / 'necromancer/scripts/python_regions.py'
    source = 'raise RuntimeError("source must not execute")\nclass Service:\n    def value(self):\n        return 42\n'
    selected = json.loads(run([sys.executable, '-I', '-B', str(selector), '--name', 'Service.value'], input=source))
    assert selected['complete'] and len(selected['regions']) == 1
    assert selected['regions'][0]['text'] == '    def value(self):\n        return 42\n'
    missing = json.loads(run([sys.executable, '-I', '-B', str(selector), '--name', 'missing'],
                             input=source, expected_exit=1))
    assert not missing['complete'] and missing['missing_names'] == ['missing']
    with tempfile.TemporaryDirectory(prefix='receipt-native-', dir=project) as folder:
        root = Path(folder)
        def git(*args):
            return run(['git', '-C', str(root), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.invalid', '-c', 'commit.gpgSign=false',
                        '-c', 'core.hooksPath=/dev/null', *args])
        git('init', '-q')
        (root / 'rule.py').write_text('def eligible(age): return age > 18\n')
        (root / 'test_rule.py').write_text('import unittest\nfrom rule import eligible\n'
            'class Boundary(unittest.TestCase):\n'
            '    def test_inclusive_age(self): self.assertTrue(eligible(18))\n')
        git('add', 'rule.py', 'test_rule.py')
        git('commit', '-qm', 'before')
        (root / 'rule.py').write_text('def eligible(age): return age >= 18\n')
        git('add', 'rule.py')
        git('commit', '-qm', 'after')
        original = inventory(root)
        recipe = dict(fixed=['test_rule.py'], vary=['rule.py'], before='HEAD^', after='HEAD',
                      imports=['rule', 'test_rule'], runner='unittest', tests=['-v', 'test_rule'],
                      invocation='module', guard_tree=True)
        observed = json.loads(run([sys.executable, '-I', '-B',
                                   str(installed / 'receipt/scripts/compare.py'),
                                   '--source', str(root), '--spec', '-'], input=json.dumps(recipe)))
        assert set(observed['checks']) == {'before', 'after'}
        for phase, expected in [('before', 1), ('after', 0)]:
            check = observed['checks'][phase]
            assert check['exit_code'] == check['native_exit_code'] == expected, check
            assert check['provenance_ready'] and not check['timed_out'] and not check['output_truncated']
            assert 'test_inclusive_age' in check['output'] and 'Ran 1 test' in check['output']
        assert 'AssertionError: False is not true' in observed['checks']['before']['output']
        assert observed['comparison_copies_removed'] and observed['tree_guard']['unchanged']
        assert inventory(root) == original
    return dict(named_regions_complete=True, missing_region_exit=1,
                receipt_native_before_exit=1, receipt_native_after_exit=0,
                receipt_original_tree_unchanged=True)


def check(source, cli):
    names = sorted(p.parent.name for p in (source / 'skills').glob('*/SKILL.md'))
    assert len(names) == 8
    # The catalog README at skills/ is not part of an installable skill.
    source_before = inventory(source / 'skills')
    expected = {path: value for path, value in source_before.items() if path.split('/')[0] in names}
    commands = []
    with tempfile.TemporaryDirectory(prefix='skills-install-check-') as folder:
        project = Path(folder)

        def run(args, input=None, expected_exit=0):
            completed = subprocess.run(args, cwd=project, input=input, text=True, capture_output=True, timeout=30)
            commands.append({'command': args, 'exit_code': completed.returncode,
                             'stdin': input, 'expected_exit': expected_exit,
                             'stdout': completed.stdout, 'stderr': completed.stderr})
            assert completed.returncode == expected_exit, completed.stdout + completed.stderr
            return completed.stdout

        run(['node', str(cli), 'add', str(source), '--list'])
        assert not (project / '.agents').exists()
        run(['node', str(cli), 'add', str(source), '--agent', 'codex', '--skill', '*', '--copy', '-y'])
        installed = project / '.agents/skills'
        assert sorted(p.name for p in installed.iterdir()) == names
        actual = inventory(installed)
        assert actual == expected, dict(missing=sorted(expected.keys() - actual.keys()),
            extra=sorted(actual.keys() - expected.keys()),
            changed=sorted(path for path in expected.keys() & actual.keys() if expected[path] != actual[path]))
        scripts = sorted(installed.glob('*/scripts/*.py'))
        for script in scripts:
            run([sys.executable, '-I', '-B', str(script), '--help'])
        run([sys.executable, '-I', '-B', '-c', '''
import asyncio, runpy
api = runpy.run_path('.agents/skills/hostage-negotiator/assets/controlled_call.py')
async def check():
    callback = api['ControlledCall']()
    task = asyncio.create_task(callback('installed'))
    try:
        entry = await callback.started_before(task)
        assert entry.args == ('installed',)
        value = object()
        entry.complete(value)
        assert await task is value
    finally:
        if not task.done(): task.cancel()
        await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)
asyncio.run(check())
print('installed Python task-aware callback passed')
'''])
        run(['node', '--input-type=module', '-e', '''
import assert from 'node:assert/strict';
import { withControlledCalls } from './.agents/skills/hostage-negotiator/assets/controlled_call.mjs';
await withControlledCalls(async scope => {
  const save = scope.call(), value = {};
  const task = scope.run(() => save(value));
  const entry = await save.startedBefore(task);
  assert.equal(entry.args[0], value);
  entry.complete(value);
  assert.equal(await scope.wait(task), value);
});
console.log('installed JavaScript task-aware callback passed');
'''])
        recent = exercise_recent_helpers(installed, project, run)
        assert inventory(installed) == expected
        assert inventory(source / 'skills') == source_before
        report = dict(kind='local skills CLI copy and executable check; not remote/model evidence',
                      skills=names, installed_inventory=expected, python_entrypoints=len(scripts),
                      commands=commands, copied_bytes_and_modes_match=True, recent_helpers=recent)
        text = json.dumps(report, indent=2)
        return text.replace(str(project), '<PROJECT>').replace(str(source), '<SOURCE>').replace(str(cli), '<CLI>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--cli', type=Path, required=True)
    args = parser.parse_args()
    print(check(args.source.resolve(), args.cli.resolve()))
