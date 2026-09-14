import unittest
from flags import read_flag
from worker import worker_options


class ExistingFlagTests(unittest.TestCase):
    def test_existing_true(self):
        self.assertIs(read_flag({"TRACE": "true"}, "TRACE"), True)

    def test_existing_missing(self):
        self.assertIs(read_flag({}, "TRACE"), False)


class FlagContractTests(unittest.TestCase):
    def test_accepted_spellings_case_and_whitespace(self):
        for expected, spellings in (
            (True, ("true", "yes", "on", "1")),
            (False, ("false", "no", "off", "0")),
        ):
            for spelling in spellings:
                for value in (spelling, spelling.upper(),
                              " \t" + spelling.title() + "\r\n"):
                    for default in (False, True):
                        with self.subTest(value=value, default=default):
                            env = {"CUSTOM": value, "TRACE": "invalid"}
                            before = env.copy()
                            self.assertIs(read_flag(env, "CUSTOM", default), expected)
                            self.assertEqual(env, before)

    def test_missing_and_none_with_both_defaults(self):
        for default in (False, True):
            for env in ({"OTHER": "yes"}, {"CUSTOM": None, "OTHER": "yes"}):
                with self.subTest(env=env, default=default):
                    before = env.copy()
                    self.assertIs(read_flag(env, "CUSTOM", default), default)
                    self.assertEqual(env, before)

    def test_invalid_and_blank_strings(self):
        for value in ("", " \t\r\n", "maybe", "2", "-1", "t", "f", "y", "n",
                      "enabled", "disabled", "none", "null", "true false", "o n"):
            for default in (False, True):
                with self.subTest(value=value, default=default):
                    env = {"CUSTOM": value, "OTHER": "keep"}
                    before = env.copy()
                    with self.assertRaises(ValueError):
                        read_flag(env, "CUSTOM", default)
                    self.assertEqual(env, before)

    def test_worker_accepted_values(self):
        for expected, spellings in (
            (True, ("true", "yes", "on", "1")),
            (False, ("false", "no", "off", "0")),
        ):
            for spelling in spellings:
                with self.subTest(spelling=spelling):
                    env = {"TRACE": " \t" + spelling.upper() + "\n", "OTHER": "keep"}
                    before = env.copy()
                    options = worker_options(env)
                    self.assertEqual(options, {"trace": expected, "retries": 3})
                    self.assertIs(options["trace"], expected)
                    self.assertEqual(env, before)

    def test_worker_missing_and_none_default_to_false(self):
        for env in ({"OTHER": "yes"}, {"TRACE": None, "OTHER": "yes"}):
            with self.subTest(env=env):
                before = env.copy()
                options = worker_options(env)
                self.assertEqual(options, {"trace": False, "retries": 3})
                self.assertIs(options["trace"], False)
                self.assertEqual(env, before)

    def test_worker_propagates_invalid_and_blank_errors(self):
        for value in ("", " \t\n", "maybe", "2", "enabled"):
            with self.subTest(value=value):
                env = {"TRACE": value, "OTHER": "keep"}
                before = env.copy()
                with self.assertRaises(ValueError):
                    worker_options(env)
                self.assertEqual(env, before)
