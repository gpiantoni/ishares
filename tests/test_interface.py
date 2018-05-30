from ishares.interface import iShares


def test_interface():
    all_etfs = iShares()
    fund = all_etfs.get_fund('IMAE')
    fund.report()

    fund = all_etfs.get_fund('CSPX')
    fund.report()
