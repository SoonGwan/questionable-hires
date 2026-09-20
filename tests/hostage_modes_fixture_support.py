"""Synthetic Git objects for rejected mode-candidate tests, not model evidence."""
from contextlib import ExitStack, contextmanager
from types import SimpleNamespace
from unittest.mock import patch
import hostage_modes_candidate as candidate

ENTRY = '''---
name: hostage-negotiator
description: Synthetic resource-copy fixture
---

# Synthetic entry

Keep the requested behavior.

For stateful behavior, preserve ownership.
Without equivalent project support, read [support](assets/controlled_call.py).

## Deliver and stop

Keep [native evidence](references/native-evidence.md).
'''


@contextmanager
def controlled_modes(runner=None):
    revision = 'unit-fixture-hostage-modes'
    files = {
        'SKILL.md': ('100644', ENTRY.encode()),
        'assets/controlled_call.py': ('100755', b'# Synthetic support; never executed\n'),
        'references/native-evidence.md': ('100644', b'# Synthetic evidence guide\n'),
        'agents/openai.yaml': ('100644', b'interface: {}\n'),
    }
    objects = {str(i):raw for i,(_,raw) in enumerate(files.values())}
    listing = '\n'.join(f'{mode} blob {i}\tskills/hostage-negotiator/{name}'
                        for i,(name,(mode,_)) in enumerate(files.items()))+'\n'

    def check_output(args, **kwargs):
        if args == ['git','ls-tree','-r',revision,'--','skills/hostage-negotiator']:
            result = listing.encode()
        elif len(args)==4 and args[:3]==['git','cat-file','blob'] and args[3] in objects:
            result = objects[args[3]]
        elif args == ['git','rev-parse','HEAD']:
            result = b'unit-fixture-launch\n'
        else:
            raise AssertionError('Unexpected synthetic Git command: '+repr(args))
        return result.decode() if kwargs.get('text') else result

    with ExitStack() as stack:
        stack.enter_context(patch.object(candidate,'RESOURCE',revision))
        stack.enter_context(patch.object(candidate,'subprocess',SimpleNamespace(check_output=check_output)))
        if runner is not None:
            stack.enter_context(patch.object(runner,'RESOURCE',revision))
            stack.enter_context(patch.object(runner,'subprocess',SimpleNamespace(check_output=check_output)))
        yield
