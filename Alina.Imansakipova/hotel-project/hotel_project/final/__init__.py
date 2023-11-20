import pandas as pd

from output import allocation_analysis
from vizualization import visualize_allocation
from random_allocation_class import RandomHotelAllocator
from availability_allocation_class import HotelAvailabilityAllocator
from preferences_allocation_class import HotelPreferenceAllocator
from price_allocation_class import HotelPriceAllocator

def main():
    hotelsdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/hotels.xlsx").set_index('hotel')
    guestdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/guests.xlsx").set_index('guest')
    preferencesdata = pd.read_excel(r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/preferences.xlsx").drop_duplicates(subset=['guest', 'hotel'])


    print('Start calculate random allocation')
    r_allocator = RandomHotelAllocator(hotelsdata.copy(), guestdata, preferencesdata)
    random_allocation = r_allocator.get_random_allocation()
    allocation_analysis(random_allocation)
    visualize_allocation(random_allocation.head(30))

    print('Start calculate availability allocation')
    a_allocator = HotelAvailabilityAllocator(hotelsdata.copy(), guestdata, preferencesdata)
    availability_allocation = a_allocator.get_availability_allocation()
    allocation_analysis(availability_allocation)
    visualize_allocation(availability_allocation.head(30))

    print('Start calculate price allocation')
    price_allocator = HotelPriceAllocator(hotelsdata.copy(), guestdata, preferencesdata)
    price_allocation = price_allocator.get_price_allocation()
    allocation_analysis(price_allocation)
    visualize_allocation(price_allocation.head(30))

    print('Start calculate preference allocation')
    pref_allocator = HotelPreferenceAllocator(hotelsdata.copy(), guestdata, preferencesdata)
    customer_preference_allocation = pref_allocator.get_customer_preference_allocation()
    allocation_analysis(customer_preference_allocation)
    visualize_allocation(customer_preference_allocation.head(30))

if __name__ == "__main__":
    main()
