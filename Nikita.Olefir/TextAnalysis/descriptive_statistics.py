"""
  This module includes functions for the collecting descriptive statistics from the data:
  
    1) The distribution of the words' length (+ graph)

    2) Calculation of the statistics regaridng words' appearances

    3) Indentification of the n most popular words (+graph)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def word_length_distribution(dataframe:pd.DataFrame, column_name:str):
    """
    Calculates the length of the words in a column of a pandas dataframe

    Arguments:
        dataframe (pd.DataFrame): The input pandas DataFrame containing text data.
        column_name (str): column_name (str): the name of the column in a pandas dataframe.

    Returns:
        The function displays a histogram using Matplotlib.
    
    Examples:
        word_length_distribution(df,'column_name')
    """    
    word_lengths = dataframe[column_name].apply(lambda x: len(x.split()))
    plt.hist(
        word_lengths,
        bins=np.arange(0, max(word_lengths) + 1, 1),
        alpha=0.75,
        edgecolor="black",
    )
    plt.title("Distribution of Word Lengths")
    plt.xlabel("Word Length")
    plt.ylabel("Frequency")
    plt.show()


def calculate_word_statistics(dataframe:pd.DataFrame, column_name:str):
    """
    Calculates total number of words, the number of unique words, 
    average lenght of the words, median word length in a column of a 
    pandas dataframe

    Args:
        dataframe (pd.DataFrame): The input pandas DataFrame containing text data.
        column_name (str): the name of the column in a pandas dataframe.

    Returns:
        pd.DataFrame: dataframe with the following columns:
        1) Total_Words
        2) Unique_Words
        3) Avg_Word_Length
        4) Median_Word_Length

    Examples:
        plot_most_frequent_words(df,'column_name')
    """    
    word_lengths = dataframe[column_name].apply(lambda x: len(x.split()))
    total_words = np.sum(word_lengths)
    unique_words = len(set(dataframe[column_name].str.split().sum()))
    avg_word_length = np.mean(word_lengths)
    median_word_length = np.median(word_lengths)

    statistics_df = pd.DataFrame({
        'Total_Words': [total_words],
        'Unique_Words': [unique_words],
        'Avg_Word_Length': [avg_word_length],
        'Median_Word_Length': [median_word_length]
    })
    return statistics_df


def plot_most_frequent_words(dataframe:pd.DataFrame, column_name:str, top_n=10):
    """
    Finds the most frequently used words and shows the histrogram.

    Arguments:
        dataframe (pd.DataFrame): The input pandas DataFrame containing text data.
        column_name (str): the name of the column in a pandas dataframe.
        top_n (int, optional): the number of the most frequent words to show. Defaults to 10.

    Returns:
        The function displays a histogram using Matplotlib.

    Examples:
        plot_most_frequent_words(df,'column_name', 20)
    """    
    word_counts = Counter(dataframe[column_name].str.split().sum())

    most_common_words = word_counts.most_common(top_n)

    words, counts = zip(*most_common_words)
    plt.bar(words, counts, color="skyblue")
    plt.title(f"Top {top_n} Most Frequent Words")
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.xticks(rotation=90)
    plt.show()
