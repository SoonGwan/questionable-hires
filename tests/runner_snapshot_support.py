"""Synthetic resources for scheduling tests, never historical/model evidence."""
from contextlib import contextmanager
from pathlib import Path
import subprocess
from unittest.mock import patch


@contextmanager
def controlled_resources(runner, skill, changed):
    revisions = set(runner.REVISIONS.values())
    def git(*args):
        if len(args) != 2 or args[0] != 'rev-parse' or args[1] not in revisions | {'HEAD'}:
            raise AssertionError('Unexpected Git dependency in schedule unit test: ' + repr(args))
        return ('unit-fixture-' + args[1]).encode()

    def snapshot(directory, revision):
        if revision not in revisions:
            raise AssertionError('Unknown synthetic resource revision')
        names = {skill + '/SKILL.md', *changed}
        for name in names:
            path = Path(directory) / 'skills' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            body = 'Synthetic schedule fixture; not executable skill evidence.\n'
            if name in changed:
                body += revision + '\n'
            path.write_text(body)

    with patch.object(runner, 'git', side_effect=git), patch.object(runner, 'snapshot', side_effect=snapshot):
        yield


def require_history(test, root, revisions):
    root = Path(root).resolve()
    if not (root / '.git').exists():
        test.skipTest('No project-owned Git history; synthetic schedule checks still run')
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root,
                            capture_output=True, text=True, timeout=10)
    test.assertEqual(result.returncode, 0, result.stderr)
    test.assertEqual(Path(result.stdout.strip()).resolve(), root)
    for revision in revisions:
        result = subprocess.run(['git', 'cat-file', '-e', revision + '^{commit}'],
                                cwd=root, capture_output=True, timeout=10)
        if result.returncode:
            test.skipTest('Pinned history absent; synthetic schedule checks still run')
