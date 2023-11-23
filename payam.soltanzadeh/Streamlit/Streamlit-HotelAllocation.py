import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from io import BytesIO
import base64


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



# Random Allocation function
def random_allocation( hotels_df,guests_df, preferences_df):
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


# Price Allocation function
def price_allocation(hotels_df, guests_df, preferences_df):
    allocation = { 'hotel': [],'guest': [], 'final_price': [], 'guest_satisfaction': []}

    guest_list = guests_df['guest'].tolist()

    hotel_ordered = hotels_df.sort_values(by='price')
    hotel_list = pd.Series(hotel_ordered['rooms'].values, index=hotel_ordered.hotel).to_dict()

    for guest in guest_list:

        guest_discount = guests_df[guests_df['guest'] == guest]['discount'].values[0]

        priority_hotels = preferences_df[preferences_df['guest'] == guest].sort_values(by='priority')['hotel'].tolist()

        for hotel in hotel_list:
            if hotel in priority_hotels and hotel_list[hotel] > 0:
                hotel_list[hotel] -= 1

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
                break

    price_allocation = pd.DataFrame(allocation)
    return price_allocation


def availability_allocation(hotels_df, guests_df, preferences_df):
    allocation = { 'hotel': [] ,'guest': [], 'final_price': [], 'guest_satisfaction': []}

    guest_list = guests_df['guest'].tolist()

    hotel_ordered = hotels_df.sort_values(by='rooms')
    hotel_list = pd.Series(hotel_ordered['rooms'].values, index=hotel_ordered.hotel).to_dict()

    for guest in guest_list:

        guest_discount = guests_df[guests_df['guest'] == guest]['discount'].values[0]

        priority_hotels = preferences_df[preferences_df['guest'] == guest].sort_values(by='priority')['hotel'].tolist()

        for hotel in hotel_list:
            if hotel in priority_hotels and hotel_list[hotel] > 0:
                hotel_list[hotel] -= 1

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
                break

    allocation_df = pd.DataFrame(allocation)
    return allocation_df


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
        "Average Guest Satisfaction": round(allocation_df['guest_satisfaction'].mean(), 2) if not allocation_df[
            'guest_satisfaction'].isna().all() else np.nan
    }

    return pd.DataFrame(list(results.items()), columns=['Metric', 'Value'])


def extract_metrics(df):
    return {
        'Total Guests Allocated': df.loc[df['Metric'] == 'Total Guests Allocated', 'Value'].values[0],
        'Total Rooms Filled': df.loc[df['Metric'] == 'Total Rooms Filled', 'Value'].values[0],
        'Number of Hotels Utilized': df.loc[df['Metric'] == 'Number of Hotels Utilized', 'Value'].values[0],
        'Full Capacity Hotels Count': df.loc[df['Metric'] == 'Full Capacity Hotels Count', 'Value'].values[0],
        'Overall Revenue Earned': df.loc[df['Metric'] == 'Overall Revenue Earned', 'Value'].values[0],
        'Average Earnings Per Hotel': df.loc[df['Metric'] == 'Average Earnings Per Hotel', 'Value'].values[0],
        'Average Guest Satisfaction': df.loc[df['Metric'] == 'Average Guest Satisfaction', 'Value'].values[0]
    }

# Function to calculate metrics

def execute_strategy(strategy,hotels_df,guests_df, preferences_df):
    if strategy == 'Random Allocation':
        return random_allocation( hotels_df,guests_df, preferences_df)
    elif strategy == 'Customer Preference Allocation':
        return customer_preference_allocation(hotels_df, guests_df, preferences_df)
    elif strategy == 'Price Allocation':
        return price_allocation(hotels_df, guests_df, preferences_df)
    elif strategy == 'Availability Allocation':
        return availability_allocation(hotels_df, guests_df, preferences_df)

# Convert DataFrame to CSV for download
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')
# Function to plot guest satisfaction

# Function to create a summary string from a DataFrame
def create_summary_string(summary_df):
    summary_string = ""
    for index, row in summary_df.iterrows():
        summary_string += f"{row['Metric']}: {row['Value']}\n"
    return summary_string

# Function for download buttons
def download_buttons(data_df, summary_df, data_filename='data.csv', summary_filename='summary.txt'):
    # Convert data to CSV
    csv = data_df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name=data_filename,
        mime='text/csv',
    )

    # Create summary string
    summary_string = create_summary_string(summary_df)

    # Download button for the summary text
    st.download_button(
        label="Download Summary as TXT",
        data=summary_string,
        file_name=summary_filename,
        mime='text/plain',
    )




def plot_Satisfaction(streamlit, comparison_df):
    strategies = comparison_df['Strategy']
    total_guests = comparison_df['Total Guests Allocated']
    total_rooms = comparison_df['Total Rooms Filled']
    avg_satisfaction = comparison_df['Average Guest Satisfaction']

    fig, ax = plt.subplots()
    ax.bar(strategies, total_guests, label='Total Guests Allocated')
    ax.bar(strategies, total_rooms, bottom=total_guests, label='Total Rooms Filled')
    ax.plot(strategies, avg_satisfaction * max(total_guests) / 5, color='red', marker='o', label='Average Guest Satisfaction (scaled)')

    ax.set_xlabel('Strategy')
    ax.set_title('Average Satisfaction of Guests For each Strategy')
    ax.legend()
    streamlit.pyplot(fig)

# Function to plot revenue chart
def plot_revenue_chart(streamlit, comparison_df):
    strategies = comparison_df['Strategy']
    overall_revenue = comparison_df['Overall Revenue Earned']
    avg_earnings = comparison_df['Average Earnings Per Hotel']

    fig, ax1 = plt.subplots()
    ax1.bar(strategies, overall_revenue, color='blue', alpha=0.6, label='Overall Revenue Earned')
    ax1.set_xlabel('Strategy')
    ax1.set_ylabel('Overall Revenue Earned')
    ax1.set_title('Strategy Comparison: Revenue and Earnings')
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(strategies, avg_earnings, color='green', marker='o', label='Average Earnings Per Hotel')
    ax2.set_ylabel('Average Earnings Per Hotel (€)')
    ax2.legend(loc='upper right')
    streamlit.pyplot(fig)

def execute_all_strategies(hotels_df, guests_df, preferences_df):
    strategies = {
        'Random Allocation': random_allocation,
        'Customer Preference Allocation': customer_preference_allocation,
        'Price Allocation': price_allocation,
        'Availability Allocation': availability_allocation
    }

    comparison_data = []
    strategy_results = {}

    for strat_name, strat_func in strategies.items():
        allocation_df = strat_func(hotels_df, guests_df, preferences_df)
        results_df = calculate_metrics(allocation_df, hotels_df)
        metrics = extract_metrics(results_df)

        comparison_data.append({'Strategy': strat_name, **metrics})
        strategy_results[strat_name] = (allocation_df, results_df)

    comparison_df = pd.DataFrame(comparison_data)
    return comparison_df, strategy_results

# Streamlit Main Function
def main():
    st.title('Hotel Allocation System')

    # Sidebar for File Upload and Strategy Selection
    with st.sidebar:
        uploaded_hotels = st.file_uploader("Upload Hotels Data", type=['xlsx'])
        uploaded_guests = st.file_uploader("Upload Guests Data", type=['xlsx'])
        uploaded_preferences = st.file_uploader("Upload Preferences Data", type=['xlsx'])
        strategy = st.selectbox(
            'Select an Allocation Strategy',
            ['Execute All', 'Random Allocation', 'Customer Preference Allocation', 'Price Allocation', 'Availability Allocation']
        )
        execute_button = st.button('Execute Strategy')

    # Main Area for Displaying Results
    if uploaded_hotels and uploaded_guests and uploaded_preferences and execute_button:
        try:
            # Load and Clean Data
            hotels_df = pd.read_excel(uploaded_hotels)
            guests_df = pd.read_excel(uploaded_guests)
            preferences_df = pd.read_excel(uploaded_preferences)

            hotels_df = clean_data(hotels_df, 'hotels')
            guests_df = clean_data(guests_df, 'guests')
            preferences_df = clean_data(preferences_df, 'preferences')

            # Execute Selected Strategy or All
            if strategy == 'Execute All':
                comparison_df, strategy_results = execute_all_strategies(hotels_df, guests_df, preferences_df)

                # Displaying Results for Each Strategy
                for strat_name, (allocation_df, results_df) in strategy_results.items():
                    st.subheader(f"{strat_name} Results")
                    st.write(allocation_df.head(10))
                    st.write(results_df)
                    # Call the function to create download buttons
                    download_buttons(allocation_df, results_df)

                # Visualizations
                plot_Satisfaction(st, comparison_df)
                plot_revenue_chart(st, comparison_df)

            else:
                allocation_df = execute_strategy(strategy, hotels_df, guests_df, preferences_df)
                results_df = calculate_metrics(allocation_df, hotels_df)

                # Display Strategy Results
                st.subheader(f"{strategy} Results")
                st.write(allocation_df.head(10))
                st.write(results_df)


            # Download Button for allocation_df
            if allocation_df is not None:
                csv = convert_df_to_csv(allocation_df)
                st.download_button(
                    label="Download data as CSV",
                    data=csv,
                    file_name='allocation_data.csv',
                    mime='text/csv',
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
