import sys
from domain_models import *


# PURPOSE:
class Service:

    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def __init__(self, database):
        self.db = database


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def create_account(self, credentials : tuple[str, str]) -> User:
        # TODO: Add user to the db
        # TODO: Create user and return object
        pass


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def find_account(self, login : str) -> User:
        # TODO: Create, Populate and return user object
        pass


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def fund_account(self, user_account : User, funds_request : float) -> None:
        user_account.add_funds(funds_request)
        #TODO: update db funds
        pass


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def create_portfolio(self, user_account : User, portfolio_name : str) -> None:
        # TODO: add new empty portfolio to user_account object
        user_account.portfolios[portfolio_name].id = self.db.insert_portfolio(user_account.id, portfolio_name)


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def remove_portfolio(self, user_account : User, portfolio_name : str) -> None:
        user_account.remove_portfolio(portfolio_name)
        #TODO: call remove function for removing portfolio from db


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def execute_buy(self, user_account : User, portfolio : Portfolio, shares_requested : tuple[str, int]) -> None:
        # TODO: call api to get stock price
        # TODO: subtract funds from user account
        r = portfolio.buy_shares(shares_requested)
        s_id = r[0]
        flag = r[1]

        if flag == "new":
            portfolio.stocks[shares_requested[0]].id = self.db.insert_stock(portfolio.id, shares_requested)
        else:
            # TODO: update the db
            pass


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def execute_sell(self, user_account : User, portfolio : Portfolio, shares_requested : tuple[str, int]) -> None:
        # TODO: call api to get stock price
        # TODO: add funds to user account
        # TODO: remove the stock(s) from the portfolio
        r = portfolio.sell_shares(shares_requested)
        s_id = r[0]
        flag = r[1]

        if flag == "removed":
            # TODO: remove from the db
            pass
        else:
            # TODO: update the db
            pass

        pass


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def user_exists_in_storage(self, login : str) -> bool:
        u_id = self.db.resolve_user_id(login)
        return u_id != None


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def populate_user(self, user_account : User, login : str) -> None:
        user_info = self.db.pull_user(login)

        user_account.id = user_info[0]
        user_account.login = user_info[1]
        user_account.password = user_info[2]
        user_account.balance = user_info[3]

        self.populate_user_portfolios(user_account.id, user_account.portfolios)


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def populate_user_portfolios(self, user_id : int, portfolios : dict[str, Portfolio]) -> None:
        stored_portfolios = self.db.pull_portfolios(user_id)

        for portfolio in stored_portfolios:

            p_id = portfolio[0]
            p_name = portfolio[1]

            portfolios[p_name] = Portfolio(id=p_id,name=p_name)

            self.populate_portfolio_stocks(p_id, portfolios[p_name].stocks)


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def populate_portfolio_stocks(self, portfolio_id : int, stocks : dict[str, Stock]) -> None:
        stored_stocks = self.db.pull_stocks(portfolio_id)

        for stock in stored_stocks:

            s_id = stock[0]
            s_ticker = stock[1]
            s_quantity = stock[2]

            stocks[s_ticker] = Stock(id=s_id, ticker=s_ticker, quantity=s_quantity)


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    @staticmethod
    def exitApp():
        sys.exit(0)