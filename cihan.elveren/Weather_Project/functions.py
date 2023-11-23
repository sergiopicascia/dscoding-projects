from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import functions as fun
import TemperatureDataProcessor as dp

def convert_coordinates(coord):
    # Validate the input format
    if not isinstance(coord, str) or len(coord) < 2 or coord[-1] not in 'NSEW':
        raise ValueError("Invalid coordinate format. Expected format 'DD.DD[D]'.")

    # Separate the numerical value and direction
    numeric_part, direction = coord[:-1], coord[-1]

    # Try converting the numeric part to float, raise ValueError if conversion fails
    try:
        numeric_value = float(numeric_part)
    except ValueError:
        raise ValueError("Invalid numeric value in the coordinate.")

    # Make the value negative if direction is West or South
    if direction in ['W', 'S']:
        numeric_value *= -1

    return numeric_value


def suggest_route(start_record, end_record, cities_data):
    """
    Suggest a route from a start city to an end city based on the nearest unvisited cities with the highest 
    average temperature.

    The function iterates through cities, selecting the nearest unvisited city with the highest average temperature, 
    until it reaches the destination city or runs out of unvisited cities.

    Parameters:
    start_record (dict): A dictionary containing data of the starting city, including the 'City' key.
    end_record (dict): A dictionary containing data of the destination city, including the 'City' key.
    cities_data (DataFrame): A pandas DataFrame containing city data, including 'City' and 'AverageTemperature'.

    Returns:
    list: A list of cities representing the suggested route.

    Raises:
    ValueError: If the start or end records are not in the expected format or if cities_data is not a DataFrame.
    """

    # Validate input data
    if not isinstance(start_record, dict) or not isinstance(end_record, dict):
        raise ValueError("Start and end records must be dictionaries.")
    if 'City' not in start_record or 'City' not in end_record:
        raise ValueError("Start and end records must contain a 'City' key.")
    if not isinstance(cities_data, pd.DataFrame):
        raise ValueError("cities_data must be a pandas DataFrame.")

    route = [start_record['City']]
    current_record = start_record
    visited_cities = set(route)

    while current_record['City'] != end_record['City']:
        unvisited_cities = cities_data[~cities_data['City'].isin(visited_cities)]
        nearest_cities = find_nearest_cities(current_record, unvisited_cities, n=3)

        if nearest_cities.empty:
            print("No more unvisited cities to go to. Ending route search.")
            break

        next_city_record = nearest_cities.loc[nearest_cities['AverageTemperature'].idxmax()]

        if next_city_record['City'] == end_record['City']:
            route.append(next_city_record['City'])
            break

        route.append(next_city_record['City'])
        visited_cities.add(next_city_record['City'])
        current_record = next_city_record

    return route



def plot_temperature_range(city_data, top_cities, start_year, end_year):
    """
    Plot the temperature range for top cities over a specified period.

    This function filters the city data for the specified period and plots the temperature range 
    for each city. It creates subplots for each city showing the trend of temperature range over time.

    Parameters:
    city_data (DataFrame): A pandas DataFrame containing city temperature data.
    top_cities (list or Series): A list or pandas Series of top cities to be plotted.
    start_year (int): The starting year for the period.
    end_year (int): The ending year for the period.

    Raises:
    ValueError: If the input data is not in the expected format or if the years are not valid.
    """

    # Validate input data
    if not isinstance(city_data, pd.DataFrame):
        raise ValueError("city_data must be a pandas DataFrame.")
    if not (isinstance(top_cities, list) or isinstance(top_cities, pd.Series)):
        raise ValueError("top_cities must be a list or a pandas Series.")
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise ValueError("start_year and end_year must be integers.")
    if start_year > end_year:
        raise ValueError("start_year must be less than or equal to end_year.")

    # Convert top_cities to list if it is not already
    if isinstance(top_cities, pd.Series):
        top_cities = top_cities.tolist()

    city_data_period = city_data[(city_data['Year'] >= start_year) & (city_data['Year'] <= end_year)]
    city_data_sorted = city_data_period.sort_values(['City', 'Year'])

    fig, axes = plt.subplots(5, 2, figsize=(15, 20), sharex=True)
    axes = axes.flatten()

    for i, city in enumerate(top_cities):
        city_specific_data = city_data_sorted[city_data_sorted['City'] == city]
        sns.lineplot(x='Year', y='temp_range', data=city_specific_data, ax=axes[i], color="m", marker="o")
        axes[i].set_title(f'Temperature Range Over Time for {city} ({start_year}-{end_year})')
        axes[i].set_ylabel('Temperature Range (°C)')
        axes[i].set_xlabel('Year')

    plt.tight_layout()
    plt.show()



# Bu fonksiyonu kullanarak, örneğin 1920-1970 yılları arasında sıcaklık aralığı en yüksek 10 şehrin grafiğini çizebilirsiniz.
# Örnek kullanım: plot_temperature_range(city_yearly_temps, top_10_cities, 1920, 1970)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_temperature_range_bar(city_data, top_cities):
    """
    Plot a bar chart showing the temperature range for top cities.

    Parameters:
    city_data (DataFrame): A pandas DataFrame containing city temperature data.
    top_cities (list or Series): A list or pandas Series of top cities to be plotted.

    Raises:
    ValueError: If the input data is not in the expected format.
    """

    # Validate input data
    if not isinstance(city_data, pd.DataFrame):
        raise ValueError("city_data must be a pandas DataFrame.")
    if not (isinstance(top_cities, list) or isinstance(top_cities, pd.Series)):
        raise ValueError("top_cities must be a list or a pandas Series.")

    # Convert top_cities to list if it is not already
    if isinstance(top_cities, pd.Series):
        top_cities = top_cities.tolist()

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
    """
    Plot a map showing the top cities with the largest temperature ranges.

    Args:
    top_cities (DataFrame): DataFrame containing the top cities with their temperature range and geographical coordinates.
    top_n (int): Number of top cities to be plotted.

    Raises:
    ValueError: If the input data is not in the expected format or if top_n is not a valid number.
    """
    # Validate input data
    if not isinstance(top_cities, pd.DataFrame):
        raise ValueError("top_cities must be a pandas DataFrame.")
    if not isinstance(top_n, int) or top_n <= 0:
        raise ValueError("top_n must be a positive integer.")

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
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees).

    Args:
    lon1, lat1: Longitude and latitude of the first point.
    lon2, lat2: Longitude and latitude of the second point.

    Returns:
    float: Distance between the two points in kilometers.
    """
    # Validate input data
    for value in [lon1, lat1, lon2, lat2]:
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude and latitude values must be numeric.")

    # Convert coordinates from decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth's radius in kilometers
    return c * r

def find_nearest_cities(current_coords, cities_data, n=3):
    """
    Find the nearest cities to the given coordinates.

    Args:
    current_coords (dict): A dictionary containing 'City', 'Longitude', and 'Latitude' of the current city.
    cities_data (DataFrame): A pandas DataFrame containing city data with 'City', 'Longitude', and 'Latitude'.
    n (int): Number of nearest cities to return.

    Returns:
    DataFrame: A DataFrame of the n nearest cities.

    Raises:
    ValueError: If the input data is not in the expected format.
    """
    # Validate input data
    if 'City' not in current_coords or 'Longitude' not in current_coords or 'Latitude' not in current_coords:
        raise ValueError("current_coords must contain 'City', 'Longitude', and 'Latitude'.")
    if not isinstance(cities_data, pd.DataFrame):
        raise ValueError("cities_data must be a pandas DataFrame.")
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n must be a positive integer.")

    cities_data = cities_data.copy()
    cities_data = cities_data[cities_data['City'] != current_coords['City']]

    distances = cities_data.apply(
        lambda row: haversine(current_coords['Longitude'], current_coords['Latitude'], row['Longitude'], row['Latitude']),
        axis=1
    )
    cities_data['Distance'] = distances
    return cities_data.sort_values('Distance').head(n)
