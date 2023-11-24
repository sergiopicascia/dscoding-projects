#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import pandas, streamlit and geopy libraries
import streamlit as st
import pandas as pd
from geopy.distance import geodesic


# In[2]:


#name the Project
st.set_page_config(page_title="My Travel App")


# In[3]:


#get Dataset
@st.cache_data
def get_dataset():
    url = "http://island.ricerca.di.unimi.it/~alfio/shared/worldcities.xlsx"
    return pd.read_excel(url)

#Set dataset
world_cities_dataset = get_dataset()


# In[ ]:


#Return dataset
#world_cities_dataset


# In[4]:


#introduce helper functions

#gets city_id
def get_city_id(city, cities_map):
    return cities_map[city]

#calculates distance
def calculate_distance(city1_id, city2_id):
    coords1 = (world_cities_dataset.loc[world_cities_dataset['id'] == city1_id, 'lat'].values[0],
                       world_cities_dataset.loc[world_cities_dataset['id'] == city1_id, 'lng'].values[0]) #ex:coordinates of Seoul
    coords2 = (world_cities_dataset.loc[world_cities_dataset['id'] == city2_id, 'lat'].values[0],
                       world_cities_dataset.loc[world_cities_dataset['id'] == city2_id, 'lng'].values[0]) #ex:coordinates of Tokyo
    return geodesic(coords1, coords2).kilometers  #1000

#introducing conditions to calculate tral weight(hours)
def calculate_travelling_cost(city1_id, city2_id, i):
    weight = 2 * (i + 1)  # 2 hours for the nearest, 4 for the second, 8 for the third, etc. #2
    city_1_country = world_cities_dataset.loc[world_cities_dataset['id'] == city1_id, 'country'].values[0]
    city_2_country = world_cities_dataset.loc[world_cities_dataset['id'] == city2_id, 'country'].values[0]
    city_2_population = world_cities_dataset.loc[world_cities_dataset['id'] == city2_id, 'population'].values[0]
    if city_1_country != city_2_country:
        weight += 2  # Additional 2 hours if the destination city is in another country
    if city_2_population > 200000:
        weight += 2  # Additional 2 hours if the destination city has more than 200,000 inhabitants
    return weight

#gets longitude by city_id
def get_lng_city(city_id):
    lng = world_cities_dataset.loc[world_cities_dataset['id'] == city_id, 'lng'].values[0]
    return lng


# In[5]:


#app starts here
st.title("Travel App")
st.write("This is a travel app that will help you to identify if you would be able to travel the world from the selected city in 80 days")

cities_map = {f"{city}": id for id, city in
                        zip(world_cities_dataset['id'], world_cities_dataset['city'])}
    #{"London": "458", "Tokyo: "577}

start_city = st.selectbox('Select your starting location', list(cities_map)) #selecting city where we start. ex:Seoul

selected_cities = st.multiselect('Select cities you want to visit', list(cities_map)) #choosing where we want to go, ex:{Tokyo, Jakarta, Manila}
st.write(f"You selected {selected_cities}")


# In[6]:


#introducing calculating logic

if st.button("Start Travelling"):
    distances = {} #empty map
    for city in selected_cities: #Tokyo
        distance = calculate_distance(get_city_id(start_city,cities_map), get_city_id(city,cities_map)) #from Seoul to Tokyo
        distances[city] = distance #{"Tokyo": 1000, "jakarta: 2000, Manila: 200}
    # Sorting the dictionary by values in ascending order
    sorted_map = dict(sorted(distances.items(), key=lambda item: item[1]))   #{Manila:200, Tokyo:1000, Jakarta:2000. London:5000}

    hours = 0  #in the beginning 0 hours spent travelling
    i = 1 #sorted by the nearest city, 1 is nearest
    init_city = start_city #where we start. ex: Seoul
    prev_city = start_city #previous city, Seoul in the start
    east = True
    for city, distance in sorted_map.items(): #Manila, 200   #Tokyo, 1000

        if get_lng_city(get_city_id(city, cities_map)) < get_lng_city(get_city_id(start_city, cities_map)):  #if lng decreases, we are not travelling east
            east = False #set east flag to false
        if start_city == city:
            continue
        if i>3: #2>3
            init_city = prev_city #set third city to be initial
            i = 0
        hours += calculate_travelling_cost(get_city_id(init_city,cities_map),get_city_id(city,cities_map), i) #Seoul, Manila, 1 #56
        i+=1 #3
        prev_city = city #Jakarta

    days = hours // 24    #converting hours to days
    remaining_hours = hours % 24 #remainder hours

#print the result
    if selected_cities:
        if (start_city not in selected_cities):
            st.write(f"This is not a round trip. You did not return back to {start_city}")
        if not east:
            st.write(f"You can travel only to the east of {start_city}")
        else:
            if days>80:
                st.write(f"It's not possible to travel around the world in 80 days, the minimum days needed: {days} days {remaining_hours} hours")
            else:
                st.write(f"Congratulations, you just travelled the world in {days} days {remaining_hours} hours")
    else:
        st.write("You did not select destination cities")


# In[ ]:





# In[ ]:




