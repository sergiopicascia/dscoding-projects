import geopy.distance
from modules.utils import convert_to_decimal

class RouteFinder:
    def __init__(self, data):
        self.data = data

    def get_distance(self, city1, city2):
        city_data = self.data[self.data['City'] == city1][['Latitude', 'Longitude']]
        if city_data.empty:
            return float('inf')
        lat1, lon1 = city_data.values[0]

        city_data = self.data[self.data['City'] == city2][['Latitude', 'Longitude']]
        if city_data.empty:
            return float('inf')
        lat2, lon2 = city_data.values[0]

        lat1, lat2 = float(convert_to_decimal(lat1)), float(convert_to_decimal(lat2))
        lon1, lon2 = float(convert_to_decimal(lon1)), float(convert_to_decimal(lon2))

        return geopy.distance.distance((lat1, lon1), (lat2, lon2)).km

    def get_closest_cities(self, current_city, all_cities):
        distances = [(city, self.get_distance(current_city, city)) for city in all_cities if city != current_city]
        distances.sort(key=lambda x: x[1])
        return [city[0] for city in distances][:3]  # Returning only the top 3 closest cities

    def find_warmest_route(self, start_city="London", end_city="Cape Town"):
        route = [start_city]
        current_city = start_city
        visited_cities = set()

        max_iterations = 1000
        iteration_count = 0

        while current_city != end_city and iteration_count < max_iterations:
            iteration_count += 1
            visited_cities.add(current_city)

            all_cities = self.data['City'].unique().tolist()
            possible_cities = self.get_closest_cities(current_city, all_cities)
            possible_cities = [city for city in possible_cities if city not in visited_cities]

            if not possible_cities:
                print("No available next city. Exiting...")
                break

            closest_data = self.data[self.data['City'].isin(possible_cities)]
            temperatures = closest_data.groupby('City')['AverageTemperature'].mean()
            warmest_city = temperatures.idxmax()

            route.append(warmest_city)
            current_city = warmest_city

        return route

