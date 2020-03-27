import numpy as np
import pandas as pd
from dev_lib import IntegrateData, stdev


class IntegrateConversionData(IntegrateData):

    def __init__(self, input_path, new_data, output_path):
        self.conversion_path = new_data
        self.conversion_data = None

        super().__init__(input_path, output_path)

    def integrate_data(self):
        conversion_df = self.age_data
        master_df = self.data

        #Executing the inner join
        current_data = pd.merge(master_df, conversion_data, how="inner", left_on="CompanyID", right_on="COMPANYID")

        #Only keeping "CEO"s
        self.data = current_data

        #Integrating with master
        super().integrate_data()


    def read_data(self):
        self.conversion_data = pd.read_csv(self.conversion_path)
        super().read_data()


def main():

    in_path = "Checkpoints/master_v1.csv"
    new = "conversion_dataset.csv"
    out_path = "Checkpoints/master_v2.csv"

    data = IntegrateConversionData(in_path, new, out_path)
    data.process()
