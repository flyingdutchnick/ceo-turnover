from data.dev.dev_lib import IntegrateData, FactoryIntegrateData


# Define an IntegrateData subclass to transform monthly data into yearly data
class MakeYearly(IntegrateData):

    def __init__(self, in_file, out_file, date_col='date', date_form='YYYYMMDD'):
        self.date_column = date_col
        self.date_format = date_form
        super().__init__(in_file, out_file)

    def integrate_data(self):
        if self.date_format == 'YYYYMMDD':
            self.data.drop(self.data[(self.data[self.date_column] // 100) % 100 != 1].index, inplace=True)
        elif self.date_format == 'YYYYMMMDD':
            self.data.drop(self.data["JAN" not in (self.data[self.date_column])].index, inplace=True)
        else:
            print("Unrecognized date format")
            return

        super().integrate_data()


# Example of the FactoryIntegrateData class in action, this is functionally equivalent to main()
def factory_integrate_example():
    in_path = "csv_files/master_data_monthly_v2.csv"
    out_path = "csv_files/master_data_yearly_v0.csv"

    def monthly_to_yearly(df):
        return df.drop(df[(df['date'] // 100) % 100 != 1].index)

    data = FactoryIntegrateData(in_path, out_path, monthly_to_yearly)
    data.process()


# Execute the data transform from monthly to yearly
def main():
    in_path = "csv_files/master_data_monthly_v2.csv"
    out_path = "csv_files/master_data_yearly_v0.csv"

    data = MakeYearly(in_path, out_path)
    data.process()

