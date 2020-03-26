import numpy as np
from data.dev.dev_lib import stdev, IntegrateData


class IntegrateSPData(IntegrateData):

    def __init__(self, in_path, out_path):
        super().__init__(in_path, out_path)

    def integrate_data(self):
        self.data['idx'] = self.data.index

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
    input_path = "csv_files/SP500-Monthly-2000.csv"
    output_path = "csv_files/SP500-Returns-Volatility.csv"

    SPData = IntegrateSPData(input_path, output_path)
    SPData.process()

