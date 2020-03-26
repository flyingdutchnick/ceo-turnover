import pandas as pd
from data.dev.dev_lib import IntegrateData


class MakePanel(IntegrateData):

    def __init__(self, input_path, output_path, input_type='csv', output_type='csv'):
        super().__init__(input_path, output_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):

        #Creating the panel_data dataframe
        panel_data = self.data
        
        #Saving the original column names
        original_columns = list(panel_data.columns)

        #Saving each row of the array to an individual entry of a "row_list" list
        row_list = []
        for index, row_data in panel_data.iterrows():
            curr_list = list(row_data)
            row_list.append(curr_list)

        #Creating the pannel dataset
        final_list = []

        for row in row_list:
            initial_year = int(row[-1])
            initial_tenure = int(row[-4])
            initial_age = int(row[-2])

            for i in range(initial_tenure + 1):
            
                #copy the row
                row_copy = row[:]

                #add new row with change in age
                row_copy[-2] = initial_age - i
            
                #add new row with change in tenure
                row_copy[-4] = initial_tenure - i
        
                #add new row with change in year
                row_copy[-1] = initial_year - i
        
                #account for turnover event
                if i > 0:
                    row_copy[-7] = False
        
                #update the final list
                final_list.append(row_copy)
        
        #Recreating the dataframe
        panel_data = pd.DataFrame(final_list)

        #Re-assinging the original column names
        panel_data.columns = original_columns

        #Updating
        self.data = panel_data

        #Calling the integrate_data function
        super().integrate_data()


def main():

    in_path = "Checkpoints/master_v2.csv"
    out_path = "Checkpoints/master_v3.csv"

    data = MakePanel(in_path, out_path)
    data.process()


main()