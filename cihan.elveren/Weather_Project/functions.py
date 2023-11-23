from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import functions as fun
import TemperatureDataProcessor as dp

def convert_coordinates(coord):
    # Function to convert coordinate data to numerical value.
    # Example: "41.23N" -> 41.23, "41.23W" -> -41.23
    
    # Separate the numerical value and direction of the coordinate.
    parts = coord[:-1], coord[-1]
    # Convert the numeric value to float type.
    numeric_value = float(parts[0])
    # If the direction is west or south, make it negative.
    if parts[1] in ['W', 'S']:
        numeric_value *= -1
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
    # Filter data for the specified period
    city_data_period = city_data[(city_data['Year'] >= start_year) & (city_data['Year'] <= end_year)]
    
    # Sort the data by city and year
    city_data_sorted = city_data_period.sort_values(['City', 'Year'])

    # Create subplots
    fig, axes = plt.subplots(5, 2, figsize=(15, 20), sharex=True)
    axes = axes.flatten()

    # Plot for each city
    for i, city in enumerate(top_cities):
        city_specific_data = city_data_sorted[city_data_sorted['City'] == city]
        sns.lineplot(x='Year', y='temp_range', data=city_specific_data, ax=axes[i], color="m", marker="o")
        axes[i].set_title(f'Temperature Range Over Time for {city} ({start_year}-{end_year})')
        axes[i].set_ylabel('Temperature Range (°C)')
        axes[i].set_xlabel('Year')

    plt.tight_layout()
    plt.show()


def plot_temperature_range_bar(city_data, top_cities):

    plt.figure(figsize=(14, 8))
    barplot = sns.barplot(
        x='temp_range',
        y='City',
        data=city_data[city_data['City'].isin(top_cities)],
        palette='coolwarm'
    )

    plt.title('Top Cities with the Largest Temperature Ranges')
    plt.xlabel('Temperature Range (°C)')
    plt.ylabel('City')

    for p in barplot.patches:
        barplot.annotate(format(p.get_width(), '.2f'), 
                         (p.get_width(), p.get_y() + p.get_height() / 2.), 
                         ha = 'left', va = 'center', 
                         xytext = (20, 0), 
                         textcoords = 'offset points')

    plt.show()


def plot_temperature_range_map(top_cities, top_n=10):

    # Create a GeoDataFrame for the top cities
    top_cities_gdf = gpd.GeoDataFrame(
        top_cities.head(top_n),
        geometry=gpd.points_from_xy(top_cities.Longitude, top_cities.Latitude)
    )

    # Load the world dataset for the background map
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Plot the map
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    world.plot(ax=ax, color='lightgrey')
    top_cities_gdf.plot(ax=ax, column='temp_range', cmap='OrRd', legend=True,
                        legend_kwds={'label': "Temperature Range (°C)",
                                     'orientation': "horizontal"})

    # Add city numbers and labels to the map
    for idx, row in top_cities_gdf.iterrows():
        ax.text(row.geometry.x, row.geometry.y, str(idx+1), fontsize=12, ha='right', va='bottom')
    city_labels = [f"{idx+1}. {row['City']}" for idx, row in top_cities_gdf.iterrows()]
    city_labels_str = "\n".join(city_labels)
    plt.text(0.90, 0.5, city_labels_str, transform=ax.transAxes, fontsize=10,
             verticalalignment='center', bbox=dict(boxstyle="round,pad=0.3", edgecolor='black', facecolor='white', alpha=0.5))

    plt.title(f'Top {top_n} Cities with the Widest Temperature Range', fontsize=14)
    ax.set_axis_off()
    plt.show()

def haversine(lon1, lat1, lon2, lat2):
    # Convert coordinates in radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Longitude and latitude differences
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth's radius in kilometers
    return c * r


def find_nearest_cities(current_coords, cities_data, n=3):
    # Create a copy of the data to avoid SettingWithCopyWarning
    cities_data = cities_data.copy()

    # Exclude the current city from the dataset
    cities_data = cities_data[cities_data['City'] != current_coords['City']]

    # Calculate distances using the Haversine formula
    distances = cities_data.apply(
        lambda row: haversine(current_coords['Longitude'], current_coords['Latitude'], row['Longitude'], row['Latitude']),
        axis=1
    )
    cities_data['Distance'] = distances
    return cities_data.sort_values('Distance').head(n)