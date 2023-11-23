"""
This module contains a function to calculate the sentiment of the comments and draw a graph with 5-minutes intervals when Milan was playing
"""
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

def analyze_sentiment_over_time(dataframe: pd.DataFrame, date_str: str, start_hour: int, end_hour: int, interval_minutes=5):
    """
    This functions calculates the sentiment of the comments using TextBlob on the specified date and time range, 
    and draws a graph with 5-minutes intervals when Milan was playing

    Arguments:
        dataframe(pd.DataFrame): the input pandas DataFrame containing text data.
        date_str(str): the date in the format 'YYYY-MM-DD'.
        start_hour(int): the starting hour of the time range for analysis (inclusive).
        end_hour(int): the ending hour of the time range for analysis (exclusive).
        interval_minutes(int, optional): the time interval in minutes for grouping data. Defaults to 5.
    
    Returns:
        A matplotlib plot with the sentiment analysis results over time.

    Example:
        analyze_sentiment_over_time(dataframe, '2023-10-10', 20, 23, interval_minutes=10)  
    
    """    

    dataframe['created_datetime'] = pd.to_datetime(dataframe['created_datetime'])

    filtered_data = dataframe[
        (dataframe['created_datetime'].dt.date == pd.to_datetime(date_str).date()) &
        (dataframe['created_datetime'].dt.hour >= start_hour) &
        (dataframe['created_datetime'].dt.hour < end_hour)
    ]

    filtered_data = filtered_data[filtered_data['body'].apply(lambda x: TextBlob(str(x)).sentiment.polarity != 0)]
    filtered_data = filtered_data.assign(sentiment=filtered_data['body'].apply(lambda x: TextBlob(str(x)).sentiment.polarity))

    minute_sentiment = filtered_data.groupby(
        [filtered_data['created_datetime'].dt.hour, (filtered_data['created_datetime'].dt.minute // interval_minutes) * interval_minutes],
        as_index=False
    ).agg({'sentiment': 'mean', 'created_datetime': 'first'})

    minute_sentiment['combined_datetime'] = minute_sentiment['created_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    if date_str == '2023-11-07':
        title = "The day Milan won (20:00 - 23:00 UTC)"
    elif date_str == '2023-10-25':
        title = "The day Milan lost (20:00 - 23:00 UTC)"
    else:
        title = "Incorrect date"

    plt.figure(figsize=(12, 10))
    plt.plot(minute_sentiment['combined_datetime'], minute_sentiment['sentiment'], marker='o')
    plt.title(f'{title}')
    plt.xlabel('Date and Time')
    plt.ylabel('Mean Sentiment')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.show()