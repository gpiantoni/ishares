from ishares.dataframe import WorkSheets

from .paths import DOWNLOAD_PATH, FUND_ID


def test_worksheet_names():
    with (DOWNLOAD_PATH / (FUND_ID + '.xls')).open() as f:
        content = f.read()
    ws = WorkSheets(content)
    assert ws.worksheets[2] == 'Historisch'


def test_worksheet_read():
    with (DOWNLOAD_PATH / (FUND_ID + '.xls')).open() as f:
        content = f.read()
    ws = WorkSheets(content)

    pos = ws.read_worksheet('Posities')
    assert len(pos.columns) == 5

    perf = ws.read_worksheet('Performance')
    assert len(perf.columns) == 2
