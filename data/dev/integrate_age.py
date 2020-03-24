import numpy as np
import pandas as pd
from dev_lib import IntegrateData, stdev


class IntegrateAge(IntegrateData):

    def __init__(self, input_path, new_data, output_path):
        self.age_path = new_data
        self.age_data = None

        super().__init__(input_path, output_path)

    def integrate_data(self):
        age_df = self.age_data
        master_df = self.data

        #Dropping the null values of the age column
        index_list = age_df[age_df["DOB"] == 'n.a.'].index.tolist()
        age_df.drop(index_list, inplace=True)

        #Creating the column with only birth year and dropping the column with DOB strings
        n = age_df.shape[0]
        dob_year_list = []
        for i in np.arange(n):
            dob_year_list.append(int(age_df["DOB"][i].split(" ")[-1]))
        age_df["DOB_year"] = dob_year_list
        age_df.drop(columns=['DOB'], inplace=True)

        #Executing the inner join
        joined_df = pd.merge(left=master_df, right=age_df)

        #Creating the "age" column
        age_list = abs(np.array(joined_df["end_year"].tolist()) - np.array(joined_df["DOB_year"].tolist()))
        joined_df["age"] = age_list
        
        #Creating the "year" column
        joined_df["year"] = joined_df["end_year"]

        #Only keeping "CEO"s
        self.data = joined_df[joined_df["RoleName"].str.contains("CEO")]

        #Integrating with master
        super().integrate_data()
    
    def read_data(self):
        self.age_data = pd.read_csv(self.age_path)
        super().read_data()


def main():

    in_path = "Checkpoints/master_v1.csv"
    new = "DirectorIDByDOB.csv"
    out_path = "Checkpoints/master_v2.csv"

    data = IntegrateAge(in_path, new, out_path)
    data.process()


main()
