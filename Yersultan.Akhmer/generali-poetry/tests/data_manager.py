import pandas as pd

class DataManager:
    def __init__(self, hotels_path, guests_path, preferences_path):
        self.hotels_df = pd.read_excel(hotels_path, index_col=0)
        self.guests_df = pd.read_excel(guests_path, index_col=0)
        self.preferences_df = pd.read_excel(preferences_path, index_col=0)
        self.preferences_df.sort_values(by=['guest', 'priority'], inplace=True)

    def get_hotels(self):
        return self.hotels_df

    def get_guests(self):
        return self.guests_df

    def get_preferences(self):
        return self.preferences_df
