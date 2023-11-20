import string
import re
import spacy

# python -m spacy download en_core_web_sm
class TextPreprocessor:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def text_to_lower_case(self, column_name):
        """Transfroms all text of the column in a pandas dataframe to the lower case.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text in lower case (in a specified column).
        """
        self.dataframe[column_name] = self.dataframe[column_name].str.lower()
        return self

    def remove_links(self, column_name):
        """Removes all links in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout links (in a specified column).
        """
        self.dataframe[column_name] = self.dataframe[column_name].apply(
            lambda x: re.sub(r"http\S+", "", x)
        )
        return self

    def remove_punctuations(self, column_name):
        """Removes all punctuations in the text of a specified column in a pandas dataframe.

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

    def remove_stopwords(self, column_name):
        """Removes all stopwords in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout stopwords (in a specified column).
        """
        nlp = spacy.load("en_core_web_sm")

        def remove_stopwords_from_text(text):
            doc = nlp(text)
            return " ".join([token.text for token in doc if not token.is_stop])

        self.dataframe[column_name] = self.dataframe[column_name].apply(
            remove_stopwords_from_text
        )
        return self

    def remove_special_characters(self, column_name):
        """Removes all special characters in the text of a specified column in a pandas dataframe.

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

    def remove_words_with_small_length(self, column_name):
        """Removes all words that consist of less than 3 words in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout special characters (in a specified column).
        """
        self.dataframe[column_name] = self.dataframe[column_name].apply(
            lambda x: " ".join([word for word in x.split() if len(word) > 2])
        )
        return self

    def mask_curse_words(self, column_name, curse_word_list=None):
        """Mask all the specified curse words in the text of a specified column in a pandas dataframe.

        Arguments:
            column_name (str): the name of the column in a pandas dataframe.
            curse_word_list (list, optional): the list of curse words to mask. Defaults to None.

        Returns:
            pd.DataFrame: pandas dataframe with the text witout curse words masked (in a specified column).
        """
        if curse_word_list is None:
            curse_word_list = ["fuck", "fucking", "dipshit", "shit", "shiiit", "cunt"]
        pattern = re.compile(
            r"\b(?:" + "|".join(curse_word_list) + r")\b", flags=re.IGNORECASE
        )

        def mask_text(text):
            def mask_word(match):
                word = match.group(0)
                return word[:2] + "*" * (len(word) - 2)

            return pattern.sub(mask_word, text)

        self.dataframe[column_name] = self.dataframe[column_name].apply(mask_text)
        return self

    def apply_all(self, column_name):
        """Applies all of the above function to the text in a specified column in a pandas dataframe.

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
