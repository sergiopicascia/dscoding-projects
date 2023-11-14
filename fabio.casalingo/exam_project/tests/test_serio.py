import pandas as pd
from geopy.distance import great_circle as gc
import exam_project.self_made_functions as func

dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

'''close_city = func.three_close_city('Tokyo')
# Display the closest cities
print("Three closest cities to input city:")
for index, city in close_city.iterrows():
    print(city['city'], city['country'], f"{city['Distance from start']:.2f} kilometers")

print(close_city.iloc[0]['city'])

a = func.distance_between_two_cities('Rome','Milan')
print (a['city'].values[0])
'''
'''city_coords1 = (dataset.loc[dataset['id'] == 1392685764, 'lat'].values[0], dataset.loc[dataset['id'] == 1392685764, 'lng'].values[0])
city_coords2 = (dataset.loc[dataset['id'] == 1360771077, 'lat'].values[0], dataset.loc[dataset['id'] == 1360771077, 'lng'].values[0])
a = gc(city_coords1, city_coords2).kilometers
print(a)'''

'''a = dataset.loc[dataset['id'] == 1392685764, 'lat'].values[0]
city = dataset[dataset['id'] == 1392685764]  # seleziono il record relativo ad input_city
id_city = city['lat'].iloc[0]
if a == id_city:
    print('ug')'''

'''# Example usage:
starting_city_id = 1826645935 # Replace with the ID of your starting city
visited_cities = func.east(starting_city_id)
print("Visited cities:", visited_cities)
func.maps(visited_cities)'''

'''a = func.distance_between_two_cities()

func.maps(a)'''
b = func.distance_between_two_cities(1380382862, 1380724377)
print(b)
func.maps(b)
