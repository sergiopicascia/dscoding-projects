import pandas as pd
import requests
class Location:
    def __init__(self, path, api_key):
        self.path = path
        self.api_key = api_key
        self.data = pd.read_csv(path)

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
        for i in range(len(cities)):
            coord = self._google_coords(cities.iloc[i])
            if coord is not None:
                cities_coord[cities['City'][i]] = coord
            else :
                cities_coord[cities['City'][i]] = self._coordinates(cities.iloc[i])
        return cities_coord


    def update_file(self):
            cities_coord = self.get_coordinates()
            self.data['Latitude'] = self.data['City'].map(lambda x: cities_coord[x][0])
            self.data['Longitude'] = self.data['City'].map(lambda x: cities_coord[x][1])
            self.data.to_csv(self.path, index=False)
