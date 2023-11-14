'''
Import all the libraries needed
'''
import random
import pandas as pd
from geopy.distance import great_circle as gc
import folium
import streamlit as st
import plotly.graph_objects as go

'''
Creation of the class, the class is actually one because from my point of view the oop wasn't needed for such type of program
'''
class Travel:
    '''
    The inizialization of the class requires the path of the dataset, in this case in set a default value for path for
    '''
    def __init__(self, dataset_path='C:/Uni/Coding/python/worldcities.xlsx'):
        self.dataset = pd.read_excel(dataset_path)

    '''
    Given a city ID and a value 'n', this function returns the 'n' closest cities to the input city.
    '''
    def n_close_city(self, input_city_id, n):
        city = self.dataset[self.dataset['id'] == input_city_id]
        id_city = int(city['id'].iloc[0])
        city_coords = (self.dataset.loc[self.dataset['id'] == id_city, 'lat'].values[0],
                       self.dataset.loc[self.dataset['id'] == id_city, 'lng'].values[0])

        self.dataset['Distance from start'] = self.dataset.apply(
            lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers, axis=1)

        sorted_dataset = self.dataset.sort_values(by='Distance from start')

        closest_cities = sorted_dataset.iloc[1:n]
        return closest_cities

    '''
    Given a start city, end city, and a value 'n', this function calculates the shortest path between the two cities.
    '''
    def distance_between_two_cities(self, start_city, end_city, n):
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

    '''
     Given a starting city, this function calculates the eastward path until it return to the starting city.
    '''
    def east(self, input_city_id):
        visited_cities = [input_city_id]
        starting_city = input_city_id
        city_coords = (self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0],
                       self.dataset.loc[self.dataset['id'] == input_city_id, 'lng'].values[0])
        start_coords = city_coords
        next_city_id = 0
        x = 0
        while next_city_id != starting_city:
            self.dataset['Distance from prev'] = self.dataset.apply(lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers,
                                                                    axis=1)
            self.dataset['Distance from start'] = self.dataset.apply(
                lambda row: gc(start_coords, (row['lat'], row['lng'])).kilometers,
                axis=1)
            self.dataset['Diff_lat'] = abs(self.dataset['lat'] - self.dataset.loc[self.dataset['id'] == input_city_id, 'lat'].values[0])

            if city_coords[1] > 0:
                if gc(city_coords, start_coords).kilometers < 150 and len(visited_cities) > 60:
                    visited_cities.append(starting_city)
                    next_city_id = starting_city
                    break
                east_cities = self.dataset[(self.dataset['lng'] > city_coords[1])]

                east_cities = east_cities.sort_values(by='Distance from prev')[:5]
                if east_cities.empty:
                    # far partire una diversa logica
                    westernmost_city = self.dataset[self.dataset['lng'] == self.dataset['lng'].min()]
                    closest_city = westernmost_city.iloc[0]
                else:
                    # Sort the east cities by distance
                    if (east_cities['lat'].iloc[0], east_cities['lng'].iloc[0]) != start_coords:
                        east_cities = east_cities.sort_values(by='Diff_lat')
                    # Get the closest city to the east
                    closest_city = east_cities.iloc[0]
            else:
                east_cities = self.dataset[(self.dataset['lng'] > city_coords[1]) & (self.dataset['lng'] < 0)]

                east_cities = east_cities.sort_values(by='Distance from prev')[:5]

                if east_cities.empty:
                    east_cities = self.dataset[(self.dataset['lng'] > city_coords[1])]
                    east_cities = east_cities.sort_values(by='Distance from prev')[:5]
                if (east_cities['lat'].iloc[0], east_cities['lng'].iloc[0]) != start_coords:
                    east_cities = east_cities.sort_values(by='Distance from start')[:5]
                closest_city = east_cities.iloc[0]

            next_city_id = closest_city['id']
            visited_cities.append(next_city_id)
            if -17.4572 <= start_coords[1] <= 1.484 and start_coords[0] < 49.6504 and -60.4467 <= closest_city['lng'] <= -52.7333:
                city_coords = (self.dataset.loc[self.dataset['id'] == 1620177495, 'lat'].values[0],
                               self.dataset.loc[self.dataset['id'] == 1620177495, 'lng'].values[0])
            elif -9.6962 <= start_coords[1] <= -1.9025 and start_coords[0] > 49.6504 and -60.4467 <= closest_city['lng'] <= -52.7333:
                city_coords = (self.dataset.loc[self.dataset['id'] == 1372403494, 'lat'].values[0],
                               self.dataset.loc[self.dataset['id'] == 1372403494, 'lng'].values[0])
            elif 16.5033 <= start_coords[1] <= 49.18 and start_coords[0] < 12.0 and -60.4467 <= closest_city[
                'lng'] <= -52.7333:
                visited_cities.append(1076697777)
                city_coords = (self.dataset.loc[self.dataset['id'] == 1024669127, 'lat'].values[0],
                               self.dataset.loc[self.dataset['id'] == 1024669127, 'lng'].values[0])
            elif 92.75 <= start_coords[1] <= 133.6667 and -12.6167 < start_coords[0] < 9.2833 and 79.826 <= \
                    closest_city['lng'] <= 81.7:
                city_coords = (self.dataset.loc[self.dataset['id'] == 1360353144, 'lat'].values[0],
                               self.dataset.loc[self.dataset['id'] == 1360353144, 'lng'].values[0])
            elif 92.75 <= start_coords[1] <= 133.6667 and start_coords[0] < -12.6167 and 79.826 <= closest_city[
                'lng'] <= 81.7:
                city_coords = (self.dataset.loc[self.dataset['id'] == 1036561011, 'lat'].values[0],
                               self.dataset.loc[self.dataset['id'] == 1036561011, 'lng'].values[0])
            else:
                city_coords = (closest_city['lat'], closest_city['lng'])
        return visited_cities

    '''
    Given a list of visited cities, this function calculates the total time of the journey based on distance.
    '''
    def time(self, visited):
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

    '''
    Given a list of visited cities, this function creates a 2D map with markers and a line connecting them.
    '''
    def map_2d(self, visit):
        zoom = self.dataset[(self.dataset['id'] == visit[0])][['lat', 'lng']].values[0]
        mappa = folium.Map(location=zoom, zoom_start=2)
        icon_url = 'C:/Uni/Coding/python/exam_project/Map-Marker-Free-Download-PNG.png'
        folium.TileLayer('cartodbdark_matter').add_to(mappa)
        for i in range(len(visit)):
            s = self.dataset[(self.dataset['id'] == visit[i])][['lat', 'lng']].values[0]
            folium.Marker(s, icon=folium.CustomIcon(icon_image=icon_url, icon_size=(25, 25)),
                          popup=self.dataset[(self.dataset['id'] == visit[i])][['city']].values[0]).add_to(mappa)
        locations = [(self.dataset.loc[self.dataset['id'] == visit[j], ['lat', 'lng']].values[0]) for j in
                     range(len(visit))]
        line = folium.PolyLine(locations=locations,
                               color='orange',
                               weight=6,
                               opacity=0.3
                               )
        line.add_to(mappa)
        mappa.save('mappa.html')
        return mappa

    '''
    Given a list of visited cities, this function creates a 3D map with lines connecting them on a globe.
    '''
    def map_3d(self, visit):

        coordinates = [self.dataset.loc[self.dataset['id'] == city_id, ['lat', 'lng', 'city']].iloc[0] for city_id in visit]

        path = go.Scattergeo(
            lon=[coord['lng'] for coord in coordinates],
            lat=[coord['lat'] for coord in coordinates],
            mode="lines+markers",
            line=dict(width=2, color="black"),
            marker=dict(size=8,
            color=["orange" if i == 0 else "red" if i == len(coordinates) - 1 else " #ffb84d" for i in range(len(coordinates))]),
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