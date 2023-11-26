import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DataVisualization:
    def __init__(self, title, x, y, z, k):
        """
        :parameter title: the "title" column of the full_table in Data.py
        :parameter x: the "Number of votes" column of the full_table in Data.py
        :parameter y: the "Average rating score" column of the full_table in Data.py
        :parameter z: the "Bayesian Average rating score" column of the full_table in Data.py
        :parameter k: the "Wilson lower bound" column of the full_table in Data.py
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

    def plot_boxplot(self):
        # Create a boxplot to compare the distributions of the three methods
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=[self.y, self.z, self.k], palette=['blue', 'orange', 'green'])
        plt.title('Boxplot Comparison of Rating Methods')
        plt.xlabel('Rating Method')
        plt.ylabel('Scores')
        plt.show()
