import unittest
from settings.parser import parse
from checks.support import sample

class ParserTests(unittest.TestCase):
    def test_token_padding(self):
        self.assertEqual(parse(sample("token")), {"TOKEN": "abc=="})

    def test_query_value(self):
        self.assertEqual(parse(sample("query")), {"URL": "https://example.invalid/a?x=1&y=2"})

    def test_whitespace_and_comments(self):
        self.assertEqual(parse(sample("plain")), {"NAME": "Ada"})

    def test_empty_value(self):
        self.assertEqual(parse(sample("empty")), {"EMPTY": ""})

    def test_duplicate_last_wins(self):
        self.assertEqual(parse(sample("duplicate")), {"NAME": "last"})
