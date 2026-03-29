import matplotlib.pyplot as plt
import pandas as pd


# PURPOSE:
#   -Visualizer provides a data visualization abstraction
#   -provides a isolated layer that allows for construction of data charts
class Visualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        
    # INPUT:
    #   -portfolio_data(list[dict[str|int]]); formatted portfolio data
    # OUTPUT: None
    # PRECONDITION:
    #   -portfolio_data; non-empty, each dict contains 'ticker'(str) and 'quantity'(int)
    # POSTCONDITION:
    #   -process; a pie chart is displayed with stock data distributions does not block program execution
    # RAISES: None
    def display_pie_chart(self, portfolio_data : list[dict[str, str | int]]) -> None:


        # TODO: use pandas to format the data
        # TODO: use matplotlib to display the data

        
        plt.show(block=False) #Displays chart doesnt block program

    
    # INPUT: None
    # OUTPUT: None
    # PRECONDITION:
    #   -process; current process has a chart displayed
    # POSTCONDITION:
    #   -process; chart is closed
    # RAISES: None
    def close_chart(self) -> None:
        plt.close(self.fig)
            