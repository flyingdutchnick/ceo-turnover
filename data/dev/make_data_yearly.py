from dev_lib import IntegrateData, FactoryIntegrateData


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


def monthly_to_yearly(data):
    return data.drop(data[(data['date'] // 100) % 100 != 1].index)


def main():
    in_path = "csv_files/master_data_monthly_v2.csv"
    out_path = "csv_files/master_data_yearly_v0.csv"

    data = FactoryIntegrateData(in_path, out_path, monthly_to_yearly)
    data.process()


main()
