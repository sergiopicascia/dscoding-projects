# routing.py

import geopy.distance as gd
from utils import convert_to_decimal as ut

class Routing:
    def get_distance(self, city1, city2, data):
        """Calculate the distance between two cities based on their latitude and longitude."""
        lat_col = 'Latitude'
        lon_col = 'Longitude'

        # Check if the specified columns exist in the DataFrame
        if lat_col not in data.columns or lon_col not in data.columns:
            return float('inf')

        city_data1 = data[data['City'] == city1][[lat_col, lon_col]]
        city_data2 = data[data['City'] == city2][[lat_col, lon_col]]

        if city_data1.empty or city_data2.empty:
            return float('inf')

        lat1, lon1 = city_data1.values[0]
        lat2, lon2 = city_data2.values[0]

        lat1 = float(ut(lat1))
        lat2 = float(ut(lat2))
        lon1 = float(ut(lon1))
        lon2 = float(ut(lon2))

        return gd.distance((lat1, lon1), (lat2, lon2)).km

    def get_closest_cities(self, current_city, cities, data):
        """Get the three closest cities to the current city."""
        lat_col = 'Latitude'
        lon_col = 'Longitude'

        # Check if the specified columns exist in the DataFrame
        if lat_col not in data.columns or lon_col not in data.columns:
            return []

        distances = [
            (city, self.get_distance(current_city, city, data)) for city in cities if city != current_city
        ]
        distances = [(city, distance) for city, distance in distances if distance != float('inf')]
        distances.sort(key=lambda x: x[1])
        return [city[0] for city in distances[:3]]  # Retrieve only three closest cities
        #def get_distance(self, city1, city2, data):
        """Calculate the distance between two cities based on their latitude and longitude."""
        #city_data1 = data[data['City'] == city1][['Latitude', 'Longitude']]
        #city_data2 = data[data['City'] == city2][['Latitude', 'Longitude']]

        #if city_data1.empty or city_data2.empty:
            #return float('inf')

        #lat1, lon1 = city_data1.values[0]
        #lat2, lon2 = city_data2.values[0]

        #lat1 = float(ut(lat1))
        #lat2 = float(ut(lat2))
        #lon1 = float(ut(lon1))
        #lon2 = float(ut(lon2))

        #return gd.distance((lat1, lon1), (lat2, lon2)).km

    #def get_closest_cities(self, current_city, cities, data):
        """Get the three closest cities to the current city."""
        #distances = [(city, self.get_distance(current_city, city, data)) for city in cities if city != current_city]
        #distances.sort(key=lambda x: x[1])
        #return [city[0] for city in distances[:3]]  # Retrieve only three closest cities

    def find_warmest_route(self, avg_temperatures, start_city, end_city="Cape Town"):
        """Find the warmest route from the specified starting city to the end city, based on average temperatures."""
        route = [start_city]
        current_city = start_city
        visited_cities = set()

        max_iterations = 1000
        iteration_count = 0

        while current_city != end_city and iteration_count < max_iterations:
            iteration_count += 1
            visited_cities.add(current_city)

            # Get the three closest cities
            possible_cities = self.get_closest_cities(current_city, avg_temperatures['City'].unique(), avg_temperatures)
            possible_cities = [city for city in possible_cities if city not in visited_cities]

            if not possible_cities:
                print("No available next city. Exiting...")
                break

            # From the three closest cities, select the one with the highest temperature
            temperatures = [avg_temperatures[avg_temperatures['City'] == city]['AverageTemperature'].values[0] for city in
                            possible_cities]
            warmest_city = possible_cities[temperatures.index(max(temperatures))]

            route.append(warmest_city)
            current_city = warmest_city

        return route
