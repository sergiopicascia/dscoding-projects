import pandas as pd
import numpy as np
import openpyxl
from utils import satisfaction
guests= pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\guests.xlsx")
hotels = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\hotels.xlsx")
preferences = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\preferences.xlsx")

class PreferencesAllocator(HotelAllocation):
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
        


    def allocate_and_calculate(self):
        """Allocate guests to their preferred hotels, calculate paid price and satisfaction.

        Returns:
        - pd.DataFrame: DataFrame containing allocation information for each guest,
          including guest ID, hotel ID, satisfaction, and paid price.
        """
        allocation_list = []

        for guest_id, guest_row in self.guests.iterrows():
            #the code is iterating through the guests in the guests DataFrame and, for each guest,
            #extracting the preferred hotels from the preferences DataFrame based on their ID.
            guest_preferred_hotels = self.preferences[self.preferences['guest'] == f'guest_{guest_id}']['hotel']

            for _, preferred_hotel_id in guest_preferred_hotels.items():
                #we extract a numerical index from hotel_id, removing the prefix "hotel_", subtracting 1 to the remain number
                #and covert it into an integer to get the hotel_id number
                hotel_index = int(preferred_hotel_id.lstrip('hotel_')) - 1
                preferred_hotel_row = self.hotels.loc[hotel_index]

                if preferred_hotel_row['rooms'] > 0:
                    self.hotels.loc[hotel_index, 'rooms'] -= 1

                    paid_price_coefficient = 1 - guest_row['discount']
                    paid_price = preferred_hotel_row['price'] * paid_price_coefficient

                    satisfaction = self.calculate_satisfaction_percentage(f"guest_{guest_id}", preferred_hotel_id)

                    allocation_entry = [f"guest_{guest_id}", preferred_hotel_id, satisfaction, paid_price]
                    allocation_list.append(allocation_entry)

                    break

        return pd.DataFrame(allocation_list, columns=['guest_id', 'hotel_id', 'satisfaction', 'paid_price'])
