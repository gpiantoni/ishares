"""High-level abstraction
"""

from .dataframe import WorkSheets
from .scrape import download_fund, download_all, import_fund_ids
from .report import create_fig, write_report


class iShares():

    def __init__(self):

        content = download_all()
        self.ws = WorkSheets(content)
        self.df = self.ws.read_worksheet('iShares ETFs')
        self.df.insert(0, 'id', import_fund_ids())

    def get_fund(self, code):
        fund_id = self.df.loc[self.df['Product-\ncode'] == code, 'id'].item()
        return Fund(fund_id, code)


class Fund():
    def __init__(self, fund_id, code):
        self.id = fund_id
        self.code = code

        content = download_fund(fund_id)
        self.ws = WorkSheets(content)
        self.df = self.ws.read_worksheet('Historisch')

    def plot(self):
        return create_fig(self.df)

    def report(self):
        fig = create_fig(self.df)
        write_report(fig, self.code)
