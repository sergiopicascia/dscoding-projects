from opencage.geocoder import OpenCageGeocode
from countryinfo import CountryInfo
import pandas as pd


# The following class contains the imported data and data that I used frequently in other functions.

class Data:
    path = "C:\\Users\sangi\Desktop\Info progetto python\Datasets"
    tempByCity = pd.read_csv(path + "\GlobalLandTemperaturesByCity.csv").dropna().reset_index(drop=True)
    tempByMajorCity = pd.read_csv(path + "\GlobalLandTemperaturesByMajorCity.csv").dropna().reset_index(drop=True)
    majorCities = pd.read_csv(path + "\majorCities.csv", index_col=0)
    cities = pd.read_csv(path + "\cities.csv", index_col=0)
    cities_old = pd.read_csv(path + "\cities_old.csv", index_col=0, on_bad_lines="skip")
    months = {"01": 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', '07': 'July',
              '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}


# I created the function add_continents, which I used to create a new CSV file. The file created is basically the
# same as cities.csv, but it contains two additional columns: one for the continent and one for the subregion. To do
# so, I used the library countryinfo. I had to skip 9 countries, because the function didn't find their data. Also,
# when creating the file, I accidentally created two identical columns; that's why, when loading the csv,
# I dropped the "Region" column. REMEMBER THAT THIS FUNCTION MUST NOT BE RUN. I INSERTED IT HERE JUST FOR INFO PURPOSES.


def add_continents():
    cities_copied = Data.cities_old.copy()
    for index, row in cities_copied.iterrows():
        my_country = row["Country"]
        if my_country in ["Côte D'Ivoire", "Burma", "Congo (Democratic Republic Of The)", "Guinea Bissau", "Congo",
                          "Gambia", "Macedonia", "Bahamas", "Montenegro"]:
            continue
        my_country_info = CountryInfo(my_country)
        my_continent = my_country_info.info().get("region")
        my_subregion = my_country_info.info().get("subregion")
        cities_copied.at[index, 'Continent'] = my_continent
        cities_copied.at[index, 'Subregion'] = my_subregion
    cities_copied.to_csv(Data.path + "\citiesWithContinents.csv")


# The following classes are the ones I used to retrieve the coordinates of the cities from the internet,
# using an API. I didn't use the original coordinates present in the dataset because they were not in the right
# format, so I decided to directly download new coordinates, and substitute the old coordinates with the downloaded
# ones. I did this thing both with the dataset of major cities and the dataset of all the cities.The only problem I
# had was with the dataset containing all the cities: the API I chose allowed only to retrieve a certain amount of
# data each day; because of this, I had to split the list of cities for which I wanted to get the coordinates in
# smaller datasets, and run them one by one. Finally, all I had to do was concatenate all the small datasets
# together, and save them as csv file.
# REMEMBER THAT THIS CODE MUST NOT BE RUN. I INSERTED IT HERE JUST FOR INFO PURPOSES.


class DownloadNewCoordinates:

    def MCconversion(self):
        majorCities = Data.tempByMajorCity[["City", "Country", "Latitude", "Longitude"]].groupby(
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
        majorCities.to_csv(Data.path + "\majorCities.csv")


class Conversion:
    cities1 = Data.cities_old.iloc[:400, :]
    cities2 = Data.cities_old.iloc[400:800, :]
    cities3 = Data.cities_old.iloc[800:1200, :]
    cities4 = Data.cities_old.iloc[1200:1600, :]
    cities5 = Data.cities_old.iloc[1600:2000, :]
    cities6 = Data.cities_old.iloc[2000:2400, :]
    cities7 = Data.cities_old.iloc[2400:2800, :]
    cities8 = Data.cities_old.iloc[2800:3200, :]
    cities9 = Data.cities_old.iloc[3200:, :]

    def citiesConversion1(self):
        key = "1867ae77e86948d9a54c0a7bb9f3d0bd"
        geocoder = OpenCageGeocode(key)
        list_lat = []
        list_lon = []
        for index, row in Data.cities1.iterrows():
            City = row["City"]
            Country = row["Country"]
            query = str(City) + ',' + str(Country)
            results = geocoder.geocode(query)
            lat = results[0]['geometry']['lat']
            lon = results[0]['geometry']['lng']
            list_lat.append(lat)
            list_lon.append(lon)
        Data.cities1['Latitude'] = list_lat
        Data.cities1['Longitude'] = list_lon
        Data.cities1.to_csv(Data.path + "\cities1.csv")

    def list_of_cities_corrected(self):
        cities1 = pd.read_csv(Data.path + "\cities1.csv", index_col=0)
        cities2 = pd.read_csv(Data.path + "\cities2.csv", index_col=0)
        cities3 = pd.read_csv(Data.path + "\cities3.csv", index_col=0)
        cities4 = pd.read_csv(Data.path + "\cities4.csv", index_col=0)
        cities5 = pd.read_csv(Data.path + "\cities5.csv", index_col=0)
        cities6 = pd.read_csv(Data.path + "\cities6.csv", index_col=0)
        cities7 = pd.read_csv(Data.path + "\cities7.csv", index_col=0)
        cities8 = pd.read_csv(Data.path + "\cities8.csv", index_col=0)
        cities9 = pd.read_csv(Data.path + "\cities9.csv", index_col=0)

        cities_old = pd.concat([cities1, cities2, cities3, cities4, cities5, cities6, cities7, cities8, cities9])
        cities_old.to_csv(Data.path + "\cities.csv")
