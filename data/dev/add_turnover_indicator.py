import numpy as np
import datetime as datetime

master_data_path = ""


def add_turnover_indicator(df, window_before=12):

    def date_difference(date_1, date_2):
        if not isinstance(date_2, datetime.datetime):
            return window_before + 1
        else:
            return (date_2 - date_1) / np.timedelta64(1, 'M')

    def turnover_for_row(idx):
        current_date = df.iloc[idx]['Date']
        end_date = df.iloc[idx]['role_end_date']

        if date_difference(current_date, end_date) < window_before:
            return True
        else:
            return False

    df['temp_idx'] = df.index

    df['turnover_next_12_mo'] = df['temp_idx'].apply(lambda idx: turnover_for_row(idx))

    df.drop(['temp_idx'], axis=1, inplace=True)

