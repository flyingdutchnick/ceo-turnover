import numpy as np
import pandas as pd
from dev_lib import IntegrateData, stdev


class IntegrateConversionData(IntegrateData):

    def __init__(self, input_path, new_data, output_path, input_type='csv', conversion_type='csv', output_type='csv'):
        self.conversion_path = new_data
        self.conversion_data = None
        self.conversion_type = conversion_type

        super().__init__(input_path, output_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):
        conversion_df = self.age_data
        master_df = self.data

        #Executing the inner join
        current_data = pd.merge(master_df, conversion_df, how="inner", left_on="CompanyID", right_on="COMPANYID")

        #Only keeping "CEO"s
        self.data = current_data

        #Integrating with master
        super().integrate_data()


    def read_data(self):
        if self.conversion_type == 'csv':
            self.conversion_data = pd.read_csv(self.conversion_path)
        elif self.conversion_type == 's3':
            self.conversion_data = self.read_s3_to_df(self.conversion_path)
        super().read_data()


def main():

    in_path = "Checkpoints/master_v1.csv"
    new = "conversion_dataset.csv"
    out_path = "Checkpoints/master_v2.csv"

    data = IntegrateConversionData(in_path, new, out_path)
    data.process()
