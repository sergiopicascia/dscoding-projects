import pandas as pd
import random

hotelsdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/hotels.xlsx").set_index('hotel')
guestdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/guests.xlsx").set_index('guest')
preferencesdata=pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/preferences.xlsx").drop_duplicates(subset=['guest','hotel'])
from tests.satisfactionpercentage import calculate_satisfaction_percentage
from hotel_project.final.vizualization import visualize_allocation
from hotel_project.final.output import allocation_analysis

def allocate_random_hotel(guest_id, guest_row, hotelsdata, preferencesdata):
    available_hotels = hotelsdata[hotelsdata['rooms'] > 0]
    if available_hotels.empty:
        return None

    # randomly picking the hotel
    random_available_hotel_id = random.choice(available_hotels.index)
    # returning the row (aka the room)
    random_available_hotel_row = available_hotels.loc[random_available_hotel_id]
    # excluding the room from table of available rooms
    random_available_hotel_row['rooms'] -= 1

    paid_price_coefficient = 1 - guest_row['discount']
    paid_price = random_available_hotel_row['price'] * paid_price_coefficient

    satisfaction = calculate_satisfaction_percentage(guest_id, random_available_hotel_id, preferencesdata)

    return [guest_id, random_available_hotel_id, satisfaction, paid_price]

def get_random_allocation(hotelsdata, guestdata, preferencesdata):
    allocation = pd.DataFrame(columns=['guest_id', 'hotel_id', 'satisfaction_percentage', 'paid_price'])

    # randomizing guests
    shuffled_guests = guestdata.sample(frac=1, random_state=42)
    # we're taking every guest_id AND every pair guest_id|discount
    for guest_id, guest_row in shuffled_guests.iterrows():
        allocation_entry = allocate_random_hotel(guest_id, guest_row, hotelsdata, preferencesdata)
        if allocation_entry is not None:
            allocation.loc[len(allocation)] = allocation_entry

    return allocation

print('Start calculate random allocation')
random_allocation = get_random_allocation(hotelsdata.copy(), guestdata, preferencesdata)
allocation_analysis(random_allocation)
visualize_allocation(random_allocation.head(20))