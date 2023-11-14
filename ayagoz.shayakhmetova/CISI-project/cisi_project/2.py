import pandas as pd
import random
import numpy as np

data_movie = pd.read_csv("/Users/apple/Documents/GitHub/dscoding-projects/ayagoz.shayakhmetova/CISI-project/cisi_project/tmdb_5000_movies.csv")
data_credits = pd.read_csv("/Users/apple/Documents/GitHub/dscoding-projects/ayagoz.shayakhmetova/CISI-project/cisi_project/tmdb_5000_credits.csv")

out = np.random.sample()
print("Output random value : ", out)