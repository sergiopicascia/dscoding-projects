import streamlit as st
from location import Location
from visualize import City, Country
import pandas as pd
import os
#Change .streamlit/config.toml to change the theme color, the map will change accordingly
#For all the comments i used _ =  because streamlit doesn't support """ """ comments
_ = """
 This file contains the streamlit app.
It contains the following methods:
    - load_location: load the location data
    - load_city_data: load the city data
    - load_country_data: load the country data
    - create_html: create the html files for the heatmaps
    - load_html: load the html files for the heatmaps
    - choose_dataset: choose the dataset to display
    - display_statistics: display the statistics of the dataset
    - display_heatmap: display the heatmap of the dataset
    - display_boxplot: display the boxplot of the dataset
    - display_line_chart: display the line chart of the dataset
    - display_prediction: display the prediction of the dataset
    - display_line_year: display the line chart of the dataset for a specific year
    - display_general: display the general information of the dataset
    - display_specific: display the specific information of the dataset
"""

st.set_page_config(layout = 'wide', initial_sidebar_state = 'collapsed', page_title = 'Global Climate Data Analysis', page_icon = '🌍')
API_KEY = pd.read_csv('/Users/dani/Desktop/api_key.txt', header = None)[0][0] #change with your google api key
ALL_PATH = 'Data/GlobalLandTemperaturesByCity.csv'
MAJOR_PATH = 'Data/GlobalLandTemperaturesByMajorCity.csv'
COUNTRY_PATH = 'Data/GlobalLandTemperaturesByCountry.csv'

_ = """
Load the location data

Parameters
----------
path : str
    Path of the CSV file
API_KEY : str
    Google API key

Returns
-------
location : Location
    Location object
"""
@st.cache_data
def load_location(path, API_KEY):
    location = Location(path, API_KEY)
    return location

_ = """
Load the city data

Parameters
----------
data : pandas.core.frame.DataFrame
    Dataframe with data from the cities about the temperature

Returns
-------
city : City
    City object
"""
@st.cache_data
def load_city_data(data):
    city = City(data)
    return city

_ = """
Load the country data

Parameters
----------
path : str
    Path of the CSV file

Returns
-------
country : Country
    Country object
"""
@st.cache_data
def load_country_data(path):
    country = Country(path)
    return country

major = load_city_data(load_location(MAJOR_PATH, API_KEY).data)
all = load_city_data(load_location(ALL_PATH, API_KEY).data)
country = load_country_data(COUNTRY_PATH)

_ = """
Create the html files for the heatmaps
"""
def create_html():
    major.temperature().write_html('temperature_major.html')
    major.range().write_html('range_major.html')
    all.temperature().write_html('temperature_all.html')
    all.range().write_html('range_all.html')

_ = """
Load the html files for the heatmaps. If the file doesn't exist, create it.

Parameters
----------
path : str
    Path of the html file

Returns
-------
html : str
    Html file
"""
@st.cache_data
def load_html(path):
    if not os.path.exists(path):
        create_html()
    with open(path, 'r') as f:
        return f.read()
    
_ = """
Choose the dataset to display

Returns
-------
vis : City
    City object
temperature : str 
    Html file for the temperature heatmap
range : str
    Html file for the range heatmap
"""
def choose_dataset(general = True):
    dataset = st.radio('Choose a dataset', ('Major cities', 'All cities'))
    st.write(f'This dataset contains the climate data from {dataset.lower()} around the world.')
    vis = major if dataset  ==  'Major cities' else all
    temperature = None
    range = None
    if general:
        temperature = load_html(f'temperature_{dataset.lower().split()[0]}.html')
        range = load_html(f'range_{dataset.lower().split()[0]}.html')
    return vis, temperature, range

_ = """
Display the statistics of the dataset

Parameters
----------
data : City or Country
    City or Country object
label : str
    Label of the dataset
"""
def display_statistics(place, label):
    st.subheader('Dataset Statistics')
    stats = place.statistics()
    stats = stats.rename(columns = {
        'AverageTemperature': 'Average Temperature', 
        'MinTemperature': 'Minimum Temperature', 
        'MaxTemperature': 'Maximum Temperature', 
        'Std': 'Standard Deviation', 
    })
    stats.index.name = label
    st.dataframe(stats, width = 1400, height = 420)

_ = """
Display the heatmap of the dataset

Parameters
----------
place : City or Country
    City or Country object
average : bool
    True if the heatmap is for the average temperature, False if it is for the temperature range
label : str
    Label of the dataset
html : str
    Html file for the heatmap
"""
def display_heatmap(place, average, label, html = None):
    max = None
    number = None
    high = None
    if average:
        st.subheader('Average Temperature Heatmap')
        caption = 'average'
        if label.lower()  ==  'city':
            order = st.radio('Choose the order of the cities', ('Descending (From the *hottest*)', 'Ascending (From the *coldest*)'))
            high = True if order  ==  'Descending (Hottest)' else False
            caption_number = 'hottest' if high else 'coldest'
    else:
        st.subheader('Temperature Range Heatmap')
        caption_number = 'most significant temperature range'
        caption = 'range (max-min)'
    if label.lower()  ==  'city':  
        max = place.data_year['City_Country'].nunique()
        number = st.number_input(f'Choose the number of {caption_number} cities to display on the map. Enter a number from 1 to {max}.', min_value = 1, max_value = max, value = max)
    st.caption(f'This heatmap displays the {caption} of the temperatures for each {label.lower()} in the dataset.')
    if number  ==  max and html is not None:
        st.components.v1.html(html, width = 1400, height = 800, scrolling = True)
    else:
        st.plotly_chart(place.temperature(number, high) if average else place.range(number))

_ = """
Display the boxplot of the dataset

Parameters
----------
place : City or Country
    City or Country object
selected : str
    Selected city or country
"""
def display_boxplot(place, selected):
    st.subheader(f'Temperature Boxplot for {selected}')
    st.caption(f'This boxplot shows the distribution of temperatures for {selected} overviewing each month.')
    boxplot = place.boxplot(selected)
    st.plotly_chart(boxplot)

_ = """
Display the line chart of the dataset

Parameters
----------
place : City or Country
    City or Country object
selected : str
    Selected city or country
"""
def display_line_chart(place, selected):
    st.subheader(f'Temperature Line Chart for {selected}')
    st.caption(f'This line chart shows the temperature trends for {selected} over the years.')
    fig = place.line(selected)
    st.plotly_chart(fig)

_ = """
Display the prediction of the dataset

Parameters
----------
place : City or Country
    City or Country object
selected : str
    Selected city or country
"""
def display_prediction(place, selected):
    st.subheader("Temperature's Prediction")
    next = st.slider('Choose the number of years to predict', min_value = 1, max_value = 100, value = 50)
    st.caption(f'This line chart shows the predicted temperatures for the next {next} years.')
    predicted_temperatures = place.predict_temperature(selected, next)
    st.plotly_chart(predicted_temperatures)

_ = """
Display the line chart of the dataset for a specific year

Parameters
----------
place : City or Country
    City or Country object
selected : str
    Selected city or country
year : int
    Selected year
upper : str
    Upper level of the dataset (Country or Continent)
"""
def display_line_year(place, selected, year, upper):
    st.subheader(f'Climate Data for {selected} in {year}')
    st.caption(f'This line chart shows the temperatures for {selected} during the months of {year}.')
    fig = place.line_year(selected, year, upper)
    st.plotly_chart(fig)
_ = """
Display the general information of the dataset

Parameters
----------
place : City or Country
    City or Country object
label : str
    Label of the dataset
temperature : str
    Html file for the temperature heatmap
range : str
    Html file for the range heatmap
"""
def display_general(place, label, temperature = None, range = None):
    display_statistics(place, label)
    display_heatmap(place, False, label, range)
    display_heatmap(place, True, label, temperature)

_ = """
Display the specific information of the dataset

Parameters
----------
place : City or Country
    City or Country object
label : str
    Label of the dataset
"""
def display_specific(place, label):
    if label  ==  'City':
        upper = 'Country'
        filter = 'City_Country'
    else:
        upper = 'Continent'
        filter = label
    unique = place.data_year[upper].unique()
    unique.sort()
    selected = st.selectbox(f'Choose a {upper}', ('All', *unique))
    if selected !=  'All':
        places = place.data_year[place.data_year[upper]  ==  selected][filter].unique()
    else:
        places = place.data_year[filter].unique()
    places.sort()
    selected_place = st.selectbox(f'Choose a {label}', places, placeholder = f'Select a {label}', index = None)
    if selected_place is not None:
        st.header(f'Climate Data for {selected_place}')
        if label  ==  'City':
            st.plotly_chart(place.show_city(selected_place))
        display_boxplot(place, selected_place)
        display_line_chart(place, selected_place)
        display_prediction(place, selected_place)
        selected_year = st.selectbox('Choose a year', place.data_year[place.data_year[filter] == selected_place]['Year'].unique())
        display_line_year(place, selected_place, selected_year, upper)

def main():
    st.title('Global Climate Data Analysis')
    page = st.selectbox('Select a page', ('General Cities Data', 'Specific City Information', 'General Countries Data', 'Specific Country Information'))
    if page  ==  'General Cities Data':
        city, temperature, range = choose_dataset()
        display_general(city, 'City', temperature, range)
    elif page  ==  'Specific City Information':
        city, _, _ = choose_dataset()
        display_specific(city, 'City')
    elif page  ==  'General Countries Data':
        display_general(country, 'Country')
    elif page  ==  'Specific Country Information':
        display_specific(country, 'Country')

if __name__  ==  '__main__':
    main()