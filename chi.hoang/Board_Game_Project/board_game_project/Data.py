import pandas as pd
import numpy as np
import scipy.stats as st


class DataSet:
    def __init__(self, data):
        """
        Initialize the DataSet with input data.

        Parameter
        data: Input data containing game ratings. In this case it is 'bgg.csv'
        """
        self.data = data

    def clean_data(self):
        """
        Clean the data by removing rows with nan result.
        """
        self.data = self.data.dropna(subset=['rating'])

    def calculate_game_statistics(self):
        """
        Calculate various statistics for games, including the Average Rating Score,
        Bayesian Average Rating Score, and Wilson Lower Bound.

        Returns:
        - full_table: DataFrame containing various statistics for each game.
        - average_table: DataFrame sorted by Average Rating Score.
        - bayesian_table: DataFrame sorted by Bayesian Average Rating Score.
        - wilson_table: DataFrame sorted by Wilson Lower Bound.
        """

        # Clean the data
        self.clean_data()

        # Group data by game title
        grouped_data = self.data.groupby('title')

        # Create a full table with sum of rating scores, number of votes, and average rating score
        full_table = pd.DataFrame({
            'Sum of rating score': grouped_data['rating'].sum(),
            'Number of votes': grouped_data['rating'].count()
        }).reset_index()

        # Calculate Average Rating Score
        full_table['Average rating score'] = (
                full_table['Sum of rating score'] / full_table['Number of votes']
        )

        # Calculate Bayesian Average Rating Score
        prior_weight = np.mean(full_table['Number of votes'])
        prior_mean = np.mean(full_table['Average rating score'])

        def bayesian_average_function(row):
            m = row['Average rating score']
            n = row['Number of votes']
            bayesian_avg = (prior_mean * prior_weight + m * n) / (prior_weight + n)
            return bayesian_avg

        full_table['Bayesian Average rating score'] = full_table.apply(lambda row: bayesian_average_function(row),
                                                                       axis=1)

        # Calculate Wilson Lower Bound
        def wilson_score(positive, total, confidence=0.95):
            if total == 0:
                return 0
            z = st.norm.ppf(1 - (1 - confidence) / 2)
            p_hat = positive / total
            denominator = 1 + z ** 2 / total
            centre_adjusted_probability = p_hat + z ** 2 / (2 * total)
            variance_term = max((p_hat * (1 - p_hat) + z ** 2 / (4 * total)) / total, 0)
            adjusted_standard_deviation = np.sqrt(variance_term)
            lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) / denominator
            return lower_bound

        full_table['Wilson lower bound'] = full_table.apply(
            lambda row: wilson_score(row['Sum of rating score'], row['Number of votes']),
            axis=1)

        # Create tables sorted in descending order by different ranking methods
        average_table = full_table[['title', 'Number of votes', 'Average rating score']]
        average_table = average_table.sort_values(by='Average rating score', ascending=False).reset_index(drop=True)

        bayesian_table = full_table[['title', 'Number of votes', 'Bayesian Average rating score']]
        bayesian_table = bayesian_table.sort_values(by='Bayesian Average rating score', ascending=False).reset_index(
            drop=True)

        wilson_table = full_table[['title', 'Number of votes', 'Wilson lower bound']]
        wilson_table = wilson_table.sort_values(by='Wilson lower bound', ascending=False).reset_index(drop=True)

        return full_table, average_table, bayesian_table, wilson_table
