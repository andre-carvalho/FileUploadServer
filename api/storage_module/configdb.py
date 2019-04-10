#!/usr/bin/python3
from configparser import ConfigParser
import os

class ConfigDB:

    #constructor
    def __init__(self, filename='db.cfg', section='database'):
        self.filename = filename
        self.section = section

    def get(self):
        
        config_file = (os.path.dirname(__file__) or '.') + '/config/' + self.filename

        # Test if db.cfg exists
        if not os.path.exists(config_file):
            # get connection params from env vars
            host = os.getenv('HOST', 'localhost')
            port = os.getenv('PORT', 5432)
            database = os.getenv('DBNAME', 'deter_beta')
            username = os.getenv('DBUSER', 'postgres')
            password = os.getenv('DBPASS', 'postgres')
            with open(config_file, "w") as configfile:
                print('[database]', file=configfile)
                print("host={}".format(host), file=configfile)
                print("port={}".format(port), file=configfile)
                print("database={}".format(database), file=configfile)
                print("user={}".format(username), file=configfile)
                print("password={}".format(password), file=configfile)

        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(config_file)
    
        # get section, default to database
        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.section, self.filename))
    
        return db