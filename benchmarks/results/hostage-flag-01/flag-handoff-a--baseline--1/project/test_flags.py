import unittest
from flags import read_flag
from worker import worker_options


class ExistingFlagTests(unittest.TestCase):
    def test_existing_true(self):
        self.assertIs(read_flag({"TRACE": "true"}, "TRACE"), True)

    def test_existing_missing(self):
        self.assertIs(read_flag({}, "TRACE"), False)


TRUE_VALUES = ("true", "yes", "on", "1")
FALSE_VALUES = ("false", "no", "off", "0")
INVALID_VALUES = ("", " ", "\t\r\n", "truthy", "falsey", "t", "f", "y", "n",
                  "2", "-1", "yes please", "o n", "none", "null")


def spellings(value):
    return (value, value.upper(), value.title(), " \t" + value.upper() + "\r\n")


class FlagContractTests(unittest.TestCase):
    def test_accepted_spellings_whitespace_and_case(self):
        for values, expected in ((TRUE_VALUES, True), (FALSE_VALUES, False)):
            for value in values:
                for spelling in spellings(value):
                    for default in (False, True):
                        with self.subTest(value=spelling, default=default):
                            self.assertIs(read_flag({"TRACE": spelling}, "TRACE", default),
                                          expected)

    def test_missing_and_none_with_both_defaults(self):
        for env in ({}, {"TRACE": None}):
            for default in (False, True):
                with self.subTest(env=env, default=default):
                    self.assertIs(read_flag(env, "TRACE", default), default)

    def test_invalid_and_blank_strings(self):
        for value in INVALID_VALUES:
            for default in (False, True):
                with self.subTest(value=value, default=default):
                    with self.assertRaises(ValueError):
                        read_flag({"TRACE": value}, "TRACE", default)

    def test_reads_requested_key_from_supplied_mapping(self):
        self.assertIs(read_flag({"TRACE": "true", "OTHER": "false"}, "OTHER"), False)
        self.assertIs(read_flag({"TRACE": "false", "OTHER": "true"}, "OTHER"), True)

    def test_mapping_preserved_on_return_and_error(self):
        for env in ({"OTHER": "untouched"},
                    *({"TRACE": value, "OTHER": "untouched"}
                      for value in (None, *TRUE_VALUES, *FALSE_VALUES, " YES ",
                                    " OFF ", *INVALID_VALUES))):
            for default in (False, True):
                with self.subTest(env=env, default=default):
                    before = env.copy()
                    try:
                        if env.get("TRACE") in INVALID_VALUES:
                            with self.assertRaises(ValueError):
                                read_flag(env, "TRACE", default)
                        else:
                            read_flag(env, "TRACE", default)
                    finally:
                        self.assertEqual(env, before)


class WorkerContractTests(unittest.TestCase):
    def test_accepted_spellings_whitespace_and_case(self):
        for values, expected in ((TRUE_VALUES, True), (FALSE_VALUES, False)):
            for value in values:
                for spelling in spellings(value):
                    with self.subTest(value=spelling):
                        env = {"TRACE": spelling, "OTHER": "untouched"}
                        before = env.copy()
                        result = worker_options(env)
                        self.assertEqual(result, {"trace": expected, "retries": 3})
                        self.assertIs(result["trace"], expected)
                        self.assertEqual(env, before)

    def test_missing_and_none_default_false(self):
        for env in ({"OTHER": "true"}, {"TRACE": None, "OTHER": "true"}):
            with self.subTest(env=env):
                before = env.copy()
                result = worker_options(env)
                self.assertEqual(result, {"trace": False, "retries": 3})
                self.assertIs(result["trace"], False)
                self.assertEqual(env, before)

    def test_invalid_and_blank_strings_propagate_without_mutation(self):
        for value in INVALID_VALUES:
            with self.subTest(value=value):
                env = {"TRACE": value, "OTHER": "untouched"}
                before = env.copy()
                try:
                    with self.assertRaises(ValueError):
                        worker_options(env)
                finally:
                    self.assertEqual(env, before)
