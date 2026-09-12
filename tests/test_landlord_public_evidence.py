"""Audit shipped evidence without private logs, Git history or model calls."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'benchmarks/results/landlord-compact-01'


class LandlordPublicEvidenceTests(unittest.TestCase):
    def test_export_preserves_usage_commands_and_fixture(self):
        fixture_path = ROOT / 'benchmarks/landlord-check-scope-cases.json'
        fixture = json.loads(fixture_path.read_text())[0]
        for arm in ('previous', 'candidate'):
            with self.subTest(arm=arm):
                run = json.loads((EVIDENCE/arm/'run.json').read_text())
                cell = EVIDENCE/arm/'store-check-scope--skill--1'
                meta = json.loads((cell/'metadata.json').read_text())
                events = [json.loads(line) for line in (cell/'events.jsonl').read_text().splitlines()]
                usage = [event['usage'] for event in events if event['type'] == 'turn.completed']
                self.assertEqual(usage, [meta['usage']])
                self.assertTrue(meta['completed'])
                self.assertFalse(meta['timed_out'])
                self.assertEqual(meta['exit_code'], 0)
                self.assertEqual(run['cases_sha256'], hashlib.sha256(fixture_path.read_bytes()).hexdigest())
                self.assertEqual(run['skill_snapshot_sha256']['landlord'], meta['skill_sha256'])
                self.assertEqual(meta['installed_resources_before'], meta['installed_resources_after'])
                commands = [event['item'] for event in events
                            if event['type'] == 'item.completed'
                            and event.get('item', {}).get('type') == 'command_execution']
                self.assertEqual(commands, json.loads((cell/'commands.json').read_text()))
                self.assertEqual(len(commands), 5)
                self.assertTrue(all(command['exit_code'] == 0 for command in commands))
                self.assertEqual((cell/'changes.diff').read_text().strip(), '')
                self.assertEqual({p.relative_to(cell/'project').as_posix()
                                  for p in (cell/'project').rglob('*') if p.is_file()},
                                 set(fixture['files']))
                for name, contents in fixture['files'].items():
                    self.assertEqual((cell/'project'/name).read_bytes(), contents.encode())


if __name__ == '__main__':
    unittest.main()
