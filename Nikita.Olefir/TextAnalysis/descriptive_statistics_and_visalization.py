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


def word_length_distribution(dataframe: pd.DataFrame, column_names: list, figsize=(8, 5)):
    """
    Calculates the length of the words in a column of a pandas dataframe

    Arguments:
        dataframe (pd.DataFrame): the input pandas DataFrame containing text data.
        column_names (list): the list of the column names of a pandas dataframe.
        figsize (tuple): figure size, default is (8, 5).

    Returns:
        The function displays a histogram using Matplotlib.
    
    Examples:
        word_length_distribution(df,list_of_columns)
    """  
    num_columns = len(column_names)
    fig, axes = plt.subplots(1, num_columns, figsize=(figsize[0] * num_columns, figsize[1]))
  
    for i, column_name in enumerate(column_names):
        word_lengths = dataframe[column_name].apply(lambda x: len(x.split()))
        axes[i].hist(
            word_lengths,
            bins=np.arange(0, max(word_lengths) + 1, 1),
            alpha=0.75,
            edgecolor="black",
        )
        mean_length = word_lengths.mean()
        axes[i].axvline(mean_length, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_length:.2f}')
        
        axes[i].set_title(f"Distribution of Word Lengths in {column_name}")
        axes[i].set_xlabel("Word Length")
        axes[i].set_ylabel("Frequency")

    plt.show()


def calculate_word_statistics(dataframe:pd.DataFrame, column_names: list):
    """
    Calculates total number of words, the number of unique words, 
    average lenght of the words, median word length in a column of a 
    pandas dataframe

    Args:
        dataframe (pd.DataFrame): the input pandas DataFrame containing text data.
        column_name (list): the list of the column names of a pandas dataframe.

    Returns:
        pd.DataFrame: dataframe with the following columns:
        1) Total_Words
        2) Unique_Words
        3) Avg_Word_Length
        4) Median_Word_Length

    Examples:
        plot_most_frequent_words(df,'column_name')
    """    
    result_dfs = []

    for column_name in column_names:
        word_lengths = dataframe[column_name].apply(lambda x: len(x.split()))
        total_words = np.sum(word_lengths)
        unique_words = len(set(dataframe[column_name].str.split().sum()))
        avg_word_length = np.mean(word_lengths)
        median_word_length = np.median(word_lengths)

        column_stats = pd.DataFrame({
            'Column_Name': [column_name],
            'Total_Words': [total_words],
            'Unique_Words': [unique_words],
            'Avg_Word_Length': [avg_word_length],
            'Median_Word_Length': [median_word_length]
        })

        result_dfs.append(column_stats)

    result_df = pd.concat(result_dfs, axis=0, ignore_index=True)
    return result_df


def plot_most_frequent_words(dataframe:pd.DataFrame, column_names: list, top_n=10):
    """
    Finds the most frequently used words and shows the histrogram.

    Arguments:
        dataframe (pd.DataFrame): The input pandas DataFrame containing text data.
        column_name (list): the list of the column names of a pandas dataframe.
        top_n (int, optional): the number of the most frequent words to show. Defaults to 10.

    Returns:
        The function displays a histogram using Matplotlib.

    Examples:
        plot_most_frequent_words(df,'column_name', 20)
    """    
    num_columns = len(column_names)
    fig, axes = plt.subplots(1, num_columns, figsize=(8 * num_columns, 5))

    for i, column_name in enumerate(column_names):
        word_counts = Counter(dataframe[column_name].str.split().sum())
        most_common_words = word_counts.most_common(top_n)

        words, counts = zip(*most_common_words)
        axes[i].bar(words, counts, color="skyblue")
        axes[i].set_title(f"Top {top_n} Most Frequent Words in {column_name}")
        axes[i].set_xlabel("Word")
        axes[i].set_ylabel("Frequency")
        axes[i].tick_params(axis='x', rotation=90)

    plt.tight_layout()
    plt.show()
