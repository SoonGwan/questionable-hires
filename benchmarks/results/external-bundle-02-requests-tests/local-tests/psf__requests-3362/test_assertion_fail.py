def test_native_assertion():
    actual = 41
    assert actual == 42, "actual=%s expected=%s" % (actual, 42)
