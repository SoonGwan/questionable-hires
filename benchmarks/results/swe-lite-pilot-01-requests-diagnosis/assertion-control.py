def test_passing_assertion():
    assert 7 == 7


def test_deliberate_failure():
    actual = 7
    expected = 9
    assert actual == expected
