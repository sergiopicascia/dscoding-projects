import pandas as pd
from haversine import haversine

# Load the dataset
url = 'http://island.ricerca.di.unimi.it/~alfio/shared/worldcities.xlsx'
df = pd.read_excel(url)

# Create a dictionary to map city names to their coordinates
city_coords = {city: (lat, lng) for city, lat, lng in zip(df['city_ascii'], df['lat'], df['lng'])}

# Function to calculate Haversine distance between two cities
def calculate_distance(city1, city2):
    return haversine(city_coords[city1], city_coords[city2], unit='km')

# Create a dictionary to represent the graph with distances
city_graph = {city: [] for city in df['city_ascii']}
for city1 in city_graph:
    for city2 in df['city_ascii']:
        if city1 != city2:
            distance = calculate_distance(city1, city2)
            city_graph[city1].append((city2, distance))

# Function to find the shortest path between two cities
def find_shortest_path(graph, start, end, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path = path + [start]

    if start == end:
        return path

    shortest = None
    for city, distance in graph[start]:
        if city not in visited:
            new_path = find_shortest_path(graph, city, end, visited, path)
            if new_path:
                if shortest is None or len(new_path) < len(shortest):
                    shortest = new_path

    return shortest

# Calculate the shortest path around the world starting and ending in London
start_city = 'London'
visited_cities = set([start_city])
total_travel_time = 0
current_city = start_city

while len(visited_cities) < len(df):
    remaining_cities = set(df['city_ascii']) - visited_cities
    shortest_paths = []

    for city in remaining_cities:
        path = find_shortest_path(city_graph, current_city, city)
        if path:
            shortest_paths.append((city, path))

    # Sort paths by distance
    shortest_paths.sort(key=lambda x: len(x[1]))

    # Choose the shortest path and update the current city
    next_city, path = shortest_paths[0]
    travel_distance = len(path) - 1
    travel_time = 2**travel_distance  # 2 hours for the nearest, 4 hours for the second nearest, 8 hours for the third nearest
    total_travel_time += travel_time

    if travel_distance > 1:
        # Additional 2 hours if the destination city is in another country
        total_travel_time += 2

    if df[df['city_ascii'] == next_city]['population'].values[0] > 200000:
        # Additional 2 hours if the destination city has more than 200,000 inhabitants
        total_travel_time += 2

    visited_cities.add(next_city)
    current_city = next_city

# Return to London
total_travel_time += 2**travel_distance

# Check if it's possible to return to London within 80 days
if total_travel_time <= 80 * 24:
    print(f"It is possible to travel around the world and return to London in {total_travel_time} hours ({total_travel_time / 24} days).")
else:
    print(f"It is not possible to complete the journey within 80 days.")

