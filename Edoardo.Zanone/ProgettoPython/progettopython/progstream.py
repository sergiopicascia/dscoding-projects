import streamlit as st
from path import Percorso
from mapping import Map
from helpingfunction import find_index

st.title('My Maps for the Travel Around the World')
p=Percorso("/Users/Gulli/Downloads/worldcities.xlsx")
#map=Map(p.lat[p.listaindici],p.lng[p.listaindici],p.city[p.listaindici])
#map.tracecities()

action = st.selectbox('Select an action',
                              ['Find the n closest cities', 'Show the n closest cities' , 'Show the path from City to city', 'Show me the number of the cities seen and which ones' ])
i=0
mycities = [(p.city[i],p.country[i]) for i in range(len(p.city))]

if action == 'Find the n closest cities':
    startingcity = st.selectbox('Cities', mycities)
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=10)
    if st.button('Find the n cities '):
        j=find_index(p.city,p.country,startingcity)
        p.ritorna_minime((p.lat[j] ,p.lng[j]),j,n)
        st.write(f"The {n} closest cities are:")
        indixes = [p.nmin[i][1] for i in range(len(p.nmin))]
        for i in indixes:
            st.write(f"{p.city[i]},{p.country[i]}\n")

if action == 'Show the n closest cities':
    startingcity = st.selectbox('Cities', mycities)
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=10)
    if st.button('Show the n cities on the map'):
        j=find_index(p.city,p.country,startingcity)
        p.ritorna_minime((p.lat[j] ,p.lng[j]),j,n)
        indixes = [p.nmin[i][1] for i in range(len(p.nmin))]
        indixes.insert(0,j)
        st.write(f"The map of the {n} closest cities are:")
        mappa=Map(p.lat[indixes],p.lng[indixes],p.city[indixes],p.country[indixes])
        mappa.tracefromjust1()
        folium_map_html = mappa.map.get_root().render()
        st.components.v1.html(folium_map_html, width=1000, height=700)

if action == 'Show the path from City to city' :
    startingcity = st.selectbox('Starting city', mycities)
    endingcity = st.selectbox('Ending city', mycities)
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=10)
    if st.button('show the path'):
        j=find_index(p.city,p.country,startingcity)
        k=find_index(p.city,p.country,startingcity)
        p.trova_percorso_lista(j,k,0,n)
        st.write(f"The path from {j} to {k} is:")
        mappa=Map(p.lat[p.listaindici],p.lng[p.listaindici],p.city[p.listaindici],p.country[p.listaindici])
        mappa.tracecities()
        folium_map_html = mappa.map.get_root().render()
        st.components.v1.html(folium_map_html, width=1000, height=700)

if action=='Show me the number of the cities seen and which ones':
    startingcity = st.selectbox('Starting city', mycities)
    endingcity = st.selectbox('Ending city', mycities)
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=10)
    if st.button('show the path'):
        j=find_index(p.city,p.country,startingcity)
        k=find_index(p.city,p.country,startingcity)
        dist=p.trova_percorso_lista(j,k,0,n)
        st.write(f"The path from {j} to {k} is:")
        for i in range(len(p.listaindici)):
            st.write(f"{p.city[p.listaindici[i]]}, {p.country[p.listaindici[i]]} \n")
        st.write(f"The total distance is of {dist} kilometers")
