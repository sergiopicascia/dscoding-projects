import pandas as pd
from math import cos, asin, sqrt, pi

"""
-- Documentation --
    This class is used to plan the "best" route according to the terms
"""


class RoutePlanner:
    def __init__(self, data_file):
        """
        Initialize RoutePlanner object.
        :param data_file: input dataset
        """
        self.data = self._read_data(data_file)
        self.path = []

    def _read_data(self, file):
        """
        Reading dataset and updating coordinates from string to float for plan_route()
        :param file: input dataset
        :return: returns the data with updated coordinates
        """
        df = pd.read_csv(file)
        specific_data = df[(df['dt'] >= '2010-02-01') & (df['dt'] <= '2010-02-31')]
        data = specific_data.values.tolist()

        # converting all the city coordinates
        for city in data:
            city[5] = self._convert_coordinates(city[5])
            city[6] = self._convert_coordinates(city[6])

        return data

    def _convert_coordinates(self, coord_str):
        """
        Converting coordinates from string to float
        :param coord_str: input coordinates
        :return: returns coordinates in float in order to use it in plan_route()
        """
        if coord_str is not None:
            if 'N' in coord_str or 'E' in coord_str:
                return float(coord_str[:-1])
            elif 'S' in coord_str or 'W' in coord_str:
                return -float(coord_str[:-1])
            else:
                return float(coord_str)
        else:
            return None

    def distance(self, lat1, lon1, lat2, lon2):
        """
        Calculates distance given latitude and longitude
        :param lat1: latitude first city
        :param lon1: longitude first city
        :param lat2: latitude second city
        :param lon2: longitude second city
        :return: distance between two cities
        """
        r = 6371  # km
        p = pi / 180

        a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        return 2 * r * asin(sqrt(a))

    def present(self, city, path):
        """
        Checks presence of a city in the path, so it avoids redundant cities and infinite loop
        excludes the city already visited
        :param city: city to check
        :param path: path already done until this point
        :return: boolean value --> True = present, False = not present
        """

        # Searching in the path if the city I want to go was already visited
        for x in path:
            # Checks the name of the city
            if city[3] == x[3]:
                return True
        return False

    def plan_route(self, start_city, end_city):
        """
        Plans the route according to the terms: search the first 3 closest cities and pick the most
        heated one among all --> does the same until destination arrival
        :param start_city: starting point
        :param end_city: ending point
        :return: best route to follow
        """

        # Default path is nothing
        self.path = []
        # Putting country as the starting city
        # I need to update it every time I visit another city
        country = start_city
        # Appends the city the first time so now I have path = [start_city]
        self.path.append(country)

        while country[3] != end_city:
            # index for searching the three closest cities
            j = 0
            # initializing as default values
            # container for the 3 closest cities
            three_closest = [0, 0, 0]
            while j < 3:
                # setting min_dist to default value
                min_dist = 10000000
                for city in self.data:
                    # I consider only non visited cities --> saving time
                    if not self.present(city, self.path):
                        # calculates distance between the current city and the ref country
                        dist = self.distance(country[5], country[6], city[5], city[6])
                        # checks if the distance is less than the current min
                        if dist < min_dist and (city not in three_closest):
                            # updates the values and appends to the three_closest
                            min_dist = dist
                            three_closest[j] = city

                j += 1

            # I have now the three closest cities
            # chooses the warmest one
            max_city = three_closest[0]
            for c in three_closest:
                # finds the warmest city
                if c[1] > max_city[1]:
                    max_city = c

            # appends to the path my new city
            self.path.append(max_city)
            # updates the ref value to this new city
            country = max_city

        return self.path

    def print_route(self):
        """
        Prints the route to dislay
        :return: nothing
        """
        print("Planning the route...")
        for x in self.path:
            print(x[3], ',', x[4])
