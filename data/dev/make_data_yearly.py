from dev_lib import IntegrateData


class MakeYearly(IntegrateData):

    def __init__(self, in_file, out_file, date_col='date', date_form='YYYYMMDD'):
        self.date_column = date_col
        self.date_format = date_form
        super().__init__(in_file, out_file)

    def integrate_data(self):
        if self.date_form == 'YYYYMMDD':
            self.data.drop(self.data[(self.data[self.date_col] // 100) % 100 != 1].index, inplace=True)
        elif self.date_form == 'YYYYMMMDD':
            self.data.drop(self.data["JAN" not in (self.data[self.date_col])].index, inplace=True)
        else:
            print("Unrecognized date format")
            return

        super().integrate_data()


def main():
    in_path = "csv_files/master_data_monthly_v2.csv"
    out_path = "csv_files/master_data_yearly_v0.csv"

    data = MakeYearly(in_path, out_path)
    data.process()

