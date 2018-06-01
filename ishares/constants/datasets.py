from pandas import read_csv

from .paths import DATA_PATH


DEGIRO = read_csv(DATA_PATH / 'degiro.csv').dropna(0)
OWNED = read_csv(DATA_PATH / 'owned.csv', parse_dates=['Bought', 'Sold'])
