"""
Methods to find different paths through the cities.
"""

import numpy as np
import pandas as pd
from haversine import haversine
import networkx as nx
from networkx import NetworkXNoPath


class TravelGraphRight:

    def __init__(self, df, num_cities=15):
        """
        Initialize the TravelGraphBidirectional class.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing city information.
        num_cities : int, optional
            Number of neighboring cities to consider, by default 30.
        """
        self.df = df

        self.num_cities = num_cities

        self.hav_matrix = self.haversine_matrix()

        self.G = self.create_graph()

        self.add_edges()

    def create_graph(self):
        """
        Create a directed graph to represent the connections between cities.

        Returns
        -------
        nx.DiGraph
            Directed graph representing city connections.
        """

        G = nx.DiGraph()

        for city_id in self.df['id']:
            G.add_node(city_id)
        return G

    def haversine_matrix(self):
        """
        Calculate the Haversine distance matrix between cities.

        Returns
        -------
        pd.DataFrame
            Haversine distance matrix.
        """

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
                                             check=False
                                             )
                    hav_distances[i, j] = hav_distance

        self.hav_matrix = pd.DataFrame(hav_distances, index=self.df['id'], columns=self.df['id'])
        return self.hav_matrix

    def add_edges(self):
        """
        Add edges to the graph based on the Haversine distance between cities.
        """
        for i in range(len(self.hav_matrix)):
            close_city = pd.DataFrame(self.hav_matrix.iloc[i].sort_values())

            lng_start = (self.df.iloc[i]['lng'] + 360) % 360

            total_city = 0
            city_num = 1

            while total_city < (self.num_cities + 1) and city_num < len(close_city.index):
                lng_arrive = (self.df.loc[self.df['id'] == close_city.index[city_num], 'lng'].values[0] + 360) % 360

                if lng_arrive > lng_start and lng_arrive - lng_start < 180:
                    self.G.add_edge(self.df.iloc[i]['id'],
                                    close_city.index[city_num],
                                    weight=close_city.iloc[city_num].values[0])
                    total_city += 1
                    city_num += 1

                elif lng_start > 315 and lng_arrive < 45:
                    self.G.add_edge(self.df.iloc[i]['id'], close_city.index[city_num],
                                    weight=close_city.iloc[city_num].values[0])
                    total_city += 1
                    city_num += 1
                else:
                    city_num += 1

    def farthest_city(self, city_id):
        """
        Find the farthest city based on longitude.

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

        neighbors.sort(key=lambda neighbors_city: (self.df.loc[self.df['id'] == int(neighbors_city), 'lng'].values[0] +
                                                   360) % 360)

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
        try:
            if source_id == target_id:
                close_id = self.farthest_city(source_id)
                short_path = nx.shortest_path(self.G, source=close_id, target=target_id, weight='weight')
                short_path = [source_id] + short_path

            else:
                short_path = nx.shortest_path(self.G, source=source_id, target=target_id, weight='weight')

            for ID in short_path:
                cities_name.append(self.df.loc[self.df['id'] == ID, 'city_ascii'].values[0])

            return cities_name
        except NetworkXNoPath:
            return ["No path found between the specified cities."]

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


class TravelGraphBidirectional(TravelGraphRight):
    def create_graph(self):
        """
        Create an undirected graph to represent the connections between cities.

        Returns
        -------
        nx.Graph
            Undirected graph representing city connections.
        """
        G = nx.Graph()

        for city_id in self.df['id']:
            G.add_node(city_id)
        return G

    def add_edges(self):
        """
        Add edges to the graph based on the Haversine distance between cities.
        """
        for i in range(len(self.hav_matrix)):
            close_city = pd.DataFrame(self.hav_matrix.iloc[i].sort_values())

            for j in range(1, self.num_cities):
                self.G.add_edge(self.df.iloc[i]['id'],
                                close_city.index[j],
                                weight=close_city.iloc[j].values[0]
                                )

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
        try:
            if source_id == target_id:
                raise ValueError("The source and target cities must be different.")

            else:
                short_path = nx.shortest_path(self.G, source=source_id, target=target_id, weight='weight')

            for ID in short_path:
                cities_name.append(self.df.loc[self.df['id'] == ID, 'city_ascii'].values[0])

            return cities_name
        except NetworkXNoPath:
            return ["No path found between the specified cities."]


class TravelGraphLeft(TravelGraphRight):

    def add_edges(self):
        """
        Add edges to the graph based on the Haversine distance between cities.
        """
        for i in range(len(self.hav_matrix)):
            close_city = pd.DataFrame(self.hav_matrix.iloc[i].sort_values())

            lng_start = (self.df.iloc[i]['lng'] + 360) % 360
            total_city = 0
            city_num = 1

            while total_city < (self.num_cities + 1) and city_num < len(close_city.index):
                lng_arrive = (self.df.loc[self.df['id'] == close_city.index[city_num], 'lng'].values[0] + 360) % 360

                if lng_arrive < lng_start and lng_start - lng_arrive < 180:
                    self.G.add_edge(self.df.iloc[i]['id'],
                                    close_city.index[city_num],
                                    weight=close_city.iloc[city_num].values[0])
                    total_city += 1
                    city_num += 1

                elif lng_start < 45 and lng_arrive > 315:
                    self.G.add_edge(self.df.iloc[i]['id'], close_city.index[city_num],
                                    weight=close_city.iloc[city_num].values[0])
                    total_city += 1
                    city_num += 1
                else:
                    city_num += 1
