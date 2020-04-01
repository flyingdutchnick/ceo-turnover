""" Master file for classes and functions repeatedly used in /dev"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import time
import boto3


"""     Class: IntegrateData. This is the abstract superclass used to generalize data pre-processing 

        The motivation is that some data operations (ex, reading and writing to and from files) are identical,
        and the broad sequence of data reading, data integration, and data writing occurs for each pre-processing step.
        
        To define a non-abstract subclass of IntegrateData, one only needs to implement the integrate_data() function
        and constructor.  
        
        Once defined and instantiated, invoking the process() function will carry out all steps of pre-processing"""


class IntegrateData(ABC):

    # __init__() ... constructor
    #   input_path: file path to existing raw data
    #   output_path: file path to write pre-processed data to
    #   input_type: format to read input file, set to 'csv' by default
    #   output_type: format to write output file, set to 'csv' by default
    def __init__(self, input_path, output_path, input_type='csv', output_type='csv'):
        self.input = input_path
        self.output = output_path
        self.input_type = input_type
        self.output_type = output_type
        self.data = None
        self.data_integrated = False

    # runs through the sequence of reading, pre-processing, and writing data
    def process(self):
        self.read_data()
        self.integrate_data()
        self.drop_unnamed()
        self.write_data()

    # to be implemented by concrete subclasses
    @abstractmethod
    def integrate_data(self):
        self.data_integrated = True

    # reads and stores data from the input_path
    def read_data(self):
        if self.input_type == 'csv':
            self.data = pd.read_csv(self.input)
        elif self.input_type == 'pkl':
            self.data = pd.read_pickle(self.input)
        elif self.input_type == 's3':
            self.read_sagemaker()
        else:
            print("Unrecognized input file type")

    # writes stored data to the output_path
    def write_data(self):
        if not self.data_integrated:
            print("Must integrate data before writing to new file")
        else:

            if self.output_type == 'csv':
                self.data.to_csv(self.output)
            elif self.output_type == 'pkl':
                self.data.to_pickle(self.output)
            elif self.output_type == 's3':
                self.write_sagemaker()
            else:
                print("Unrecognized output file type")

    # prints a preview of stored data
    def print_head(self, n=5):
        if not isinstance(self.data, pd.DataFrame):
            print("Error accessing self.data, ensure input_file has been read and stored with read_data()")
        else:
            print(self.get_data_df().head(n=n))

    # getter for the internally stored data frame
    def get_data_df(self):
        return self.data

    # drop unnamed columns from data
    def drop_unnamed(self):
        self.data.drop([col for col in self.data.columns if 'unnamed' in col.lower()], axis=1, inplace=True)

    def read_sagemaker(self):
        bucket = 'sagemaker-us-east-1-936165954724/ceo-turnover'
        data_location = 's3://{}/{}'.format(bucket, self.input)
        self.data = pd.read_csv(data_location)

    def read_s3_to_df(self, location):
        return pd.read_csv('s3://{}/{}'.format('sagemaker-us-east-1-936165954724/ceo-turnover', location))

    def write_sagemaker(self):
        filename = self.output
        filepath = "ceo-turnover/" + self.output
        bucket = 'sagemaker-us-east-1-936165954724'
        self.data.to_csv(filename)

        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(filename, bucket, filepath)


class FactoryIntegrateData(IntegrateData):

    def __init__(self, in_file, out_file, integrate_function):
        self.in_function = integrate_function
        super().__init__(in_file, out_file)

    def integrate_data(self):
        self.data = self.in_function(self.data)
        super().integrate_data()



""" Below are helper methods which may be useful for pre-processing on multiple datasets"""


def timed_execution(func_to_execute):
    t0 = time.time()
    print("Beginning execution...")
    func_to_execute()
    t1 = time.time()
    print("Execution completed in {}s".format(round(t1 - t0, 2)))


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
