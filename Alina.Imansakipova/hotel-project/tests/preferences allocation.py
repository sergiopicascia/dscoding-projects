import pandas as pd

hotelsdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/hotels.xlsx").set_index('hotel')
guestdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/guests.xlsx").set_index('guest')
preferencesdata=pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/preferences.xlsx").drop_duplicates(subset=['guest','hotel'])
from tests.satisfactionpercentage import calculate_satisfaction_percentage
from hotel_project.final.vizualization import visualize_allocation
from hotel_project.final.output import allocation_analysis

def allocate_preferred_hotel(guest_id, guest_row, hotelsdata, preferencesdata):
    # dictionary, where we turn the table into dictionary
    guest_preferred_hotels = preferencesdata[preferencesdata['guest'] == guest_id]['hotel']
    for _, preferred_hotel_id in guest_preferred_hotels.items():
        # we returning the row of a matrix
        preferred_hotel_row = hotelsdata.loc[preferred_hotel_id]

        if preferred_hotel_row['rooms'] > 0:
            preferred_hotel_row['rooms'] -= 1

            paid_price_coefficient = 1 - guest_row['discount']
            paid_price = preferred_hotel_row['price'] * paid_price_coefficient

            satisfaction = calculate_satisfaction_percentage(guest_id, preferred_hotel_id, preferencesdata)

            return [guest_id, preferred_hotel_id, satisfaction, paid_price]

    return None


def get_customer_preference_allocation(hotelsdata, guestdata, preferencesdata):
    allocation = pd.DataFrame(columns=['guest_id', 'hotel_id', 'satisfaction_percentage', 'paid_price'])

    for guest_id, guest_row in guestdata.iterrows():
        allocation_entry = allocate_preferred_hotel(guest_id, guest_row, hotelsdata, preferencesdata)
        if allocation_entry is not None:
            allocation.loc[len(allocation)] = allocation_entry

    return allocation


print('Start calculate preference allocation')
customer_preference_allocation = get_customer_preference_allocation(hotelsdata, guestdata, preferencesdata)
allocation_analysis(customer_preference_allocation)
visualize_allocation(customer_preference_allocation.head(20))