import numpy as np
from datetime import datetime
from data.dev.dev_lib import IntegrateData


class CleanTenure(IntegrateData):

    def __init__(self, input_path, output_path, input_type='csv', output_type='csv'):
        super().__init__(input_path, output_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):

        #Saving current data
        tenure_data = self.data

        #Dropping "N" (null) values in "DateStartRole"
        index_list = tenure_data[tenure_data["DateStartRole"] == 'N'].index.tolist()
        tenure_data.drop(index_list, inplace=True)

        #Dropping "N" (null) values in "DateEndRole"
        index_list = tenure_data[tenure_data["DateEndRole"] == 'N'].index.tolist()
        tenure_data.drop(index_list, inplace=True)

        #Creating the turnover column
        turnover_list = (tenure_data["DateEndRole"] != 'C').tolist()
        tenure_data["Turnover"] = turnover_list

        #Updating the "C" value (which denotes continuation) to be today's year
        end_data_list = tenure_data["DateEndRole"].tolist()
        n = len(end_data_list)
        for i in np.arange(n):
            if end_data_list[i] == "C":
                end_data_list[i] = datetime.today().strftime('%Y') 

        #Converting the "DateStartRole" column to ints
        for i in np.arange(n):
            end_data_list[i] = int(end_data_list[i][0:4])
        tenure_data["end_year"] = end_data_list

        #Converting the "DateStartRole" column to ints
        start_data_list = tenure_data["DateStartRole"].tolist()
        n = len(start_data_list)
        for i in np.arange(n):
            start_data_list[i] = int(start_data_list[i][0:4])
        tenure_data["start_year"] = start_data_list

        #dropping the "DateStartRole" and "DateEndRole" columns now that we have the year columns
        tenure_data.reset_index(inplace=True)
        tenure_data.drop(columns=['DateStartRole', 'DateEndRole','index'], inplace=True)

        #Creating the "role tenure" column
        tenure_list = abs(np.array(end_data_list) - np.array(start_data_list))
        tenure_data["role_tenure"] = tenure_list

        #Replacing the old data with the clean one
        self.data = tenure_data

        #Calling the integrate_data function
        super().integrate_data()


def main():

    in_path = "DirectorTurnoverData.csv"
    out_path = "Checkpoints/master_v1.csv"

    data = CleanTenure(in_path, out_path)
    data.process()

