from geopy.distance import great_circle

def distancefrom(id, dataframe):
    distance = []
    city = dataframe.loc[dataframe['id']==id,['lat','lng']].iloc[0]
    for column_name, item in dataframe.iterrows():
        distance.append(great_circle(city, dataframe.loc[column_name,['lat','lng']]))
    return distance #no, too slow

#better
def distfrom([lat1, lng1],lat,lng):
    distance = []
    for i in range(len(lat)):
        distance.append(great_circle([lat1 ,lng1],[lat[i],lng[i]]))
    return distance 