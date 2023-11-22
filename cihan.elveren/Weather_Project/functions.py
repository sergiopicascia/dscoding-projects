from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd
import functions as fun

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def clean_and_transform_data(data):
    
    # Convert the 'dt' column to datetime type
    data['dt'] = pd.to_datetime(data['dt'])

    # Extract the year from the 'dt' column
    data['Year'] = data['dt'].dt.year

    # Remove rows with any missing values
    data_cleaned = data.dropna()

    return data_cleaned




def transform_coordinates(data):
    data['Latitude'] = data['Latitude'].apply(fun.convert_coordinates)
    data['Longitude'] = data['Longitude'].apply(fun.convert_coordinates)
    return data

def filter_data_by_year_range(data, start_year, end_year):
    return data[(data['Year'] >= start_year) & (data['Year'] <= end_year)]

def find_top_cities_with_temp_ranges(data, n=10):
    temp_ranges = data.sort_values('temp_range', ascending=False).groupby('City').first().reset_index()
    return temp_ranges.sort_values('temp_range', ascending=False).head(n)

def merge_with_geographical_data(data, city_data):
    return data.merge(city_data[['City', 'temp_range']], on='City').drop_duplicates(subset=['City'])



# Function to calculate the distance between two coordinates using the Haversine formula
def haversine(lon1, lat1, lon2, lat2):
   # Convert coordinates in radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

   # Longitude and latitude differences
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth's radius (in km)
    return c * r

def find_nearest_cities(current_coords, cities_data, n=3):
    # Calculate distances with Haversine formula
    distances = cities_data.apply(
        lambda row: haversine(current_coords['Longitude'], current_coords['Latitude'], row['Longitude'], row['Latitude']),
        axis=1
    )
    
   # When returning nearest cities, exclude current location (at 0 distance)
    nearest_cities = cities_data.loc[distances.nlargest(len(distances) - 1).nsmallest(n).index]
    return nearest_cities

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
    """
    Plot the temperature range over time for the top cities.
    
    Args:
    city_data (DataFrame): DataFrame containing city, year, and temperature data.
    top_cities (list): List of top cities to be plotted.
    start_year (int): The starting year for the plot.
    end_year (int): The ending year for the plot.
    """
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

# Bu fonksiyonu kullanarak, örneğin 1920-1970 yılları arasında sıcaklık aralığı en yüksek 10 şehrin grafiğini çizebilirsiniz.
# Örnek kullanım: plot_temperature_range(city_yearly_temps, top_10_cities, 1920, 1970)


def plot_temperature_range_bar(city_data, top_cities):
    """
    Plot a bar graph showing the top cities with the largest temperature ranges.
    
    Args:
    city_data (DataFrame): DataFrame containing city and temperature range data.
    top_cities (list): List of top cities to be plotted.
    """
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

# Bu fonksiyonu kullanarak, belirli şehirlerin sıcaklık aralıklarını gösteren bir bar grafiği çizebilirsiniz.
# Örnek kullanım: plot_temperature_range_bar(city_data=top_cities_with_ranges, top_cities=top_10_cities)



def plot_temperature_range_map(city_data_file, start_year, end_year, top_n=10):
    """
    Plot a map showing the top cities with the largest temperature ranges within a specific time range.
    
    Args:
    city_data_file (str): File path to the city data CSV.
    start_year (int): Starting year of the time range.
    end_year (int): Ending year of the time range.
    top_n (int): Number of top cities to be plotted.
    """
    cities_df = pd.read_csv(city_data_file)

    # Filter data for the specified period and calculate temperature range
    filtered_data = cities_df[(pd.to_datetime(cities_df['dt']).dt.year >= start_year) & 
                              (pd.to_datetime(cities_df['dt']).dt.year <= end_year)]
    city_temp_range = filtered_data.groupby('City').agg(
        max_temp=('AverageTemperature', 'max'),
        min_temp=('AverageTemperature', 'min')
    ).reset_index()
    city_temp_range['temp_range'] = city_temp_range['max_temp'] - city_temp_range['min_temp']

    # Identify the top cities with the largest temperature range
    top_cities = city_temp_range.nlargest(top_n, 'temp_range')

    # Merge with geographical coordinates
    top_cities_geo = pd.merge(top_cities, filtered_data[['City', 'Latitude', 'Longitude']].drop_duplicates(), on='City')

    # Create a GeoDataFrame for the top cities
    top_cities_gdf = gpd.GeoDataFrame(
        top_cities_geo,
        geometry=gpd.points_from_xy(top_cities_geo.Longitude, top_cities_geo.Latitude)
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

    plt.title(f'Top {top_n} Cities with the Widest Temperature Range Between {start_year}-{end_year}', fontsize=14)
    ax.set_axis_off()
    plt.show()

# Bu fonksiyonu kullanarak, belirli bir zaman aralığında en geniş sıcaklık aralığına sahip şehirlerin haritasını çizebilirsiniz.
# Örnek kullanım: plot_temperature_range_map('MajorCities.csv', 1920, 1970, top_n=10)

def calculate_city_yearly_temperature_ranges(data):
    # Create a copy of the DataFrame to avoid SettingWithCopyWarning
    data = data.copy()

    # Extract year from date
    data['Year'] = pd.to_datetime(data['dt']).dt.year

    # Calculate max and min temperatures for each city and year
    yearly_temps = data.groupby(['City', 'Year'])['AverageTemperature'].agg(['max', 'min']).reset_index()

    # Calculate temperature range
    yearly_temps['temp_range'] = yearly_temps['max'] - yearly_temps['min']

    return yearly_temps

