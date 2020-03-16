import pandas as pd
import numpy as np


filepath = "stock_df.pkl"
raw_data = pd.read_pickle(filepath)


day = lambda date: date % 100
month = lambda date: (date // 100) % 100
year = lambda date: date // 10000


def month_difference(date_1, date_2):
    return ((year(date_1) - year(date_2)) * 12) + (month(date_1) - month(date_2))


def pct_chg(current, historical):
    if historical != 0:
        return (current - historical) / historical
    else:
        return 0


def trailing_n_months_return(row, n=12):
    if row < n:
        return 0

    trailing_date = raw_data.loc[row - n, 'date']
    current_date = raw_data.loc[row, 'date']

    trailing_price = raw_data.loc[row - n, 'prccm']
    current_price = raw_data.loc[row, 'prccm']

    trailing_id = raw_data.loc[row - n, 'gvkey']
    current_id = raw_data.loc[row, 'gvkey']

    if month_difference(current_date, trailing_date) == n and trailing_id == current_id:
        return pct_chg(current_price, trailing_price)
    else:
        return 0


def trailing_n_months_returns(row, n=12):
    if row < n:
        return np.array([1])

    trailing_date = raw_data.loc[row - n, 'date']
    current_date = raw_data.loc[row, 'date']

    trailing_id = raw_data.loc[row - n, 'gvkey']
    current_id = raw_data.loc[row, 'gvkey']

    if month_difference(current_date, trailing_date) == n and trailing_id == current_id:
        return np.array([raw_data.loc[row - i, 'prccm'] for i in range(n)])
    else:

        # stdev of [1] will always be zero, so this is effectively the dummy variable
        return np.array([1])


def avg(array):
    return np.sum(array) / array.shape[0]


def squared_devs(array):
    average = avg(array)
    return np.array([(i - average) ** 2 for i in array])


def stdev(array):
    return np.sum(squared_devs(array) / array.shape[0]) ** 0.5


def stdev_returns(row, n=12):
    return stdev(trailing_n_months_returns(row, n=n))


raw_data['idx'] = raw_data.index
raw_data['12_mo_stdev'] = raw_data['idx'].apply(lambda row: stdev_returns(row))
raw_data['24_mo_stdev'] = raw_data['idx'].apply(lambda row: stdev_returns(row, n=24))
raw_data['36_mo_stdev'] = raw_data['idx'].apply(lambda row: stdev_returns(row, n=36))
raw_data = raw_data.drop(['idx'], axis=1)

preview_data = raw_data.drop(['iid', 'date', 'sic', 'gvkey'], axis=1).head(n=100)
print(preview_data)

raw_data.to_pickle('volatility_df.pkl')