import math
"""
-- Documentation --
A set of functions called by the Map class in order to compute the best route between the top 5 warmest ones.
"""


def calculate_distance(city1, city2, route):
    """
     Calculates the great-circle distance between two cities on the Earth's surface using their latitude and longitude coordinates.
    Parameters:
    city1: Pandas Series representing the first city with 'Latitude' and 'Longitude' columns.
    city2: Pandas Series representing the second city with 'Latitude' and 'Longitude' columns.
    route: List of cities already visited to avoid loops.
    Returns:
    If city1['City'] is in the route, returns a large distance value (1000000000) to avoid loops.
    Otherwise, returns the calculated distance between city1 and city2 using the Haversine formula.
    """
    # calculate the distance between two cities using their latitude and longitude coordinates
    lat1, lon1 = city1['Latitude'], city1['Longitude']
    lat2, lon2 = city2['Latitude'], city2['Longitude']

    # Haversine formula to compute distances on the Earth's surface in kms
    radius = 6371  # earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    if city1['City'] in route:   # I set the cities where we already have been and the current city out of the planet to avoid loops :)
        return 1000000000
    else:
        return distance


def warmest_closest_city(current_city, ds, route):
    """
    Finds the warmest city among the top 5 closest cities to the given current city based on temperature.

    Parameters:
    current_city: Pandas Series representing the current city with 'Latitude', 'Longitude', and 'AverageTemperature' columns.
    ds: Pandas DataFrame containing data about cities, including 'Latitude', 'Longitude', 'AverageTemperature', and 'City' columns.
    route: List of cities already visited to avoid loops.
    Returns:
    The name of the warmest city among the top 5 closest cities to the current_city.
    """
    cities = []
    for idx, city in ds.iterrows():
        distance = calculate_distance(city, current_city, route)
        cities.append((distance, city))

    top5 = sorted(cities, key=lambda x: x[0])[:5]    # one line function to take the top 5 cities by distance (closest)
    warmest = max(top5, key=lambda x: x[1]['AverageTemperature'])   # same but by AverageTemperature

    return warmest[1].loc['City']        # we return the name of the warmest city


def best_route(ds, date, start_city, target_city):
    """
     Finds the best route from a starting city to a target city based on both distance and temperature.

    Parameters:
    ds: Pandas DataFrame containing data about cities, including 'Latitude', 'Longitude', 'AverageTemperature', 'City', and 'dt' columns.
    date: Date for which the city data is considered.
    start_city: Name of the starting city.
    target_city: Name of the target city.
    Returns:
    A list representing the best route from the start_city to the target_city based on both distance and temperature. The list includes the names of cities in the order of the route.

    """
    ds = ds[ds['dt'] == date]
    route = [start_city]
    current_city = start_city  # initialize current_city with the start city name

    while current_city != target_city:
        # find the GeoDataFrame row for the current city
        current_city_row = ds[ds['City'] == current_city].iloc[0]
        warmest = warmest_closest_city(current_city_row, ds, route)
        # extract the city name from the GeoDataFrame row
        current_city = warmest
        route.append(current_city)
    return route










