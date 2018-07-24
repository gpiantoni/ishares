from ishares.constants.datasets import DEGIRO
from docutils.core import publish_file

from .constants.paths import SRC_PATH, HTML_PATH


COLS = [
    'Code',
    'ISIN',
    'Naam en aandelenklasse',
    'TER', 'Methodologie',
    'Beleggingscategorie', 'Sector / Thema', 'Regio', 'Basis-\nvaluta',
    'Markt', 'Strategieën', 'Land', 'Aandelen-\nklasse',
    'Netto-activa',
    'op jaarbasis (5 jr. (%))', 'Kenmerken (Uitkeringsrendement (%))'
]


FORMAT = {
    'TER': '{:5.2f}',
    'Netto-activa': '{:.3f} B',
    'op jaarbasis (5 jr. (%))': '{:5.2f}',
    'Kenmerken (Uitkeringsrendement (%))': '{:5.2f}',
    }


def publish(rst, rst_file, html_file):

    with rst_file.open('w') as f:
        f.write('\n'.join(rst))

    publish_file(
        source_path=str(rst_file),
        destination_path=str(html_file),
        writer_name='html')


def report_ishares(df):
    rst_file = SRC_PATH / ('ishares' + '.rst')
    html_file = HTML_PATH / ('index' + '.html')

    degiro_isin = list(DEGIRO['ISIN'])
    idx = (
        df['ISIN'].isin(degiro_isin)
        & (df['TER'] <= 0.3))
    torst = df.loc[idx, COLS].sort_values('TER')

    torst['ISIN'] = torst.apply(lambda x: f'`{x["ISIN"]} <{x["Code"]}_{x["ISIN"]}.html>`_', axis=1)

    rst = _prepare_table(torst, FORMAT)
    publish(rst, rst_file, html_file)

    return df.loc[idx]


def _prepare_table(torst, tableformat):
    col_len = []
    for row in torst:
        format_ = tableformat.get(row, '{}')
        col_len.append(
            max([len(format_.format(x)) for x in torst[row]] + [len(row), ])
            )

    formatter = ' '.join('{:<%d}' % c for c in col_len)

    all_rows = []
    for row in torst.iterrows():
        ROW = _row2str(tableformat, row)
        good_row = formatter.format(*ROW)
        all_rows.append(good_row)

    separator = ' '.join(['=' * c for c in col_len])
    header = formatter.format(*[x.replace('\n', ' ') for x in torst])
    rst = [separator, header, separator] + all_rows + [separator, ]

    return rst


def _row2str(FORMAT, row):
    ROW = []
    for col, cell in row[1].iteritems():
        format_ = FORMAT.get(col, '{}')
        ROW.append(
            format_.format(cell)
        )
    return ROW

