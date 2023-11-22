import streamlit as st

st.set_page_config(layout="wide")


def introduction():

    st.title('Welcome to my WebApp!')
    st.title('Please select a database from the sidebar')

#the following section is used to create the different pages
def major_cities_page():
    df = dataframer()
    map_plotter(df)
    city_plots(df)

def all_cities_page():
    df = dataframer()
    map_plotter(df)
    city_plots()

def countries_page():
    df = dataframer()
    country_plots(df)

page_names ={
    "-" : introduction,
    "Major cities" : major_cities_page,
    "All cities" : all_cities_page,
    "Countries" : countries_page
}

page_selector = st.sidebar.selectbox("Select the desired dataframe", page_names, key='THAPAGESELECTOR')

#the following section is used to assign the page to the correct dataframe
def dataframer():
    from Classes import MyDataFrame
    majorCityPath = "DFtoImport.csv"
    allCityPath = "GlobalLandTemperaturesByCity.csv"
    countryPath = "GlobalLandTemperaturesByCountry.csv"

    on_df = st.sidebar.checkbox('Show dataframe')

    if page_selector == 'Major cities':
        df1 = MyDataFrame(majorCityPath)
        df1.coordinatore()
        df1.data_fixer()
        df1.data_yearly()
        df1.data_monthly()
        df = df1.df

    elif page_selector == 'All cities':
        df1 = MyDataFrame(allCityPath)
        df1.coordinatore()
        df1.data_fixer()
        df1.data_yearly()
        df1.data_monthly()
        df = df1.df

    elif page_selector == 'Countries':
        df1 = MyDataFrame(countryPath)
        df1.data_fixer()
        df1.data_monthly()
        df = df1.df

    content_placeholder = st.empty()

    if on_df:
        content_placeholder.dataframe(df, use_container_width=True, hide_index=True)

    return df

#this functions specifically plots the map, and is thus separated from the other plots
def map_plotter (df):
    from Classes import Graficante
    on_map = st.sidebar.checkbox('Show map')
    if page_selector != "Countries":
        mappa = Graficante(df)
        mappa_show = mappa.mapper()
        if on_map:
            st.plotly_chart(mappa_show, use_container_width=True)


#this function plots the graphs related to the cities pages, and thus is used both in "major cities" and "all cities"
def city_plots(df):
    from Classes import Graficante
    plottino = Graficante(df)
    graph_selector = st.sidebar.selectbox("Select the desired graph", ["-","Histogram Comparison","Scatter Plot", "Bee Swarm Plot", "Monthly Temperature"], key='CITYselector')
    if graph_selector == "-":
        '''# Select a graph from the sidebar'''
    if graph_selector == "Bee Swarm Plot":
        plottino.bee_double()
    if graph_selector == "Scatter Plot":
        plottino.city_scatter()
    if graph_selector == "Histogram Comparison":
        plottino.histogram_city()
    if graph_selector == "Monthly Temperature":
        plottino.city_liner()


#this function plots the graphs related to the countries page
def country_plots(df):
    from Classes import Graficante
    plotter = Graficante(df)
    graph_selector = st.sidebar.selectbox("Select the desired graph", ["-","Single Country Line Plot","Double Country Comparison", "Continent Temperature Distribution Plot"], key='COUNTRYselector')
    if graph_selector == "-":
        '''# Select a graph from the sidebar'''
    if graph_selector == "Double Country Comparison":
        plotter.double_country()
    if graph_selector == "Single Country":
        plotter.single_country()
    if graph_selector == "Continent Temperature Distribution Plot":
        plotter.ridge_plot()


page_names[page_selector]()