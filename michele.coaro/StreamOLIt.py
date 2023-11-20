import streamlit as st
from Classes import MyDataFrame, Graficante

st.set_page_config(layout="wide")
majorCityPath = "DFtoImport.csv"
allCityPath = "GlobalLandTemperaturesByCity.csv"
countryPath = "GlobalLandTemperaturesByCountry.csv"
continents4cities = "data/c4cities.csv"
continents4countries = "data/c4country.csv"

graficante_instance = Graficante()

def embed_map(data, namesave="Animated_YT_Map.html"):
    graficante_instance = Graficante(data)
    graficante_instance.mapper(namesave)
    with open(namesave, "r", encoding="utf-8") as f:
        map_html = f.read()
    return map_html

def dataframer():
    page = st.sidebar.selectbox('Select dataset', ['Major cities', 'All cities', 'Countries'])

    on_df = st.sidebar.checkbox('Show dataframe')

    if page == 'Major cities':
        df1 = MyDataFrame(majorCityPath)
        df1.coordinatore()
        df1.aggiustatutto()
        df1.data_monthly()
        df = df1.df
        st.write('This dataset includes climate data from major cities around the world.')

    elif page == 'All cities':
        df1 = MyDataFrame(allCityPath)
        df1.coordinatore()
        df1.aggiustatutto()
        df1.data_yearly()
        df = df1.df
        st.write('This dataset includes climate data from all cities around the world.')

    elif page == 'Countries':
        df1 = MyDataFrame(countryPath)
        df1.aggiustatutto()
        df1.data_monthly()
        df = df1.df
        st.write('This dataset includes climate data from all countries around the world.')

    content_placeholder = st.empty()

    if on_df:
        content_placeholder.dataframe(df, use_container_width=True, hide_index=True)

    # Embed the map in the Streamlit app


dataframer()

mappa = Graficante(df)
mappa.mapper("aaaaa.html")