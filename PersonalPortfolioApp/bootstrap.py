import os

from persistence_layer import Database
from service_layer import Service
from validation_layer import Validator
from interface_layer import Cli


class App:
    def __init__(self, testing = False):
        self.db = None
        self.serv = None
        self.val = None
        self.display = None
        self.init(testing = testing)


    def init(self, testing = False):

        if testing:
            self.db = Database(':memory:')
            self.serv = Service(self.db)
            self.val = Validator(self.serv)
            self.display = Cli(self.serv, self.val)
            return


        db_dir = 'AppData'
        db_source = 'app_data.db'

        
        db_path = os.path.join(db_dir, db_source)

        os.makedirs(db_dir, exist_ok = True)
        

        self.db = Database(db_path)
        self.serv = Service(self.db)
        self.val = Validator(self.serv)
        self.display = Cli(self.serv, self.val)

    def run(self):
        self.display.execute()