import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import requests
from countryinfo import CountryInfo
from PIL import Image
from geopy.distance import geodesic
from project.visualization import CityCountry, BigCities, Temperatures
from project.utils import Data


# The Sidebar class contains the data related to the creation of the sidebar menu, from which the user can choose to
# select different pages. I created the sidebar using an external additional library available on the streamlit
# website.


class Sidebar:
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.set_page_config(page_title="Weather data project", layout="wide", initial_sidebar_state="expanded", )
    with st.sidebar:
        options = option_menu("Weather data project", ["Main menu", "Cities overview", "Country information",
                                                       "Temperatures charts and map", "Temperatures shock"],
                              menu_icon="umbrella",
                              icons=["house", "pin-map", "book", "graph-up-arrow", "cloud-lightning-rain"])


# The MainMenu class contains one function, which generates the first page that the user sees when he opens the app.
# It only contains some text and images; because of this, I decided to use a streamlit property which allows to save
# the data to a cache, so that the program doesn't run every time the user goes to the main menu, but only the first
# time, with the information being cached. This thing strongly speeds up the process.


class MainMenu:
    @st.cache_data
    def main_menu(self):
        st.title("WEATHER DATA PROJECT")
        st.divider()
        st.write("""This project aims to analyze the change of temperatures from various cities around the world. Select 
                the page you wish to see from the menu on the left.""")
        st.write("For more info, check the readme file on GitHub or contact me at luca.sangiovanni.2001@gmail.com")
        st.write("Have fun!")
        st.write("")
        col1, col2, col3 = st.columns(
            [0.27, 0.38, 0.35])  # Percentage of occupation of each column (to fit the images correctly)
        url1 = "https://www.weather.gov/images/ffc/events/severe_011114/500mb_140112.png"
        url2 = ("https://image.cnbcfm.com/api/v1/image/106140709-1568982403673gettyimages-1169784640.jpeg?v=1568992875"
                "&w=740&h=416&ffmt=webp&vtcrop=y")
        url3 = ("https://images.nationalgeographic.org/image/upload/t_edhub_resource_key_image/v1638886301"
                "/EducationHub/photos/lightning-bolts.jpg")
        img1 = Image.open(requests.get(url1, stream=True).raw)
        img2 = Image.open(requests.get(url2, stream=True).raw)
        img3 = Image.open(requests.get(url3, stream=True).raw)
        col1.image(img1)
        col2.image(img2)
        col3.image(img3)


# The following class contains three functions. The first one refers to the three charts related to the cities,
# the second one refers to the function which allows to calculate the distance between two cities, and the third one
# allows to generate the map of the major cities in the dataset. Also here, the first function is cached, as it contains
# data that doesn't change (the charts are always the same).


class CitiesOverview:
    @st.cache_data
    def cities_overview(self):
        st.header("CITIES OVERVIEW")
        st.divider()
        st.write("""In this page you will be able to see an overview of the cities in the dataset. First of all,
                 just by looking at the dataset, we can see that there are some countries that are represented by a lot
                 of cities; as one would expect, the most represented countries are the most populated ones.""")
        st.write("In particular, here's a chart showing the top 15 most represented countries in the dataset:\n")
        st.text(" ")
        st.pyplot(CityCountry.byCountry_Plot(any))
        st.divider()
        st.write("In the chart below, instead, we can see how cities are distributed among continents.\n")
        st.write("")
        st.pyplot(CityCountry.byContinent_Plot(any))
        st.divider()
        st.write("Here instead we can see how cities are distributed among the sub-regions of each continent.\n")
        st.write("")
        st.pyplot(CityCountry.bySubregion_plot(any))

    def distance_calculator(self):
        st.divider()
        st.write("Here, you can calculate the distance between two cities:")
        st.write("")
        col1, col2 = st.columns([0.5, 0.5])
        col1.subheader("Choose a starting city:\n")
        col2.subheader("Choose an arriving city:\n")
        col1.continent1 = col1.selectbox("In which continent is the city located?", sorted(list(Data.cities["Continent"].unique())), index=None, placeholder="Click here to select a continent...", key="distcont1")
        col2.continent2 = col2.selectbox("In which continent is the city located?", sorted(list(Data.cities["Continent"].unique())), index=None, placeholder="Click here to select a continent...", key="distcont2")
        col1.subregion1 = col1.selectbox("In which sub-region is the city located?", sorted(list(Data.cities[Data.cities["Continent"] == col1.continent1]["Subregion"].unique())), index=None, placeholder="Click here to select a sub-region...", key="distsubr1")
        col2.subregion2 = col2.selectbox("In which sub-region is the city located?", sorted(list(Data.cities[Data.cities["Continent"] == col2.continent2]["Subregion"].unique())), index=None, placeholder="Click here to select a sub-region...", key="distsubr2")
        col1.country1 = col1.selectbox("In which country is the city located?", sorted(list(Data.cities[Data.cities["Subregion"] == col1.subregion1]["Country"].unique())), index=None, placeholder="Click here to select a country...", key="distcoun1")
        col2.country2 = col2.selectbox("In which country is the city located?", sorted(list(Data.cities[Data.cities["Subregion"] == col2.subregion2]["Country"].unique())), index=None, placeholder="Click here to select a country...", key="distcoun2")
        col1.city1 = col1.selectbox("What is the starting city?", sorted(list(Data.cities[Data.cities["Country"] == col1.country1]["City"].unique())), index=None, placeholder="Click here to select a city...", key="distcity1")
        col2.city2 = col2.selectbox("What is the arriving city?", sorted(list(Data.cities[Data.cities["Country"] == col2.country2]["City"].unique())), index=None, placeholder="Click here to select a city...", key="distcity2")
        if col1.toggle("Choose a random starting city"):
            col1.city1 = str(np.random.choice(Data.cities["City"]))
        if col2.toggle("Choose a random arriving city"):
            col2.city2 = str(np.random.choice(Data.cities["City"]))
        c1 = Data.cities[Data.cities["City"] == str(col1.city1)]
        c2 = Data.cities[Data.cities["City"] == str(col2.city2)]
        c1_coord = (c1[["Latitude", "Longitude"]]).values.flatten().tolist()
        c2_coord = (c2[["Latitude", "Longitude"]]).values.flatten().tolist()
        st.write("")
        if st.button("Calculate distance", type="primary"):
            if (col1.city1 and col2.city2) is not None:
                if col1.city1 != col2.city2:
                    distance = round(geodesic(c1_coord, c2_coord).km, 2)
                    phrase = "The distance between " + str(col1.city1) + " and " + str(col2.city2) + " is " + str(distance) + " kilometers."
                    st.write("")
                    st.write(phrase)
                else:
                    st.write("")
                    st.write("The starting city must be different from the arriving city.")
            else:
                st.write("")
                st.write("You need to select both the starting and the arriving city.")

    def major_map(self):
        st.divider()
        st.write("""All the data shown above is referring to the bigger dataset, which contains thousands of cities. 
        I also used a smaller dataset, which contains only 100 cities. Click the button below to show the map of only 
        the major cities.""")
        st.write("")
        projection = st.radio("Choose a map type", ["Equirectangular", "Orthographic"], captions=["2D map", "3D map"])
        if st.button("Show map", help="Click here to show the map of major cities", type="primary"):
            BigCities.majorCitiesMap(any, projection.lower())


# The class below contains only one function, which prints the information about a chosen country, and creates a
# map of the country. The information of each country are obtained using the library CountryInfo, which retrieves the
# data from its database; this was extremely useful, as I didn't have to store the data in a dataset, and allowed me to
# have interesting information about all the countries.


class CountryInformation:
    def country_info(self):
        random_country = np.random.choice(Data.cities["Country"].unique())
        st.header("COUNTRY INFORMATIONS")
        st.divider()
        st.write("""In this page you can see some informations about the countries present in the dataset. In addition,
                you will be able to see the map of the country, with its cities.""")
        st.write("")
        selected_continent = st.selectbox("In which continent is the city located?",
                                          sorted(list(Data.cities["Continent"].unique())),
                                          index=None, placeholder="Click here to select a continent...", key="cont1")
        selected_subregion = st.selectbox("In which sub-region is the city located?",
                                          sorted(list(Data.cities[
                                                          Data.cities["Continent"] == selected_continent][
                                                          "Subregion"].unique())), index=None,
                                          placeholder="Click here to select a sub-region...", key="sub1")
        selected_country = st.selectbox("Which country do you want to know about?", sorted(list(
            Data.cities[Data.cities["Subregion"] == selected_subregion][
                "Country"].unique())), index=None, placeholder="Click here to select a country...", key="coun1")
        if st.toggle("Choose a completely random country", help="Activate to show the data of a random country"):
            selected_country = random_country
        st.write("")
        if st.button("Show me the country information", type="primary"):
            nation = selected_country
            byNation = Data.tempByCity[Data.tempByCity.Country == nation]
            first = str(byNation.dt.iloc[0])
            latest = str(byNation.dt.iloc[-1])
            maxTemp = str(round(max(byNation.AverageTemperature), 2))
            minTemp = str(round(min(byNation.AverageTemperature), 2))
            highest = str(byNation.sort_values(by=["AverageTemperature"], ascending=False).City.iloc[0])
            lowest = str(byNation.sort_values(by=["AverageTemperature"], ascending=True).City.iloc[0])
            try:
                country_name = CountryInfo(nation).name().capitalize()
                country_area = format(CountryInfo(country_name).area(), ",d")
                country_capital = CountryInfo(country_name).capital()
                country_population = format(CountryInfo(country_name).population(), ",d")
                country_region = CountryInfo(country_name).region()
                country_subregion = CountryInfo(country_name).subregion()
                st.divider()
                st.write(("\nHere is some stats about " + nation + "\n").upper())
                st.write("")
                st.markdown("\n*WEATHER STATS:*\n")
                st.write("")
                st.write("First recorded temperature: " + Data.months[first[-5:-3]] + " " + first[:4])
                st.write("Latest recorded temperature: " + Data.months[latest[-5:-3]] + " " + latest[:4])
                st.write("Highest monthly average temperature recorded: " + maxTemp + "°C" + " in " + highest)
                st.write("Lowest monthly average temperature recorded: " + minTemp + "°C" + " in " + lowest)
                st.write("")
                st.write("")
                st.markdown("\n*OTHER INFOS:*\n")
                st.write("")
                st.write("Area (in square km): " + str(country_area))
                st.write("Population: " + str(country_population))
                st.write("Capital city: " + str(country_capital))
                st.write("Continent: " + str(country_region))
                st.write("Subregion: " + str(country_subregion))
                st.divider()
            except AttributeError:
                st.write("Please choose another country")
        if st.button("Show me the map of the country", type="primary"):
            CityCountry.byCountry_Map(any, nation=str(selected_country))


# In the following class, I created two functions: the first one allows the user to select a city, and returns two
# charts: one containing the temperatures in both january and august during the years, and one comparing the
# temperatures in 2012 to the ones in 1900. The second function, instead, given a year and a month from the user,
# generates a world map containing the temperatures of the major cities on the selected date.


class TempChartsMap:
    months_codes = list(Data.months.keys())

    def temp_charts(self):
        Data.tempByMajorCity["dt"] = pd.to_datetime(Data.tempByMajorCity["dt"])
        Data.tempByMajorCity["Month"] = Data.tempByMajorCity["dt"].dt.month
        st.header("TEMPERATURES CHARTS AND MAP")
        st.divider()
        st.write("""One thing that can be done to see how temperatures change in time is to plot the average 
        temperature registered in a city in a certain month during the years. Below, we can see the difference in 
        temperature registered in the cities present in the dataset, both in january and august.""")
        st.write("""It is also interesting to notice how temperatures change during different times of the year. You 
        can see this in the second chart, where there is a comparison between the average temperature registered in 
        the chosen city in 1900 and in 2012.""")
        st.write("")
        st.write("")
        chosen_continent = st.selectbox("In which continent is the city located?",
                                        sorted(list(Data.cities["Continent"].unique())),
                                        index=None, placeholder="Click here to select a continent...", key="cont2")
        chosen_subregion = st.selectbox("In which sub-region is the city located?",
                                        sorted(list(Data.cities[
                                                        Data.cities["Continent"] == chosen_continent][
                                                        "Subregion"].unique())),
                                        index=None, placeholder="Click here to select a sub-region...", key="sub2")
        chosen_country = st.selectbox("In which country is the city located?",
                                      sorted(list(Data.cities[
                                                      Data.cities["Subregion"] == chosen_subregion][
                                                      "Country"].unique())), index=None, placeholder="Click here to select a country...", key="coun2")
        chosen_city = st.selectbox("Of which city do you want to see the temperatures?",
                                   sorted(list(Data.cities[
                                                   Data.cities["Country"] == chosen_country][
                                                   "City"].unique())),
                                   index=None, placeholder="Click here to select a city...", key="city2")
        st.write("")
        if st.toggle("Choose a completely random city", help="Activate to show the plots of a random city in a random "
                                                             "country"):
            chosen_city = np.random.choice(Data.cities["City"])
        st.write("")
        if st.button("Show me the plots", help="Click here to show the plots", type="primary"):
            st.divider()
            st.write("")
            st.write("")
            st.pyplot(Temperatures.tempJanAug(any, chosen_city))
            st.divider()
            st.pyplot(Temperatures.tempMonths(any, chosen_city))

    def temp_map(self):
        st.divider()
        st.write("""Another useful thing to do is viewing the difference of temperatures between cities around the 
        world in the same time period. Below, you can choose a specific year and month, or let the randomness choose 
        them for you.""")
        st.write("")
        st.write("")
        selected_year = st.slider("Choose a year", min_value=1891, max_value=2013)
        if st.toggle("Choose a random year"):
            selected_year = np.random.randint(1891, 2013)
        selected_month = st.selectbox("Choose a month", TempChartsMap.months_codes, placeholder="Click here to select a month...")
        if st.toggle("Choose a random month"):
            selected_month = np.random.choice(TempChartsMap.months_codes)
        st.write("")
        st.info("""Keep in mind that the location of the following cities is wrongly displayed on the map below, 
        although the coordinates in the dataset are correct:\n - São Paulo (Brasil) -> shown in Russia\n - Saint 
        Petersburg (Russia) -> shown in Brasil\n - Salvador (Brasil) -> shown in Chile\n - Sydney (Australia) -> 
        shown in Brasil\n - Surat (India) -> shown in Australia\n - Santo Domingo (Dominican Republic) -> shown in 
        South Korea\n - Surabaya (Indonesia) -> shown in India\n - Shenyang (China) -> shown in Indonesia""", icon="ℹ️")
        st.write("")
        full_date = (str(selected_year) + "-" + str(selected_month))
        if st.button("Show me the map", type="primary"):
            st.pyplot(Temperatures.bubbleMap(any, full_date))


# The TemperaturesShock class contains one functions, which generates two charts that refer to temperature shock: the
# first one shows the cities with the biggest tempretures shock, given a chosen year, and the second one describes
# how temperatures shock has changed during the years.


class TemperaturesShock:
    def temp_shock(self):
        st.header("TEMPERATURES SHOCK")
        st.divider()
        st.write("""A good way of analyzing the weather is through the analysis of how often and how much 
        temperatures change in time. A big temperature difference in a short time may not be a good sign for the 
        climate. In the charts below you can see a list of cities that had the biggest temperatures shock in a given 
        year, and the number of cities that had a big temperature shock in the last decades. For instance, 
        I defined the temperature shock to be very significant in the case in which the difference between the 
        maximum monthly temperature registered in a year and the minimum temperature registered in a year is greater 
        than 49°C.""")
        st.write("Below, you can select a year or choose a random year, then click the button to show the charts.")
        st.write("")
        my_year = st.slider("Choose a year\n", min_value=1891, max_value=2013)
        if st.toggle("Choose a random year", help="Activate to show the plots of a random year"):
            my_year = np.random.randint(1891, 2013)
        st.write("")
        if st.button("Show me the plots", type="primary"):
            st.pyplot(Temperatures.tempShock(any, str(my_year)))
            st.divider()
            st.pyplot(Temperatures.shockByYear(any))


# This last part of the code is very important: it allows the user to show a certain page and its functions,
# based on the one he selects from the sidebar menu.


if Sidebar.options == "Main menu":
    MainMenu.main_menu(any)
elif Sidebar.options == "Cities overview":
    CitiesOverview.cities_overview(any)
    CitiesOverview.distance_calculator(any)
    CitiesOverview.major_map(any)
elif Sidebar.options == "Country information":
    CountryInformation.country_info(any)
elif Sidebar.options == "Temperatures charts and map":
    TempChartsMap.temp_charts(any)
    TempChartsMap.temp_map(any)
elif Sidebar.options == "Temperatures shock":
    TemperaturesShock.temp_shock(any)
