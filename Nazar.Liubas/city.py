import numpy as np


class City:
    '''
    A class that represents a city.
    '''
    def __init__(self, name, latitude, longitude, country, population, city_id):
        '''
        :param name: str
        :param latitude: int
        :param longitude: int
        :param country: str
        :param population: int
        :param city_id: int
        '''
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.country = country
        self.population = population
        self.id = city_id
        self.neighbors = []

    def add_neighbor(self, neighbor, travel_time):
        '''
        Adds city and time to travel to list of neighbours of a city
        :param neighbor: City
        :param travel_time: int, hours to travel
        :return:
        '''
        # TODO change back. Commented thing is useful for saving data to json
        self.neighbors.append({'city': neighbor, 'travel_time': travel_time})
        # this is used for saving to json
        # self.neighbors.append({'city': neighbor.id, 'travel_time': travel_time})

    def calculate_distance(self, destination_city):
        '''
        Calculates distance between 2 cities based on Euclidian distance
        :param destination_city: City, destination point
        :return: Euclidian distance between two cities
        '''
        # Check if longitudes of cities have different signs,
        # then check if if is closer to move there from east or from west.
        # This additional logic is needed, if, for example, longitudes are -150 and 150.
        if (self.longitude > 0 > destination_city.longitude and
                (180 - self.longitude <= abs(destination_city.longitude))):
            temp_dest_long = 360 + destination_city.longitude
            temp_self_long = self.longitude
        elif (destination_city.longitude > 0 > self.longitude and
              (180 - destination_city.longitude <= abs(self.longitude))):
            temp_self_long = 360 + self.longitude
            temp_dest_long = destination_city.longitude
        else:
            temp_self_long = self.longitude
            temp_dest_long = destination_city.longitude

        return np.sqrt((destination_city.latitude - self.latitude) ** 2 +
                       (temp_dest_long - temp_self_long) ** 2)

    def calc_travel_time(self, destination_city, n_closest=1):
        '''
        Calculates travel time between current and destination city. It takes
        2 hours to the nearest city, 4 hours to the second nearest city,
        and 8 hours to the third nearest city. In addition, the trip takes an additional
        2 hours if the destination city is in another country than the starting city and
        an additional 2 hours if the destination city has more than 200,000 inhabitants.
        :param destination_city: City, the one with which travel time is calculated
        :param n_closest: int, 1 is the closest city, 2 - second closest, etc.
        :return: int, travel time in hours
        '''
        result_time = 2 ** n_closest
        if self.country != destination_city.country:
            result_time += 2
        if destination_city.population > 200000:
            result_time += 2
        return result_time

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name