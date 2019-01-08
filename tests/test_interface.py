from pytest import raises


def test_interface(all_etfs):
    all_etfs.report()


def test_interface_isin(all_etfs):
    fund = all_etfs.get_fund(isin='IE0032895942')
    fund.report()


def test_interface_nofund(all_etfs):
    with raises(ValueError):
        all_etfs.get_fund('XXXXXXX')


def test_interface_manyfund(all_etfs):
    with raises(ValueError):
        all_etfs.get_fund('LQDA')
