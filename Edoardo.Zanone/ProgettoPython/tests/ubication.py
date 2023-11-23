from geopy.distance import great_circle

'''def distancefrom(id, dataframe):
    distance = []
    city = dataframe.loc[dataframe['id']==id,['lat','lng']].iloc[0]
    for column_name, item in dataframe.iterrows():
        distance.append(great_circle(city, dataframe.loc[column_name,['lat','lng']]))
    return distance #no, too slow'''

#better
def distfrom(coord0,lat,lng):
    distance = []
    for i in range(len(lat)):
        distance.append((great_circle(coord0,[lat[i],lng[i]]).kilometers,i))
    return distance 


'''def nminime (distance,lng,index,n):
    nmin=[]
    for i in range(len(distance)):
        if len(nmin)==n:
            break
        if lng[distance[i][1]]>lng[index]:
            nmin.append([distance[i][0],distance[i][1]])
    return nmin'''

#better this one
def nminime2 (distance,lng,index,n):
    nmin=[]
    i=0
    while len(nmin)!=n and i<(len(distance)):
        if (lng[index]<0) & (lng[distance[i][1]]>100):
            pass
        elif lng[distance[i][1]]>lng[index]:
            nmin.append((distance[i][0],distance[i][1]))
        i+=1
    i=0
    if len(nmin)<n:
        while len(nmin)!=n:
            if lng[distance[i][1]]<0:
                nmin.append((distance[i][0],distance[i][1]))
            i+=1
    return nmin

'''if lng[index] <0 & lng[distance[i][1]]<0:
            if lng[distance[i][1]]>lng[index]:
                nmin.append((distance[i][0],distance[i][1]))'''

def ritorna_minime(coord0,lat,lng,index0,n):
    dist=distfrom(coord0,lat,lng)
    dist.sort(key=lambda x: x[0])
    minime=nminime2(dist,lng,index0,n)
    return minime
