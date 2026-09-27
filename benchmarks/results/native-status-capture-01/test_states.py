import pytest


def test_pass():
    assert 1 == 1


def test_fail():
    assert 'observed' == 'expected'


def test_skip():
    pytest.skip('control')


@pytest.mark.xfail(reason='control')
def test_xfail():
    assert False


@pytest.mark.xfail(reason='control')
def test_xpass():
    assert True


@pytest.fixture
def setup_error():
    raise RuntimeError('setup control')


def test_setup_error(setup_error):
    pass


@pytest.fixture
def teardown_error(request):
    def fail():
        raise RuntimeError('teardown control')
    request.addfinalizer(fail)


def test_teardown_error(teardown_error):
    assert True
