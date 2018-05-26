from ishares.scrape import download_fund
from ishares.dataframe import WorkSheets
from ishares.report import create_fig

from docutils.core import publish_file

from .utils import save_plotly_fig
from .paths import HTML_PATH, SRC_PATH


def test_download():
    resp = download_fund('251861')
    w = WorkSheets(resp)
    df = w.read_worksheet('Historisch')
    assert len(df.columns) == 7

    fig = create_fig(df)
    save_plotly_fig(fig, 'interactive')
    publish_file(
        source_path=str(SRC_PATH / 'report.rst'),
        destination_path=str(HTML_PATH / 'index.html')
        )
