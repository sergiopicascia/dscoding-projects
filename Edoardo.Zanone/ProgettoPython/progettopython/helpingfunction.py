def find_index(city,country,selected): #Finding the correct index 
    for j in range(len(city)):
            if (city[j]==selected[0]) & (country[j]==selected[1]):
                break
    return j