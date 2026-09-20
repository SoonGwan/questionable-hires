from pathlib import Path
import re
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
from hostage_modes_candidate import snapshot
from run import resource_manifest


class HostageModesCandidateTests(unittest.TestCase):
    def test_resource_split_preserves_assets_metadata_and_links(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch:
            root=Path(scratch)
            snapshot(root/'original')
            snapshot(root/'candidate',candidate=True)
            old=resource_manifest(root/'original/skills')
            new=resource_manifest(root/'candidate/skills')
            added=set(new)-set(old)
            self.assertEqual(added,{'hostage-negotiator/references/stateful-changes.md'})
            self.assertEqual(set(old)-set(new),set())
            self.assertEqual({p for p in old if old[p]!=new[p]}, {'hostage-negotiator/SKILL.md'})
            for path in (root/'candidate/skills').rglob('*.md'):
                for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
                    self.assertTrue((path.parent/link.split('#')[0]).exists(),link)
            old_entry=(root/'original/skills/hostage-negotiator/SKILL.md').read_text()
            new_entry=(root/'candidate/skills/hostage-negotiator/SKILL.md').read_text()
            guide=(root/'candidate/skills/hostage-negotiator/references/stateful-changes.md').read_text()
            # A lossless relocation check, not evidence of model compliance.
            moved=old_entry[old_entry.index('For stateful behavior,'):old_entry.index('## Deliver and stop')]
            self.assertEqual(guide.split('\n\n',1)[1].replace('(../assets/','(assets/'),moved)
            self.assertEqual(new_entry.split('## Deliver and stop')[1],old_entry.split('## Deliver and stop')[1])
