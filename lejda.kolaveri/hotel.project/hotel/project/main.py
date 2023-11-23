import pandas as pd
from Visualization import visualization
from random_allocation import RandomHotelAllocation
from preferences_allocation import PreferencesAllocator
from price_allocation import PriceBasedAllocator
from availability_allocation import AvailabilityBasedAllocator
import utils


def main():
    guests= pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\guests.xlsx")
    hotels = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\hotels.xlsx")
    preferences = pd.read_excel(r"C:\Users\lejda\Desktop\coding - Python\preferences.xlsx")
    
    random_allocator = RandomHotelAllocation(hotels, guests, preferences)
    r_allocation = random_allocator.accomodate_guests()
    # Print and visualize random allocation
    print("Random Allocation:")
    print(r_allocation)
    visualization(r_allocation)
    
    preferences_allocator = PreferencesAllocator(hotels, guests, preferences)
    p_allocation = preferences_allocator.allocate_and_calculate()
    # Print and visualize preferences allocation
    print("Preferences Allocation:")
    print(p_allocation)
    visualization(p_allocation)
    
    price_allocator = PriceBasedAllocator(hotels, guests, preferences)
    price_allocation = price_allocator.allocate_and_calculate()
    # Print and visualize price-based allocation
    print("Price-Based Allocation:")
    print(price_allocation)
    visualization(price_allocation)
    
    availability_allocator = AvailabilityBasedAllocator(hotels, guests, preferences)
    availability_allocation = availability_allocator.allocate_and_calculate()
    # Print and visualize availability-based allocation
    print("Availability-Based Allocation:")
    print(availability_allocation)
    visualization(availability_allocation)

if __name__ == "__main__":
    main()