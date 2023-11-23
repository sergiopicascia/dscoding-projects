import pandas as pd
import numpy as np


class DataSet:
    def __init__(self, data):
        self.data = data

    def clean_data(self):
        self.data = self.data.dropna(subset=['rating'])

    def calculate_game_statistics(self):
        self.clean_data()

        grouped_data = self.data.groupby('title')

        full_table = pd.DataFrame({
            'Sum of rating score': grouped_data['rating'].sum(),
            'Number of votes': grouped_data['rating'].count()
        }).reset_index()

        full_table['Average rating score'] = (
                full_table['Sum of rating score'] / full_table['Number of votes']
        )

        prior_weight = np.mean(full_table['Number of votes'])
        prior_mean = np.mean(full_table['Average rating score'])

        def bayesian_average_function(row):
            m = row['Average rating score']
            n = row['Number of votes']
            bayesian_avg = (prior_mean * prior_weight + m * n) / (prior_weight + n)
            return bayesian_avg

        full_table['Bayesian Average rating score'] = full_table.apply(lambda row: bayesian_average_function(row),
                                                                       axis=1)

        average_table = full_table[['title', 'Number of votes', 'Average rating score']]
        average_table = average_table.sort_values(by='Average rating score', ascending=False).reset_index(drop=True)

        bayesian_table = full_table[['title', 'Number of votes', 'Bayesian Average rating score']]
        bayesian_table = bayesian_table.sort_values(by='Bayesian Average rating score', ascending=False).reset_index(drop=True)

        return full_table, average_table, bayesian_table

