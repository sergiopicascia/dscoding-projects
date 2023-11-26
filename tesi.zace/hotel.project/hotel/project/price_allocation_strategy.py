import pandas as pd
from utils import calc_degree_satisfaction

class PriceAllocator:
    def __init__(self, hotels, guests, preferences):
        self.hotels = hotels
        self.guests = guests
        self.preferences = preferences
        self.allocation = pd.DataFrame(columns=['guest_no', 'hotel_no', 'satisfaction_percentage', 'price_to_pay'])

    def available_rooms(self, empty_rooms, hotel_no, hotel_row):
        # Exclude guests who are accommodated
        not_accommodated_guest = self.guests[~self.guests.index.isin(self.allocation['guest_no'])]
        available_guests = not_accommodated_guest.head(empty_rooms)

        # Creates a loop that iterates until all guests are accommodated
        if not available_guests.empty:
            # Calculate price to be paid
            price_to_pay = hotel_row['price'] * (1 - available_guests['discount'])
            # Create row in dataframe with information about available guests and their allocation
            new_rows = pd.DataFrame({
                'guest_no': available_guests.index,
                'hotel_no': hotel_no,
                'satisfaction_percentage': [0] * len(available_guests),
                'paid_price': price_to_pay.tolist()
            })
            # Add rows to the allocation dataframe for each available guest
            for _, row in new_rows.iterrows():
                self.allocation.loc[len(self.allocation)] = row

    def rooms_priority(self, hotel_no, hotel_row):
        # Filters only the guests who have specified a hotel as preference
        prioritized_hotel_guest = self.preferences[self.preferences['hotel'].eq(hotel_no)]['guest']
        # Exclude those who are accommodated
        not_accommodated_guest = prioritized_hotel_guest[~prioritized_hotel_guest.isin(self.allocation['guest_no'])]
        #  Gives the number of empty rooms
        empty_rooms = hotel_row['rooms']

        # Loop that iterates over the guests numbers until there are no more empty rooms
        for guest_no in not_accommodated_guest[:empty_rooms]:
            empty_rooms -= 1

            guest_row = self.guests.loc[guest_no]
            # Calculate price to pay and satisfaction
            price_to_pay = hotel_row['price'] * (1 - guest_row['discount'])
            satisfaction = calc_degree_satisfaction(guest_no, hotel_no, self.preferences)
            # Adds a new row to the dataframe with the information about the allocated room for the guest
            self.allocation.loc[len(self.allocation)] = [guest_no, hotel_no, satisfaction, price_to_pay]

        return empty_rooms

    def allocate_by_price(self):
        # Sort the hotels so that the ones with more available rooms come first
        sorted_hotels = self.hotels.sort_values(by='price')
        # A loop that iterates over the sorted hotels
        # Allocates rooms to guests based on priority for the current hotel
        for hotel_no, hotel_row in sorted_hotels.iterrows():
            hotel_available_rooms = self.rooms_priority(hotel_no, hotel_row)
            # If there are available rooms it passes the information below
            self.available_rooms(hotel_available_rooms, hotel_no, hotel_row) if hotel_available_rooms > 0 else None
        return self.allocation


