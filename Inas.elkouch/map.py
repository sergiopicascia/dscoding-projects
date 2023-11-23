import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from shapely.geometry import Point
import ipywidgets as widgets
from IPython.display import display

"""
-- Documentation --
   This class is used to visualize the temperature changes through a world map
"""


class TemperatureVisualization:
    def __init__(self, data_file):
        """
        Basic setup of the data and cleaning
        :param data_file: dataset to consider
        """
        self.data = pd.read_csv(data_file)
        self.clean_data()

    def clean_data(self):
        """
        Cleaning all the dataset
        :return: data is now cleaned and organised --> ready to be used
        """

        # drops non available data
        self.data.dropna(inplace=True)
        # splitting and reformatting the rest
        self.data[['year', 'month', 'day']] = self.data['dt'].str.split("-", expand=True)
        # erasing duplicates in the subset['City','year']
        self.data = self.data.drop_duplicates(subset=['City', 'year'])
        # converting coordinates and year
        self.data['Latitude'] = self.data['Latitude'].apply(self.convert_to_decimal)
        self.data['Longitude'] = self.data['Longitude'].apply(self.convert_to_decimal)
        self.data['year'] = self.data['year'].astype(int)

    @staticmethod
    def convert_to_decimal(coord):
        """
        Converting coordinates to decimal
        :param coord: coordinates in str type
        :return: value: coordinates in float type
        """
        direction = coord[-1]
        value = float(coord[:-1])
        if direction in ['S', 'W']:
            value = -value
        return value

    def assign_color(self, temp):
        """
        Assigning color depending on the temperature ranges
        :param temp: temperature
        :return: color
        """
        if -40 < temp < -20:
            return 'blue'
        elif -20 < temp < 0:
            return 'green'
        elif 0 < temp < 20:
            return 'yellow'
        else:
            return 'red'

    def plot_cities(self, selected_year):
        """
        Shows the "points" on the map
        :param selected_year: year to display
        :return: no return value --> shows the map
        """

        df_selected = self.data[self.data['year'] == selected_year]
        # applying the color pattern based on AverageTemperature
        df_selected['color'] = df_selected['AverageTemperature'].apply(self.assign_color)

        # locating the point based on Longitude and Latitude
        geometry = [Point(xy) for xy in zip(df_selected['Longitude'], df_selected['Latitude'])]
        # applying it to the map through GeoDataFrame
        gdf = gpd.GeoDataFrame(df_selected, geometry=geometry)

        # creating the map (type: naturalearth_lowres)
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        # creating a figure with subplots and plotting geographical data on it
        # indicates a figure with a width of 15 inches and a height of 10 inches
        fig, ax = plt.subplots(figsize=(15, 10))

        # setting the color of the plot to lightgrey with black edges
        world.plot(ax=ax, color='lightgrey', edgecolor='k')

        # creating the legend with info
        legend_text = {
            'blue': 'Temperature: -40°C to -20°C',
            'green': 'Temperature: -20°C to 0°C',
            'yellow': 'Temperature: 0°C to 20°C',
            'red': 'Temperature: Above 20°C'
        }

        handles = []
        labels = []

        # iterates through the 'color' groups in the GeoDataFrame (gdf),
        # creates legend handles and labels for each color, and plots the corresponding
        # data points with markers differentiated by color on the specified axes (ax)
        for color, subset in gdf.groupby('color'):
            handles.append(plt.Line2D([0], [0], marker='o', color='w', markersize=10, markerfacecolor=color))
            labels.append(legend_text[color])
            subset.plot(ax=ax, color=color, markersize=20, marker='o', label=color)

        # final details by labelling each part
        plt.title(f"City Locations by Temperature Ranges: {selected_year}")
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.legend(handles, labels, title='Temperature Ranges')
        # showing the map
        plt.show()

    def update_map(self, year):
        """
        Updates the map based on the year
        :param year: selected year
        :return: no return value --> shows the updated map with the selected year
        """
        self.plot_cities(year)
