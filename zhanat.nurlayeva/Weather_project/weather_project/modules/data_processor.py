# DataProcessor Class
# Load and clean data.
# Compute average temperatures.
# Merge dataframes.

import pandas as pd
from modules.utils import convert_to_decimal

def load_data(file_path):
    # Your implementation here
    return pd.read_csv(file_path)

class DataProcessor:
# Initialize the DataProcessor class with the path to the CSV file.
# Parameters: - file_path (str): Path to the CSV file containing temperature data.
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def clean_data(self):
        # Clean the loaded data:
        # Remove rows with missing values in the 'AverageTemperature' column.
        # Remove duplicate rows based on the 'City' column.
        # Convert 'Latitude' and 'Longitude' columns to decimal format.
        # Handling missing values
        self.data.dropna(subset=['AverageTemperature'], inplace=True)
        self.data.drop_duplicates(subset='City', inplace=True)

        # Convert Latitude and Longitude to decimal format
        self.data['Latitude'] = self.data['Latitude'].apply(convert_to_decimal)
        self.data['Longitude'] = self.data['Longitude'].apply(convert_to_decimal)

    def compute_avg_temperature(self):
        # Compute the average temperature for each city.
        # Returns: - pd.DataFrame: DataFrame with 'City' and corresponding average temperatures.
        return self.data.groupby('City')['AverageTemperature'].mean().reset_index()

    def merge_avg_with_original(self, avg_temperatures):
        # Merge the computed average temperatures with the original data based on 'City'.
        # Parameters: - avg_temperatures (pd.DataFrame): DataFrame with 'City' and corresponding average temperatures.
        # Returns: - pd.DataFrame: Merged DataFrame with original data and average temperatures.
        return avg_temperatures.merge(self.data[['City', 'Latitude', 'Longitude']], on='City', how='left')

    def filter_data_by_period(self, start_date, end_date):
        # Filter the data based on a specified date range.
        # Parameters:- start_date (str): Start date in the format 'YYYY-MM-DD'.
        #             - end_date (str): End date in the format 'YYYY-MM-DD'.
        # Returns: - pd.DataFrame: Filtered DataFrame containing data within the specified date range.
        mask = (self.data['dt'] >= start_date) & (self.data['dt'] <= end_date)
        return self.data[mask]


''''# DataProcessor Class
# Load and clean data.
# Compute average temperatures.
# Merge dataframes.
# modules/data_processor.py

# modules/data_processor.py

import streamlit as st
import pandas as pd


def convert_to_decimal(coord):
    """Convert a coordinate from string format to decimal format."""
    if isinstance(coord, (float, int)):
        return coord
    elif isinstance(coord, str):
        if 'W' in coord:
            return -float(coord.replace('W', ''))
        elif 'E' in coord:
            return float(coord.replace('E', ''))
        elif 'S' in coord:
            return -float(coord.replace('S', ''))
        elif 'N' in coord:
            return float(coord.replace('N', ''))
        else:
            return float(coord)

class DataProcessor:
    # ... (previous code)

    def clean_data(self):
        # ... (previous code)
        # Convert Latitude and Longitude to decimal format
        self.data['Latitude'] = self.data['Latitude'].apply(convert_to_decimal)
        self.data['Longitude'] = self.data['Longitude'].apply(convert_to_decimal)

    # ... (remaining code)



def load_data(file_path):
    # Your implementation here
    return pd.read_csv(file_path)

class DataProcessor:
# Initialize the DataProcessor class with the path to the CSV file.
# Parameters: - file_path (str): Path to the CSV file containing temperature data.
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def clean_data(self):
        # Clean the loaded data:
        # Remove rows with missing values in the 'AverageTemperature' column.
        # Remove duplicate rows based on the 'City' column.
        # Convert 'Latitude' and 'Longitude' columns to decimal format.
        # Handling missing values
        self.data.dropna(subset=['AverageTemperature'], inplace=True)
        self.data.drop_duplicates(subset='City', inplace=True)

        # Convert Latitude and Longitude to decimal format
        self.data['Latitude'] = self.data['Latitude'].apply(convert_to_decimal)
        self.data['Longitude'] = self.data['Longitude'].apply(convert_to_decimal)

    def compute_avg_temperature(self):
        # Compute the average temperature for each city.
        # Returns: - pd.DataFrame: DataFrame with 'City' and corresponding average temperatures.
        return self.data.groupby('City')['AverageTemperature'].mean().reset_index()

    def merge_avg_with_original(self, avg_temperatures):
        # Merge the computed average temperatures with the original data based on 'City'.
        # Parameters: - avg_temperatures (pd.DataFrame): DataFrame with 'City' and corresponding average temperatures.
        # Returns: - pd.DataFrame: Merged DataFrame with original data and average temperatures.
        return avg_temperatures.merge(self.data[['City', 'Latitude', 'Longitude']], on='City', how='left')

    def filter_data_by_period(self, start_date, end_date):
        # Filter the data based on a specified date range.
        # Parameters:- start_date (str): Start date in the format 'YYYY-MM-DD'.
        #             - end_date (str): End date in the format 'YYYY-MM-DD'.
        # Returns: - pd.DataFrame: Filtered DataFrame containing data within the specified date range.
        mask = (self.data['dt'] >= start_date) & (self.data['dt'] <= end_date)
        return self.data[mask] '''''