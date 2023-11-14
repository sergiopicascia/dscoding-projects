import pandas as pd

# Load the datasets
hotels_df = pd.read_excel('C:/Users/irpay/OneDrive/Documents/GitHub/payam/hotels.xlsx')
guests_df = pd.read_excel('C:/Users/irpay/OneDrive/Documents/GitHub/payam/guests.xlsx')
preferences_df = pd.read_excel('C:/Users/irpay/OneDrive/Documents/GitHub/payam/preferences.xlsx')

# Display the first few rows of each dataframe for inspection
hotels_head = hotels_df.head()
guests_head = guests_df.head()
preferences_head = preferences_df.head()

(hotels_head, guests_head, preferences_head)

# Remove the unnecessary 'Unnamed: 0' columns from all dataframes
hotels_df.drop(columns='Unnamed: 0', inplace=True)
guests_df.drop(columns='Unnamed: 0', inplace=True)
preferences_df.drop(columns='Unnamed: 0', inplace=True)

# Confirm the changes
hotels_df_cleaned = hotels_df.head()
guests_df_cleaned = guests_df.head()
preferences_df_cleaned = preferences_df.head()

(hotels_df_cleaned, guests_df_cleaned, preferences_df_cleaned)

import numpy as np


# Function to implement the random allocation strategy
def random_allocation(hotels_df, guests_df):
    # Create a shuffled list of guests
    guests_list = guests_df['guest'].sample(frac=1).tolist()

    # Initialize the result dictionary
    allocation_results = {
        'guest': [],
        'hotel': [],
        'price_paid': []
    }

    # Convert room availability to a dictionary for faster updates
    room_availability = hotels_df.set_index('hotel')['rooms'].to_dict()

    # Iterate over the shuffled list of guests
    for guest in guests_list:
        # Get the discount for the guest
        discount = guests_df[guests_df['guest'] == guest]['discount'].values[0]

        # Try to find an available hotel
        for hotel, available_rooms in room_availability.items():
            if available_rooms > 0:
                # Update room availability
                room_availability[hotel] -= 1

                # Calculate price paid with discount
                room_price = hotels_df[hotels_df['hotel'] == hotel]['price'].values[0]
                price_paid = room_price * (1 - discount)

                # Add to results
                allocation_results['guest'].append(guest)
                allocation_results['hotel'].append(hotel)
                allocation_results['price_paid'].append(price_paid)
                break  # Move on to the next guest after allocation

    # Convert the results to a DataFrame
    allocation_df = pd.DataFrame(allocation_results)
    return allocation_df


# Apply the random allocation strategy
random_allocation_df = random_allocation(hotels_df, guests_df)
random_allocation_df.head()  # Display the first few allocations


# Function to implement the customer preference allocation strategy
def customer_preference_allocation(hotels_df, guests_df, preferences_df):
    # Sort guests by the order of reservation (assuming the order in the guests_df is the reservation order)
    guests_list = guests_df['guest'].tolist()

    # Initialize the result dictionary
    allocation_results = {
        'guest': [],
        'hotel': [],
        'price_paid': [],
        'preference_score': []  # How high the allocated hotel was on the guest's preference list
    }

    # Convert room availability to a dictionary for faster updates
    room_availability = hotels_df.set_index('hotel')['rooms'].to_dict()

    # Iterate over the list of guests
    for guest in guests_list:
        # Get the discount for the guest
        discount = guests_df[guests_df['guest'] == guest]['discount'].values[0]

        # Get the ordered list of preferred hotels for the guest
        preferred_hotels = preferences_df[preferences_df['guest'] == guest] \
            .sort_values(by='priority')['hotel'].tolist()

        # Try to find an available hotel from the guest's preferences
        for hotel in preferred_hotels:
            if room_availability.get(hotel, 0) > 0:
                # Update room availability
                room_availability[hotel] -= 1

                # Calculate price paid with discount
                room_price = hotels_df[hotels_df['hotel'] == hotel]['price'].values[0]
                price_paid = room_price * (1 - discount)

                # Determine preference score (1 is highest preference)
                preference_score = preferred_hotels.index(hotel) + 1

                # Add to results
                allocation_results['guest'].append(guest)
                allocation_results['hotel'].append(hotel)
                allocation_results['price_paid'].append(price_paid)
                allocation_results['preference_score'].append(preference_score)
                break  # Move on to the next guest after allocation

    # Convert the results to a DataFrame
    allocation_df = pd.DataFrame(allocation_results)
    return allocation_df


# Apply the customer preference allocation strategy
customer_preference_allocation_df = customer_preference_allocation(hotels_df, guests_df, preferences_df)
customer_preference_allocation_df.head()  # Display the first few allocations