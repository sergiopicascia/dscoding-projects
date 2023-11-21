import ubication

def trova_percorso_lista(lat,lng,city,id,country,index0,index1,n,distcurr,listaindici):
    if (index0==index1) & (distcurr!=0):
        listaindici.append(index0)
        return 0
    nmin=ubication.ritorna_minime([lat[index0],lng[index0]],lat,lng,index0,n)
    latmax=best_lat(n,lat,index1,nmin)
    j=find_index(n,latmax,nmin)
    print(city[latmax[0][1]], latmax[0][1],lng[latmax[0][1]],latmax[0][0])
    listaindici.append(index0)
    return (distcurr + trova_percorso_lista(lat,lng,city,id,country,latmax[0][1],index1, n,nmin[j][0], listaindici))

def best_lat(n,lat,index1,nmin):
    latmax=[]
    for i in range(n):
        latmax.append((abs(lat[nmin[i][1]]-lat[index1]),nmin[i][1]))
        #lngmax.appen((lng[tenmin[i][1]],tenmin[i][1]))
    latmax.sort(key=lambda x: x[0])
    return latmax

def find_index(n,latmax,nmin):
    for i in range(n):
        if latmax[0][1] == nmin[i][1]:
            j=i
    return j
