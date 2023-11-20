import pandas as pd
import streamlit as st

from random_allocation_class import RandomHotelAllocator
from availability_allocation_class import HotelAvailabilityAllocator
from preferences_allocation_class import HotelPreferenceAllocator
from price_allocation_class import HotelPriceAllocator

def allocation_analysis(allocation):
    result = {}
    result['Customers accommodated'] = allocation['guest_id'].count()
    result['Number of rooms occupied'] = allocation['guest_id'].count()
    result['Number of different hotels occupied'] = allocation['hotel_id'].nunique()
    result['Average satisfaction'] = round(allocation['satisfaction_percentage'].mean(), 2)

    return result

def main():
    hotelsdata = pd.read_excel(
        r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/hotels.xlsx").set_index('hotel')
    guestdata = pd.read_excel(
        r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/guests.xlsx").set_index('guest')
    preferencesdata = pd.read_excel(
        r"/Users/menimalina/Desktop/uni_due/coding/python/python-project/hotels/preferences.xlsx").drop_duplicates(
        subset=['guest', 'hotel'])

    r_allocator = RandomHotelAllocator(hotelsdata.copy(), guestdata, preferencesdata)
    a_allocator = HotelAvailabilityAllocator(hotelsdata.copy(), guestdata, preferencesdata)
    price_allocator = HotelPriceAllocator(hotelsdata.copy(), guestdata, preferencesdata)
    pref_allocator = HotelPreferenceAllocator(hotelsdata.copy(), guestdata, preferencesdata)

    st.title("Hotel Allocation App")

    allocation_method = st.sidebar.radio("Choose Allocation Method", ["Randomly","By availability", "By price","By customer preferences"])

    # Display allocation based on the chosen method
    if allocation_method == "Randomly":
        final_allocation = r_allocator.get_random_allocation()
    elif allocation_method == "By availability":
        final_allocation = a_allocator.get_availability_allocation()
    elif allocation_method == "By price":
        final_allocation = price_allocator.get_price_allocation()
    else:
        final_allocation = pref_allocator.get_customer_preference_allocation()

    if st.button('Perform Allocation Analysis'):
        analysis_result = allocation_analysis(final_allocation)
        for key, value in analysis_result.items():
            st.write(f'{key}: {value}')
    # Display the result
    st.dataframe(final_allocation)


if __name__ == "__main__":
    main()