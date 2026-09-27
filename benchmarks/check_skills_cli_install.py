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
            '    def test_inclusive_age(self): self.assertEqual(eligible(18), True)\n')
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
        assert 'AssertionError: False != True' in observed['checks']['before']['output']
        assert observed['comparison_copies_removed'] and observed['tree_guard']['unchanged']
        assert inventory(root) == original
        arguments = json.loads(run([sys.executable, '-I', '-B',
                                    str(installed / 'receipt/scripts/compare.py'),
                                    '--source', str(root), '--spec', '-'],
                                   input=json.dumps(dict(recipe, observe_assertions=True))))
        for phase, expected in [('before', 1), ('after', 0)]:
            check = arguments['checks'][phase]
            assert check['native_exit_code'] == check['exit_code'] == expected
            report = check['assertion_observation']
            assert report['v'] == 2 and report['complete'] and report['reason'] is None
            assert report['observations'] == [dict(method='assertEqual', actual=phase=='after',
                                                   expected=True, same_object=phase=='after')]
        assert arguments['comparison_copies_removed'] and arguments['tree_guard']['unchanged']
        assert inventory(root) == original
    return dict(receipt_assertion_format=2, receipt_actual_arguments_verified=True, named_regions_complete=True, missing_region_exit=1,
                receipt_native_before_exit=1, receipt_native_after_exit=0,
                receipt_original_tree_unchanged=True)


def exercise_audit_and_deadline(installed, project, run):
    """Check installed runtime assets through real child processes and assertions."""
    with tempfile.TemporaryDirectory(prefix='installed-audit-', dir=project) as folder:
        root = Path(folder)
        (root / 'service.py').write_text(
            'def save(values, value):\n    values.append(value)\n    return True\n')
        (root / 'test_service.py').write_text(
            'import unittest\nfrom service import save\nclass SaveTests(unittest.TestCase):\n'
            '    def test_acknowledges(self):\n        self.assertTrue(save([], "item"))\n')
        before = inventory(root)
        recipe = dict(files=['service.py', 'test_service.py'], imports=['service', 'test_service'],
            target='service.py', old='    values.append(value)\n', new='',
            runner='unittest', invocation='module', tests=['-v', 'test_service'],
            precheck='import service, test_service\nassert test_service.save is service.save\n',
            probe_replacements={'test_service.py':
                'import unittest\nfrom service import save\nclass SaveTests(unittest.TestCase):\n'
                '    def test_saved(self):\n        values = []\n'
                '        self.assertTrue(save(values, "item"))\n'
                '        self.assertEqual(values, ["item"])\n'},
            probe_tests=['-v', 'test_service'], guard_project=True)
        command = [sys.executable, '-I', '-B', str(installed / 'con-artist/scripts/audit.py'),
                   '--source', str(root), '--spec', '-']
        report = json.loads(run(command, input=json.dumps(recipe)))
        assert report['status'] == 'observed'
        expected = {'correct_tests': 0, 'mutant_tests': 0, 'correct_probe': 0, 'mutant_probe': 1}
        assert set(report['checks']) == set(expected)
        for phase, status in expected.items():
            check = report['checks'][phase]
            assert check['exit_code'] == check['native_exit_code'] == status, check
            assert check['command'][1:4] == ['-B', '-m', 'unittest']
            assert check['suite_observation']['tests'] == 1
            assert not check['timed_out'] and not check['output_truncated']
            assert 'Verified copied import: service ' in check['output']
        assert 'AssertionError: Lists differ:' in report['checks']['mutant_probe']['output']
        assert report['integrity']['project_guard']['unchanged']
        assert report['integrity']['owned_scratch_removed']
        rejected = json.loads(run(command, expected_exit=2, input=json.dumps(dict(recipe,
            precheck='import service, test_service\nassert test_service.save is not service.save\n'))))
        assert rejected['status'] == 'incomplete'
        assert set(rejected['checks']) == {'correct_tests'}
        assert rejected['checks']['correct_tests']['exit_code'] == 7
        assert inventory(root) == before
    deadline = [sys.executable, '-I', '-B', str(installed / 'exorcist/scripts/run_probe.py')]
    failed = json.loads(run([*deadline, '--timeout', '2', '--', sys.executable, '-I', '-B',
        '-c', 'import sys; print("native failure witnessed", flush=True); sys.exit(17)'], expected_exit=1))
    assert failed['exit_code'] == 17 and not failed['timed_out']
    assert failed['output'].strip() == 'native failure witnessed'
    assert failed['cleanup_complete'] and not failed['output_truncated']
    expired = json.loads(run([*deadline, '--timeout', '0.2', '--', sys.executable, '-I', '-B',
        '-c', 'import time; time.sleep(60)'], expected_exit=124))
    assert expired['timed_out'] and expired['cleanup_complete']
    assert expired['exit_code'] != 0
    return dict(audit_native_exits=expected, wrong_binding_incomplete_exit=7,
                audit_original_tree_unchanged=True, deadline_child_failure_exit=17,
                deadline_timeout_cli_exit=124, deadline_cleanup_complete=True)


def check(source, cli):
    names = sorted(p.parent.name for p in (source / 'skills').glob('*/SKILL.md'))
    assert len(names) == 8
    # The catalog README at skills/ is not part of an installable skill.
    source_before = inventory(source / 'skills')
    # The CLI excludes cache directories; still retain them in source_before
    # so the final integrity check detects changes to the owner's local cache.
    expected = {path: value for path, value in source_before.items()
                if path.split('/')[0] in names and '__pycache__' not in Path(path).parts[:-1]}
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
        # Receipt observer/preservation modules are APIs, not CLI entrypoints.
        scripts = sorted(p for p in installed.glob('*/scripts/*.py')
                         if p not in {installed / 'receipt/scripts/assertions.py',
                                      installed / 'receipt/scripts/preserve.py'})
        for script in scripts:
            help_text = run([sys.executable, '-I', '-B', str(script), '--help'])
            assert 'usage:' in help_text, 'No CLI help: ' + str(script)
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
        run([sys.executable, '-I', '-B', '-c', """
import pathlib, runpy, tempfile
api = runpy.run_path('.agents/skills/receipt/scripts/preserve.py')
with tempfile.TemporaryDirectory(dir='.') as temporary:
    root = pathlib.Path(temporary)
    source = root / 'owned.txt'
    source.write_text('before')
    with api['preserved_tree'](root) as report:
        assert source.read_text() == 'before'
    assert report['unchanged'] and report['file_bytes'] == len('before')
    try:
        with api['preserved_tree'](root):
            source.write_text('changed')
    except RuntimeError:
        assert source.read_text() == 'changed'
    else:
        raise AssertionError('mutation not detected')
print('installed preservation API unchanged/mutation controls passed')
"""])
        recent = exercise_recent_helpers(installed, project, run)
        audit_and_deadline = exercise_audit_and_deadline(installed, project, run)
        assert inventory(installed) == expected
        assert inventory(source / 'skills') == source_before
        report = dict(kind='local skills CLI copy and executable check; not remote/model evidence',
                      skills=names, installed_inventory=expected, python_entrypoints=len(scripts),
                      commands=commands, copied_bytes_and_modes_match=True, recent_helpers=recent,
                      audit_and_deadline=audit_and_deadline)
        text = json.dumps(report, indent=2)
        return text.replace(str(project), '<PROJECT>').replace(str(source), '<SOURCE>').replace(str(cli), '<CLI>')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--cli', type=Path, required=True)
    args = parser.parse_args()
    print(check(args.source.resolve(), args.cli.resolve()))
