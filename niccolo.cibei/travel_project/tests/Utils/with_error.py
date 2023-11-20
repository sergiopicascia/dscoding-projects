class TravelGraph:
    # ... (previous code) ...

    def get_city_id(self, city_name):
        try:
            city_id = self.df.loc[self.df['city_ascii'] == city_name, 'id'].values[0]
            return city_id
        except IndexError:
            raise ValueError(f"City not found: {city_name}")

    def shortest_path(self, source_city_name, target_city_name):
        cities_name = []

        # Find the corresponding IDs for the source and target cities
        try:
            source_id = self.get_city_id(source_city_name)
            target_id = self.get_city_id(target_city_name)
        except ValueError as e:
            return str(e)

        # Find the shortest path between the source and target city IDs
        try:
            short_path = nx.shortest_path(self.G, source=source_id, target=target_id, weight='weight')
        except nx.NetworkXNoPath:
            return "No path found between the specified cities."

        for i in short_path:
            cities_name.append(self.df.loc[self.df['id'] == i, 'city_ascii'].values[0])

        return cities_name

    def cycle_tour(self, start_city_name):
        tour_cities = []

        # Find the corresponding ID for the starting city
        try:
            start_id = self.get_city_id(start_city_name)
        except ValueError as e:
            return str(e)

        # Utilizza l'algoritmo di Dijkstra per trovare il percorso più breve che forma un ciclo
        try:
            cycle_path = nx.approximation.traveling_salesman_problem(self.G, cycle=True)
        except nx.NetworkXError:
            return "Error finding a cycle tour."

        # Trova l'indice della città di partenza nel percorso
        start_index = cycle_path.index(start_id)

        # Ruota la lista del percorso in modo che inizi dalla città di partenza
        tour_path = cycle_path[start_index:] + cycle_path[:start_index]
        for i in tour_path:
            tour_cities.append(self.df.loc[self.df['id'] == i, 'city_ascii'].values[0])

        return tour_cities
