
from city import City
from company import Company
from registry import Registry

registry = Registry()

my_city = City(0,
               "London",
               "United Kingdom",
               "Europe",
               51.5072,
               0.1276,
               50,
               99,
               32,
               81,
               73,
               {"Livestock": 1_000_000},
               [1],
               0.25,
               0.02)

my_company = Company(1,
                     "Transatlantic Steel LTD",
                     "TSTE",
                     my_city,
                     "Steel",
                     "Cole Cook",
                     1966,
                     0.61,
                     {"Iron ore": 500, "Coal": 50},
                     {"Steel": 50},
                     {"Steel": 50},
                     {"Iron ore": 5000, "Coal": 500, "Steel": 250},
                     25_000_000,
                     6_500,
                     2.5,
                     1_300,
                     500_000,
                     5,
                     0.19,
                     True,
                     90,
                     0.5,
                     0.88,
                     0.23,
                     True)

def generate_company() -> Company:

    # Pick a random city

    # Pick a random sector from that city's sector list

    # Generate a random name based on chosen sector

    # Generate a ticker based on name

    # Apply to the registry

    # If successful, continue. If not, go back to name generation step

    # Generate the rest of the company information

    return True
