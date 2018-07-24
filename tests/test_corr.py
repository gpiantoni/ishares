from ishares.corr import corr_funds
from ishares.report_all import publish
from ishares.constants.paths import SRC_PATH, HTML_PATH
from .conftest import read_ishares


def test_correlation():
    all_etfs = read_ishares()

    fund0 = all_etfs.get_fund(isin='IE0008471009')
    fund1 = all_etfs.get_fund(isin='IE0031442068')

    rst = corr_funds(fund0, fund1, 1)[1]

    rst_file = SRC_PATH / ('corr' + '.rst')
    html_file = HTML_PATH / ('corr' + '.html')
    publish(rst, rst_file, html_file)
