import pandas as pd
import numpy as np
from statistics import NormalDist
import matplotlib as plt

class rating:
    def __init__(self, path):
        self.bgg = pd.read_csv(path)
        self.bgg = self.bgg.dropna().sort_values(by= ['game']).reset_index(drop = True)
        self.bgg = self.bgg[0:100000]

    def compute_avg_rating (self):
        self.avg = self.bgg.groupby(['game']).mean('rating')
        self.avg_rating = self.avg.sort_values(by=['rating'])

    def compute_geek_rating (self):
        count = self.bgg.groupby(['game']).count()
        len = int(self.bgg.size/3)
        c = len
        bgg1 = self.bgg
        for i in range (0, len):
            if bgg1.game.loc[i] != bgg1.game.loc[i+1]:
                for j in range (0,5):
                    bgg1.loc[c] = [bgg1.game.loc[i],bgg1.title.loc[i], 5.5]
                    c = c+1
        avg_geek = bgg1.groupby(['game']).mean('rating')
        self.geek_rating = avg_geek.sort_values(by = ['rating'])

    def compute_new_rating(self):
        K = 20
        len = int(self.bgg.size / 3)
        sk = np.arange(start = 0.5, stop = 10.5, step = 0.5)
        alfa = 0.1
        z = NormalDist().inv_cdf(1-alfa/2)
        start = 0
        self.bgg.loc[len] = [0,0,0]
        self.new_rating = []
        for x in range(0,len):
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
                self.new_rating.append(S)
                start = x+1
        self.new_rating = np.array(self.new_rating)

