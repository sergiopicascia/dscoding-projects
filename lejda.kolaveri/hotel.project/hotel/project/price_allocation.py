import pandas as pd
import numpy as np
from utils import satisfaction


class PriceBasedAllocator:
    def __init__(self, hotels, guests, preferences):
        self.hotels = hotels
        self.guests = guests
        self.preferences = preferences

    def allocate_and_calculate(self):
        """
        Allocate guests to hotels based on price, calculate satisfaction and paid price.

        Returns:
        - pd.DataFrame: DataFrame containing allocation information.
        """
        allocation_list = []

        sorted_hotels = preferences.merge(hotels, on=['hotel']).merge(guests).sort_values(by='price')

        for group_key, group in sorted_hotels.groupby('hotel', sort=False):
            for id, row in group.iterrows():
                if group.iloc[0]['rooms'] == 0:
                    break
                group['rooms'] -= 1
                paid_price = self.calculate_paid_price(row)
                satisfaction = calculate_satisfaction_percentage(row['guest'], row['hotel'], preferences)
                allocation_entry = [row['guest'], row['hotel'], satisfaction, paid_price]
                allocation_list.append(allocation_entry)
        return pd.DataFrame(allocation_list, columns=['guest_id', 'hotel_id', 'satisfaction', 'paid_price'])
    def can_allocate_to_hotel(self, hotel_row, guest_id):
        """
        Check if a guest can be allocated to a hotel.

        Parameters:
        - hotel_row (pd.Series): Row of the hotel DataFrame.
        - guest_id: ID of the guest.

        Returns:
        - bool: True if allocation is possible, False otherwise.
        """
        return hotel_row['rooms'] > 0 and guest_id not in self.preferences.index

    def calculate_paid_price(self, row):
        return row['price'] * 1 - row['discount']