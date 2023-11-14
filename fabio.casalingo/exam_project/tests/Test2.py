import numpy as np
import pandas as pd
from geopy.distance import great_circle as gc
import exam_project.self_made_functions as func
import networkx as nx

dataset = pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')
'''
print(dataset['city'][0])
print(dataset['city'][1])
tok = (dataset['lat'][0],dataset['lng'][0])
jak = (dataset['lat'][1],dataset['lng'][1])
distance = gc(tok,jak).kilometers
print(distance)

print(type(dataset))

city = dataset[dataset['city'] == 'Jakarta']
print(city)
id_city = city['id']
print(id_city)
latitude = dataset.loc[dataset['id'] == id_city.iloc[0], 'lat']
print(latitude)
'''
'''start_city = 'Rome'
end_city = 'Milan'
srt_city = dataset[(dataset['city'] == start_city) & (dataset['admin_name'] == 'Lazio')]
des_city = dataset[(dataset['city'] == end_city) & (dataset['admin_name'] == 'Lombardy')]
id_des_city = int(des_city['id'].iloc[0])
end_city_coords = (
dataset.loc[dataset['id'] == id_des_city, 'lat'].values[0], dataset.loc[dataset['id'] == id_des_city, 'lng'].values[0])
# print(dataset['id'][0])

city_id = int(srt_city['id'].iloc[0])
city = start_city
i = 0
visited_cities = []
while city_id != id_des_city:
    in the while build a cycle that use i for minimize the city into the func func.three_close_city(city) 
    but avoiding  an infinite loop
    close_city = func.three_close_city(city)[:i]
    close_city['Distance from destination: '] = close_city.apply(
        lambda row: gc(end_city_coords, (row['lat'], row['lng'])).kilometers, axis=1)
    sorted_closed_city = close_city.sort_values(by='Distance from destination: ')
    for _,row in sorted_closed_city.iterrows():
        if city not in visited_cities:
            city = row['city']
            visited_cities.append(city)
            city_id = row['id']
            break
    print(visited_cities)
    print(city, city_id)'''

# Crea un grafo con le città come nodi e le distanze tra le città come archi
def crea_grafo(città):
    G = nx.Graph()
    for città[1] in città:
        for città[2] in città:
            if città[1] != città[2]:

                distanza = gc((dataset.loc[dataset['id'] == città[1], 'lat'].values[0]),
                    (dataset.loc[dataset['id'] == città[1], 'lng'].values[0]) ,
                     (dataset.loc[dataset['id'] == città[2], 'lat'].values[0]),
                   (dataset.loc[dataset['id'] == città[2], 'lat'].values[0])).kilometers  # Sostituire con la funzione reale di calcolo della distanza
                G.add_edge(città[1], città[2], weight=distanza)
    return G

# Trova il percorso ottimale utilizzando l'algoritmo del commesso viaggiatore
def trova_percorso_ottimale(grafo, città_partenza):
    percorso_ottimale = [città_partenza]

    while len(percorso_ottimale) < len(grafo.nodes()):
        città_attuale = percorso_ottimale[-1]
        vicini = list(grafo[città_attuale])
        vicini.sort(key=lambda città: grafo[città_attuale][città]['weight'])

        for città in vicini:
            if città not in percorso_ottimale:
                percorso_ottimale.append(città)
                break

    # Torna alla città di partenza
    percorso_ottimale.append(città_partenza)

    return percorso_ottimale

# Esempio di utilizzo
#città = ['A', 'B', 'C', 'D', 'E', 'F']  # Sostituire con le tue città
città = []
for index, city in dataset.iterrows():
    città.append(city['id'])
grafo = crea_grafo(città)
percorso_ottimale = trova_percorso_ottimale(grafo, 1826645935)
print(percorso_ottimale)
func.maps(percorso_ottimale)




