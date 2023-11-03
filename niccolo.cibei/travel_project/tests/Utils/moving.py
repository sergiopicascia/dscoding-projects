import pandas as pd
import numpy as np
from scipy.spatial import distance

df = pd.read_excel(r"C:\Users\cibei\OneDrive\Desktop\Coding_for_data_science\Python\dscoding-projects\niccolo"
                  r".cibei\travel_project\travel_project\dataset\worldcities.xlsx")

def cleaned_Dataframe(df):
    df.drop(columns=['city', 'country', 'iso3', 'admin_name'], axis=1, inplace=True)
    return df


def find_closest_cities(df, k=3):
    mat = distance.cdist(df[['lat', 'lng']], df[['lat', 'lng']], metric='euclidean')
    new_df = pd.DataFrame(mat, index=df['id'], columns=df['id'])

    arr = new_df.values
    np.fill_diagonal(arr, np.nan)  # Replace diagonal with NaN

    closest_cities = []

    for i in range(k):
        closest = np.nanargmin(arr, axis=1)
        closest_cities.append(df['id'].iloc[closest].to_list())
        arr[np.arange(arr.shape[0]), closest] = np.nan  # Set the closest city's distance to NaN

    for i in range(k):
        df[f'closest_city_{i + 1}'] = closest_cities[i]

    return df

def plan_route_around_world(df, starting_city='London', k=3):

    # Ensure starting_city is valid
    if starting_city not in df['city_ascii'].tolist():
        raise ValueError(f"Starting city '{starting_city}' not found in the DataFrame.")

    # Initialize the route
    route = []

    # Start in the specified city
    current_location = starting_city
    route.append(current_location)

    # Create a loop to plan your route
    while len(route) < len(df):
        # Get the k closest cities from the DataFrame
        closest_cities = df.loc[df['id'] == current_location][[f'closest_city_{i}' for i in range(1, k + 1)]].values[0]

        # Choose the city furthest to the east from the list of closest cities
        next_city = min(closest_cities, key=lambda city_id: df.loc[df['id'] == city_id]['lng'].values[0])

        # Update your current location to the chosen city
        current_location = next_city
        route.append(current_location)

    # Ensure the route is circular by returning to the starting city
    route.append(starting_city)

    return route


def maps(visit):
    zoom = dataset[(dataset['id'] == visit[0])][['lat', 'lng']].values[0] #errore
    mappa = folium.Map(location = zoom, zoom_start = 6)
    #mappa = folium.Map(location=[45.5236, -122.6750], zoom_start=0)
    for i in range(len(visit)):
        s = dataset[(dataset['id'] == visit[i])][['lat', 'lng']].values[0]
        #if i > 0 and i < (len (visit) - 1):
            #s2 = dataset[(dataset['id'] == visit[i + 1])][['lat', 'lng']].values[0]
        folium.Marker(s,popup = dataset[(dataset['id'] == visit[i])][['city']].values[0] ).add_to(mappa)
    locations = [(dataset.loc[dataset['id'] == visit[j], ['lat', 'lng']].values[0]) for j in range(len(visit))]
    line = folium.PolyLine(locations=locations,
                           color='blue',  # Colore della linea
                           weight=5,  # Spessore della linea
                           opacity=0.7  # Opacità della linea
                           )
    line.add_to(mappa)
    mappa.save('mappa.html')



'''

import pandas as pd
import numpy as np
import scipy
from scipy.spatial import distance

df = pd.read_excel(r"C:\Users\cibei\OneDrive\Desktop\Coding_for_data_science\Python\dscoding-projects\niccolo"
                  r".cibei\travel_project\travel_project\dataset\worldcities.xlsx")

def cleaned_Dataframe1(df):
    df.drop(columns=['city', 'country', 'iso3', 'admin_name'], axis=1)

    return df


def find_closest_cities1(df=df, k: int = 3):
    i = 0
    new_list = []
    mat = scipy.spatial.distance.cdist(df[['lat', 'lng']],
                                       df[['lat', 'lng']], metric='euclidean')
    new_df = pd.DataFrame(mat, index=df['id'], columns=df['id'])

    # Store the array values in a variable
    arr = new_df.values
    # We dont want to find mimimum to be same point, so replace diagonal by nan
    arr[np.diag_indices_from(new_df)] = np.nan
    while i < k:
        i += 1
        # Replace the non nan min with column name and otherwise with false
        new_close = np.where(arr == np.nanmin(arr, axis=1)[:, None], new_df.columns, False)

        # Get column names ignoring false.
        df['closest_city_' + str(i)] = [i[i.astype(bool)].tolist() for i in new_close]

        # we want to eliminate the brackets from the column 'close'
        df['closest_city_' + str(i)] = df['closest_city_' + str(i)].str.get(0)

        mask = new_close != 0

        new_df[mask] = np.nan

    return df


'''
