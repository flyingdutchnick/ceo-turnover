""" Master file for libraries and classes repeatedly used in /dev"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class IntegrateData(ABC):

    def __init__(self, input_path, output_path, input_type='csv', output_type='csv'):
        self.input = input_path
        self.output = output_path
        self.input_type = input_type
        self.output_type = output_type
        self.data = None
        self.data_integrated = False

    @abstractmethod
    def integrate_data(self):
        self.data_integrated = True

    def read_data(self):
        if self.input_type == 'csv':
            self.data = pd.read_csv(self.input)
        elif self.input_type == 'pkl':
            self.data = pd.read_pickle(self.input)
        else:
            print("Unrecognized input file type")

    def write_data(self):
        if not self.data_integrated:
            print("Must integrate data before writing to new file")
        else:

            if self.output_type == 'csv':
                self.data.to_csv(self.output)
            elif self.output_type == 'pkl':
                self.data.to_pickle(self.output)
            else:
                print("Unrecognized output file type")

    def check_input_path(self):
        print(self.input)

    def print_output_path(self):
        print(self.output)

    def head(self):
        print(self.get_data_df().head())

    def get_data_df(self):
        return self.data


def array_avg(array):
    if isinstance(array, list):
        return np.sum(array) / len(array)
    elif isinstance(array, np.ndarray):
        return np.sum(array) / array.shape[0]
    else:
        print("Unrecognized input type for array_avg")
        return None


def squared_devs(array):
    average = array_avg(array)
    return np.array([(i - average) ** 2 for i in array])


def stdev(array):
    return (np.sum(squared_devs(array)) / array.shape[0]) ** 0.5


def pct_chg(current, historical):
    if historical != 0:
        return (current - historical) / historical
    else:
        return 0