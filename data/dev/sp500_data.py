import pandas as pd
from volatility_data import IntegrateVolatilityData

sp_df = pd.read_csv("csv_files/SP500-Monthly.csv")


def convert_date(x): return int(x.replace('-', ''))


date_series = sp_df['Date'].apply(convert_date)
sp_df['Date'] = date_series
sp_df.drop(['Open', 'High', 'Low', 'Volume', 'Close'], axis=1, inplace=True)


def trailing_n_rows_change(row, n=12, column='Adj Close'):
    if row < n:
        return 0
    else:
        prev_close = sp_df.loc[row - n, column]
        curr_close = sp_df.loc[row, column]

        return (curr_close - prev_close) / prev_close



def trailing_12_months_return(row): return trailing_n_rows_change(row)

def stdev_returns(row, n=12):
    return stdev(trailing_n_rows_change(row, n=n))

sp_df['idx'] = sp_df.index
sp_df['12mo return'] = sp_df['idx'].apply(trailing_12_months_return)
sp_df['12mo volatility'] = sp_df['idx'].apply(stdev_returns)
sp_df.drop(['idx'], axis=1, inplace=True)

