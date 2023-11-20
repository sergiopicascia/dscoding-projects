# Visualization Class
# Plot temperature trends.
# Plot city temperature trends.
# modules/visualization.py

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from modules.utils import convert_to_decimal

class Visualization:
    def plot_data(self, avg_temperatures):
        """
        Plot the average temperature data for all cities using geopandas.

        Parameters:
        - avg_temperatures (pd.DataFrame): DataFrame with city temperature data, including 'City', 'Latitude', 'Longitude', and 'AverageTemperature'.
        """
        # Merge avg_temperatures with original_data to get Latitude and Longitude
        merged_data = avg_temperatures.merge(avg_temperatures[['City', 'Latitude', 'Longitude']], on='City', how='left')

        # Drop duplicates to ensure each city appears only once
        merged_data.drop_duplicates(subset='City', inplace=True)

        # Convert the Latitude and Longitude columns to decimal format
        merged_data['Latitude'] = merged_data['Latitude'].apply(convert_to_decimal)
        merged_data['Longitude'] = merged_data['Longitude'].apply(convert_to_decimal)

        # Convert the DataFrame to a GeoDataFrame
        gdf = gpd.GeoDataFrame(merged_data, geometry=gpd.points_from_xy(merged_data.Longitude, merged_data.Latitude))

        # Plot the world map
        world = gpd.read_file(gpd.datasets.get_path('ne_110m_admin_0_countries.shp'))
        ax = world.plot(color='lightgrey', edgecolor='black', figsize=(15, 10))

        # Plot the cities on top of the world map
        gdf.plot(ax=ax, marker='o', color='red', markersize=50, alpha=0.5)

        plt.title("Average Temperature for Cities")
        plt.show()

    def annotate_countries(self, ax, world):
        """
        Annotate countries on the world map.

        Parameters:
        - ax: Matplotlib axis object.
        - world (GeoDataFrame): GeoDataFrame with world map data.
        """
        for x, y, label in zip(world.geometry.centroid.x, world.geometry.centroid.y, world['ADMIN']):
            ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=8)

    def plot_temperature_trends(self, df):
        """
        Plot temperature trends for cities with different marker sizes representing temperature ranges.

        Parameters:
        - df (pd.DataFrame): DataFrame with city temperature data, including 'City', 'Latitude', 'Longitude', 'AverageTemperature'.
        """
        # Convert the Latitude and Longitude columns to decimal format
        df_copy = df.copy()
        df_copy['Latitude'] = df_copy['Latitude'].apply(convert_to_decimal)
        df_copy['Longitude'] = df_copy['Longitude'].apply(convert_to_decimal)

        # Calculate temperature range for each city
        temp_ranges = df_copy.groupby('City').apply(lambda x: x['AverageTemperature'].max() - x['AverageTemperature'].min())
        df_copy['TempRange'] = df_copy['City'].map(temp_ranges)

        # Convert the DataFrame to a GeoDataFrame
        gdf = gpd.GeoDataFrame(df_copy, geometry=gpd.points_from_xy(df_copy.Longitude, df_copy.Latitude))

        # Plot the world map
        world = gpd.read_file('ne_110m_admin_0_countries\\ne_110m_admin_0_countries.shp')
        ax = world.plot(color='lightgrey', edgecolor='black', figsize=(15, 10))

        # Plot the cities on top of the world map with different marker sizes
        gdf.plot(ax=ax, marker='o', color='red', markersize=df_copy['TempRange'] * 10, alpha=0.5)

        # Annotate country names
        self.annotate_countries(ax, world)

        plt.title("Cities with Largest Temperature Ranges")
        plt.show()

    def plot_city_temperature_trend(self, data, city):
        """
        Plot temperature trend for a given city over time.

        Parameters:
        - data (pd.DataFrame): DataFrame with city temperature data, including 'dt', 'AverageTemperature', 'Latitude', 'Longitude', and 'City'.
        - city (str): Name of the city for which to plot the temperature trend.
        """
        city_data = data[data['City'] == city].copy()

        # Convert 'dt' column to datetime format
        city_data['dt'] = pd.to_datetime(city_data['dt'])

        # Convert Latitude and Longitude to decimal format
        city_data['Latitude'] = city_data['Latitude'].apply(convert_to_decimal)
        city_data['Longitude'] = city_data['Longitude'].apply(convert_to_decimal)

        # Plot temperature trend for the specified city
        plt.figure(figsize=(15, 7))
        plt.plot(city_data['dt'], city_data['AverageTemperature'], label=city)
        plt.title(f"Temperature Trend for {city}")
        plt.xlabel("Year")
        plt.ylabel("Average Temperature")
        plt.legend()
        plt.grid(True)
        plt.show()
