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


class WorkSheets():
    def __init__(self, raw):
        self.raw = _fix_xls(raw)
        self.root = ET.fromstring(self.raw)
        self.ns = self.root.tag[:-8]  # TODO: find a better way

    def read_worksheet(self, name):
        table = self._get_worksheet(name)

        worksheet = []
        for row in table:
            one_row = []
            for cell in row:
                one_row.append(next(iter(cell)).text)

            worksheet.append(one_row)

        return _convert_to_df(worksheet, name)

    def _get_worksheet(self, name):
        """Historish"""
        for worksheet in self.root:
            if worksheet.tag == self.ns + 'Worksheet':
                if worksheet.attrib[self.ns + 'Name'] == name:
                    break

        return next(iter(worksheet))


def _fix_xls(raw):
    raw = raw.replace('&euml;', 'ë')
    raw = raw.replace('</Style>', '</ss:Style>')
    return raw


def _convert_to_df(worksheet, name):
    df = DataFrame(worksheet)
    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop(0))

    if name == 'Historisch':
        DATE_COLS = ['Per', ]
        FLOAT_COLS = [list(df)[2:]]

    df[DATE_COLS] = df[DATE_COLS].apply(_to_date)
    df[FLOAT_COLS] = df[FLOAT_COLS].apply(to_numeric, errors='coerce', axis=1)

    return df


def _to_date(s):
    d, m, y = s.split('/')
    return date(int(y), MONTHS[m], int(d))
