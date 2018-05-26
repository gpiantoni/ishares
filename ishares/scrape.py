from requests import Session

ENTRY_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/?siteEntryPassthrough=true&locale=nl_NL&userType=individual'
DOWNLOAD_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/{id_fund}/fund-download.dl'

SESSION = None


def download_fund(id_fund):
    global SESSION

    if SESSION is None:
        print('make session')
        SESSION = site_session()

    resp = SESSION.get(DOWNLOAD_URL.format(id_fund=id_fund))
    return resp.content.decode('utf-8-sig')


def site_session():

    s = Session()
    s.get(ENTRY_URL)
    return s
