import folium 

class Map():
    def __init__(self, lat, lng, city, country):
        self.map= folium.Map( location =[30,10], zoom_start=2)
        self.lat=lat
        self.lng=lng
        self.city=city
        self.country=country
        self.coord=[]

    def Mappa(self):
        for i in range(len(self.lat)):
            folium.Marker(location=[self.lat[i],self.lng[i]],popup=f"{self.city[i]} \n {self.country[i]}").add_to(self.map)

    def _createcoord(self):
        for i in range(len(self.lat)):
            self.coord.append((self.lat[i],self.lng[i]))

    def tracecities(self):
        self.Mappa()
        self._createcoord()
        folium.PolyLine(locations=self.coord, color='black').add_to(self.map)
    
    def tracefromjust1(self):
        self.Mappa()
        self._createcoord()
        start_coord = (self.lat[0], self.lng[0])
        for i in range(1, len(self.lat)):
            end_coord = (self.lat[i], self.lng[i])
            folium.PolyLine(locations=[start_coord, end_coord], color='black').add_to(self.map)

    def savemap(self):
        self.map.save("GiroMondo.html")

