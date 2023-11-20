import os
import pandas as pd

class Hotelsdata:
    """
    This is a data structure consisting in three DataFrames containing data about guests, hotels and guests' preference.
    
    Parameters:
        path (str): A path that points where the datasets are stored.
    """
    def __init__(self, path):
        self.path = os.path.join(path, "")

    def import_data(self, filepath):
        data = pd.read_excel(filepath)
        return data

    @property
    def guests(self):
        """
        This is a DataFrame containing data about the guests.

        A new column is added (guest_num) to facilitate future operations of sorting the list based on guest numbers.

        The first column (Unnamed: 0) is dropped, as it has no further purpose.

        """
        data = self.import_data(self.path + "guests.xlsx")
        data['guest_num'] = data['guest'].str.split('_').str[1].astype(int)
        data.drop(['Unnamed: 0'], axis=1, inplace=True)
        return data
    
    @property
    def hotels(self):
        """
        This is a DataFrame containing data about the hotels.

        A new column is added (hotel_num) to facilitate future operations of sorting the list based on hotel numbers.

        The first column (Unnamed: 0) is dropped, as it has no further purpose.

        """
        data = self.import_data(self.path + "hotels.xlsx")
        data['hotel_num'] = data['hotel'].str.split('_').str[1].astype(int)
        data.drop(['Unnamed: 0'], axis=1, inplace=True)
        return data
    
    @property
    def preference(self):
        """
        This is a DataFrame containing data about the guests' preferences about the available hotels.

        Two new columns are added (guest_num, hotel_num) to facilitate future operations of sorting the list based on guest numbers.
        
        The first column (Unnamed: 0) is dropped, as it has no further utility.

        Some rows are dropped because some guests' preferences are duplicated (same guest and same hotel, more than once).

        """
        data = self.import_data(self.path + "preferences.xlsx")
        data['guest_num'] = data['guest'].str.split('_').str[1].astype(int)
        data['hotel_num'] = data['hotel'].str.split('_').str[1].astype(int)
        data.drop(['Unnamed: 0'], axis=1, inplace=True)
        data['concat'] = data['guest']+data['hotel']
        data.drop_duplicates(subset=['concat'], keep='first', inplace=True)
        data.reset_index(drop=True, inplace=True)
        data.drop(['concat'], axis=1, inplace=True)
        return data