import pandas as pd
from geopy.distance import great_circle as gc

dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

def three_close_city(input_city):

    city = dataset[dataset['city'] == input_city]  # seleziono il record relativo ad input_city
    id_city = int(city['id'].iloc[0])  # prendo l'id
    #     dataset.loc[dataset['id'] == id_city, 'lat'].values[0] estraggo la latitudine
    #     dataset.loc[dataset['id'] == id_city, 'lng'].values[0] estraggo la longitudine
    city_coords = (dataset.loc[dataset['id'] == id_city, 'lat'].values[0], dataset.loc[dataset['id'] == id_city, 'lng'].values[0])

    # Calculate distances from input_city to all cities in the dataset
    dataset['Distance from start'] = dataset.apply(lambda row: gc(city_coords, (row['lat'], row['lng'])).kilometers, axis=1)

    # Sort the dataset by distance
    sorted_dataset = dataset.sort_values(by='Distance from start')

    # Get the three closest cities
    closest_cities = sorted_dataset.iloc[1:]  # Skip the first row (starting city)
    return closest_cities


def distance_between_two_cities(start_city,end_city):
    srt_city = dataset[dataset['city'] == start_city]
    des_city = dataset[dataset['city'] == end_city]
    id_des_city = int(des_city['id'].iloc[0])
    end_city_coords = (dataset.loc[dataset['id'] == id_des_city, 'lat'].values[0], dataset.loc[dataset['id'] == id_des_city, 'lng'].values[0])
    '''closest_cities = pandas.DataFrame()
       closest_cities[0] = srt_city'''
    closest_cities = srt_city #potrebbe esssere un problema in caso controllare
    while closest_cities['city'].values[0] != id_des_city:
        close_city = three_close_city(closest_cities['city'].values[0])
        '''first = close_city.iloc[0]
        second = close_city.iloc[1]
        third = close_city.iloc[2]'''

        close_city['Distance from end'] = close_city.apply(lambda row: gc(end_city_coords, (row['lat'], row['lng'])).kilometers, axis=1)
        sorted_closed_city = close_city.sort_values(by='Distance from destination: ')
        closest_cities = sorted_closed_city.iloc[0]

    return closest_cities