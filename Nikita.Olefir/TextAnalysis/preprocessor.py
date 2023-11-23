"""
This module includes TextPreprocessor class and related methods to preprocess text data in a pandas dataframe
"""
import string
import re
import spacy
import pandas as pd


# python -m spacy download en_core_web_sm
# after importing spacy, run the above command to download the list of the stopwords
class TextPreprocessor(object):
    """
    A class for preprocessing text data in a pandas DataFrame.

    Methods:
    - text_to_lower_case(column_name:str): Transform text to lowercase in the specified column.
    - remove_links(column_name:str): Remove hyperlinks from the text in the specified column.
    - remove_punctuations(column_name:str): Remove punctuations from the text in the specified column.
    - remove_stopwords(column_name:str): Remove stopwords from the text in the specified column.
    - remove_special_characters(column_name:str): Remove special characters from the text in the specified column.
    - remove_words_with_small_length(column_name:str): Remove words with length less than 3 from the text in the specified column.
    - mask_curse_words(column_name:str, curse_word_list=None): Mask specified curse words in the text of the specified column.
    - apply_all(column_name:str): Apply all preprocessing steps to the text in the specified column.

    Arguments:
        dataframe (pd.DataFrame): The input pandas DataFrame containing text data.
    """

    def __init__(self, dataframe: pd.DataFrame):
        """
        Initialize the TextPreprocessor object.

        Arguments:
            dataframe (pd.DataFrame): the input pandas DataFrame containing text data.
        """
        self.dataframe = dataframe

    def text_to_lower_case(self, column_name: str):
        """
        Transfroms all text of the column in a pandas dataframe to the lower case.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text in lower case (in a specified column).
        """
        self.dataframe[column_name] = self.dataframe[column_name].str.lower()
        return self

    def remove_links(self, column_name: str):
        """
        Removes all links in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout links (in a specified column).
        """
        self.dataframe[column_name] = self.dataframe[column_name].apply(
            lambda x: re.sub(r"http\S+", "", x)
        )
        return self

    def remove_punctuations(self, column_name: str):
        """
        Removes all punctuations in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout punctuations (in a specified column).
        """
        punctuations = string.punctuation
        additional_chars = ["…", "\\"]
        all_chars_to_remove = punctuations + "".join(additional_chars)
        self.dataframe[column_name] = self.dataframe[column_name].apply(
            lambda x: x.translate(str.maketrans("", "", all_chars_to_remove))
        )
        return self

    def remove_stopwords(self, column_name: str):
        """
        Removes all stopwords in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout stopwords (in a specified column).
        """
        nlp = spacy.load("en_core_web_sm")

        def remove_stopwords_from_text(text: str):
            doc = nlp(text)
            return " ".join([token.text for token in doc if not token.is_stop])

        self.dataframe[column_name] = self.dataframe[column_name].apply(
            remove_stopwords_from_text
        )
        return self

    def remove_special_characters(self, column_name: str):
        """
        Removes all special characters in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout special characters (in a specified column).
        """
        self.dataframe[column_name] = self.dataframe[column_name].apply(
            lambda x: re.sub(r"[^a-zA-Z0-9]", " ", x)
        )
        self.dataframe[column_name] = self.dataframe[column_name].apply(
            lambda x: re.sub(r"\s+", " ", x)
        )
        return self

    def remove_words_with_small_length(self, column_name: str):
        """
        Removes all words that consist of less than 3 words in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout special characters (in a specified column).
        """
        self.dataframe[column_name] = self.dataframe[column_name].apply(
            lambda x: " ".join([word for word in x.split() if len(word) > 2])
        )
        return self

    def mask_curse_words(self, column_name: str, curse_word_list=None):
        """
        Mask all the specified curse words in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.
            curse_word_list (list, optional): the list of curse words to mask. Defaults to None.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout curse words masked (in a specified column).
        """
        if curse_word_list is None:
            curse_word_list = ["fuck", "fucking", "dipshit", "shit", "shiiit", "cunt", "garbage"]
        pattern = re.compile(
            r"\b(?:" + "|".join(curse_word_list) + r")\b", flags=re.IGNORECASE
        )

        def mask_text(text: str):
            def mask_word(match):
                word = match.group(0)
                return word[:2] + "*" * (len(word) - 2)

            return pattern.sub(mask_word, text)

        self.dataframe[column_name] = self.dataframe[column_name].apply(mask_text)
        return self

    def apply_all(self, column_name: str):
        """
        Applies all of the above function to the text in a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with all the functions applied (in a specified column).
        """
        return (
            self.text_to_lower_case(column_name)
            .remove_links(column_name)
            .remove_punctuations(column_name)
            .remove_stopwords(column_name)
            .remove_special_characters(column_name)
            .remove_words_with_small_length(column_name)
            .mask_curse_words(column_name)
            .dataframe
        )
