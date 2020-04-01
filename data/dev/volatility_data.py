from dev_lib import IntegrateData
from tqdm import tqdm
from integrate_stock import IntegrateStockData
import warnings


class IntegrateVolatilityData(IntegrateData):

    def __init__(self, input_path, output_path, input_type='csv', output_type='csv', periods=(3, 6, 12)):
        self.vol_periods = periods
        super().__init__(input_path, output_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):

        # if we don't have trailing 1 month returns in our df, add them
        if 'trailing_1_mo_return' not in self.data.columns:
            IntegrateStockData(self.input, self.input, input_type=self.input_type, returns_to_calc=[1]).process()
            self.read_data()

        # save the index to a named column to use the apply function but keep track of the idx we are currently mapping
        self.data['unnamed'] = self.data.index

        # suppress FutureWarning from tqdm -> pandas calls
        warnings.simplefilter('ignore')

        # for each volatility period we would like to measure
        for n in self.vol_periods:
            tqdm.pandas(desc='Integrating {} month historical volatility'.format(n))

            # trailing n month volatility is standard deviation of trailing_1_mo returns over the prior n observations
            self.data['trailing_{}_mo_volatility'.format(n)] = self.data['unnamed'].progress_apply(
                lambda i: 0 if i < n or self.data.loc[max(i - n, 0), 'gvkey'] != self.data.loc[i, 'gvkey']
                else self.data.loc[i - n + 1:i,'trailing_1_mo_return'].std()
            )

        # call super, this will mark that data has been integrated and is ready to write to destination file
        super().integrate_data()


def main():

    # Defining our paths
    absolute_path = '/Users/ozzialkhayat/PycharmProjects/ceo-turnover/data/dev/'
    input_file = absolute_path + "csv_files/master_data_monthly.csv"
    output_file = absolute_path + "csv_files/master_data_monthly_v1.csv"

    # Instantiate IntegrateData object with input and output pointers
    volatility = IntegrateVolatilityData(input_file, output_file)

    # Run data integration pipeline
    volatility.process()
