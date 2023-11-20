import pandas as pd

hotelsdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/hotels.xlsx").set_index('hotel')
guestdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/guests.xlsx").set_index('guest')
preferencesdata=pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/preferences.xlsx").drop_duplicates(subset=['guest','hotel'])
from tests.satisfactionpercentage import calculate_satisfaction_percentage
from hotel_project.final.vizualization import visualize_allocation
from hotel_project.final.output import allocation_analysis

#to allocate in the order of preference
def allocate_preferred_rooms(hotel_id, hotel_row, guestdata, preferencesdata, allocation):
    #dictionary where we assigning hotels to a guests, all guests who prefer this hotel
    guests_who_preferred_hotel = preferencesdata[preferencesdata['hotel'] == hotel_id]['guest']
    guests_to_allocate = guests_who_preferred_hotel[~guests_who_preferred_hotel.isin(allocation['guest_id'])]
    # as well
    hotel_available_rooms = hotel_row['rooms']

    for _, guest_id in guests_to_allocate.items():
        if hotel_available_rooms == 0:
            break
        #excluding one room
        hotel_available_rooms -= 1
        #returning the row according to a guest id
        guest_row = guestdata.loc[guest_id]

        paid_price_coefficient = 1 - guest_row['discount']
        paid_price = hotel_row['price'] * paid_price_coefficient

        satisfaction = calculate_satisfaction_percentage(guest_id, hotel_id, preferencesdata)
        #output
        allocation.loc[len(allocation)] = [guest_id, hotel_id, satisfaction, paid_price]

    return hotel_available_rooms, allocation


def allocate_remaining_rooms(hotel_available_rooms, hotel_id, hotel_row, guestdata, allocation):
    guests_to_allocate = guestdata[~guestdata.index.isin(allocation['guest_id'])]
    for guest_id, guest_row in guests_to_allocate.iterrows():
        if hotel_available_rooms == 0:
            break

        hotel_available_rooms -= 1

        paid_price_coefficient = 1 - guest_row['discount']
        paid_price = hotel_row['price'] * paid_price_coefficient

        allocation.loc[len(allocation)] = [guest_id, hotel_id, 0, paid_price]

    return allocation


def get_price_allocation(hotelsdata, guestdata, preferencesdata):
    allocation = pd.DataFrame(columns=['guest_id', 'hotel_id', 'satisfaction_percentage', 'paid_price'])

    sorted_hotels = hotelsdata.sort_values(by='price')
    #for every index and every row
    for hotel_id, hotel_row in sorted_hotels.iterrows():
        hotel_remaining_rooms_count, allocation = allocate_preferred_rooms(hotel_id, hotel_row, guestdata, preferencesdata, allocation)
        if hotel_remaining_rooms_count > 0:
            allocation = allocate_remaining_rooms(hotel_remaining_rooms_count,  hotel_id, hotel_row, guestdata, allocation)

    return allocation

print('Start calculate price allocation')
price_allocation = get_price_allocation(hotelsdata, guestdata, preferencesdata)
allocation_analysis(price_allocation)
visualize_allocation(price_allocation.head(20))