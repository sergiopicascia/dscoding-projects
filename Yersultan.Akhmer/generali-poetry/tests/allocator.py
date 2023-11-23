import numpy as np
import random
from hotel import Hotel
from guest import Guest
import pandas as pd
import os
class Allocator:
    def __init__(self, data_manager):
        self.hotels_df = data_manager.get_hotels()
        self.guests_df = data_manager.get_guests()
        self.preferences_df = data_manager.get_preferences()
        self.guest_allocation_info = []

    def load_data(self):
        self.hotels = [Hotel(row['hotel'], row['rooms'], row['price']) for index, row in self.hotels_df.iterrows()]
        self.guests = [Guest(row['guest'], row['discount']) for index, row in self.guests_df.iterrows()]

    def price_allocation(self):
        self.load_data()
        self.hotels.sort(key=lambda hotel: hotel.price)
        self.allocate_rooms()

    def customer_preference_allocation(self):
        self.load_data()
        guest_names = np.array([guest.name for guest in self.guests])
        sorted_indices = np.argsort(guest_names)
        self.guests = [self.guests[i] for i in sorted_indices]
        self.allocate_rooms(preferential=True)

    def random_allocation(self):
        self.load_data()
        random.shuffle(self.guests)
        self.allocate_rooms()


    def availability_allocation(self):
        self.load_data()
        self.hotels.sort(key=lambda hotel: hotel.rooms, reverse=True)
        self.allocate_rooms()

    def allocate_rooms(self, preferential=False):
        for guest in self.guests:
            allocated = False
            guest_preferences = self.preferences_df[self.preferences_df['guest'] == guest.name].sort_values(by='priority')['hotel'].tolist()

            if preferential:
                # Try to allocate based on preferences
                for hotel_name in guest_preferences:
                    allocated = self.try_allocate(guest, hotel_name)
                    if allocated:
                        break

            if not allocated:
                # If preferred hotels are full, allocate to any available hotel
                for hotel in self.hotels:
                    if hotel.allocate_customer(guest):
                        guest.allocated_hotel = hotel.name
                        self.guest_allocation_info.append((guest.name, hotel.name, hotel.price * (1 - guest.discount)))
                        allocated = True
                        break

            if not allocated:
                print(f"No available rooms for {guest.name}")
                self.guest_allocation_info.append((guest.name, None, 0))  # No hotel allocated and no earnings

            # Calculate and store satisfaction rate for each guest
            guest.satisfaction = 100 if guest.allocated_hotel in guest_preferences else 0


    def try_allocate(self, guest, hotel_name):
        for hotel in self.hotels:
            if hotel.name == hotel_name and hotel.allocate_customer(guest):
                guest.allocated_hotel = hotel.name
                self.guest_allocation_info.append((guest.name, hotel.name))
                return True
        return False

    def calculate_customer_satisfaction(self):
        # Using NumPy for efficient calculations
        satisfaction_counts = np.array([guest.allocated_hotel in self.preferences_df[self.preferences_df['guest'] == guest.name].sort_values(by='priority')['hotel'].tolist() for guest in self.guests])
        satisfaction_count = np.sum(satisfaction_counts)
        return np.divide(satisfaction_count, len(self.guests)) * 100

    def get_hotel_earnings(self):
        # Assuming each Hotel object has a method called calculate_total_earnings
        # that calculates the hotel's total earnings based on allocated guests.
        return {hotel.name: hotel.calculate_total_earnings() for hotel in self.hotels}
    
    def get_top_earning_hotels(self, top_n=10):
        earnings = self.get_hotel_earnings()
        # Sort the hotels by earnings and get the top ones
        top_earning_hotels = sorted(earnings.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return top_earning_hotels

    def display_report(self):
        total_customers = len(self.guests)
        total_rooms_occupied = sum(len(hotel.customers) for hotel in self.hotels)
        total_hotels_occupied = sum(1 for hotel in self.hotels if len(hotel.customers) > 0)
        total_earnings = sum(hotel.calculate_total_earnings() for hotel in self.hotels)
        
        # Assemble the report DataFrame with additional columns for satisfaction and earnings
        report_data = {
            "Guest": [guest.name for guest in self.guests],
            "Allocated Hotel": [guest.allocated_hotel for guest in self.guests],
            # Calculate the satisfaction rate for each guest
            "Satisfaction Rate (%)": [self.calculate_individual_satisfaction(guest) for guest in self.guests],
            # Calculate the earnings for each guest
            "Earned Money": [self.calculate_individual_earnings(guest) for guest in self.guests]
        }

        # Create a DataFrame for the report
        detailed_report_df = pd.DataFrame(report_data)

        # Calculate overall satisfaction and earnings
        total_satisfaction = np.mean([guest.satisfaction for guest in self.guests if guest.satisfaction is not None])
        total_earnings = sum([guest.earnings for guest in self.guests if guest.earnings is not None])

        # Create a summary DataFrame
        summary_data = {
            "Number of customers accommodated": len(self.guests),
            "Number of rooms occupied": sum(1 for guest in self.guests if guest.allocated_hotel),
            "Total volume of business": total_earnings,
            "Customer satisfaction rate": f"{total_satisfaction}%"
        }
        summary_df = pd.DataFrame([summary_data])

        hotel_earnings = self.get_hotel_earnings()

        return detailed_report_df, summary_df, hotel_earnings

    def save_allocation_info_to_excel(self, output_file):
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Create a DataFrame from the allocation information
        # Update the columns to match the data
        allocation_df = pd.DataFrame(self.guest_allocation_info, columns=["Guest", "Allocated Hotel", "Earned Money"])

        # Save the DataFrame to an Excel file
        allocation_df.to_excel(output_file, index=False)

        # Return the DataFrame
        return allocation_df
    
    def calculate_individual_satisfaction(self, guest):
        # Check if the allocated hotel is among the guest's preferences
        preferences = self.preferences_df[self.preferences_df['guest'] == guest.name]['hotel'].tolist()
        satisfaction = 100 if guest.allocated_hotel in preferences else 0
        # Store satisfaction rate in the guest object for later use
        guest.satisfaction = satisfaction
        return satisfaction

    def calculate_individual_earnings(self, guest):
        # Find the hotel object and calculate earnings
        hotel = next((hotel for hotel in self.hotels if hotel.name == guest.allocated_hotel), None)
        earnings = hotel.price * (1 - guest.discount) if hotel else 0
        # Store earnings in the guest object for later use
        guest.earnings = earnings
        return earnings
    
