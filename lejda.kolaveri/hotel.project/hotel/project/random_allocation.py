import pandas as pd
import numpy as np
from utils import satisfaction
import openpyxl
guests= pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\guests.xlsx")
hotels = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\hotels.xlsx")
preferences = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\preferences.xlsx")


class HotelAllocation:
    def __init__(self, hotels, guests):
        """Initialize the HotelAllocation.

        Parameters:
        - hotels (pd.DataFrame): DataFrame containing information about hotels.
        - guests (pd.DataFrame): DataFrame containing information about guests.
        """
        #we use copy to avoid modifying the original dataframes
        self.hotels = hotels.copy()
        self.guests = guests.copy()
    
    def accomodate_single_guest():
        pass

    def accomodate_guests(self):
        allocations = []

        for _, guest_row in self.guests.iterrows(): #iterrows returns a series for each row
            allocation_entry = self.accomodate_single_guest(guest_row) #allocate the current guest to a random avaiable hotel
            if allocation_entry is not None:
                allocations.append(allocation_entry)

        allocation_df = pd.DataFrame(allocations, columns=['guest_id', 'hotel_id', 'paid_price'])
        return allocation_df

class RandomHotelAllocation(HotelAllocation):
    """ Allocate a guest to a random available hotel based on availability.

        Parameters:
        - guest_row (pd.Series): A row from the guests DataFrame.

        Returns:
        - dict: Allocation information with keys 'guest_id', 'hotel_id', and 'paid_price'.
    """
    def accomodate_single_guest(self, guest_row):
        available_hotels = self.hotels[self.hotels['rooms'] > 0]
        if available_hotels.empty:
            return None

        random_hotel_id = np.random.choice(available_hotels.index) #we randomly select a hotel with available rooms
        self.hotels.loc[random_hotel_id, 'rooms'] -= 1 #reduce the number of avaiable rooms in that hotel by 1
        
        #we calculate the discounted price that a guest will pay for staying in the randomly allocated hotel,
        #taking into account both the original price of the hotel and the guest's discount.
        price_paid = round(available_hotels.loc[random_hotel_id, 'price'] * (1 - guest_row['discount']), 2)
        satisfaction = calculate_satisfaction_percentage(guest_id, random_available_hotel_id, preferences)

        return {'guest_id': guest_row.name, 'hotel_id': random_hotel_id, 'paid_price': price_paid, 'satisfaction': satisfaction}
