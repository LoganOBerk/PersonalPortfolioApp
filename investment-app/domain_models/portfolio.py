from .stock import Stock

# PURPOSE:
class Portfolio:
    def __init__(self, id=None, *, name, stocks: dict[str, Stock] = None):
        self.id = id
        self.name = name
        self.stocks = stocks if stocks is not None else {}


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def has_stock(self, ticker : str) -> bool:
        return ticker in self.stocks


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def buy_shares(self, shares_requested : tuple[str, int]) -> None:

        t, q = shares_requested


        if (self.has_stock(t)):
            self.stocks[t].increment_quantity(q)
        else:
            self.stocks[t] = Stock(ticker=t, quantity=q)


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def sell_shares(self, shares_requested : tuple[str, int]) -> None:

        t, q = shares_requested


        self.stocks[t].decrement_quantity(q)

        if (self.stocks[t].quantity == 0):
            del self.stocks[t]

