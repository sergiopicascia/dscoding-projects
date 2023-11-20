from map import Map
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math

path = 'venv/data/data_cities.csv'
tem_dataframe = pd.read_csv(path, sep=',')  # import the data
gpd_cities = gpd.GeoDataFrame(
    tem_dataframe, geometry=gpd.points_from_xy(tem_dataframe.Longitude, tem_dataframe.Latitude)
)

gpd_world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
gpd_world = gpd_world[gpd_world.continent != "Antarctica"]  # removing antartica

# let's create the base object
my_map = Map(gpd_cities, gpd_world)

my_map.avg_temperature_graph('Peking', 11)

