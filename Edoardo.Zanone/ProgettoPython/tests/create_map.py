
import folium 
map= folium.Map( location =[30,10], zoom_start=2)
def Mappa(lat , lng , city):
    folium.Marker(location=[lat,lng],popup=city).add_to(map)
    return map

#map.save("Città.html")