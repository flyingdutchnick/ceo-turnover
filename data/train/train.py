import pandas as pd
import random as rand


data = pd.read_pickle('volatility_df.pkl')
data.drop(['Unnamed: 0'], axis=1, inplace=True)


def train_test_split(dataframe, group_by='gvkey', test_prop=0.2):

    # start with two empty lists to dynamically store data
    train_data, test_data = [], []

    # keep track of the prior company id to check whether we have changed companies
    prev_id = dataframe.loc[0, group_by]

    # keep track of iteration indices
    start_idx = 0
    iter_idx = 1

    # we need the array to be sorted by the group_by axis to ensure comprehensive groupings
    dataframe.sort_values(by=[group_by])

    # loop through input df, group maximal sets of contiguous rows representing the same company
    # assign those sets to either train_data or test_data based on test_prop
    while iter_idx < len(dataframe):
        if dataframe.loc[iter_idx, group_by] == prev_id:
            iter_idx += 1
        else:
            data_for_training = rand.random() > test_prop
            contiguous_ids = dataframe[start_idx:iter_idx]
            if data_for_training:
                print(contiguous_ids.shape)
                train_data.append(contiguous_ids)
            else:
                test_data.append(contiguous_ids)
                print(iter_idx)

            prev_id = dataframe.loc[iter_idx, group_by]
            start_idx = iter_idx
            iter_idx += 1

    train_df, test_df = pd.concat(train_data, axis=0), pd.concat(test_data, axis=0)

    train_df.reset_index(inplace=True, drop=True)
    test_df.reset_index(inplace=True, drop=True)

    return train_df, test_df


train, test = train_test_split(data)