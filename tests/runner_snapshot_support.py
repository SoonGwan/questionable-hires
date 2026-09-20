"""Synthetic resources for scheduling tests, never historical/model evidence."""
from contextlib import contextmanager
from pathlib import Path
import subprocess
from unittest.mock import patch


@contextmanager
def controlled_bundle_git(runner, revision):
    """Exercise real snapshot-copy logic with explicitly synthetic Git objects."""
    skills = sorted({case['skill'] for case in runner.cases()})
    if len(skills) != 8:
        raise AssertionError('Expected all eight synthetic skill resources')
    objects, listing = {}, []
    for skill in skills:
        for suffix, mode, raw in (
            ('SKILL.md', '100644', f'---\nname: {skill}\ndescription: Synthetic schedule fixture\n---\n\nNot model evidence.\n'.encode()),
            ('assets/control.sh', '100755', b'# Synthetic fixture, never executed\n')):
            oid = f'unit-object-{len(objects)}'
            objects[oid] = raw
            listing.append(f'{mode} blob {oid}\tskills/{skill}/{suffix}')

    def git(*args):
        if args == ('ls-tree', '-r', revision, '--', 'skills'):
            return ('\n'.join(listing)+'\n').encode()
        if len(args)==3 and args[:2]==('cat-file','blob') and args[2] in objects:
            return objects[args[2]]
        if len(args)==2 and args[0]=='rev-parse' and args[1] in {revision,'HEAD'}:
            return ('unit-fixture-'+args[1]).encode()
        raise AssertionError('Unexpected Git dependency: '+repr(args))

    with patch.object(runner, 'git', side_effect=git):
        yield


def assert_pinned_bundle(test, root, directory, revision):
    """Compare real historical bytes/modes; caller must require_history first."""
    listing = subprocess.check_output(['git','ls-tree','-r',revision,'--','skills'], cwd=root).decode()
    expected = set()
    for line in listing.splitlines():
        metadata, name = line.split('\t',1)
        mode, kind, oid = metadata.split()
        test.assertEqual(kind, 'blob')
        raw = subprocess.check_output(['git','cat-file','blob',oid], cwd=root)
        test.assertEqual((directory/name).read_bytes(), raw)
        test.assertEqual((directory/name).stat().st_mode & 0o777, int(mode[-3:],8))
        expected.add(name)
    test.assertTrue(expected)
    test.assertEqual({p.relative_to(directory).as_posix() for p in (directory/'skills').rglob('*') if p.is_file()}, expected)


@contextmanager
def controlled_revision_labels(runner):
    revisions = set(runner.REVISIONS.values())
    def git(*args):
        if len(args) != 2 or args[0] != 'rev-parse' or args[1] not in revisions | {'HEAD'}:
            raise AssertionError('Unexpected Git dependency in schedule unit test: ' + repr(args))
        return ('unit-fixture-' + args[1]).encode()

    with patch.object(runner, 'git', side_effect=git):
        yield


@contextmanager
def controlled_resources(runner, skill, changed):
    revisions = set(runner.REVISIONS.values())

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

    with controlled_revision_labels(runner), patch.object(runner, 'snapshot', side_effect=snapshot):
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
