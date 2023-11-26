import streamlit as st
import pandas as pd


# importing all the classes needed
from datasets import DataProcessor
from mappe import Mappe
from statistiche import Statistiche
from dati import TempVar


# importing datas
folder_path = "/Users/apple/Desktop/project"
data_processor = DataProcessor(folder_path)


country = data_processor.load_country_data()
major = data_processor.load_majorcity_data()
state = data_processor.load_state_data()

# datasets info (to create them use the GetDataInfo class in datasets.py)
# but they're already in the data folder
info_city = pd.read_csv(folder_path + "/data/InfoCountry_city.csv")
info_country = pd.read_csv(folder_path + "/data/InfoCountry_country.csv")
info_major = pd.read_csv(folder_path + "/data/InfoCountry_major.csv")
info_state = pd.read_csv(folder_path + "/data/InfoCountry_state.csv")





# Setta il titolo dell'app e la configurazione della pagina
st.set_page_config(
    page_title="Weather App",
    page_icon=":sunny:",
    layout="wide",
    initial_sidebar_state="auto"
)


st.markdown("<h1 style='text-align: center; color: #F70F74;'>Weather App</h1>", unsafe_allow_html=True)



option = st.selectbox(
    '',
    ('Statistics', 'Maps', 'Datasets',)
)



if option == 'Statistics':

    st.title('Temperature Statistics')

    dataset_option = st.selectbox(
        'Chose the dataset',
        ('Country', 'Major Cities', 'State')
    )


    if dataset_option == 'Country':
        
        st.header('Descriptive statistics for Country')
        country_stats = Statistiche(country)

        visualizza_stat = st.radio("Show:", ('Descriptive statistics', 'Overall Temperature Distribution by Countries', 'Temperature Distribution for a Single Country'))
        available_countries = country['Country'].unique()

        if visualizza_stat == 'Descriptive statistics':
            descriptive_stats = country_stats.descriptive_stats()
            st.write(descriptive_stats)

        elif visualizza_stat == 'Overall Temperature Distribution by Countries':
            plot = country_stats.Distribution('AverageTemperature')
            st.pyplot(plot)

        elif visualizza_stat == 'Temperature Distribution for a Single Country':
            location = st.selectbox("Select Country", available_countries)
            fig = country_stats.plot_temperature_distribution('Country', location)
            st.plotly_chart(fig)

        
        st.header('Boxplots')
        selected_countries = st.multiselect('Select the countries you want to compare:', list(country['Country'].unique()))
        fig = country_stats.BoxplotCreator(selected_countries, is_country=True)
        st.plotly_chart(fig)
        

        st.header('Temperature comparison')
        st.write("Comparison of Average Monthly Temperatures")

        country_1 = st.selectbox("Select First Country", available_countries)
        country_2 = st.selectbox("Select Second Country", available_countries)

        fig = country_stats.TemperatureComparisonHistogram(country_1, country_2, is_country=True)
        st.plotly_chart(fig)


        st.header('Temperature Ranges by Countries')
        fig = country_stats.TempRange('Country')
        st.pyplot(fig)

        st.write("From this we extract the four at the top and bottom")
        fig = country_stats.TopTempRange('Country')
        st.pyplot(fig)

        fig = country_stats.ScatterPlot('Country')
        st.plotly_chart(fig)




    elif dataset_option == 'Major Cities':
        
        st.header('Descriptive statistics for Major Cities')
        major_stats = Statistiche(major)
        available_cities = major['City'].unique()

        visualizza_stat = st.radio("Show:", ('Descriptive statistics', 'Overall Temperature Distribution by Cities', 'Temperature Distribution for a Single City'))

        if visualizza_stat == 'Descriptive statistics':
            descriptive_stats = major_stats.descriptive_stats()
            st.write(descriptive_stats)

        elif visualizza_stat == 'Overall Temperature Distribution by Cities':
            plot = major_stats.Distribution('AverageTemperature')
            st.pyplot(plot)

        elif visualizza_stat == 'Temperature Distribution for a Single City':
            location = st.selectbox("Select City", available_cities)
            fig = major_stats.plot_temperature_distribution('City', location)
            st.plotly_chart(fig)

        
        st.header('Boxplots')
        selected_cities = st.multiselect('Select the cities you want to compare:', list(major['City'].unique()))
        fig = major_stats.BoxplotCreator(selected_cities, is_country=False)
        st.plotly_chart(fig)
        

        st.header('Temperature comparison')
        st.write("Comparison of Average Monthly Temperatures")


        city_1 = st.selectbox("Select First City", available_cities)
        city_2 = st.selectbox("Select Second City", available_cities)

        fig = major_stats.TemperatureComparisonHistogram(city_1, city_2, is_country=False)
        st.plotly_chart(fig)

        st.header('Temperature Ranges by Cities')
        fig = major_stats.TempRange('City')
        st.pyplot(fig)

        st.write("From this we extract the four at the top and bottom")
        fig = major_stats.TopTempRange('City')
        st.pyplot(fig)

        fig = major_stats.ScatterPlot('City')
        st.plotly_chart(fig)




    elif dataset_option == 'State':
        
        st.header('Descriptive statistics for State')
        state_stats = Statistiche(state)
        available_states = state['State'].unique()

        visualizza_stat = st.radio("Show:", ('Descriptive statistics', 'Overall Temperature Distribution by States', 'Temperature Distribution for a Single State'))

        if visualizza_stat == 'Descriptive statistics':
            descriptive_stats = state_stats.descriptive_stats()
            st.write(descriptive_stats)

        elif visualizza_stat == 'Overall Temperature Distribution by States':
            plot = state_stats.Distribution('AverageTemperature')
            st.pyplot(plot)

        elif visualizza_stat == 'Temperature Distribution for a Single State':
            location = st.selectbox("Select State", available_states)
            fig = state_stats.plot_temperature_distribution('State', location)
            st.plotly_chart(fig)
        
        
        
        st.header('Boxplots')
        selected_country = st.selectbox('Select a country from those that have States', state['Country'].unique())
        fig = state_stats.StateBoxPlotter(selected_country)
        st.plotly_chart(fig)

        
        st.header('Temperature comparison')
        st.write("Comparison of Average Monthly Temperatures")

        available_countries = state['Country'].unique()

        country_1 = st.selectbox("Select First Country", available_countries)
        country_2 = st.selectbox("Select Second Country", available_countries)

        fig = state_stats.TemperatureComparisonHistogram(country_1, country_2, is_country=True)
        st.plotly_chart(fig)


        st.header('Temperature Ranges by Countries (with states)')
        fig = state_stats.TempRange('Country')
        st.pyplot(fig)

        st.write("From this we extract the four at the top and bottom")
        fig = state_stats.TopTempRange('Country')
        st.pyplot(fig)

        fig = state_stats.ScatterPlot('Country')
        st.plotly_chart(fig)


        

    














elif option == 'Maps':
    data_option = st.radio("Select a dataset:", ("Country", "Major Cities"))

    country_map = Mappe(country)
    major_map = Mappe(major)

    if data_option == "Country":
        fig = country_map.GlobalYearlyTemperaturePlotter()
        st.plotly_chart(fig)
    elif data_option == "Major Cities":
        fig = major_map.GlobalYearlyTemperaturePlotter()
        st.plotly_chart(fig)


    dataset_option = st.selectbox(
        'Select',
        ('Country', 'Major Cities')
    )
    st.title('Temperature Maps')

    if dataset_option == 'Country':
        st.header('Country Maps')
        
        temperature_option = st.selectbox(
            'Choose temperature representation:',
            ('Average Temperature', 'Temperature Variations')
        )

        interval_option = st.radio("Select interval:", ("Per Year", "Decades", "30 years", "Custom"))
        if interval_option == "Per Year":
            interval = 1
        elif interval_option == "Decades":
            interval = 10
        elif interval_option == "30 years":
            interval = 30
        elif interval_option == "Custom":
            interval = st.number_input("Enter custom interval:", value=1, min_value=1, max_value=270)


        if temperature_option == 'Average Temperature':
            fig = country_map.AvgTemp_Period_country(period_interval=interval)
            st.plotly_chart(fig)

        elif temperature_option == 'Temperature Variations':
            if interval == 1:
                year_option = st.radio("Select:", ("Temperature variation within the year", "Temperature variation from the previous year"))
                if year_option == "Temperature variation within the year":
                    fig = country_map.TempVar_Year_Country()
                    st.plotly_chart(fig)
                else:
                    fig = country_map.TempVar_Period_country(period_interval=interval)
                    st.plotly_chart(fig)
            else:
                fig = country_map.TempVar_Period_country(period_interval=interval)
                st.plotly_chart(fig)  
            pass


    elif dataset_option == 'Major Cities':
        st.header('Major Cities Maps')

        temperature_option = st.selectbox(
            'Choose temperature representation:',
            ('Average Temperature', 'Temperature Variations')
        )

        interval_option = st.radio("Select interval:", ("Per Year", "Decades", "30 years", "Custom"))
        if interval_option == "Per Year":
            interval = 1
        elif interval_option == "Decades":
            interval = 10
        elif interval_option == "30 years":
            interval = 30
        elif interval_option == "Custom":
            interval = st.number_input("Enter custom interval:", value=1, min_value=1, max_value=270)

        
        if temperature_option == 'Average Temperature':
            fig = major_map.AvgTemp_Period_City(period_interval=interval)
            st.plotly_chart(fig)

        elif temperature_option == 'Temperature Variations':
            if interval == 1:
                year_option = st.radio("Select:", ("Temperature variation within the year", "Temperature variation from the previous year"))
                if year_option == "Temperature variation within the year":
                    fig = major_map.TempVar_Year_City()
                    st.plotly_chart(fig)
                else:
                    fig = major_map.TempVar_Period_City(period_interval=interval)
                    st.plotly_chart(fig)
            else:
                fig = major_map.TempVar_Period_City(period_interval=interval)
                st.plotly_chart(fig)  
            pass













elif  option == 'Datasets':
    st.title('Datasets')
    datas_option = st.radio("Select:", ("Country", "Major Cities", "State"))
    if datas_option == "Country":
        st.write(country)
    elif datas_option == "Major Cities":
        st.write(major)
    elif datas_option == "State":
        st.write(state)

    st.header('Dataset Information')
    dataset_option = st.selectbox(
    'Choose the dataset:',
    ('Country', 'State', 'Major Cities', 'Cities')
    )

    if dataset_option == 'Country':
        st.write(info_country)
    elif dataset_option == 'State':
        st.write(info_state)
    elif dataset_option == 'Major Cities':
        st.write(info_major)
    elif dataset_option == 'Cities':
        st.write(info_city)
    
    country_data = TempVar(country)
    state_data = TempVar(state)
    major_data = TempVar(major)
    
    st.header('Variation Informations')
    if dataset_option == 'Country':
        annual_variation_country = country_data.CountryTemperatureVariationCalculator()
        
        selected_country = st.selectbox('Select a Country', annual_variation_country['Country'].unique())
        filtered_variation_data = annual_variation_country[annual_variation_country['Country'] == selected_country]
        st.write(f"Temperature variation data for {selected_country}:")
        st.write(filtered_variation_data)

        fil = TempVar(filtered_variation_data)
        temperature_series_fig = fil.TemperatureSeriesPlotter()
        st.plotly_chart(temperature_series_fig)

    elif dataset_option == 'State':
        annual_variation_country = state_data.CountryTemperatureVariationCalculator()
        
        selected_country = st.selectbox('Select a Country', annual_variation_country['Country'].unique())
        filtered_variation_data = annual_variation_country[annual_variation_country['Country'] == selected_country]
        st.write(f"Temperature variation data for {selected_country}:")
        st.write(filtered_variation_data)

        fil = TempVar(filtered_variation_data)
        temperature_series_fig = fil.TemperatureSeriesPlotter()
        st.plotly_chart(temperature_series_fig)

    elif dataset_option == 'Major Cities':
        annual_variation_city = major_data.TemperatureVariationCalculator()
        
        selected_city = st.selectbox('Select a City', annual_variation_city['City'].unique())
        filtered_variation_data = annual_variation_city[annual_variation_city['City'] == selected_city]
        st.write(f"Temperature variation data for {selected_city}:")
        st.write(filtered_variation_data)

        fil = TempVar(filtered_variation_data)
        temperature_series_fig = fil.TemperatureSeriesPlotter()
        st.plotly_chart(temperature_series_fig)
    
    
    st.header('Time Series')
    dataset_option = st.selectbox(
    'Choose the dataset:',
    ('Country', 'State', 'Major Cities')
    )
    if dataset_option == 'Country':
        selected_items = st.multiselect('Select Countries', country['Country'].unique())

        fig = country_data.GlobalMonthlyTemperaturePlotter(selected_items, is_country=True)
        st.plotly_chart(fig)


    elif dataset_option == 'State':
        selected_items = st.multiselect('Select Countries', state['Country'].unique())

        fig = state_data.GlobalMonthlyTemperaturePlotter(selected_items, is_country=True)
        st.plotly_chart(fig)

    
    elif dataset_option == 'Major Cities':
        selected_items = st.multiselect('Select Cities', major['City'].unique())

        fig = major_data.GlobalMonthlyTemperaturePlotter(selected_items, is_country=False)
        st.plotly_chart(fig)

