import pandas as pd
import numpy as np
import openpyxl
from utils import satisfaction
guests= pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\guests.xlsx")
hotels = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\hotels.xlsx")
preferences = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\preferences.xlsx")

class PriceBasedAllocator:
    def __init__(self, hotels, guests, preferences):
    """Initialize the AvailabilityBasedAllocator.

        Parameters:
        - hotels (pd.DataFrame): DataFrame containing information about hotels.
        - guests (pd.DataFrame): DataFrame containing information about guests.
        - preferences (pd.DataFrame): DataFrame containing guest preferences.
    """
        #we use copies to avoid modifying the original dataframes   
        self.hotels = hotels.copy()
        self.guests = guests.copy()
        self.preferences = preferences.copy()
        
    def can_allocate_to_hotel(self, hotel_row, guest_id):
        """
        Check if a guest can be allocated to a hotel.

        Parameters:
        - hotel_row (pd.Series): Row of the hotel DataFrame.
        - guest_id: ID of the guest.

        Returns:
        - bool: True if allocation is possible, False otherwise.
        """
        #we ensure that there are available rooms in the hotel and we check that the guest has not specified any preferences
        return hotel_row['rooms'] > 0 and guest_id not in self.preferences.index

    def calculate_paid_price(self, row):
        return row['price'] * 1 - row['discount']

    def allocate_and_calculate(self):
        """
        Allocate guests to hotels based on price, calculate satisfaction and paid price.

        Returns:
        - pd.DataFrame: DataFrame containing allocation information.
        """
        allocation_list = []
        #we merge the three dataframes and we sort the values based on price in ascending order
        sorted_hotels = preferences.merge(hotels, on=['hotel']).merge(guests).sort_values(by='price')

        for group_key, group in sorted_hotels.groupby('hotel', sort=False): #we group the rows of sorted_hotels dataframe based on the         hotel column 
            for id, row in group.iterrows():
                if group.iloc[0]['rooms'] == 0: #we check if the number of available rooms in the first row of the current group is                      equal to zero
                    break
                group['rooms'] -= 1 #we decrement the number of rooms for the current hotel group by 1
                paid_price = self.calculate_paid_price(row)
                satisfaction = calculate_satisfaction_percentage(row['guest'], row['hotel'], preferences)
                allocation_entry = [row['guest'], row['hotel'], satisfaction, paid_price]
                allocation_list.append(allocation_entry)
        return pd.DataFrame(allocation_list, columns=['guest_id', 'hotel_id', 'satisfaction', 'paid_price'])
