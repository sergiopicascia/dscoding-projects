import keplergl
import pandas as pd
from geopy.distance import great_circle as gc
import folium
import streamlit as st
import self_made_functions as func
import plotly.express as px
import numpy as np
import random
st.title('Python Project')


@st.cache_data(persist=True)
def shuffle_close(input_city_id, n):
    close = func.three_close_city(input_city_id, n)['city'].tolist()
    random.shuffle(close)
    return close
@st.cache_data
def load_dataset():
    return pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')

dataset = load_dataset()

city_name_to_id_iso3 = {f"{city} ({iso3})": id for id, city, iso3 in
                        zip(dataset['id'], dataset['city'], dataset['iso3'])}
action = st.sidebar.selectbox('Select an action',
                              ['Find the n closest cities', 'City to city',
                               'Show the path going only on east', 'Minigame'])


if action == 'Find the n closest cities':
    selected_city_name_iso3 = st.selectbox('City', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=3)
    n += 1
    if st.button('Find the n cities '):
        closest_cities = func.three_close_city(input_city_id, n)
        st.write('The closest cities are:')
        st.write(closest_cities)

if action == 'City to city':
    selected_city1_name_iso3 = st.selectbox('Città1', list(city_name_to_id_iso3.keys()))
    selected_city2_name_iso3 = st.selectbox('Città2', list(city_name_to_id_iso3.keys()))
    input_city1_id = city_name_to_id_iso3[selected_city1_name_iso3]
    input_city2_id = city_name_to_id_iso3[selected_city2_name_iso3]
    n = st.number_input('Insert how many cities you want to consider to travel', min_value=1, value=35)
    n += 1
    if st.button('Show the travel'):
        st.write    (input_city1_id)
        path = func.distance_between_two_cities(input_city1_id, input_city2_id,n)
        st.write('La durata del percorso è: ')
        travel_time = func.time(path)
        if travel_time > 24:
            d = int(travel_time / 24)
            h = travel_time %24
            st.write(d, 'Days',h, 'Hours')
        else:
            st.write(travel_time,'hours')
        st.write('The path')
        mappa = func.maps(path)
        st.components.v1.html(mappa._repr_html_(), width=800, height=600)

if action == 'Show the path going only on east':
    selected_city_name_iso3 = st.selectbox('Città', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]
    if st.button('Select a city'):
        if input_city_id == 1380382862:
            html_file_path = "C:/Uni/Coding/python/exam_project/tests/rome_it.html"
            st.components.v1.iframe(html_file_path, width=800, height=600)
        else:
            closest_cities = func.east(input_city_id)
            st.write('The duration of the travel is:')
            travel_time = func.time(closest_cities)
            if travel_time > 24:
                d = int(travel_time / 24)
                h = travel_time %24
                st.write(d, 'Days',h, 'Hours')
            else:
                st.write(travel_time,'hours')
            st.write('path')
            mappa = func.map_test(closest_cities)
            st.components.v1.html(mappa._repr_html_(), width=800, height=600)

if action == 'Minigame':
    selected_city_name_iso3 = st.selectbox('City', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]

    #if st.button('Find the 10 closest cities'):

    closest_cities = shuffle_close(input_city_id, 10)
    st.write('Choose the three closest cities between the chosen:')

    #shuffled_cities = closest_cities['city'].tolist()
    #random.shuffle(shuffled_cities)

    # Visualizzare le città mischiate
    selected_cities = set(st.multiselect('Select 3 closest cities', closest_cities,max_selections=3, key='unique_key'))
    true = set(func.three_close_city(input_city_id,3))

    # Perform actions based on the user's selection (e.g., display the selected cities)
    if st.button('Check'):
        if selected_cities == true:
            st.write('Hai vinto')
        else:
            st.write('Hai perso')
