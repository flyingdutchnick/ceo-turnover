from data.dev.dev_lib import IntegrateData, pct_chg


class IntegrateStockData(IntegrateData):

    def __init__(self, in_path, out_path, returns_to_calc=(3, 6, 12, 24, 36)):
        self.returns_lengths = returns_to_calc
        super().__init__(in_path, out_path)

    def integrate_data(self):
        self.construct_date_from_datadate()

        self.data['Unnamed'] = self.data.index

        for return_len in self.returns_lengths:
            col_label = "trailing_{}_mo_return".format(return_len)
            return_func = lambda x: self.trailing_n_months_return(x, n=return_len)
            self.data[col_label] = self.data['Unnamed'].apply(return_func)

        super().integrate_data()

    def construct_date_from_datadate(self):
        month_str_to_num = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6, "JUL": 7,
                            "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}

        def make_data_sortable(date):
            days = int(date[0:2])
            month = month_str_to_num[date[2:5]]
            year = int(date[5:9])

            return days + month * 100 + year * 10000

        self.data['date'] = self.data['datadate'].apply(lambda x: make_data_sortable(x))

        self.data.sort_values(by=['sic', 'gvkey', 'date'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

    def trailing_n_months_return(self, row, n=12):
        if row < n:
            return 0

        trailing_date = self.data.loc[row - n, 'date']
        current_date = self.data.loc[row, 'date']

        trailing_price = self.data.loc[row - n, 'prccm']
        current_price = self.data.loc[row, 'prccm']

        trailing_id = self.data.loc[row - n, 'gvkey']
        current_id = self.data.loc[row, 'gvkey']

        if IntegrateStockData.month_difference(current_date, trailing_date) == n and trailing_id == current_id:
            return pct_chg(current_price, trailing_price)
        else:
            return 0

    @staticmethod
    def month_difference(date_1, date_2):
        month = lambda date: (date // 100) % 100
        year = lambda date: date // 10000

        return ((year(date_1) - year(date_2)) * 12) + (month(date_1) - month(date_2))


def main():

    file_in = "csv_files/SharePriceData.csv"
    file_out = "csv_files/StockReturns.csv"

    data = IntegrateStockData(file_in, file_out)
    data.process()


main()
