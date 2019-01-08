from pytest import fixture
from ishares.interface import iShares

@fixture(scope='session')
def all_etfs():
    return iShares()
