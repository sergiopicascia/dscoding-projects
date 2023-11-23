import pandas as pd
from utils import calc_degree_satisfaction

class PreferenceAllocator:
    def __init__(self, hotels, guests, preferences):
        self.hotels = hotels
        self.guests = guests
        self.preferences = preferences
        self.allocation = pd.DataFrame(columns=['guest_no', 'hotel_no', 'satisfaction_percentage', 'price_to_pay'])

    def hotel_preference(self, guest_no, guest_row):
        # Filters the hotels that are prioritized by the guests
        prioritized_hotels = self.preferences[self.preferences['guest'] == guest_no]['hotel']

        # Loop that iterates through the prioritized hotels for specified guest
        for _, prioritized_hotel_id in prioritized_hotels.items():
            prioritized_hotel_row = self.hotels.loc[prioritized_hotel_id]
            # While there are available rooms in prioritized hotel
            # Calculate price and % of satisfaction
            for _ in range(prioritized_hotel_row['rooms']):
                price_to_pay = (1 - guest_row['discount']) * prioritized_hotel_row['price']
                satisfaction = calc_degree_satisfaction(guest_no, prioritized_hotel_id, self.preferences)
                # Result contains information about the allocated room for the current guest
                result = [guest_no, prioritized_hotel_id, satisfaction, price_to_pay]
                return result
        return None

    def allocate_by_priority(self):
        # A loop that iterates over the guests and allocates a room to the specified guest according to preference
        for guest_no, guest_row in self.guests.iterrows():
            allocated_in = self.hotel_preference(guest_no, guest_row)
            # If the guest has been accommodated the information about the room is appended
            if allocated_in:
                self.allocation.loc[len(self.allocation)] = allocated_in
        return self.allocation

