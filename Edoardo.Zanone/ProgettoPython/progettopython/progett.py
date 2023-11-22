#Consider the dataset describing some of the world's major cities. Assume that it is always possible to 
#travel from each city to the 3 nearest cities and that such travel takes 2 hours to the nearest city, 
#4 hours to the second nearest city, and 8 hours to the third nearest city. In addition, the trip takes an 
#additional 2 hours if the destination city is in another country than the starting city and an additional 
#2 hours if the destination city has more than 200,000 inhabitants.

#Starting in London and always traveling east, is it possible to travel around the world by returning to 
#London in 80 days? How long does this take at a minimum?

from path import Percorso
from mapping import Map
p=Percorso("/Users/Gulli/Downloads/worldcities.xlsx")
p.trova_percorso_lista(34,34,0,30)
print(len(p.listaindici))
map=Map(p.lat[p.listaindici],p.lng[p.listaindici],p.city[p.listaindici])
map.tracecities()
map.savemap()
