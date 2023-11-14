import pandas as pd
import requests
class Location:
    def __init__(self, path, api_key):
        self.path = path
        self.api_key = api_key
        self.data = pd.read_csv(path,index_col=False)
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        self.data['Year'] = self.data['dt'].dt.year
        self.data['City_Country'] = self.data['City'] + ', ' + self.data['Country']
    
    def _coords(self,x):
        sign = 1 if x[-1] in ('N', 'E') else -1
        return sign * float(x[:-1])

    def _coordinates(self,city):
        return [self._coords(city['Latitude']), self._coords(city['Longitude'])]

    def _google_coords(self,city):
        try:
            base_url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                "address": f"{city['City']}, {city['Country']}",
                "key": self.api_key
            }
            response = requests.get(base_url, params=params).json()
            if response['status'] == "OK":
                location = response['results'][0]['geometry']['location']
                return [location['lat'], location['lng']]
            else:
                print(f"Error getting coordinates for {city['City']}: {response['status']}")
        except Exception as e:
            print(f"Error getting coordinates for {city['City']}: {str(e)}")
        return None

    def get_coordinates(self):
        cities = self.data[['City', 'Country', 'Latitude', 'Longitude']].drop_duplicates().reset_index(drop=True)
        cities_coord = {}
        for i in range(cities.shape[0]):
            city = cities.iloc[i]['City']
            country = cities.iloc[i]['Country']
            city_country = f"{city}, {country}"
            if city_country not in cities_coord:
                coord = self._google_coords(cities.iloc[i])
                if coord is not None:
                    cities_coord[city_country] = coord
                else:
                    cities_coord[city_country] = self._coordinates(cities.iloc[i])
        return cities_coord

    def update_file(self):
        cities_coord = self.get_coordinates()
        self.data['City_Country'] = self.data['City'] + ', ' + self.data['Country']
        self.data['Latitude'] = self.data['City_Country'].map(lambda x: cities_coord[x][0])
        self.data['Longitude'] = self.data['City_Country'].map(lambda x: cities_coord[x][1])
        self.data.drop(columns='City_Country', inplace=True)
        self.data.to_csv(self.path, index=False)

