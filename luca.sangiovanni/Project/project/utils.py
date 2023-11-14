from opencage.geocoder import OpenCageGeocode


class DownloadNewCoordinates:

    def MCconversion(self):

        majorCities = tempByMajorCity[["City", "Country", "Latitude", "Longitude"]].groupby(
            ["City"]).first().reset_index()
        key = "1867ae77e86948d9a54c0a7bb9f3d0bd"
        geocoder = OpenCageGeocode(key)
        list_lat = []
        list_lon = []
        for index, row in majorCities.iterrows():
            City = row["City"]
            Country = row["Country"]
            query = str(City) + ',' + str(Country)
            results = geocoder.geocode(query)
            lat = results[0]['geometry']['lat']
            lon = results[0]['geometry']['lng']
            list_lat.append(lat)
            list_lon.append(lon)
        majorCities['Latitude'] = list_lat
        majorCities['Longitude'] = list_lon
        MCconversion()
        majorCities.to_csv(path + "\majorCities.csv")


class Conversion():

    cities1 = cities.iloc[:400, :]
    cities2 = cities.iloc[400:800, :]
    cities3 = cities.iloc[800:1200, :]
    cities4 = cities.iloc[1200:1600, :]
    cities5 = cities.iloc[1600:2000, :]
    cities6 = cities.iloc[2000:2400, :]
    cities7 = cities.iloc[2400:2800, :]
    cities8 = cities.iloc[2800:3200, :]
    cities9 = cities.iloc[3200:, :]

    def citiesConversion1(self):

        key = "1867ae77e86948d9a54c0a7bb9f3d0bd"
        geocoder = OpenCageGeocode(key)
        list_lat = []
        list_lon = []
        for index, row in cities.iterrows():
            City = row["City"]
            Country = row["Country"]
            query = str(City) + ',' + str(Country)
            results = geocoder.geocode(query)
            lat = results[0]['geometry']['lat']
            lon = results[0]['geometry']['lng']
            list_lat.append(lat)
            list_lon.append(lon)
        cities['Latitude'] = list_lat
        cities['Longitude'] = list_lon
        citiesConversion1()
        cities1.to_csv(path + "\cities1.csv")


    def list_of_cities_corrected(self):

        cities1 = pd.read_csv(path + "\cities1.csv", index_col=0)
        cities2 = pd.read_csv(path + "\cities2.csv", index_col=0)
        cities3 = pd.read_csv(path + "\cities3.csv", index_col=0)
        cities4 = pd.read_csv(path + "\cities4.csv", index_col=0)
        cities5 = pd.read_csv(path + "\cities5.csv", index_col=0)
        cities6 = pd.read_csv(path + "\cities6.csv", index_col=0)
        cities7 = pd.read_csv(path + "\cities7.csv", index_col=0)
        cities8 = pd.read_csv(path + "\cities8.csv", index_col=0)
        cities9 = pd.read_csv(path + "\cities9.csv", index_col=0)

        cities = pd.concat([cities1, cities2, cities3, cities4, cities5, cities6, cities7, cities8, cities9])
        cities.to_csv(path + "\cities.csv")
