import pandas as pd

def compute_city_avg_temperature(data):
    return data.groupby('City')['AverageTemperature'].mean().reset_index()

def load_data(file_path):
    return pd.read_csv(file_path)

def clean_data(data):
    data.dropna(subset=['AverageTemperature'], inplace=True)
    clean_data = data.dropna()
    return clean_data

def merge_avg_with_original(avg_temperatures, original_data):
    merged_data = avg_temperatures.merge(original_data[['City', 'Latitude', 'Longitude']], on='City', how='left')
    return merged_data.drop_duplicates(subset='City')

def filter_data_by_period(data, start_date, end_date):

    mask = (data['dt'] >= start_date) & (data['dt'] <= end_date)
    return data[mask]