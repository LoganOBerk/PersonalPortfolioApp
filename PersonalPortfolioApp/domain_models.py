class User:
    def __init__(self, id = None, *, login, password, balance, portfolios : dict[str, Portfolio] = None):
        self.id = id
        self.login = login
        self.password = password
        self.balance = balance
        self.portfolios = portfolios if portfolios is not None else {}

    def add_portfolio(self, portfolio_dat):
        n, s = portfolio_dat
        self.portfolios[n] = Portfolio(name = n, stocks = s)

    def add_funds(self, funds_to_add):
        self.balance += funds_to_add

    def sub_funds(self, funds_to_sub):
        self.balance -= funds_to_sub

class Portfolio:
    def __init__(self, id = None, *, name, stocks : dict[str, Stock] = None):
        self.id = id
        self.name = name
        self.stocks = stocks if stocks is not None else {}

    def portfolio_has_stock(self, ticker):
        return ticker in self.stocks

    def buy_shares(self, stock_dat):
        flag = ""

        t, q = stock_dat
        
        s_id = None

        if(self.portfolio_has_stock(t)):
            self.stocks[t].increment_quantity(q)
            s_id = self.stocks[t].id
        else:
            self.stocks[t] = Stock(ticker = t, quantity = q)
            flag = "new"

        return s_id, flag

    def sell_shares(self, stock_dat):
        flag = ""

        t, q = stock_dat

        s_id = self.stocks[t].id

        self.stocks[t].decrement_quantity(q)
        
        if(self.stocks[t].quantity == 0):
            del self.stocks[t]
            flag = "removed"

        return s_id, flag 

class Stock:
    def __init__(self, id = None, *, ticker, quantity):
        self.id = id
        self.ticker = ticker
        self.quantity = quantity

    def increment_quantity(self, inc_amt):
        self.quantity += inc_amt

    def decrement_quantity(self, dec_amt):
        self.quantity -= dec_amt