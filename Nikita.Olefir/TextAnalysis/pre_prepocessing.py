"""
This module contains functions to hash text data and convert utc_time to a datetime format.
"""

import pandas as pd
import hashlib

def hash_text(dataframe: pd.DataFrame, column_name: str, hash_length: int = 10):
    """
    This function hashes text data in a column of the dataframe.

    Arguments:
        dataframe (pd.DataFrame): the input pandas DataFrame containing text data.
        column_name (str): the name of the column in a pandas dataframe.
        hash_length (int): the desired length of the hash (default is 10).

    Returns:
        pd.DataFrame: pandas dataframe with hashed text (in a specified column).
    
    Examples:
        hash_text(dataframe, "column_name")
    """    
    dataframe[column_name] = dataframe[column_name].apply(lambda x: hashlib.sha256(x.encode('utf-8')).hexdigest()[:hash_length])
    return dataframe

def change_time_format(dataframe: pd.DataFrame, column_name: str):
    """
    This function coverts utc_time to a datetime format

    Arguments:
        dataframe (pd.DataFrame): the input pandas DataFrame containing text data.
        column_name (str): the name of the column in a pandas dataframe.

    Returns:
        pd.DataFrame: pandas dataframe with utc_time converted to a datetime format (in a specified column).
    
    Examples:
        change_time_format(dataframe, "column_name")
    """    
    dataframe['created_datetime'] = pd.to_datetime(dataframe[column_name], unit='s')
    dataframe.drop(column_name, axis=1, inplace=True)

    return dataframe