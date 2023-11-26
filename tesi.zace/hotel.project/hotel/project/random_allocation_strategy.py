import pandas as pd
from utils import calc_degree_satisfaction
import random

class RandomAllocator:
    def __init__(self, hotels, guests, preferences):
        self.hotels = hotels
        self.guests = guests
        self.preferences = preferences
        self.allocation = pd.DataFrame(columns=['guest_no', 'hotel_no', 'satisfaction_percentage', 'price_to_pay'])

    def random_hotel(self, guest_no, guest_row):
        # Filters the hotels that have more than 0 remaining available rooms
        remaining_hotels = self.hotels[self.hotels['rooms'] > 0]

        if remaining_hotels.empty:
            return None
        # Choose a random hotel from the remaining hotels group
        random_remaining_hotel_row = remaining_hotels.sample(n=1, random_state=20).iloc[0]
        # Decrease the number of available rooms, calculate price and % of satisfaction
        remaining_hotels.at[random_remaining_hotel_row.name, 'rooms'] -= 1
        price_to_pay = (1 - guest_row['discount']) * random_remaining_hotel_row['price']
        satisfaction = calc_degree_satisfaction(guest_no, random_remaining_hotel_row.name, self.preferences)

        #  Return a dictionary containing information about the allocated room for the guest
        return {
            'guest_no': guest_no,
            'hotel_no': random_remaining_hotel_row.name,
            'satisfaction_percentage': satisfaction,
            'price_to_pay': price_to_pay
        }

    def allocate_randomly(self):
        # Shuffle the guests
        randomized_guests = self.guests.sample(frac=1, random_state=42)
        # A loop that iterates over the randomized guests and randomly allocates a room to the specified guest
        for guest_no, guest_row in randomized_guests.iterrows():
            allocated_in = self.random_hotel(guest_no, guest_row)
            # If the guest has been accommodated the information about the room is appended
            if allocated_in:
                self.allocation.loc[len(self.allocation)] = allocated_in
        return self.allocation


