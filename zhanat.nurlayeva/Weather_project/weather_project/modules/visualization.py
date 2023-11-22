# visualization.py
import streamlit as st
# visualization.py
import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils import convert_to_decimal

class Visualization:
    def plot_data(self, avg_temperatures):
        """Plot the average temperature data for all cities using geopandas."""
        # Print coordinates causing conversion errors
        avg_temperatures['Longitude'] = avg_temperatures['Longitude'].apply(self.print_problematic_coordinate)
        avg_temperatures['Latitude'] = avg_temperatures['Latitude'].apply(self.print_problematic_coordinate)

        # Ensure 'Latitude' and 'Longitude' columns exist in avg_temperatures
        if 'Latitude' not in avg_temperatures.columns or 'Longitude' not in avg_temperatures.columns:
            st.warning("Latitude or Longitude columns not found in the dataset.")
            return

        merged_data = avg_temperatures[['City', 'Latitude', 'Longitude']].drop_duplicates()

        gdf = gpd.GeoDataFrame(merged_data, geometry=gpd.points_from_xy(merged_data.Longitude, merged_data.Latitude))

        # world = gpd.read_file(gpd.datasets.get_path('ne_110m_admin_0_countries.shp'))
        world = gpd.read_file(
            '/Users/zhanatnurlayeva/Documents/GitHub/dscoding-projects/zhanat.nurlayeva/Weather_project/weather_project/packages/Natural_Earth_quick_start/110m_cultural/ne_110m_admin_0_countries.shp')

        fig, ax = plt.subplots(figsize=(15, 10))
        world.plot(ax=ax, color='lightgrey', edgecolor='black')
        gdf.plot(ax=ax, marker='o', color='red', markersize=50, alpha=0.5)

        st.pyplot(fig)

        #def plot_data(self, avg_temperatures):
        """Plot the average temperature data for all cities using geopandas."""
        #avg_temperatures['Longitude'] = avg_temperatures['Longitude'].apply(self.print_problematic_coordinate)
        #avg_temperatures['Latitude'] = avg_temperatures['Latitude'].apply(self.print_problematic_coordinate)

        #if 'Latitude' not in avg_temperatures.columns or 'Longitude' not in avg_temperatures.columns:
            #st.warning("Latitude or Longitude columns not found in the dataset.")
            #return

        #merged_data = avg_temperatures[['City', 'Latitude', 'Longitude']].drop_duplicates()

        #gdf = gpd.GeoDataFrame(merged_data, geometry=gpd.points_from_xy(merged_data.Longitude, merged_data.Latitude))

        #world = gpd.read_file('/Users/zhanatnurlayeva/Documents/GitHub/dscoding-projects/zhanat.nurlayeva/Weather_project/weather_project/packages/Natural_Earth_quick_start/110m_cultural/ne_110m_admin_0_countries.shp')

        # Convert to a projected CRS before plotting
        #world = world.to_crs("EPSG:3395")

        #ax = world.plot(color='lightgrey', edgecolor='black', figsize=(15, 10))

        #gdf.plot(ax=ax, marker='o', color='red', markersize=50, alpha=0.5)

        #plt.title("Average Temperature for Cities")
        #plt.show()

    def annotate_countries(self, ax, world):
        """Annotate countries on the world map."""
        # Convert to a projected CRS before using centroid
        world = world.to_crs("EPSG:3395")
        for x, y, label in zip(world.geometry.centroid.x, world.geometry.centroid.y, world['ADMIN']):
            ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=8)

    def plot_city_temperature_trend(self, original_data, start_city):
        """Plot the temperature trend for a specific city over time."""
        fig, ax = plt.subplots(figsize=(15, 7))

        city_data = original_data[original_data['City'] == start_city]
        sns.lineplot(x='dt', y='AverageTemperature', data=city_data, ax=ax)
        plt.title(f'Temperature Trend for {start_city}')
        plt.xlabel('Year')
        plt.ylabel('Average Temperature (°C)')

        st.pyplot(fig)

    def plot_temperature_trends(self, filtered_data):
        """Plot temperature ranges for cities during different historical periods."""
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plot temperature ranges for cities during different historical periods
        sns.boxplot(x='dt', y='AverageTemperature', hue='City', data=filtered_data, ax=ax)
        plt.title('Cities with Largest Temperature Ranges')
        plt.xlabel('Year')
        plt.ylabel('Average Temperature (°C)')

        st.pyplot(fig)
        #def plot_temperature_trends(self, df):
        #df_copy = df.copy()
        #df_copy['Latitude'] = df_copy['Latitude'].apply(convert_to_decimal)
        #df_copy['Longitude'] = df_copy['Longitude'].apply(convert_to_decimal)

        #temp_ranges = df_copy.groupby('City').apply(lambda x: x['AverageTemperature'].max() - x['AverageTemperature'].min())
        #df_copy['TempRange'] = df_copy['City'].map(temp_ranges)

        #gdf = gpd.GeoDataFrame(df_copy, geometry=gpd.points_from_xy(df_copy.Longitude, df_copy.Latitude))

        #world = gpd.read_file(gpd.datasets.get_path('ne_110m_admin_0_countries.shp'))
        #world = gpd.read_file('/Users/zhanatnurlayeva/Documents/GitHub/dscoding-projects/zhanat.nurlayeva/Weather_project/weather_project/packages/Natural_Earth_quick_start/110m_cultural/ne_110m_admin_0_countries.shp')

        #ax = world.plot(color='lightgrey', edgecolor='black', figsize=(15, 10))

        #gdf.plot(ax=ax, marker='o', color='red', markersize=df_copy['TempRange'] * 10, alpha=0.5)

        #self.annotate_countries(ax, world)

        #plt.title("Cities with Largest Temperature Ranges")
        #plt.show()

    #def plot_city_temperature_trend(self, data, start_city):
        """Plot temperature trend for the specified starting city over time."""
        #city_data = data[data['City'] == start_city].copy()
        #city_data['dt'] = pd.to_datetime(city_data['dt'])
        #city_data['Latitude'] = city_data['Latitude'].apply(convert_to_decimal)
        #city_data['Longitude'] = city_data['Longitude'].apply(convert_to_decimal)

        #plt.figure(figsize=(15, 7))
        #plt.plot(city_data['dt'], city_data['AverageTemperature'], label=start_city)
        #plt.title(f"Temperature Trend for {start_city}")
        #plt.xlabel("Year")
        #plt.ylabel("Average Temperature")
        #plt.legend()
        #plt.grid(True)
        #plt.show()

    def print_problematic_coordinate(self, coord):
        converted_coord = convert_to_decimal(coord)
        if converted_coord is None:
            st.write(f"Problem converting coordinate: {coord}")
        return converted_coord
    #def print_problematic_coordinate(self, coord):
        #converted_coord = convert_to_decimal(coord)
        #if converted_coord is None:
            #print(f"Problem converting coordinate: {coord}")
        #return converted_coord