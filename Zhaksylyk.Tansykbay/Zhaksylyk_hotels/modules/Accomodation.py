import pandas as pd
import numpy as np

#Creating Solution class to perform accomodations according to the strategies, each written in their own class methods
class Solution:

    def __init__(self): #Initialize solution values
        self.guests_accomodated = 0
        self.rooms_occupied = 0
        self.diff_hotels = 0
        self.revenue = []
        self.satisfaction = []

    def random(self, guests_file, hotels_file, preferences_file):
        # Write the path to the EXCEL files
        guests = pd.read_excel(guests_file, sheet_name='Sheet1') 
        hotels = pd.read_excel(hotels_file, sheet_name='Sheet1') 
        preferences = pd.read_excel(preferences_file, sheet_name='Sheet1') 

        #Creating a copy of datasets for manipulations
        guests_copy = guests.copy()
        hotels_copy = hotels.copy()

        #Recording the initial number of guests, rooms
        initial_num_guests = len(guests)
        initial_num_rooms = hotels.rooms.sum()
        diff_hotels = set() #Initializing set for counting the number of different hotels occupied 

        for index in range(len(guests)): #Loop through all guests
            valid = False #Checking if the customer was accomodated
            while valid != True:
                rand_hotel = np.random.randint(0,400) #picking random hotel
                if hotels_copy.at[rand_hotel,'rooms'] > 0: #if there is a free room
                    valid = True #means accomodated
                    diff_hotels.add(rand_hotel) #adding to the set of different hotels
                    hotels_copy.at[rand_hotel,'rooms'] -= 1 #decreasing the number of free rooms by 1
                    prefs = preferences.loc[preferences['guest'] == f'guest_{index+1}'] #searching for accomodated customer's preferences 
                    pref = prefs.loc[prefs['hotel'] == f'hotel_{rand_hotel+1}'] #recording the preferences
                    if len(pref) != 0: # if hotel is in preferences
                        self.satisfaction.append(pref.priority[pref.priority.index[0]]/4000) # add the satisfaction score, dividing by 4000 in order to get mean score
                    else:
                        self.satisfaction.append(50/4000) # if hotel not in preferences, record as score 50
                else: 
                    valid = False

        final_num_rooms = hotels_copy.rooms.sum() # getting the final number of free rooms 
        for index in range(len(hotels)): # counting the revene by finding the difference in free rooms from initial dataset and final, and the multiplyong by price
            rev = abs(hotels.at[index, 'rooms'] - hotels_copy.at[index, 'rooms']) * hotels.at[index, 'price']
            self.revenue.append(rev)

        self.rooms_occupied = initial_num_rooms - final_num_rooms
        self.guests_accomodated = initial_num_rooms - final_num_rooms
        self.diff_hotels = len(diff_hotels)

        print("Random Accomodation Strategy")
        print(f"The number of guests accomodated: {self.rooms_occupied}")
        print(f"The number of rooms occupied: {self.guests_accomodated}")
        print(f"The number of different hotels occupied: {self.diff_hotels}")
        print("------------------------------------------------------------------")

    def preference(self, guests_file, hotels_file, preferences_file):
        # Write the path to the EXCEL files
        guests = pd.read_excel(guests_file, sheet_name='Sheet1') 
        hotels = pd.read_excel(hotels_file, sheet_name='Sheet1') 
        preferences = pd.read_excel(preferences_file, sheet_name='Sheet1') 

        guests_copy = guests.copy()
        hotels_copy = hotels.copy()

        initial_num_guests = len(guests)
        initial_num_rooms = hotels.rooms.sum()
        diff_hotels = set()

        for i in range(1,4001): # Loop through all guests
            prefs = preferences.loc[preferences['guest'] == f'guest_{i}'] # getting all of their preferences
            hotels_pref = prefs.hotel
            for h_num in hotels_pref: # Loop through all preferenced hotels
                if hotels_copy.at[hotels_copy.loc[hotels_copy['hotel'] == h_num].index[0], 'rooms'] > 0: # if there is a free room in current hotel
                    hotels_copy.at[hotels_copy.loc[hotels_copy['hotel'] == h_num].index[0], 'rooms'] -= 1 # accomodate the customer and decrease the number of free rooms by 1
                    diff_hotels.add(h_num)
                    pref = prefs.loc[prefs['hotel'] == h_num] # getting the satisfaction score
                    if len(pref) != 0:
                        self.satisfaction.append(pref.priority[pref.priority.index[0]]/4000)
                    else:
                        self.satisfaction.append(50/4000)
                    break
                else:
                    continue

        final_num_rooms = hotels_copy.rooms.sum()
        for index in range(len(hotels)):
            rev = abs(hotels.at[index, 'rooms'] - hotels_copy.at[index, 'rooms']) * hotels.at[index, 'price']
            self.revenue.append(rev)

        self.rooms_occupied = initial_num_rooms - final_num_rooms
        self.guests_accomodated = initial_num_rooms - final_num_rooms
        self.diff_hotels = len(diff_hotels)

        print("Customer Preference Accomodation Strategy")
        print(f"The number of guests accomodated: {self.rooms_occupied}")
        print(f"The number of rooms occupied: {self.guests_accomodated}")
        print(f"The number of different hotels occupied: {self.diff_hotels}")
        print("------------------------------------------------------------------")

    def cheapest_first(self, guests_file, hotels_file, preferences_file):
        # Write the path to the EXCEL files
        guests = pd.read_excel(guests_file, sheet_name='Sheet1') 
        hotels = pd.read_excel(hotels_file, sheet_name='Sheet1') 
        preferences = pd.read_excel(preferences_file, sheet_name='Sheet1') 

        guests_copy = guests.copy()
        hotels_sorted = hotels.sort_values(by='price') # sort the hotels dataset by price
        hotels_copy = hotels_sorted.copy()

        initial_num_guests = len(guests)
        initial_num_rooms = hotels.rooms.sum()
        diff_hotels = set()

        accomodated = [] # list for recording the accomodated guests

        for i in hotels_sorted.index: # Loop through sorted hotels dataset by indexing 
            g_index = 0 # keeping track of guests who prefer the current hotel
            order = preferences.loc[preferences['hotel'] == f'hotel_{i+1}'] 
            while hotels_copy.at[hotels_copy.loc[hotels_copy['hotel'] == f'hotel_{i+1}'].index[0], 'rooms'] > 0 and g_index < len(order): #Loop until the rooms ot guests for specific hotel are exhausted
                if order.iloc[g_index].guest not in accomodated: # if guest is not accomodated
                    accomodated.append(order.iloc[g_index].guest) # add guest to accomodated list
                    hotels_copy.at[hotels_copy.loc[hotels_copy['hotel'] == f'hotel_{i+1}'].index[0], 'rooms'] -= 1 #decrease the number of free room in the hotel
                    self.satisfaction.append(order.iloc[g_index].priority/4000) # record the satisfaction
                    diff_hotels.add(f'hotel_{i+1}')
                    g_index += 1 # increment the guest index
                else:
                    g_index += 1
                    continue

        final_num_rooms = hotels_copy.rooms.sum()
        for index in range(len(hotels_sorted)):
            rev = abs(hotels_sorted.at[index, 'rooms'] - hotels_copy.at[index, 'rooms']) * hotels.at[index, 'price']
            self.revenue.append(rev)

        self.rooms_occupied = initial_num_rooms - final_num_rooms
        self.guests_accomodated = initial_num_rooms - final_num_rooms
        self.diff_hotels = len(diff_hotels)

        print("Cheapest First + Preference Accomodation Strategy")
        print(f"The number of guests accomodated: {self.rooms_occupied}")
        print(f"The number of rooms occupied: {self.guests_accomodated}")
        print(f"The number of different hotels occupied: {self.diff_hotels}")
        print("------------------------------------------------------------------")

    def availability(self, guests_file, hotels_file, preferences_file):
        # Write the path to the EXCEL files
        guests = pd.read_excel(guests_file, sheet_name='Sheet1') 
        hotels = pd.read_excel(hotels_file, sheet_name='Sheet1') 
        preferences = pd.read_excel(preferences_file, sheet_name='Sheet1') 

        guests_copy = guests.copy()
        hotels_sorted = hotels.sort_values(by='rooms', ascending=False) # sort the hotels dataset by room in descending order
        hotels_copy = hotels_sorted.copy()

        initial_num_guests = len(guests)
        initial_num_rooms = hotels.rooms.sum()
        diff_hotels = set()

        accomodated = []

        for i in hotels_sorted.index:
            g_index = 0
            order = preferences.loc[preferences['hotel'] == f'hotel_{i+1}'] #.sort_values(by=['priority', 'Unnamed: 0'])
            while hotels_copy.at[hotels_copy.loc[hotels_copy['hotel'] == f'hotel_{i+1}'].index[0], 'rooms'] > 0 and g_index < len(order):
                if order.iloc[g_index].guest not in accomodated:
                    accomodated.append(order.iloc[g_index].guest)
                    hotels_copy.at[hotels_copy.loc[hotels_copy['hotel'] == f'hotel_{i+1}'].index[0], 'rooms'] -= 1
                    self.satisfaction.append(order.iloc[g_index].priority/4000)
                    diff_hotels.add(f'hotel_{i+1}')
                    g_index += 1
                else:
                    g_index += 1
                    continue

        final_num_rooms = hotels_copy.rooms.sum()
        for index in range(len(hotels_sorted)):
            rev = abs(hotels_sorted.at[index, 'rooms'] - hotels_copy.at[index, 'rooms']) * hotels.at[index, 'price']
            self.revenue.append(rev)

        self.rooms_occupied = initial_num_rooms - final_num_rooms
        self.guests_accomodated = initial_num_rooms - final_num_rooms
        self.diff_hotels = len(diff_hotels)

        print("Starting with the Most Roomy Hotels Accomodation Strategy")
        print(f"The number of guests accomodated: {self.rooms_occupied}")
        print(f"The number of rooms occupied: {self.guests_accomodated}")
        print(f"The number of different hotels occupied: {self.diff_hotels}")
        print("------------------------------------------------------------------")