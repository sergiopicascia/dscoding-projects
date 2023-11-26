import pandas as pd
import json
from city import City


class Traveler:
    '''
    A class that makes a simulation of a travel around the world
    '''

    def __init__(self, path, json_path=None):
        '''
        :param json_path: str, path to Json where ids of cities and their neighbours are saved
        :param path: str, path to excel with data
        '''
        self.cities_data = pd.read_excel(path, engine='openpyxl')
        self.cities = {}
        if json_path:
            self.build_city_graph_from_json(json_path)
        else:
            self.build_city_graph()

    def build_city_graph_from_json(self, json_path):
        '''
        Parses json file with data about neighbours and creates graph of cities
        :param json_path: str, path to Json where ids of cities and their neighbours are saved
        :return: None, creates city graph with closest neighbours
        '''
        with open(json_path, 'r') as json_file:
            loaded_data = json.load(json_file)
        for value in loaded_data.keys():
            row_curr_city = self.cities_data[self.cities_data['id'] == int(value)].iloc[0]
            curr_city = self.row_to_city(row_curr_city)
            for neighbour in loaded_data[value]:
                neighbour_city_row = self.cities_data[self.cities_data['id'] == neighbour['city']].iloc[0]
                neighbour_city = self.row_to_city(neighbour_city_row)
                curr_city.add_neighbor(neighbour_city, neighbour['travel_time'])
            self.cities[int(value)] = curr_city

    def row_to_city(self, row):
        '''
        Creates a city object from a line on original dataframe
        :param row: Series, row of DataFrame with cities
        :return: City
        '''
        return City(row['city_ascii'], row['lat'], row['lng'],
                    row['country'], row['population'], row['id'])

    def build_city_graph(self):
        '''
        Creates a graph of cities, where each city has linked 3 closest neighbours and time to get there
        :return:
        '''
        for index, row in self.cities_data.iterrows():
            city = self.row_to_city(row)
            self.cities[row['id']] = city

        # 'id' is a unique identifier for each city
        for index, row in self.cities_data.iterrows():
            current_city = self.cities[row['id']]
            closest_neighbors = self.find_closest_neighbors(current_city, n=3)
            n_closest = 1
            for neighbor_row in closest_neighbors.itertuples(index=False):
                neighbor = self.cities[neighbor_row.id]
                if current_city != neighbor:
                    travel_time = current_city.calc_travel_time(neighbor, n_closest=n_closest)
                    current_city.add_neighbor(neighbor, travel_time)
                    n_closest += 1

    def find_closest_neighbors(self, city, n=3):
        '''
        Finds an n closest eastern neighbours to the given city and returns dataframe with n lines
        :param city: City
        :param n: int, number of closest cities
        :return: pd.DataFrame
        '''
        # applying a logic that we can only move to east;
        # assuming that there will not be any closest cities farer away than 30 longitude and +- 20 latitude
        lat_shift = 25
        long_shift = 30
        if city.longitude > 150:
            filter_condition = (
                    ((self.cities_data['lng'] > city.longitude) &
                     (self.cities_data['lng'] > city.longitude + long_shift)) |
                    ((self.cities_data['lng'] > -180) &
                     (self.cities_data['lng'] < -150))
            )
        else:
            filter_condition = (self.cities_data['lng'] > city.longitude) & \
                               (self.cities_data['lng'] < city.longitude + long_shift)
        filter_condition = filter_condition & ((self.cities_data['lng'] < city.latitude + lat_shift) |
                                               (self.cities_data['lng'] > city.latitude - lat_shift))
        temp_df = self.cities_data[filter_condition]
        # Find the n closest neighbors based on latitude and longitude
        distances = temp_df.apply(lambda row: city.calculate_distance(self.row_to_city(row)), axis=1)
        closest_neighbors = temp_df.iloc[distances.argsort()[:n]]
        return closest_neighbors

    def travel_around_world(self, current_city, hours_left, path, total_distance):
        '''
        Recursive function that finds a way to around the world to reach current city
        :param current_city: City
        :param hours_left: int
        :param path: list
        :param total_distance: int
        :return:
        '''
        # Stop if we made a circle over the earth
        if current_city.longitude >= -0.1275 and current_city.longitude < 0.6 and hours_left < 500 * 24 - 400:
            return path, total_distance
        if current_city == self.start_city and len(path) > 1:
            # Return to start
            return path, total_distance
        min_path = None
        for neighbor in current_city.neighbors:
            next_city = self.cities[neighbor['city'].id]
            distance = neighbor['travel_time']
            if next_city not in path:
                new_path = path + [next_city]
                new_distance = total_distance + distance
                result = self.travel_around_world(next_city, hours_left - distance, new_path, new_distance)
                if result and (min_path is None or result[1] < min_path[1]):
                    min_path = result
                # Returning the first good enough result. Can be connected if need really best result
                if result:
                    break
        return min_path

    def start_travel(self, start_city):
        '''
        Starts a travel around world from the given city
        :param start_city: City
        :return:
        '''
        self.start_city = start_city
        initial_path = [start_city]
        initial_distance = 0
        # Give enough time for travel
        result = self.travel_around_world(start_city, 500 * 24, initial_path, initial_distance)
        if result:
            return result
        else:
            return "It's not possible to travel around the world in 80 days."
