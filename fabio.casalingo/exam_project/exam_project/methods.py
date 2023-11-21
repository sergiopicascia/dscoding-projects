'''
Import all the libraries needed
'''
import random
import pandas as pd
from geopy.distance import great_circle as gc
import folium
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
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

    def haversine_distance(self, coords1, coords2):
        # Calcola la distanza tra due coordinate utilizzando la formula di Haversine
        lat1, lon1 = map(radians, coords1)
        lat2, lon2 = map(radians, coords2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Raggio medio della Terra in chilometri (approssimato)
        r = 6371.0

        distance = r * c
        return distance

    # Aggiorna il metodo n_close_city per utilizzare la formula di Haversine
    def n_close_city(self, input_city_id, n):
        city_coords = (self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0],
                       self.dataset.loc[self.dataset['id'] == input_city_id, 'lng'].values[0])

        self.dataset['Distance from start'] = self.dataset.apply(
            lambda row: self.haversine_distance(city_coords, (row['lat'], row['lng'])), axis=1)

        sorted_dataset = self.dataset.sort_values(by='Distance from start')

        closest_cities = sorted_dataset.iloc[1:n]
        return closest_cities

    '''def n_close_city(self, input_city_id, n):
        """
        Calculate the n cities closest to the one given in input.

        Parameters
        ----------
        input_city_id: int
            The ID associated to the starting city.
        n: int
            The numbrer of closest cities to select.

        Returns
        -------
        closest_cities: list[]
            A list containaining all the IDs of the n closest cities.
        """
        city = self.dataset[self.dataset['id'] == input_city_id]
        id_city = int(city['id'].iloc[0])
        city_coords = (self.dataset.loc[self.dataset['id'] == id_city, 'lat'].values[0],
                       self.dataset.loc[self.dataset['id'] == id_city, 'lng'].values[0])

        self.dataset['Distance from start'] = self.dataset.apply(
            lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers, axis=1)

        sorted_dataset = self.dataset.sort_values(by='Distance from start')

        closest_cities = sorted_dataset.iloc[1:n]
        return closest_cities'''

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
                    self.dataset = self.dataset[self.dataset['lng'].between(city_coords[1], 180)]
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
                    self.dataset = self.dataset[self.dataset['lng'].between(-180, 0)]
                    self.dataset = self.dataset._append(original_dataset[original_dataset['id'] == input_city_id], ignore_index=True)

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

class MapHandler:
    def __init__(self, dataset_path='C:/Uni/Coding/python/worldcities.xlsx'):
        self.dataset = pd.read_excel(dataset_path)

    def map_2d(self, visit):
        """
        Show with a 2d map the path of the input travel path.

        Parameters
        ----------
        visit: list[]
            The IDs associated to the cities visited in the travel path.

        Returns
        -------
        map: folium.folium.Map
            A folium map containing the graphical travel path.
        """
        zoom = self.dataset[(self.dataset['id'] == visit[0])][['lat', 'lng']].values[0]
        map = folium.Map(location=zoom, zoom_start=2)
        icon_url = 'C:/Uni/Coding/python/exam_project/Map-Marker-Free-Download-PNG.png'
        folium.TileLayer('cartodbdark_matter').add_to(map)
        for i in range(len(visit)):
            s = self.dataset[(self.dataset['id'] == visit[i])][['lat', 'lng']].values[0]
            folium.Marker(s, icon=folium.CustomIcon(icon_image=icon_url, icon_size=(25, 25)),
                          popup=self.dataset[(self.dataset['id'] == visit[i])][['city']].values[0]).add_to(map)
        locations = [(self.dataset.loc[self.dataset['id'] == visit[j], ['lat', 'lng']].values[0]) for j in
                     range(len(visit))]
        line = folium.PolyLine(locations=locations,
                               color='orange',
                               weight=6,
                               opacity=0.3
                               )
        line.add_to(map)
        map.save('mappa.html')
        return map

    def map_3d(self, visit):
        """
        Show with a 3d map the path of the input travel path.

        Parameters
        ----------
        visit: list[]
            The IDs associated to the cities visited in the travel path.

        Returns
        -------
        fig: plotly.graph_objs.Figure
            A 3d map that show the travel path.
        """
        coordinates = [self.dataset.loc[self.dataset['id'] == city_id, ['lat', 'lng', 'city']].iloc[0] for city_id in
                       visit]

        path = go.Scattergeo(
            lon=[coord['lng'] for coord in coordinates],
            lat=[coord['lat'] for coord in coordinates],
            mode="lines+markers",
            line=dict(width=2, color="black"),
            marker=dict(size=8,
                        color=["orange" if i == 0 else "red" if i == len(coordinates) - 1 else " #ffb84d" for i in
                               range(len(coordinates))]),
            text=[f"City: {coord['city']}" for coord in coordinates]
        )

        layout = go.Layout(
            geo=dict(
                showland=True,
                showocean=True,
                landcolor="#267326",
                countrycolor="rgb(0, 0, 0)",
                oceancolor="#80bfff",
                projection=dict(
                    type="orthographic"
                )
            )
        )

        fig = go.Figure(data=[path], layout=layout)

        fig.update_layout(
            title_text='Path on 3D Globe',
            title_x=0.5,
            title_font=dict(size=20),
            title_xanchor='center'
        )

        fig.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig.show()
        return fig

    def population(self,dataset):
        df = dataset.groupby('iso3')['population'].sum().reset_index()
        df
        fig = px.choropleth(df,
                            locations='iso3',
                            color='population',
                            hover_name='iso3',
                            projection='natural earth',
                            range_color=(0, 155000000),
                            title='Population distribution',
                            color_continuous_scale='Viridis')

        fig.show()



