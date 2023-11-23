import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from geopy.distance import geodesic
from countryinfo import CountryInfo
from project.utils import Data


class CityCountry:
    numCities = Data.cities.drop(["Latitude", "Longitude", "Continent", "Subregion"], axis=1).groupby(
        "Country").count().sort_values(by="City", ascending=False)

    # The following function prints a small dataframe containing the countries that have most cities in the dataset.

    def byCountry_List(self):
        count_cities = CityCountry.numCities.copy()
        count_cities.columns = ["Number of cities"]
        return count_cities.head(15)

    # The function below plots the data of the previous function, using a bar plot.

    def byCountry_Plot(self):
        plt.figure(figsize=(12, 5))
        plt.bar(CityCountry.numCities.index[:15], CityCountry.numCities.City[:15], color="brown")
        plt.xticks(rotation=70)
        plt.title("Number of cities in the dataset, by country\n", fontsize=18)

    # The following function generates a map of a chosen country, showing all the cities that are part of it.

    def byCountry_Map(self, nation):
        byCountry = Data.cities[Data.cities["Country"] == nation]
        number = str(byCountry["City"].count())
        if number == "1":
            mapTitle = str("There is " + number + " city in " + nation)
        else:
            mapTitle = str("There are " + number + " cities in " + nation)
        fig = px.scatter_geo(byCountry, lat=byCountry["Latitude"], lon=byCountry["Longitude"],
                             hover_name=byCountry["City"], color_discrete_sequence=["DarkRed"])
        fig.update_geos(showocean=True, oceancolor="LightBlue", fitbounds="locations", showcountries=True,
                        showland=True, landcolor="LightGreen")
        fig.update_layout(title_text=mapTitle, title_x=0.5)
        fig.show()

    # The function below creates a bar plot containing the cities of the dataset, divided by continent.

    def byContinent_Plot(self):
        byContinent = Data.cities.value_counts("Continent")
        sns.barplot(byContinent, orient="y", color="MediumOrchid")
        plt.title("Number of cities in the dataset, by continent\n", fontsize=18)
        plt.xlabel("")
        plt.ylabel("")
        plt.show()

    # The following function generates a plot containing subplots of the cities divided by continent and by subregion.

    def bySubregion_plot(self):
        grouped_asia = Data.cities[Data.cities["Continent"] == "Asia"]
        subregions_asia = grouped_asia["Subregion"].value_counts()
        grouped_americas = Data.cities[Data.cities["Continent"] == "Americas"]
        subregions_americas = grouped_americas["Subregion"].value_counts()
        grouped_europe = Data.cities[Data.cities["Continent"] == "Europe"]
        subregions_europe = grouped_europe["Subregion"].value_counts()
        grouped_africa = Data.cities[Data.cities["Continent"] == "Africa"]
        subregions_africa = grouped_africa["Subregion"].value_counts()
        grouped_oceania = Data.cities[Data.cities["Continent"] == "Oceania"]
        subregions_oceania = grouped_oceania["Subregion"].value_counts()
        fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(12, 15), constrained_layout=True)
        fig.suptitle("Number of cities in the dataset, by subregion\n", fontsize=18)
        fig.supylabel("Number of cities\n", fontsize=14)
        ax1.set_title("\nAsia\n", fontsize=14)
        ax2.set_title("\nAmericas\n", fontsize=14)
        ax3.set_title("\nEurope\n", fontsize=14)
        ax4.set_title("\nAfrica\n", fontsize=14)
        ax5.set_title("\nOceania\n", fontsize=14)
        sns.barplot(subregions_asia, ax=ax1, color="DarkGreen")
        sns.barplot(subregions_americas, ax=ax2, color="RoyalBlue")
        sns.barplot(subregions_europe, ax=ax3, color="DarkGoldenRod")
        sns.barplot(subregions_africa, ax=ax4, color="LightCoral")
        sns.barplot(subregions_oceania, ax=ax5, color="Teal")
        fig.show()

    # The function below calculates the distance between two cities, by using the geodesic function.

    def cities_distance(self, city1, city2):
        c1 = Data.cities[Data.cities["City"] == str(city1)]
        c2 = Data.cities[Data.cities["City"] == str(city2)]
        c1_coord = (c1[["Latitude", "Longitude"]]).values.flatten().tolist()
        c2_coord = (c2[["Latitude", "Longitude"]]).values.flatten().tolist()
        distance = round(geodesic(c1_coord, c2_coord).km, 2)
        phrase = "The distance between " + str(city1) + " and " + str(city2) + " is " + str(distance) + " kilometers."
        return phrase


class BigCities:

    # This function generates a map which shows all the major cities in the dataset (100 cities). Based on the user
    # input, the map will be 3D or 2D.

    def majorCitiesMap(self, projection):
        geo_df = gpd.read_file(r"C:\Users\sangi\Desktop\Info progetto python\Datasets\majorCities.csv", index_col=0)
        fig = px.scatter_geo(geo_df, lat="Latitude", lon="Longitude", hover_name="City",
                             hover_data=["Country", "Latitude", "Longitude"])
        fig.update_geos(showocean=True, oceancolor="grey", projection_type=projection)
        fig.update_layout(title_text="List of major cities in the dataset\n", title_x=0.5)
        fig.show()


class Temperatures:

    # The function below shows the temperatures in january and august during the years, given a city name.

    def tempJanAug(self, city_name):
        temp = Data.tempByCity[Data.tempByCity["City"] == city_name]
        tempJan = temp[temp["dt"].str.contains("5-01-01")]
        tempAug = temp[temp["dt"].str.contains("5-08-01")]
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(17, 8))
        fig.suptitle("Temperatures in " + city_name + " during the years\n", fontsize=18)
        ax1.plot(tempJan["dt"], tempJan["AverageTemperature"], color="b")
        ax2.plot(tempAug["dt"], tempAug["AverageTemperature"], color="r")
        ax1.set_title("January\n", fontsize=14)
        ax2.set_title("August\n", fontsize=14)
        ax1.set_xticks(tempJan.dt, tempJan.dt.str[:4], fontsize=12)
        ax2.set_xticks(tempAug.dt, tempAug.dt.str[:4], fontsize=12)
        fig.supylabel("Temperatures (°C)", fontsize=14)
        plt.subplots_adjust(bottom=0.15, top=0.85, hspace=0.8)
        plt.show()

    # The following function shows a comparison between the temperatures in 2012 and in 1900, given a city name.

    def tempMonths(self, city_name):
        temp = Data.tempByCity[Data.tempByCity["City"] == city_name]
        t1900 = temp[temp["dt"].str.contains("1900")]
        t2012 = temp[temp["dt"].str.contains("2012")]
        fig = plt.figure(figsize=(15, 6))
        ax1 = fig.add_subplot(111, label="1")
        ax2 = fig.add_subplot(111, label="2",
                              frame_on=False)  # I don't want the plot rectangle to be shown, otherwise it would overlap with the other rectangle
        ax1.plot(t1900["dt"], t1900["AverageTemperature"], label="1900", color="DarkGreen")
        ax2.plot(t2012["dt"], t2012["AverageTemperature"], label="2012", color="DarkBlue")
        ax1.tick_params(left=False, labelleft=False, bottom=False,
                        labelbottom=False)  # I hide the labels and values of ax1, so that they don't overlap with ax2
        plt.xticks(t2012["dt"], Data.months.values(), rotation=50, fontsize=12)
        plt.yticks(fontsize=12)
        plt.title("Temperatures in " + city_name + " in 1900 and 2012\n", fontsize=18)
        plt.ylabel("Temperatures (°C)\n", fontsize=14)
        fig.legend()
        plt.grid(True)
        plt.show()

    # This function creates a bubble map, which contains the data of the temperatures of the major world cities in a
    # given year and month.

    def bubbleMap(self, selected_date):
        titleText = "Average temperature in " + Data.months[selected_date[-2:]] + " " + selected_date[:4]
        tempMonthYear = Data.tempByMajorCity[Data.tempByMajorCity["dt"] == selected_date + "-01"]
        for index, row in tempMonthYear.iterrows():
            bubbleScale = (tempMonthYear["AverageTemperature"] + 30)
        fig = px.scatter_geo(tempMonthYear, lat=Data.majorCities["Latitude"], lon=Data.majorCities["Longitude"],
                             size=bubbleScale,
                             hover_name=tempMonthYear["City"], color=tempMonthYear["AverageTemperature"],
                             color_continuous_scale=px.colors.sequential.Hot_r,
                             hover_data=["Country", "AverageTemperature"])
        fig.update_geos(showocean=True, oceancolor="Lightblue", fitbounds="locations")
        fig.update_layout(title_text=titleText, title_x=0.47)
        fig.show()

    # The function below shows some information about a chosen country. In the first part, the data is taken from the
    # temperatures dataset, while the other info are obtained using the CountryInfo package, which contains a
    # database of all the world countries. I inserted the exception in the case in which there is some country not
    # recognised by the library (maybe because it has a different name).

    def countryStats(self, nation):
        byNation = Data.tempByCity[Data.tempByCity["Country"] == nation]
        first = str(byNation.dt.iloc[0])
        latest = str(byNation.dt.iloc[-1])
        maxTemp = str(round(max(byNation.AverageTemperature), 2))
        minTemp = str(round(min(byNation.AverageTemperature), 2))
        highest = str(byNation.sort_values(by=["AverageTemperature"], ascending=False).City.iloc[0])
        lowest = str(byNation.sort_values(by=["AverageTemperature"], ascending=True).City.iloc[0])
        try:
            random_country = CountryInfo(nation).name().capitalize()
            country_area = format(CountryInfo(random_country).area(),
                                  ",d")  # I use the format function to show separators between numbers
            country_capital = CountryInfo(random_country).capital()
            country_population = format(CountryInfo(random_country).population(), ",d")
            country_region = CountryInfo(random_country).region()
            country_subregion = CountryInfo(random_country).subregion()
            print(("\nHere is some stats about " + nation + "\n").upper())
            print("-" * 80)
            print("\nWEATHER STATS:\n")
            print("First recorded temperature: " + Data.months[first[-5:-3]] + " " + first[:4])
            print("Latest recorded temperature: " + Data.months[latest[-5:-3]] + " " + latest[:4])
            print("Highest monthly average temperature recorded: " + maxTemp + "°C" + " in " + highest)
            print("Lowest monthly average temperature recorded: " + minTemp + "°C" + " in " + lowest)
            print("\n" + "-" * 80)
            print("\nOTHER INFOS:\n")
            print("Area (in square km): " + str(country_area))
            print("Population: " + str(country_population))
            print("Capital city: " + str(country_capital))
            print("Continent: " + str(country_region))
            print("Subregion: " + str(country_subregion))
        except KeyError:
            print("Please choose another country")

    # This function creates a bar plot which contains the cities with the highest temperature shock in a chosen year.

    def tempShock(self, chosen_year):
        tempYear = Data.tempByCity[Data.tempByCity["dt"].str.contains(chosen_year)].drop(
            ["Latitude", "Longitude", "AverageTemperatureUncertainty"], axis=1)
        minTemp = tempYear.groupby("City").min("AverageTemperature")
        minTemp.rename(columns={"AverageTemperature": "MinimumTemperature"}, inplace=True)
        maxTemp = tempYear.groupby("City").max("AverageTemperature")
        maxTemp.rename(columns={"AverageTemperature": "MaximumTemperature"}, inplace=True)
        temp1 = pd.concat([minTemp, maxTemp], axis=1, join="inner")
        temp1["TempDifference"] = temp1["MaximumTemperature"] - temp1["MinimumTemperature"]
        tempDiff = temp1.sort_values(by="TempDifference", ascending=False)
        plt.figure(figsize=(15, 6))
        fig = tempDiff["TempDifference"][:10].plot(kind="barh", color="SaddleBrown")
        fig.set_xlim(left=40)
        plt.title(
            "Cities with the biggest difference between highest and lowest temperature in " + str(chosen_year) + "\n",
            fontsize=18)
        plt.xlabel("\nTemperature shock (°C)", fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.show()

    # The function below generates a plot showing the number of cities that have a temperature shock greater than 49
    # degrees, by year.

    def shockByYear(self):
        temp = Data.tempByCity.drop(["AverageTemperatureUncertainty", "Latitude", "Longitude"], axis=1)
        temp["year"] = temp["dt"].str.slice(0, 4)
        max = temp.groupby(["City", "year"]).max("AverageTemperature")
        max.rename(columns={"AverageTemperature": "MaximumTemperature"}, inplace=True)
        min = temp.groupby(["City", "year"]).min("AverageTemperature")
        min.rename(columns={"AverageTemperature": "MinimumTemperature"}, inplace=True)
        temp_minmax = pd.concat([min, max], axis=1, join="inner").reset_index()
        temp_minmax["TempDifference"] = temp_minmax["MaximumTemperature"] - temp_minmax["MinimumTemperature"]
        temp_withDiff = temp_minmax.sort_values(by=["year", "TempDifference"], ascending=(True, False))
        temp49 = temp_withDiff[temp_withDiff["TempDifference"] > 49].value_counts().reset_index().rename(
            columns={"count": "TimesAbove49"}).sort_values(by="year")
        temp_counted = temp49["year"].value_counts().sort_values(ascending=False).reset_index()
        temp_shock = temp_counted.sort_values(by="year")
        plt.figure(figsize=(20, 6))
        plt.plot(temp_shock["year"], temp_shock["count"], color="mediumseagreen")
        plt.xticks(temp_shock["year"][0::10], fontsize=12)
        plt.yticks(fontsize=12)
        plt.title("Number of cities with a yearly temperature shock greater than 49°C, by year\n", fontsize=18)
        plt.show()
