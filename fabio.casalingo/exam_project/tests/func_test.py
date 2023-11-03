import pandas as pd
from geopy.distance import great_circle as gc
import exam_project.self_made_functions as func

'''
il piano è quello di far si che partendo da A si calcolino le 3 città più vicine 
e tra queste si scelga quella con la distanza dal punto finalle più corta continuanto fino al raggiungimento della città finale
questo non risolve il problema di andare da londra a londra ma è interessante da implementare
'''

def distance_between_two_cities(start_city,end_city):
    srt_city = dataset[dataset['city'] == start_city]
    des_city = dataset[dataset['city'] == end_city]
    id_des_city = int(des_city['id'].iloc[0])
    end_city_coords = (dataset.loc[dataset['id'] == id_des_city, 'lat'].values[0], dataset.loc[dataset['id'] == des_city, 'lng'].values[0])
    closest_cities[1] = srt_city #potrebbe esssere un problema in caso controllare
    while closest_cities[1]['id'] != id_des_city:
        close_city = func.three_close_city(closest_cities[1])
        first = close_city.iloc[0]
        second = close_city.iloc[1]
        third = close_city.iloc[2]

        close_city['Distance from end'] = close_city.apply(lambda row: gc(end_city_coords, (row['lat'], row['lng'])).kilometers, axis=1)
        sorted_closed_city = close_city.sort_values(by='Distance from destination: ')
        closest_cities = sorted_closed_city.iloc[1]

    return closest_cities