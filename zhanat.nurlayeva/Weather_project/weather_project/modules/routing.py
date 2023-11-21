# Routing Class
# Calculate distances.
# Find the warmest route.
import geopy.distance
from modules.utils import convert_to_decimal as ut

class Routing:
    @staticmethod
    def get_distance(city1, city2, data):
        """
        Calculate the distance between two cities based on their latitude and longitude.

        Parameters:
        - city1 (str): Name of the first city.
        - city2 (str): Name of the second city.
        - data (pd.DataFrame): DataFrame with city data, including 'City', 'Latitude', and 'Longitude'.

        Returns:
        - float: Distance between the two cities in kilometers.
        """
        # Retrieve the latitude and longitude for city1
        city_data = data[data['City'] == city1][['Latitude', 'Longitude']]
        if city_data.empty:
            return float('inf')
        lat1, lon1 = city_data.values[0]

        # Retrieve the latitude and longitude for city2
        city_data = data[data['City'] == city2][['Latitude', 'Longitude']]
        if city_data.empty:
            return float('inf')
        lat2, lon2 = city_data.values[0]

        # Convert coordinates to floats
        lat1, lat2, lon1, lon2 = map(float, map(ut, [lat1, lat2, lon1, lon2]))

        return geopy.distance.distance((lat1, lon1), (lat2, lon2)).km

    @staticmethod
    def get_closest_cities(current_city, cities, data):
        """
        Get the three closest cities to the current city.

        Parameters:
        - current_city (str): Name of the current city.
        - cities (list): List of city names.
        - data (pd.DataFrame): DataFrame with city data, including 'City', 'Latitude', and 'Longitude'.

        Returns:
        - list: Names of the three closest cities.
        """
        distances = [(city, Routing.get_distance(current_city, city, data)) for city in cities if city != current_city]
        distances.sort(key=lambda x: x[1])
        return [city[0] for city in distances[:3]]  # Retrieve only three closest cities

    @staticmethod
    def find_warmest_route(avg_temperatures, start_city="London", end_city="Cape Town"):
        """
        Find the warmest route from the start city to the end city, based on average temperatures.

        Parameters:
        - avg_temperatures (pd.DataFrame): DataFrame with city temperature data, including 'City' and 'AverageTemperature'.
        - start_city (str): Name of the starting city. Default is "London".
        - end_city (str): Name of the destination city. Default is "Cape Town".

        Returns:
        - list: Route from the start city to the end city, considering the warmest cities.
        """
        route = [start_city]
        current_city = start_city
        visited_cities = set()

        max_iterations = 1000
        iteration_count = 0

        while current_city != end_city and iteration_count < max_iterations:
            iteration_count += 1
            visited_cities.add(current_city)

            # Get the three closest cities
            possible_cities = Routing.get_closest_cities(current_city, avg_temperatures['City'].unique(), avg_temperatures)
            possible_cities = [city for city in possible_cities if city not in visited_cities]

            if not possible_cities:
                print("No available next city. Exiting...")
                break

            # From the three closest cities, select the one with the highest temperature
            temperatures = [
                avg_temperatures[avg_temperatures['City'] == city]['AverageTemperature'].values[0] for city in
                possible_cities
            ]
            warmest_city = possible_cities[temperatures.index(max(temperatures))]

            route.append(warmest_city)
            current_city = warmest_city

        return route

'''import geopy.distance

class Routing:
    @staticmethod
    def get_distance(city1, city2, data):
        """
        Calculate the distance between two cities based on their latitude and longitude.

        Parameters:
        - city1 (str): Name of the first city.
        - city2 (str): Name of the second city.
        - data (pd.DataFrame): DataFrame with city data, including 'City', 'Latitude', and 'Longitude'.

        Returns:
        - float: Distance between the two cities in kilometers.
        """
        # Retrieve the latitude and longitude for city1
        city_data = data[data['City'] == city1][['Latitude', 'Longitude']]
        if city_data.empty:
            return float('inf')
        lat1, lon1 = city_data.values[0]

        # Retrieve the latitude and longitude for city2
        city_data = data[data['City'] == city2][['Latitude', 'Longitude']]
        if city_data.empty:
            return float('inf')
        lat2, lon2 = city_data.values[0]

        # Convert coordinates to floats
        lat1, lat2, lon1, lon2 = map(float, map(ut, [lat1, lat2, lon1, lon2]))

        return geopy.distance.distance((lat1, lon1), (lat2, lon2)).km

    @staticmethod
    def get_closest_cities(current_city, cities, data):
        """
        Get the three closest cities to the current city.

        Parameters:
        - current_city (str): Name of the current city.
        - cities (list): List of city names.
        - data (pd.DataFrame): DataFrame with city data, including 'City', 'Latitude', and 'Longitude'.

        Returns:
        - list: Names of the three closest cities.
        """
        distances = [(city, Routing.get_distance(current_city, city, data)) for city in cities if city != current_city]
        distances.sort(key=lambda x: x[1])
        return [city[0] for city in distances[:3]]  # Retrieve only three closest cities

    @staticmethod
    def find_warmest_route(avg_temperatures, start_city="London", end_city="Cape Town"):
        """
        Find the warmest route from the start city to the end city, based on average temperatures.

        Parameters:
        - avg_temperatures (pd.DataFrame): DataFrame with city temperature data, including 'City' and 'AverageTemperature'.
        - start_city (str): Name of the starting city. Default is "London".
        - end_city (str): Name of the destination city. Default is "Cape Town".

        Returns:
        - list: Route from the start city to the end city, considering the warmest cities.
        """
        route = [start_city]
        current_city = start_city
        visited_cities = set()

        max_iterations = 1000
        iteration_count = 0

        while current_city != end_city and iteration_count < max_iterations:
            iteration_count += 1
            visited_cities.add(current_city)

            # Get the three closest cities
            possible_cities = Routing.get_closest_cities(current_city, avg_temperatures['City'].unique(), avg_temperatures)
            possible_cities = [city for city in possible_cities if city not in visited_cities]

            if not possible_cities:
                print("No available next city. Exiting...")
                break

            # From the three closest cities, select the one with the highest temperature
            temperatures = [
                avg_temperatures[avg_temperatures['City'] == city]['AverageTemperature'].values[0] for city in
                possible_cities
            ]
            warmest_city = possible_cities[temperatures.index(max(temperatures))]

            route.append(warmest_city)
            current_city = warmest_city

        return route'''
