from ishares.corr import corr_funds
from ishares.report_all import publish
from ishares.constants.paths import SRC_PATH, HTML_PATH
from .test_interface import all_etfs


def test_correlation():

    fund0 = all_etfs.get_fund(isin='IE0008471009')
    fund1 = all_etfs.get_fund(isin='IE0031442068')

    rst = corr_funds(fund0, fund1)

    rst_file = SRC_PATH / ('corr' + '.rst')
    html_file = HTML_PATH / ('corr' + '.html')
    publish(rst, rst_file, html_file)
