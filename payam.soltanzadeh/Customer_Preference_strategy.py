#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import os
from IPython.display import display, FileLink
from ipywidgets import Button, Output, Layout
import random
import numpy as np
import matplotlib.pyplot as plt


# Function to clean data
def clean_data(df, dataset_type):
    # Remove unnamed columns
    df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col], errors='ignore')

    # Check for missing values
    if df.isnull().sum().any():
        raise ValueError(f"Missing values found in {dataset_type} dataset")

    # Data-specific checks
    if dataset_type == 'hotels':
        if (df['rooms'] < 0).any() or (df['price'] < 0).any():
            raise ValueError("Negative values found in room count or price in hotels dataset")
    elif dataset_type == 'guests':
        if (df['discount'] < 0).any() or (df['discount'] > 1).any():
            raise ValueError("Invalid discount values in guests dataset")
    elif dataset_type == 'preferences':
        if (df['priority'] <= 0).any():
            raise ValueError("Non-positive priority values found in preferences dataset")

    return df

# Function to load datasets
def load_datasets(hotels_path, guests_path, preferences_path):
    try:
        hotels_df = pd.read_excel(hotels_path)
        guests_df = pd.read_excel(guests_path)
        preferences_df = pd.read_excel(preferences_path)

        # Clean and validate data
        hotels_df = clean_data(hotels_df, 'hotels')
        guests_df = clean_data(guests_df, 'guests')
        preferences_df = clean_data(preferences_df, 'preferences')

        return hotels_df, guests_df, preferences_df
    except Exception as e:
        print(f"Error loading file: {e}")
        exit()

def customer_preference_allocation(hotels_df, guests_df, preferences_df):
    # Data Integrity Checks
    # Check for Null Values
    if guests_df['guest'].isnull().any():
        raise ValueError("Missing guest data in guests_df")
    if hotels_df['hotel'].isnull().any():
        raise ValueError("Missing hotel data in hotels_df")
    if preferences_df.isnull().any().any():  # Checks for any null value in the entire DataFrame
        raise ValueError("Missing data in preferences_df")

    # Ensure all guests have preferences
    guests_with_preferences = preferences_df['guest'].unique()
    if not all(guest in guests_with_preferences for guest in guests_df['guest']):
        raise ValueError("Not all guests have hotel preferences")

    # Ensure all preferred hotels exist in the hotels list
    hotels_in_preferences = set(preferences_df['hotel'])
    if not hotels_in_preferences.issubset(set(hotels_df['hotel'])):
        raise ValueError("Some hotels in preferences are not in the hotels list")

    # Sort guests by the order of reservation (assuming the order in the guests_df is the reservation order)
    guests_list = guests_df['guest'].tolist()

    # Initialize the result dictionary
    allocation_results = {
        'guest': [],
        'hotel': [],
        'final_price': [],
        'guest_satisfaction': []  # How high the allocated hotel was on the guest's preference list
    }

    # Convert room availability to a dictionary for faster updates
    room_availability = hotels_df.set_index('hotel')['rooms'].to_dict()

    # Pre-compute discounts and room prices for efficiency
    guest_discounts = guests_df.set_index('guest')['discount'].to_dict()
    hotel_prices = hotels_df.set_index('hotel')['price'].to_dict()

    # Iterate over the list of guests
    for guest in guests_list:
        # Get the discount for the guest
        discount = guest_discounts[guest]

        # Get the ordered list of preferred hotels for the guest
        preferred_hotels = preferences_df[preferences_df['guest'] == guest] \
            .sort_values(by='priority')['hotel'].tolist()

        # Try to find an available hotel from the guest's preferences
        for hotel in preferred_hotels:
            if room_availability.get(hotel, 0) > 0:
                # Update room availability
                room_availability[hotel] -= 1

                # Calculate price paid with discount
                room_price = hotel_prices[hotel]
                final_price = room_price * (1 - discount)

                # Determine preference score (1 is highest preference) and convert to integer
                guest_satisfaction = int(preferred_hotels.index(hotel) + 1)

                # Add to results
                allocation_results['guest'].append(guest)
                allocation_results['hotel'].append(hotel)
                allocation_results['final_price'].append(final_price)
                allocation_results['guest_satisfaction'].append(guest_satisfaction)
                
                break
        else:
            # Guest could not be allocated to any hotel
            allocation_results['guest'].append(guest)
            allocation_results['hotel'].append(None)
            allocation_results['final_price'].append(0)
            allocation_results['guest_satisfaction'].append(None)
            
    allocation_df = pd.DataFrame(allocation_results)
    

    # Convert the guest_satisfaction column to integer type
    allocation_df['guest_satisfaction'] = allocation_df['guest_satisfaction'].fillna(0).astype(int)
    return allocation_df



# Function to calculate metrics
def calculate_metrics(allocation_df, hotels_df):
    # Calculate the number of fully occupied hotels
    allocated_room_counts = allocation_df['hotel'].value_counts()
    hotels_fully_occupied = sum(
        allocated_room_counts.get(hotel, 0) == room_count
        for hotel, room_count in hotels_df.set_index('hotel')['rooms'].items()
    )

    # Calculating the metrics
    results = {
        "Total Guests Allocated": allocation_df[allocation_df['hotel'].notnull()].shape[0],
        "Total Rooms Filled": allocation_df[allocation_df['hotel'].notnull()].shape[0],  # Same as Guests Allocated
        "Number of Hotels Utilized": allocation_df['hotel'].nunique(),
        "Full Capacity Hotels Count": hotels_fully_occupied,
        "Overall Revenue Earned": allocation_df['final_price'].sum(),
        "Average Earnings Per Hotel": allocation_df.groupby('hotel')['final_price'].sum().mean(),
        "Average Guest Satisfaction": allocation_df['guest_satisfaction'].mean(),
    }

    return pd.DataFrame(list(results.items()), columns=['Metric', 'Value'])


    



def style_dataframe(df):
    if 'final_price' in df.columns:  # Check if final_price column is present
        return df.style \
            .background_gradient(cmap='Blues') \
            .set_properties(**{'text-align': 'left', 'font-size': '12pt'}) \
            .format({'final_price': "€{:,.2f}"}) \
            .set_table_styles([{'selector': 'th', 'props': [('font-size', '12pt'), ('text-align', 'center')]}])
    else:  # For the metrics table
        # Custom formatter for different metrics
        def custom_format(x, metric):
            if metric in ["Overall Revenue Earned", "Average Earnings Per Hotel"]:
                return f"€{x:,.4f}"
            elif metric == "Average Guest Satisfaction":
                return f"{x:.2f}"
            return f"{x:,.0f}"

        return df.style \
            .background_gradient(cmap='Blues') \
            .set_properties(**{'text-align': 'left', 'font-size': '12pt'}) \
            .format({'Value': lambda x: custom_format(x, df[df['Value'] == x]['Metric'].iloc[0])}) \
            .set_table_styles([{'selector': 'th', 'props': [('font-size', '12pt'), ('text-align', 'center')]}])


# Function to save results and show sub of the tables 
def save_files(allocation_df, results_df, directory='results'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        csv_path = os.path.join(directory, 'customer_preference_results.csv')
        txt_path = os.path.join(directory, 'summary_report_customer_preference.txt')

        allocation_df.to_csv(csv_path, index=False)
        with open(txt_path, 'w') as file:
            file.write("Summary Report of Random Allocation Strategy\n")
            file.write("-------------------------------------------------\n")
            file.writelines([f"{row['Metric']}: {row['Value']}\n" for _, row in results_df.iterrows()])

        return csv_path, txt_path
    except Exception as e:
        print(f"Error saving files: {e}")
        return None, None




from IPython.display import HTML, Markdown

def display_with_description(description, dataframe, post_description=None):
    display(HTML(description))
    display(style_dataframe(dataframe))
    if post_description:
        display(Markdown(post_description))



# Main execution block
def main():
    hotels_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/hotels.xlsx'
    guests_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/guests.xlsx'
    preferences_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/preferences.xlsx'

    # Load and clean datasets
    hotels_df, guests_df, preferences_df = load_datasets(hotels_path, guests_path, preferences_path)

    # Execute the Random_allocation function with the loaded data
    customer_preference_allocation_df = customer_preference_allocation(hotels_df,guests_df, preferences_df)

    # Calculate metrics
    results_df = calculate_metrics(customer_preference_allocation_df, hotels_df)

    # Display tables with descriptions
    allocation_description = "<b>Table 1: Allocation Results Summary</b><br>This table shows the distribution of guests across various hotels, the price paid, and their satisfaction scores."
    allocation_post_description = "*Note: Only the first 5 rows are displayed for brevity. For the complete data, please use the download link below.*"
    display_with_description(allocation_description, customer_preference_allocation_df.head(), allocation_post_description)
    metrics_description = "<b>Table 2: Performance Metrics Overview</b><br>This table provides key metrics summarizing the allocation's effectiveness, including total guests allocated, revenue earned, and average guest satisfaction."
    metrics_post_description = "*Note: Guest satisfaction scores range from 1 to 5, with 1 being the guest's top choice and 5 being around their last preference.*"
    display_with_description(metrics_description, results_df, metrics_post_description)

    # Save files and display download links
    csv_path, txt_path = save_files(customer_preference_allocation_df, results_df)
    if csv_path and txt_path:
        display(FileLink(csv_path, result_html_prefix="Download CSV: "))
        display(FileLink(txt_path, result_html_prefix="Download Summary Report: "))

# Run the script
if __name__ == "__main__":
    main()


# In[ ]:




