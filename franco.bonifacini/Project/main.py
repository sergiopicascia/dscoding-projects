#Import libraries
import pandas as pd
import numpy as np
import matplotlib as mpl
import seaborn as sbr

# Import datasets:
guests_db = pd.read_excel('Project/Datasets/guests.xlsx')
hotels_db = pd.read_excel('Project/Datasets/hotels.xlsx')
pref_db = pd.read_excel('Project/Datasets/preferences.xlsx')

#RANDOM ALLOCATION:
## Random Guest:
def Random_guest():
    Random_guests = list(np.random.choice(guests_db["guest"],size = len(guests_db), replace = False))
    return Random_guests

## Random hotel rooms:
def Random_hotel():
    hotel_list = []
    for hotel, rooms in zip(hotels_db['hotel'], hotels_db['rooms']):
        hotel_list.extend([hotel] * rooms)

    np.random.shuffle(hotel_list)
    return hotel_list

## Random Allocation:
def Random_allocation():
    guest = Random_guest()
    hotel = Random_hotel()
    length = min(len(guest),len(hotel))
    allocation = [[guest, hotel] for guest, hotel in zip(guest[:length],hotel[:length])]
    return allocation

#PREFERENCE ALLOCATION:
