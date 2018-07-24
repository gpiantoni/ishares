from pytest import fixture
from ishares.interface import iShares

@fixture(scope='session')
def test_interface():
    return iShares()
