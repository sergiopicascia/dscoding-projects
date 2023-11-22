# dataprocessor.py

import pandas as pd

class DataProcessor:
    def __init__(self, file_path):
        self.data = None
        self.load_data(file_path)

    def load_data(self, file_path):
        """Load data from a CSV file."""
        self.data = pd.read_csv(file_path)

    def compute_city_avg_temperature(self):
        """Compute the average temperature for each city."""
        avg_temperatures = self.data.groupby('City')['AverageTemperature'].mean().reset_index()

        # Include 'Latitude' and 'Longitude' in the resulting DataFrame
        avg_temperatures = avg_temperatures.merge(self.data[['City', 'Latitude', 'Longitude']].drop_duplicates(),
                                                  on='City', how='left')

        return avg_temperatures

    #def compute_city_avg_temperature(self):
        #"""Compute the average temperature for each city."""
        #return self.data.groupby('City')['AverageTemperature'].mean().reset_index()

    def clean_data(self):
        """Clean and preprocess data."""
        self.data.dropna(subset=['AverageTemperature'], inplace=True)
        return self.data.dropna()

    def merge_avg_with_original(self, avg_temperatures):
        merged_data = avg_temperatures.merge(self.data[['City', 'Latitude', 'Longitude']], on='City', how='left')
        return merged_data.drop_duplicates(subset='City')

    def filter_data_by_period(self, start_date, end_date):
        mask = (self.data['dt'] >= start_date) & (self.data['dt'] <= end_date)
        return self.data[mask]
