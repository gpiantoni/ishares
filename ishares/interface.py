"""High-level abstraction
"""

from .dataframe import WorkSheets
from .scrape import download_fund, download_all, import_fund_ids
from .report import create_fig, write_report
from .report_all import report_ishares


class iShares():

    def __init__(self):

        content = download_all()
        self.ws = WorkSheets(content)
        self.df = self.ws.read_worksheet('iShares ETFs')
        self.df.insert(0, 'id', import_fund_ids())

    def get_fund(self, code=None, fund_id=None, isin=None):
        if code is not None:
            idx = self.df['Code'] == code
            args_name = f'code="{code}"'

        elif fund_id is not None:
            idx = self.df['id'] == fund_id
            args_name = f'fund_id="{fund_id}"'

        elif isin is not None:
            idx = self.df['ISIN'] == isin
            args_name = f'isin="{isin}"'

        funds = self.df.loc[idx, ]
        if len(funds) == 0:
            raise ValueError(f'Could not find any ETF matching {args_name}')
        elif len(funds) > 1:
            raise ValueError(f'Multiple ETFs matching {code}, use fund_id= or isin=')

        name = funds['Code'].item() + '_' + funds['ISIN'].item()
        return Fund(funds['id'].item(), name)

    def report(self):
        df = report_ishares(self.df)
        for isin in df['ISIN']:
            fund = self.get_fund(isin=isin)
            fund.report()


class Fund():
    dividend = None

    def __init__(self, fund_id, name):
        self.id = fund_id
        self.name = name

        content = download_fund(fund_id)
        self.ws = WorkSheets(content)
        self.df = self.ws.read_worksheet('Historisch')
        if 'Uitkeringen' in self.ws.worksheets:
            self.dividend = self.ws.read_worksheet('Uitkeringen')

    def plot(self):
        return create_fig(self.df, self.dividend)

    def report(self):
        fig = create_fig(self.df)
        write_report(fig, self.name)
