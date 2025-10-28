import networkx as nx

class Map:
    """
    Stores a graph that represents all connections between cities.
    """
    def __init__(self):
        self.graph = nx.Graph()
    
    def add_city(self, city_id, **attributes):
        """
        Adds a city to the graph.

        Args:
            city_id (int): The unique ID for the city.
            ?
        """
        self.graph.add_node(city_id, **attributes)
    
    def add_connection(self, city_a, city_b, distance: int, route_type: str, accessible=True):
        """
        Adds a connection between two existing cities to the graph.

        Args:
            city_a (int): The unique ID for city A.
            city_b (int): The unique ID for city B.
            distance (float): The distance between the two cities in km. This is the average of the distance by road and the as the crow flies distance.
            route_type (str): Determines if the connection is by land or sea.
            accessible (bool): TRUE if route is currently accessible (default), FALSE if not. If FALSE, cargo must be shipped using another route.
        """
        self.graph.add_edge(city_a, city_b,
                            distance=distance,
                            route_type=route_type,
                            accessible=accessible)
    
    def set_accessibility(self, city_a, city_b, accessible: bool):
        """
        Sets the accessibility of a connection to TRUE or FALSE

        Args:
            city_a (int): The ID for the first city on the relevant connection.
            city_b (int): The ID for the second city on the relevant connection.
            accessible (bool): The Boolean state the connection will be set to.
        """
        if self.graph.has_edge(city_a, city_b):
            self.graph[city_a][city_b]["accessible"] = accessible
    
    def get_shortest_path(self, start, end):
        """
        Calculates the shortest (multimodal) path between two given cities.

        Args:
            start (int): The ID for the city at the start of the path.
            end (int): The ID for the city at the end of the path.
        
        Returns:
            A list of the steps on the shortest path. Will always include both the start and end cities.
        """
        subgraph = nx.subgraph_view(self.graph, filter_edge=lambda u, v: self.graph[u][v]["accessible"])

        return nx.shortest_path(subgraph, start, end, weight="distance")

    def get_cheapest_path(self, start, end, land_cost_per_km: float, sea_cost_per_km: float):
        """
        Calculates the cheapest (multimodal) path between two given cities.

        Args:
            start (int): The ID for the city at the start of the path.
            end (int): The ID for the city at the end of the path.
            land_cost_per_km (float): Cost per km to travel by land (typically less).
            sea_cost_per_km (float): Cost per km to travel by sea (typically more).
        
        Returns:
            A list of the steps on the cheapest path. Will always include both the start and end cities.
        """
        def cost(u, v, a):
            base = a["distance"]

            if a["route_type"] == "land":
                return base * land_cost_per_km
            else:
                return base * sea_cost_per_km
        
        subgraph = nx.subgraph_view(self.graph, filter_edge=lambda u, v: self.graph[u][v]["accessible"])

        return nx.shortest_path(subgraph, start, end, weight=cost)

if __name__ == "__main__":
    world_map = Map()

    world_map.add_city(0, name="London")
    world_map.add_city(1, name="Paris")
    world_map.add_city(2, name="Lille")

    world_map.add_connection(0, 1, distance=400, route_type="sea", accessible=True)
    world_map.add_connection(0, 2, distance=250, route_type="land", accessible=True)
    world_map.add_connection(2, 1, distance=250, route_type="land", accessible=True)

    print("Shortest path: ", world_map.get_shortest_path(0, 1))
    print("Cheapest path: ", world_map.get_cheapest_path(0, 1, 1, 1.5))