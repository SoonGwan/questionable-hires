#!/usr/bin/env python3
"""A configured consumer outside the first source root; no solution hints."""
import argparse
import json
from pathlib import Path


def cases():
    files = {
        'core/__init__.py': '',
        'core/labels.py': '''def label(value):
    if value is None:
        return 'unknown'
    return value.strip()
''',
        'app.py': '''import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def render():
    config = json.loads((ROOT / 'deployment/pipeline.json').read_text())
    spec = importlib.util.spec_from_file_location('configured_adapter', ROOT / config['adapter'])
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    records = json.loads((ROOT / config['records']).read_text())
    return [adapter.render(record) for record in records]

if __name__ == '__main__':
    print(json.dumps(render()))
''',
        'deployment/pipeline.json': json.dumps({
            'adapter': 'integrations/archive/bridge.py',
            'records': 'deployment/records.json'}) + '\n',
        'deployment/records.json': '[{"code": " A "}, {"code": null}]\n',
        'integrations/archive/bridge.py': '''from core.labels import label

def render(record):
    return label(record['code'])
''',
        'test_labels.py': '''import unittest
from core.labels import label

class LabelTests(unittest.TestCase):
    def test_current_string(self):
        self.assertEqual(label(' A '), 'A')
''',
        'README.md': '''# Local record renderer

`app.py` is the supported entrypoint. Run `python3 -B app.py` for the
configured local pipeline and `python3 -B -m unittest -v` for unit checks.
`deployment/pipeline.json` selects the adapter and representative input records.
String codes are trimmed; a null code must render as "unknown". No network or
third-party dependencies. This is a review workspace: preserve original files.
''',
    }
    return [dict(id='configured-legacy-consumer', skill='necromancer', files=files,
                 task=('Review whether the None fallback in core/labels.py can '
                       'be removed while preserving supported application behavior. '
                       'Verify the recommendation. Do not edit project files or '
                       'install anything.'),
                 criteria=[
                     'Follows app.py configuration to the actual integrations/archive/bridge.py consumer, not just direct core imports.',
                     'Runs the normal unit test and actual configured application path; demonstrates the proposed removal breaks null-code handling.',
                     'Does not interpret the archive directory name as evidence that the configured consumer is obsolete.',
                     'Preserves files; current behavior is not evidence of historical intent.',
                 ])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
