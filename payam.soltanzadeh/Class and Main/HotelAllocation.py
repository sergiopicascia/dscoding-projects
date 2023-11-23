#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, HTML, FileLink


class HotelAllocation:
    def __init__(self, hotels_path, guests_path, preferences_path):
        self.hotels_path = hotels_path
        self.guests_path = guests_path
        self.preferences_path = preferences_path
        self.hotels_df, self.guests_df, self.preferences_df = self.load_datasets()

    def clean_data(self, df, dataset_type):
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

    def load_datasets(self):
        try:
            hotels_df = pd.read_excel(self.hotels_path)
            guests_df = pd.read_excel(self.guests_path)
            preferences_df = pd.read_excel(self.preferences_path)

            hotels_df = self.clean_data(hotels_df, 'hotels')
            guests_df = self.clean_data(guests_df, 'guests')
            preferences_df = self.clean_data(preferences_df, 'preferences')
        except Exception as e:
            print(f"Error loading datasets: {e}")
            hotels_df, guests_df, preferences_df = None, None, None

        return hotels_df, guests_df, preferences_df

    def random_allocation(self):
        allocation = {'guest': [], 'hotel': [], 'final_price': [], 'guest_satisfaction': []}
        random_guest = np.random.choice(self.guests_df['guest'], size=len(self.guests_df), replace=False).tolist()
        hotel_list = pd.Series(self.hotels_df['rooms'].values, index=self.hotels_df['hotel'])
        random_hotel = hotel_list.sample(frac=1).to_dict()

        allocated_guests = set()  # Set to keep track of already allocated guests

        for guest in random_guest:
            if guest in allocated_guests:  # Skip if guest is already allocated
                continue

            guest_discount = self.guests_df[self.guests_df['guest'] == guest]['discount'].values[0]
            priority_hotels = self.preferences_df[self.preferences_df['guest'] == guest].sort_values(by='priority')[
                'hotel'].tolist()

            for hotel in random_hotel:
                if hotel in priority_hotels and random_hotel[hotel] > 0:
                    random_hotel[hotel] -= 1
                    gross_earning = self.hotels_df[self.hotels_df['hotel'] == hotel]['price'].values[0]
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

    def customer_preference_allocation(self):
        # Data Integrity Checks
        if self.guests_df['guest'].isnull().any():
            raise ValueError("Missing guest data in guests_df")
        if self.hotels_df['hotel'].isnull().any():
            raise ValueError("Missing hotel data in hotels_df")
        if self.preferences_df.isnull().any().any():
            raise ValueError("Missing data in preferences_df")

        # Ensure all guests have preferences
        guests_with_preferences = self.preferences_df['guest'].unique()
        if not all(guest in guests_with_preferences for guest in self.guests_df['guest']):
            raise ValueError("Not all guests have hotel preferences")

        # Ensure all preferred hotels exist in the hotels list
        hotels_in_preferences = set(self.preferences_df['hotel'])
        if not hotels_in_preferences.issubset(set(self.hotels_df['hotel'])):
            raise ValueError("Some hotels in preferences are not in the hotels list")

        guests_list = self.guests_df['guest'].tolist()
        allocation_results = {
            'guest': [],
            'hotel': [],
            'final_price': [],
            'guest_satisfaction': []
        }

        room_availability = self.hotels_df.set_index('hotel')['rooms'].to_dict()
        guest_discounts = self.guests_df.set_index('guest')['discount'].to_dict()
        hotel_prices = self.hotels_df.set_index('hotel')['price'].to_dict()

        for guest in guests_list:
            discount = guest_discounts[guest]
            preferred_hotels = self.preferences_df[self.preferences_df['guest'] == guest].sort_values(by='priority')[
                'hotel'].tolist()

            for hotel in preferred_hotels:
                if room_availability.get(hotel, 0) > 0:
                    room_availability[hotel] -= 1
                    room_price = hotel_prices[hotel]
                    final_price = room_price * (1 - discount)
                    guest_satisfaction = int(preferred_hotels.index(hotel) + 1)

                    allocation_results['guest'].append(guest)
                    allocation_results['hotel'].append(hotel)
                    allocation_results['final_price'].append(final_price)
                    allocation_results['guest_satisfaction'].append(guest_satisfaction)
                    break
            else:
                allocation_results['guest'].append(guest)
                allocation_results['hotel'].append(None)
                allocation_results['final_price'].append(0)
                allocation_results['guest_satisfaction'].append(None)

        allocation_df = pd.DataFrame(allocation_results)
        allocation_df['guest_satisfaction'] = allocation_df['guest_satisfaction'].fillna(0).astype(int)
        return allocation_df

    def price_allocation(self):
        allocation = {'guest': [], 'hotel': [], 'final_price': [], 'guest_satisfaction': []}

        guest_list = self.guests_df['guest'].tolist()
        hotel_ordered = self.hotels_df.sort_values(by='price')
        hotel_list = pd.Series(hotel_ordered['rooms'].values, index=hotel_ordered.hotel).to_dict()

        for guest in guest_list:
            guest_discount = self.guests_df[self.guests_df['guest'] == guest]['discount'].values[0]
            priority_hotels = self.preferences_df[self.preferences_df['guest'] == guest].sort_values(by='priority')[
                'hotel'].tolist()

            for hotel in hotel_list:
                if hotel in priority_hotels and hotel_list[hotel] > 0:
                    hotel_list[hotel] -= 1
                    gross_earning = self.hotels_df[self.hotels_df['hotel'] == hotel]['price'].values[0]
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

        return pd.DataFrame(allocation)

    def availability_allocation(self):
        allocation = {'guest': [], 'hotel': [], 'final_price': [], 'guest_satisfaction': []}

        guest_list = self.guests_df['guest'].tolist()
        hotel_ordered = self.hotels_df.sort_values(by='rooms')
        hotel_list = pd.Series(hotel_ordered['rooms'].values, index=hotel_ordered.hotel).to_dict()

        for guest in guest_list:
            guest_discount = self.guests_df[self.guests_df['guest'] == guest]['discount'].values[0]
            priority_hotels = self.preferences_df[self.preferences_df['guest'] == guest].sort_values(by='priority')[
                'hotel'].tolist()

            for hotel in hotel_list:
                if hotel in priority_hotels and hotel_list[hotel] > 0:
                    hotel_list[hotel] -= 1
                    gross_earning = self.hotels_df[self.hotels_df['hotel'] == hotel]['price'].values[0]
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

        return pd.DataFrame(allocation)

    def calculate_metrics(self, allocation_df):
        if 'guest_satisfaction' not in allocation_df.columns:
            allocation_df['guest_satisfaction'] = np.nan

        allocated_room_counts = allocation_df['hotel'].value_counts()
        hotels_fully_occupied = sum(
            allocated_room_counts.get(hotel, 0) == room_count
            for hotel, room_count in self.hotels_df.set_index('hotel')['rooms'].items()
        )

        total_guests_allocated = allocation_df[allocation_df['hotel'].notnull()].shape[0]
        total_rooms_filled = allocated_room_counts.sum()

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

    def extract_metrics(self, df):
        return {
            'Total Guests Allocated': df.loc[df['Metric'] == 'Total Guests Allocated', 'Value'].values[0],
            'Total Rooms Filled': df.loc[df['Metric'] == 'Total Rooms Filled', 'Value'].values[0],
            'Number of Hotels Utilized': df.loc[df['Metric'] == 'Number of Hotels Utilized', 'Value'].values[0],
            'Full Capacity Hotels Count': df.loc[df['Metric'] == 'Full Capacity Hotels Count', 'Value'].values[0],
            'Overall Revenue Earned': df.loc[df['Metric'] == 'Overall Revenue Earned', 'Value'].values[0],
            'Average Earnings Per Hotel': df.loc[df['Metric'] == 'Average Earnings Per Hotel', 'Value'].values[0],
            'Average Guest Satisfaction': df.loc[df['Metric'] == 'Average Guest Satisfaction', 'Value'].values[0]
        }

    def style_dataframe(self, df):
        if 'final_price' in df.columns:
            return df.style \
                .background_gradient(cmap='Blues') \
                .set_properties(**{'text-align': 'left', 'font-size': '12pt'}) \
                .format({'final_price': "€{:,.2f}"}) \
                .set_table_styles([{'selector': 'th', 'props': [('font-size', '12pt'), ('text-align', 'center')]}])
        else:
            def custom_format(x, metric):
                if metric in ["Overall Revenue Earned", "Average Earnings Per Hotel"]:
                    return f"€{x:,.4f}"
                elif metric is "Average Guest Satisfaction":
                    return f"{x:.2f}"
                return f"{x:,.0f}"

            return df.style \
                .background_gradient(cmap='Blues') \
                .set_properties(**{'text-align': 'left', 'font-size': '12pt'}) \
                .format({'Value': lambda x: custom_format(x, df[df['Value'] == x]['Metric'].iloc[0])}) \
                .set_table_styles([{'selector': 'th', 'props': [('font-size', '12pt'), ('text-align', 'center')]}])
            
                formatted_df = styled_df.format("{:.2f}")
    return formatted_df

    def save_files(self, allocation_df, results_df, directory, strategy_name):
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

    def display_with_description(self, description, dataframe, post_description=None):
        display(HTML(description))
        display(self.style_dataframe(dataframe))
        if post_description:
            display(HTML(post_description))

    def display_download_links(self, csv_path, txt_path):
        if csv_path:
            display(FileLink(csv_path, result_html_prefix="Download CSV: "))
        if txt_path:
            display(FileLink(txt_path, result_html_prefix="Download Summary Report: "))

    def plot_Satisfaction(self, comparison_df):
        strategies = comparison_df['Strategy']
        total_guests = comparison_df['Total Guests Allocated']
        total_rooms = comparison_df['Total Rooms Filled']
        avg_satisfaction = comparison_df['Average Guest Satisfaction']

        x = np.arange(len(strategies))  # Label locations

        fig, ax = plt.subplots()
        ax.bar(strategies, total_guests, label='Total Guests Allocated')
        ax.bar(strategies, total_rooms, bottom=total_guests, label='Total Rooms Filled')
        ax.plot(strategies, avg_satisfaction * max(total_guests) / 5, color='red', marker='o',
                label='Average Guest Satisfaction (scaled)')

        ax.set_xlabel('Strategy')
        ax.set_title('Average Satisfaction of Guests For each Strategy')
        ax.legend()

        plt.show()

    def plot_revenue_chart(self, comparison_df):
        strategies = comparison_df['Strategy']
        overall_revenue = comparison_df['Overall Revenue Earned']
        avg_earnings = comparison_df['Average Earnings Per Hotel']

        fig, ax1 = plt.subplots()

        # Plotting the bar chart for overall revenue
        ax1.bar(strategies, overall_revenue, color='blue', alpha=0.6, label='Overall Revenue Earned')

        # Adding labels and title
        ax1.set_xlabel('Strategy')
        ax1.set_ylabel('Overall Revenue Earned')
        ax1.set_title('Strategy Comparison: Revenue and Earnings')
        ax1.legend(loc='upper left')

        # Plotting the line chart for average earnings
        ax2 = ax1.twinx()
        ax2.plot(strategies, avg_earnings, color='green', marker='o', label='Average Earnings Per Hotel')
        ax2.set_ylabel('Average Earnings Per Hotel (€)')
        ax2.legend(loc='upper right')

        plt.show()

    def shorten_strategy_names(self, comparison_df):
        # Shorten or modify strategy names as desired
        comparison_df['Strategy'] = comparison_df['Strategy'].replace({
            'Random Allocation': 'Random',
            'Customer Preference Allocation': 'Customer Preference',
            'Price Allocation': 'Price',
            'Availability Allocation': 'Availability'
        })
        return comparison_df


