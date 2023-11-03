import pandas as pd

# Load the datasets
hotels = pd.read_excel("C:\Users\irpay\OneDrive\Documents\GitHub\hotels.xlsx")
guests = pd.read_excel("C:\Users\irpay\OneDrive\Documents\GitHub\guests.xlsx")
preferences = pd.read_excel("C:\Users\irpay\OneDrive\Documents\GitHub\preferences.xlsx")

# Explore the first few rows of each dataset
(hotels.head(), guests.head(), preferences.head())


# Step 2: Data Pre-processing

hotels = hotels.set_index('Unnamed: 0')
guests = guests.set_index('Unnamed: 0')
preferences = preferences.set_index('Unnamed: 0')

# 2. Data Type Verification
data_types = (hotels.dtypes, guests.dtypes, preferences.dtypes)

# 3. Missing Values Check
missing_values = (hotels.isnull().sum(), guests.isnull().sum(), preferences.isnull().sum())

(data_types, missing_values)


import random

# Helper function to calculate price paid by customer after discount
def calculate_price(room_price, discount):
    return room_price * (1 - discount)

# Helper function to calculate customer satisfaction
def calculate_satisfaction(actual_hotel, preferred_hotels):
    # If the actual hotel is in the preferred list, return the inverse of the preference rank, else return 0
    preferred_hotels = preferred_hotels.set_index('hotel')
    if actual_hotel in preferred_hotels.index:
        return 1 / preferred_hotels.loc[actual_hotel, 'priority']
    else:
        return 0

