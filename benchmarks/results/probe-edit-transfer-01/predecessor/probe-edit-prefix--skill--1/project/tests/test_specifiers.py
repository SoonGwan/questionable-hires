# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

import itertools
import operator

import pytest

from packaging.specifiers import InvalidSpecifier, Specifier, SpecifierSet
from packaging.version import Version, parse

from .test_version import VERSIONS

LEGACY_SPECIFIERS = [
    "==2.1.0.3",
    "!=2.2.0.5",
    "<=5",
    ">=7.9a1",
    "<1.0.dev1",
    ">2.0.post1",
]

SPECIFIERS = [
    "~=2.0",
    "==2.1.*",
    "==2.1.0.3",
    "!=2.2.*",
    "!=2.2.0.5",
    "<=5",
    ">=7.9a1",
    "<1.0.dev1",
    ">2.0.post1",
]


class TestSpecifier:
    @pytest.mark.parametrize("specifier", SPECIFIERS)
    def test_specifiers_valid(self, specifier):
        Specifier(specifier)
