
from __future__ import annotations
from city import City

class Company:

    """
    Represents a company within the simulation.

    Attributes:

        Identity

        - company_id (int): Unique, numerical identifier for this company.
        - name (str): Full company name.
        - ticker (str): Short stock market ticker.
        - city (int): ID number for the city wherein the company is located.
        - industry (str): Sector classification.
        - ceo_name (str): Name of the CEO, used in some news reports.
        - year_founded (int): The year the company was founded.
        - reputation (float): Public perception score (0-1). 1 = favourable, 0.5 = neutral, 0 = unfavourable.

        Operations

        - inputs (dict[str, int]): Required input goods per hour.
        - outputs (dict[str, int]): Produced output goods per hour.
        - capacity (dict[str, int]): Maximum output attainable.
        - efficiency (float): % of maximum possible output actually being produced. 100% during normal operations.
        - inventory (dict[str, int]): Inventory of all resources/products the company posesses.
        - status (str): Operational status classification. Either 'Operational', 'Limited' or 'Idle'.

        Finances

        - cash (float): Current balance.
        - revenue (float): Total money coming in per day.
        - var_costs (float): Cost incurred per unit produced per day.
        - fixed_costs (float): Cost incurred regardless of production level per day.
        - profit (float): revenue - var_costs - fixed_costs.

        The Market

        - shares_outstanding (int): Number of shares currently issued.
        - share_price (float): The price of a single share on the market.
        - market_cap (float): shares_outstanding * share_price.
        - volatility (float): Scale of random deviations in stock price (0-1). Higher = more volatile.
        - pays_dividend (bool): TRUE if the company pays dividends to its shareholders, FALSE if not.
        - dividend_freq (int): Frequency of dividends, in days.
        - dividend_yield (float): Amount of money paid per share when a dividend is paid.

        Behaviour

        - trade_bias (float): Preference for trade (0-1). 1 = international, 0.5 = both, 0 = domestic.
        - sensitivity (float): Event sensitivity (0-1). Higher = more affected.
        - prefers_fast_shipping (bool): TRUE if company takes the quickest delivery route, FALSE if they take the cheapest.

        History

        - profit_history (list[float]): History of company profits, recorded daily.
        - price_history (list[float]): History of the stock price, recorded hourly.
        - event_log (dict[int, str]): Record of regional and world events relevant to this company.
    """

    def __init__(self, company_id: int, name: str, ticker: str, city: City, industry: str, ceo_name: str, year_founded: int, reputation: float,
                 inputs: dict[str, int], outputs: dict[str, int], capacity: dict[str, int], inventory: dict[str, int],
                 cash: float, revenue: float, var_costs: float, fixed_costs: float,
                 shares_outstanding: int, share_price: float, volatility: float, pays_dividend: bool, dividend_freq: int, dividend_yield: float,
                 trade_bias: float, sensitivity: float, prefers_fast_shipping: bool) :
        
        # Indentity
        self.company_id = company_id
        self.name = name
        self.ticker = ticker
        self.city = city
        self.industry = industry
        self.ceo_name = ceo_name
        self.year_founded = year_founded
        self.reputation = reputation

        # Operations
        self.inputs = inputs
        self.outputs = outputs
        self.capacity = capacity
        self.efficiency = self.calculate_efficiency(outputs, capacity)
        self.inventory = inventory
        self.status = self.set_status(self.efficiency)

        # Finances
        self.cash = cash
        self.revenue = revenue
        self.var_costs = var_costs
        self.fixed_costs = fixed_costs
        self.profit_before_tax = revenue - var_costs - fixed_costs
        self.net_profit = self.profit_before_tax * (1 - self.city.corporation_tax)

        # The Market
        self.shares_outstanding = shares_outstanding
        self.share_price = share_price
        self.market_cap = shares_outstanding * share_price
        self.volatility = volatility
        self.pays_dividend = pays_dividend
        self.dividend_freq = dividend_freq
        self.dividend_yield = dividend_yield

        # Behaviour
        self.trade_bias = trade_bias
        self.sensitivity = sensitivity
        self.prefers_fast_shipping = prefers_fast_shipping

        # History
        self.profit_history = []
        self.price_history = []
        self.event_log = []
    
    def __str__(self):
        """
        Displays a selection of information about a company when it is printed. Additional information is printed for companies that give out dividends.
        """
        if (self.pays_dividend):
            return (f"\n{self.name}\n\n"
                    f"Company ID          | {self.company_id}\n"
                    f"Ticker              | {self.ticker}\n"
                    f"City                | {self.city.name}\n"
                    f"Industry            | {self.industry}\n"
                    f"CEO                 | {self.ceo_name}\n"
                    f"Year Founded        | {self.year_founded}\n"
                    f"Reputation          | {self.reputation}\n"
                    f"Efficiency          | {self.efficiency}\n"
                    f"Status              | {self.status}\n"
                    f"Profit (before tax) | ${self.profit_before_tax} / day\n"
                    f"Profit (after tax)  | ${self.net_profit} / day\n"
                    f"Outstanding shares  | {self.shares_outstanding}\n"
                    f"Share price         | ${self.share_price}\n"
                    f"Market cap          | ${self.market_cap}\n"
                    f"Pays dividend?      | Yes\n"
                    f"Dividend frequency  | Pays every {self.dividend_freq} days\n"
                    f"Dividend yield      | ${self.dividend_yield} per share\n")
        else:
            return (f"\n{self.name}\n\n"
                    f"Company ID          | {self.company_id}\n"
                    f"Ticker              | {self.ticker}\n"
                    f"City                | {self.city.name}\n"
                    f"Industry            | {self.industry}\n"
                    f"CEO                 | {self.ceo_name}\n"
                    f"Year Founded        | {self.year_founded}\n"
                    f"Reputation          | {self.reputation}\n"
                    f"Efficiency          | {self.efficiency}\n"
                    f"Status              | {self.status}\n"
                    f"Profit (before tax) | ${self.profit_before_tax} / day\n"
                    f"Profit (after tax)  | ${self.net_profit} / day\n"
                    f"Outstanding shares  | {self.shares_outstanding}\n"
                    f"Share price         | ${self.share_price}\n"
                    f"Market cap          | ${self.market_cap}\n"
                    f"Pays dividend?      | No\n")
    
    def calculate_efficiency(self, outputs: dict[str, int], capacity: dict[str, int]) -> float:
        """
        Calculates % efficiency of current production.

        Args:
            outputs (dict[str, int]): Products → units/day currently produced.
            capacity (dict[str, int]): Products → max units/day possible.
        
        Returns:
            float: Efficiency % across all products.
        """
        total_output = 0
        total_capacity = 0

        for product, cap in capacity.items():
            prod = outputs.get(product, 0) # If product not in outputs, assume 0 produced
            total_output += prod
            total_capacity += cap
    
        # Avoid divideByZero
        if total_capacity == 0:
            return 0
        
        return total_output / total_capacity * 100

    def set_status(self, efficiency: float) -> str:
        """
        Sets the status of a company based on its current effiency.

        Args:
            - efficiency (float): % of maximum possible output actually being produced. 100% during normal operations.
        
        Returns:
            - Either an "Operational", "Limited" or "Idle" status
        """
        if efficiency >= 0.9:
            return "Operational"
        elif efficiency > 0:
            return "Limited"
        else:
            return "Idle"

# Testing version control
