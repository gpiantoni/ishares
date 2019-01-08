from ishares.corr import corr_funds
from ishares.report_all import publish
from ishares.constants.paths import SRC_PATH, HTML_PATH


def test_correlation(all_etfs):

    fund0 = all_etfs.get_fund(isin='IE0031442068')
    fund1 = all_etfs.get_fund(isin='IE00B4L5YC18')

    rst = corr_funds(fund0, fund1, 1)[1]

    rst_file = SRC_PATH / ('corr' + '.rst')
    html_file = HTML_PATH / ('corr' + '.html')
    publish(rst, rst_file, html_file)
