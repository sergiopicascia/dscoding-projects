'''
program to check if there is exist a path between two vertices
of a graph
'''

from collections import defaultdict

from traveler import Traveler


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)

    def isReachable(self, s, d):
        visited = set()
        queue = []

        queue.append(s)
        visited.add(s)

        while queue:
            n = queue.pop(0)
            if n == d:
                return True
            for i in self.graph[n]:
                if i not in visited:
                    queue.append(i)
                    visited.add(i)

        return False


my_traveler = Traveler('worldcities.xlsx', 'data_optimized.json')

print('graph_creation')
dict_int_to_id = dict()
g = Graph()
for city_id in my_traveler.cities.keys():
    for neighbour in my_traveler.cities[city_id].neighbors:
        g.addEdge(city_id, neighbour['city'].id)
print('Graph created')

print('Real tests: cities below definitely have path to London')
# Spoinler: required path doesn't exist

# London
u = 1826645935
# city that has path to London (checked manually)
v = 1826877782
if g.isReachable(u, v):
    print("There is a path from %d to %d" % (u, v))
else:
    print("There is no path from %d to %d" % (u, v))

# London
u = 1826645935
# city that has path to London (checked manually)
v = 1826583042
if g.isReachable(u, v):
    print("There is a path from %d to %d" % (u, v))
else:
    print("There is no path from %d to %d" % (u, v))
