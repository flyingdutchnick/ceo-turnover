import numpy as np
from dev_lib import IntegrateData, stdev


class IntegrateVolatilityData(IntegrateData):

    def __init__(self, input_path, output_path, input_type='csv', output_type='csv'):
        super().__init__(input_path, output_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):
        if self.data is None:
            self.read_data()

        self.integrate_volatility_data()
        super().integrate_data()

    def integrate_volatility_data(self):

        def trailing_n_months_returns(row_idx, n=12, trailing_arr=[]):
            if row_idx < n:
                return trailing_n_months_returns(row_idx, n=row_idx, trailing_arr=trailing_arr)

            trailing_row_count = len(trailing_arr)
            new_rows_needed = n - trailing_row_count

            trailing_date = self.data.loc[row_idx - n, 'date']
            current_date = self.data.loc[row_idx, 'date']

            trailing_id = self.data.loc[row_idx - n, 'gvkey']
            current_id = self.data.loc[row_idx, 'gvkey']

            if month_difference(current_date, trailing_date) == n and trailing_id == current_id:
                return np.array([] + [self.data.loc[row_idx - i, 'prccm'] for i in range(new_rows_needed)])
            else:

                # stdev of [1] will always be zero, so this is effectively the dummy variable
                return np.array([1])

        def month_difference(date_1, date_2):
            def month(date): return (date // 100) % 100
            def year(date): return date // 10000
            return ((year(date_1) - year(date_2)) * 12) + (month(date_1) - month(date_2))


        def stdev_returns(row, n=12, arr=[]):
            return stdev(trailing_n_months_returns(row, n=n, arr=arr))

        def update_df(df):
            df['idx'] = df.index
            df['12_mo_stdev'] = df['idx'].apply(lambda row: stdev_returns(row))
            df['24_mo_stdev'] = df['idx'].apply(lambda row: stdev_returns(row, n=24))
            df['36_mo_stdev'] = df['idx'].apply(lambda row: stdev_returns(row, n=36))
            df.drop(['idx'], axis=1, inplace=True)

        update_df(self.data)


def main():

    # Defining our paths
    absolute_path = '/Users/ozzialkhayat/PycharmProjects/ceo-turnover/data/dev/'
    input_file = absolute_path + "csv_files/master_data_monthly.csv"
    output_file = absolute_path + "csv_files/master_data_monthly_v1.csv"

    # Instantiate IntegrateData object with input and output pointers
    volatility = IntegrateVolatilityData(input_file, output_file)

    # Run data integration pipeline
    volatility.process()
