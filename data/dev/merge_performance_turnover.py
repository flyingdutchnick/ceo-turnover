from dev_lib import IntegrateData
from pandas import read_csv


class MergePerformanceTurnover(IntegrateData):

    def __init__(self, performance_in, turnover_in, merged_out, perf_type='csv', turn_type='csv', merged_type='csv'):
        self.perform_path = performance_in
        self.perform_data = None
        self.perform_type = perf_type
        super().__init__(turnover_in, merged_out, input_type=turn_type, output_type=merged_type)

    def integrate_data(self):

        pass



    def read_data(self):
        if self.perform_type == 'csv':
            self.perform_data = read_csv(self.perform_path)
        elif self.perform_type == 's3':
            self.perform_data = self.read_s3_to_df(self.perform_path)