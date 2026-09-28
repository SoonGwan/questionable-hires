import pytest
def test_outer(tmpdir):
    inner = tmpdir.join("test_inner.py")
    inner.write("def test_inner_failure():\n    assert 41 == 42\n")
    result = pytest.main(["-q", "--tb=short", "-p", "no:cacheprovider", str(inner)])
    assert result == 1
    print("QH_NESTED_NATIVE_EXIT=1")
