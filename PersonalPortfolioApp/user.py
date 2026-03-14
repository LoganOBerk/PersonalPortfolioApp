from portfolio import Portfolio

class User:
    def __init__(self, login, password, balance, portfolios : dict[str, Portfolio]):
        self.id = None
        self.login = login
        self.password = password
        self.balance = balance
        self.portfolios = portfolios

    def add_portfolio(self, portfolio_dat):
        n, s = portfolio_dat
        self.portfolios[n] = Portfolio(name = n, stocks = s)

    def add_funds(self, funds_to_add):
        self.balance += funds_to_add

    def sub_funds(self, funds_to_sub):
        self.balance -= funds_to_sub