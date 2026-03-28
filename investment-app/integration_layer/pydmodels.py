from pydantic import BaseModel


# PURPOSE:
#   -LogoutRequest provides a serializable abstraction for logout data
#   -structures the HTTP request body for the /logout endpoint
class LogoutRequest(BaseModel):
    session_id: str


# PURPOSE:
#   -CredsRequest provides a serializable abstraction for credentials
#   -structures the HTTP request body for the /register and /login endpoints
class CredsRequest(BaseModel):
    login: str
    password: str


# PURPOSE:
#   -FundsRequest provides a serializable abstraction for funds deposit data
#   -structures the HTTP request body for the /fund endpoint
class FundsRequest(BaseModel):
    session_id: str
    funds_requested: float


# PURPOSE:
class PortfolioRequest(BaseModel):
    session_id: str
    name: str


# PURPOSE:
class TransactionRequest(BaseModel):
    session_id: str
    portfolio_name: str
    ticker: str
    quantity: int


# PURPOSE:
class StockData(BaseModel):
    ticker: str
    quantity: int


# PURPOSE:
class PortfolioData(BaseModel):
    name: str
    stocks: dict[str, StockData]


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    # RAISES:
    @classmethod
    def convert(cls, portfolio):
        
        stocks = {}

        for ticker, stock in portfolio.stocks.items():
            stocks[ticker] = StockData(ticker = ticker, quantity = stock.quantity)

        return cls(name = portfolio.name, stocks = stocks)
       

# PURPOSE:
class UserData(BaseModel):
    login: str
    balance: float
    portfolios: dict[str, PortfolioData]


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    # RAISES:
    @classmethod
    def convert(cls, user):

        portfolios = {}

        for name, portfolio in user.portfolios.items():
            portfolios[name] = PortfolioData.convert(portfolio)
        
        return cls(login = user.login, balance = user.balance, portfolios = portfolios)