from ishares.scrape import download_fund, download_all
from ishares.dataframe import WorkSheets
from ishares.report import create_fig

from docutils.core import publish_file

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


def tst_download():
    resp = download_fund('251861')
    w = WorkSheets(resp)
    df = w.read_worksheet('Historisch')
    assert len(df.columns) == 7

    df.to_pickle('/home/giovanni/tools/ishares/tests/download/251861.pkl')

    fig = create_fig(df)
    save_plotly_fig(fig, 'interactive')
    publish_file(
        source_path=str(SRC_PATH / 'report.rst'),
        destination_path=str(HTML_PATH / 'index.html')
        )
