import pandas as pd
import numpy as np
from scipy.spatial import distance


#df = pd.read_excel(r"C:\Users\cibei\OneDrive\Desktop\Coding_for_data_science\Python\dscoding-projects\niccolo.cibei\travel_project\travel_project\dataset\worldcities.xlsx")


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




