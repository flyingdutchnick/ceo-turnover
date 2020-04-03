from pandas import read_csv, merge
from dev_lib import IntegrateData
from tqdm import tqdm


class MergeSPWithMaster(IntegrateData):

    def __init__(self, input_master, input_sp, output_path, input_type='csv', output_type='csv', sp_type='csv'):
        self.sp_path = input_sp
        self.sp_data = None
        self.sp_type = sp_type

        super().__init__(input_master, output_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):
        sp_df = self.sp_data
        master_df = self.data

        master_df['matched_date'] = master_df['datadate'].apply(
            lambda date: int(date[-4:] + date[0:2]) if '/' not in date[0:2] else int(date[-4:] + '0' + date[0]))
        sp_df['matched_date'] = sp_df['Date'].apply(lambda date: date // 100)

        tqdm.pandas(desc='Merging stock performance and market performance datasets')
        self.data = merge(master_df, sp_df, how='inner', left_on='matched_date', right_on='matched_date').\
            progress_apply(lambda x: x)

        super().integrate_data()

    def read_data(self):
        if self.sp_type == 's3':
            self.sp_data = self.read_s3_to_df(self.sp_path)
        elif self.sp_type == 'csv':
            self.sp_data = read_csv(self.sp_path)

        super().read_data()


def main():

    in_master = 'csv_files/master_data_monthly_v1.csv'
    in_sp = 'csv_files/sp500-returns-volatility.csv'
    out_path = 'csv_files/master_data_monthly_v2.csv'

    data = MergeSPWithMaster(in_master, in_sp, out_path)
    data.process()
