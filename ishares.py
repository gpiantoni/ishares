
from datetime import date
import xml.etree.ElementTree as ET

from requests import Session
from pandas import DataFrame, to_numeric

MONTHS = {
    'jan': 1,
    'feb': 2,
    'mrt': 3,
    'apr': 4,
    'mei': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'okt': 10,
    'nov': 11,
    'dec': 12,
}

def site_session():

    s = Session()
    s.get('https://www.ishares.com/nl/particuliere-belegger/nl/?siteEntryPassthrough=true&locale=nl_NL&userType=individual')
    return s


def dutch_date(s):
    d, m, y = s.split('/')
    return date(int(y), MONTHS[m], int(d))


def read_ishares(d):
    d = d.replace('&euml;', 'ë')
    d = d.replace('</Style>', '</ss:Style>')

    root = ET.fromstring(d)
    ns = root.tag[:-8]

    for worksheet in root:
        if worksheet.tag == ns + 'Worksheet':
            if worksheet.attrib[ns + 'Name'] == 'Historisch':
                break

    table = next(iter(worksheet))

    worksheets = []
    for row in table:
        one_row = []
        for cell in row:
            one_row.append(next(iter(cell)).text)

        worksheets.append(one_row)

    df = DataFrame(worksheets)
    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop(0))
    df['Per'] = df['Per'].apply(dutch_date)
    cols = list(df)[2:]
    df[cols] = df[cols].apply(to_numeric, errors='coerce', axis=1)
    return df
