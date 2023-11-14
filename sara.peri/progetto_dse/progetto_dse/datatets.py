

import pandas as pd
import os
import numpy as np
import functions as fun

## Importing Datasets


folder_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO"
city_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO/archive/GlobalLandTemperaturesByCity.csv"
country_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO/archive/GlobalLandTemperaturesByCountry.csv"
majorcity_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO/archive/GlobalLandTemperaturesByMajorCity.csv"
state_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO/archive/GlobalLandTemperaturesByState.csv"


city = pd.read_csv(city_path)
country = pd.read_csv(country_path)
major = pd.read_csv(majorcity_path)
state = pd.read_csv(state_path)


## Data Cleaning
city['dt'] = pd.to_datetime(city['dt'], format='%Y-%m-%d')
country['dt'] = pd.to_datetime(country['dt'], format='%Y-%m-%d')
major['dt'] = pd.to_datetime(major['dt'], format='%Y-%m-%d')
state['dt'] = pd.to_datetime(state['dt'], format='%Y-%m-%d')


city['Latitude'] = city['Latitude'].apply(fun.change_latitude)
city['Longitude'] = city['Longitude'].apply(fun.change_longitude)

major['Latitude'] = major['Latitude'].apply(fun.change_latitude)
major['Longitude'] = major['Longitude'].apply(fun.change_longitude)


datasets = [city, country, major, state]

for i in datasets:
    fun.calcola_valori_mancanti(i)


df_per_country_city= fun.split_dataframes_by_country(city)
df_per_country_country = fun.split_dataframes_by_country(country)
df_per_country_major = fun.split_dataframes_by_country(major)
df_per_country_state = fun.split_dataframes_by_country(state)

Italy = fun.get_dataframe_for_country(df_per_country_city, 'Italy')

info_country_city = fun.get_country_info(city, df_per_country_city, city_column='City')
info_country_country = fun.get_country_info(country, df_per_country_country)
info_country_major = fun.get_country_info(major, df_per_country_major, city_column='City')
info_country_state = fun.get_country_info(state, df_per_country_state, city_column='City')


info_country_city_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO/archive/InfoCountry_city.csv"
info_country_country_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO/archive/InfoCountry_country.csv"
info_country_major_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO/archive/InfoCountry_major.csv"
info_country_state_path = "/Users/apple/Desktop/Coding for Data Science and Data Management/Python/PROGETTO/archive/InfoCountry_state.csv"

info_country_city.to_csv(info_country_city_path, index=False)
info_country_country.to_csv(info_country_country_path, index=False)
info_country_major.to_csv(info_country_major_path, index=False)
info_country_state.to_csv(info_country_state_path, index=False)