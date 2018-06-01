from requests import Session
from pathlib import Path

ENTRY_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/?siteEntryPassthrough=true&locale=nl_NL&userType=individual'
SINGLE_FUND_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/{id_fund}/fund-download.dl'
ALL_FUNDS_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/producten/etf-product-list/1524727818159.ajax'

SESSION = None


def download_fund(id_fund):
    global SESSION

    if SESSION is None:
        print('make session')
        SESSION = site_session()

    resp = SESSION.get(SINGLE_FUND_URL.format(id_fund=id_fund))
    return strip_bom(resp.content).decode('utf-8')


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
        portfolios = f.read().split('\n')
    return portfolios
