import numpy as np
from data.dev.dev_lib import IntegrateData, stdev


class IntegrateVolatilityData(IntegrateData):

    def __init__(self, input_path, output_path, input_type='csv', output_type='csv', date_key=''):
        super().__init__(input_path, output_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):
        if self.data is None:
            self.read_data()

        self.integrate_volatility_data()
        super().integrate_data()

    def integrate_volatility_data(self):

        def trailing_n_months_returns(row, n=12):
            if row < n:
                return np.array([1])

            trailing_date = self.data.loc[row - n, 'date']
            current_date = self.data.loc[row, 'date']

            trailing_id = self.data.loc[row - n, 'gvkey']
            current_id = self.data.loc[row, 'gvkey']

            if month_difference(current_date, trailing_date) == n and trailing_id == current_id:
                return np.array([self.data.loc[row - i, 'prccm'] for i in range(n)])
            else:

                # stdev of [1] will always be zero, so this is effectively the dummy variable
                return np.array([1])

        def month_difference(date_1, date_2):
            def month(date): return (date // 100) % 100
            def year(date): return date // 10000
            return ((year(date_1) - year(date_2)) * 12) + (month(date_1) - month(date_2))

        def stdev_returns(row, n=12):
            return stdev(trailing_n_months_returns(row, n=n))

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
