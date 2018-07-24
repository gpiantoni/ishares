from pytest import fixture
from ishares.interface import iShares

@fixture(scope='session')
def read_ishares():
    return iShares()
