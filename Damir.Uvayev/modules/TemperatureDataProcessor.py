import pandas as pd


class TemperatureDataProcessor:
    def __init__(self, file_path):
        self.data = self.load_data(file_path)

    @staticmethod
    def load_data(file_path):
        return pd.read_csv(file_path)

    @staticmethod
    def compute_city_avg_temperature(data):
        return data.groupby('City')['AverageTemperature'].mean().reset_index()

    def filter_data_by_period(self, start_date, end_date):
        mask = (self.data['dt'] >= start_date) & (self.data['dt'] <= end_date)
        return self.data[mask]

    def merge_avg_with_original(self, avg_temperatures):
        merged_data = avg_temperatures.merge(self.data[['City', 'Latitude', 'Longitude']], on='City', how='left')
        return merged_data.drop_duplicates(subset='City')
