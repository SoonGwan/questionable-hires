"""Isolated known-input read candidate; no runner/helper behavior changes."""
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
RESOURCE='ca668a4'
BEFORE=('Reuse supplied guidance; discover missing instructions only within authorized roots, '
        'never through an out-of-scope ancestor sweep. Report inaccessible evidence instead of broadening access.')
AFTER=('Read supplied paths, applicable project instructions and working-tree status together. '
       'List or search only unresolved paths; a known file does not need a preceding directory inventory. '
       'Include hidden instruction files when discovery is needed, within authorized roots only, '
       'never through an out-of-scope ancestor sweep. Report inaccessible evidence instead of broadening access.')


def revise(entry):
    if entry.count(BEFORE)!=1:
        raise ValueError('Unexpected frozen Receipt entry')
    return entry.replace(BEFORE,AFTER)


def snapshot(destination,candidate=False):
    listing=subprocess.check_output(['git','ls-tree','-r',RESOURCE,'--','skills/receipt'],cwd=ROOT,text=True)
    for line in listing.splitlines():
        metadata,name=line.split('\t',1)
        mode,kind,oid=metadata.split()
        if kind!='blob' or mode not in ('100644','100755'):
            raise ValueError('Unsupported frozen resource')
        path=Path(destination)/name
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as stream:
            stream.write(subprocess.check_output(['git','cat-file','blob',oid],cwd=ROOT))
        path.chmod(int(mode[-3:],8))
    if candidate:
        entry=Path(destination)/'skills/receipt/SKILL.md'
        entry.write_text(revise(entry.read_text()))
