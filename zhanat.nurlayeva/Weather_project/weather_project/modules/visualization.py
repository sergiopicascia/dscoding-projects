import streamlit as st
#from streamlit import cache_data
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import convert_to_decimal

class Visualization:
    @staticmethod
    @st.cache_data
    def plot_data(avg_temperatures):
        """Plot the average temperature data for all cities using geopandas."""
        # Print coordinates causing conversion errors
        avg_temperatures['Longitude'] = avg_temperatures['Longitude'].apply(Visualization.print_problematic_coordinate)
        avg_temperatures['Latitude'] = avg_temperatures['Latitude'].apply(Visualization.print_problematic_coordinate)

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

        # Annotate countries
        Visualization().annotate_countries(ax, world)  # Note the instantiation of Visualization

        st.pyplot(fig)

    @staticmethod
    def plot_city_temperature_trend(original_data, start_city):
        """Plot the temperature trend for a specific city over time."""
        fig, ax = plt.subplots(figsize=(15, 7))

        city_data = original_data[original_data['City'] == start_city]
        sns.lineplot(x='dt', y='AverageTemperature', data=city_data, ax=ax)
        plt.title(f'Temperature Trend for {start_city}')
        plt.xlabel('Year')
        plt.ylabel('Average Temperature (°C)')

        st.pyplot(fig)

    @staticmethod
    def plot_temperature_trends(filtered_data):
        """Plot temperature ranges for cities during different historical periods."""
        fig, ax = plt.subplots(figsize=(15, 10))

        # Plot temperature ranges for cities during different historical periods
        sns.boxplot(x='dt', y='AverageTemperature', hue='City', data=filtered_data, ax=ax)
        plt.title('Cities with Largest Temperature Ranges')
        plt.xlabel('Year')
        plt.ylabel('Average Temperature (°C)')

        # Get unique labels for legend
        unique_labels = filtered_data['City'].unique()

        # Set legend
        ax.legend(labels=unique_labels, title='City')

        st.pyplot(fig)

    #@staticmethod
    #def plot_temperature_trends(filtered_data):
        #"""Plot temperature ranges for cities during different historical periods."""
        #fig, ax = plt.subplots(figsize=(15, 10))

        # Plot temperature ranges for cities during different historical periods
        #sns.boxplot(x='dt', y='AverageTemperature', hue='City', data=filtered_data, ax=ax)
        #plt.title('Cities with Largest Temperature Ranges')
        #plt.xlabel('Year')
        #plt.ylabel('Average Temperature (°C)')

        #st.pyplot(fig)

    def annotate_countries(self, ax, world):
        """Annotate countries on the world map."""
        # Convert to a projected CRS before using centroid
        world = world.to_crs("EPSG:3395")
        for x, y, label in zip(world.geometry.centroid.x, world.geometry.centroid.y, world['ADMIN']):
            ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=8)

    @staticmethod
    @st.cache_data
    def print_problematic_coordinate(coord):
        converted_coord = convert_to_decimal(coord)
        if converted_coord is None:
            st.write(f"Problem converting coordinate: {coord}")
        return converted_coord

