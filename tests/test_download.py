from ishares.scrape import download_fund
from ishares.dataframe import WorkSheets


def test_download():
    resp = download_fund('251861')
    w = WorkSheets(resp)
    df = w.read_worksheet('Historisch')
    assert len(df.columns) == 7
