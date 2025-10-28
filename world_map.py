import networkx as nx
import matplotlib.pyplot as plt

class Map:
    """
    Stores a graph that represents all connections between cities. Initialises the graph with the default set of 60 cities and their connections.
    """
    def __init__(self):
        self.graph = nx.Graph()

        self.initialise_map()
    
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
    
    def initialise_map(self):
        city_names = [
        "Abu Dhabi", "Addis Ababa", "Astana", "Athens", "Auckland", "Baotou",
        "Barcelona", "Beijing", "Buenos Aires", "Cairo", "Cape Town", "Caracas",
        "Casablanca", "Chicago", "Colombo", "Conakry", "Dar es Salaam", "Dhaka",
        "Hamburg", "Havana", "Ho Chi Minh City", "Houston", "Istanbul", "Jakarta",
        "Jeddah", "Johannesburg", "Kinshasa", "Kolkata", "Kuwait City", "Kyiv",
        "Lagos", "Lahore", "Lima", "London", "Los Angeles", "Luanda", "Manila",
        "Mexico City", "Montreal", "Moscow", "Mumbai", "New York City", "Paris",
        "Perth", "Port Moresby", "Rio de Janeiro", "Rome", "Rotterdam",
        "Saint Petersburg", "Santiago", "Santo Domingo", "São Paulo", "Seoul",
        "Shanghai", "Shenzhen", "Singapore", "Tokyo", "Vancouver", "Vienna",
        "Vladivostok"
        ]

        for city_id, name in enumerate(city_names, start=1):
            self.add_city(city_id, name=name)
        
        connections = [
            self.add_connection(14, 39, distance=1381, route_type='land'),  # Chicago <-> Montreal
            self.add_connection(14, 42, distance=1272, route_type='land'),  # Chicago <-> New York City
            self.add_connection(22, 14, distance=1745, route_type='land'),  # Houston <-> Chicago
            self.add_connection(22, 38, distance=1493, route_type='land'),  # Houston <-> Mexico City
            self.add_connection(35, 14, distance=3413, route_type='land'),  # Los Angeles <-> Chicago
            self.add_connection(35, 22, distance=2492, route_type='land'),  # Los Angeles <-> Houston
            self.add_connection(35, 38, distance=2953, route_type='land'),  # Los Angeles <-> Mexico City
            self.add_connection(39, 42, distance=595, route_type='land'),  # Montreal <-> New York City
            self.add_connection(42, 22, distance=2621, route_type='land'),  # New York City <-> Houston
            self.add_connection(58, 14, distance=3505, route_type='land'),  # Vancouver <-> Chicago
            self.add_connection(58, 35, distance=2057, route_type='land'),  # Vancouver <-> Los Angeles
            self.add_connection(9, 52, distance=2234, route_type='land'),  # Buenos Aires <-> São Paulo
            self.add_connection(12, 33, distance=4335, route_type='land'),  # Caracas <-> Lima
            self.add_connection(33, 52, distance=4378, route_type='land'),  # Lima <-> São Paulo
            self.add_connection(50, 9, distance=1389, route_type='land'),  # Santiago <-> Buenos Aires
            self.add_connection(52, 46, distance=433, route_type='land'),  # São Paulo <-> Rio de Janeiro
            self.add_connection(2, 17, distance=2375, route_type='land'),  # Addis Ababa <-> Dar es Salaam
            self.add_connection(16, 32, distance=2715, route_type='land'),  # Conakry <-> Lagos
            self.add_connection(26, 11, distance=1398, route_type='land'),  # Johannesburg <-> Cape Town
            self.add_connection(26, 17, distance=3516, route_type='land'),  # Johannesburg <-> Dar es Salaam
            self.add_connection(27, 2, distance=5080, route_type='land'),  # Kinshasa <-> Addis Ababa
            self.add_connection(27, 17, distance=4099, route_type='land'),  # Kinshasa <-> Dar es Salaam
            self.add_connection(27, 36, distance=808, route_type='land'),  # Kinshasa <-> Luanda
            self.add_connection(32, 2, distance=5363, route_type='land'),  # Lagos <-> Addis Ababa
            self.add_connection(32, 27, distance=2937, route_type='land'),  # Lagos <-> Kinshasa
            self.add_connection(36, 26, distance=3179, route_type='land'),  # Abu Dhabi <-> Kuwait City
            self.add_connection(3, 29, distance=4935, route_type='land'),  # Astana <-> Kuwait City
            self.add_connection(3, 33, distance=3541, route_type='land'),  # Astana <-> Lahore
            self.add_connection(6, 3, distance=3700, route_type='land'),  # Baotou <-> Astana
            self.add_connection(8, 6, distance=663, route_type='land'),  # Beijing <-> Baotou
            self.add_connection(8, 55, distance=1213, route_type='land'),  # Beijing <-> Shanghai
            self.add_connection(10, 29, distance=2060, route_type='land'),  # Cairo <-> Kuwait City
            self.add_connection(18, 21, distance=3225, route_type='land'),  # Dhaka <-> Ho Chi Minh City
            self.add_connection(18, 56, distance=4540, route_type='land'),  # Dhaka <-> Shenzhen
            self.add_connection(23, 10, distance=2481, route_type='land'),  # Istanbul <-> Cairo
            self.add_connection(25, 1, distance=1844, route_type='land'),  # Jeddah <-> Abu Dhabi
            self.add_connection(28, 18, distance=330, route_type='land'),  # Kolkata <-> Dhaka
            self.add_connection(28, 33, distance=2150, route_type='land'),  # Kolkata <-> Lahore
            self.add_connection(29, 25, distance=1530, route_type='land'),  # Kuwait City <-> Jeddah
            self.add_connection(33, 42, distance=1950, route_type='land'),  # Lahore <-> Mumbai
            self.add_connection(40, 3, distance=2704, route_type='land'),  # Moscow <-> Astana
            self.add_connection(42, 28, distance=1901, route_type='land'),  # Mumbai <-> Kolkata
            self.add_connection(55, 6, distance=1868, route_type='land'),  # Shanghai <-> Baotou
            self.add_connection(56, 6, distance=2614, route_type='land'),  # Shenzhen <-> Baotou
            self.add_connection(56, 8, distance=2180, route_type='land'),  # Shenzhen <-> Beijing
            self.add_connection(56, 55, distance=1508, route_type='land'),  # Shenzhen <-> Shanghai
            self.add_connection(60, 54, distance=1200, route_type='land'),  # Vladivostok <-> Seoul
            self.add_connection(4, 30, distance=2145, route_type='land'),  # Athens <-> Kyiv
            self.add_connection(7, 43, distance=1035, route_type='land'),  # Barcelona <-> Paris
            self.add_connection(19, 7, distance=1800, route_type='land'),  # Hamburg <-> Barcelona
            self.add_connection(23, 30, distance=1480, route_type='land'),  # Istanbul <-> Kyiv
            self.add_connection(30, 19, distance=1636, route_type='land'),  # Kyiv <-> Hamburg
            self.add_connection(30, 40, distance=1685, route_type='land'),  # Kyiv <-> Moscow
            self.add_connection(30, 49, distance=1938, route_type='land'),  # Kyiv <-> Saint Petersburg
            self.add_connection(30, 59, distance=1331, route_type='land'),  # Kyiv <-> Vienna
            self.add_connection(34, 43, distance=467, route_type='land'),  # London <-> Paris
            self.add_connection(40, 49, distance=702, route_type='land'),  # Moscow <-> Saint Petersburg
            self.add_connection(43, 47, distance=1457, route_type='land'),  # Paris <-> Rome
            self.add_connection(43, 48, distance=517, route_type='land'),  # Paris <-> Rotterdam
            self.add_connection(43, 59, distance=1235, route_type='land'),  # Paris <-> Vienna
            self.add_connection(47, 19, distance=1687, route_type='land'),  # Rome <-> Hamburg
            self.add_connection(47, 59, distance=1100, route_type='land'),  # Rome <-> Vienna
            self.add_connection(48, 19, distance=529, route_type='land'),  # Rotterdam <-> Hamburg
            self.add_connection(59, 4, distance=1708, route_type='land'),  # Vienna <-> Athens
            self.add_connection(59, 7, distance=1987, route_type='land'),  # Vienna <-> Barcelona
            self.add_connection(59, 19, distance=973, route_type='land'),  # Vienna <-> Hamburg
            self.add_connection(59, 23, distance=1560, route_type='land'),  # Vienna <-> Istanbul
            ]

if __name__ == "__main__":
    plt.figure(figsize=(18, 12))
    pos = nx.spring_layout(m.graph, seed=42, k=0.4)

    labels = nx.get_node_attributes(m.graph, "name")

    nx.draw_networkx_nodes(m.graph, pos, node_size=800)
    nx.draw_networkx_labels(m.graph, pos, labels, font_size=8)

    edges = m.graph.edges(data=True)
    land_edges = [(u, v) for u, v, a in edges if a["route_type"] == "land"]
    sea_edges  = [(u, v) for u, v, a in edges if a["route_type"] == "sea"]

    nx.draw_networkx_edges(m.graph, pos, edgelist=land_edges, edge_color="green")
    nx.draw_networkx_edges(m.graph, pos, edgelist=sea_edges, edge_color="blue")

    plt.show()

# Implement coordinates in the City class so matplotlib can display a geophically accurate graph