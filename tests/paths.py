from pathlib import Path

FUND_ID = '251861'


DOWNLOAD_PATH = Path(__file__).resolve().parent / 'download'
DOWNLOAD_PATH.mkdir(parents=True, exist_ok=True)
