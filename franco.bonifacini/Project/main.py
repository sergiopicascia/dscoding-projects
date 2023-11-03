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
    random_guests = list(np.random.choice(guests_db["guest"], size=len(guests_db), replace=False))
    return random_guests

## Hotel rooms:
def Assigned_hotel():
    hotel_occupancy = {hotel: list(range(1, rooms + 1)) for hotel, rooms in zip(hotels_db['hotel'], hotels_db['rooms'])}
    assigned_hotels = [hotel for hotel, room_numbers in hotel_occupancy.items() for _ in room_numbers]
    return assigned_hotels

## Allocation:
def Random_allocation():
    guest = Random_guest()
    hotel_room = Hotel_rooms()
    length = min(len(guest),len(hotel_room))
    allocation = ['{} in {}'.format(guest, room) for guest, room in zip(guest[:length],hotel_room[:length])]
    return allocation

#PREFERENCE ALLOCATION:
