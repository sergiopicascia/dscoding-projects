from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import functions as fun
import TemperatureDataProcessor as dp

def convert_coordinates(coord):
    # Split the coordinate into its numeric and directional parts
    parts = coord[:-1], coord[-1]
    
    # Convert the numeric part of the coordinate to a float
    numeric_value = float(parts[0])
   
    # If the directional part is 'W' or 'S', make the value negative
    if parts[1] in ['W', 'S']:
        numeric_value *= -1

    # Return the converted numeric value
    return numeric_value


def suggest_route(start_record, end_record, cities_data):
    # Start with the initial city
    route = [start_record['City']]
    current_record = start_record
    visited_cities = set(route)

    # Loop until the current city is the destination city
    while current_record['City'] != end_record['City']:
        # Exclude visited cities and the current city from the search
        unvisited_cities = cities_data[~cities_data['City'].isin(visited_cities)]

        # Find the nearest cities that have not been visited
        nearest_cities = find_nearest_cities(current_record, unvisited_cities, n=3)

        # If there are no unvisited cities left, break the loop (to avoid an infinite loop)
        if nearest_cities.empty:
            print("No more unvisited cities to go to. Ending route search.")
            break

        # Select the nearest city with the highest average temperature
        next_city_record = nearest_cities.loc[nearest_cities['AverageTemperature'].idxmax()]

        # If the destination city is the next city, add it to the route and break the loop
        if next_city_record['City'] == end_record['City']:
            route.append(next_city_record['City'])
            break

        # Add the selected city to the route and mark it as visited
        route.append(next_city_record['City'])
        visited_cities.add(next_city_record['City'])
        
        # Update the current city record
        current_record = next_city_record

    return route



def plot_temperature_range(city_data, top_cities, start_year, end_year):
    # Filter the data to include only the specified time period
    city_data_period = city_data[(city_data['Year'] >= start_year) & (city_data['Year'] <= end_year)]
    
    # Sort the filtered data by city and then by year
    city_data_sorted = city_data_period.sort_values(['City', 'Year'])

    # Create a grid of subplots with 5 rows and 2 columns, sharing the X axis
    fig, axes = plt.subplots(5, 2, figsize=(15, 20), sharex=True)
    axes = axes.flatten()  # Flatten the axes array for easy iteration

    # Plot the temperature range for each city in the top cities list
    for i, city in enumerate(top_cities):
        # Extract data for the specific city
        city_specific_data = city_data_sorted[city_data_sorted['City'] == city]

        # Create a line plot of temperature range over time for the city
        sns.lineplot(
            x='Year', 
            y='temp_range', 
            data=city_specific_data, 
            ax=axes[i], 
            color="magenta", 
            marker="o"  # Magenta color and circle marker for the plot
        )

        # Set the title, Y axis label, and X axis label for each subplot
        axes[i].set_title(f'Temperature Range Over Time for {city} ({start_year}-{end_year})')
        axes[i].set_ylabel('Temperature Range (°C)')
        axes[i].set_xlabel('Year')

    # Adjust the layout to prevent overlap
    plt.tight_layout()

    # Display the plot
    plt.show()



def plot_temperature_range_bar(city_data, top_cities):
    # Create a figure with dimensions 14x8
    plt.figure(figsize=(14, 8)) 

    # Create a bar plot showing temperature ranges of specified cities
    barplot = sns.barplot(
        x='temp_range',  # Data for the X axis: temperature ranges
        y='City',  # Data for the Y axis: city names
        data=city_data[city_data['City'].isin(top_cities)],  # Use data only for cities in 'top_cities' list
        palette='coolwarm'  # Use 'coolwarm' color palette
    )

    # Add title and labels to the plot
    plt.title('Top Cities with the Largest Temperature Ranges')  # Title of the plot
    plt.xlabel('Temperature Range (°C)')  # Label for the X axis
    plt.ylabel('City')  # Label for the Y axis

    # Annotate each bar with its length (temperature range)
    for p in barplot.patches:
        barplot.annotate(
            format(p.get_width(), '.2f'),  # Format the width of the bar (temperature range)
            (p.get_width(), p.get_y() + p.get_height() / 2.),  # Position of the text on the bar
            ha = 'left', va = 'center',  # Horizontal and vertical alignment
            xytext = (20, 0),  # Offset for text position relative to the bar
            textcoords = 'offset points'  # Type of text positioning
        )

    # Display the plot
    plt.show() 



def plot_temperature_range_map(top_cities, top_n=10):
    # Create a GeoDataFrame for the top cities, using their longitude and latitude for geometry
    top_cities_gdf = gpd.GeoDataFrame(
        top_cities.head(top_n),
        geometry=gpd.points_from_xy(top_cities.Longitude, top_cities.Latitude)
    )

    # Load the world map dataset for background
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Initialize a plot with specific size
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    # Plot the world map as a background with light grey color
    world.plot(ax=ax, color='lightgrey')

    # Plot the top cities on the map, color-coded by temperature range
    top_cities_gdf.plot(
        ax=ax, 
        column='temp_range',  # Column used to determine the color of points
        cmap='OrRd',          # Color map for different temperature ranges
        legend=True,          # Include a legend
        legend_kwds={
            'label': "Temperature Range (°C)",  # Legend label
            'orientation': "horizontal"        # Legend orientation
        }
    )

    # Annotate each city point with its ranking number
    for idx, row in top_cities_gdf.iterrows():
        ax.text(
            row.geometry.x, 
            row.geometry.y, 
            str(idx+1), 
            fontsize=12, 
            ha='right', 
            va='bottom'
        )

    # Create a list of city labels with their ranking
    city_labels = [f"{idx+1}. {row['City']}" for idx, row in top_cities_gdf.iterrows()]
    city_labels_str = "\n".join(city_labels)

    # Add the list of city labels to the map
    plt.text(
        0.90, 0.5, 
        city_labels_str, 
        transform=ax.transAxes, 
        fontsize=10,
        verticalalignment='center', 
        bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5)
    )

    # Set the title of the plot and turn off axis display
    plt.title(f'Top {top_n} Cities with the Widest Temperature Range', fontsize=14)
    ax.set_axis_off()

    # Display the plot
    plt.show()


def haversine(lon1, lat1, lon2, lat2):
    # Convert longitude and latitude from degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Calculate the differences in longitude and latitude
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Apply the Haversine formula to calculate the distance
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  # Haversine formula's component
    c = 2 * asin(sqrt(a))  # Final part of the formula to compute the great-circle distance
    r = 6371  # Radius of the Earth in kilometers

    # Return the distance in kilometers
    return c * r



def find_nearest_cities(current_coords, cities_data, n=3):
    # Create a copy of the cities data to prevent modifying the original dataset
    cities_data = cities_data.copy()

    # Remove the current city from the dataset to avoid self-comparison
    cities_data = cities_data[cities_data['City'] != current_coords['City']]

    # Calculate the distance of each city from the current city using the Haversine formula
    distances = cities_data.apply(
        lambda row: haversine(
            current_coords['Longitude'], 
            current_coords['Latitude'], 
            row['Longitude'], 
            row['Latitude']
        ),
        axis=1
    )
    cities_data['Distance'] = distances  # Add a new column for distances

    # Return the top n nearest cities sorted by distance
    return cities_data.sort_values('Distance').head(n)
