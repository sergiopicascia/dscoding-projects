
import folium 
map= folium.Map( location =[30,10], zoom_start=2)
def Mappa(lat , lng , city):
    folium.Marker(location=[lat,lng],popup=city).add_to(map)
    return map

def tracecities(map,coord):
    folium.PolyLine(locations=coord, color='black').add_to(map)
    return map
#map.save("Città.html")