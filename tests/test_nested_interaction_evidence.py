import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class NestedInteractionEvidenceTests(unittest.TestCase):
    def test_export_reconciles_without_private_logs(self):
        run = ROOT / 'benchmarks/results/interaction-nested-01'
        cases = ROOT / 'benchmarks/interaction-nested-cases.json'
        manifest = json.loads((run / 'run.json').read_text())
        self.assertEqual(manifest['cases_sha256'], hashlib.sha256(cases.read_bytes()).hexdigest())
        originals = json.loads(cases.read_text())[0]['files']
        cells = {'nested-search-qa--' + arm + '--1' for arm in ('baseline', 'skill')}
        self.assertEqual(set(manifest['schedule']), cells)
        self.assertEqual(len(manifest['schedule']), 2)
        self.assertEqual({p.name for p in run.iterdir() if p.is_dir()}, cells)
        for arm, total in [('baseline', 84515), ('skill', 70416)]:
            cell = run / ('nested-search-qa--' + arm + '--1')
            events = [json.loads(line) for line in (cell / 'events.jsonl').read_text().splitlines()]
            commands = [e['item'] for e in events if e.get('type') == 'item.completed'
                        and e.get('item', {}).get('type') == 'command_execution']
            self.assertEqual(commands, json.loads((cell / 'commands.json').read_text()))
            meta = json.loads((cell / 'metadata.json').read_text())
            self.assertEqual([e['usage'] for e in events if e.get('type') == 'turn.completed'],
                             [meta['usage']])
            self.assertEqual(meta['usage']['input_tokens'] + meta['usage']['output_tokens'], total)
            self.assertEqual(meta['installed_resources_before'], meta['installed_resources_after'])
            self.assertEqual(bool(meta['installed_resources_before']), arm == 'skill')
            for name, content in originals.items():
                self.assertEqual((cell / 'project' / name).read_bytes(), content.encode())
            files = {str(p.relative_to(cell / 'project')) for p in (cell / 'project').rglob('*') if p.is_file()}
            self.assertEqual(files, set(originals) | {'apps/catalog/qa/test_search.py'})
            checks = [json.loads(c['aggregated_output']) for c in commands
                      if 'check.py --timeout 3 --' in c['command']]
            self.assertEqual(len(checks), 1)
            self.assertEqual(checks[0]['exit_code'], 1)
            self.assertFalse(checks[0]['timed_out'])
            self.assertFalse(checks[0]['output_truncated'])
            self.assertTrue(checks[0]['cleanup_complete'])
            # Integrity only; assertion correctness and coverage require review/replay.
