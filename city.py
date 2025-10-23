
class City:
    """
    Represents a city that hosts companies in the simulation.

    Attributes:

        Identity

        - city_id (int): Unique, numerical identifier for this city.
        - name (str): Full city name.
        - country (str): The country within which the city is located.
        - continent (str): The continent within which the city is located.
        - latitude (float): Degrees North of the equator.
        - longitude (float): Degrees West of the prime Meridian.

        Statistics

        - population (int): Relative population, normalised 1-100.
        - wealth (int): Relative wealth, normalised 1-100.
        - industrialisation (int): Relative industrialisation, normalised 1-100.
        - stability (int): Relative stability, normalised 1-100.
        - connectivity (int): Relative connectivity, normalised 1-100.

        Trade

        - resources (dict[str, int]): Daily available resources for extraction.
        - companies (list[int]): A list of IDs of comapanies based in this city.
        - corporation_tax (float): % corporation tax in this city.
        - transit_fee (float): Price per unit to transport goods through this city.
    """

    def __init__(self, city_id: int, name: str, country: str, continent: str, latitude: float, longitude: float,
                 population: int, wealth: int, industrialisation: int, stability: int, connectivity: int,
                 resources: dict[str, int], companies: list[int], corporation_tax: float, transit_fee: float):
        
        # Identity
        self.city_id = city_id
        self.name = name
        self.country = country
        self.continent = continent
        self.latitude = latitude
        self.longitude = longitude

        # Statistics
        self.population = population
        self.wealth = wealth
        self.industrialisation = industrialisation
        self.stability = stability
        self.connectivity = connectivity

        # Trade
        self.resources = resources
        self.companies = companies
        self.corporation_tax = corporation_tax
        self.transit_fee = transit_fee

