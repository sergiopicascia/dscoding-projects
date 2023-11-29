import pandas as pd
import numpy as np
from prettytable import PrettyTable
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt

class Guest:
    def __init__(self, guest_id, discount):
        self.guest_id = guest_id
        self.discount = discount

class Hotel:
    def __init__(self, hotel_id, rooms, price):
        self.hotel_id = hotel_id
        self.rooms = rooms
        self.price = price

class AllocationMethods:
    @staticmethod
    def random_allocation(guests, hotels):
        guests_df = pd.DataFrame([(guest.guest_id, guest.discount) for guest in guests], columns=['guest', 'discount'])
        hotels_df = pd.DataFrame([(hotel.hotel_id, hotel.rooms, hotel.price) for hotel in hotels], columns=['hotel', 'rooms', 'price'])

        guests_df = guests_df.sample(frac=1, random_state=42).reset_index(drop=True)
        hotels_df = hotels_df.sample(frac=1, random_state=42).reset_index(drop=True)

        allocation_result = []
        total_revenue = 0

        for _, row in guests_df.iterrows():
            guest_id = row['guest']
            guest_discount = row['discount']

            available_hotels = hotels_df[hotels_df['rooms'] > 0]

            if not available_hotels.empty:
                selected_hotel = available_hotels.sample(1, random_state=42)
                hotel_id = selected_hotel['hotel'].values[0]
                room_price = selected_hotel['price'].values[0]

                discounted_price = room_price * (1 - guest_discount / 100)
                total_revenue += discounted_price

                allocation_result.append((guest_id, hotel_id))
                hotels_df.loc[hotels_df['hotel'] == hotel_id, 'rooms'] -= 1

        return allocation_result, total_revenue

    @staticmethod
    def price_allocation(guests, hotels):
        guests_df = pd.DataFrame([(guest.guest_id, guest.discount) for guest in guests], columns=['guest', 'discount'])
        hotels_df = pd.DataFrame([(hotel.hotel_id, hotel.rooms, hotel.price) for hotel in hotels], columns=['hotel', 'rooms', 'price'])

        hotels_df = hotels_df.sort_values(by='price', ascending=False)

        allocation_result = []
        total_revenue = 0

        for _, row in guests_df.iterrows():
            guest_id = row['guest']
            guest_discount = row['discount']

            available_hotels = hotels_df[hotels_df['rooms'] > 0]

            if not available_hotels.empty:
                selected_hotel = available_hotels.head(1)
                hotel_id = selected_hotel['hotel'].values[0]
                room_price = selected_hotel['price'].values[0]

                discounted_price = room_price * (1 - guest_discount / 100)
                total_revenue += discounted_price

                allocation_result.append((guest_id, hotel_id))
                hotels_df.loc[hotels_df['hotel'] == hotel_id, 'rooms'] -= 1

        return allocation_result, total_revenue

    @staticmethod
    def availability_allocation(guests, hotels):
        guests_df = pd.DataFrame([(guest.guest_id, guest.discount) for guest in guests], columns=['guest', 'discount'])
        hotels_df = pd.DataFrame([(hotel.hotel_id, hotel.rooms, hotel.price) for hotel in hotels], columns=['hotel', 'rooms', 'price'])

        allocation_result = []
        total_revenue = 0

        for _, row in guests_df.iterrows():
            guest_id = row['guest']
            guest_discount = row['discount']

            available_hotels = hotels_df[hotels_df['rooms'] > 0]

            if not available_hotels.empty:
                selected_hotel = available_hotels.head(1)
                hotel_id = selected_hotel['hotel'].values[0]
                room_price = selected_hotel['price'].values[0]

                discounted_price = room_price * (1 - guest_discount / 100)
                total_revenue += discounted_price

                allocation_result.append((guest_id, hotel_id))
                hotels_df.loc[hotels_df['hotel'] == hotel_id, 'rooms'] -= 1

        return allocation_result, total_revenue

    @staticmethod
    def priority_allocation(guests, hotels, preferences):
        guests_df = pd.DataFrame([(guest.guest_id, guest.discount) for guest in guests], columns=['guest', 'discount'])
        hotels_df = pd.DataFrame([(hotel.hotel_id, hotel.rooms, hotel.price) for hotel in hotels], columns=['hotel', 'rooms', 'price'])
        preferences_df = pd.DataFrame(preferences, columns=['guest', 'hotel', 'priority'])

        allocation_result = []
        total_revenue = 0

        guests_with_preferences = guests_df[guests_df['guest'].isin(preferences_df['guest'])]

        for _, row in guests_with_preferences.iterrows():
            guest_id = row['guest']
            guest_discount = row['discount']

            guest_preferences = preferences_df[preferences_df['guest'] == guest_id]
            guest_preferences = guest_preferences.sort_values(by='priority')

            for _, preference_row in guest_preferences.iterrows():
                hotel_id = preference_row['hotel']
                available_hotels = hotels_df[(hotels_df['hotel'] == hotel_id) & (hotels_df['rooms'] > 0)]

                if not available_hotels.empty:
                    room_price = available_hotels['price'].values[0]
                    discounted_price = room_price * (1 - guest_discount / 100)
                    total_revenue += discounted_price

                    allocation_result.append((guest_id, hotel_id))
                    hotels_df.loc[hotels_df['hotel'] == hotel_id, 'rooms'] -= 1
                    break
            else:
                available_hotels = hotels_df[hotels_df['rooms'] > 0]
                if not available_hotels.empty:
                    selected_hotel = available_hotels.sample(1, random_state=42)
                    hotel_id = selected_hotel['hotel'].values[0]
                    room_price = selected_hotel['price'].values[0]

                    discounted_price = room_price * (1 - guest_discount / 100)
                    total_revenue += discounted_price

                    allocation_result.append((guest_id, hotel_id))
                    hotels_df.loc[hotels_df['hotel'] == hotel_id, 'rooms'] -= 1

        guests_without_preferences = guests_df[~guests_df['guest'].isin(preferences_df['guest'])]

        for _, row in guests_without_preferences.iterrows():
            guest_id = row['guest']
            guest_discount = row['discount']

            available_hotels = hotels_df[hotels_df['rooms'] > 0]
            if not available_hotels.empty:
                selected_hotel = available_hotels.sample(1, random_state=42)
                hotel_id = selected_hotel['hotel'].values[0]
                room_price = selected_hotel['price'].values[0]

                discounted_price = room_price * (1 - guest_discount / 100)
                total_revenue += discounted_price

                allocation_result.append((guest_id, hotel_id))
                hotels_df.loc[hotels_df['hotel'] == hotel_id, 'rooms'] -= 1

        return allocation_result, total_revenue

    @staticmethod
    def satisfaction(allocation_result, preferences):
        satisfaction_scores = []

        for guest_id, hotel_id in allocation_result:
            guest_preferences = preferences[(preferences['guest'] == str(guest_id)) & (preferences['hotel'] == str(hotel_id))]

            if guest_preferences.empty:
                satisfaction_scores.append(1)
            else:
                priority = guest_preferences['priority'].values[0]

                if priority == 1:
                    satisfaction_scores.append(1)
                elif priority <= 10:
                    satisfaction_scores.append(1 - 0.1 * (priority - 1))
                else:
                    satisfaction_scores.append(0)

        return np.mean(satisfaction_scores)

def import_data():
    guests_data = pd.read_excel(r'C:\Users\ayata\Documents\GitHub\dscoding-projects\Ayat.Ahmad\hotel.project\hotel\project\hotels\guests.xlsx')
    hotels_data = pd.read_excel(r'C:\Users\ayata\Documents\GitHub\dscoding-projects\Ayat.Ahmad\hotel.project\hotel\project\hotels\hotels.xlsx')
    preferences_data = pd.read_excel(r'C:\Users\ayata\Documents\GitHub\dscoding-projects\Ayat.Ahmad\hotel.project\hotel\project\hotels\preferences.xlsx')

    guests = [Guest(row['guest'], row['discount']) for _, row in guests_data.iterrows()]
    hotels = [Hotel(row['hotel'], row['rooms'], row['price']) for _, row in hotels_data.iterrows()]
    preferences = pd.DataFrame(preferences_data, columns=['guest', 'hotel', 'priority'])

    return guests, hotels, preferences

def print_report(method_name, allocation_result, total_revenue, satisfaction_level):
    console = Console()

    table = Table(title=f"[bold blue]{method_name} Allocation Report[/bold blue]")
    table.add_column("Guest ID", justify="center")
    table.add_column("Hotel ID", justify="center")

    allocated_guests = set()
    for guest_id, hotel_id in allocation_result:
        table.add_row(str(guest_id), str(hotel_id))
        allocated_guests.add(guest_id)

    console.print(table)

    num_allocated_guests = len(allocated_guests)
    num_unallocated_guests = len(set(guest.guest_id for guest in guests) - allocated_guests)

    console.print(f"\nTotal Revenue: [bold green]${total_revenue:.2f}[/bold green]")
    console.print(f"Mean Satisfaction: [bold cyan]{satisfaction_level:.2%}[/bold cyan]")
    console.print(f"Number of Guests Allocated: [bold yellow]{num_allocated_guests}[/bold yellow]")
    console.print(f"Number of Guests Not Allocated: [bold red]{num_unallocated_guests}[/bold red]\n\n")

def print_report(method_name, allocation_result, total_revenue, satisfaction_level):
    console = Console()

    table = Table(title=f"[bold blue]{method_name} Allocation Report[/bold blue]")
    table.add_column("Guest ID", justify="center")
    table.add_column("Hotel ID", justify="center")

    allocated_guests = set()
    for guest_id, hotel_id in allocation_result:
        table.add_row(str(guest_id), str(hotel_id))
        allocated_guests.add(guest_id)

    console.print(table)

    num_allocated_guests = len(allocated_guests)
    num_unallocated_guests = len(set(guest.guest_id for guest in guests) - allocated_guests)

    console.print(f"\nTotal Revenue: [bold green]${total_revenue:.2f}[/bold green]")
    console.print(f"Mean Satisfaction: [bold cyan]{satisfaction_level:.2%}[/bold cyan]")
    console.print(f"Number of Guests Allocated: [bold yellow]{num_allocated_guests}[/bold yellow]")
    console.print(f"Number of Guests Not Allocated: [bold red]{num_unallocated_guests}[/bold red]\n\n")

def print_report(method_name, allocation_result, total_revenue, satisfaction_level):
    console = Console()

    table = Table(title=f"[bold blue]{method_name} Allocation Report[/bold blue]")
    table.add_column("Guest ID", justify="center")
    table.add_column("Hotel ID", justify="center")

    allocated_guests = set()
    for guest_id, hotel_id in allocation_result:
        table.add_row(str(guest_id), str(hotel_id))
        allocated_guests.add(guest_id)

    console.print(table)

    num_allocated_guests = len(allocated_guests)
    num_unallocated_guests = len(set(guest.guest_id for guest in guests) - allocated_guests)

    console.print(f"\nTotal Revenue: [bold green]${total_revenue:.2f}[/bold green]")
    console.print(f"Mean Satisfaction: [bold cyan]{satisfaction_level:.2%}[/bold cyan]")
    console.print(f"Number of Guests Allocated: [bold yellow]{num_allocated_guests}[/bold yellow]")
    console.print(f"Number of Guests Not Allocated: [bold red]{num_unallocated_guests}[/bold red]\n\n")

def plot_comparison(revenues, satisfaction_levels, num_allocated_guests, num_unallocated_guests):
    methods = ['Random', 'Price', 'Availability', 'Priority']
    x = np.arange(len(methods))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot 1: Revenue and Satisfaction
    ax1.bar(x - 0.2, revenues, 0.4, label='Revenue', color=['#388E3C', '#FFA000'])
    ax1.set_xlabel('Allocation Methods')
    ax1.set_ylabel('Total Revenue', color='#388E3C')
    ax1.tick_params(axis='y', labelcolor='#388E3C')
    ax1.set_xticks(x)
    ax1.set_xticklabels(methods)

    ax1_twin = ax1.twinx()
    ax1_twin.bar(x + 0.2, satisfaction_levels, 0.4, label='Satisfaction', color=['#1565C0', '#F57C00'])
    ax1_twin.set_ylabel('Mean Satisfaction', color='#1565C0')
    ax1_twin.tick_params(axis='y', labelcolor='#1565C0')

    # Plot 2: Number of Guests Allocated and Unallocated
    ax2.bar(x - 0.2, num_allocated_guests, 0.4, label='Allocated', color=['#7CB342', '#FFB74D'])
    ax2.bar(x + 0.2, num_unallocated_guests, 0.4, label='Unallocated', color=['#E57373', '#FF8A65'])
    ax2.set_xlabel('Allocation Methods')
    ax2.set_ylabel('Number of Guests')
    ax2.set_xticks(x)
    ax2.set_xticklabels(methods)

    fig.tight_layout()
    fig.suptitle('Comparison of Allocation Methods', y=1.02)
    plt.show()


def main():
    guests, hotels, preferences = import_data()

    # Random Allocation
    random_allocation_result, random_allocation_revenue = AllocationMethods.random_allocation(guests, hotels)
    satisfaction_random = AllocationMethods.satisfaction(random_allocation_result, preferences)

    # Price Allocation
    price_allocation_result, price_allocation_revenue = AllocationMethods.price_allocation(guests, hotels)
    satisfaction_price = AllocationMethods.satisfaction(price_allocation_result, preferences)

    # Availability Allocation
    availability_allocation_result, availability_allocation_revenue = AllocationMethods.availability_allocation(guests, hotels)
    satisfaction_availability = AllocationMethods.satisfaction(availability_allocation_result, preferences)

    # Priority Allocation
    priority_allocation_result, priority_allocation_revenue = AllocationMethods.priority_allocation(guests, hotels, preferences)
    satisfaction_priority = AllocationMethods.satisfaction(priority_allocation_result, preferences)

    # Calculate the number of guests allocated and unallocated
    num_allocated_guests = [
        len(set(guest_id for guest_id, _ in random_allocation_result)),
        len(set(guest_id for guest_id, _ in price_allocation_result)),
        len(set(guest_id for guest_id, _ in availability_allocation_result)),
        len(set(guest_id for guest_id, _ in priority_allocation_result)),
    ]

    num_unallocated_guests = [
        len(set(guest.guest_id for guest in guests)) - num_allocated_guests[0],
        len(set(guest.guest_id for guest in guests)) - num_allocated_guests[1],
        len(set(guest.guest_id for guest in guests)) - num_allocated_guests[2],
        len(set(guest.guest_id for guest in guests)) - num_allocated_guests[3],
    ]

    # Plot Comparison
    revenues = [random_allocation_revenue, price_allocation_revenue, availability_allocation_revenue, priority_allocation_revenue]
    satisfaction_levels = [satisfaction_random, satisfaction_price, satisfaction_availability, satisfaction_priority]

    plot_comparison(revenues, satisfaction_levels, num_allocated_guests, num_unallocated_guests)

if __name__ == "__main__":
    main()
