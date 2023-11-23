import folium 

class Map():
    def __init__(self, lat, lng, city, country):  # Initializing Map object with a folium Map centered at [30, 10] with zoom level 2
        self.map= folium.Map( location =[30,10], zoom_start=2)
        self.lat=lat
        self.lng=lng
        self.city=city
        self.country=country
        self.coord=[]

    def Mappa(self): # Adding markers for each city seen to the map
        for i in range(len(self.lat)):
            folium.Marker(location=[self.lat[i],self.lng[i]],popup=f"{self.city[i]} \n {self.country[i]}").add_to(self.map)

    def _createcoord(self): # Creating a list of tuples for the coordinates (in order to use them in folium.PolyLine)
        for i in range(len(self.lat)):
            self.coord.append((self.lat[i],self.lng[i]))

    def tracecities(self): # Trace a line connecting all the cities, in order, on the map
        self.Mappa()
        self._createcoord()
        folium.PolyLine(locations=self.coord, color='black').add_to(self.map)
    
    def tracefromjust1(self): # Tracing lines connecting the n closest cities to the first selected city (using it on streamlit)
        self.Mappa()
        self._createcoord()
        start_coord = (self.lat[0], self.lng[0])
        for i in range(1, len(self.lat)):
            end_coord = (self.lat[i], self.lng[i])
            folium.PolyLine(locations=[start_coord, end_coord], color='black').add_to(self.map)

    def savemap(self): # Saving the map as a HTML file
        self.map.save("GiroMondo.html")

