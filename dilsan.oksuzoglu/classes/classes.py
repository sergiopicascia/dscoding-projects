import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


class CityPreprocessor:
    
    def __init__(self, excel_path, london_lat, london_lng, sample_size=500, random_seed=50):
        """
        Initialize the CityPreprocessor object with the specified parameters.
        __init__ method to initialize the class attributes like excel_path, london_lat, london_lng, dc, random_seed, and sample_size

        Parameters:
        - excel_path (str): The path to the Excel file containing city data.
        - london_lat (float): Latitude of London.
        - london_lng (float): Longitude of London.
        - dc (DistanceCalculator): An instance of the DistanceCalculator class.
        - random_seed (int): Seed for numpy's random number generator for reproducibility.
        - sample_size (int): Number of cities to sample from the dataset.
        """
        self.excel_path = excel_path
        self.london_lat = london_lat
        self.london_lng = london_lng
        self.sample_size = sample_size
        self.random_seed = random_seed
        self.dc = DistanceCalculator()

    def load_and_preprocess_data(self):
        """
        Load city data from an Excel file, filter and preprocess it, and return a sampled DataFrame.

        Returns:
        pandas.DataFrame: Sampled and preprocessed DataFrame with city information.
        """
        cities = pd.read_excel(self.excel_path)

        cities = cities[cities['lat'] > 30].reset_index().drop(['index'], axis=1)

        cities['distance_km'] = cities.apply(
            lambda row: self.dc.haversine_distance_in_km(self.london_lat, self.london_lng, row['lat'], row['lng']), axis=1)

        df = cities.sort_values('distance_km').rename(columns={'id': 'city_id', 'city': 'city_name'}).reset_index(drop=True)

        np.random.seed(self.random_seed)
        indices_to_sample = np.concatenate(([0], np.random.choice(df.index[1:], size=self.sample_size - 1, replace=False)))
        sampled_df = df.iloc[indices_to_sample].sort_values(by='distance_km').reset_index(drop=True)

        return sampled_df
    
    
    



class DistanceCalculator:

    # to calculate the distance between the cities
    def haversine_distance_in_km(self, lat1, lon1, lat2, lon2):
        """
        Calculate the Haversine distance between two points on the Earth's surface.

        Parameters:
        - lat1 (float): Latitude of the first point in degrees.
        - lon1 (float): Longitude of the first point in degrees.
        - lat2 (float): Latitude of the second point in degrees.
        - lon2 (float): Longitude of the second point in degrees.

        Returns:
        float: The Haversine distance between the two points in kilometers.

        Formula:
        The Haversine formula calculates the shortest distance between two points on the surface
        of a sphere using their latitudes and longitudes.
        """
        # Radius of the Earth in kilometers
        earth_radius = 6371 

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


    
    
class CostCalculator:

    def check_population(self, population):
        """
        Check the population size and return a code based on a threshold.

        Parameters:
        - population (int): The population size to be checked.

        Returns:
        int: Return 2 if the population is greater than 200,000, and 0 otherwise.
        """
        if population > 200000:
            return 2
        else:
            return 0



    def check_country(self, current_city_country, destination_country):
        """
        Check if the current city and destination have different countries.

        Parameters:
        - current_city_country (str): The country of the current city.
        - destination_country (str): The country of the destination.

        Returns:
        int: Return 2 if the current city and destination have different countries, and 0 otherwise.
        """
        if current_city_country != destination_country:
            return 2
        else:
            return 0




    #calculating the cost resulting from the distance only
    def get_travel_cost(self, index):
        """
        Retrieve travel cost based on the given index.

        Parameters:
        - index (int): An index representing a specific travel scenario.

        Returns:
        int: The travel cost corresponding to the given index.

        The function uses a predefined dictionary (`res_dict`) to map indices to travel costs.
        It is designed to provide the cost associated with a particular travel scenario based on the input index.
        """
        res_dict = {0:2,1:4,2:8}
        return res_dict[index]



    
    def calculate_cost(self, current_city_country, current_city_id, df):
        """
        Calculate travel costs based on the current city's country, city ID, and a DataFrame of destination cities.

        Parameters:
        - current_city_country (str): The country of the current city.
        - current_city_id (int): The ID of the current city.
        - df (pandas.DataFrame): A DataFrame containing information about three nearest destination cities.

        Returns: pandas.DataFrame: The DataFrame with added columns for travel cost calculations.
        """

        df = df.reset_index().drop('index',axis=1)       
        #creates a new column named 'cost_country'
        df['cost_country'] = df.apply(lambda row: self.check_country(current_city_country,row['country']), axis=1)
        df['cost_pop'] = df.apply(lambda row: self.check_population(row['population']), axis=1)
        df['travel_cost'] = df.apply(lambda row: self.get_travel_cost(row.name), axis=1)


        return df



    #in info_cities list
    def sum_total_cost(self, row):
        """
        Calculate the total cost based on the provided DataFrame row.

        Parameters:
        - row (pandas.Series): A row from a DataFrame containing cost-related columns.

        Returns:
        float: The total cost calculated as the sum of 'cost_country', 'cost_pop', and 'travel_cost'.
        """
        return row['cost_country'] + row['cost_pop'] + row['travel_cost']


    

class RouteCalculator:
    def __init__(self, df: pd.DataFrame, cc: CostCalculator, dc: DistanceCalculator):
        self.df = df.copy()
        self.cc = cc
        self.dc = dc

    def calculate_route(self) -> dict:
        """
        Calculate information about the nearest three cities for each city in the provided DataFrame.

        Returns:
        dict: A dictionary containing information about the nearest three cities for each city, including
              'city_names', 'city_ids', 'city_distances', 'city_latitudes', 'city_longitudes', 'city_pops',
              'city_countries', and 'city_total_cost'.
        """
        city_ids = self.df.city_id.to_list()
        info_cities = {}

        for each_city_id in city_ids:
            lat = self.df[self.df['city_id'] == each_city_id].lat.values[0]
            lng = self.df[self.df['city_id'] == each_city_id].lng.values[0]
            name = self.df[self.df['city_id'] == each_city_id].city_name.values[0]
            country_name = self.df[self.df['city_id'] == each_city_id].country.values[0]

            self.df['distance_km'] = self.df.apply(
                lambda row: self.dc.haversine_distance_in_km(lat, lng, row['lat'], row['lng']), axis=1
            )
            df_sorted = self.df.sort_values(by='distance_km').reset_index().drop('index', axis=1)
            nearest_three = df_sorted[1:4]
            cost_df = self.cc.calculate_cost(country_name, each_city_id, nearest_three)
            sum_df_calculated = cost_df.assign(total_cost=cost_df.apply(self.cc.sum_total_cost, axis=1))
            city_info = {
                'city_names': nearest_three['city_name'].to_list(),
                'city_ids': nearest_three['city_id'].to_list(),
                'city_distances': nearest_three['distance_km'].to_list(),
                'city_latitudes': nearest_three['lat'].to_list(),
                'city_longitudes': nearest_three['lng'].to_list(),
                'city_pops': nearest_three['population'].to_list(),
                'city_countries': nearest_three['country'].to_list(),
                'city_total_cost': sum_df_calculated['total_cost'].to_list()
            }

            info_cities[each_city_id] = city_info

        return info_cities

    
    
class EastestCityFinder:

    def go_most_east(self,info_cities:dict):
        """
        Find the easternmost city for each city in the provided dictionary.

        Parameters:
        - info_cities (dict): A dictionary containing information about the nearest three cities for each city,
                             including 'city_names', 'city_ids', 'city_distances', 'city_latitudes', 'city_longitudes',
                             'city_pops', 'city_countries', and 'city_total_cost'.

        Returns:
        dict: A dictionary containing information about the easternmost city for each city, including coordinates,
              total cost, and city names with countries.
        This function iterates through each city in the provided dictionary, finds the easternmost city based on
        longitude, and collects information about total cost, coordinates, and city names with countries.
        """

        self.total_cost = 0
        coordinates_lat = []
        coordinates_lng = []
        self.city_and_country = []
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
            self.total_cost += eastest_city_cost
            #find the coordinates of the each eastest city 
            coordinates_lat.append(eastest_city_lat)
            coordinates_lng.append(eastest_city_lng)
            local_travel_costs.append(eastest_city_cost)
            self.city_and_country.append(eastest_city_country+'_'+eastest_city_name)

        result_dict = dict(zip(self.city_and_country, zip(coordinates_lat, coordinates_lng)))
        
        return result_dict




class PlotMaker:
    def cities_plot(self, city_and_country):
        """
        Visualize the count of cities visited per country using a bar plot.

        Parameters:
        - city_and_country (list): A list of strings where each string represents a city and its corresponding country,
                                   separated by an underscore.

        Returns:
        - The function generates and displays a bar plot using Matplotlib to visualize the distribution of cities
                across different countries.
        """
        #how many city in each country has been visited
        # Split city_and_country to extract countries
        # Count occurrences of each country
        city_and_country = city_and_country
        country_counts = {}

        # Count occurrences of each country
        for entry in city_and_country:
            country = entry.split('_')[0]
            country_counts[country] = country_counts.get(country, 0) + 1

        # Create a bar plot with adjusted size and labels
        plt.figure(figsize=(12, 6))  # Adjust the figure size (width, height)

        # Create a bar plot
        plt.bar(country_counts.keys(), country_counts.values())
        plt.xlabel('Country', fontsize=12)  # Adjust the font size
        plt.ylabel('Number of Cities', fontsize=12)
        plt.title('City Counts Visited per Country', fontsize=14)

        # Rotate x-axis labels vertically
        plt.xticks(rotation=90, ha='center')  # Rotate labels 90 degrees and center them

        # Show the plot
        plt.tight_layout()  # Adjust layout for better appearance
        return plt.show()








