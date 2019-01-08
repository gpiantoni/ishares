from bs4 import BeautifulSoup
from requests import Session
from requests.compat import urljoin
from pathlib import Path

ENTRY_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/?siteEntryPassthrough=true&locale=nl_NL&userType=individual'
SINGLE_FUND_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/producten/{id_fund}/'
ALL_FUNDS_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/producten/etf-product-list/1524727818159.ajax'

SESSION = None


def download_fund(id_fund):
    global SESSION

    if SESSION is None:
        print('make session')
        SESSION = site_session()

    # parse html page
    resp_page = SESSION.get(SINGLE_FUND_URL.format(id_fund=id_fund))
    soup_page = BeautifulSoup(resp_page.content.decode(), features='html.parser')
    a_href = soup_page.find("a", {'data-link-event': "fund download:common"})
    download_url = urljoin(resp_page.url, a_href.attrs['href'])

    # download url
    resp_xls = SESSION.get(download_url)
    return strip_bom(resp_xls.content).decode('utf-8')


def download_all():
    PORTFOLIOS = '-'.join(import_fund_ids())

    payload = dict(
        fileType='xls',
        productView='emeaIshares',
        portfolios=PORTFOLIOS,
        disclosureContentDcrPath='templatedata/config/product-screener-v2/data/nl/ishares-nl',
        )

    s = site_session()
    resp = s.post(ALL_FUNDS_URL, data=payload)
    return strip_bom(resp.content).decode('utf-8')


def site_session():

    s = Session()
    s.get(ENTRY_URL)
    return s


def strip_bom(content):
    """Remove UTF-8 Byte Order Mark (there might be two)
    """
    return content.strip(b'\xef\xbb\xbf')


def import_fund_ids():
    """

    TODO
    ----
    path to fund_all.txt
    """
    funds_txt = Path(__file__).parent / 'data' / 'fund_all.txt'
    with funds_txt.open() as f:
        portfolios = f.read().strip().split('\n')
    return portfolios
