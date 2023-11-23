import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class DataVisualization:
    def __init__(self, title, x, y, z):
        self.title = title
        self.x = x
        self.y = y
        self.z = z

    def plot_average_ranking(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.scatter(self.x, self.y, c='b')
        ax1.set_xlabel('Number of votes')
        ax1.set_ylabel('Average scores')
        ax1.set_title('Game ratings based on Average scores')
        ax1.grid(True)

        sns.histplot(self.y, kde=True, ax=ax2, color='b')
        ax2.set_xlabel('Average scores')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Average Scores')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

        average_rating_variance = self.y.var()
        print("Variance of Average Rating Scores:", average_rating_variance)

    def plot_bayesian_ranking(self):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.scatter(self.x, self.z, c='c')
        ax1.set_xlabel('Number of votes')
        ax1.set_ylabel('Bayesian average scores')
        ax1.set_title('Game ratings based on Bayesian average scores')
        ax1.grid(True)

        sns.histplot(self.z, kde=True, ax=ax2, color='c')
        ax2.set_xlabel('Bayesian average scores')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Distribution of Bayesian Average Scores')
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

        bayesian_rating_variance = self.z.var()
        print("Variance of Bayesian Average Rating Scores:", bayesian_rating_variance)

    def compare_rankings_table(self):
        print("Table of absolute difference in ranking")
        rankings_df = pd.DataFrame({
            'Game Title': self.title,
            'Average Rating Score': self.y,
            'Bayesian Average Rating Score': self.z,
            'Absolute Difference': abs(self.y - self.z)
        })
        return rankings_df
