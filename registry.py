
class Registry:
    """
    Central registry for all companies in the simulation.

    Attributes:
        - registry (dict[str, tuple[str, int]]): Contains a reference for all companies in the simulation. Stored as {company_id: (name, ticker)}.
        - next_company_id: Holds the next available ID to give out. Does not backtrack when a company goes bust.
    """

    def __init__(self):
        self.registry = {}
        self.next_company_id = 1
    
    def register_company(self, name: str, ticker: str) -> int | None:
        """
        Adds uniquely named and tickered companies to the registry.

        Args:
            - name (str): Name for the potential new company.
            - ticker (str): Ticker for the potential new company.
        
        Returns:
            - company_id (int): The ID for the new company.
        """

        # Check if both name and ticker are unique, cancel registration if not
        if name in self.registry or ticker in self.registry.values():
            return None
        
        company_id = self.next_company_id
        self.next_company_id += 1

        self.registry[company_id] = (name, ticker)

        return company_id
    
    def get_name(self, company_id: int) -> str:
        """
        Returns the company name for a given ID.
        """
        return self.registry[company_id][0]
    
    def get_ticker(self, company_id: int) -> str:
        """
        Returns the ticker for a given ID.
        """
        return self.registry[company_id][1]