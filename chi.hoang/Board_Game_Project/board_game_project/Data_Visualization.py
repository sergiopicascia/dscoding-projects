import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DataVisualization:
    def __init__(self, title, x, y, z, k):
        """
        :param title: the "title" column of the full_table in Data.py
        :param x: the "Number of votes" column of the full_table in Data.py
        :param y: the "Average rating score" column of the full_table in Data.py
        :param z: the "Bayesian Average rating score" column of the full_table in Data.py
        :param k: the "Wilson lower bound" column of the full_table in Data.py
        """
        self.title = title
        self.x = x
        self.y = y
        self.z = z
        self.k = k

    def _plot_ratings(self, x_data, y_data, color, x_label, y_label, title):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Scatter plot
        ax1.scatter(x_data, y_data, c=color)
        ax1.set_xlabel('Number of votes')
        ax1.set_ylabel(y_label)
        ax1.set_title(title)
        ax1.grid(True)

        # Histogram
        sns.histplot(y_data, kde=True, ax=ax2, color=color)
        ax2.set_xlabel(y_label)
        ax2.set_ylabel('Frequency')
        ax2.set_title(f'Distribution of {y_label}')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

        # Calculate and print the variance of y_data
        variance = y_data.var()
        print(f"Variance of {y_label}:", variance)

    def plot_average_ranking(self):
        # Plot average ranking based on average scores
        self._plot_ratings(self.x, self.y, 'b', 'Number of votes', 'Average scores', 'Game ratings based on Average '
                                                                                     'scores')

    def plot_bayesian_ranking(self):
        # Plot ranking based on Bayesian average scores
        self._plot_ratings(self.x, self.z, 'c', 'Number of votes', 'Bayesian average scores',
                           'Game ratings based on Bayesian average scores')

    def plot_wilson_lower_bound(self):
        # Plot ranking based on Wilson lower bound
        self._plot_ratings(self.x, self.k, 'c', 'Number of votes', 'Wilson scores',
                           'Game ratings based on Wilson lower bound')

    def compare_rankings_table(self):
        # Generate a table of absolute differences in ranking
        print("Table of absolute difference in ranking")
        rankings_df = pd.DataFrame({
            'Game Title': self.title,
            'Average Rating Score': self.y,
            'Bayesian Average Rating Score': self.z,
            'Wilson lower bound': self.k,
            'Absolute Difference 1': abs(self.y - self.z),
            'Absolute Difference 2': abs(self.y - self.k)
        })
        self._plot_absolute_differences(rankings_df)

    def _plot_absolute_differences(self, rankings_df):
        # Plot the absolute differences in rankings
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Game Title', y='Absolute Difference 1', data=rankings_df, color='blue', label='Avg vs Bayesian')
        sns.barplot(x='Game Title', y='Absolute Difference 2', data=rankings_df, color='green', label='Avg vs Wilson')

        plt.title('Absolute Differences in Rankings Comparison')
        plt.xlabel('Game Title')
        plt.ylabel('Absolute Difference in Ranking')
        plt.legend()
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        return rankings_df
