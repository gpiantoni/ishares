"""High-level abstraction
"""

from .dataframe import WorkSheets
from .scrape import download_fund, download_all, import_fund_ids


class iShares():

    def __init__(self):

        content = download_all()
        self.ws = WorkSheets(content)
        self.df = self.ws.read_worksheet('iShares ETFs')
        self.df.insert(0, 'id', import_fund_ids())

    def get_fund(self, code):
        fund_id = self.df.loc[self.df['Product-\ncode'] == code, 'id'].item()
        return Fund(fund_id)


class Fund():
    def __init__(self, fund_id):

        content = download_fund(fund_id)
        self.ws = WorkSheets(content)
        self.df = self.ws.read_worksheet('Historisch')
