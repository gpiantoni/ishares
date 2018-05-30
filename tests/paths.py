from pathlib import Path

FUND_ID = '251861'

ROOT_PATH = Path(__file__).resolve().parents[1]

DOWNLOAD_PATH = Path(__file__).resolve().parent / 'download'
DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)

SRC_PATH = ROOT_PATH / 'report/src'
SRC_PATH.mkdir(parents=True, exist_ok=True)

PLOTLY_PATH = SRC_PATH / 'img'
PLOTLY_PATH.mkdir(parents=True, exist_ok=True)

HTML_PATH = ROOT_PATH / 'report/html'
HTML_PATH.mkdir(parents=True, exist_ok=True)
