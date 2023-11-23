import matplotlib.pyplot as plt
import numpy as np

#util function for plotting
def plot(guests_accomodated, hotels_occupied, revenue, satisfaction):
    fig, ax = plt.subplots(2, 2, figsize=(14, 12))

    guests = [guests_accomodated[0], guests_accomodated[1], guests_accomodated[2], guests_accomodated[3]]
    bar1 = ax[0,0].bar(['Random', 'Preference', 'Price', 'Availability'], guests, color = 'orange')
    # adding annotation to the plot
    for rect in bar1:
        height = rect.get_height()
        ax[0,0].text(rect.get_x() + rect.get_width()/2.0, height, int(height), ha='center', va='bottom')

    ax[0,0].set_title('Number of Guests accomodated by each strategy')
    ax[0,0].set_xlabel('Accomodation Strategy')


    hotels = [hotels_occupied[0], hotels_occupied[1], hotels_occupied[2], hotels_occupied[3]]
    bar2 = ax[0,1].bar(['Random', 'Preference', 'Price', 'Availability'], hotels, color = 'orange')
    # adding annotation to the plot
    for rect in bar2:
        height = rect.get_height()
        ax[0,1].text(rect.get_x() + rect.get_width()/2.0, height, int(height), ha='center', va='bottom')

    ax[0,1].set_title('Number of Hotels occupied by each strategy')
    ax[0,1].set_xlabel('Accomodation Strategy')


    mean_revenue = [np.mean(revenue[0]) , np.mean(revenue[1]), np.mean(revenue[2]), np.mean(revenue[3])]
    bar3 = ax[1,0].bar(['Random', 'Preference', 'Price', 'Availability'], mean_revenue, color = 'orange')
    # adding annotation to the plot
    for rect in bar3:
        height = rect.get_height()
        ax[1,0].text(rect.get_x() + rect.get_width()/2.0, height, int(height), ha='center', va='bottom')

    ax[1,0].set_title('Mean Revenue for Hotels')
    ax[1,0].set_xlabel('Accomodation Strategy')


    mean_satisfaction = [sum(satisfaction[0]), sum(satisfaction[1]), sum(satisfaction[2])+75*(50/4000), sum(satisfaction[3])+46*(50/4000)]
    bar4 = ax[1,1].bar(['Random', 'Preference', 'Price', 'Availability'], mean_satisfaction, color = 'orange')
    # adding annotation to the plot
    for rect in bar4:
        height = rect.get_height()
        ax[1,1].text(rect.get_x() + rect.get_width()/2.0, height, int(height), ha='center', va='bottom')

    ax[1,1].set_title('Mean Customer Satisfaction')
    ax[1,1].set_xlabel('Accomodation Strategy')
    ax[1,1].set_ylabel('Customer Satisfaction (Lower is better)')
    plt.show()