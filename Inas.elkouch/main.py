from PIL._imaging import display
from matplotlib import widgets

from map import *
from planner import RoutePlanner

"""
-- Documentation --
   This is the main.py module, where all the classes and functions are called
"""

# Example usage:
file_name = 'temperatures.csv'

# Creating a new object
temperature_viz = TemperatureVisualization(file_name)
year_list = np.unique(temperature_viz.data['year']).tolist()

# Possibility to select a year of your choice
year_dropdown = widgets.Dropdown(
    options=year_list,
    value=min(year_list),
    description='Select Year:'
)

# Plotting the cities in 2005 as ref value
temperature_viz.plot_cities(2010)
# Displaying the complete map
interact = widgets.interactive(temperature_viz.update_map, year=year_dropdown)
display(interact)

# Creating che RoutePlanner object
planner = RoutePlanner(file_name)
planner.plan_route(['2010-02-01', -5.3050000000000015, 0.419, 'Peking', 'China', 39.38, 116.53], 'Los Angeles')
# Displaying the route
planner.print_route()
