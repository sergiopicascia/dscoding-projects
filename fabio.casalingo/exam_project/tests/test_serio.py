import pandas as pd
from geopy.distance import great_circle as gc
import exam_project.self_made_functions as func

dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

close_city = func.three_close_city('Tokyo')
# Display the closest cities
print("Three closest cities to input city:")
for index, city in close_city.iterrows():
    print(city['city'], city['country'], f"{city['Distance from start']:.2f} kilometers")

print(close_city.iloc[0]['city'])

a = func.distance_between_two_cities('Rome','Milan')
print (a['city'].values[0])