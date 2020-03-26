import numpy as np
import pandas as pd
from data.dev.dev_lib import IntegrateData, stdev


class CreateRoleTenure(IntegrateData):

    def __init__(self, input_path, output_path, input_type='csv', output_type='csv'):
        super().__init__(input_path, output_path, input_type=input_type, output_type=output_type)

    def integrate_data(self):

        #Copying the data
        panel_data = self.data

        #Data clean-up and sorting
        panel_data["company_tenure"] = panel_data["role_tenure"]
        panel_data.drop(columns=['Seniority', 'end_year', 'start_year', 'DOB_year'], inplace=True)
        panel_data.sort_values(["year", "CompanyName", "DirectorName"], inplace = True)

        #Creating a "rows" array that contains all the rows of the dataframe as entries
        rows = []
        for row in panel_data.iterrows():
            rows.append(row[1])

        #Creating the dictionary with each company name as the key and an array of
        #coresponding rows as the values
        dataDict = dict()
        for i in np.arange(len(rows)):
            current_company = rows[i]["CompanyName"]
            if current_company not in dataDict.keys():
                dataDict[current_company] = [rows[i]]
            else:
                current_company_values = dataDict.get(current_company)
                current_company_values.append(rows[i])
                dataDict[current_company] = current_company_values

        #Update tenure helper function
        def update_tenures(curr_company):
            n = len(curr_company)
            for i in range(n):
                for j in range(n):
                    if (curr_company[i]["DirectorName"] ==
                        curr_company[j]["DirectorName"]
                        and curr_company[i]["company_tenure"] ==
                        curr_company[j]["company_tenure"]):
                            t1 = curr_company[i]["company_tenure"]
                            t2 = curr_company[j]["company_tenure"]
                            age_diff = curr_company[i]["age"]-curr_company[j]["age"]
                            t2 += age_diff
                            if age_diff == 0:
                                curr_company[i]["company_tenure"] = max(t1, t2)
                                curr_company[j]["company_tenure"] = max(t1, t2)
                            elif age_diff > 0:
                                curr_company[i]["company_tenure"] = max(t1, t2)

        #Updating the tenures - this part takes ~8 minutes to run
        company_names_array = np.array(sorted(dataDict.keys()))
        for curr_company in company_names_array:
            update_tenures(dataDict[curr_company])

        #Reconstructing the dataframe - this part takes ~28 minutes to run
        final_data = pd.DataFrame()
        for curr_company in company_names_array:
            curr_company_df = pd.DataFrame.from_dict(dataDict[curr_company])
            final_data = final_data.append(curr_company_df)

        #Updating
        self.data = final_data

        #Calling the integrate_data function
        super().integrate_data()


def main():

    in_path = "Checkpoints/master_v3.csv"
    out_path = "Checkpoints/master_v4.csv"

    data = CreateRoleTenure(in_path, out_path)
    data.process()
