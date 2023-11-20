import pandas as pd
import numpy as np
import random
import os
import math



# to calculate the distance between the cities
def haversine_distance_in_km(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    earth_radius = 6371  # You can use 3959 for miles

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences in latitude and longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula: to calculate the shortest distance between two points on the surface of a sphere
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))   # arctangent of the quotient y/x in radians
    distance = earth_radius * c

    return distance


#used in calculate_cost function
def check_population(population):
    if population > 200000:
        return 2
    else:
        return 0
    
    

#used in calculate_cost function
def check_country(current_city_country,destination_country):
    if current_city_country != destination_country:
        return 2
    else:
        return 0
    
    
    
    
#used in calculate_cost function
#calculating the cost resulting from the distance only
def get_travel_cost(index):
    res_dict = {0:2,1:4,2:8}
    return res_dict[index]






def sum_integers(row):
    # Filter out non-integer values and sum the remaining
    int_values = [value for value in row if isinstance(value, int)]
    return sum(int_values)





def calculate_cost(current_city_country,current_city_id,df):
    #current_city_country = df[df['city_id']==current_city_id]['country'].values[0]
    #df = df[df['city_id']!=current_city_id]
    #df = df.reset_index().drop('index',axis=1)
#DataFrame df called 'cost_country'.    
#applies a function to each row or column of the DataFrame
#lambda function takes each row of the DataFrame (row) and calls the check_country function with current_city_country 
#and the value in the 'country', 'population' columns of that row.
#axis=1: lambda function should be applied to rows. If axis=0 (or not specified), it would apply the function to columns.
    df['cost_country'] = df.apply(lambda row: check_country(current_city_country,row['country']), axis=1)
    #creates a new column named 'cost_country'
    df['cost_pop'] = df.apply(lambda row: check_population(row['population']), axis=1)
    df['travel_cost'] = df.apply(lambda row: get_travel_cost(row.name), axis=1)


    return df





def calculate_cost(current_city_country,current_city_id,df):
    #current_city_country = df[df['city_id']==current_city_id]['country'].values[0]
    #df = df[df['city_id']!=current_city_id]
    df = df.reset_index().drop('index',axis=1)
    
    df['cost_country'] = df.apply(lambda row: check_country(current_city_country,row['country']), axis=1)
    df['cost_pop'] = df.apply(lambda row: check_population(row['population']), axis=1)
    df['travel_cost'] = df.apply(lambda row: get_travel_cost(row.name), axis=1)


    return df




#in info_cities list
def sum_total_cost(row):
    return row['cost_country'] + row['cost_pop'] + row['travel_cost']




def choose_optimum_city(df):
    #Longitude is measured in degrees east or west from the Prime Meridian, and as we move east, the values increase
    #resets the index after sorting.
    #.loc[0]: selects the first row after sorting and resetting index, used to access a specific row by label (index) (which was reset in the previous step)
    df = df.sort_values(by=['lng'], ascending=[False]).reset_index().loc[0]
    city_id = df['city_id']
    total_cost = df['total_cost']
    city_name = df['city_name']
    lat = df['lat']
    lng = df['lng']
    country= df['country']
    return {'city_id':city_id,'total_cost':total_cost,'city_name':city_name,'lat':lat,'lng':lng,'country':country}



def calculate_route(df:pd.DataFrame)->dict:
    
    city_ids = df.city_id.to_list()
    info_cities = {}

    for each_city_id in city_ids:
        lat = df[df['city_id']==each_city_id].lat.values[0]
        lng = df[df['city_id']==each_city_id].lng.values[0]    
        name = df[df['city_id']==each_city_id].city_name.values[0]
        country_name = df[df['city_id']==each_city_id].country.values[0]

        df['distance_km'] = df.apply(lambda row: haversine_distance_in_km(lat,lng, row['lat'], row['lng']), axis=1)
        df_sorted = df.sort_values(by='distance_km').reset_index().drop('index',axis=1)
        nearest_three = df_sorted[1:4]   
        cost_df = calculate_cost(country_name,each_city_id,nearest_three)
        sum_df_calculated = cost_df.assign(total_cost=cost_df.apply(sum_total_cost, axis=1))
        city_info = {
            'city_names': nearest_three['city_name'].to_list(),
            'city_ids': nearest_three['city_id'].to_list(),
            'city_distances': nearest_three['distance_km'].to_list(),
            'city_latitudes':  nearest_three['lat'].to_list(),
            'city_longitudes':  nearest_three['lng'].to_list(),
            'city_pops': nearest_three['population'].to_list(),
            'city_countries': nearest_three['country'].to_list(),
            'city_total_cost' : sum_df_calculated['total_cost'].to_list()
        }

        info_cities[each_city_id] = city_info
    
    return info_cities
    

def go_most_east(info_cities:dict):
    
    total_cost = 0
    coordinates_lat = []
    coordinates_lng = []
    city_and_country = []
    local_travel_costs=[]

    for each_city in info_cities.keys():
        eastest_city_index = info_cities[each_city]['city_longitudes'].index(max(info_cities[each_city]['city_longitudes']))
        eastest_city_id = info_cities[each_city]['city_ids'][eastest_city_index]
        eastest_city_cost = info_cities[each_city]['city_total_cost'][eastest_city_index]
        eastest_city_lat = info_cities[each_city]['city_latitudes'][eastest_city_index]
        eastest_city_lng = info_cities[each_city]['city_longitudes'][eastest_city_index]
        eastest_city_country = info_cities[each_city]['city_countries'][eastest_city_index]
        eastest_city_name= info_cities[each_city]['city_names'][eastest_city_index]
        #add up to the total_cost variable the cost for each selected city 
        total_cost += eastest_city_cost
        #find the coordinates of the each eastest city 
        coordinates_lat.append(eastest_city_lat)
        coordinates_lng.append(eastest_city_lng)
        local_travel_costs.append(eastest_city_cost)
        city_and_country.append(eastest_city_country+'_'+eastest_city_name)

    coordinates = zip(coordinates_lat,coordinates_lng)
    
    return coordinates














