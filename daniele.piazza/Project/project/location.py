import pandas as pd
import requests

"""
This class is used to upload the data and update the coordinates of the cities.
It contains the following methods:
__init__: initialize the class
_coords: convert the coordinate from the format Coord(N/S/E/W)
coordinates: convert latitude and longitude
google_coords: get the coordinates from the google api
_get_coordinates: get the coordinates of the cities
_update_file: update the csv file with the new coordinates
"""
class Location:
    """
    Initialize the class with the path of the CSV file and the Google API key. 
    Also, convert the format of the date to datetime.

    Parameters
    ----------
    path : str
        Path of the CSV file
    api_key : str
        Google API key
    """
    def __init__(self, path, api_key):
        self.path = path
        self.api_key = api_key
        self.data = pd.read_csv(path,index_col = False)
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        self.data['Year'] = self.data['dt'].dt.year
        self.data['City_Country'] = self.data['City'] + ', ' + self.data['Country']
        if type(self.data['Latitude'].iloc[0]) == str:
            self._update_file()

    
    """
    Convert the coordinate from the format Coord(N/S/E/W)

    Parameters
    ----------
    x : str
        Coordinate in the format Coord(N/S/E/W)

    Returns
    -------
    coord : float
        Coordinate in the format float
    """
    def _coords(self,x):
        sign = 1 if x[-1] in ('N', 'E') else -1
        return sign * float(x[:-1])

    """
    Convert latitude and longitude

    Parameters
    ----------
    city : pandas.core.series.Series
        Dataframe with the city, country, latitude and longitude

    Returns
    -------
    location : list
        List with the latitude and longitude of the city
    """
    def coordinates(self,city):
        return [self._coords(city['Latitude']), self._coords(city['Longitude'])]

    """
    Get the coordinates from the google api

    Parameters
    ----------
    city : pandas.core.series.Series
        Dataframe with the city, country, latitude and longitude

    Returns
    -------
    location : list
        List with the latitude and longitude of the city
    """
    def google_coords(self,city):
        # Google api can't find: Bally, Nigel, Sakura
        try:
            base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
            params = {
                'address': f"{city['City']}, {city['Country']}",
                'key': self.api_key
            }
            response = requests.get(base_url, params = params).json()
            if response['status'] == 'OK':
                location = response['results'][0]['geometry']['location']
                return [location['lat'], location['lng']]
            else:
                print(f"Error getting coordinates for {city['City']}: {response['status']}")
        except Exception as e:
            print(f"Error getting coordinates for {city['City']}: {str(e)}")
        return None

    """
    Get the coordinates of the cities

    Returns
    -------
    cities_coord : dict
        Dictionary with the city and the coordinates
    """
    def _get_coordinates(self):
        cities = self.data[['City', 'Country', 'Latitude', 'Longitude']].drop_duplicates().reset_index(drop = True)
        cities_coord = {}
        for i in range(cities.shape[0]):
            city = cities.iloc[i]['City']
            country = cities.iloc[i]['Country']
            city_country = f'{city}, {country}'
            if city_country not in cities_coord:
                coord = self.google_coords(cities.iloc[i])
                if coord is not None:
                    cities_coord[city_country] = coord
                else:
                    cities_coord[city_country] = self.coordinates(cities.iloc[i])
        return cities_coord

    """
    Update the csv file with the new coordinates
    """
    def _update_file(self):
        cities_coord = self._get_coordinates()
        self.data['Latitude'] = self.data['City_Country'].map(lambda x: cities_coord[x][0])
        self.data['Longitude'] = self.data['City_Country'].map(lambda x: cities_coord[x][1])
        self.data.to_csv(self.path, index = False)

