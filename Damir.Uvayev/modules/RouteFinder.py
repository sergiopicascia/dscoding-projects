from modules.utils import convert_to_decimal
from geopy.distance import great_circle


class RouteFinder:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def get_closest_cities(current_city, all_cities, merged_data, limit=3):
        current_city_data = merged_data[merged_data['City'] == current_city]
        if current_city_data.empty:
            return []

       
        current_lat = convert_to_decimal(current_city_data.iloc[0]['Latitude'])
        current_lon = convert_to_decimal(current_city_data.iloc[0]['Longitude'])
        current_city_coords = (current_lat, current_lon)

        distances = []
        for city in all_cities:
            if city == current_city:
                continue
            city_data = merged_data[merged_data['City'] == city]
            if city_data.empty:
                continue

           
            city_lat = convert_to_decimal(city_data.iloc[0]['Latitude'])
            city_lon = convert_to_decimal(city_data.iloc[0]['Longitude'])
            city_coords = (city_lat, city_lon)

            distance = great_circle(current_city_coords, city_coords).km
            distances.append((city, distance))

        
        closest_cities = sorted(distances, key=lambda x: x[1])[:limit]
        return [city for city, _ in closest_cities]

    @staticmethod
    def get_warmest_city(cities, merged_data):
        warmest_city = None
        highest_avg_temp = -float('inf')

        for city in cities:
            city_data = merged_data[merged_data['City'] == city]
            if city_data.empty:
                continue
            avg_temp = city_data.iloc[0]['AverageTemperature']
            if avg_temp > highest_avg_temp:
                highest_avg_temp = avg_temp
                warmest_city = city

        return warmest_city

    def find_warmest_route(self, merged_data, start_city, end_city):
        route = [start_city]
        current_city = start_city
        visited_cities = set()

        max_iterations = 1000
        iteration_count = 0

        while current_city != end_city and iteration_count < max_iterations:
            iteration_count += 1
            visited_cities.add(current_city)

            
            all_cities = merged_data['City'].unique().tolist()
            closest_cities = self.get_closest_cities(current_city, all_cities, merged_data, limit=3)
            closest_cities = [city for city in closest_cities if city not in visited_cities]

            if not closest_cities:
                print("No available next city. Exiting...")
                break

            
            warmest_city = self.get_warmest_city(closest_cities, merged_data)

            if warmest_city:
                route.append(warmest_city)
                current_city = warmest_city
            else:
                break

        return route
