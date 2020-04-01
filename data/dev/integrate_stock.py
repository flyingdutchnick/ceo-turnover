import pandas as pd
from tqdm import tqdm
import warnings
from dev_lib import IntegrateData, pct_chg


class IntegrateStockData(IntegrateData):

    def __init__(self, in_path, out_path, returns_to_calc=(3, 6, 12, 24, 36), input_type='csv', output_type='csv'):
        self.returns_lengths = returns_to_calc
        super().__init__(in_path, out_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):
        # make sure we have the correct date format
        self.construct_date_from_datadate()

        # sort data so all observations for each company are contiguous and chronological, then reset index
        self.data.sort_values(by=['sic', 'gvkey', 'date'], inplace=True)
        self.data.reset_index(drop=True, inplace=True)

        # save the index to a named column to use the apply function but keep track of the idx we are currently mapping
        self.data['Unnamed'] = self.data.index

        # ignore FutureWarning from tqdm -> pandas call
        warnings.simplefilter('ignore')

        # for each returns period we would like to measure
        for return_len in self.returns_lengths:
            col_label = "trailing_{}_mo_return".format(return_len)
            tqdm.pandas(desc='Integrating {} month trailing returns'.format(return_len))

            self.data[col_label] = self.data['Unnamed'].progress_apply(
                lambda x: self.trailing_n_months_return(x, n=return_len))

        # call super, this will mark that data has been integrated and is ready to write to destination file
        super().integrate_data()

    def construct_date_from_datadate(self):
        try:
            self.data['date'] = pd.to_datetime(self.data['datadate'], format='%m/%d/%Y')
        except KeyError:
            mon_to_int = {'JAN':'01', 'FEB':'02', 'MAR':'03', 'APR':'04', 'MAY':'05',
                          'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09', 'OCT':'10',
                          'NOV':'11', 'DEC':'12'}
            self.data['datadate'] = self.data['datadate'].apply(
                lambda date : mon_to_int[date[2:5]] + '/' + date[0:2] + '/' + date[5:9])
            self.data['date'] = pd.to_datetime(self.data['datadate'], format='%m/%d/%Y')

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