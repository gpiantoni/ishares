from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[2]

REPORT_PATH = ROOT_PATH / 'report'

SRC_PATH = REPORT_PATH / 'src'
SRC_PATH.mkdir(parents=True, exist_ok=True)

PLOTLY_PATH = SRC_PATH / 'img'
PLOTLY_PATH.mkdir(parents=True, exist_ok=True)

HTML_PATH = REPORT_PATH / 'html'
HTML_PATH.mkdir(parents=True, exist_ok=True)
