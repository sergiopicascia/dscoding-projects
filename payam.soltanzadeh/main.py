#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
import os
from IPython.display import display, HTML, FileLink
import numpy as np
import random

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
    hotels_df = pd.read_excel(hotels_path)
    guests_df = pd.read_excel(guests_path)
    preferences_df = pd.read_excel(preferences_path)

    # Clean and validate data
    hotels_df = clean_data(hotels_df, 'hotels')
    guests_df = clean_data(guests_df, 'guests')
    preferences_df = clean_data(preferences_df, 'preferences')

    return hotels_df, guests_df, preferences_df

# Customer Preference Allocation function
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


# Random Allocation function
# Random Allocation function 
def random_allocation(guests_df, hotels_df, preferences_df):
    allocation = {'guest': [], 'hotel': [], 'final_price': [], 'guest_satisfaction': []}
    random_guest = np.random.choice(guests_df['guest'], size=len(guests_df), replace=False).tolist()
    hotel_list = pd.Series(hotels_df['rooms'].values, index=hotels_df['hotel'])
    random_hotel = hotel_list.sample(frac=1).to_dict()
    
    allocated_guests = set()  # Set to keep track of already allocated guests

    for guest in random_guest:
        if guest in allocated_guests:  # Skip if guest is already allocated
            continue

        guest_discount = guests_df[guests_df['guest'] == guest]['discount'].values[0]
        priority_hotels = preferences_df[preferences_df['guest'] == guest].sort_values(by='priority')['hotel'].tolist()
        
        for hotel in random_hotel:
            if hotel in priority_hotels and random_hotel[hotel] > 0:
                random_hotel[hotel] -= 1
                gross_earning = hotels_df[hotels_df['hotel'] == hotel]['price'].values[0]
                net_earning = gross_earning * (1 - guest_discount)
                satisfaction = 1 if priority_hotels.index(hotel) + 1 == 1 else (
                    2 if priority_hotels.index(hotel) + 1 <= (len(priority_hotels) * 0.25) else (
                    3 if priority_hotels.index(hotel) + 1 <= (len(priority_hotels) * 0.5) else (
                    4 if priority_hotels.index(hotel) + 1 < (len(priority_hotels) * 0.75) else 5)))
                allocation['guest'].append(guest)
                allocation['hotel'].append(hotel)
                allocation['final_price'].append(net_earning)
                allocation['guest_satisfaction'].append(satisfaction)
                
                allocated_guests.add(guest)  # Mark the guest as allocated
                break  # Move to the next guest

    return pd.DataFrame(allocation)
# Function to calculate metrics
def calculate_metrics_random(allocation_df, hotels_df):
    allocated_room_counts = allocation_df['hotel'].value_counts()
    hotels_fully_occupied = sum(
        allocated_room_counts.get(hotel, 0) == room_count
        for hotel, room_count in hotels_df.set_index('hotel')['rooms'].items()
    )

    results = {
        "Total Guests Allocated": len(allocation_df),
        "Total Rooms Filled": len(allocation_df),
        "Number of Hotels Utilized": allocation_df['hotel'].nunique(),
        "Full Capacity Hotels Count": hotels_fully_occupied,
        "Overall Revenue Earned": round(allocation_df['final_price'].sum(), 2),
        "Average Earnings Per Hotel": round(allocation_df.groupby('hotel')['final_price'].sum().mean(), 2),
        "Average Guest Satisfaction": round(allocation_df['guest_satisfaction'].mean(), 2)
    }

    return pd.DataFrame(list(results.items()), columns=['Metric', 'Value'])

def calculate_metrics_customer_preference(allocation_df, hotels_df):
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
def save_files(allocation_df, results_df, directory, strategy_name):
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        csv_path = os.path.join(directory, f'{strategy_name}_results.csv')
        txt_path = os.path.join(directory, f'summary_report_{strategy_name}.txt')

        allocation_df.to_csv(csv_path, index=False)
        with open(txt_path, 'w') as file:
            file.write(f"Summary Report of {strategy_name} Strategy\n")
            file.write("-------------------------------------------------\n")
            file.writelines([f"{row['Metric']}: {row['Value']}\n" for _, row in results_df.iterrows()])

        return csv_path, txt_path
    except Exception as e:
        print(f"Error saving files: {e}")
        return None, None


# Function to display with description
def display_with_description(description, dataframe, post_description=None):
    display(HTML(description))
    display(style_dataframe(dataframe))
    if post_description:
        display(HTML(post_description))
        
        
def display_download_links(csv_path, txt_path):
    if csv_path:
        display(FileLink(csv_path, result_html_prefix="Download CSV: "))
    if txt_path:
        display(FileLink(txt_path, result_html_prefix="Download Summary Report: "))


# Main execution block
def main():
    # Paths to the data files
    hotels_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/hotels.xlsx'
    guests_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/guests.xlsx'
    preferences_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/preferences.xlsx'

    # Load and clean datasets
    hotels_df, guests_df, preferences_df = load_datasets(hotels_path, guests_path, preferences_path)

    # Execute Random_allocation strategy
    random_allocation_df = random_allocation(guests_df, hotels_df, preferences_df)
    random_results_df = calculate_metrics_random(random_allocation_df, hotels_df)
    
    # Execute customer_preference_allocation strategy
    customer_preference_allocation_df = customer_preference_allocation(hotels_df, guests_df, preferences_df)
    customer_preference_results_df = calculate_metrics_customer_preference(customer_preference_allocation_df, hotels_df)
    # Display and save results for Random Allocation Strategy
    display(HTML("<h2>Random Allocation Strategy Results</h2>"))
    display_with_description("<b>Table 1: Random Allocation Results Summary</b>", random_allocation_df.head())
    display_with_description("<b>Table 2: Random Allocation Performance Metrics</b>", random_results_df)
    csv_path, txt_path = save_files(random_allocation_df, random_results_df, 'results', 'random_allocation')
    display_download_links(csv_path, txt_path)

    # Display and save results for Customer Preference Allocation Strategy
    display(HTML("<h2>Customer Preference Allocation Strategy Results</h2>"))
    display_with_description("<b>Table 3: Customer Preference Allocation Results Summary</b>", customer_preference_allocation_df.head())
    display_with_description("<b>Table 4: Customer Preference Allocation Performance Metrics</b>", customer_preference_results_df)
    csv_path, txt_path = save_files(customer_preference_allocation_df, customer_preference_results_df, 'results', 'customer_preference')
    display_download_links(csv_path, txt_path)


if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




