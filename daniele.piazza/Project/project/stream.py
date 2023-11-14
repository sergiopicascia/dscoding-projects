import streamlit as st
from location import Location
from visualize import Visualize
import pandas as pd
import os
#Change .streamlit/config.toml to change the theme color, the map will change accordingly

update = False # Set to True if you want to update the coordinates of the cities in the csv files

st.set_page_config(layout="wide")
api_key = pd.read_csv("/Users/dani/Desktop/api_key.txt",header=None)[0][0] #change with your google api key
all_path = "Data/GlobalLandTemperaturesByCity.csv"
major_path = "Data/GlobalLandTemperaturesByMajorCity.csv"

@st.cache_data
def load_location(path, api_key):
    location = Location(path, api_key)
    if update:
        location.update_file()
    return location

@st.cache_data
def load_map_data(location_data):
    vis = Visualize(location_data)
    return vis

location_major = load_location(major_path, api_key)
location_all = load_location(all_path, api_key)
major = load_map_data(location_major.data)
all = load_map_data(location_all.data)

def create_html():
    major.bubble().write_html("bubble_major.html")
    major.bubble_range().write_html("range_major.html")
    all.bubble().write_html("bubble_all.html")
    all.bubble_range().write_html("range_all.html")

@st.cache_data
def load_html(path):
    if not os.path.exists(path):
        create_html()
    with open(path, 'r') as f:
        return f.read()
    
def main():
    page = st.selectbox("Choose a page", ("General Climate Data", "Specific City Information"))
    st.title("Global Climate Data Analysis")
    dataset = st.radio("Choose a dataset", ("Major cities", "All cities"))
    if dataset == "Major cities":
        location = location_major
        st.write("This dataset includes climate data from major cities around the world.")
        vis = major
        bubble = load_html("bubble_major.html")
        range = load_html("range_major.html")
    else:
        location = location_all
        st.write("This dataset includes climate data from all cities around the world.")
        vis = all
        bubble = load_html("bubble_all.html")
        range = load_html("range_all.html")
    if page == "General Climate Data":
        st.header("General Climate Data")
        st.header("Dataset Statistics")
        city_stats = vis.additional_statistics()
        st.dataframe(city_stats, width=1400, height=420)
        max = vis.data_year['City_Country'].nunique()
        st.subheader("Temperature Range Heatmap")
        st.text("This heatmap displays the range (max-min) of temperatures for each city in the dataset.")
        number_range = st.number_input("Choose the number of cities with the highest temperature range to display on the map. Enter a number from 1 to {}. Leave empty to display all cities.".format(max), min_value=1, max_value=max, value=None)
        if number_range is None:
            st.components.v1.html(range, width=1400, height=800, scrolling=True)
        else:
            st.plotly_chart(vis.bubble_range(number_range))
        st.subheader("Average Temperature Heatmap")
        st.text("This heatmap displays the average temperature for each city in the dataset.")
        number_temp = st.number_input("Choose the number of hottest cities to display on the temperature map. Enter a number from 1 to {}. Leave empty to display all cities.".format(max), min_value=1, max_value=max, value=None)
        if number_temp is None or number_temp == max:
            st.components.v1.html(bubble, width=1400, height=800, scrolling=True)
        else:
            st.plotly_chart(vis.bubble(number_temp))
    elif page == "Specific City Information":
        country = location.data['Country'].unique()
        country.sort()
        selected_country = st.selectbox("Choose a country", ("All", *country))
        if selected_country != "All":
            city_list = location.data[location.data['Country'] == selected_country]['City_Country'].unique()
        else:
            city_list = location.data['City_Country'].unique()
        st.header("City-Specific Information")
        city_list.sort()
        selected_city = st.selectbox("Choose a City", city_list)
        st.subheader(f"Climate Data for {selected_city}")
        st.plotly_chart(vis.show_city(selected_city))
        st.subheader("Temperature Boxplot for the City")
        st.text("This boxplot shows the distribution of temperatures for the selected city.")
        boxplot = vis.boxplot(selected_city)
        st.plotly_chart(boxplot)
        st.subheader("Temperature Line Chart for the City")
        st.text("This line chart shows the temperature trends for the selected city over the years.")
        fig_city = vis.line(selected_city)
        st.plotly_chart(fig_city)
        st.subheader("Predicted Temperatures")
        st.text("This line chart shows the predicted temperatures for the next 50 years.")
        predicted_temperatures = vis.predict_city_temperature(selected_city)
        st.plotly_chart(predicted_temperatures)
        selected_year = st.selectbox("Choose a year", vis.data_year[vis.data_year['City_Country']==selected_city]['Year'].unique())
        st.subheader(f"Climate Data for {selected_city} in {selected_year}")
        st.text("This line chart shows the temperatures for the selected city during the months of the selected year.")
        fig_city_year = vis.line_year(selected_city,selected_year)
        st.plotly_chart(fig_city_year)

if __name__ == "__main__":
    main()