import pandas as pd
import numpy as np
from statistics import NormalDist
import matplotlib.pyplot as plt
from pandasgui import show

class rating:
    def __init__(self, path):
        self.bgg = pd.read_csv(path)
        self.bgg = self.bgg.dropna().sort_values(by= ['game']).reset_index(drop = True)
        self.bgg = self.bgg[0:100000]
        self.counting = self.bgg.groupby(['game']).count()
        self.title = self.bgg.groupby('game')['title'].first()

    def compute_avg_rating (self):
        self.avg_rating = self.bgg.groupby(['game']).mean('rating')
        self.avg_rating = self.avg_rating.sort_values(by=['rating'], ascending = False)

    def compute_geek_rating (self):
        self.l= int(self.bgg.size/3)
        c = self.l
        bgg1 = self.bgg
        for i in range (0, self.l):
            if bgg1.game.loc[i] != bgg1.game.loc[i+1]:
                for j in range (0,5):
                    bgg1.loc[c] = [bgg1.game.loc[i],bgg1.title.loc[i], 5.5]
                    c += 1
        self.geek_rating = bgg1.groupby(['game']).mean('rating')
        self.geek_rating = self.geek_rating.sort_values(by = ['rating'], ascending = False)
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
                    counter = 0
                    for j in range (start,x+1):
                        if i == bgg2.rating.loc[j]:
                           counter += 1
                    nk.append(counter)
                N = bgg2.groupby(['game']).count().rating.to_numpy()[0]
                sum = 0
                for i in range (0,K):
                    a = sk[i]*((nk[i]+1)/(N+K))
                    sum += a
                sum1 = 0
                for i in range (0,K):
                    b = (sk[i]**2)*((nk[i]+1)/(N+K))
                    sum1 += b
                S = sum - z * (np.sqrt((sum1-(sum**2))/(N+K+1)))
                self.new_rating.append([self.bgg.game.loc[x],S])
                start = x+1
        self.new_rating = np.array(self.new_rating)
        self.new_rating = pd.DataFrame(self.new_rating)
        self.new_rating[0] = self.new_rating[0].astype(int)
        self.new_rating = self.new_rating.set_index(0)
        self.new_rating.columns = ['New_rating']
        self.new_rating = self.new_rating.sort_values(by = 'New_rating',ascending = False)

    def create_ranking(self, sort_by = 'Average_rating'):
        self.result = pd.concat([self.title, self.avg_rating, self.geek_rating, self.new_rating, self.counting.rating], axis=1)
        self.result.columns = ['Game','Average_rating','Geek_rating', 'New_rating','Number_of_ratings']
        self.result = self.result.sort_values(by=sort_by, ascending=False).reset_index(drop = True)
        self.result.index += 1

    def visualize_ranking(self):
        self.table = show(self.result)

    def get_info(self,identifier,by='index'):
        try:
            if by == 'index':
                row = self.result.loc[identifier]
                return(f"{identifier}° position:\n{row}")
            elif by == 'title':
                row = self.result.loc[self.result.Game == identifier]
                position = row.index[0]
                row = row.iloc[0]
                return(f"{position}° position:\n{row}")
            else:
                return("Error: Invalid value for 'by' parameter. Use 'index' or 'title'.")
        except:
            return(f"Error: {identifier} doesn't exist in DataFrame.")

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

    def create_scatterplot(self, result, plot_avg=True, plot_avg_geek=True, plot_new=True):
        plt.figure(figsize=(8, 6))
        if plot_avg:
            plt.scatter(result.Average_rating, result.Number_of_ratings, s=15, c='blue', alpha=0.5, label='Average Rating')
        if plot_avg_geek:
            plt.scatter(result.Geek_rating, result.Number_of_ratings, s=15, c='red', alpha=0.5, label='Geek Rating')
        if plot_new:
            plt.scatter(result.New_rating, result.Number_of_ratings, s=15, c='green', alpha=0.5, label='New Rating')
        plt.xlabel('Rating')
        plt.ylabel('Number of Ratings')
        plt.title('Rating vs. Number of Ratings')
        plt.grid(True)
        plt.legend()
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
        