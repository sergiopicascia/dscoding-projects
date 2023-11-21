"""
Methods to find different paths through the cities.
"""

import numpy as np
import pandas as pd
from haversine import haversine
import networkx as nx


class TravelGraph:

    def __init__(self, df, num_cities=30, graph_type="bidirectional"):
        """
        Initialize the TravelGraph class.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing city information.
        num_cities : int, optional
            Number of neighboring cities to consider, by default 30.
        graph_type : str, optional
            Type of graph ("right_only", "bidirectional", "left_only"), by default "bidirectional".
        """
        self.graph_type = graph_type
        self.df = df

        coordinates = self.df[['lat', 'lng']].to_numpy()

        hav_distances = np.zeros((len(coordinates), len(coordinates)))
        for i in range(len(coordinates)):
            for j in range(len(coordinates)):
                if i != j:
                    coords1 = coordinates[i]
                    coords2 = coordinates[j]
                    hav_distance = haversine(coords1,
                                             coords2,
                                             normalize=False,
                                             check=False)
                    hav_distances[i, j] = hav_distance

        self.hav_matrix = pd.DataFrame(hav_distances, index=self.df['id'], columns=self.df['id'])

        if graph_type == "right_only":
            self.G = nx.DiGraph()

            for city_id in self.df['id']:
                self.G.add_node(city_id)

            for i in range(len(self.hav_matrix)):
                close_city = pd.DataFrame(self.hav_matrix.iloc[i].sort_values())
                lng_start = (self.df.iloc[i]['lng'] + 360) % 360
                total_city = 0
                city_num = 1
                while total_city < (num_cities + 1):
                    lng_arrive = (self.df.loc[self.df['id'] == close_city.index[city_num], 'lng'].values[0] + 360) % 360

                    if lng_arrive > lng_start:
                        self.G.add_edge(self.df.iloc[i]['id'],
                                        close_city.index[city_num],
                                        weight=close_city.iloc[city_num].values[0])
                        total_city += 1
                        city_num += 1

                    else:
                        if lng_arrive < 90 and lng_start > 270:
                            self.G.add_edge(self.df.iloc[i]['id'], close_city.index[city_num],
                                            weight=close_city.iloc[city_num].values[0])
                            total_city += 1
                            city_num += 1
                        else:
                            city_num += 1

        elif graph_type == "bidirectional":
            self.G = nx.Graph()

            for city_id in self.df['id']:
                self.G.add_node(city_id)

            for i in range(len(self.hav_matrix)):
                close_city = pd.DataFrame(self.hav_matrix.iloc[i].sort_values())
                for j in range(1, num_cities):
                    self.G.add_edge(self.df.iloc[i]['id'], close_city.index[j], weight=close_city.iloc[j].values[0])

        if graph_type == "left_only":
            self.G = nx.DiGraph()

            for city_id in self.df['id']:
                self.G.add_node(city_id)

            for i in range(len(self.hav_matrix)):
                close_city = pd.DataFrame(self.hav_matrix.iloc[i].sort_values())
                lng_start = (self.df.iloc[i]['lng'] + 360) % 360
                total_city = 0
                city_num = 1
                while total_city < (num_cities + 1):
                    lng_arrive = (self.df.loc[self.df['id'] == close_city.index[city_num], 'lng'].values[0] + 360) % 360

                    if lng_arrive < lng_start:
                        self.G.add_edge(self.df.iloc[i]['id'],
                                        close_city.index[city_num],
                                        weight=close_city.iloc[city_num].values[0])
                        total_city += 1
                        city_num += 1

                    else:
                        if lng_start < 90 and lng_arrive > 270:
                            self.G.add_edge(self.df.iloc[i]['id'], close_city.index[city_num],
                                            weight=close_city.iloc[city_num].values[0])
                            total_city += 1
                            city_num += 1
                        else:
                            city_num += 1

        else:
            raise ValueError("Invalid graph_type. Choose 'right_only' or 'bidirectional'.")

    def farthest_city(self, city_id):
        """
        Find the farthest city to the right or left (depends on the structure of the Graph) based on longitude.

        Parameters
        ----------
        city_id : int
            ID of the city.

        Returns
        -------
        int or None
            ID of the farthest city or None if no neighbors.
        """
        neighbors = list(self.G.neighbors(city_id))

        if not neighbors:
            return None

        neighbors.sort(key=lambda x: (self.df.loc[self.df['id'] == x, 'lng'].values[0] + 360) % 360)

        farthest_city = neighbors[-1]

        return farthest_city

    def shortest_path(self, source_city_name, target_city_name):
        """
        Find the shortest path between two cities.

        Parameters
        ----------
        source_city_name : str
            Name of the source city.
        target_city_name : str
            Name of the target city.

        Returns
        -------
        list
            List of city names representing the shortest path.
        """
        cities_name = []

        source_id = self.df.loc[self.df['city_ascii'] == source_city_name, 'id'].values[0]
        target_id = self.df.loc[self.df['city_ascii'] == target_city_name, 'id'].values[0]

        if source_id == target_id and self.graph_type == 'bidirectional':
            close_id = self.farthest_city(source_id)
            short_path = nx.shortest_path(self.G, source=close_id, target=target_id, weight='weight')
            short_path = [source_id] + short_path

        else:
            short_path = nx.shortest_path(self.G, source=source_id, target=target_id, weight='weight')

        for i in short_path:
            cities_name.append(self.df.loc[self.df['id'] == i, 'city_ascii'].values[0])

        return cities_name

    def travel_time(self, path, speed: float):
        """
        Estimate travel time along a given path.

        Parameters
        ----------
        path : list
            List of city names representing the path.
        speed : float
            Travel speed in km/h.

        Returns
        -------
        str
            Estimated travel time.
        """
        base_time = 0
        for city in range(len(path) - 1):
            next_city = path[city + 1]
            starting_city = self.df.loc[self.df['city_ascii'] == path[city], 'id'].values[0]
            arriving_city = self.df.loc[self.df['city_ascii'] == next_city, 'id'].values[0]

            distance = self.hav_matrix.loc[starting_city, arriving_city]
            base_time += distance / speed

            if self.df.loc[self.df['id'] == arriving_city, 'population'].values[0] > 200000:
                base_time += 2

            if (self.df.loc[self.df['id'] == starting_city, 'country'].values[0] !=
                    self.df.loc[self.df['id'] == arriving_city, 'country'].values[0]):
                base_time += 2
        days = int(base_time // 24)
        hour = int(base_time % 24)
        time = f"You need {days} days and {hour} hours to arrive to {path[-1]}."

        return time

    def cycle_tour(self, start_city_name):
        """
        Generate a cycle tour starting from a specified city.

        Parameters
        ----------
        start_city_name : str
            Name of the starting city.

        Returns
        -------
        list
            List of city names representing the cycle tour.
        """
        tour_cities = []

        start_id = self.df.loc[self.df['city_ascii'] == start_city_name, 'id'].values[0]

        cycle_path = nx.approximation.traveling_salesman_problem(self.G, cycle=True)

        start_index = cycle_path.index(start_id)

        tour_path = cycle_path[start_index:] + cycle_path[:start_index]
        for i in tour_path:
            tour_cities.append(self.df.loc[self.df['id'] == i, 'city_ascii'].values[0])

        return tour_cities
