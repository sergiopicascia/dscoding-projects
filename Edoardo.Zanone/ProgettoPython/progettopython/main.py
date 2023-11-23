import streamlit as st
from path import Percorso
from mapping import Map
from helpingfunction import find_index
#IMPORTING THE CLASSES END THE LIBRARIES I NEED

st.title('My Maps for the Travel Around the World')
p=Percorso("/Users/Gulli/Downloads/worldcities.xlsx")
#map=Map(p.lat[p.listaindici],p.lng[p.listaindici],p.city[p.listaindici])
#map.tracecities()

action = st.selectbox('Select an action',
                              ['Find the n closest cities', 'Show the n closest cities' , 'Show the path from City to city', 'Show me the number of the cities seen and which ones' ])
#creating the action section, they're the different choices you have at the top of the page
i=0
mycities = [(p.city[i],p.country[i]) for i in range(len(p.city))]

if action == 'Find the n closest cities': #If we enter in this case
    startingcity = st.selectbox('Cities', mycities) #creating other box with all the cities in my DataFrame
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=10) #Choosing the number of cities we should consider
    if st.button('Find the n cities '): #The button to click to activate the next commands
        j=find_index(p.city,p.country,startingcity) #finding the index of the city selected
        p.ritorna_minime((p.lat[j] ,p.lng[j]),j,n) #Calling the function I need to operate in order to fulfill the task
        st.write(f"The {n} closest cities are:") #Showing the sentence
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
        mappa=Map(p.lat[indixes],p.lng[indixes],p.city[indixes],p.country[indixes]) # Creating the map through the class
        mappa.tracefromjust1() # Using the right function in the class
        folium_map_html = mappa.map.get_root().render() #get_root() is a method provided by Folium to get the root of the map/ render() is a method that generates the HTML representation of the map.       
        st.components.v1.html(folium_map_html, width=1000, height=700) #to display the Folium map in a Streamlit application.

if action == 'Show the path from City to city' :
    startingcity = st.selectbox('Starting city', mycities)
    endingcity = st.selectbox('Ending city', mycities)
    n = st.number_input('Insert the number of closest cities: ', min_value=1, value=10)
    if st.button('show the path'):
        j=find_index(p.city,p.country,startingcity)
        k=find_index(p.city,p.country,endingcity)
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
    if st.button('show the list of cities'):
        j=find_index(p.city,p.country,startingcity)
        k=find_index(p.city,p.country,endingcity)
        dist=p.trova_percorso_lista(j,k,0,n)
        st.write(f"The path from {j} to {k} is:")
        for i in range(len(p.listaindici)):
            st.write(f"{p.city[p.listaindici[i]]}, {p.country[p.listaindici[i]]} \n")
        st.write(f"The total distance is of {dist[0]:.2f} kilometers and it takes {dist[1]} hours")
