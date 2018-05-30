from ishares.scrape import download_fund, download_all
from ishares.dataframe import WorkSheets
from ishares.report import create_fig


from .utils import save_plotly_fig
from .paths import HTML_PATH, SRC_PATH, DOWNLOAD_PATH, FUND_ID


def test_download_fund():
    content = download_fund(FUND_ID)

    assert content.startswith('<?xml version="1.0"?>')
    assert len(content) > 1690000

    with (DOWNLOAD_PATH / (FUND_ID + '.xls')).open('w') as f:
        f.write(content)


def test_download_all():
    content = download_all()

    assert content.startswith('<?xml version="1.0"?>')
    assert len(content) > 1240000

    with (DOWNLOAD_PATH / ('all' + '.xls')).open('w') as f:
        f.write(content)
