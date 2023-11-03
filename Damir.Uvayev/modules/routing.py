import geopy.distance
from modules.utils import convert_to_decimal as ut


def get_distance(city1, city2, data):

    city_data = data[data['City'] == city1][['Latitude', 'Longitude']]
    if city_data.empty:
        return float('inf')
    lat1, lon1 = city_data.values[0]

    city_data = data[data['City'] == city2][['Latitude', 'Longitude']]
    if city_data.empty:
        return float('inf')
    lat2, lon2 = city_data.values[0]

    if not isinstance(lat1, float):
        lat1 = float(ut(lat1))

    if not isinstance(lat2, float):
        lat2 = float(ut(lat2))

    if not isinstance(lon1, float):
        lon1 = float(ut(lon1))

    if not isinstance(lon2, float):
        lon2 = float(ut(lon2))

    return geopy.distance.distance((lat1, lon1), (lat2, lon2)).km


def get_closest_cities(current_city, cities, data):
    distances = [(city, get_distance(current_city, city, data)) for city in cities if city != current_city]
    distances.sort(key=lambda x: x[1])
    return [city[0] for city in distances[:3]]

def find_warmest_route(avg_temperatures, start_city="London", end_city="Cape Town"):
    route = [start_city]
    current_city = start_city
    visited_cities = set()

    max_iterations = 1000
    iteration_count = 0

    while current_city != end_city and iteration_count < max_iterations:
        iteration_count += 1
        visited_cities.add(current_city)

        possible_cities = get_closest_cities(current_city, avg_temperatures['City'].unique(), avg_temperatures)
        possible_cities = [city for city in possible_cities if city not in visited_cities]

        if not possible_cities:
            print("No available next city. Exiting...")
            break

        temperatures = [avg_temperatures[avg_temperatures['City'] == city]['AverageTemperature'].values[0] for city in
                        possible_cities]
        warmest_city = possible_cities[temperatures.index(max(temperatures))]

        route.append(warmest_city)
        current_city = warmest_city

    return route