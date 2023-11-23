import pandas as pd
import matplotlib.pyplot as plt

def visualization(allocation):
    fig, (ax1, ax2) = plt.subplots(2, 2, figsize=(15, 10))
    #calculate total earnings and mean earnings for each hotel
    paid_price_by_hotel_sum = allocation.groupby('hotel_id')['paid_price'].sum()
    paid_price_by_hotel_mean = allocation.groupby('hotel_id')['paid_price'].mean()
    
    # Plot total earnings
    paid_price_by_hotel_sum.plot(kind='bar', ax=ax1, title='Total Earnings by Hotel')
    ax1.set_xlabel('Hotel ID')
    ax1.set_ylabel('Paid Price Sum')

    # Plot mean earnings
    paid_price_by_hotel_mean.plot(kind='bar', ax=ax2, title='Mean Earnings by Hotel')
    ax2.set_xlabel('Hotel ID')
    ax2.set_ylabel('Paid Price Mean')
    
    #graph 2: boxplot of the mean satisfaction percentage by guest
    satisfaction_by_guest = allocation.groupby('guest_id')['satisfaction_percentage'].mean()
    ax.boxplot(satisfaction_by_guest, vert=False, labels=['Mean Satisfaction'])
    ax.set_title('Boxplot of Mean Satisfaction Percentage by Guest')
    ax.set_xlabel('Satisfaction Percentage')
    ax.set_yticklabels(['Guests']) 

    plt.show()
