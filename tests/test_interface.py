from pytest import raises

from ishares.interface import iShares

from .conftest import read_ishares


def test_interface():
	all_etfs = read_ishares()
    all_etfs.report()


def test_interface_isin():
	all_etfs = read_ishares()
    fund = all_etfs.get_fund(isin='IE0032895942')
    fund.report()


def test_interface_nofund():
	all_etfs = read_ishares()
    with raises(ValueError):
        all_etfs.get_fund('XXXXXXX')


def test_interface_manyfund():
	all_etfs = read_ishares()
    with raises(ValueError):
        all_etfs.get_fund('LQDA')
