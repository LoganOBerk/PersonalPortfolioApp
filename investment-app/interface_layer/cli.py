from common.errors import ServiceError

# PURPOSE: 
#   -Cli provides a user interaction abstraction
#   -Handles all user interaction and enforces program control flow
class Cli:
    def __init__(self, service, validator, visualizer):
        self.user_account = None
        self.serv = service
        self.validator = validator
        self.vis = visualizer


    # INPUT: None
    # OUTPUT: None
    # PRECONDITION:
    #   -Cli; user_account is None, all dependencies are injected and constructed
    # POSTCONDITION:
    #   -terminal; initial startup menu is displayed
    # RAISES: None
    def execute(self) -> None:
        self.display_startup_menu()


    # INPUT: None
    # OUTPUT: None
    # PRECONDITION: None
    # POSTCONDITION:
    #   -self.user_account; is None
    #   -Cli; user is navigated to selected menu or app is exited
    # RAISES: None
    def display_startup_menu(self) -> None:
        while True:
            selection = 0
            self.user_account = None

            # TODO: Welcome menu display
            # TODO: Display selection options
            # TODO: Selection input receiver

            if selection == 1:
                self.display_account_credential_gatherer(new=True)
                continue
            elif selection == 2:
                self.display_account_credential_gatherer(new=False)
            elif selection == 3:
                self.serv.exit_app()
            else:
                # TODO: invalid selection error msg
                continue

            self.display_user_dashboard(self.user_account)


    # INPUT: 
    #   -new(bool); True if creating a new account, False if logging in
    # OUTPUT: None
    # PRECONDITION:
    #   -new; True or False
    # POSTCONDITION:
    #   -self.user_account; if confirmed, see Service.create_account() or Service.find_account() POSTCONDITION, otherwise unchanged
    #   -Cli; if new return to the startup menu, otherwise display user dashboard
    # RAISES: None  
    def display_account_credential_gatherer(self, new : bool) -> None:

        valid = False

        while True:
            # TODO: Login/Signup menu display
            # TODO: Credential input receiver (login & password)

            creds = login, password

            valid = self.validator.account_validator(creds, new)

            if valid:
                break

            # TODO: invalid credentials error msg


        while True:
            selection = 0

            # TODO: Display selection options
            # TODO: Selection input receiver

            if selection == 1:
                try:

                    if new:
                        self.user_account = self.serv.create_account(creds)
                        # TODO: Msg that indicates a action was successfully performed
                    else:
                        self.user_account = self.serv.find_account(login)

                except ServiceError as e:
                    print(f"ERROR: {e}")
                    continue
                    
            elif selection != 2:
                # TODO: invalid selection error msg
                continue

            return


    # INPUT:
    #   -user_account(User); current user account
    # OUTPUT: None
    # PRECONDITION:
    #   -user_account; user account is fully populated and up to date
    # POSTCONDITION:
    #   -Cli; user is navigated to selected menu, logged out, or app is exited
    # RAISES: None 
    def display_user_dashboard(self, user_account) -> None:

        while True:
            selection = 0
            numPortfolios = len(user_account.portfolios)

            # TODO: User dashboard display
            # TODO: Display selection options
            # TODO: Selection input receiver

            portfolio_list = list(user_account.portfolios.values())

            if 0 < selection <= numPortfolios:
                r = self.display_portfolio_contents(portfolio_list[selection - 1])
                if r == "logout":
                    return
            elif selection == numPortfolios + 1:
                self.display_funding_menu(user_account)
            elif selection == numPortfolios + 2:
                self.display_portfolio_modification_menu(user_account, create = True)
            elif selection == numPortfolios + 3:
                self.display_portfolio_modification_menu(user_account, create = False)
            elif selection == numPortfolios + 4:
                return
            elif selection == numPortfolios + 5:
                self.serv.exit_app()
            else:
                # TODO: invalid selection error msg
                pass  # Remove this once you implement

    
    # INPUT: 
    #   -user_account(User); current user account
    # OUTPUT: None
    # PRECONDITION:
    #   -user_account; user account is fully populated and up to date
    # POSTCONDITION:
    #   -user_account; if confirmed see Service.fund_account() POSTCONDITION, otherwise unchanged
    #   -Cli; return to user dashboard
    # RAISES: None
    def display_funding_menu(self, user_account) -> None:

        valid = False

        while True :
            # TODO: Account Funding display
            # TODO: Funds input reciever

            funds_request = funds_request

            valid = self.validator.fund_validator(user_account.balance, funds_request)

            if valid:
                break

            # TODO: invalid funds error msg

        while True:
            selection = 0

            # TODO: Display selection options
            # TODO: Selection input receiver

            if selection == 1:
                try:

                    self.serv.fund_account(user_account, funds_request)
                    # TODO: Msg that indicates a action was successfully performed

                except ServiceError as e:
                    print(f"ERROR: {e}")
                    continue
            elif selection != 2:
                # TODO: invalid selection error msg
                continue

            return

    # INPUT:
    #   -user_account(User); current user account
    #   -create(bool); True if creating a new portfolio, False if removing one
    # OUTPUT: None
    # PRECONDITION:
    #   -user_account; user account is fully populated and up to date
    #   -create; True or False
    # POSTCONDITION:
    #   -user_account; if confirmed see Service.create_portfolio() or Service.remove_portfolio() POSTCONDITION, otherwise unchanged
    #   -Cli; return to user dashboard
    # RAISES: None
    def display_portfolio_modification_menu(self, user_account, create : bool) -> None:

        valid = False

        while True:
            # TODO: Portfolio creation display
            # TODO: Portfolio name input receiver

            name_request = name_request

            valid = self.validator.portfolio_validator(user_account, name_request, create)

            if valid:
                break

            # TODO: invalid name error msg


        while True:
            selection = 0

            # TODO: Display selection options
            # TODO: Selection input receiver

            if selection == 1:
                try:

                    if(create):
                        self.serv.create_portfolio(user_account, name_request)
                        # TODO: Msg that indicates a action was successfully performed
                    else:
                        self.serv.remove_portfolio(user_account, name_request)
                        # TODO: Msg that indicates a action was successfully performed

                except ServiceError as e:
                    print(f"ERROR: {e}")
                    continue
            elif selection != 2:
                # TODO: invalid selection error msg
                continue

            return


    # INPUT: 
    #   -portfolio(Portfolio); a user portfolio
    # OUTPUT:
    #   -return(str | None); "logout" if user wishes to log out, otherwise None
    # PRECONDITION:
    #   -portfolio; user portfolio is fully populated and up to date 
    # POSTCONDITION:
    #   -Cli; user is navigated to selected menu, logged out or app is exited
    # RAISES: None
    def display_portfolio_contents(self, portfolio) -> str | None:
        while True:
            selection = 0
            packaged_data = self.serv.package_portfolio_data(portfolio)
            
            self.vis.display_pie_chart(packaged_data)

            # TODO: Portfolio contents display
            # TODO: Display selection options
            # TODO: Selection input receiver

            self.vis.close_chart()

            if selection == 1:
                self.display_stock_transaction_menu(portfolio, purchase=True)
            elif selection == 2:
                self.display_stock_transaction_menu(portfolio, purchase=False)
            elif selection == 3:
                return
            elif selection == 4:
                return "logout"
            elif selection == 5:
                self.serv.exit_app()
            else:
                # TODO: invalid selection error msg
                pass  # Remove this once you implement
           
            


    # INPUT:
    #   -portfolio(Portfolio); a user portfolio
    #   -purchase(bool); True if purchasing a stock, False if selling
    # OUTPUT: None
    # PRECONDITION:
    #   -portfolio; user portfolio is fully populated and up to date 
    #   -purchase; True or False
    #   -self.user_account; user account is fully populated and up to date
    # POSTCONDITION:
    #   -portfolio; if confirmed see Service.execute_buy() or Service.execute_sell() POSTCONDITION, otherwise unchanged
    #   -Cli; return to portfolio menu
    # RAISES: None 
    def display_stock_transaction_menu(self, portfolio, purchase : bool) -> None:

        while True:
            # TODO: Transaction menu display
            # TODO: shares_requested input receiver (ticker & quantity)

            shares_requested = ticker, quantity

            valid = self.validator.stock_ticker_validator(portfolio, ticker, purchase)
            if not valid:
                # TODO: invalid ticker error msg
                continue

            valid = self.validator.stock_quantity_validator(portfolio, shares_requested, purchase)
            if not valid:
                # TODO: invalid quantity error msg
                continue

            valid = self.validator.sufficient_balance_validator(self.user_account.balance, shares_requested, purchase)
            if not valid:
                # TODO: invalid selection error msg
                continue

            break


        while True:
            selection = 0

            # TODO: Display selection options
            # TODO: Selection input receiver

            if selection == 1:

                try:

                    if purchase:
                        self.serv.execute_buy(self.user_account, portfolio, shares_requested)
                        # TODO: Msg that indicates a action was successfully performed
                    else:
                        self.serv.execute_sell(self.user_account, portfolio, shares_requested)
                        # TODO: Msg that indicates a action was successfully performed

                except ServiceError as e:
                    print(f"ERROR: {e}")
                    continue

            elif selection != 2:
                # TODO: invalid selection error msg
                continue

            return