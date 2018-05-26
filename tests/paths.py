from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[1]

SRC_PATH = ROOT_PATH / 'report/src'
SRC_PATH.mkdir(parents=True, exist_ok=True)

PLOTLY_PATH = SRC_PATH / 'img'
PLOTLY_PATH.mkdir(parents=True, exist_ok=True)

HTML_PATH = ROOT_PATH / 'report/html'
HTML_PATH.mkdir(parents=True, exist_ok=True)
