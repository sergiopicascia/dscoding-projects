"""
This module includes WordReplacer class and related method to replace words in a column in a pandas dataframe
"""
import pandas as pd
import re


class WordReplacer(object):
    """
    A class for replacing words in a pandas DataFrame.

    Method:
    - replace_words(column_name:str, word_mapping:dict): Replace specified words in a pandas dataframe
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the TextPreprocessor object.

        Arguments:
            dataframe (pd.DataFrame): The input pandas DataFrame containing text data.
        """
        self.dataframe = dataframe

    def replace_words(self, column_name: str, word_mapping: dict):
        """
        Replaces specified words in a column of the Pandas DataFrame using a custom function.

        Arguments:
            column_name(str): the name of the column in a pandas dataframe.
            word_mapping(dict): Dictionary where keys are words to be replaced and values are their replacements

        Returns:
            pd.DataFrame: pandas dataframe with the substituted words

        Examples:
            word_mapping = {'house': 'apartment','Milano': 'Milan'}. Replace 'house' with 'apartment', 'Milano' with 'Milan'
        """
        df_copy = self.dataframe.copy()

        def custom_replace(text: str):
            for word, replacement in word_mapping.items():
                pattern = r"\b{}\b".format(re.escape(word))
                text = re.sub(pattern, replacement, text)
            return text

        df_copy[column_name] = df_copy[column_name].apply(custom_replace)

        return df_copy
