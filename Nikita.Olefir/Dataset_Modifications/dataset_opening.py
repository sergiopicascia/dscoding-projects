import pandas as pd
import os


def open_csv_as_dataframe(file_path: str):
    """This function opens a csv file as pandas dataframe

    Argumenst:
        file_path (str): the path to the csv file downloaded on a computer

    Returns:
       pd.DataFrame: returns a pandas dataframe

    ---

    Examples:
        open_csv_as_dataframe (/Users/user_name/documents/some_file.csv)
    """
    if os.path.exists(file_path):
        dataframe = pd.read_csv(file_path)
        return dataframe
    else:
        return print("File does not exist or the path is incorrect")
