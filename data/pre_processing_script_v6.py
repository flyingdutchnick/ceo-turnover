# importing packages
import pandas as pd
import numpy as np


# Reading in the data
updated_data = pd.read_csv("pre_processed_v5_CEO.csv")


# Data clean-up
updated_data["Role Tenure"] = updated_data["Tenure (Years)"]
updated_data.rename(columns={"Tenure (Years)": "Company Tenure"}, inplace=True)
updated_data.drop(columns=['Unnamed: 0'], inplace=True)

# Creating a "rows" array that contains all the rows of the dataframe as entries
rows = []
for row in updated_data.iterrows():
    rows.append(row[1])


# Creating the dictionary with each company name as the key and an array of
# corresponding rows as the values
dataDict = dict()
for i in np.arange(len(rows)):
    current_company = rows[i]["Company Name"]
    if current_company not in dataDict.keys():
        dataDict[current_company] = [rows[i]]
    else:
        current_company_values = dataDict.get(current_company)
        current_company_values.append(rows[i])
        dataDict[current_company] = current_company_values


#Creating a helper function to sort the values of the dictionary
#entries by year
def sorting_function(company_values):
    n = len(company_values)
    for i in range(n):
        for j in range(0, n-i-1):
            if company_values[j]["Year"] > company_values[j+1]["Year"]:
                company_values[j], company_values[j+1] = company_values[j+1],
                company_values[j]


#Update tenure helper function
def update_tenures(curr_company):
    n = len(curr_company)
    sorting_function(curr_company)
    for i in range(n):
        for j in range(n):
            if (curr_company[i]["Director Name"] ==
                curr_company[j]["Director Name"]
                and curr_company[i]["Company Name"] ==
                curr_company[j]["Company Name"]):
                    t1 = curr_company[i]["Company Tenure"]
                    t2 = curr_company[j]["Company Tenure"]
                    age_diff = curr_company[i]["Ages"]-curr_company[j]["Ages"]
                    t2 += age_diff
                    if age_diff == 0:
                        curr_company[i]["Company Tenure"] = max(t1, t2)
                        curr_company[j]["Company Tenure"] = max(t1, t2)
                    elif age_diff > 0:
                        curr_company[i]["Company Tenure"] = max(t1, t2)


#Updating the tenures - this part takes ~8 minutes to run
company_names_array = np.array(sorted(dataDict.keys()))
for curr_company in company_names_array:
    update_tenures(dataDict[curr_company])


#Reconstructing the dataframe - this part takes ~28 minutes to run
final_data = pd.DataFrame()
for curr_company in company_names_array:
    curr_company_df = pd.DataFrame.from_dict(dataDict[curr_company])
    final_data = final_data.append(curr_company_df)


#Exporting to CSV
final_data.to_csv("processed_data_v6.csv")
