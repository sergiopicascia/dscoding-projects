"""
This module includes TextStemLem class and related methods to create
columns with stemmed and lemmatized words from a column in a pandas dataframe
"""
import pandas as pd
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk
from contextlib import redirect_stdout
from io import StringIO

with StringIO() as captured_output, redirect_stdout(captured_output):
    nltk.download('wordnet')

class TextStemLem(object):
    """
    A class for to create columns with stemmed and lemmatized words from a column in a pandas DataFrame.

    Methods:
    - stem_words(column_name:str): Create a new column with stemmed words from the specified column.
    - lemmatize_words(column_name:str): Create a new column with lemmatized words from the specified column.
    """    
    def __init__(self, dataframe:pd.DataFrame):
        """
        Initialize the TextPreprocessor object.

        Arguments:
            dataframe (pd.DataFrame): The input pandas DataFrame containing text data.
        """        
        self.dataframe = dataframe

    def stem_words(self, column_name:str):
        """
        Create a new column with stemmed words from the specified column.

        Arguments:
            column_name (str): The name of the column in the pandas dataframe.

        Returns:
            pd.DataFrame: A pandas dataframe with an additional column containing stemmed words.
        """
        ps = PorterStemmer()
        self.dataframe['stemmed_words'] = self.dataframe[column_name].apply(
            lambda x: ' '.join([ps.stem(word) for word in x.split()])
        )
        return self.dataframe

    def lemmatize_words(self, column_name:str):
        """
        Create a new column with lemmatized words from the specified column.

        Arguments:
            column_name (str): The name of the column in the pandas dataframe.

        Returns:
            pd.DataFrame: A pandas dataframe with an additional column containing lemmatized words.
        """
        lemmatizer = WordNetLemmatizer()
        self.dataframe['lemmatized_words'] = self.dataframe[column_name].apply(
            lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()])
        )
        return self.dataframe