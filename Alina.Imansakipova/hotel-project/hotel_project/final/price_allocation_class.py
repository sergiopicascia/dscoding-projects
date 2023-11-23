import pandas as pd
import numpy as np

class HotelPriceAllocator:
    def __init__(self, hotelsdata, guestdata, preferencesdata):
        self.hotelsdata = hotelsdata
        self.guestdata = guestdata
        self.preferencesdata = preferencesdata
        self.allocation = pd.DataFrame(columns=['guest_id', 'hotel_id', 'satisfaction_percentage', 'paid_price'])

    def calculate_satisfaction_percentage(self, guest_id, hotel_id):
        guest_preferences = self.preferencesdata[self.preferencesdata['guest'] == guest_id].reset_index()

        if guest_preferences.empty:
            return 100

        is_hotel_one_of_preferred = np.isin(hotel_id, guest_preferences['hotel'].values)

        if is_hotel_one_of_preferred.any():
            index_of_preference = np.argmax(guest_preferences['hotel'].values == hotel_id)
            guest_preferences_count = len(guest_preferences)
            return round(((guest_preferences_count - index_of_preference) / guest_preferences_count) * 100)
        else:
            return 0

    def allocate_preferred_rooms(self, hotel_id, hotel_row):
        guests_who_preferred_hotel = self.preferencesdata[self.preferencesdata['hotel'] == hotel_id]['guest']
        guests_to_allocate = guests_who_preferred_hotel[~guests_who_preferred_hotel.isin(self.allocation['guest_id'])]
        hotel_available_rooms = hotel_row['rooms']

        for _, guest_id in guests_to_allocate.items():
            if hotel_available_rooms == 0:
                break

            hotel_available_rooms -= 1
            guest_row = self.guestdata.loc[guest_id]

            paid_price_coefficient = 1 - guest_row['discount']
            paid_price = hotel_row['price'] * paid_price_coefficient

            satisfaction = self.calculate_satisfaction_percentage(guest_id, hotel_id)
            self.allocation.loc[len(self.allocation)] = [guest_id, hotel_id, satisfaction, paid_price]

        return hotel_available_rooms, self.allocation

    def allocate_remaining_rooms(self, hotel_available_rooms, hotel_id, hotel_row):
        guests_to_allocate = self.guestdata[~self.guestdata.index.isin(self.allocation['guest_id'])]
        for guest_id, guest_row in guests_to_allocate.iterrows():
            if hotel_available_rooms == 0:
                break

            hotel_available_rooms -= 1
            paid_price_coefficient = 1 - guest_row['discount']
            paid_price = hotel_row['price'] * paid_price_coefficient
            self.allocation.loc[len(self.allocation)] = [guest_id, hotel_id, 0, paid_price]

        return self.allocation

    def get_price_allocation(self):
        allocation = pd.DataFrame(columns=['guest_id', 'hotel_id', 'satisfaction_percentage', 'paid_price'])
        sorted_hotels = self.hotelsdata.sort_values(by='price')

        for hotel_id, hotel_row in sorted_hotels.iterrows():
            hotel_remaining_rooms_count, allocation = self.allocate_preferred_rooms(hotel_id, hotel_row)
            if hotel_remaining_rooms_count > 0:
                allocation = self.allocate_remaining_rooms(hotel_remaining_rooms_count,  hotel_id, hotel_row)

        return allocation
