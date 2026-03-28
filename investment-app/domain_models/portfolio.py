from .stock import Stock

# PURPOSE:
#   -Portfolio provides a portfolio abstraction
#   -encapsulates data related to a portfolio and provides methods for manipulating or evaluating a portfolio
class Portfolio:
    def __init__(self, id=None, *, name, stocks: dict[str, Stock] = None):
        self.id = id
        self.name = name
        self.stocks = stocks if stocks is not None else {}


    # INPUT:
    #   -ticker(str); a stock ticker symbol
    # OUTPUT:
    #   -exists(bool); True or False
    # PRECONDITION: None
    # POSTCONDITION:
    #   -exists; True if ticker held, False if not
    # RAISES: None
    def has_stock(self, ticker : str) -> bool:
        exists = ticker in self.stocks
        return exists


    # INPUT:
    #   -shares_requested(tuple[str,int]); a request for a ticker and quantity of stocks
    # OUTPUT: None
    # PRECONDITION:
    #   -shares_requested; ticker exists as a real stock ticker, quantity does not exceed market available shares
    # POSTCONDITION:
    #   -Portfolio; stocks are either incremented or newly added to the portfolio
    # RAISES: None
    def buy_shares(self, shares_requested : tuple[str, int]) -> None:

        t, q = shares_requested


        if (self.has_stock(t)):
            self.stocks[t].increment_quantity(q)
        else:
            self.stocks[t] = Stock(ticker=t, quantity=q)


    # INPUT:
    #   -shares_requested(tuple[str,int]); a request for a ticker and quantity of stocks
    # OUTPUT: None
    # PRECONDITION:
    #   -shares_requested; ticker exists in portfolio, quantity does not exceed current holdings
    # POSTCONDITION:
    #   -Portfolio; stock quantity is decremented, and if 0 deleted from portfolio
    # RAISES: None
    def sell_shares(self, shares_requested : tuple[str, int]) -> None:

        t, q = shares_requested


        self.stocks[t].decrement_quantity(q)

        if (self.stocks[t].quantity == 0):
            del self.stocks[t]

