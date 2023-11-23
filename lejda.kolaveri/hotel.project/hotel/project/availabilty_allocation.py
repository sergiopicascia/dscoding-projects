import pandas as pd
import numpy as np
import openpyxl
from utils import satisfaction
guests= pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\guests.xlsx")
hotels = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\hotels.xlsx")
preferences = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\preferences.xlsx")

class AvailabilityBasedAllocator(HotelAllocation):
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
        
        
    def can_allocate_to_hotel(self, hotel_row, guest_id):
        """
        Check if a guest can be allocated to a hotel.

        Returns:
        - bool: True if allocation is possible, False otherwise.
        """
        #we ensure that there are available rooms in the hotel and if the guest has preferences for that hotel
        return hotel_row['rooms'] > 0 and guest_id in self.preferences['guest'].values
    
        
    def allocate_and_calculate(self):
        """
        Allocate guests to hotels based on available rooms, calculate satisfaction, and paid price.

        Returns:
        - pd.DataFrame: DataFrame containing allocation information.
        """
        allocation_list = []

        sorted_hotels = preferences.merge(hotels, on='hotel').merge(guests, on='guest').sort_values(by=['rooms', 'hotel'], ascending=False)
        allocated_guests = set()
        for _, group in sorted_hotels.groupby('hotel', sort=False):
            for id, hotel_row in group.iterrows():
                if hotel_row['guest'] not in allocated_guests and hotel_row['rooms'] > 0:
                    group['rooms'] -= 1
                    paid_price = hotel_row['price'] * (1 - hotel_row['discount'])
                    satisfaction = self.calculate_satisfaction_percentage(hotel_row['guest'], hotel_row['hotel'])
                    allocation_entry = [hotel_row['guest'], hotel_row['hotel'], satisfaction, paid_price]
                    allocation_list.append(allocation_entry)
                    
                    # Update the set of allocated guests for the current hotel
                    allocated_guests.add(hotel_row['guest'])


        return pd.DataFrame(allocation_list, columns=['guest_id', 'hotel_id', 'satisfaction', 'paid_price'])