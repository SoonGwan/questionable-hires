import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ProbeAdoptionEvidenceTests(unittest.TestCase):
    def test_public_records_agree_without_private_logs_or_git_history(self):
        run = ROOT / 'benchmarks/results/probe-adoption-01'
        cases = ROOT / 'benchmarks/probe-adoption-cases.json'
        manifest = json.loads((run / 'run.json').read_text())
        self.assertEqual(manifest['cases_sha256'], hashlib.sha256(cases.read_bytes()).hexdigest())
        fixture = json.loads(cases.read_text())[0]['files']
        for arm in ('baseline', 'auto'):
            cell = run / ('two-write-faults--' + arm + '--1')
            events = [json.loads(line) for line in (cell / 'events.jsonl').read_text().splitlines()]
            commands = [event['item'] for event in events
                        if event.get('type') == 'item.completed'
                        and event.get('item', {}).get('type') == 'command_execution']
            self.assertEqual(commands, json.loads((cell / 'commands.json').read_text()))
            usage = [event['usage'] for event in events if event.get('type') == 'turn.completed']
            metadata = json.loads((cell / 'metadata.json').read_text())
            self.assertEqual(usage, [metadata['usage']])
            self.assertEqual(metadata['installed_resources_before'], metadata['installed_resources_after'])
            self.assertEqual(bool(metadata['installed_resources_before']), arm == 'auto')
            self.assertFalse((cell / 'changes.diff').read_text().strip())
            self.assertEqual({str(p.relative_to(cell / 'project')): p.read_text()
                              for p in (cell / 'project').rglob('*') if p.is_file()}, fixture)
            self.assertNotIn(' admin  staff ', (cell / 'events.jsonl').read_text())
            # Integrity only: matching records do not establish behavioral success.
