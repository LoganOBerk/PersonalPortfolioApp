from pathlib import Path
from persistence_layer import Database
from service_layer import Service
from validation_layer import Validator
from interface_layer import *


# PURPOSE: To provide a high level initialization method,
# allows for clean dependancy injection and easy swaps between test mode
class App:
    def __init__(self, testing=False):
        self.db = None
        self.serv = None
        self.val = None
        self.display = None
        self.vis = None
        self.init(testing=testing)


    # INPUT: bool to indicate testing status
    # OUTPUT: None
    # PRECONDITION: Default App object is constructed
    # POSTCONDITION: App is initialized based on the testing bool,
    # dependancies are properly injected 
    def init(self, testing=False) -> None:
        if testing:
            db_path = ':memory:'
        else:
            db_path = self.establish_path('investment-app.db')
        
        
        self.db = Database(db_path)
        self.serv = Service(self.db)
        self.vis = Visualizer()
        self.val = Validator(self.serv)
        self.display = Cli(self.serv, self.val, self.vis)


    # INPUT: 
    # OUTPUT:
    # PRECONDITION: 
    # POSTCONDITION:
    def establish_path(self, db_source : str) -> Path:
        base_dir = Path(__file__).parent

        db_dir = base_dir / 'app_data'

        db_dir.mkdir(exist_ok = True)

        return db_dir / db_source


    # INPUT: None
    # OUTPUT: None
    # PRECONDITION: App object is correctly initialized with proper dependancies
    # POSTCONDITION: The application starts running
    def run(self) -> None:
        self.display.execute()


if __name__ == "__main__" :
    app = App(testing = True)
    app.run()