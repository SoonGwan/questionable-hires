import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'benchmarks/export.py'
spec = importlib.util.spec_from_file_location('privacy_export', SCRIPT)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class ExportPrivacyTests(unittest.TestCase):
    def test_account_directory_identity_is_redacted_after_home_placeholder(self):
        identity = '12345678-1234-4321-abcd-123456789012'
        data = {'hook': '<HOME>/Library/Application Support/orca/codex-accounts/'
                + identity + '/home/skills/tool/SKILL.md',
                'run_id': identity,
                'ordinary_path': 'fixtures/' + identity + '/input.json'}
        result = json.loads(exporter.redact_paths(json.dumps(data)))
        self.assertEqual(result['hook'], '<HOME>/Library/Application Support/orca/codex-accounts/<ACCOUNT>/home/skills/tool/SKILL.md')
        self.assertEqual(result['run_id'], identity)
        self.assertEqual(result['ordinary_path'], data['ordinary_path'])
        self.assertEqual(exporter.redact_paths(json.dumps(result)), json.dumps(result))

    def test_native_export_redacts_both_temp_shapes_without_eating_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, target = root / 'raw', root / 'public'
            cell = source / 'case--skill--1'
            project = cell / 'project'
            project.mkdir(parents=True)
            paths = ['/private/var/folders/fy/privateid/T/run/file.py',
                     '/private/var/fy/privateid/T/run/file.py',
                     '/var/fy/privateid/T/run/file.py',
                     '/tmp/qh-privateid/source/file.py',
                     '/private/tmp/qh-privateid/source/file.py']
            evidence = '\n'.join(paths) + '\nAssertionError: actual != expected\nRan 3 tests\n'
            (source / 'run.json').write_text(json.dumps({'note': paths[1], 'schedule': [cell.name]}))
            (cell / 'metadata.json').write_text(json.dumps({'workspace': '/synthetic/project', 'diagnostic': evidence}))
            event = {'type': 'item.completed', 'item': {'type': 'command_execution', 'id': 'item_1',
                     'command': 'python3 file.py', 'aggregated_output': evidence, 'exit_code': 1}}
            (cell / 'events.jsonl').write_text(json.dumps(event) + '\n')
            (cell / 'stderr.txt').write_text(evidence)
            (cell / 'changes.diff').write_text(evidence)
            (cell / 'initial.diff').write_text(evidence)
            (cell / 'answer.md').write_text('[malformed](' + paths[1] + ':1)\n[good](/synthetic/project/file.py:2)\n')
            (project / 'file.py').write_text('# safe source\n')
            (project / 'diagnostic.txt').write_text(evidence)
            before = {p.relative_to(source): p.read_bytes() for p in source.rglob('*') if p.is_file()}
            self.assertEqual(exporter.export(source, target), 1)
            for p in target.rglob('*'):
                if p.is_file():
                    text = p.read_text()
                    self.assertNotIn('privateid', text, str(p))
                    if p.suffix in ('.json', '.jsonl'):
                        for line in text.splitlines() if p.suffix == '.jsonl' else [text]:
                            json.loads(line)
            public = target / cell.name
            exported = json.loads((public / 'events.jsonl').read_text())['item']
            self.assertEqual(exported['aggregated_output'], '<TEMP>\n'*5 + 'AssertionError: actual != expected\nRan 3 tests\n')
            self.assertEqual(exported['exit_code'], 1)
            self.assertEqual((public / 'answer.md').read_text(), 'malformed\n[good](project/file.py#L2)\n')
            provenance = json.loads((public / 'source-sha256.json').read_text())
            self.assertEqual(provenance['events.jsonl'], hashlib.sha256(before[Path(cell.name) / 'events.jsonl']).hexdigest())
            self.assertEqual(before, {p.relative_to(source): p.read_bytes() for p in source.rglob('*') if p.is_file()})

    def test_qh_scratch_redaction_preserves_delimiters_and_unrelated_paths(self):
        raw = {'command': 'python /tmp/qh-privateid/run.py',
               'output': 'AssertionError\n/private/tmp/qh-privateid/log.txt\nactual=2 expected=3',
               'unrelated': '/tmp/application/input.txt',
               'relative': 'tmp/qh-relative/file.py'}
        observed = json.loads(exporter.redact_paths(json.dumps(raw)))
        self.assertEqual(observed['command'], 'python <TEMP>')
        self.assertEqual(observed['output'], 'AssertionError\n<TEMP>\nactual=2 expected=3')
        self.assertEqual(observed['unrelated'], raw['unrelated'])
        self.assertEqual(observed['relative'], raw['relative'])


if __name__ == '__main__':
    unittest.main()
