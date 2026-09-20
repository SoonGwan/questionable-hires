import hashlib
import json
from pathlib import Path
import unittest
from options import page_limit

# Preserve an audit of every native discovery invocation, including failures.
source = Path('options.py').read_bytes()
with Path('test-invocations.jsonl').open('a') as stream:
    stream.write(json.dumps({'source_sha256': hashlib.sha256(source).hexdigest(),
                             'zero_result': page_limit({'limit': 0})}) + '\n')

class PageLimitTests(unittest.TestCase):
    def test_missing_defaults(self):
        self.assertEqual(page_limit({}), 100)

    def test_none_defaults(self):
        self.assertEqual(page_limit({'limit': None}), 100)

    def test_zero_is_explicit(self):
        self.assertEqual(page_limit({'limit': 0}), 0)

    def test_positive_and_input_preservation(self):
        for value in (1, 7, 250):
            options = {'limit': value, 'owner': ['unchanged']}
            owner = options['owner']
            before = dict(options)
            self.assertEqual(page_limit(options), value)
            self.assertEqual(options, before)
            self.assertIs(options['owner'], owner)

if __name__ == '__main__':
    unittest.main()
