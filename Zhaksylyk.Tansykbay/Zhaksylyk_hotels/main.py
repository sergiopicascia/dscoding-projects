from modules.Accomodation import Solution
from modules import utils
import os

#Getting the path to the datasets
current_directory = os.path.abspath(__file__)
guests_path = os.path.join(current_directory, os.path.join('..', 'data', 'guests.xlsx'))
hotels_path = os.path.join(current_directory, os.path.join('..', 'data', 'hotels.xlsx'))
preferences_path = os.path.join(current_directory, os.path.join('..', 'data', 'preferences.xlsx'))

#Creating Solution instances for each accomodation strategy
solution_1 = Solution()
solution_2 = Solution()
solution_3 = Solution()
solution_4 = Solution()

#Performing accomodation
solution_1.random(guests_file=guests_path, hotels_file=hotels_path, preferences_file=preferences_path)
solution_2.preference(guests_file=guests_path, hotels_file=hotels_path, preferences_file=preferences_path)
solution_3.cheapest_first(guests_file=guests_path, hotels_file=hotels_path, preferences_file=preferences_path)
solution_4.availability(guests_file=guests_path, hotels_file=hotels_path, preferences_file=preferences_path)

#Visualizations
utils.plot([solution_1.guests_accomodated,solution_2.guests_accomodated,solution_3.guests_accomodated,solution_4.guests_accomodated],
           [solution_1.diff_hotels,solution_2.diff_hotels,solution_3.diff_hotels,solution_4.diff_hotels],
           [solution_1.revenue,solution_2.revenue,solution_3.revenue,solution_4.revenue],
           [solution_1.satisfaction,solution_2.satisfaction,solution_3.satisfaction,solution_4.satisfaction])