import pandas as pd
import matplotlib.pyplot as plt
import functions as fun

class Processor:
    def __init__(self):
        # Initialize class
        pass
    
    def transform_data(self, data):
        # Convert the 'dt' column to date format
        data['dt'] = pd.to_datetime(data['dt'])

        # Extracting year
        data['Year'] = data['dt'].dt.year
        return data
        
    def change_coord(self, data):
        data['Latitude'] = data['Latitude'].apply(fun.convert_coord)
        data['Longitude'] = data['Longitude'].apply(fun.convert_coord)
        return data
    
    def filter_period(self, data, start_year, end_year):
        return data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]
    
    def find_top_anomaly_cities(self, data, n=5):
        temp_ranges = data.sort_values('temp_range', ascending=False).groupby('City').first().reset_index()
        return temp_ranges.sort_values('temp_range', ascending=False).head(n)
    
    def calculate_city_temp_ranges(self, data):
        # Calculate yearly maximum and minimum temperatures for each city
        city_yearly_temps = data.groupby(['City', 'Year'])['AverageTemperature'].agg(['min', 'max'])
        city_yearly_temps['temp_range'] = city_yearly_temps['max'] - city_yearly_temps['min']
        return city_yearly_temps.reset_index()
        