from datetime import date
from pandas import DataFrame
from numpy import array, corrcoef

from .report_all import _prepare_table

TODAY = date.today()


def corr_funds(fund1, fund2, n_years):
    df1 = fund1.df
    df2 = fund2.df
    mdf = df1.merge(df2, on='Per')

    min_year = mdf['Per'].iloc[-1].year

    out = {
        'from': [],
        'to': [],
        fund1.name: [],
        fund2.name: [],
        'correlation': [],
        }

    for i in range(min_year, TODAY.year - n_years + 1):

        date_0 = TODAY.replace(year=i)
        date_1 = TODAY.replace(year=i + n_years)
        date_range = (mdf['Per'] >= date_0) & (mdf['Per'] <= date_1)

        x = mdf.loc[date_range, 'NAV_x']
        y = mdf.loc[date_range, 'NAV_y']

        r_x = annual_return(array(x), n_years) * 100
        r_y = annual_return(array(y), n_years) * 100
        c_xy = corrcoef(x, y)[0, 1]

        out['from'].append(date_0)
        out['to'].append(date_1)
        out[fund1.name].append(r_x)
        out[fund2.name].append(r_y)
        out['correlation'].append(c_xy)

    DATAFORMAT = {
        'from': '{:%d-%m-%Y}',
        'to': '{:%d-%m-%Y}',
        fund1.name: '{:.2f}',
        fund2.name: '{:.2f}',
        'correlation': '{:.2f}',
    }
    dfx = DataFrame(out)

    rst = _prepare_table(dfx, DATAFORMAT)

    return dfx, rst


def annual_return(x, n_years):
    latest = x[0]
    basis = x[-1]
    percent = (latest - basis) / basis
    return (1 + percent) ** (1 / n_years) - 1
