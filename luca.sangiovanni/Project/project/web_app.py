import streamlit as st
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import requests
from countryinfo import CountryInfo
from PIL import Image
from project.visualization import CityCountry, BigCities, Temperatures
from project.utils import Data


st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Weather data project", layout="wide", initial_sidebar_state="expanded",)
with st.sidebar:
    options = option_menu("Weather data project", ["Main menu", "Cities overview", "Country informations",
                                                   "Temperatures charts and map", "Temperatures shock"], menu_icon="umbrella",
                          icons=["house", "pin-map", "book", "graph-up-arrow", "cloud-lightning-rain"])

def main_page():
    st.title("WEATHER DATA PROJECT")
    st.divider()
    st.write("""This project aims to analyze the change of temperatures from various cities around the world. Select 
            the page you wish to see from the menu on the left.""")
    st.write("For more info, check the readme file on GitHub or contact me at luca.sangiovanni.2001@gmail.com")
    st.write("Have fun!")
    st.write("")
    col1, col2, col3 = st.columns([0.27, 0.38, 0.35]) # Percentage of occupation of each column (to fit the images correclty)
    url1 = "https://www.weather.gov/images/ffc/events/severe_011114/500mb_140112.png"
    url2 = "https://image.cnbcfm.com/api/v1/image/106140709-1568982403673gettyimages-1169784640.jpeg?v=1568992875&w=740&h=416&ffmt=webp&vtcrop=y"
    url3 = "https://images.nationalgeographic.org/image/upload/t_edhub_resource_key_image/v1638886301/EducationHub/photos/lightning-bolts.jpg"
    img1 = Image.open(requests.get(url1, stream=True).raw)
    img2 = Image.open(requests.get(url2, stream=True).raw)
    img3 = Image.open(requests.get(url3, stream=True).raw)
    col1.image(img1)
    col2.image(img2)
    col3.image(img3)

def cities_overview():
    st.header("CITIES OVERVIEW")
    st.divider()
    st.write("""In this page you will be able to see an overview of the cities in the dataset. First of all,
             just by loking at the dataset, we can see that there are some countries that are represented by a lot
             of cities; as one would expect, the most represented countries are the most populated ones.""")
    st.write("In particular, here's a chart showing the top 15 most represented countries in the dataset:\n")
    st.text(" ")
    st.pyplot(CityCountry.byCountry_Plot(any))
    st.divider()
    st.write("""The data shown above is referring to the bigger dataset, which contains thousands of cities. I also 
            used a smaller dataset, which contains only 100 cities. Click the button below to show the map of only
             the major cities.""")
    st.write("")
    if st.button("Show map", help="Click here to show the map of major cities", type="primary"):
        BigCities.majorCitiesMap(any)


def country_info():
    random_country = np.random.choice(Data.cities["Country"].unique())
    st.header("COUNTRY INFORMATIONS")
    st.divider()
    st.write("""In this page you can see some informations about the countries present in the dataset. In addition,
            you will be able to see the map of the country, with its cities.""")
    st.write("")
    selected_country = st.selectbox("Which country do you want to know about?", sorted(list(Data.cities["Country"].unique())),
                                    placeholder="Click here to select a country...")
    if st.toggle("Choose a random country", help="Activate to show the data of a random country"):
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


def temp_charts_map():
    months_codes = list(Data.months.keys())
    months_names = list(Data.months.values())
    Data.tempByMajorCity["dt"] = pd.to_datetime(Data.tempByMajorCity["dt"])
    Data.tempByMajorCity["Month"] = Data.tempByMajorCity["dt"].dt.month
    st.header("TEMPERATURES CHARTS AND MAP")
    st.divider()
    st.write("""One thing that can be done to see how temperatures change in time is to plot the average temperature
            registered in a city in a certain month during the years. Below, we can see the difference in temperature 
            registered in the cities present in the dataset, both in january and august.""")
    st.write("""It is also interesting to noctice how temperatures change during different times of the year. You can see
            this in the second chart, where there is a comparison between the average temperature registered in the chosen
             city in 1900 and in 2012.""")
    st.write("")
    st.write("")
    selected_country = st.selectbox("Of which country do you want to see the temperatures?", sorted(list(Data.cities["Country"].unique())),
                                placeholder="Click here to select a country...")
    selected_city = st.selectbox("And of which city of the selected country do you want to see the temperatures?",
                                 sorted(list(Data.cities[Data.cities["Country"] == selected_country]["City"])),
                                placeholder="Click here to select a city...")
    st.write("")
    if st.toggle("Choose a random city", help="Activate to show the plots of a random city in a random country"):
        selected_city = np.random.choice(Data.cities["City"])
    st.write("")
    if st.button("Show me the plots", help="Click here to show the plots", type="primary"):
        st.divider()
        st.write("")
        st.write("")
        st.pyplot(Temperatures.tempJanAug(any, selected_city))
        st.divider()
        st.pyplot(Temperatures.tempMonths(any, selected_city))
    st.divider()
    st.write("""Another useful thing to do is viewing the difference of temperatures between cities around the world in
            the same time period. Below, you can choose a specific year and month, or let the randomness choose them for
            you.""")
    st.write("")
    st.write("")
    selected_year = st.slider("Choose a year", min_value=1891, max_value=2013)
    if st.toggle("Choose a random year"):
        selected_year = np.random.randint(1891, 2013)
    selected_month = st.selectbox("Choose a month", months_codes, placeholder="Click here to select a month...")
    if st.toggle("Choose a random month"):
        selected_month = np.random.choice(months_codes)
    st.write("")
    st.info("""Keep in mind that the location of the following cities is wrongly displayed on the map below, although 
            the coordinates in the dataset are correct:\n
            - São Paulo (Brasil) -> shown in Russia\n
            - Saint Petersburg (Russia) -> shown in Brasil\n
            - Salvador (Brasil) -> shown in Chile\n
            - Sydney (Australia) -> shown in Brasil\n
            - Surat (India) -> shown in Australia\n
            - Santo Domingo (Dominican Republic) -> shown in South Korea\n
            - Surabaya (Indonesia) -> shown in India\n
            - Shenyang (China) -> shown in Indonesia""", icon="ℹ️")
    st.write("")
    full_date = (str(selected_year) + "-" + str(selected_month))
    if st.button("Show me the map", type="primary"):
            st.pyplot(Temperatures.bubbleMap(any, full_date))


def temp_shock():
    st.header("TEMPERATURES SHOCK")
    st.divider()
    st.write("""A good way of analyzing the weather is through the analysis of how often and how much temperatures
            change in time. A big temperature difference in a short time may not be a good sign for the climate.
            In the charts below you can see a list of cities that had the biggest temperatures shock in a given year, 
            and the number of cities that had a big temperature shock in the last decades. For instance, I defined
            the temperature shock to be very significant in the case in which the difference between the maximum monthly
            temperature registered in a year and the minimum temperature registered in a year is greater than 49°C.""")
    st.write("Below, you can select a year or choose a random year, then click the button to show the charts.")
    st.write("")
    my_year = st.slider("Choose a year\n", min_value=1891, max_value=2013)
    if st.toggle("Choose a random year", help="Activate to show the plots of a random year"):
        my_year=np.random.randint(1891, 2013)
    st.write("")
    if st.button("Show me the plots", type="primary"):
        st.pyplot(Temperatures.tempShock(any, str(my_year)))
        st.divider()
        st.pyplot(Temperatures.shockByYear(any))


if options == "Main menu":
    main_page()
elif options == "Cities overview":
    cities_overview()
elif options == "Country informations":
    country_info()
elif options == "Temperatures charts and map":
    temp_charts_map()
elif options == "Temperatures shock":
    temp_shock()
