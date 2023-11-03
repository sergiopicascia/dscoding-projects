import numpy as np
import pandas as pd
from geopy.distance import great_circle as gc
import exam_project.self_made_functions as func

# Load the dataset
dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

start_city = 'Rome'
end_city = 'Milan'

# Find the coordinates of the start and end cities
start_coords = dataset[(dataset['city'] == start_city) & (dataset['admin_name'] == 'Lazio')][['lat', 'lng']].values[0]
end_coords = dataset[(dataset['city'] == end_city) & (dataset['admin_name'] == 'Lombardy')][['lat', 'lng']].values[0]

visited_cities = []
city = start_city
while city != end_city:
    # Get the closest unvisited cities to the destination
    i =3
    unvisited_cities = func.three_close_city(city)[:i][~func.three_close_city(city)['city'].isin(visited_cities)]
    while unvisited_cities.empty:
        i+=1
        unvisited_cities = func.three_close_city(city)[:i][~func.three_close_city(city)['city'].isin(visited_cities)]

    # Calculate distances to the destination for the unvisited cities
    unvisited_cities['Distance to destination'] = unvisited_cities.apply(
        lambda row: gc((row['lat'], row['lng']), end_coords).kilometers, axis=1)

    # Sort by distance and choose the closest unvisited city
    closest_city = unvisited_cities.sort_values(by='Distance to destination').iloc[0]

    # Update the current city and add it to the visited cities list
    city = closest_city['city']
    visited_cities.append(city)

print("Route from {} to {}:".format(start_city, end_city))
for i, visited_city in enumerate(visited_cities):
    print("Step {}: {}".format(i + 1, visited_city))
