from pytest import raises

from ishares.interface import iShares


all_etfs = None

def test_interface():
    global all_etfs
    all_etfs = iShares()
    fund = all_etfs.get_fund('IMAE')
    fund.report()

    fund = all_etfs.get_fund('CSPX')
    fund.report()


def test_interface_findfund():
    global all_etfs

    with raises(ValueError):
        all_etfs.get_fund('XXXXXXX')
