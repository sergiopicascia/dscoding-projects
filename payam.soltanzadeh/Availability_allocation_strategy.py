#!/usr/bin/env python
# coding: utf-8

# In[11]:


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



def availability_allocation(hotels_df, guests_df, preferences_df):
    
    allocation = {'guest': [], 'hotel': [], 'final_price': [], 'guest_satisfaction': []}
    
    guest_list = guests_df['guest'].tolist()

    hotel_ordered = hotels_df.sort_values(by='rooms') 
    hotel_list = pd.Series(hotel_ordered['rooms'].values, index = hotel_ordered.hotel).to_dict()
        
    for guest in guest_list:
            
        guest_discount = guests_df[guests_df['guest'] == guest]['discount'].values[0]

        priority_hotels = preferences_df[preferences_df['guest'] == guest].sort_values(by='priority')['hotel'].tolist()
        
        for hotel in hotel_list:
            if hotel in priority_hotels and hotel_list[hotel]>0:
                hotel_list[hotel] -=1
    
                gross_earning = hotels_df[hotels_df['hotel'] == hotel]['price'].values[0]
                net_earning = gross_earning*(1-guest_discount)
        
                satisfaction = 1 if priority_hotels.index(hotel)+1 == 1 else(
                    2 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.25) else(
                    3 if priority_hotels.index(hotel)+1 <= (len(priority_hotels) * 0.5) else(
                    4 if priority_hotels.index(hotel)+1 < (len(priority_hotels) * 0.75) else 5)))
        
                allocation['guest'].append(guest)
                allocation['hotel'].append(hotel)
                allocation['final_price'].append(net_earning)
                allocation['guest_satisfaction'].append(satisfaction)
                break

    allocation_df = pd.DataFrame(allocation)
    return allocation_df

# Apply the availability allocation strategy


# Function to calculate metrics
def calculate_metrics(allocation_df, hotels_df):
    # Ensure 'guest_satisfaction' column exists and handle if not
    if 'guest_satisfaction' not in allocation_df.columns:
        allocation_df['guest_satisfaction'] = np.nan  # Fill with NaN if column doesn't exist

    allocated_room_counts = allocation_df['hotel'].value_counts()
    hotels_fully_occupied = sum(
        allocated_room_counts.get(hotel, 0) == room_count
        for hotel, room_count in hotels_df.set_index('hotel')['rooms'].items()
    )

    # For 'Total Guests Allocated', count only non-null allocations if 'hotel' column can be null
    total_guests_allocated = allocation_df[allocation_df['hotel'].notnull()].shape[0]

    # For 'Total Rooms Filled', sum the filled rooms, considering only non-null hotel allocations
    total_rooms_filled = allocated_room_counts.sum()

    # Calculating metrics with rounding applied uniformly for consistency
    results = {
        "Total Guests Allocated": total_guests_allocated,
        "Total Rooms Filled": total_rooms_filled,
        "Number of Hotels Utilized": allocation_df['hotel'].nunique(),
        "Full Capacity Hotels Count": hotels_fully_occupied,
        "Overall Revenue Earned": round(allocation_df['final_price'].sum(), 2),
        "Average Earnings Per Hotel": round(allocation_df.groupby('hotel')['final_price'].sum().mean(), 2),
        "Average Guest Satisfaction": round(allocation_df['guest_satisfaction'].mean(), 2) if not allocation_df['guest_satisfaction'].isna().all() else np.nan
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
        csv_path = os.path.join(directory, 'availability_allocation.csv')
        txt_path = os.path.join(directory, 'availability_allocation_summeryreport.txt')

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
    availability_allocation_df = availability_allocation(hotels_df, guests_df, preferences_df)


    # Calculate metrics
    results_df = calculate_metrics(availability_allocation_df, hotels_df)

    # Display tables with descriptions
    allocation_description = "<b>Table 1: Allocation Results Summary</b><br>This table shows the distribution of guests across various hotels, the price paid, and their satisfaction scores."
    allocation_post_description = "*Note: Only the first 5 rows are displayed for brevity. For the complete data, please use the download link below.*"
    display_with_description(allocation_description, availability_allocation_df.head(), allocation_post_description)
    metrics_description = "<b>Table 2: Performance Metrics Overview</b><br>This table provides key metrics summarizing the allocation's effectiveness, including total guests allocated, revenue earned, and average guest satisfaction."
    metrics_post_description = "*Note: Guest satisfaction scores range from 1 to 5, with 1 being the guest's top choice and 5 being around their last preference.*"
    display_with_description(metrics_description, results_df, metrics_post_description)

    # Save files and display download links
    csv_path, txt_path = save_files(availability_allocation_df, results_df)
    if csv_path and txt_path:
        display(FileLink(csv_path, result_html_prefix="Download CSV: "))
        display(FileLink(txt_path, result_html_prefix="Download Summary Report: "))

# Run the script
if __name__ == "__main__":
    main()


# In[ ]:




