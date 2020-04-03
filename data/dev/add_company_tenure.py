import pandas as pd


def add_company_tenure(df):

    df["company_tenure"] = df["role_tenure"]

    df.sort_values(by=['role_tenure'], inplace=True, ascending=False)
    df.sort_values(by=['date', 'DirectorID', 'CompanyID'], inplace=True)

    for idx in range(1, df.shape[0]):
        if df.iloc[idx]["DirectorID"] != df.iloc[idx - 1]["DirectorID"] or \
                df.iloc[idx]["CompanyID"] != df.iloc[idx - 1]["CompanyID"]:
            pass

        elif df.iloc[idx]["date"] != df.iloc[idx - 1]["date"]:
            df.at[idx, "company_tenure"] = df.iloc[idx - 1]["company_tenure"] + (1 / 12)

        else:
            df.at[idx, "company_tenure"] = df.iloc[idx - 1]["company_tenure"]

    return df


def main():

    costco_data = pd.read_csv("csv_files/costco_data.csv")

    costco_data.drop([col for col in costco_data.columns if col not in
                      ['CompanyID', 'DirectorID', 'role_tenure', 'date', 'DateStartRole',
                       'date_end_role', 'DirectorName', 'CompanyName', 'RoleName']], axis=1, inplace=True)

    add_company_tenure(costco_data)

    print(costco_data)