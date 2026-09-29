def is_even(value):
    return value % 2 == 0

def test_authored():
    assert all([is_even(value) for value in [11, 13]])
