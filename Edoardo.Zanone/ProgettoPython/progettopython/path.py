import pandas as pd
from geopy.distance import great_circle


class Percorso:
    def __init__(self, path):
        self.df=pd.read_excel(path)
        self.listaindici=[]
        self.convertinlist()
    
    def convertinlist(self):
        self.lat=self.df["lat"].values
        self.lng=self.df["lng"].values
        self.id=self.df["id"].values
        self.city=self.df["city"].values
        self.country=self.df["country"].values
    
 
    def distfrom(self, coord0 : ( )):
        self.distance = []
        for i in range(len(self.lat)):
            self.distance.append((great_circle(coord0,[self.lat[i],self.lng[i]]).kilometers,i))
    
    def nminime (self, index : int, n):
        self.nmin=[]
        i=0
        while len(self.nmin)!=n and i<(len(self.distance)):
            if (self.lng[index]<0) & (self.lng[self.distance[i][1]]>100):
               pass
            elif self.lng[self.distance[i][1]]>self.lng[index]:
                self.nmin.append((self.distance[i][0],self.distance[i][1]))
            i+=1
        i=0
        if len(self.nmin)<n:
          while len(self.nmin)!=n:
              if self.lng[self.distance[i][1]]<0:
                self.nmin.append((self.distance[i][0],self.distance[i][1]))
              i+=1
    
    def ritorna_minime(self, coord0 : (), index0 : int,n ):
        self.distfrom(coord0)
        self.distance.sort(key=lambda x: x[0])
        self.nminime(index0, n)
    
    def best_lat(self, index1 : int,n):
        self.latmax = []
        for i in range(n):
            self.latmax.append((abs(self.lat[self.nmin[i][1]]-self.lat[index1]),self.nmin[i][1]))
        self.latmax.sort(key=lambda x: x[0])

    def find_index(self,n):
        for i in range(n):
            if self.latmax[0][1] == self.nmin[i][1]:
                j=i
        return j
    
    def trova_percorso_lista(self, index0 : int ,index1 : int ,distcurr:int,n):
        if (index0==index1) & (distcurr!=0):
            self.listaindici.append(index0)
            return (0 , 0)
        self.ritorna_minime([self.lat[index0],self.lng[index0]],index0,n)
        self.best_lat(index1,n)
        j=self.find_index(n)
        d=self.findthetime(index0,n,j) 
        #print(self.city[self.latmax[0][1]], self.latmax[0][1],self.lng[self.latmax[0][1]],self.latmax[0][0])
        self.listaindici.append(index0)
        tupla=self.trova_percorso_lista(self.latmax[0][1],index1,self.nmin[j][0],n)
        return (tupla[0]+self.nmin[j][0],d+tupla[1])

    def findthetime(self,index0,n,j):
        d = 0
        if j <=n//3:
            d = 2
        elif (j>n//3) & (j<=(2*n)//3):
            d = 4
        else :
            d = 6
        if self.country[self.latmax[0][1]]!=self.country[index0]:
            return d + 2
        return d