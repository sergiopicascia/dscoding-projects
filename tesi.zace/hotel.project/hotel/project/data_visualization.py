import matplotlib.pyplot as plt
import numpy as np

# Function to create plots and visualize the data
def visualize_allocation(allocation):
    figure, (p1, p2, p3) = plt.subplots(1, 3, figsize=(20, 8))

    # Plot 1: Total earnings for each hotel
    tot_earnings = allocation.groupby('hotel_no')['price_to_pay'].sum()
    tot_earnings.plot(kind='bar', ax=p1, color='#B98FE5')
    p1.set_title(r'Total Earnings of Hotel', fontweight='bold')
    p1.set_xlabel(r'Hotel No.', fontweight='bold')
    p1.set_ylabel(r'Total Earnings', fontweight='bold')

    # Plot 2: Degree of satisfaction for each customer
    deg_satisfaction = allocation.groupby('guest_no')['satisfaction_percentage'].mean()
    deg_satisfaction.plot(kind='bar', ax=p2, color='#97BF98')
    p2.set_title(r'Degree of Customer Satisfaction', fontweight='bold')
    p2.set_xlabel('Guest No.', fontweight='bold')
    p2.set_ylabel('Degree of Satisfaction', fontweight='bold')

    # Plot 3: Create data for the bar plot
    categories = ['No. of Guests Allocated', 'No. of Rooms Occupied', 'No. of Hotels Occupied']
    values = np.array([len(allocation), len(allocation), allocation['hotel_no'].nunique()])

    # Create a bar plot
    p3.bar(categories, values, color=['#ACD3D4', '#EEDBA7', '#EEA7D3'])
    p3.set_title(r'Allocation Statistics', fontweight='bold')
    p3.set_ylabel('Count')

    # Display the counts on top of the bars
    for i, v in enumerate(values):
        p3.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')

    plt.tight_layout(
                     pad=1.08,
                     h_pad=None,
                     w_pad=None,
                     rect=None)
    plt.show()
