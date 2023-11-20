import pandas as pd
import os
from IPython.display import display, FileLink
from ipywidgets import Button, Output, Layout
import random
import numpy as np


# Function to clean data
def clean_data(df):
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
        return hotels_df, guests_df, preferences_df
    except Exception as e:
        print(f"Error loading file: {e}")
        exit()


# Function for random allocation- MOST IMPORTANT PART WORK AS ENGINE
def random_allocation(hotels_df, guests_df):
    # Randomize the guest list
    random_guests = guests_df['guest'].sample(frac=1).tolist()

    # Initialize the result dictionary
    allocation_results = {
        'guest': [],
        'hotel': [],
        'price_paid': [],
        'guest_satisfaction': []  # Random guest satisfaction score
    }

    # Convert room availability to a dictionary for faster updates
    room_availability = hotels_df.set_index('hotel')['rooms'].to_dict()

    # Pre-compute discounts and room prices for efficiency
    guest_discounts = guests_df.set_index('guest')['discount'].to_dict()
    hotel_prices = hotels_df.set_index('hotel')['price'].to_dict()

    # Iterate over the list of guests
    for guest in random_guests:
        discount = guest_discounts[guest]

        # Randomly shuffle hotel list for each guest
        shuffled_hotels = hotels_df['hotel'].sample(frac=1).tolist()

        for hotel in shuffled_hotels:
            if room_availability.get(hotel, 0) > 0:
                room_availability[hotel] -= 1
                room_price = hotel_prices[hotel]
                price_paid = room_price * (1 - discount)
                guest_satisfaction = np.random.randint(1, 6)  # Random satisfaction score between 1 and 5

                allocation_results['guest'].append(guest)
                allocation_results['hotel'].append(hotel)
                allocation_results['price_paid'].append(price_paid)
                allocation_results['guest_satisfaction'].append(guest_satisfaction)
                break
        else:
            allocation_results['guest'].append(guest)
            allocation_results['hotel'].append(None)
            allocation_results['price_paid'].append(0)
            allocation_results['guest_satisfaction'].append(None)

    # Convert the results to a DataFrame
    allocation_df = pd.DataFrame(allocation_results)
    return allocation_df


# Function to calculate metrics
def calculate_metrics(allocation_df, hotels_df):
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
        "Overall Revenue Earned": allocation_df['price_paid'].sum(),
        "Average Earnings Per Hotel": allocation_df.groupby('hotel')['price_paid'].sum().mean(),
        "Average Guest Satisfaction": round(allocation_df['guest_satisfaction'].mean(),
                                            2) if 'guest_satisfaction' in allocation_df.columns else None

    }

    return pd.DataFrame(list(results.items()), columns=['Metric', 'Value'])


# UNTIL DEF MAIN I ATTEMPTED  TO ILLUSTRATE BETTER

# Function to style DataFrames
def style_dataframe(df):
    return df.style \
        .background_gradient(cmap='Blues') \
        .set_properties(**{'text-align': 'left', 'font-size': '12pt'}) \
        .format({'price_paid': "${:,.2f}"}) \
        .set_table_styles([{'selector': 'th', 'props': [('font-size', '12pt'), ('text-align', 'center')]}])


# Function to save results
def save_files(allocation_df, results_df, directory='results'):
    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        csv_path = os.path.join(directory, 'random_allocation_results.csv')
        txt_path = os.path.join(directory, 'summary_report.txt')

        allocation_df.to_csv(csv_path, index=False)
        with open(txt_path, 'w') as file:
            file.write("Summary Report of Random Allocation Strategy\n")
            file.write("-------------------------------------------------\n")
            file.writelines([f"{row['Metric']}: {row['Value']}\n" for _, row in results_df.iterrows()])

        return csv_path, txt_path
    except Exception as e:
        print(f"Error saving files: {e}")
        return None, None


from IPython.display import HTML


def display_with_description(description, dataframe):
    display(HTML(description))
    display(style_dataframe(dataframe))


# Main execution block
# Main execution block
def main():
    hotels_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/hotels.xlsx'
    guests_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/guests.xlsx'
    preferences_path = 'C:/Users/irpay/OneDrive/Documents/GitHub/payam/preferences.xlsx'

    hotels_df, guests_df, preferences_df = load_datasets(hotels_path, guests_path, preferences_path)

    random_allocation_df = random_allocation(hotels_df, guests_df)
    results_df = calculate_metrics(random_allocation_df, hotels_df)

    # Display tables with descriptions
    allocation_description = "<b>Table 1: Allocation Results Summary</b><br>This table shows the distribution of guests across various hotels, the price paid, and their satisfaction scores."
    metrics_description = "<b>Table 2: Performance Metrics Overview</b><br>This table provides key metrics summarizing the allocation's effectiveness, including total guests allocated, revenue earned, and average guest satisfaction."
    display_with_description(allocation_description, random_allocation_df.head())
    display_with_description(metrics_description, results_df)

    # Save files and display download links
    csv_path, txt_path = save_files(random_allocation_df, results_df)
    if csv_path and txt_path:
        display(FileLink(csv_path, result_html_prefix="Download CSV: "))
        display(FileLink(txt_path, result_html_prefix="Download Summary Report: "))

# Run the script
if __name__ == "__main__":
    main()
