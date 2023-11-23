from path import Percorso
from mapping import Map
p=Percorso("/Users/Gulli/Downloads/worldcities.xlsx")
p.trova_percorso_lista(34,34,0,30)
print(len(p.listaindici))
map=Map(p.lat[p.listaindici],p.lng[p.listaindici],p.city[p.listaindici])
map.tracecities()
map.savemap()
