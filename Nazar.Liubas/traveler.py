import pandas as pd
import json
from city import City


class Traveler:
    def __init__(self, path, json_path=None):
        '''

        :param json_path: str, path to Json where ids of cities and their neighbours are saved
        :param path: str
        '''
        self.cities_data = pd.read_excel(path, engine='openpyxl')#.iloc[:10]
        self.cities = {}
        if json_path:
            self.build_city_graph_from_json(json_path)
        else:
            self.build_city_graph()

    def build_city_graph_from_json(self, json_path):
        '''

        :param json_path: str, path to Json where ids of cities and their neighbours are saved
        :return:
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

        :param row: Series, row of DataFrame with cities
        :return: City
        '''
        return City(row['city_ascii'], row['lat'], row['lng'],
                    row['country'], row['population'], row['id'])

    def build_city_graph(self):
        '''

        :return:
        '''
        for index, row in self.cities_data.iterrows():
            city = self.row_to_city(row)
            self.cities[row['id']] = city

        # 'id' is a unique identifier for each city
        ind = 0
        for index, row in self.cities_data.iterrows():
            # TODO delete
            print(ind)
            ind += 1

            current_city = self.cities[row['id']]
            closest_neighbors = self.find_closest_neighbors(current_city, n=4)

            n_closest = 1
            for neighbor_row in closest_neighbors.itertuples(index=False):
                neighbor = self.cities[neighbor_row.id]
                if current_city != neighbor:
                    travel_time = current_city.calc_travel_time(neighbor, n_closest=n_closest)
                    current_city.add_neighbor(neighbor, travel_time)
                    n_closest += 1

    def find_closest_neighbors(self, city, n=4):
        '''

        :param city: City
        :param n: int, number of closest city including the current one
        :return:
        '''
        # TODO optimize
        # Find the n closest neighbors based on latitude and longitude
        distances = self.cities_data.apply(lambda row: city.calculate_distance(self.row_to_city(row)), axis=1)
        closest_neighbors = self.cities_data.iloc[distances.argsort()[:n]]

        return closest_neighbors



# Code for testing
# TODO delete
# x = Traveler('worldcities.xlsx')

# data = pd.read_excel('worldcities.xlsx', engine='openpyxl')
# #London
# source_city_row = data[data['id']==1826645935]
# source_city = City(source_city_row['city_ascii'].iloc[0], source_city_row['lat'].iloc[0],
#                    source_city_row['lng'].iloc[0], source_city_row['country'].iloc[0],
#                    source_city_row['population'].iloc[0], source_city_row['id'].iloc[0])
# print(source_city)

# print(x.find_closest_neighbors(source_city, 4).head())

# Tokyo - 1392685764
# print(x.cities[1826645935].neighbors)
# print(x.cities)
#
# my_dict = {}
# for i in x.cities.keys():
#     my_dict[i] = x.cities[i].neighbors
#
# print(my_dict)
#

# with open('data_full.json', 'w') as json_file:
#     json.dump(my_dict, json_file)