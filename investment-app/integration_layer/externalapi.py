import yfinance as yf


# PURPOSE: To provide a clean abstraction interface for retrieving live stock data
class ExternalApi:

    # INPUT: string representing a stock ticker
    # OUTPUT: int representing stock price
    # PRECONDITION: stock ticker is a real ticker
    # POSTCONDITION: Non
    @staticmethod
    def get_stock_price(ticker : str) -> int:
        # TODO: Pull stock price data given a ticker
        pass


    # INPUT: string representing a stock ticker
    # OUTPUT: bool representing if the ticker exists
    # PRECONDITION: stock ticker is a valid ticker format
    # POSTCONDITION: None
    @staticmethod
    def does_ticker_exist(ticker : str) -> bool:
        # TODO: Call the api to identify if the ticker actually exists
        pass