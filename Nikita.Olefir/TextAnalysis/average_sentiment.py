"""
This module contains the function calculate_avg_sentiment() that calculates the average sentiment score of a text column in a pandas DataFrame.
"""
from textblob import TextBlob
import pandas as pd

def calculate_avg_sentiment(dataframe: pd.DataFrame, column_names: str):
    """
    This functions calculates the average sentiment score of a text column in a pandas DataFrame and adds a column with sentiment scores for each record.

    Arguments:
        dataframe (pd.DataFrame): the input pandas DataFrame containing text data.
        column_names (list): the list of the column names of a pandas dataframe.

    Returns:
        float: the average sentiment score
    
    Examples:
        calculate_avg_sentiment(dataframe, column_name)

    """
    if column_names not in dataframe.columns:
        raise ValueError(f"The specified column '{column_names}' does not exist in the DataFrame.")

    def get_sentiment_score(text):
        analysis = TextBlob(str(text))
        return analysis.sentiment.polarity

    dataframe['Sentiment_Score'] = dataframe[column_names].apply(get_sentiment_score)

    non_zero_sentiments = dataframe[dataframe['Sentiment_Score'] != 0]

    avg_sentiment = non_zero_sentiments['Sentiment_Score'].mean()

    return avg_sentiment