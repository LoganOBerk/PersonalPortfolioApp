class Stock:
    def __init__(self, ticker, quantity):
        self.id = None
        self.ticker = ticker
        self.quantity = quantity

    def increment_quantity(self, inc_amt):
        self.quantity += inc_amt

    def decrement_quantity(self, dec_amt):
        self.quantity -= dec_amt