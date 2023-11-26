'''
Module for saving created graph to JSON
'''

from traveler import Traveler
import json

x = Traveler('worldcities.xlsx')

my_dict = {}
for i in x.cities.keys():
    my_dict[i] = x.cities[i].neighbors

print(my_dict)

with open('data_calculated.json', 'w') as json_file:
    json.dump(my_dict, json_file)