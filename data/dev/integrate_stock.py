import pandas as pd
from dev_lib import IntegrateData, pct_chg


class IntegrateStockData(IntegrateData):

    def __init__(self, in_path, out_path, returns_to_calc=(3, 6, 12, 24, 36), input_type='csv', output_type='csv'):
        self.returns_lengths = returns_to_calc
        super().__init__(in_path, out_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):
        self.construct_date_from_datadate()

        self.data['Unnamed'] = self.data.index

        for return_len in self.returns_lengths:
            col_label = "trailing_{}_mo_return".format(return_len)
            return_func = lambda x: self.trailing_n_months_return(x, n=return_len)
            self.data[col_label] = self.data['Unnamed'].apply(return_func)

        super().integrate_data()

    def construct_date_from_datadate(self):
        self.data['date'] = pd.to_datetime(self.data['datadate'], format='%m/%d/%Y')

        self.data.sort_values(by=['sic', 'gvkey', 'date'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def trailing_n_months_return(self, row, n=12):
        if row < n:
            return "NaN"

        trailing_price = self.data.loc[row - n, 'prccm']
        current_price = self.data.loc[row, 'prccm']

        trailing_id = self.data.loc[row - n, 'gvkey']
        current_id = self.data.loc[row, 'gvkey']

        if trailing_id == current_id:
            return pct_chg(current_price, trailing_price)
        else:
            return "NaN"

    # @staticmethod
    # def month_difference(date_1, date_2):
    #     month = lambda date: (date // 100) % 100
    #     year = lambda date: date // 10000
    #
    #     return ((year(date_1) - year(date_2)) * 12) + (month(date_1) - month(date_2))

