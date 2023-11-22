import pandas as pd
import numpy as np
from utils import satisfaction

class PreferencesAllocator:
    def __init__(self, hotels, guests, preferences):
         """Initialize the AvailabilityBasedAllocator.

        Parameters:
        - hotels (pd.DataFrame): DataFrame containing information about hotels.
        - guests (pd.DataFrame): DataFrame containing information about guests.
        - preferences (pd.DataFrame): DataFrame containing guest preferences.
     """
        self.hotels = hotels
        self.guests = guests
        self.preferences = preferences
        
    def allocate_and_calculate(hotels, guests, preferences):
    """
    Allocate guests to their preferred hotels, calculate paid price and satisfaction.

    Parameters:
    - hotels (pd.DataFrame): DataFrame containing information about hotels.
    - guests (pd.DataFrame): DataFrame containing information about guests.
    - preferences (pd.DataFrame): DataFrame containing guest preferences.

    Returns:
    - list: List of allocation information for each guest, including guest ID, hotel ID,
            satisfaction, and paid price.
    """
    allocation_list = []

    for guest_id, guest_row in guests.iterrows():
        #the code is iterating through the guests in the guests DataFrame and, for each guest,
        #extracting the preferred hotels from the preferences DataFrame based on their ID.
        guest_preferred_hotels = preferences[preferences['guest'] == f'guest_{guest_id}']['hotel']

        for _, preferred_hotel_id in guest_preferred_hotels.items():
            hotel_index = int(preferred_hotel_id.lstrip('hotel_')) - 1
            preferred_hotel_row = hotels.loc[hotel_index]

            if preferred_hotel_row['rooms'] > 0:
                hotels.loc[hotel_index, 'rooms'] -= 1

                paid_price_coefficient = 1 - guest_row['discount']
                paid_price = preferred_hotel_row['price'] * paid_price_coefficient

                satisfaction = calculate_satisfaction_percentage(guest_id, preferred_hotel_id, preferences)

                allocation_entry = [guest_id, preferred_hotel_id, satisfaction, paid_price]
                allocation_list.append(allocation_entry)

                break

    return allocation_list
