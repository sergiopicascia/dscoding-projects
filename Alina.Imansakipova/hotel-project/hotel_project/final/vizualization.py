import matplotlib.pyplot as plt

def visualize_allocation(allocation):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Total earnings for each hotel
    paid_price_by_hotel = allocation.groupby('hotel_id')['paid_price'].sum()
    paid_price_by_hotel.plot(kind='bar', ax=ax1, title='Total Earnings by Hotel')
    ax1.set_xlabel('Total Earnings')
    ax1.set_ylabel('Paid Price Sum')

    # Plot 2: Satisfaction percentage for each guest
    satisfaction_by_guest = allocation.groupby('guest_id')['satisfaction_percentage'].mean()
    satisfaction_by_guest.plot(kind='bar', ax=ax2, title='Satisfaction Percentage by Guest')
    ax2.set_xlabel('Guest ID')
    ax2.set_ylabel('Satisfaction Percentage')

    fig.suptitle(f"number of customers/rooms = {str(len(allocation))}; number of hotels = {str(allocation['hotel_id'].nunique())}")

    plt.tight_layout()
    plt.show()