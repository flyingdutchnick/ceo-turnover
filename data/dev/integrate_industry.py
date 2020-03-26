from pandas import read_csv, merge
from data.dev.dev_lib import IntegrateData


class IntegrateIndustry(IntegrateData):

    def __init__(self, in_master, out_master, industry_map, id_col='gvkey'):
        self.industry_path = industry_map
        self.industry_data = None
        self.id = id_col
        super().__init__(in_master, out_master)

    def integrate_data(self):
        self.industry_data.drop_duplicates(subset=self.id, inplace=True)
        self.data = merge(self.data, self.industry_data, how='inner', left_on=self.id, right_on=self.id)
        super().integrate_data()

    def read_data(self):
        self.industry_data = read_csv(self.industry_path)
        super().read_data()


def main():

    in_path = "csv_files/master_data_yearly_v0.csv"
    out_path = "csv_files/master_data_yearly_v1.csv"
    industry_map = "csv_files/CompustatIDMappings.csv"

    data = IntegrateIndustry(in_path, out_path, industry_map)
    data.process()


