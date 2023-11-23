'''
Import all the libraries needed
'''
import pandas as pd
from geopy.distance import great_circle as gc
from math import radians, sin, cos, sqrt, atan2


'''
Creation of the class, the class is actually one because from my point of view the oop wasn't needed for such type of program
'''
class Travel:
    '''
    The inizialization of the class requires the path of the dataset, in this case in set a default value for path for
    '''

    def __init__(self, dataset_path='C:/Uni/Coding/python/worldcities.xlsx'):
        self.dataset = pd.read_excel(dataset_path)

    def __haversine_distance(self, coords1, coords2):
        """
        Calculate the Haversine distance between two sets of geographic coordinates.

        Parameters
        ----------
        coords1: list[]
            The geographic coordinates [latitude, longitude] of the first location.
        coords2: list[]
            The geographic coordinates [latitude, longitude] of the second location.

        Returns
        -------
        distance: float
            The Haversine distance between the two locations in kilometers.
        """
        lat1, lon1 = map(radians, coords1)
        lat2, lon2 = map(radians, coords2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        r = 6371.0

        distance = r * c
        return distance

    def n_close_city(self, input_city_id, n):
        """
        Calculate the n cities closest to the one given in input.

        Parameters
        ----------
        input_city_id: int
            The ID associated to the starting city.
        n: int
            The number of closest cities to select.

        Returns
        -------
        closest_cities: list[]
            A list containaining all the IDs of the n closest cities.
        """
        city_coords = (self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0],
                       self.dataset.loc[self.dataset['id'] == input_city_id, 'lng'].values[0])

        self.dataset['Distance from start'] = self.dataset.apply(
            lambda row: self.__haversine_distance(city_coords, (row['lat'], row['lng'])), axis=1)

        sorted_dataset = self.dataset.sort_values(by='Distance from start')

        closest_cities = sorted_dataset.iloc[1:n]
        return closest_cities

    def distance_between_two_cities(self, start_city, end_city, n):
        """
        Calculate the travel path, considering n cities, for going from start_city to end_city .

        Parameters
        ----------
        start_city: int
            The ID associated to the starting city.
        end_city: int
            The ID associated to the starting city.

        Returns
        -------
        visited_cities: list[]
            A list containaining all the IDs of the visited cities during the travel.
        """
        start_coords = self.dataset[(self.dataset['id'] == start_city)][['lat', 'lng']].values[0]
        end_coords = self.dataset[(self.dataset['id'] == end_city)][['lat', 'lng']].values[0]

        visited_cities = []
        city = start_city
        visited_cities.append(city)
        while city != end_city:
            i = n
            while city in visited_cities:
                un_city = self.n_close_city(city, i)
                un_city['Distance to destination'] = un_city.apply(
                    lambda row: gc((row['lat'], row['lng']), end_coords).kilometers, axis=1)
                for x in range(i):
                    closest_city = un_city.sort_values(by='Distance to destination').iloc[x]
                    if closest_city['id'] not in visited_cities:
                        city = closest_city['id']
                        name = closest_city['city']
                        break
                i += 1
            visited_cities.append(city)
        return visited_cities

    def east(self, input_city_id):
        """
        Calculate the travel path, for going from start_city until turning back to it going only to east .

        Parameters
        ----------
        input_city_id: int
            The ID associated to the starting city.

        Returns
        -------
        visited_cities: list[]
            A list containaining all the IDs of the visited cities during the travel.
        """
        visited_cities = [input_city_id]
        starting_city = input_city_id
        original_dataset = self.dataset.copy()
        city_coords = (
            self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0],
            self.dataset.loc[self.dataset['id'] == input_city_id, 'lng'].values[0]
        )
        self.dataset['Distance from prev'] = self.dataset.apply(
            lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers,
            axis=1)
        self.dataset['Diff_lat'] = abs(
            self.dataset['lat'] - self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0])
        start_coords = city_coords
        next_city_id = 0
        while next_city_id != starting_city:
            east_cities = self.dataset[
                (self.dataset['lng'] > city_coords[1]) &
                (abs(self.dataset['lat'] - self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0]) < 10)
                ]

            if east_cities.empty:
                if city_coords[1] < 0:
                    self.dataset = original_dataset.copy()
                    self.dataset['Distance from prev'] = self.dataset.apply(
                        lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers,
                        axis=1)
                    self.dataset['Diff_lat'] = abs(
                        self.dataset['lat'] - self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0])

                    east_cities = self.dataset[(self.dataset['lng'] > 0) & (abs(
                        self.dataset['lat'] - self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[
                            0]) < 10)]
                    self.dataset = self.dataset[self.dataset['lng'].between(start_coords[1], 180)]
                else:
                    self.dataset = original_dataset.copy()
                    self.dataset['Distance from prev'] = self.dataset.apply(
                        lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers,
                        axis=1)
                    self.dataset['Diff_lat'] = abs(
                        self.dataset['lat'] - self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0])

                    east_cities = self.dataset[(self.dataset['lng'] < 0) & (abs(
                        self.dataset['lat'] - self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[
                            0]) < 40)]
                    self.dataset = self.dataset[self.dataset['lng'].between(-180, start_coords[1])]
                    self.dataset = self.dataset._append(original_dataset[original_dataset['id'] == input_city_id],
                                                        ignore_index=True)

            east_cities = east_cities.sort_values(by='Distance from prev')[:20]
            if start_coords[0] > 70 or start_coords[0] < -30:
                east_cities = east_cities.sort_values(by='Diff_lat')[1:4]
            else:
                east_cities = east_cities.sort_values(by='Diff_lat')[:4]

            if not east_cities.empty:
                next_city_id = east_cities['id'].iloc[0]
            else:
                next_city_id = starting_city

            visited_cities.append(next_city_id)
            city_coords = (
                self.dataset.loc[self.dataset['id'] == next_city_id, 'lat'].values[0],
                self.dataset.loc[self.dataset['id'] == next_city_id, 'lng'].values[0]
            )
        self.dataset = original_dataset
        return visited_cities

    def time(self, visited):
        """
        Calculate the time give a travel path.

        Parameters
        ----------
        visited: list[]
            The IDs associated to a path.

        Returns
        -------
        duration: int
           The time needed to complete the travel path given as input.
        """
        duration = 0
        for i in range(len(visited) - 1):
            a_coords = (
                self.dataset.loc[self.dataset['id'] == visited[i], 'lat'].values[0],
                self.dataset.loc[self.dataset['id'] == visited[i], 'lng'].values[0])
            b_coords = (
                self.dataset.loc[self.dataset['id'] == visited[i + 1], 'lat'].values[0],
                self.dataset.loc[self.dataset['id'] == visited[i + 1], 'lng'].values[0])
            if gc(a_coords, b_coords).kilometers <= 1000:
                duration += 4
            elif 1000 < gc(a_coords, b_coords).kilometers <= 2000:
                duration += 6
            else:
                duration += 8
        return duration