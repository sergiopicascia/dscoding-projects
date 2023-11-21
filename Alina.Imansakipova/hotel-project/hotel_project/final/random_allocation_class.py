import pandas as pd
import numpy as np

class RandomHotelAllocator:
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

    def allocate_random_hotel(self, guest_id, guest_row):
        available_hotels = self.hotelsdata[self.hotelsdata['rooms'] > 0]
        if available_hotels.empty:
            return None

        random_available_hotel_id = np.random.choice(available_hotels.index)
        random_available_hotel_row = available_hotels.loc[random_available_hotel_id]
        random_available_hotel_row['rooms'] -= 1

        paid_price_coefficient = 1 - guest_row['discount']
        paid_price = random_available_hotel_row['price'] * paid_price_coefficient

        satisfaction = self.calculate_satisfaction_percentage(guest_id, random_available_hotel_id)

        return [guest_id, random_available_hotel_id, satisfaction, paid_price]

    def get_random_allocation(self):
        shuffled_guests = self.guestdata.sample(frac=1, random_state=42)
        for guest_id, guest_row in shuffled_guests.iterrows():
            allocation_entry = self.allocate_random_hotel(guest_id, guest_row)
            if allocation_entry is not None:
                self.allocation.loc[len(self.allocation)] = allocation_entry

        return self.allocation