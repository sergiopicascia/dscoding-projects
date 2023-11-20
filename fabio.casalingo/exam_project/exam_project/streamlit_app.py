import random
import pandas as pd
import streamlit as st
from methods import Travel
from methods import MapHandler

st.title('Python Project')


@st.cache_data(persist=True)
def cached_travel_instance():
    ex = Travel()
    return ex


@st.cache_data(persist=True)
def cached_map_handler_instance():
    mp = MapHandler()
    return mp


city_explorer = cached_travel_instance()
maps = cached_map_handler_instance()


@st.cache_data(persist=True)
def shuffle_close(input_city_id, n):
    close = city_explorer.n_close_city(input_city_id, n)['city'].tolist()
    random.shuffle(close)
    return close


@st.cache_data()
def load_dataset():
    return pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')


dataset = load_dataset()

city_name_to_id_iso3 = {f"{city} ({iso3})": id for id, city, iso3 in
                        zip(dataset['id'], dataset['city'], dataset['iso3'])}

action = st.selectbox('Select an action',
                              ['Find the n closest cities', 'City to city',
                               'Show the path going only on east','Population', 'Minigame'])

if action == 'Find the n closest cities':
    selected_city_name_iso3 = st.selectbox('City', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=3)
    n += 1
    if st.button('Find the n cities '):
        closest_cities = city_explorer.n_close_city(input_city_id, n)
        st.write('The closest cities are:')
        st.write(closest_cities)

if action == 'City to city':
    selected_city1_name_iso3 = st.selectbox('City 1', list(city_name_to_id_iso3.keys()))
    selected_city2_name_iso3 = st.selectbox('City 2', list(city_name_to_id_iso3.keys()))
    input_city1_id = city_name_to_id_iso3[selected_city1_name_iso3]
    input_city2_id = city_name_to_id_iso3[selected_city2_name_iso3]
    n = st.number_input('Insert how many cities you want to consider to travel', min_value=1, value=35)
    n += 1
    if st.button('Show the travel'):
        path = city_explorer.distance_between_two_cities(input_city1_id, input_city2_id, n)
        st.write('The duration of the journey is : ')
        travel_time = city_explorer.time(path)
        if travel_time > 24:
            d = int(travel_time / 24)
            h = travel_time % 24
            st.write(d, 'Days', h, 'Hours')
        else:
            st.write(travel_time, 'hours')
        st.write('The path')
        mappa = maps.map_2d(path)
        st.components.v1.html(mappa._repr_html_(), width=800, height=600)

if action == 'Show the path going only on east':
    selected_city_name_iso3 = st.selectbox('City', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]
    if st.button('Select a city'):
        if input_city_id == 1380382862:
            html_file_path = "C:/Uni/Coding/python/exam_project/tests/rome_it.html"
            st.components.v1.iframe(html_file_path, width=800, height=600)
        else:
            closest_cities = city_explorer.east(input_city_id)
            city_explorer = cached_travel_instance()
            st.write('The duration of the travel is:')
            travel_time = city_explorer.time(closest_cities)
            if travel_time > 24:
                d = int(travel_time / 24)
                h = travel_time % 24
                st.write(d, 'Days', h, 'Hours')
            else:
                st.write(travel_time, 'hours')
            st.write('path')
            mappa = maps.map_3d(closest_cities)
            st.map(mappa._repr_html_(), width=800, height=800)

if action == 'Minigame':
    selected_city_name_iso3 = st.selectbox('City', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]

    closest_cities = shuffle_close(input_city_id, 10)
    st.write('Choose the three closest cities between the chosen:')

    selected_cities = set(
        st.multiselect('Select 3 closest cities', closest_cities, max_selections=3, key='unique_key'))
    true = set(city_explorer.n_close_city(input_city_id, 4)['city'])

    if st.button('Check'):
        if selected_cities == true:
            st.write('You won')
        else:
            st.write('You lost')
            st.write('Right answer was:', true)

if action == 'Population':
    maps.population(dataset)