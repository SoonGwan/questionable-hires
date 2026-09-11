#!/usr/bin/env python3
"""Historical comparison across two cooperating implementation modules."""
import argparse
import json
from pathlib import Path


def cases():
    old_reader = '''from pathlib import Path

def read_parts(directory):
    return [p.read_text() for p in sorted(Path(directory).glob('part-*.txt'))]
'''
    reader = old_reader.replace("sorted(Path(directory).glob('part-*.txt'))",
                               "sorted(Path(directory).glob('part-*.txt'), key=lambda p: int(p.stem[5:]))")
    old_writer = "def render(parts, separator):\n    return separator.join(parts) + '\\n'\n"
    writer = old_writer.replace("return separator.join(parts) + '\\n'",
                                "return separator.join(parts) + '\\n' if parts else ''")
    files = {
        'assembly/__init__.py': '', 'assembly/reader.py': reader,
        'assembly/writer.py': writer,
        'assembly/service.py': '''import json
from pathlib import Path
from .reader import read_parts
from .writer import render

def assemble(directory):
    config = json.loads(Path('settings.json').read_text())
    return render(read_parts(directory), config['separator'])
''',
        'settings.json': '{"separator": "|"}\n',
        'samples/part-1.txt': 'one', 'samples/part-2.txt': 'two',
        'samples/part-10.txt': 'ten',
        'test_assembly.py': '''import tempfile
import unittest
from assembly.service import assemble

class AssemblyTests(unittest.TestCase):
    def test_numeric_order(self):
        self.assertEqual(assemble('samples'), 'one|two|ten\\n')
    def test_empty(self):
        with tempfile.TemporaryDirectory(dir='.') as empty:
            self.assertEqual(assemble(empty), '')
''',
        'README.md': ('Run python3 -B -m unittest -v test_assembly from the root. '
                      'Part names use nonnegative integer suffixes. Assemble in '
                      'numeric order with the configured separator and a final LF; '
                      'an empty directory produces an empty string. Standard library only.\n'),
    }
    before = dict(files, **{'assembly/reader.py': old_reader, 'assembly/writer.py': old_writer})
    return [dict(id='receipt-assembly-history', skill='receipt', files=files,
        history=[dict(message='Initial assembly package', files=before),
                 dict(message='Correct numeric ordering and empty output', files={
                     'assembly/reader.py': reader, 'assembly/writer.py': writer})],
        task=('Verify the committed assembly fix against the implementation before '
              'and after it, using the same current tests, configuration and samples. '
              'Exercise the documented runner and identify the implementation '
              'revisions actually loaded. Check numeric part ordering and empty '
              'output. Use disposable project-local copies; preserve original files '
              'and do not install anything or use external services.'),
        criteria=['Both cooperating implementation modules vary together; tests, settings and samples stay fixed.',
                  'Original ordering and empty-output assertions fail for their actual defects; both pass after.',
                  'Loaded copies/revisions and actual runner results are evidenced, not inferred from helper exit alone.',
                  'Original files remain unchanged and work stays project-local.'])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
