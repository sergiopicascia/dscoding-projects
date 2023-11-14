import numpy as np
import pandas as pd
from geopy.distance import great_circle as gc
import exam_project.self_made_functions as func

# Load the dataset
dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

s = dataset[dataset['id'] == 1380382862]
start_city = int(s['id'].iloc[0])
e = dataset[dataset['id'] == 1036074917]
end_city = int(e['id'].iloc[0])

# Find the coordinates of the start and end cities
start_coords = dataset[(dataset['id'] == start_city)][['lat', 'lng']].values[0]
end_coords = dataset[(dataset['id'] == end_city)][['lat', 'lng']].values[0]

visited_cities = []
city = start_city
visited_cities.append(city)
while city != end_city:
    '''
    # Get the closest unvisited cities to the destination
    i =3
    if 
    unvisited_cities = func.three_close_city(city)[:i][~func.three_close_city(city)['city'].isin(visited_cities)]
    print(unvisited_cities)
    while unvisited_cities.empty:
        i+=1
        unvisited_cities = func.three_close_city(city)[:i][~func.three_close_city(city)['city'].isin(visited_cities)]
        print(unvisited_cities)
        '''
    i=20
    j=0
    while city in visited_cities:
        un_city =  func.three_close_city(city)[j : i]
        un_city['Distance to destination'] = un_city.apply(
            lambda row: gc((row['lat'], row['lng']), end_coords).kilometers, axis=1)
        #print('Un_City', un_city['city'])
        j=i
        for x in range(i):
            closest_city = un_city.sort_values(by='Distance to destination').iloc[x]
            #print("CLOSEST: ",closest_city['city'])
            if closest_city['id'] not in visited_cities:
                city = closest_city['id']
                name = closest_city['city']
                j=0
                break
        #print(un_city)
        #print(city)
        #if closest_city['city'] not in visited_cities:
        #else:
        #print(closest_city['city'])
        #245
        i += 1
    print(name)
    visited_cities.append(city)
    '''# Calculate distances to the destination for the unvisited cities
    unvisited_cities['Distance to destination'] = unvisited_cities.apply(
        lambda row: gc((row['lat'], row['lng']), end_coords).kilometers, axis=1)

    # Sort by distance and choose the closest unvisited city
    closest_city = unvisited_cities.sort_values(by='Distance to destination').iloc[0]
'''

print("Route from {} to {}:".format(start_city, end_city))
for i, visited_city in enumerate(visited_cities):
    print("Step {}: {}".format(i + 1, visited_city))
