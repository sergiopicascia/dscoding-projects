import pandas as pd
import numpy as np
from statistics import NormalDist
import matplotlib.pyplot as plt

class rating:
    def __init__(self, path):
        self.bgg = pd.read_csv(path)
        self.bgg = self.bgg.dropna().sort_values(by= ['game']).reset_index(drop = True)
        self.bgg = self.bgg[0:100000]
        self.counting = self.bgg.groupby(['game']).count()

    def compute_avg_rating (self):
        self.avg = self.bgg.groupby(['game']).mean('rating')
        self.avg_rating = self.avg.sort_values(by=['rating'])

    def compute_geek_rating (self):
        self.l= int(self.bgg.size/3)
        c = self.l
        bgg1 = self.bgg
        for i in range (0, self.l):
            if bgg1.game.loc[i] != bgg1.game.loc[i+1]:
                for j in range (0,5):
                    bgg1.loc[c] = [bgg1.game.loc[i],bgg1.title.loc[i], 5.5]
                    c = c+1
        avg_geek = bgg1.groupby(['game']).mean('rating')
        self.geek_rating = avg_geek.sort_values(by = ['rating'])
        self.bgg = self.bgg[0:self.l]

    def compute_new_rating(self):
        K = 20
        sk = np.arange(start = 0.5, stop = 10.5, step = 0.5)
        alfa = 0.1
        z = NormalDist().inv_cdf(1-alfa/2)
        start = 0
        self.bgg.loc[self.l] = [0,0,0]
        self.new_rating = []
        for x in range (0,self.l):
            if self.bgg.game.loc[x] == self.bgg.game.loc[x+1]:
                continue
            else:
                bgg2 = self.bgg[start:x+1]
                nk = []
                for i in sk:
                    c = 0
                    for j in range (start,x+1):
                        if i == bgg2.rating.loc[j]:
                           c = c +1
                    nk.append(c)
                N = bgg2.groupby(['game']).count().rating.to_numpy()[0]
                sum = 0
                for i in range (0,K):
                    a = sk[i]*((nk[i]+1)/(N+K))
                    sum = sum + a
                sum1 = 0
                for i in range (0,K):
                    a = (sk[i]**2)*((nk[i]+1)/(N+K))
                    sum1 = sum1 + a
                b = np.sqrt((sum1-(sum**2))/(N+K+1))
                S = sum - z*b
                self.new_rating.append([self.bgg.game.loc[x],S])
                start = x+1
        self.new_rating = np.array(self.new_rating)

    def create_ranking(self):
        df = pd.DataFrame(self.new_rating)
        df[0] = df[0].astype(int)
        df = df.set_index(0)
        self.result = pd.concat([self.avg_rating, self.geek_rating, df, self.counting.rating], axis=1)
        self.result.columns = ['Average_rating', 'Geek_rating', 'New_rating','Number_of_ratings']

class graphs:
    def __init__(self):
        pass

    def compare_methods (self,result):
        lenght = int(result.size / 4)
        x_values = np.arange(start=1, stop=lenght+1, step=1)
        y1_values = result.Average_rating.to_numpy()
        y2_values = result.Geek_rating.to_numpy()
        y3_values = result.New_rating.to_numpy()
        plt.figure(figsize=(15, 10))
        plt.plot(x_values, y1_values, label='Average rating')
        plt.plot(x_values, y2_values, label='Geek rating')
        plt.plot(x_values, y3_values, label='New rating')
        plt.xlabel('Position')
        plt.ylabel('Rating')
        plt.title('Rating methods comparison')
        plt.legend()
        plt.grid(True)
        plt.show()

    def create_scatterplot(self,result):
        avg = result.Average_rating.to_numpy()
        avg_geek = result.Geek_rating.to_numpy()
        new = result.New_rating.to_numpy()
        conta = result.Number_of_ratings.to_numpy()
        plt.figure(figsize=(8, 6))
        plt.scatter(avg, conta, s=10, c='blue', alpha=0.5)
        plt.scatter(avg_geek, conta, s=10, c='red', alpha=0.5)
        plt.scatter(new, conta, s=10, c='green', alpha=0.5)
        plt.xlabel('Rating')
        plt.ylabel('Number of Ratings')
        plt.title('Rating vs. Number of Ratings')
        plt.grid(True)
        plt.show()

    def create_pie_chart(self,result,selected):
        avg = result[selected].to_numpy()
        num_ranges = 10
        range_width = 1.0
        rating_ranges = [(i * range_width, (i + 1) * range_width) for i in range(num_ranges)]
        categories = [0] * len(rating_ranges)
        for rating in avg:
            for i, (start, end) in enumerate(rating_ranges):
                if start <= rating < end:
                    categories[i] += 1
                    break
        total_games = len(avg)
        percentages = []
        for category in categories:
            percentages.append(category / total_games * 100)
        labels = [f"{start}-{end}" for start, end in rating_ranges]
        colors = ['red', 'lightgreen', 'yellow', 'blue', 'purple', 'orange', 'lightblue', 'pink', 'silver', 'green']
        plt.pie(percentages, labels=None, colors=colors, autopct='', startangle=140)
        plt.axis('equal')
        plt.title('Distribution of Games by Rating Range')
        legend_labels = [f"{label} - {percent:.1f}%" for label, percent in zip(labels, percentages)]
        plt.legend(legend_labels, loc='best', bbox_to_anchor=(1, 1))
        plt.show()
        