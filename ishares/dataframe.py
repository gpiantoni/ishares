from datetime import date
import xml.etree.ElementTree as ET

from pandas import DataFrame, to_numeric, to_datetime

from .constants.paths import ERROR_PATH

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
        try:
            self.root = ET.fromstring(self.raw)
        except Exception as err:
            with (ERROR_PATH / ('error.xls')).open('w') as f:
                f.write(self.raw)
            raise Exception(err)

        self.ns = self.root.tag[:-8]  # TODO: find a better way

    @property
    def worksheets(self):
        names = []
        for worksheet in self.root:
            if worksheet.tag == self.ns + 'Worksheet':
                names.append(worksheet.attrib[self.ns + 'Name'])
        return names

    def read_worksheet(self, name):
        table = self._get_worksheet(name)
        worksheet = _read_worksheet(table, self.ns)

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
    raw = raw.replace('&reg;', '®')
    raw = raw.replace('&euro;', '€')
    raw = raw.replace('&copy;', '©')
    if '<ss:Style' in raw:
        raw = raw.replace('</Style>', '</ss:Style>')
    return raw


def _convert_to_df(worksheet, name):
    if name == 'Posities':
        del worksheet[0]

    elif name == 'Performance':
        del worksheet[:4]

    df = DataFrame(worksheet)

    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop(0))

    return _fix_df(df, name)


def _fix_df(df, name):
    LOCALE_DATE_COLS = None  # those in Dutch locale format (09-mar-2018)
    DATE_COLS = None  # other dates that can be parsed by pandas
    FLOAT_COLS = None

    if name == 'Posities':
        FLOAT_COLS = ['Weging (%)', ]

    elif name == 'Performance':
        LOCALE_DATE_COLS = ['Einde maand', ]
        FLOAT_COLS = ['Rendement per maand', ]

    elif name == 'Historisch':
        LOCALE_DATE_COLS = ['Per', ]
        FLOAT_COLS = list(df)[2:]

    elif name == 'Uitkeringen':
        LOCALE_DATE_COLS = ['Aankondigingsdatum', 'Ex-datum', 'Uitkeringsdatum', 'Boekdatum']
        FLOAT_COLS = ['Totale uitkering', ]

    elif name == 'iShares ETFs':
        df.rename(columns={
            'Product-\ncode': 'Code',
            }, inplace=True)
        DATE_COLS = ['Introductiedatum', 'NAV per', '12 maanden (Per)', 'op jaarbasis (NAV per)', 'Cumulatief (NAV per)']
        FLOAT_COLS = ['Netto-activa', 'TER', 'NAV', 'Index-niveau', 'Aantal uitstaande aandelen', 'op jaarbasis (5 jr. (%))', 'Kenmerken (Uitkeringsrendement (%))']

    if LOCALE_DATE_COLS is not None:
        df[LOCALE_DATE_COLS] = df[LOCALE_DATE_COLS].applymap(_to_date)
    if DATE_COLS is not None:
        df[DATE_COLS] = df[DATE_COLS].apply(to_datetime, errors='coerce', axis=1)
    if FLOAT_COLS is not None:
        df[FLOAT_COLS] = df[FLOAT_COLS].apply(to_numeric, errors='coerce', axis=1)

    df['Netto-activa'] /= 1e9

    return df


def _to_date(s):
    d, m, y = s.split('/')
    return date(int(y), MONTHS[m], int(d))


def _read_worksheet(table, ns):
    double_header = False
    worksheet = []
    for row in table:

        if double_header:
            one_row = worksheet[-1]
            del worksheet[-1]
        else:
            one_row = []

        for cell in row:
            text = next(iter(cell)).text
            times = int(cell.attrib.get(ns + 'MergeAcross', '0')) + 1

            if (ns + 'MergeDown') in cell.attrib:
                double_header = True

            if (ns + 'Index') in cell.attrib:
                index = int(cell.attrib[ns + 'Index']) - 1
                one_row[index] = one_row[index] + ' (' + text + ')'
                double_header = False

            else:
                for i in range(times):
                    one_row.append(text)

        worksheet.append(one_row)
    return worksheet
