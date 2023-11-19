import pandas as pd
from scipy.stats import beta

prior_weight = 30.382264442916092
prior_mean = 6.119832661544632


def bayesian_average_funct(row):
    m = row['rating_average']
    n = row['rating_number']
    bayesian_avg = (prior_weight*prior_mean + m*n)/(prior_weight+n)
    return bayesian_avg








