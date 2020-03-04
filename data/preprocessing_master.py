# This script will serve as the master script that, if executed, will
# take the raw data directly from WRDS and put it in the format that
# is most accessible for XGBoost


# ---------IMPORTING PACKAGES AND DATA---------#

import numpy as np
import pandas as pd

# We also need to import this package so that the "Today's date" function used when
# updating the tenure_data can update seamlessly
from datetime import datetime

# importing the data
age_data = pd.read_csv("DirectorIDByDOB.csv")
tenure_data = pd.read_csv("DirectorTurnoverData.csv")

# ---------EXECUTING A JOIN ON THE TWO DATA SETS + GENERAL CLEANING---------#

# ---- Cleaning age_data ----#

# Dropping the null values of the age column
index_list = age_data[age_data["DOB"] == 'n.a.'].index.tolist()
age_data.drop(index_list, inplace=True)

# Creating the column with only birth year and dropping the column with DOB strings
n = age_data.shape[0]
dob_year_list = []

for i in np.arange(n):
    dob_year_list.append(int(age_data["DOB"][i].split(" ")[-1]))
age_data["DOB_year"] = dob_year_list
age_data.drop(columns=['DOB'], inplace=True)

# ---- Cleaning tenure_data ----#

# Dropping "N" (null) values in "DateStartRole"
index_list = tenure_data[tenure_data["DateStartRole"] == 'N'].index.tolist()
tenure_data.drop(index_list, inplace=True)

# Dropping "N" (null) values in "DateEndRole"
index_list = tenure_data[tenure_data["DateEndRole"] == 'N'].index.tolist()
tenure_data.drop(index_list, inplace=True)

# Creating the turnover column
turnover_list = (tenure_data["DateEndRole"] != 'C').tolist()
tenure_data["Turnover"] = turnover_list

# Updating the "C" value (which denotes continuation) to be today's year
end_data_list = tenure_data["DateEndRole"].tolist()
n = len(end_data_list)

for i in np.arange(n):
    if end_data_list[i] == "C":
        end_data_list[i] = datetime.today().strftime('%Y')

# Converting the "DateStartRole" column to ints
for i in np.arange(n):
    end_data_list[i] = int(end_data_list[i][0:4])

tenure_data["end_year"] = end_data_list

# Converting the "DateStartRole" column to ints
start_data_list = tenure_data["DateStartRole"].tolist()
n = len(start_data_list)

for i in np.arange(n):
    start_data_list[i] = int(start_data_list[i][0:4])

tenure_data["start_year"] = start_data_list

# dropping the "DateStartRole" and "DateEndRole" columns now that we have the year columns
tenure_data.reset_index(inplace=True)
tenure_data.drop(columns=['DateStartRole', 'DateEndRole', 'index'], inplace=True)

# Creating the "role tenure" column
tenure_list = abs(np.array(end_data_list) - np.array(start_data_list))
tenure_data["role_tenure"] = tenure_list

# ---- Executing the inner join ----#

# Executing the inner join
joined_data = pd.merge(left=tenure_data, right=age_data)

# Creating the "age" column
age_list = abs(np.array(joined_data["end_year"].tolist()) - np.array(joined_data["DOB_year"].tolist()))
joined_data["age"] = age_list

# Creating the "year" column
joined_data["year"] = joined_data["end_year"]

# Only keeping "CEO" data
joined_data = joined_data[joined_data["RoleName"].str.contains("CEO")]

# ---------CONVERTING DATASET TO PANEL--------#


# Saving the original column names
original_columns = list(joined_data.columns)

# Saving each row of the array to an individual entry of a "row_list" list
row_list = []

for index, row_data in joined_data.iterrows():
    curr_list = list(row_data)
    row_list.append(curr_list)

# Creating the pannel dataset
final_list = []

for row in row_list:
    initial_year = int(row[-1])
    initial_tenure = int(row[-4])
    initial_age = int(row[-2])
    for i in range(initial_tenure + 1):

        # copy the row
        row_copy = row[:]

        # add new row with change in age
        row_copy[-2] = initial_age - i

        # add new row with change in tenure
        row_copy[-4] = initial_tenure - i

        # add new row with change in year
        row_copy[-1] = initial_year - i

        # account for turnover event
        if i > 0:
            row_copy[-7] = False

        # update the final list
        final_list.append(row_copy)

# Creating the panel_data df
panel_data = pd.DataFrame(final_list)

# ---------------HANDLING EDGE CASES--------------#

# Data clean-up and sorting
panel_data["company_tenure"] = panel_data["role_tenure"]
panel_data.drop(columns=['Seniority', 'end_year', 'start_year', 'DOB_year'], inplace=True)
panel_data.sort_values(["year", "CompanyName", "DirectorName"], inplace=True)

# Creating a "rows" array that contains all the rows of the dataframe as entries
rows = []
for row in panel_data.iterrows():
    rows.append(row[1])

# Creating the dictionary with each company name as the key and an array of
# coresponding rows as the values
dataDict = dict()
for i in np.arange(len(rows)):
    current_company = rows[i]["CompanyName"]
    if current_company not in dataDict.keys():
        dataDict[current_company] = [rows[i]]
    else:
        current_company_values = dataDict.get(current_company)
        current_company_values.append(rows[i])
        dataDict[current_company] = current_company_values


# Update tenure helper function
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
                age_diff = curr_company[i]["age"] - curr_company[j]["age"]
                t2 += age_diff
                if age_diff == 0:
                    curr_company[i]["company_tenure"] = max(t1, t2)
                    curr_company[j]["company_tenure"] = max(t1, t2)
                elif age_diff > 0:
                    curr_company[i]["company_tenure"] = max(t1, t2)


# Updating the tenures - this block alone takes ~8 minutes to run
company_names_array = np.array(sorted(dataDict.keys()))
for curr_company in company_names_array:
    update_tenures(dataDict[curr_company])

# Reconstructing the dataframe - this block alone takes ~28 minutes to run
final_data = pd.DataFrame()
for curr_company in company_names_array:
    curr_company_df = pd.DataFrame.from_dict(dataDict[curr_company])
    final_data = final_data.append(curr_company_df)

# Exporting to CSV
final_data.to_csv("pre_processed_v7_CEO.csv")
