import pandas as pd
from random_allocation_strategy import RandomAllocator
from preference_allocation_strategy import PreferenceAllocator
from price_allocation_strategy import PriceAllocator
from availability_allocation_strategy import AvailableRoomAllocator
from data_visualization import visualize_allocation
from utils import print_allocation_data
def main():
    # Read the data from the excel sheets
    hotels = pd.read_excel(r"/Users/tesi/Downloads/hotels/hotels.xlsx").set_index('hotel')
    guests = pd.read_excel(r"/Users/tesi/Downloads/hotels/guests.xlsx").set_index('guest')
    preferences = pd.read_excel(r"/Users/tesi/Downloads/hotels/preferences.xlsx").drop_duplicates(subset=['guest', 'hotel'])

    comment = """
    This program visualizes the data generated from the different methods of allocation.
    For each of the allocations, the generated data is displayed in three plots as follows:
    """

    print(comment)

    # For each allocation, we call the function that does the allocation in terms of preference,
    # price, availability and randomly
    # call the visualize_allocation function to create 3 graphs for each allocation
    # call the print_allocation_data to make a summary of the data that is in the graphs

    random_allocator = RandomAllocator(hotels.copy(), guests, preferences)
    print('Random Allocation Strategy')
    allocation_randomly = random_allocator.allocate_randomly()
    visualize_allocation(allocation_randomly.head(15))
    print_allocation_data(allocation_randomly)

    preference_allocator = PreferenceAllocator(hotels.copy(), guests, preferences)
    print('Customer Preference Allocation Strategy')
    allocation_by_customer_preference = preference_allocator.allocate_by_priority()
    visualize_allocation(allocation_by_customer_preference.head(15))
    print_allocation_data(allocation_by_customer_preference)

    price_allocator = PriceAllocator(hotels, guests, preferences)
    print('Price Allocation Strategy')
    allocation_by_price = price_allocator.allocate_by_price()
    visualize_allocation(allocation_by_price.head(15))
    print_allocation_data(allocation_by_price)

    availability_allocator = AvailableRoomAllocator(hotels, guests, preferences)
    print('Availability Allocation Strategy')
    allocation_by_availability = availability_allocator.allocate_by_availability()
    visualize_allocation(allocation_by_availability.head(15))
    print_allocation_data(allocation_by_availability)

if __name__ == "__main__":
    main()