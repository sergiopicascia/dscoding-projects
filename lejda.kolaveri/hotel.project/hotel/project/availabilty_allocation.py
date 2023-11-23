import pandas as pd
import numpy as np
import openpyxl
from utils import satisfaction
guests= pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\guests.xlsx")
hotels = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\hotels.xlsx")
preferences = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\preferences.xlsx")

class AvailabilityBasedAllocator:
    def __init__(self, hotels, guests, preferences):
        """
        Initialize the AvailabilityBasedAllocator.

        Parameters:
        - hotels (pd.DataFrame): DataFrame containing information about hotels.
        - guests (pd.DataFrame): DataFrame containing information about guests.
        - preferences (pd.DataFrame): DataFrame containing guest preferences.
        """
        # Use copies to avoid modifying the original DataFrames
        self.hotels = hotels.copy()
        self.guests = guests.copy()
        self.preferences = preferences.copy()
        
    def calculate_satisfaction_percentage(self, guest_id, hotel_id):
        guest_preferences = self.preferences[self.preferences['guest'] == guest_id].reset_index() #filter preferences for the given guest
        if guest_preferences.empty:
            return 100  # No preferences, 100% satisfaction

        index_of_preference = (guest_preferences['hotel'] == hotel_id).idxmax() # Find the index of the allocated hotel in the guest's         preferences
        satisfaction = round(((len(guest_preferences) - index_of_preference) / len(guest_preferences)) * 100)
        return satisfaction if satisfaction >= 0 else 0

    def allocate_and_calculate(self):
        """
        Allocate guests to hotels based on available rooms, calculate satisfaction, and paid price.

        Returns:
        - pd.DataFrame: DataFrame containing allocation information.
        """
        allocation_list = []

        # Sort hotels based on available rooms (desc order)
        sorted_hotels = self.hotels.sort_values(by='rooms', ascending=False)

        for _,hotel_row in sorted_hotels.iterrows():
            allocated_guests = set()  #iniziales an empty set and track guests already allocated to the current hotel
            for guest_row in self.guests.iterrows():
                guest_id = guest_row['guest_id']

                # Check if the guest can be allocated to the current hotel
                if can_allocate_to_hotel(hotel_row, guest_id, self.preferences) and guest_id not in allocated_guests:
                    paid_price = hotel_row['price'] * (1 - guest_row['discount'])
                    satisfaction = self.calculate_satisfaction_percentage(guest_id, hotel_row.name, self.preferences)
                    allocation_entry = [guest_id, hotel_row.name, satisfaction, paid_price]
                    allocation_list.append(allocation_entry)

                    # Update the set of allocated guests for the current hotel
                    allocated_guests.add(guest_id)

        return pd.DataFrame(allocation_list, columns=['guest_id', 'hotel_id', 'satisfaction', 'paid_price'])