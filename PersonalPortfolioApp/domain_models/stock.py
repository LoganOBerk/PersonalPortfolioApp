# PURPOSE:
class Stock:

    def __init__(self, id=None, *, ticker, quantity):
        self.id = id
        self.ticker = ticker
        self.quantity = quantity


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def increment_quantity(self, inc_amt : int) -> None:
        self.quantity += inc_amt


    # INPUT:
    # OUTPUT:
    # PRECONDITION:
    # POSTCONDITION:
    def decrement_quantity(self, dec_amt : int) -> None:
        self.quantity -= dec_amt