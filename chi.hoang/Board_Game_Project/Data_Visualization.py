import matplotlib.pyplot as plt


class DataVisualization:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def plot_average_ranking(self):
        fig, ax = plt.subplots()
        ax.scatter(self.x, self.y, c='b')
        plt.tight_layout()
        plt.xlabel('Number of votes')
        plt.ylabel('Average scores')
        plt.title('Game ratings based on Average scores')
        plt.grid(True)
        plt.show()

    def plot_bayesian_ranking(self):
        fig, ax = plt.subplots()
        ax.scatter(self.x, self.z, c='c')
        plt.tight_layout()
        plt.xlabel('Number of votes')
        plt.ylabel('Bayesian average scores')
        plt.title('Game ratings based on Bayesian average scores')
        plt.grid(True)
        plt.show()



