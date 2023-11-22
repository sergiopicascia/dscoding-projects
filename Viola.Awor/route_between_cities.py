# -*- coding: utf-8 -*-
"""route_between_cities.py: Contains class route_between_cities with functions to calculate path bweteen any given cities
"""

import pandas as pd
import haversine as hs

# Class project wrapped in a class
class route_between_cities:
  def __init__(self, df:pd.DataFrame, year:int=2013, current_city:str='Peking', last_city:str='Los Angeles'):
    self.df = df
    self.year = year
    self.current_city = current_city
    self.last_city = last_city

  def transform_df(self):
    # Drop unnecessary columns
    df_MajorCity_path = (self.df).drop(columns=['AverageTemperatureUncertainty','Country'])
    # Drop null rows if any column value is null
    df_MajorCity_path = (df_MajorCity_path.dropna(how='any')).reset_index(drop=True)
    # Convert dt to datetime type
    df_MajorCity_path['dt'] = pd.to_datetime(df_MajorCity_path['dt'])
    # Extract year from dt
    df_MajorCity_path['year'] = df_MajorCity_path['dt'].dt.year
    # Dropping hemisphere from latitude then converting it to float
    df_MajorCity_path['Latitude'] = df_MajorCity_path['Latitude'].str[:-1].astype('float')
    # Removing orientation from longitude then converting it to float
    df_MajorCity_path['Longitude'] = df_MajorCity_path['Longitude'].str[:-1].astype('float')
    # concatenating lat and long to create a consolidated location as accepted by havesine function
    df_MajorCity_path['coord'] = list(zip(df_MajorCity_path['Latitude'], df_MajorCity_path['Longitude']))
    return df_MajorCity_path
# haversine library to calculate the earth's distance between two cordinates.
  def haversine_distance(self, origin, destination):
    '''
    origin: type(tuple) Origin coordinate 
    destination: type(tuple); destination coordinate
    '''
    dist=hs.haversine(origin, destination)
    return round(dist,2)

  def warmest_of_near_cities(self, df:pd.DataFrame, current_city):
    '''
    df: Output of transformed data by function transform_df
    current_city: City to define the neighbors
    '''
    # Retrieve coordinates for current_city from df
    current_city_coord = df[df['City']==current_city]['coord'].iloc[0]
    # Filter data for a speific year year_
    data = df[df['dt'].dt.year==self.year]
    # Update dataframe wiithout current_city record, to be returned and used in next iteration
    data = data[~(data['City']==current_city)]
    # Aggregate data
    data_agg = data.groupby(['City','coord'])['AverageTemperature'].mean().rename('avg_temp').reset_index()
    # Obtain the haversine distance between current_city_coord and the different data_agg coordinates
    dist = data_agg['coord'].apply(lambda coord: self.haversine_distance(current_city_coord, coord))
    data_agg['haversine_distance'] = dist
    # Select 3 nearest cities to current_city, then select the hottest among them
    route_city = data_agg.nsmallest(3,'haversine_distance').nlargest(1,'avg_temp')['City'].iloc[0]
    return route_city, data

  def find_route(self):
    df = self.transform_df()
    current_city = self.current_city
    route = [current_city]
    while current_city != self.last_city:
      # Find the next city after current_city
      next_city, df = self.warmest_of_near_cities(df, current_city)
      # Update current_city with the calculated next_city, then append it to route
      current_city = next_city
      route.append(current_city)
    return route
