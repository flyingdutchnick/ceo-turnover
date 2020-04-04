import pandas as pd
import numpy as np

def make_panel(file_path):

    data_no_panel = pd.read_csv(file_path)

    lst_of_panels = []
    for i in range(data_no_panel.shape[0]):
        start = data_no_panel.at[i, 'date_start_role']

        end = data_no_panel.at[i, 'date_end_role']
        if end == '-1':
            end = pd.to_datetime('today')

        date_range = pd.period_range(start=start, end=end, freq='M')

        date_diff = date_range.shape[0]

        row = data_no_panel.iloc[i]

        new_df = pd.concat([row] * date_diff, axis=1).transpose()
        new_df['date'] = date_range

        lst_of_panels.append(new_df)

    panel_data = pd.concat(lst_of_panels)

    panel_data.reset_index(inplace=True)

    def age_from_idx(idx):

        dob_datetime = pd.to_datetime(panel_data.at[idx, 'DOB'], format="%Y%m%d")
        date = np.datetime64(panel_data['date'][idx], 'M')

        return (date - dob_datetime) / np.timedelta64(12, 'M')

    panel_data['idx'] = panel_data.index
    panel_data['age'] = panel_data['idx'].apply(lambda idx: age_from_idx(idx))

