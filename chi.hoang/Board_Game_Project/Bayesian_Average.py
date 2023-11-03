import numpy as np
import pandas as pd
data=pd.read_csv('Out_68.csv')

prior_mean = 6.42
prior_weight = 10


def Bayesian_average_funct(row):
    n = row['rating_number']
    m = row['rating_average']
    bayesian_avg = (prior_weight * prior_mean + n * m) / (prior_weight + n)
    return bayesian_avg


data['bayesian_average'] = data.apply(Bayesian_average_funct, axis=1)


print(data)























