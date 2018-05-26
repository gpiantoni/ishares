from datetime import date
import xml.etree.ElementTree as ET

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


def dutch_date(s):
    d, m, y = s.split('/')
    return date(int(y), MONTHS[m], int(d))

class WorkSheets():
    def __init__(self, raw):
        self.raw = _fix_xls(raw)
        self.root = ET.fromstring(self.raw)
        self.ns = self.root.tag[:-8]

    def _get_worksheet(self, name):
        for worksheet in sel.froot:
            if worksheet.tag == self.ns + 'Worksheet':
                if worksheet.attrib[ns + 'Name'] == 'Historisch':
                    break

        table = next(iter(worksheet))

def _fix_xls(raw):
    raw = raw.replace('&euml;', 'ë')
    raw = raw.replace('</Style>', '</ss:Style>')
    return raw


def read_ishares(d):



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
