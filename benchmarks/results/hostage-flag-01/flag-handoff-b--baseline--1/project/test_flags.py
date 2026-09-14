import unittest
import os
from types import MappingProxyType
from unittest.mock import patch

from flags import read_flag
from worker import worker_options


class ExistingFlagTests(unittest.TestCase):
    def test_existing_true(self):
        self.assertIs(read_flag({"TRACE": "true"}, "TRACE"), True)

    def test_existing_missing(self):
        self.assertIs(read_flag({}, "TRACE"), False)


TRUE_VALUES = ("true", "yes", "on", "1")
FALSE_VALUES = ("false", "no", "off", "0")
INVALID_VALUES = ("", " ", "\t\r\n", "t", "f", "y", "n", "2", "-1",
                  "enabled", "disabled", "none", "null", "yes please", "tr ue")


class FlagContractTests(unittest.TestCase):
    def test_accepted_spellings_and_normalization(self):
        for expected, spellings in ((True, TRUE_VALUES), (False, FALSE_VALUES)):
            for spelling in spellings:
                for value in (spelling, spelling.upper(), spelling.title(),
                              " \t" + spelling.title() + "\r\n"):
                    for default in (False, True):
                        with self.subTest(value=value, default=default):
                            self.assertIs(read_flag({"TRACE": value}, "TRACE", default),
                                          expected)

    def test_missing_and_none_return_both_defaults(self):
        for env in ({}, {"TRACE": None}):
            for default in (False, True):
                with self.subTest(env=env, default=default):
                    self.assertIs(read_flag(env, "TRACE", default), default)

    def test_none_uses_implicit_false_default(self):
        self.assertIs(read_flag({"TRACE": None}, "TRACE"), False)

    def test_invalid_and_blank_strings_raise_with_both_defaults(self):
        for value in INVALID_VALUES:
            for default in (False, True):
                with self.subTest(value=value, default=default):
                    with self.assertRaises(ValueError):
                        read_flag({"TRACE": value}, "TRACE", default)

    def test_reads_requested_key(self):
        self.assertIs(read_flag({"TRACE": "false", "OTHER": "yes"}, "OTHER"), True)

    def test_supplied_mapping_takes_precedence_over_environment(self):
        with patch.dict(os.environ, {"TRACE": "true"}):
            self.assertIs(read_flag({}, "TRACE"), False)
            self.assertIs(read_flag({"TRACE": None}, "TRACE"), False)
            self.assertIs(read_flag({"TRACE": "false"}, "TRACE"), False)

    def test_mapping_preserved_on_success_and_error(self):
        for value in (*TRUE_VALUES, *FALSE_VALUES, " \tYeS\n", None, *INVALID_VALUES):
            for default in (False, True):
                with self.subTest(value=value, default=default):
                    env = {"TRACE": value, "OTHER": "unchanged"}
                    original = env.copy()
                    if value in INVALID_VALUES:
                        with self.assertRaises(ValueError):
                            read_flag(env, "TRACE", default)
                    else:
                        read_flag(env, "TRACE", default)
                    self.assertEqual(env, original)
        for default in (False, True):
            env = {"OTHER": "unchanged"}
            read_flag(env, "TRACE", default)
            self.assertEqual(env, {"OTHER": "unchanged"})

    def test_read_only_mapping_supported(self):
        self.assertIs(read_flag(MappingProxyType({"TRACE": "yes"}), "TRACE"), True)


class WorkerContractTests(unittest.TestCase):
    def test_accepted_values_and_mapping_preservation(self):
        for expected, spellings in ((True, TRUE_VALUES), (False, FALSE_VALUES)):
            for spelling in spellings:
                for value in (spelling, " \t" + spelling.upper() + "\n"):
                    with self.subTest(value=value):
                        env = {"TRACE": value, "OTHER": "unchanged"}
                        original = env.copy()
                        options = worker_options(env)
                        self.assertEqual(options, {"trace": expected, "retries": 3})
                        self.assertIs(options["trace"], expected)
                        self.assertEqual(env, original)

    def test_missing_and_none_default_false(self):
        for env in ({"OTHER": "yes"}, {"TRACE": None, "OTHER": "yes"}):
            with self.subTest(env=env):
                original = env.copy()
                options = worker_options(env)
                self.assertEqual(options, {"trace": False, "retries": 3})
                self.assertIs(options["trace"], False)
                self.assertEqual(env, original)

    def test_invalid_values_propagate_and_preserve_mapping(self):
        for value in INVALID_VALUES:
            with self.subTest(value=value):
                env = {"TRACE": value, "OTHER": "unchanged"}
                original = env.copy()
                with self.assertRaises(ValueError):
                    worker_options(env)
                self.assertEqual(env, original)
