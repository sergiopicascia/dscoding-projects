import pandas as pd
import matplotlib.pyplot as plt
import functions as fun

class Processor:
    def __init__(self):
        # Initialize class
        pass
    
    def transform_data(self, df):
        # Convert the 'dt' column to date format
        df['dt'] = pd.to_datetime(df['dt'])

        # Extracting year
        df['Year'] = df['dt'].dt.year
        
    def change_coord(self, df):
        df['Latitude'] = df['Latitude'].apply(fun.convert_coord)
        df['Longitude'] = df['Longitude'].apply(fun.convert_coord)
        return data