import pandas as pd
import numpy as np

class Strategy:
    """
    This class represents different strategies for allocating guests to hotels.

    Parameters:
        guests: DataFrame
            DataFrame containing guests' information.
        hotels: DataFrame
            DataFrame containing hotels' information.
        pref: DataFrame
            DataFrame containing preferences' information.
    """

    def __init__(self, guests, hotels, pref):
        self.guests = guests
        self.hotels = hotels
        self.pref = pref
    
    @staticmethod
    def satisfaction(priority_hotels, hotel_index):
        """
        Calculate guest satisfaction based on the selected hotel's position in the preference list.

        Parameters:
            priority_hotels (list): List of hotels in the guest's preference order.
            hotel_index (int): Index of the selected hotel in the priority list.

        Returns:
            int: Guest satisfaction level (1 to 5).
                1 = completely satisfied.
                2 = satisfied.
                3 = neutral.
                4 = dissatisfied.
                5 = very dissatisfied.
        """
        satisfaction = 1 if hotel_index + 1 == 1 else(
            2 if hotel_index + 1 <= (len(priority_hotels) * 0.25) else(
                3 if hotel_index + 1 <= (len(priority_hotels) * 0.5) else(
                    4 if hotel_index + 1 < (len(priority_hotels) * 0.75) else 5)))
        return satisfaction
    
    def allocate_guest(self, guest, hotel_list, allocation):
        """
        Allocate a guest to a hotel based on availability and preferences.

        Parameters:
            guest (str): The guest to be allocated.
            hotel_list (dict): Dictionary containing hotels and their available rooms.
            allocation (dict): Current allocation details.
            
        Returns:
            dict: Allocation details.
        """

        # guest's discount (from the guests DataFrame)
        guest_discount = self.guests[self.guests['guest'] == guest]['discount'].values[0]
        # guest's list of preferences (from the preference DataFrame).
        priority_hotels = self.pref[self.pref['guest'] == guest].sort_values(by='priority')['hotel'].tolist()

        # for loop to iterate over the hotel list. If it is in the guest's preference list and it is available, then it will substract
        # one room to the hotel in the dictionary.
        for hotel in hotel_list:
            if hotel in priority_hotels and hotel_list[hotel] > 0:
                hotel_list[hotel] -= 1

                # Calculate the net earning by subtracting the guest discount from the hotel's price after the allocation is complete.
                gross_earning = self.hotels[self.hotels['hotel'] == hotel]['price'].values[0]
                net_earning = gross_earning * (1 - guest_discount)

                # Calling the satisfaction function to calculate the guest's satsifaction level.
                satisfaction = self.satisfaction(priority_hotels = priority_hotels, hotel_index = priority_hotels.index(hotel))

                # Appending results from each iteration, to the allocation dictionary.
                allocation['guest'].append(guest)
                allocation['hotel'].append(hotel)
                allocation['net_earning'].append(net_earning)
                allocation['guest_satisfaction'].append(satisfaction)
                break

        return allocation

    @property
    def random(self):
        """
        Randomly allocates guests to hotels.

        Algorithm:
            1. Randomly order both guests and hotels.
            2. Iterate through guests and hotels, allocating based on preferences and availability.
            3. Calculate net earnings for each hotel and guests' satisfaction.
            4. Return a Pandas DataFrame with the allocation details.

        Returns:
            DataFrame: Allocation details with columns ['guest', 'hotel', 'net_earning', 'guest_satisfaction'].
        """

        # Dictionary to store all the allocations.
        allocation = {'guest': [], 'hotel': [], 'net_earning': [], 'guest_satisfaction': []}
        
        # Random list of guests.
        random_guest = np.random.choice(self.guests['guest'],size = len(self.guests)).tolist()
        
        # Pandas Series containing hotels and number of rooms.
        hotel_list = pd.Series(self.hotels['rooms'].values, index = self.hotels['hotel'])
        
        # Randomly order the hotel_list and transform it into a dictionary for easier manipulation and room availability calculations.
        random_hotel = hotel_list.sample(frac = 1).to_dict() 

        # for loop to iterate over the guest's list and allocate a hotel to him by calling the "allocate_guest" function.
        for guest in random_guest:       
            allocation = self.allocate_guest(guest, random_hotel, allocation)
        
        # Transform the dictionary to a Pandas DataFrame to easily manipulate for calculations and graphs, and returns the DataFrame.
        random_allocation = pd.DataFrame(allocation)
        return random_allocation
    

    @property
    def preference(self):
        
        """
        Allocates guests to hotels based on guest preferences.

        Algorithm:
            1. Obtain a list of the guests and a dictionary of the hotels with their availability.
            2. Iterate through guests and allocate each guest to a hotel based on availability and preferences.
            3. Calculate net earnings for each hotel and guests' satisfaction.
            4. Return a Pandas DataFrame with the allocation details.

        Returns:
            DataFrame: Allocation details with columns ['guest', 'hotel', 'net_earning', 'guest_satisfaction'].
        """

        # Dictionary to store all the allocations.
        allocation = {'guest': [], 'hotel': [], 'net_earning': [], 'guest_satisfaction': []}

        # List of guests.
        guest_list = self.guests['guest'].tolist()

        # Pandas Series containing hotels and number of rooms is transformed into a dictionary, so manipulation and calculation of
        # room availability is easier. 
        hotel_list = pd.Series(self.hotels['rooms'].values, index = self.hotels.hotel).to_dict()

        # for loop to iterate over the guests' list, retrieving the guest's discount (from the guests DataFrame) and the list of
        # preferences (from the preference DataFrame).    
        for guest in guest_list:
            guest_discount = self.guests[self.guests['guest'] == guest]['discount'].values[0]
            priority_hotels = self.pref[self.pref['guest'] == guest].sort_values(by='priority')['hotel'].tolist()

            # for loop to iterate over the guest's preference list. If it is in the guest's preference list and it is available,
            # then it will substract one room to the hotel in the dictionary.
            for hotel in priority_hotels:
                if hotel_list[hotel] > 0:
                    hotel_list[hotel] -= 1

                    # Calculate the net earning by subtracting the guest discount from the hotel's price after the allocation is
                    # complete.
                    gross_earning = self.hotels[self.hotels['hotel'] == hotel]['price'].values[0]
                    net_earning = gross_earning * (1 - guest_discount)

                    # Calling the satisfaction function to calculate the guest's satsifaction level.
                    satisfaction = self.satisfaction(priority_hotels = priority_hotels, hotel_index = priority_hotels.index(hotel))

                    # Appending results from each iteration, to the allocation dictionary.
                    allocation['guest'].append(guest)
                    allocation['hotel'].append(hotel)
                    allocation['net_earning'].append(net_earning)
                    allocation['guest_satisfaction'].append(satisfaction)
                    break

        # Transform the dictionary to a Pandas DataFrame to easily manipulate for calculations and graphs, and returns the DataFrame.             
        priority_allocation = pd.DataFrame(allocation)
        return priority_allocation
    

    @property
    def price(self):
    
        """
        Allocates guests to hotels based on the hotels' prices (cheapest to most expensive).

        Algorithm:
            1. Order hotels based on price.
            2. Iterate through guests and allocate each guest to a hotel based on price, availability and preferences.
            3. Calculate net earnings for each hotel and guests' satisfaction.
            4. Return a Pandas DataFrame with the allocation details.

        Returns:
            DataFrame: Allocation details with columns ['guest', 'hotel', 'net_earning', 'guest_satisfaction'].
        """
        
        # Dictionary to store all the allocations.
        allocation = {'guest': [], 'hotel': [], 'net_earning': [], 'guest_satisfaction': []}
        
        # List of guests.
        guest_list = self.guests['guest'].tolist()

        # Pandas Series, containing hotels ordered by price (ascending) and the number of rooms available, is transformed into a
        # dictionary, so manipulation and calculation of room availability is easier.
        hotel_ordered = self.hotels.sort_values(by = 'price') 
        hotel_list = pd.Series(hotel_ordered['rooms'].values, index = hotel_ordered.hotel).to_dict()


        # for loop to iterate over the guests' list, retrieving the guest's discount (from the guests DataFrame) and the list of
        # preferences (from the preference DataFrame).    
        for guest in guest_list:
            allocation = self.allocate_guest(guest, hotel_list, allocation)
        
        # Transform the dictionary to a Pandas DataFrame to easily manipulate for calculations and graphs, and returns the DataFrame.
        price_allocation = pd.DataFrame(allocation)
        return price_allocation
    

    @property
    def rooms(self):
        
        """
        Allocates guests to hotels based on the hotels' room availability (most roomy to least roomy).

        Algorithm:
            1. Order hotels based on room availability.
            2. Iterate through guests and allocate each guest to a hotel based on room availability, availability and preferences.
            3. Calculate net earnings for each hotel and guests' satisfaction.
            4. Return a Pandas DataFrame with the allocation details.

        Returns:
            DataFrame: Allocation details with columns ['guest', 'hotel', 'net_earning', 'guest_satisfaction'].
        """

        # Dictionary to store all the allocations.
        allocation = {'guest': [], 'hotel': [], 'net_earning': [], 'guest_satisfaction': []}
        
        # List of guests.
        guest_list = self.guests['guest'].tolist()

        # Pandas Series, containing hotels ordered by rooms availability (ascending) and the number of rooms available, is transformed
        # into a dictionary, so manipulation and calculation of room availability is easier.
        hotel_ordered = self.hotels.sort_values(by = 'rooms', ascending = False) 
        hotel_list = pd.Series(hotel_ordered['rooms'].values, index = hotel_ordered.hotel).to_dict()

        # for loop to iterate over the guests' list, retrieving the guest's discount (from the guests DataFrame) and the list of
        # preferences (from the preference DataFrame).        
        for guest in guest_list:
            allocation = self.allocate_guest(guest, hotel_list, allocation)
        
        # Transform the dictionary to a Pandas DataFrame to easily manipulate for calculations and graphs, and returns the DataFrame.
        room_allocation = pd.DataFrame(allocation)
        return room_allocation