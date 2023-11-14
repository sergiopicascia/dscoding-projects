import pandas as pd
from scipy.stats import beta

prior_weight = 30.382264442916092
prior_mean = 6.119832661544632


def bayesian_average_funct(row):
    m = row['rating_average']
    n = row['rating_number']
    bayesian_avg = (prior_weight*prior_mean + m*n)/(prior_weight+n)
    return bayesian_avg



# beta distribution function to calculate bayesian average
def calculate_bayesian_average(rating_sum, rating_number, prior_weight, prior_average):
    alpha = prior_weight + rating_sum
    beta_ = prior_weight + rating_number - rating_sum
    mean = beta.stats(alpha, beta_, moments='m')
    return mean





