from stock import Stock

class Portfolio:
    def __init__(self, name, stocks : dict[str, Stock]):
        self.id = None
        self.name = name
        self.stocks = stocks

    def portfolio_has_stock(self, ticker):
        return ticker in self.stocks

    def add_stock(self, stock_dat):
        t, q = stock_dat
        
        if(self.portfolio_has_stock(t)):
            self.stocks[t].increment_quantity(q)
        else:
            self.stocks[t] = Stock(ticker = t, quantity = q)
            return "added"

    def remove_stock(self, stock_dat):
        t, q = stock_dat

        self.stocks[t].decrement_quantity(q)
        
        if(self.stocks[t].quantity == 0):
            del self.stocks[t]
            return "removed"
