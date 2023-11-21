import pandas as pd
import numpy as np

class HotelPreferenceAllocator:
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

    def allocate_preferred_hotel(self, guest_id, guest_row):
        guest_preferred_hotels = self.preferencesdata[self.preferencesdata['guest'] == guest_id]['hotel']

        for _, preferred_hotel_id in guest_preferred_hotels.items():
            preferred_hotel_row = self.hotelsdata.loc[preferred_hotel_id]

            if preferred_hotel_row['rooms'] > 0:
                preferred_hotel_row['rooms'] -= 1

                paid_price_coefficient = 1 - guest_row['discount']
                paid_price = preferred_hotel_row['price'] * paid_price_coefficient

                satisfaction = self.calculate_satisfaction_percentage(guest_id, preferred_hotel_id)

                return [guest_id, preferred_hotel_id, satisfaction, paid_price]

        return None

    def get_customer_preference_allocation(self):
        self.allocation = pd.DataFrame(columns=['guest_id', 'hotel_id', 'satisfaction_percentage', 'paid_price'])

        for guest_id, guest_row in self.guestdata.iterrows():
            allocation_entry = self.allocate_preferred_hotel(guest_id, guest_row)
            if allocation_entry is not None:
                self.allocation.loc[len(self.allocation)] = allocation_entry

        return self.allocation