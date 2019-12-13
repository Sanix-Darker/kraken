from pymongo import MongoClient
import configparser as ConfigParser

# Configs parameters
configParser = ConfigParser.RawConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)

# Filling parameters
DATABASE_HOST = configParser.get('kraken-config', 'DATABASE_HOST')
DATABASE_NAME = configParser.get('kraken-config', 'DATABASE_NAME')


class DATABASE:
    def __init__(self, database_name):
        # creation of MongoClient
        client = MongoClient()
        # Connect with the portnumber and host
        client = MongoClient(DATABASE_HOST)
        # Access database
        self.database_name = database_name
        self.db = client[self.database_name]


def get_db():
    DB = DATABASE(DATABASE_NAME)
    return DB.db
