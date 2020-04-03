import numpy as np
from dev_lib import stdev, IntegrateData
from tqdm import tqdm


class IntegrateSPData(IntegrateData):

    def __init__(self, in_path, out_path, input_type='csv', output_type='csv'):
        super().__init__(in_path, out_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):
        self.data['idx'] = self.data.index

        returns_periods = [1, 3, 6, 12, 24, 36]
        vol_periods = [3, 6, 12]

        for return_period in returns_periods:
            col_label = "sp500_trailing_{}_mo_return".format(return_period)
            tqdm.pandas(desc='Integrating SP500 {} month returns'.format(return_period))
            self.data[col_label] = self.data['idx'].progress_apply(
                lambda row: self.trailing_n_rows_change(row, n=return_period))

        for vol_period in vol_periods:
            col_label = "sp500_historical_{}_mo_volatility".format(vol_period)
            tqdm.pandas(desc='Integrating SP500 {} month historical volatility'.format(vol_period))
            self.data[col_label] = self.data['idx'].progress_apply(
                lambda row: self.stdev_returns(row, n=36)
            )

        self.data['12mo_sp_return'] = self.data['idx'].apply(self.trailing_12_mo_return)
        self.data['24mo_sp_return'] = self.data['idx'].apply(self.trailing_24_mo_return)
        self.data['36mo_sp_return'] = self.data['idx'].apply(self.trailing_36_mo_return)

        self.data['12mo_sp_volatility'] = self.data['idx'].apply(self.trailing_12_mo_stdev)
        self.data['24mo_sp_volatility'] = self.data['idx'].apply(self.trailing_24_mo_stdev)
        self.data['36mo_sp_volatility'] = self.data['idx'].apply(self.trailing_36_mo_stdev)

        self.data.drop(['idx'], axis=1, inplace=True)

        super().integrate_data()

    def write_data(self):
        self.data.drop(['Open', 'High', 'Low', 'Volume', 'Close'], axis=1, inplace=True)

        date_series = self.data['Date'].apply(lambda date: int(date.replace('-', '')))
        self.data['Date'] = date_series

        super().write_data()

    def trailing_n_rows_change(self, row, n=12, column='Adj Close'):
        if row < n:
            return 0
        else:
            prev_close = self.data.loc[row - n, column]
            curr_close = self.data.loc[row, column]

            return (curr_close - prev_close) / prev_close

    def trailing_12_mo_return(self, row):
        return self.trailing_n_rows_change(row)

    def trailing_24_mo_return(self, row):
        return self.trailing_n_rows_change(row, n=24)

    def trailing_36_mo_return(self, row):
        return self.trailing_n_rows_change(row, n=36)

    def trailing_n_rows_array(self, row, n=12, column='Adj Close'):
        if row < n:
            return np.array([1])
        else:
            return np.array([self.data.loc[row - i, column] for i in range(n)])

    def stdev_returns(self, row, n=12):
        return stdev(self.trailing_n_rows_array(row, n=n))

    def trailing_12_mo_stdev(self, row):
        return self.stdev_returns(row)

    def trailing_24_mo_stdev(self, row):
        return self.stdev_returns(row, n=24)

    def trailing_36_mo_stdev(self, row):
        return self.stdev_returns(row, n=36)


def main():
    input_path = "csv_files/sp500-monthly-price.csv"
    output_path = "csv_files/sp500-returns-volatility.csv"

    SPData = IntegrateSPData(input_path, output_path)
    SPData.process()

