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


def word_length_distribution(dataframe, column_name):
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
    return plt.show()


def calculate_word_statistics(dataframe, column_name):
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


def plot_most_frequent_words(dataframe, text_column, top_n=10):
    word_counts = Counter(dataframe[text_column].str.split().sum())

    most_common_words = word_counts.most_common(top_n)

    words, counts = zip(*most_common_words)
    plt.bar(words, counts, color="skyblue")
    plt.title(f"Top {top_n} Most Frequent Words")
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.xticks(rotation=90)
    plt.show()
