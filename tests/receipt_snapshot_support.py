"""Synthetic Git objects for Receipt copy/rewrite/scheduling tests only."""
from contextlib import ExitStack, contextmanager
from types import SimpleNamespace
from unittest.mock import patch

import receipt_read_candidate as reader
from receipt_route_candidate import ANCHOR, REFERENCE_SENTENCE


@contextmanager
def controlled_snapshots(runner=None):
    revisions = {reader.RESOURCE}
    if runner is not None and hasattr(runner, 'REVISIONS'):
        revisions.update(runner.REVISIONS.values())
    files = {
        'SKILL.md': ('100644', ('---\nname: receipt\ndescription: Synthetic fixture\n---\n\n'
                              + reader.BEFORE + '\n' + ANCHOR + '\n').encode()),
        'references/existing-fix.md': ('100644', ('Synthetic guide.' + REFERENCE_SENTENCE + '\n').encode()),
        'scripts/compare.py': ('100755', b'# Synthetic support, never executed\n'),
        'agents/openai.yaml': ('100644', b'interface: {}\n'),
    }
    objects = {str(i): raw for i, (_, raw) in enumerate(files.values())}
    listing = '\n'.join(f'{mode} blob {i}\tskills/receipt/{name}'
                        for i, (name, (mode, _)) in enumerate(files.items()))

    def git(*args):
        if (len(args) == 5 and args[:2] == ('ls-tree', '-r')
                and args[2] in revisions and args[3:] == ('--', 'skills/receipt')):
            return listing.encode()
        if len(args) == 3 and args[:2] == ('cat-file', 'blob') and args[2] in objects:
            return objects[args[2]]
        if len(args) == 2 and args[0] == 'rev-parse' and args[1] in revisions | {'HEAD'}:
            return ('unit-fixture-' + args[1]).encode()
        raise AssertionError('Unexpected synthetic Receipt Git request: ' + repr(args))

    def check_output(args, **kwargs):
        if args[0] != 'git':
            raise AssertionError('Only synthetic Git requests are supported')
        raw = git(*args[1:])
        return raw.decode() if kwargs.get('text') else raw

    with ExitStack() as stack:
        stack.enter_context(patch.object(reader, 'subprocess', SimpleNamespace(check_output=check_output)))
        if runner is not None:
            stack.enter_context(patch.object(runner, 'git', side_effect=git))
        yield
