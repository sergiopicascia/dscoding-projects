import pandas as pd
from Visualization import visualization
from random_allocation import RandomHotelAllocation
from preferences_allocation import PreferencesAllocator
from price_allocation import PriceBasedAllocator
from availability_allocation import AvailabilityBasedAllocator


def main():
    guests= pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\guests.xlsx")
    hotels = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\hotels.xlsx")
    preferences = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\preferences.xlsx")
    
    print('calculate random allocation')
    random_allocator=RandomHotelAllocation(hotels, guests, preferences)
    r_allocation = random_allocator.get_r_allocation()
    visualization(r_allocation.head(20))
    
    print('calculate preferences allocation')
    preferences_allocator=PreferencesAllocator(hotels, guests, preferences)
    cp_allocation=preferences_allocator.get_cp_allocation()
    visualization(cp_allocation.head(20))
    
    print('calculate price allocation')
    price_allocator=PriceBasedAllocator(hotels, guests, preferences)
    p_allocation=price_allocator.get_p_allocation()
    visualization(p_allocation.head(20))
    
    print('calculate availability allocation')
    availability_allocator=AvailabilityBasedAllocator(hotels, guests, preferences)
    a_allocation=availability_allocator.get_a_allocation()
    visualization(a_allocation.head(20))
    