from .routes import connect
from common.errors import ValidationError


# PURPOSE:
#   -FrontendApi provides a user operation abstraction
#   -This abstraction is provided to enforce function contracts on POST or GET request
class FrontendApi:
    def __init__(self, service, validator):
        self.serv = service
        self.validator = validator
    

    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION/RAISES: see respective .routes connect() fields
    def link_routes(self):
        connect(self)


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION/RAISES: see respective Service.resolve_uid() fields
    def resolve_uid(self, login):
        u_id = self.serv.resolve_uid(login)
        return u_id 


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective Service.create_account() fields
    # RAISES:
    #   -ValidationError; see Validator.account_validator() POSTCONDITION (new=True)
    def create_account(self, credentials):
        valid = self.validator.account_validator(credentials, new=True)

        if not valid:
            raise ValidationError("A user with this login already exists or field was blank")

        return self.serv.create_account(credentials)


    # INPUT:
    #   -credentials(tuple[str,str]); user login and password
    # OUTPUT/PRECONDITION/POSTCONDITION: see respective Service.find_account() fields
    # RAISES:
    #   -ValidationError; see Validator.account_validator() POSTCONDITION (new=False)
    def find_account(self, credentials):
        valid = self.validator.account_validator(credentials, new=False)

        if not valid:
            raise ValidationError("Login/Password are incorrect")

        login = credentials[0]

        return self.serv.find_account(login)


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective Service.fund_account() fields
    # RAISES:
    #   -ValidationError; see Validator.fund_validator() POSTCONDITION
    def fund_account(self, user_account, funds_request):
        valid = self.validator.fund_validator(funds_request)

        if not valid:
            raise ValidationError("Funds to add must be 1-999,999")

        return self.serv.fund_account(user_account, funds_request)


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective Service.create_portfolio() fields
    # RAISES:
    #   -ValidationError; see Validator.portfolio_validator() POSTCONDITION (create=True)
    def create_portfolio(self, user_account, portfolio_name):
        valid = self.validator.portfolio_validator(user_account, portfolio_name, create=True)

        if not valid:
            raise ValidationError("Portfolio already exists or no name entered")

        return self.serv.create_portfolio(user_account, portfolio_name)


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective Service.remove_portfolio() fields
    # RAISES:
    #   -ValidationError; see Validator.portfolio_validator() POSTCONDITION (create=False)
    def remove_portfolio(self, user_account, portfolio_name):
        valid = self.validator.portfolio_validator(user_account, portfolio_name, create=False)

        if not valid:
            raise ValidationError("Portfolio name does not exist")

        return self.serv.remove_portfolio(user_account, portfolio_name)


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective Service.execute_buy() fields
    # RAISES:
    #   -ValidationError; see Validator.stock_ticker_validator() POSTCONDITION (purchase=True)
    #   -ValidationError; see Validator.stock_quantity_validator() POSTCONDITION (purchase=True)
    #   -ValidationError; see Validator.sufficient_balance_validator() POSTCONDITION (purchase=True)
    def execute_buy(self, user_account, portfolio, shares_requested):
        ticker = shares_requested[0]
        purchase = True

        valid = self.validator.stock_ticker_validator(portfolio, ticker, purchase)
        if not valid:
            raise ValidationError("Ticker supplied does not exist")

        valid = self.validator.stock_quantity_validator(portfolio, shares_requested, purchase)
        if not valid:
            raise ValidationError("Quantity requested is too much")

        valid = self.validator.sufficient_balance_validator(user_account.balance, shares_requested, purchase)
        if not valid:
            raise ValidationError("Insufficient balance")

        return self.serv.execute_buy(user_account, portfolio, shares_requested)


    # INPUT/OUTPUT/PRECONDITION/POSTCONDITION: see respective Service.execute_sell() fields
    # RAISES:
    #   -ValidationError; see Validator.stock_ticker_validator() POSTCONDITION (purchase=False)
    #   -ValidationError; see Validator.stock_quantity_validator() POSTCONDITION (purchase=False)
    def execute_sell(self, user_account, portfolio, shares_requested):
        ticker = shares_requested[0]
        purchase = False

        valid = self.validator.stock_ticker_validator(portfolio, ticker, purchase)
        if not valid:
            raise ValidationError("Ticker is not owned")

        valid = self.validator.stock_quantity_validator(portfolio, shares_requested, purchase)
        if not valid:
            raise ValidationError("User has insufficient amount of stock")

        return self.serv.execute_sell(user_account, portfolio, shares_requested)