"""Unpromoted progressive-disclosure candidate; never edits installed skills."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = '79678f2'


def split_entry(entry):
    start = entry.index('For stateful behavior,')
    end = entry.index('## Deliver and stop', start)
    detail = entry[start:end]
    if detail.count('Without equivalent project support,') != 1:
        raise ValueError('Unexpected frozen source entry')
    route = ('For stateful or asynchronous behavior changes, read '
             '[state ownership and regression guidance](references/stateful-changes.md) '
             'alongside the affected code before designing the change or tests. '
             'Ordinary stateless edits do not need that reference.\n\n')
    guide = '# State ownership and regression checks\n\n' + detail.replace('(assets/', '(../assets/')
    return entry[:start] + route + entry[end:], guide


def snapshot(destination, candidate=False):
    destination = Path(destination)
    listing = subprocess.check_output(['git','ls-tree','-r',RESOURCE,'--','skills/hostage-negotiator'],cwd=ROOT,text=True)
    for line in listing.splitlines():
        info, name = line.split('\t',1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644','100755'):
            raise ValueError('Unsupported frozen resource')
        path = destination/name
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as stream:
            stream.write(subprocess.check_output(['git','cat-file','blob',oid],cwd=ROOT))
        path.chmod(int(mode[-3:],8))
    if candidate:
        entry = destination/'skills/hostage-negotiator/SKILL.md'
        body,guide = split_entry(entry.read_text())
        entry.write_text(body)
        with (entry.parent/'references/stateful-changes.md').open('x') as stream:
            stream.write(guide)
