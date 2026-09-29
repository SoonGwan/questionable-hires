def test_pass():
    assert 7 == 7

def test_fail():
    assert "observed" == "expected", "observed != expected"
