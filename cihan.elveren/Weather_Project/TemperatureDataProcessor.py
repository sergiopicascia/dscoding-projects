
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import functions as fun

class TemperatureDataProcessor:
    def __init__(self):
        # Initializer for the TemperatureDataProcessor class
        pass

    def load_data(self, file_path):
        # Load data from a CSV file
        data = pd.read_csv(file_path)
        return data

    def clean_and_transform_data(self, data):
        # Convert the 'dt' column to datetime format
        data['dt'] = pd.to_datetime(data['dt'])

        # Extract the year from the 'dt' column and create a new 'Year' column
        data['Year'] = data['dt'].dt.year

        # Remove rows with any missing values
        data_cleaned = data.dropna()
        return data_cleaned

    def transform_coordinates(self, data):
        # Convert the 'Latitude' and 'Longitude' columns to numerical values
        data['Latitude'] = data['Latitude'].apply(fun.convert_coordinates)
        data['Longitude'] = data['Longitude'].apply(fun.convert_coordinates)
        return data

    def filter_data_by_year_range(self, data, start_year, end_year):
        # Filter data for the specified year range
        return data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

    def find_top_cities_with_temp_ranges(self, data, n=10):
        # Identify top n cities with the largest temperature ranges
        temp_ranges = data.sort_values('temp_range', ascending=False).groupby('City').first().reset_index()
        return temp_ranges.sort_values('temp_range', ascending=False).head(n)

    def merge_with_geographical_data(self, data, city_data):
        # Merge temperature data with geographical data
        return data.merge(city_data[['City', 'temp_range']], on='City').drop_duplicates(subset=['City'])

    def calculate_city_yearly_temperature_ranges(self, data):
        # Calculate yearly maximum and minimum temperatures for each city
        city_yearly_temps = data.groupby(['City', 'Year'])['AverageTemperature'].agg(['min', 'max'])
        city_yearly_temps['temp_range'] = city_yearly_temps['max'] - city_yearly_temps['min']
        return city_yearly_temps.reset_index()

