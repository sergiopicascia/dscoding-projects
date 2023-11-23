def print_allocation_data(allocation):

    # Prints the data from the allocation DataFrame.
    print("\nAllocation Data:")
    print(allocation)

    # Prints out total earnings of the hotel by performing the sum and grouping by the number of hotel and the price
    total_earnings = allocation.groupby('hotel_no')['price_to_pay'].sum()
    print("\nTotal Earnings for Each Hotel:")
    print(total_earnings)

    # Prints out degree of satisfaction by performing the mean and grouping by the number of the guest and the satisfaction %
    deg_satisfaction = allocation.groupby('guest_no')['satisfaction_percentage'].mean()
    print("\nDegree of Satisfaction for Each Customer:")
    print(deg_satisfaction)

    # Performs the actions to get these data and then print it out using dictionaries
    allocation_statistics = {
        'No. of Guests Allocated': len(allocation),
        'No. of Rooms Occupied': len(allocation),
        'No. of Hotels Occupied': allocation['hotel_no'].nunique()
    }

    print("\nAllocation Statistics:")
    for category, value in allocation_statistics.items():
        print(f"{category}: {value}")

    print()

def calc_degree_satisfaction(guest_no, hotel_no, preferences):

    # Creates a dataframe that contains the preferences of the specified guest
    pref_of_guest = preferences[preferences['guest'] == guest_no].reset_index()
    # It then checks if the guest has no recorded preference and if they do not it returns 100% satisfaction
    if pref_of_guest.empty:
        return 100

    # then calculates the satisfaction percentage according to the guest's preferences
    # these actions are performed in order to get the index where the guest's preference matches the specified hotel,
    # then divided to get the position of the guests rank of priorities then turned into % of satisfaction

    return round((1 - pref_of_guest['hotel'].eq(hotel_no).idxmax() / len(pref_of_guest)) * 100) \
        if hotel_no in pref_of_guest['hotel'].values \
        else 0
    # If it does not satisfy the preference it returns 0

