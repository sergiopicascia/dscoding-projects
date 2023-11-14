import random
import pandas as pd
from geopy.distance import great_circle as gc
import folium
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import random

dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

def three_close_city(input_city_id,n):
    city = dataset[dataset['id'] == input_city_id]
    id_city = int(city['id'].iloc[0])
    city_coords = (dataset.loc[dataset['id'] == id_city, 'lat'].values[0], dataset.loc[dataset['id'] == id_city, 'lng'].values[0])

    dataset['Distance from start'] = dataset.apply(lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers, axis=1)

    sorted_dataset = dataset.sort_values(by='Distance from start')

    closest_cities = sorted_dataset.iloc[1:n]
    return closest_cities


def distance_between_two_cities(start_city,end_city,n):

        start_coords = dataset[(dataset['id'] == start_city)][['lat', 'lng']].values[0]
        end_coords = dataset[(dataset['id'] == end_city)][['lat', 'lng']].values[0]

        visited_cities = []
        city = start_city
        visited_cities.append(city)
        while city != end_city:
            i = n
            while city in visited_cities:
                un_city = three_close_city(city,i)
                un_city['Distance to destination'] = un_city.apply(
                    lambda row: gc((row['lat'], row['lng']), end_coords).kilometers, axis=1)
                for x in range(i):
                    closest_city = un_city.sort_values(by='Distance to destination').iloc[x]
                    if closest_city['id'] not in visited_cities:
                        city = closest_city['id']
                        name = closest_city['city']
                        #j = 0
                        break
                i += 1
            visited_cities.append(city)
        return visited_cities

def maps(visit):
    zoom = dataset[(dataset['id'] == visit[0])][['lat', 'lng']].values[0] #errore
    mappa = folium.Map(location = zoom,zoom_start = 2)
    icon_url = 'https://www.pngall.com/wp-content/uploads/2017/05/Map-Marker-Free-Download-PNG.png'
    #mappa = folium.Map(location=[45.5236, -122.6750], zoom_start=0)
    folium.TileLayer('cartodbdark_matter').add_to(mappa)
    for i in range(len(visit)):
        s = dataset[(dataset['id'] == visit[i])][['lat', 'lng']].values[0]
        #if i > 0 and i < (len (visit) - 1):
            #s2 = dataset[(dataset['id'] == visit[i + 1])][['lat', 'lng']].values[0]
        folium.Marker(s,icon=folium.CustomIcon(icon_image=icon_url,icon_size=(25,25)),popup = dataset[(dataset['id'] == visit[i])][['city']].values[0]).add_to(mappa)
    locations = [(dataset.loc[dataset['id'] == visit[j], ['lat', 'lng']].values[0]) for j in range(len(visit))]
    line = folium.PolyLine(locations=locations,
                           color='orange',  # Colore della linea
                           weight=6,  # Spessore della linea
                           opacity=0.3  # Opacità della linea
                           )
    line.add_to(mappa)
    mappa.save('mappa.html')
    return mappa

def east(input_city_id):
    visited_cities = [input_city_id]
    starting_city = input_city_id
    city_coords = (dataset.loc[dataset['id'] == input_city_id, 'lat'].values[0],
                   dataset.loc[dataset['id'] == input_city_id, 'lng'].values[0])
    start_coords = city_coords
    next_city_id= 0
    x = 0
    while next_city_id != starting_city:
        dataset['Distance from prev'] = dataset.apply(lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers,
                                                       axis=1)
        dataset['Distance from start'] = dataset.apply(lambda row: gc(start_coords, (row['lat'], row['lng'])).kilometers,
                                                     axis=1)
        dataset['Diff_lat'] = abs(dataset['lat'] - dataset.loc[dataset['id'] == input_city_id, 'lat'].values[0])

        if city_coords[1] > 0:
            if gc(city_coords, start_coords).kilometers < 150 and len(visited_cities) > 60 :
                visited_cities.append(starting_city)
                next_city_id = starting_city
                break
            east_cities = dataset[(dataset['lng'] > city_coords[1])]#[:20] #20 #mod

            east_cities =  east_cities.sort_values(by='Distance from prev')[:5] #NEW
            if east_cities.empty:
                # far partire una divesa logica
                westernmost_city = dataset[dataset['lng'] == dataset['lng'].min()]
                closest_city = westernmost_city.iloc[0]
            else:
                # Sort the east cities by distance
                if (east_cities['lat'].iloc[0], east_cities['lng'].iloc[0]) != start_coords:
                    east_cities = east_cities.sort_values(by='Diff_lat')
                # Get the closest city to the east
                closest_city = east_cities.iloc[0]
        else:
            east_cities = dataset[(dataset['lng'] > city_coords[1]) & (dataset['lng'] < 0)]#[:20] #mod

            east_cities = east_cities.sort_values(by='Distance from prev')[:5] #NEW

            if east_cities.empty:
                east_cities = dataset[(dataset['lng'] > city_coords[1])]  # 20
                east_cities = east_cities.sort_values(by='Distance from prev')[:5]  # NEW
            if(east_cities['lat'].iloc[0], east_cities['lng'].iloc[0]) != start_coords:
                east_cities = east_cities.sort_values(by='Distance from start')[:5]
            closest_city = east_cities.iloc[0]

        next_city_id = closest_city['id']
        visited_cities.append(next_city_id)
        if -17.4572 <= start_coords[1] <= 1.484 and start_coords[0] < 49.6504 and -60.4467 <= closest_city['lng'] <= -52.7333:
            city_coords = (dataset.loc[dataset['id'] == 1620177495, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1620177495, 'lng'].values[0])
        elif -9.6962 <= start_coords[1] <= -1.9025 and start_coords[0] > 49.6504 and -60.4467 <= closest_city['lng'] <= -52.7333:
            city_coords = (dataset.loc[dataset['id'] == 1372403494, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1372403494, 'lng'].values[0])
        elif 16.5033 <= start_coords[1] <= 49.18 and start_coords[0] < 12.0 and -60.4467 <= closest_city['lng'] <= -52.7333:
            visited_cities.append(1076697777)
            city_coords = (dataset.loc[dataset['id'] == 1024669127, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1024669127, 'lng'].values[0])
        elif 92.75 <= start_coords[1] <= 133.6667 and -12.6167 < start_coords[0] < 9.2833 and 79.826 <= closest_city['lng'] <= 81.7:
            city_coords = (dataset.loc[dataset['id'] == 1360353144, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1360353144, 'lng'].values[0])
        elif 92.75 <= start_coords[1] <= 133.6667 and start_coords[0] < -12.6167 and 79.826 <= closest_city['lng'] <= 81.7:
            city_coords = (dataset.loc[dataset['id'] == 1036561011, 'lat'].values[0],
                           dataset.loc[dataset['id'] == 1036561011, 'lng'].values[0])
        else:
            city_coords = (closest_city['lat'], closest_city['lng'])
    maps(visited_cities)
    return visited_cities

def time(visited):
    duration = 0
    for i in range(len(visited)-1):
        a_coords = (dataset.loc[dataset['id'] == visited[i], 'lat'].values[0], dataset.loc[dataset['id'] == visited[i], 'lng'].values[0])
        b_coords = (dataset.loc[dataset['id'] == visited[i+1], 'lat'].values[0], dataset.loc[dataset['id'] == visited[i+1], 'lng'].values[0])
        if gc(a_coords, b_coords).kilometers <= 1000:
            duration+=4
        elif 1000 < gc(a_coords, b_coords).kilometers <= 2000:
            duration+=6
        else:
            duration+=8
    return duration

def map_test(visit):
    coordinates = []
    for i in range(len(visit)):
        coordinates.append(dataset[(dataset['id'] == visit[i])][['lat', 'lng']].values[0])
    path = go.Scattergeo(
        locationmode="ISO-3",
        lon=[coord[1] for coord in coordinates],
        lat=[coord[0] for coord in coordinates],
        mode="lines+markers",
        line=dict(width=2, color="blue"),
        marker=dict(size=8, color="red")
    )

    # Create a layout for the globe with orthographic projection
    layout = go.Layout(
        geo=dict(
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
            projection=dict(
                type="orthographic"  # Utilizza la proiezione ortografica
            )
        )
    )

    # Creare una figura
    fig = go.Figure(data=[path], layout=layout)
    fig.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    # Mostrare la mappa con il percorso
    fig.show()



