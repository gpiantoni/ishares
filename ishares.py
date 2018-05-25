s = '24/mei/2018'
def dutch_date(s):
    d, m, y = s.split('/')
    return date(int(y), MONTHS[m], int(d))


from datetime import date
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

import xml.etree.ElementTree  as ET
from pandas import read_excel, read_html
from lxml import etree

from pathlib import Path
xls_orig = Path('/home/giovanni/tools/ishares/data/iShares-MSCI-Europe-UCITS-ETF-EUR-Acc_fund.xls')


from pandas import DataFrame, to_datetime

euro = read_ishares(d)


def read_ishares(d):
    root = etree.fromstring(d)

    root = ET.fromstring(d)
    ns = root.tag[:-8]

    for worksheet in root:
        if worksheet.tag == ns + 'Worksheet':
            if worksheet.attrib[namespace + 'Name'] == 'Historisch':
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
    return df


with xls_orig.open('r', encoding='utf-8-sig') as f:
    d = f.read()
    
d = d.replace('&euml;', 'ë')
d = d.replace('</Style>', '</ss:Style>')