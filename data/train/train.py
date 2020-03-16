import pandas as pd
import random as rand


# Function: train_test_split()
# Inputs:
#      dataframe - a pandas DataFrame object containing data to be split into training and testing sets
#      *group_by - the axis along which to group and split data, set to 'gvkey' by default
#      *test_prop - the rough proportion of data assigned to test set, set to 0.2 by default
# Outputs:
#      a double (2 element tuple) of pandas DataFrame objects,
#      where the first element is the training set, second element is testing set
def train_test_split(dataframe, group_by='gvkey', test_prop=0.2):

    # start with two empty lists to dynamically store data
    train_data, test_data = [], []

    # keep track of the prior group_by value to check whether we have changed characteristics
    prev_id = dataframe.loc[0, group_by]

    # keep track of iteration indices
    start_idx = 0
    iter_idx = 1

    # we need the array to be sorted by the group_by axis to ensure comprehensive groupings
    dataframe.sort_values(by=[group_by])

    # loop through input df, group maximal sets of contiguous rows representing the same characteristic
    # assign those sets to either train_data or test_data based on test_prop
    while iter_idx < len(dataframe):

        # if the previous row referenced the same characteristic, increment iter_idx (but do nothing else)
        if dataframe.loc[iter_idx, group_by] == prev_id:
            iter_idx += 1

        # otherwise, we have passed all observations referencing a given characteristic
        else:

            # add all data for that characteristic to either training or testing data sets
            data_for_training = rand.random() > test_prop
            contiguous_ids = dataframe[start_idx:iter_idx]
            if data_for_training:
                print(contiguous_ids.shape)
                train_data.append(contiguous_ids)
            else:
                test_data.append(contiguous_ids)
                print(iter_idx)

            # update tracking + iteration data and continue looping
            prev_id = dataframe.loc[iter_idx, group_by]
            start_idx = iter_idx
            iter_idx += 1

    # instantiate the output dfs using the lists of partial dfs
    train_df, test_df = pd.concat(train_data, axis=0), pd.concat(test_data, axis=0)

    # reset indices because we have done a lot of slicing
    train_df.reset_index(inplace=True, drop=True)
    test_df.reset_index(inplace=True, drop=True)

    # return df object containing training data, df object containing test data
    return train_df, test_df
