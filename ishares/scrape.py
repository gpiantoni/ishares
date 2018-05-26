from requests import Session

ENTRY_URL = 'https://www.ishares.com/nl/particuliere-belegger/nl/?siteEntryPassthrough=true&locale=nl_NL&userType=individual'


def site_session():

    s = Session()
    s.get(ENTRY_URL)
    return s
