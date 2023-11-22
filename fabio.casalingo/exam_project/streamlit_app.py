# Import necessary libraries
import random
import pandas as pd
import streamlit as st
from methods import Travel
from visualize import MapHandler

# Set up the Streamlit app with a title
st.title('Python Project')


# Cache instances of Travel and MapHandler classes to avoid unnecessary computation
@st.cache_data(persist=True)
def cached_travel_instance():
    ex = Travel()
    return ex


@st.cache_data(persist=True)
def cached_map_handler_instance():
    mp = MapHandler()
    return mp


# Create instances of Travel and MapHandler classes
city_explorer = cached_travel_instance()
maps = cached_map_handler_instance()


# create a randomized options for a select box
@st.cache_data(persist=True)
def shuffle_close(input_city_id, n):
    close = city_explorer.n_close_city(input_city_id, n)['city'].tolist()
    random.shuffle(close)
    return close


# load the dataset in the chache for avoid to reload it very times
@st.cache_data()
def load_dataset():
    return pd.read_excel('C:/Uni/Coding/python/worldcities.xlsx')


dataset = load_dataset()

# Create a dictionary mapping city names with ISO3 codes to city IDs
city_name_to_id_iso3 = {f"{city} ({iso3})": id for id, city, iso3 in
                        zip(dataset['id'], dataset['city'], dataset['iso3'])}

# Allow the user to choose an action from a selection box
action = st.selectbox('Select an action',
                      ['Find the n closest cities', 'City to city',
                       'Show the path going only on east', 'Population', 'Minigame'])

# Execute code based on the selected action
if action == 'Find the n closest cities':
    # Call the method find_n_close and shows results
    selected_city_name_iso3 = st.selectbox('City', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=3)
    n += 1
    if st.button('Find the n cities '):
        closest_cities = city_explorer.n_close_city(input_city_id, n)
        closest_cities = closest_cities
        st.write('The closest cities are:')
        st.write(closest_cities[['city', 'lat', 'lng', 'iso3', 'population', 'capital', 'admin_name']])

# Call the method city_to_city and shows map
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
        mappa = maps.map_2d(path, True)
        st.components.v1.html(mappa._repr_html_(), width=800, height=600)

# Call the method east and shows map
if action == 'Show the path going only on east':
    selected_city_name_iso3 = st.selectbox('City', list(city_name_to_id_iso3.keys()))
    input_city_id = city_name_to_id_iso3[selected_city_name_iso3]
    if st.button('Select a city'):
        closest_cities = city_explorer.east(input_city_id)
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
        st.plotly_chart(mappa, width=800, height=800)

# Create a minigame based on n_close_city method and then shows map
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
        map_cl = maps.map_2d(city_explorer.n_close_city(input_city_id, 10)['id'].tolist(), False)
        st.components.v1.html(map_cl._repr_html_(), width=800, height=600)

# Call the method population for display the population distribution
if action == 'Population':
    map_pop = maps.population()
    st.plotly_chart(map_pop, width=800, height=800)
